"""Tiny Chrome DevTools Protocol driver for recording the real dashboard (no Playwright/Selenium needed).

Launches headless Chrome at a 1280x720 CSS viewport with a 1.5 device scale factor, so every screencast frame is a
crisp 1920x1080 picture of the live app. Frames arrive as the page repaints (60+ per second during motion) and are
written to disk as JPEGs with their arrival time, so the video shows the app's own animations, scrolling and hover
states exactly as a visitor sees them. Nothing is injected into the page except scroll / mouse input.
"""
from __future__ import annotations

import asyncio
import base64
import json
import shutil
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

import websockets

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
CSS_W, CSS_H, SCALE = 1280, 720, 1.5


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    raise SystemExit("Chrome or Edge not found; edit CHROME_CANDIDATES in demo/cdp.py")


class Browser:
    def __init__(self, port: int = 9333) -> None:
        self.port = port
        self.proc: subprocess.Popen | None = None
        self.ws = None
        self._id = 0
        self._pending: dict[int, asyncio.Future] = {}
        self._reader: asyncio.Task | None = None
        self._profile = tempfile.mkdtemp(prefix="fs-demo-")
        self.rec_dir: Path | None = None       # set while recording
        self.rec_t0 = 0.0
        self.frames: list[tuple[float, str]] = []   # (seconds since rec start, file name)
        self.mouse = (CSS_W / 2, CSS_H / 2)
        self.track: list[tuple[float, float, float]] = []   # (t, x, y) of the synthetic mouse while recording
        self.clicks: list[tuple[float, float, float]] = []

    async def start(self) -> None:
        self.proc = subprocess.Popen(
            [find_chrome(), "--headless=new", f"--remote-debugging-port={self.port}", f"--user-data-dir={self._profile}",
             "--hide-scrollbars", "--no-first-run", "--disable-extensions", f"--window-size={CSS_W},{CSS_H}",
             "--remote-allow-origins=*", f"--force-device-scale-factor={SCALE}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tabs = None
        for _ in range(60):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json"))
                break
            except Exception:
                time.sleep(0.2)
        if not tabs:
            raise RuntimeError("Chrome did not open its debugging port")
        page = next(t for t in tabs if t["type"] == "page")
        self.ws = await websockets.connect(page["webSocketDebuggerUrl"], max_size=None)
        self._reader = asyncio.ensure_future(self._read())
        await self.send("Page.enable")
        await self.send("Runtime.enable")
        await self.send("Emulation.setDeviceMetricsOverride", width=CSS_W, height=CSS_H, deviceScaleFactor=SCALE, mobile=False)

    async def close(self) -> None:
        if self._reader:
            self._reader.cancel()
        if self.ws:
            await self.ws.close()
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        shutil.rmtree(self._profile, ignore_errors=True)

    async def send(self, method: str, **params):
        self._id += 1
        fut = asyncio.get_event_loop().create_future()
        self._pending[self._id] = fut
        await self.ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        return await fut

    async def _read(self) -> None:
        async for raw in self.ws:
            msg = json.loads(raw)
            if "id" in msg and msg["id"] in self._pending:
                self._pending.pop(msg["id"]).set_result(msg.get("result") or msg.get("error"))
            elif msg.get("method") == "Page.screencastFrame":
                p = msg["params"]
                if self.rec_dir is not None:
                    t = time.perf_counter() - self.rec_t0
                    name = f"f{len(self.frames):06d}.jpg"
                    (self.rec_dir / name).write_bytes(base64.b64decode(p["data"]))
                    self.frames.append((t, name))
                asyncio.ensure_future(self.send("Page.screencastFrameAck", sessionId=p["sessionId"]))

    # ------------------------------------------------------------------ page helpers
    async def js(self, expression: str):
        r = await self.send("Runtime.evaluate", expression=expression, returnByValue=True, awaitPromise=True)
        return (r.get("result") or {}).get("value")

    async def goto(self, url: str, wait: float = 1.0) -> None:
        await self.send("Page.navigate", url=url)
        for _ in range(100):
            if await self.js("document.readyState") == "complete":
                break
            await asyncio.sleep(0.1)
        await asyncio.sleep(wait)

    async def rect(self, selector: str, index: int = 0, text: str | None = None):
        """Viewport rect [x, y, w, h] (CSS px) of the index-th match (optionally containing `text`), or None."""
        flt = (f".filter(e => (e.innerText || e.textContent || '').toLowerCase().includes({json.dumps(text.lower())}))" if text else "")
        return await self.js(
            f"(() => {{ const e = [...document.querySelectorAll({json.dumps(selector)})]{flt}[{index}]; if (!e) return null; "
            "const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height]; })()")

    async def rect_text(self, text: str, root: str = "body"):
        """Rect of the SMALLEST visible element under `root` whose text contains `text` (case-insensitive), or None."""
        return await self.js(
            "(() => { const T = %s.toLowerCase(); let best = null, area = 1e15; for (const e of document.querySelectorAll(%s)) { "
            "const tx = (e.innerText || e.textContent || '').toLowerCase(); if (!tx.includes(T)) continue; const r = e.getBoundingClientRect(); "
            "if (r.width < 2 || r.height < 2) continue; const a = r.width * r.height; if (a < area) { area = a; best = r; } } "
            "return best ? [best.x, best.y, best.width, best.height] : null; })()" % (json.dumps(text), json.dumps(root + " *")))

    async def scroll_y(self) -> float:
        return float(await self.js("window.scrollY") or 0)

    async def scroll_to(self, y: float, seconds: float = 1.2) -> None:
        """Eased scroll driven from here (requestAnimationFrame in the page), so the speed is the same on every run."""
        await self.js(
            "(() => { const y0 = window.scrollY, y1 = Math.max(0, Math.min(%f, document.documentElement.scrollHeight - innerHeight)), "
            "T = %f * 1000, t0 = performance.now(); return new Promise(res => { const step = now => { const k = Math.min(1, (now - t0) / T); "
            "const e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; window.scrollTo(0, y0 + (y1 - y0) * e); "
            "k < 1 ? requestAnimationFrame(step) : res(true); }; requestAnimationFrame(step); }); })()" % (y, seconds))

    async def scroll_to_el(self, selector: str, seconds: float = 1.2, offset: float = 90, index: int = 0, text: str | None = None) -> None:
        r = await self.rect(selector, index, text)
        if r:
            await self.scroll_to(await self.scroll_y() + r[1] - offset, seconds)

    async def move_mouse(self, x: float, y: float, seconds: float = 0.6) -> None:
        x0, y0 = self.mouse
        steps = max(2, int(seconds * 60))
        for i in range(1, steps + 1):
            k = i / steps
            e = 4 * k * k * k if k < .5 else 1 - pow(-2 * k + 2, 3) / 2
            cx, cy = x0 + (x - x0) * e, y0 + (y - y0) * e
            await self.send("Input.dispatchMouseEvent", type="mouseMoved", x=cx, y=cy)
            if self.rec_dir is not None:
                self.track.append((self.now(), cx, cy))
            await asyncio.sleep(seconds / steps)
        self.mouse = (x, y)

    async def hover(self, selector: str, index: int = 0, text: str | None = None, seconds: float = 0.6) -> bool:
        r = await self.rect(selector, index, text)
        if not r:
            return False
        await self.move_mouse(r[0] + r[2] / 2, r[1] + r[3] / 2, seconds)
        return True

    async def click(self, selector: str, index: int = 0, text: str | None = None, seconds: float = 0.6) -> bool:
        if not await self.hover(selector, index, text, seconds):
            return False
        x, y = self.mouse
        await asyncio.sleep(0.15)
        if self.rec_dir is not None:
            self.clicks.append((self.now(), x, y))
        await self.send("Input.dispatchMouseEvent", type="mousePressed", x=x, y=y, button="left", buttons=1, clickCount=1)
        await self.send("Input.dispatchMouseEvent", type="mouseReleased", x=x, y=y, button="left", buttons=0, clickCount=1)
        return True

    # ------------------------------------------------------------------ recording
    async def start_recording(self, out_dir: Path) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in out_dir.glob("*.jpg"):
            f.unlink()
        self.frames = []
        self.track = [(0.0, *self.mouse)]
        self.clicks = []
        self.rec_dir = out_dir
        self.rec_t0 = time.perf_counter()
        await self.send("Page.startScreencast", format="jpeg", quality=93, maxWidth=1920, maxHeight=1080, everyNthFrame=1)

    def now(self) -> float:
        return time.perf_counter() - self.rec_t0

    async def stop_recording(self) -> list[tuple[float, str]]:
        await self.send("Page.stopScreencast")
        await asyncio.sleep(0.2)
        frames, self.rec_dir = self.frames, None
        return frames
