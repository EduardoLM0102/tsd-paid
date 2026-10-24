"""Transcribe every recording in <dir>/audio/ locally with faster-whisper. Nothing leaves the machine.

  python transcribe.py <dir> [--model small.en]

<dir> = the client folder pull_calls.py / pull_lsa.py wrote (e.g. _pessoal/call-wins/kings-window).
Writes <dir>/transcripts.json  {"<call or lead id>": "[0:03] text\n[0:09] text ..."}
Saves after every file and skips ids already transcribed, so it can be stopped and re-run.
First run downloads the model (~500 MB, cached in ~/.cache/huggingface). CPU only, roughly 2-4x faster than real time."""
import argparse, glob, json, os, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("--model", default="small.en", help="small.en (default) / medium.en (better names, ~3x slower)")
a = ap.parse_args()

try:
    from faster_whisper import WhisperModel
except ImportError:
    sys.exit("faster-whisper missing: python -m pip install -r .claude/skills/call-wins/requirements.txt")

out_fn = os.path.join(a.dir, "transcripts.json")
done = json.load(open(out_fn, encoding="utf-8")) if os.path.exists(out_fn) else {}
todo = [f for f in sorted(glob.glob(os.path.join(a.dir, "audio", "*.mp3")))
        if os.path.splitext(os.path.basename(f))[0] not in done]
print(f"{len(done)} already transcribed, {len(todo)} to go", flush=True)
if not todo:
    sys.exit()

model = WhisperModel(a.model, device="cpu", compute_type="int8")
for i, fn in enumerate(todo, 1):
    cid = os.path.splitext(os.path.basename(fn))[0]
    t0 = time.time()
    try:
        segs, _ = model.transcribe(fn, beam_size=5, vad_filter=True)
        done[cid] = "\n".join(f"[{int(s.start) // 60}:{int(s.start) % 60:02d}] {s.text.strip()}" for s in segs)
    except Exception as e:
        print(f"  {cid} FAILED: {e}", flush=True)
        continue
    json.dump(done, open(out_fn, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  [{i}/{len(todo)}] {cid}  {time.time() - t0:.0f}s", flush=True)
print(f"DONE -> {out_fn}")
