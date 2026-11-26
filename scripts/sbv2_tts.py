#!/usr/bin/env python3
"""日本語の合成音声（Style-Bert-VITS2）。AivisSpeech と同じ仕組みで、AivisHub の声（AIVM）と Hugging Face の声を使う。

使い方：
  python scripts/sbv2_tts.py prepare <声の名前...>        声のモデルと BERT を取ってくる（1回だけ。保存先は SBV2_MODELS）
  python scripts/sbv2_tts.py batch <声の名前> <jobs.json>  まとめて合成する（jobs.json は [{"text":..., "out":..., "speed":...}, ...]）
  python scripts/sbv2_tts.py one <声の名前> <テキスト> <出力.wav> [速さ]

声の定義は video/voices.yaml（engine: sbv2）。
  source: aivishub:<モデルのUUID>                              AivisHub（https://hub.aivis-project.com）から AIVM を取る
  source: hf:<repo>/<folder>/<weights.safetensors>              Hugging Face から3ファイル（重み、config.json、style_vectors.npy）を取る
  style / style_weight / sdp / noise / noise_w / assist         話し方の調子（省略可）

モデルの読み込みに数秒〜十数秒かかるので、動画1本分の文はまとめて（batch）合成する。
"""
import base64
import io
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = Path(os.environ.get("SBV2_MODELS", str(ROOT / "sbv2_models")))
BERT = "ku-nlp/deberta-v2-large-japanese-char-wwm"


def roster():
    import yaml
    vs = yaml.safe_load((ROOT / "video" / "voices.yaml").read_text(encoding="utf-8"))["voices"]
    return {v["name"]: v for v in vs if v.get("engine") == "sbv2"}


def model_dir(voice):
    d = MODELS / voice["name"]
    return d if (d / "model.safetensors").exists() and (d / "config.json").exists() and (d / "style_vectors.npy").exists() else None


def fetch(voice):
    """声のモデルを取ってきて、Style-Bert-VITS2 が読む3ファイル（model.safetensors、config.json、style_vectors.npy）にそろえる"""
    d = MODELS / voice["name"]
    if model_dir(voice):
        return d
    d.mkdir(parents=True, exist_ok=True)
    kind, _, rest = voice["source"].partition(":")
    if kind == "aivishub":
        import numpy as np
        from safetensors import safe_open
        from safetensors.torch import load_file, save_file
        aivm = d / "model.aivm"
        if not aivm.exists():
            url = f"https://api.aivis-project.com/v1/aivm-models/{rest}/download?model_type=AIVM"
            print(f"  取得：{voice['name']} ← AivisHub")
            urllib.request.urlretrieve(url, aivm)
        with safe_open(str(aivm), "np") as f:
            md = f.metadata()
        (d / "config.json").write_text(md["aivm_hyper_parameters"], encoding="utf-8")
        np.save(d / "style_vectors.npy", np.load(io.BytesIO(base64.b64decode(md["aivm_style_vectors"]))))
        save_file(load_file(str(aivm)), str(d / "model.safetensors"))   # メタデータ無しで保存し直す
        man = json.loads(md["aivm_manifest"])
        (d / "manifest.json").write_text(json.dumps({k: man.get(k) for k in ("name", "creators", "license")}, ensure_ascii=False, indent=1), encoding="utf-8")
        aivm.unlink()
    elif kind == "hf":
        import shutil
        from huggingface_hub import hf_hub_download
        repo_owner, repo_name, folder, weights = rest.split("/", 3)
        repo = f"{repo_owner}/{repo_name}"
        print(f"  取得：{voice['name']} ← Hugging Face {repo}")
        for src, dst in ((weights, "model.safetensors"), ("config.json", "config.json"), ("style_vectors.npy", "style_vectors.npy")):
            shutil.copy(hf_hub_download(repo, f"{folder}/{src}"), d / dst)
    else:
        sys.exit(f"source の形が分かりません：{voice['source']}")
    return d


def prepare(names):
    from style_bert_vits2.nlp import bert_models
    from style_bert_vits2.constants import Languages
    bert_models.load_model(Languages.JP, BERT)
    bert_models.load_tokenizer(Languages.JP, BERT)
    vs = roster()
    for n in names or vs.keys():
        fetch(vs[n])
    print("準備できました：", ", ".join(names or vs.keys()))


def load(voice):
    from style_bert_vits2.nlp import bert_models
    from style_bert_vits2.constants import Languages
    from style_bert_vits2.tts_model import TTSModel
    bert_models.load_model(Languages.JP, BERT).float()   # 新しい transformers は半精度で読むことがあるので、単精度にそろえる
    bert_models.load_tokenizer(Languages.JP, BERT)
    d = fetch(voice)
    return TTSModel(model_path=str(d / "model.safetensors"), config_path=str(d / "config.json"), style_vec_path=str(d / "style_vectors.npy"), device="cpu")


def infer(model, voice, text, speed):
    from style_bert_vits2.constants import Languages
    kw = dict(text=text, language=Languages.JP, style=voice.get("style", "ノーマル"), style_weight=float(voice.get("style_weight", 1.0)),
              sdp_ratio=float(voice.get("sdp", 0.5)), noise=float(voice.get("noise", 0.6)), noise_w=float(voice.get("noise_w", 0.8)),
              length=1.0 / float(speed))
    if voice.get("assist"):
        kw.update(assist_text=voice["assist"], assist_text_weight=float(voice.get("assist_weight", 0.7)), use_assist_text=True)
    try:
        return model.infer(**kw)
    except KeyError:   # その調子がモデルに無いときは、最初の調子で
        kw["style"] = list(json.loads((MODELS / voice["name"] / "config.json").read_text(encoding="utf-8"))["data"]["style2id"].keys())[0]
        return model.infer(**kw)


def write_wav(path, sr, audio):
    import numpy as np
    import scipy.io.wavfile as sw
    x = np.clip(audio, -1.0, 1.0) if audio.dtype.kind == "f" else audio
    if x.dtype.kind == "f":
        x = (x * 32767).astype(np.int16)
    sw.write(str(path), sr, x)


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "prepare":
        prepare(sys.argv[2:]); return
    voice = roster()[sys.argv[2]]
    model = load(voice)
    if cmd == "batch":
        jobs = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
        t0 = time.time()
        for j in jobs:
            sr, audio = infer(model, voice, j["text"], j.get("speed", 1.0))
            write_wav(j["out"], sr, audio)
        print(f"  合成 {len(jobs)} 文：{time.time() - t0:.0f}秒")
    elif cmd == "one":
        sr, audio = infer(model, voice, sys.argv[3], float(sys.argv[5]) if len(sys.argv) > 5 else 1.0)
        write_wav(sys.argv[4], sr, audio)
    else:
        sys.exit(f"知らない命令：{cmd}")


if __name__ == "__main__":
    main()
