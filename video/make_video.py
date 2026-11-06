"""Build the narrated walkthrough MP4 from video/slides/ + video/script.json.

In a Codespace (needs internet for the AI voice):
    pip install edge-tts imageio-ffmpeg
    python video/make_slides.py
    python video/make_video.py                 # -> video/out/neuroleak_walkthrough.mp4

Options:
    --voice en-NG-AbeoNeural   (default; Nigerian English, male)  e.g. en-US-GuyNeural, en-GB-RyanNeural
    --rate +0%                 speaking speed, e.g. +5% to shorten
    --silent                   no voice: silent placeholder audio timed from word count (pipeline test)
The finished video must be <= 5 minutes; the script reports the final length.
"""
import argparse
import asyncio
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / "video"


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr[-2000:])
    return p


def duration(ff, path):
    err = subprocess.run([ff, "-i", str(path)], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


async def tts(text, out, voice, rate):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(str(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="en-NG-AbeoNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--silent", action="store_true")
    a = ap.parse_args()
    ff = ffmpeg_exe()
    work = V / "out" / "work"; work.mkdir(parents=True, exist_ok=True)
    items = json.loads((V / "script.json").read_text())
    segs = []
    for i, it in enumerate(items):
        audio = work / f"a{i:02d}.mp3"
        if a.silent:
            secs = max(4, len(it["text"].split()) / 2.6)
            run([ff, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{secs:.2f}", str(audio)])
        else:
            asyncio.run(tts(it["text"], audio, a.voice, a.rate))
        seg = work / f"s{i:02d}.mp4"
        run([ff, "-y", "-loop", "1", "-framerate", "25", "-i", str(V / "slides" / it["slide"]), "-i", str(audio),
             "-af", "apad=pad_dur=0.8", "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-shortest", str(seg)])
        segs.append(seg)
        print(f"slide {i + 1}/{len(items)}: {duration(ff, seg):.1f}s")
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{s.name}'\n" for s in segs))
    out = V / "out" / "neuroleak_walkthrough.mp4"
    run([ff, "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(out)])
    total = duration(ff, out)
    print(f"\n{out}  length {int(total // 60)}:{int(total % 60):02d}  size {out.stat().st_size / 1e6:.1f} MB")
    if total > 300:
        print("WARNING: longer than 5 minutes. Re-run with --rate +8% or shorten video/script.json.")


if __name__ == "__main__":
    main()
