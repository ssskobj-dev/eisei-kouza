"""日本語の合成音声（VOICEVOX）。

使い方：
  python scripts/voicevox_tts.py <話者id> <テキスト> <出力.wav> [速さ] [高さ] [抑揚] [前の間] [後の間]
  python scripts/voicevox_tts.py list       話者と style の一覧

速さ 1.0 が標準。高さ 0.0 が標準（-0.15〜0.15）。抑揚 1.0 が標準（大きいほど起伏が付く）。
前の間・後の間は秒（文の前後に入る無音。0.1 前後）。
"""
import os
import sys

from voicevox_core import VoicevoxCore

core = VoicevoxCore(open_jtalk_dict_dir=os.environ.get("OPEN_JTALK_DICT", "/home/claude/vv/open_jtalk_dic_utf_8-1.11"))
if sys.argv[1] == "list":
    from voicevox_core import METAS
    for m in METAS:
        print(m.name, [(s.name, s.id) for s in m.styles])
else:
    sid = int(sys.argv[1]); text = sys.argv[2]; out = sys.argv[3]
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    pitch = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    intonation = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
    pre = float(sys.argv[7]) if len(sys.argv) > 7 else 0.1
    post = float(sys.argv[8]) if len(sys.argv) > 8 else 0.1
    core.load_model(sid)
    q = core.audio_query(text, sid)
    q.speed_scale = speed
    q.pitch_scale = pitch
    q.intonation_scale = intonation
    q.pre_phoneme_length = pre
    q.post_phoneme_length = post
    open(out, "wb").write(core.synthesis(q, sid))
