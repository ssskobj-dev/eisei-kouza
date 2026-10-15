#!/usr/bin/env python3
"""英語の合成音声（Piper）。英語の動画で使う。

使い方：
  python scripts/piper_tts.py <声のモデルのパス(.onnx)> <テキスト> <出力.wav> [speed]

声のモデルは、環境変数 PIPER_VOICE_DIR のフォルダに置く（<名前>.onnx と <名前>.onnx.json）。
"""
import sys
import wave

from piper import PiperVoice, SynthesisConfig

model, text_, out = sys.argv[1], sys.argv[2], sys.argv[3]
speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
v = PiperVoice.load(model)
syn = SynthesisConfig(length_scale=1.0 / speed)
with wave.open(out, "wb") as w:
    v.synthesize_wav(text_, w, syn_config=syn)
