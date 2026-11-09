"""QA helper: save still frames of a video at given seconds (scaled to 1280 wide).  python demo/qa_frames.py video.mp4 outdir 1.5 4 9"""
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

video, out = sys.argv[1], Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for t in sys.argv[3:]:
    dst = out / f"t{float(t):06.2f}.jpg"
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-ss", t, "-i", video, "-frames:v", "1",
                    "-vf", "scale=1280:-1", "-q:v", "3", str(dst)], check=True)
    print(dst)
