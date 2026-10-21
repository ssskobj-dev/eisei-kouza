#!/usr/bin/env python3
"""英語の合成音声（Piper）。英語の動画で使う。

使い方：
  python scripts/piper_tts.py <声のモデルのパス(.onnx)> <テキスト> <出力.wav> [speed] [noise] [noise_w]

声のモデルは、環境変数 PIPER_VOICE_DIR のフォルダに置く（<名前>.onnx と <名前>.onnx.json）。
speed 1.0 が標準。noise（声の揺らぎ、標準 0.667）と noise_w（長さの揺らぎ、標準 0.8）を少し上げると、平板さが減る。
"""
import sys
import wave

from piper import PiperVoice, SynthesisConfig

model, text_, out = sys.argv[1], sys.argv[2], sys.argv[3]
speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
noise = float(sys.argv[5]) if len(sys.argv) > 5 else 0.667
noise_w = float(sys.argv[6]) if len(sys.argv) > 6 else 0.8
v = PiperVoice.load(model)
syn = SynthesisConfig(length_scale=1.0 / speed, noise_scale=noise, noise_w_scale=noise_w)
with wave.open(out, "wb") as w:
    v.synthesize_wav(text_, w, syn_config=syn)
