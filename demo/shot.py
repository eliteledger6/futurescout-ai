"""Save 1920x1080 screenshots of dashboard pages (uses the recorder's screencast, like the demo video).

    python demo/shot.py out_dir /trading /trading@900 /funds@400       (@N = scroll to N px first)
"""
import asyncio
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cdp import Browser  # noqa: E402


async def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="fs-shot-"))
    b = Browser()
    await b.start()
    try:
        for i, spec in enumerate(sys.argv[2:]):
            path, _, y = spec.partition("@")
            await b.goto("http://localhost:3000" + path, wait=2.5)
            await b.move_mouse(640, 380, 0.05)
            await b.start_recording(tmp)
            await b.scroll_to(float(y or 0) + 1, 0.3)
            await b.scroll_to(float(y or 0), 0.2)
            await asyncio.sleep(1.5)
            frames = await b.stop_recording()
            dst = out / f"shot{i}.jpg"
            if frames:
                shutil.copy(tmp / frames[-1][1], dst)
            print(dst, "frames", len(frames), "| page wider than screen:", await b.js("document.documentElement.scrollWidth > innerWidth"))
    finally:
        await b.close()
        shutil.rmtree(tmp, ignore_errors=True)

asyncio.run(main())
