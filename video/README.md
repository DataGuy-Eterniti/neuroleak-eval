# Walkthrough video

The ≤ 5-minute walkthrough is built from code so it can be regenerated:

- `make_slides.py` renders the slides from the repository's real results (`results/runs.jsonl`, `results/claimed_vs_actual.png`).
- `script.json` holds the narration, one entry per slide.
- `make_video.py` adds an AI voice (Microsoft Edge neural TTS through the `edge-tts` package; the default voice is `en-NG-AbeoNeural`) and joins everything into an MP4.

```bash
pip install edge-tts imageio-ffmpeg
python video/make_slides.py
python video/make_video.py        # writes video/out/neuroleak_walkthrough.mp4 (not committed)
```

The video file itself is hosted externally (link in the main README), as the hackathon rules require.
