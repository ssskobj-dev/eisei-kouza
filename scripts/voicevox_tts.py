import sys, json
from voicevox_core import VoicevoxCore
core = VoicevoxCore(open_jtalk_dict_dir=__import__("os").environ.get("OPEN_JTALK_DICT", "/home/claude/vv/open_jtalk_dic_utf_8-1.11"))
if sys.argv[1] == "list":
    from voicevox_core import METAS
    for m in METAS: print(m.name, [(s.name, s.id) for s in m.styles])
else:
    sid = int(sys.argv[1]); text = sys.argv[2]; out = sys.argv[3]
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    core.load_model(sid)
    q = core.audio_query(text, sid); q.speed_scale = speed
    wav = core.synthesis(q, sid)
    open(out, "wb").write(wav)
