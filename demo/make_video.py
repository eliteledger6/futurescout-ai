"""FUTURESCOUT AI hackathon demo video: a real screen recording of the running app, narrated and captioned.

Run from the repo root while the API (port 8000) and the dashboard (port 3000) are running:

    .venv\\Scripts\\python.exe demo\\make_video.py                 full build (about 10 minutes)
    .venv\\Scripts\\python.exe demo\\make_video.py --skip-record   reuse the recorded takes, re-render only
    .venv\\Scripts\\python.exe demo\\make_video.py --scene 04_report   record + render one scene (silent test clip)

What is real in the video: every app shot is a live recording of the dashboard in headless Chrome (demo/cdp.py):
real pages, real data from the API, the app's own animations, real scrolling, hovering and clicking. The terminal
card shows the actual output of backend/scripts/tamper_demo.py for the report on screen. Added in post, and only
these: the opening and closing cards, section titles, captions, highlight rings, a drawn mouse pointer (headless
Chrome renders none), narration (ElevenLabs, voice Chris, via demo/voice.py) and background music (synthesised here, so copyright-free).

Output: demo/futurescout_hackathon_demo.mp4 (1920x1080, 30 fps, H.264 + AAC), .srt captions and NARRATION.md.
"""
from __future__ import annotations

import argparse
import array
import asyncio
import bisect
import json
import math
import os
import subprocess
import sys
import urllib.request
import wave
from dataclasses import dataclass, field
from pathlib import Path
from typing import Awaitable, Callable, Optional

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cdp import SCALE, Browser  # noqa: E402

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build_v4"
TAKES, AUDIO = BUILD / "takes", BUILD / "audio"
OUT = ROOT / "futurescout_hackathon_demo.mp4"
DASH = os.environ.get("DEMO_DASHBOARD_URL", "http://localhost:3000")
API = os.environ.get("DEMO_API_URL", "http://localhost:8000")
W, H, FPS = 1920, 1080, 30
SR = 44100
LEAD, GAP, TAIL = 0.45, 0.42, 0.85        # seconds: before speech, between sentences, after speech
XF = 0.45                                 # crossfade between shots
MINT, INK, DIM, RED = (0, 236, 151), (240, 243, 242), (150, 160, 156), (255, 110, 100)
FONT_DIR = Path(r"C:\Windows\Fonts")
VOICE = "Chris"                           # ElevenLabs premade voice, chosen by the owner 2026-11-10 (free plan: credit ElevenLabs)
RATE = "el-v8"                            # cache tag for the narration clips


# ============================================================================= script
@dataclass
class Scene:
    key: str
    num: str
    title: str
    lines: list[tuple[str, Optional[str]]]     # (caption, spoken text if different)
    tail: float = TAIL
    # filled in later
    start: float = 0.0
    dur: float = 0.0
    sent: list[tuple[float, float]] = field(default_factory=list)   # scene-local (start, end) of each sentence


SCENES = [
    Scene("01_intro", "", "", [
        ("So here's the question we kept asking: which technology is about to take off, and what's the actual evidence?",
         "So here's the question we kept asking. Which technology is about to take off... and what's the actual evidence?"),
        ("FUTURESCOUT AI answers that with a small team of AI agents, running on NEAR AI Cloud.",
         "FutureScout AI answers that with a small team of AI agents, running on NEAR AI Cloud."),
    ]),
    Scene("02_radar", "01", "Hot-topic radar", [
        ("This is the radar. It follows 54 topics, across nine sectors.", "This is the radar. It follows fifty-four topics, across nine sectors."),
        ("For each one, we count research papers and patent filings. Last year against this year, so far.", None),
        ("That tells you what's heating up right now. Not what was hot last year.", None),
        ("And a paper scout keeps suggesting new topics that are starting to grow.", None),
    ]),
    Scene("03_agents", "02", "The agent team", [
        ("Pick a topic, and the team gets to work.", None),
        ("A chief agent makes the plan. Then the science, patent, risk and X agents run in parallel, on real papers, patents and posts.",
         "A chief agent makes the plan. Then the science, patent, risk and X agents run in parallel... on real papers, real patents, and real posts."),
        ("The market agent follows the evidence to the companies behind it, and reads their SEC filings. Nobody hands it a list.", None),
        ("An AI check keeps the counts on topic. And the risk agent's job is to argue the other side.", None),
        ("Now, here's the part we're proud of: the agents run an economy. The trading agent has to buy each report from the report agent, in NEAR.",
         "Now, here's the part we're proud of. The agents run an economy. The trading agent has to buy each report from the report agent, in NEAR."),
        ("The report agent stakes 70% of what it earns with NEAR AI. Those rewards pay for every agent's models.",
         "The report agent stakes seventy percent of what it earns with NEAR AI. Those rewards pay for every agent's models."),
        ("It keeps the other 30%. And once that passes $200, it funds a second trading agent.",
         "It keeps the other thirty percent. And once that passes two hundred dollars, it funds a second trading agent."),
    ]),
    Scene("04_report", "03", "A research report", [
        ("Let's open one. High bandwidth memory.", None),
        ("The verdict is strong momentum, with a score of 80.", "The verdict is strong momentum, with a score of eighty."),
        ("But look at the confidence: only 50%. Risks lower the confidence, not the score.",
         "But look at the confidence. Only fifty percent. Risks lower the confidence, not the score."),
        ("Research is up 106% this year. Patents, up 81%.", "Research is up a hundred and six percent this year. Patents, up eighty-one."),
    ]),
    Scene("05_companies", "04", "Companies and price check", [
        ("It names the companies behind that evidence, including some smaller ones.", None),
        ("And it checks how far their share prices have already run. That's a risk check. It's never a buy signal.", None),
    ]),
    Scene("05b_scout", "05", "Company scout", [
        ("The company scout goes past the big names, to smaller listed companies behind the patents and papers.", None),
        ("It compares their size, growth and research spending, and ranks the ones to watch.", None),
    ]),
    Scene("06_evidence", "06", "Evidence you can check", [
        ("Open the full report, and everything is there.", None),
        ("Which agents ran, on which model, and what each one cost.", None),
        ("Every finding has a label, and the exact quote from its source.", None),
        ("If a source doesn't back a claim up, a citation guard downgrades it.", None),
    ]),
    Scene("07_seal", "07", "Sealed on NEAR", [
        ("When a report is done, its fingerprint is sealed on NEAR mainnet. The site checks it again on every page load.", None),
        ("Change a single word, and the seal breaks.", None),
        ("Fund decisions and trades get sealed the same way.", None),
    ], tail=2.4),
    Scene("09_funds", "08", "Funds and trading", [
        ("Every topic also gets a paper fund, spread across low, medium and high-risk companies.", None),
        ("Each decision comes with its reasons, and the fund is measured against the S&P 500.",
         "Each decision comes with its reasons, and the fund is measured against the S and P five hundred."),
        ("Then there's real money: a trading agent on a strong model trades tokenized stocks through NEAR Intents.",
         "Then there's real money. A trading agent on a strong model trades tokenized stocks through NEAR Intents."),
        ("Code checks every order first: the budget, the allowed stocks, the price and the cost. Only then does the agent approve its own trade.",
         "Code checks every order first. The budget, the allowed stocks, the price, and the cost. Only then does the agent approve its own trade."),
        ("In shadow mode, it also trades pretend money at real quotes, and explains every choice.", None),
    ]),
    Scene("10_round", "09", "Real money, end to end", [
        ("Here's a real round. The agent wakes up on its own: a new report, a sharp price move, or its daily review.",
         "Here's a real round. The agent wakes up on its own. A new report, a sharp price move, or its daily review."),
        ("Before it can use a report, it has to buy it. It bought three, at about $2 each, paid in NEAR straight from its near.com balance.",
         "Before it can use a report, it has to buy it. It bought three, at about two dollars each, paid in NEAR, straight from its near dot com balance."),
        ("After buying the memory report, it bought Intel, and approved the order itself, once every check had passed.", None),
        ("The report agent staked 70% of what it earned, 1.3 NEAR, with NEAR AI, and kept the rest toward a second trading agent.",
         "The report agent staked seventy percent of what it earned, one point three NEAR, with NEAR AI, and kept the rest toward a second trading agent."),
        ("Every report has a price: $2 to $3, depending on what it cost to make.",
         "Every report has a price. Two to three dollars, depending on what it cost to make."),
    ]),
    Scene("11_market", "10", "Listed on NEAR Agent Market", [
        ("And it's not just our own agent buying. The report agent is listed on NEAR's Agent Market.", None),
        ("Anyone can hire it for $3: give it a topic, and it delivers a sealed report.",
         "Anyone can hire it for three dollars. Give it a topic, and it delivers a sealed report."),
        ("Other trading bots can buy any report through our API too, paid in NEAR and checked on chain.",
         "Other trading bots can buy any report through our A P I too, paid in NEAR, and checked on chain."),
    ]),
    Scene("10_close", "", "", [
        ("That's FUTURESCOUT AI: research you can check.", "That's FutureScout AI. Research you can check."),
        ("Models on NEAR AI Cloud, and every report sealed on NEAR.", None),
        ("Built for the NEAR Hackathon.", None),
    ], tail=2.2),
]


# ============================================================================= small helpers
def get_json(path: str, timeout: int = 60):
    return json.load(urllib.request.urlopen(f"{API}{path}", timeout=timeout))


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    name = {"regular": "segoeui.ttf", "bold": "segoeuib.ttf", "semibold": "seguisb.ttf", "light": "segoeuil.ttf",
            "semilight": "segoeuisl.ttf", "mono": "consola.ttf", "monobold": "consolab.ttf"}[weight]
    path = FONT_DIR / name
    return ImageFont.truetype(str(path if path.exists() else FONT_DIR / "arial.ttf"), size)


def ease(k: float) -> float:
    k = max(0.0, min(1.0, k))
    return 4 * k * k * k if k < 0.5 else 1 - pow(-2 * k + 2, 3) / 2


def env(t: float, t0: float, t1: float, fade_in: float = 0.25, fade_out: float = 0.3) -> float:
    """0..1 visibility of something shown from t0 to t1 with soft edges."""
    if t < t0 or t > t1:
        return 0.0
    return max(0.0, min(1.0, (t - t0) / fade_in, (t1 - t) / fade_out))


def rgba(c: tuple[int, int, int], a: float) -> tuple[int, int, int, int]:
    return (*c, int(255 * max(0.0, min(1.0, a))))


def ffmpeg_exe() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd[:6])} ...\n{r.stderr[-1500:]}")


# ============================================================================= narration (ElevenLabs, demo/voice.py)
def synthesize(items: list[tuple[str, Path]], context: dict[Path, tuple[str, str]]) -> None:
    """Each sentence from ElevenLabs (voice VOICE), with the neighbouring sentences as context so the intonation flows."""
    import wave as _wave
    sys.path.insert(0, str(ROOT))
    import voice as el
    client = el.httpx.Client(headers={"xi-api-key": el.api_key()}, timeout=120)
    vid = el.voice_id(client, VOICE)
    for text, out in items:
        prev, nxt = context.get(out, ("", ""))
        pcm = el.speak(client, vid, text, prev, nxt)
        with _wave.open(str(out), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(pcm)


def read_trimmed(path: Path) -> array.array:
    """Mono 16-bit samples with leading/trailing silence removed (keeps 30 ms each side)."""
    with wave.open(str(path), "rb") as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2 and w.getnchannels() == 1, "unexpected TTS format"
        a = array.array("h")
        a.frombytes(w.readframes(w.getnframes()))
    thr, keep = 260, int(0.03 * SR)
    i = next((k for k, v in enumerate(a) if abs(v) > thr), 0)
    j = next((k for k in range(len(a) - 1, -1, -1) if abs(a[k]) > thr), len(a) - 1)
    return a[max(0, i - keep): min(len(a), j + keep)]


def wav_path(sc: Scene, k: int) -> Path:
    import hashlib
    text = sc.lines[k][1] or sc.lines[k][0]
    return AUDIO / f"{sc.key}_{k}_{hashlib.sha1(f'{RATE}|{text}'.encode()).hexdigest()[:8]}.wav"


def build_narration(scenes: list[Scene], reuse: bool) -> Path:
    items = []
    for sc in scenes:
        for k, (cap, say) in enumerate(sc.lines):
            items.append((say or cap, wav_path(sc, k)))
    context = {p: (items[i - 1][0] if i else "", items[i + 1][0] if i + 1 < len(items) else "") for i, (_, p) in enumerate(items)}
    missing = [(t, p) for t, p in items if not p.exists()]
    if missing:
        synthesize(missing, context)
    clips = {p: read_trimmed(p) for _, p in items}
    t = 0.0
    for sc in scenes:
        sc.start, sc.sent, local = t, [], LEAD
        for k in range(len(sc.lines)):
            d = len(clips[wav_path(sc, k)]) / SR
            sc.sent.append((local, local + d))
            local += d + GAP
        sc.dur = round(local - GAP + sc.tail, 3)
        t += sc.dur
    total = array.array("h", bytes(2 * int(math.ceil(t * SR)) + 2 * SR))
    for sc in scenes:
        for k, (s0, _) in enumerate(sc.sent):
            clip = clips[wav_path(sc, k)]
            off = int((sc.start + s0) * SR)
            total[off: off + len(clip)] = clip
    out = AUDIO / "narration.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(total.tobytes())
    return out


# ============================================================================= music (synthesised, so copyright-free)
def build_music_loop() -> Path:
    """A 32-second seamless loop: a slow four-chord pad (Am9, Fmaj7, C, G6) with a soft plucked pattern. Pure maths."""
    out = AUDIO / "music_loop.wav"
    if out.exists():
        return out
    sr, bar, n_bars = 22050, 8.0, 4
    chords = [(110.0, 164.81, 261.63, 493.88), (87.31, 130.81, 220.0, 329.63), (130.81, 196.0, 329.63, 587.33), (98.0, 146.83, 246.94, 329.63)]
    pattern = (0, 2, 1, 3, 2, 3, 1, 2)
    n = int(sr * bar * n_bars)
    left, right = array.array("h", bytes(2 * n)), array.array("h", bytes(2 * n))
    tau = 2 * math.pi
    sin = math.sin
    for i in range(n):
        t = i / sr
        pos = t / bar
        k = int(pos) % n_bars
        into = (pos - int(pos)) * bar
        weights = [(k, 1.0)]
        if into > bar - 2.0:                       # 2-second equal-power crossfade into the next chord
            x = (into - (bar - 2.0)) / 2.0 * (math.pi / 2)
            weights = [(k, math.cos(x) ** 2), ((k + 1) % n_bars, math.sin(x) ** 2)]
        l = r = 0.0
        for ck, wgt in weights:
            for j, f in enumerate(chords[ck]):
                amp = (0.30, 0.24, 0.17, 0.07)[j] * wgt * (0.82 + 0.18 * sin(tau * (0.07 + 0.013 * j) * t + j))
                l += amp * (sin(tau * f * t) + 0.6 * sin(tau * f * 1.003 * t + 1.1))
                r += amp * (sin(tau * f * t + 0.4) + 0.6 * sin(tau * f * 0.997 * t + 2.0))
        step = int(t / 0.5)
        tt = t - step * 0.5
        note = chords[k][pattern[step % 8]] * 2
        pl = 0.16 * math.exp(-7.0 * tt) * (1 - math.exp(-220.0 * tt)) * sin(tau * note * t)
        pan = 0.35 + 0.3 * ((step % 4) / 3)
        l += pl * (1 - pan) * 2
        r += pl * pan * 2
        left[i] = int(max(-1.0, min(1.0, l * 0.42)) * 30000)
        right[i] = int(max(-1.0, min(1.0, r * 0.42)) * 30000)
    inter = array.array("h", bytes(4 * n))
    inter[0::2], inter[1::2] = left, right
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(inter.tobytes())
    return out


# ============================================================================= cards drawn by code
_BG: Optional[Image.Image] = None


def background() -> Image.Image:
    global _BG
    if _BG is None:
        img = Image.new("RGB", (W, H), (4, 6, 6))
        glow = Image.new("L", (W, H), 0)
        g = ImageDraw.Draw(glow)
        g.ellipse((W * 0.22, H * 0.05, W * 0.78, H * 0.95), fill=70)
        g.ellipse((W * 0.55, H * -0.2, W * 1.1, H * 0.6), fill=34)
        glow = glow.filter(ImageFilter.GaussianBlur(190))
        img.paste(Image.new("RGB", (W, H), (0, 110, 74)), (0, 0), glow)
        d = ImageDraw.Draw(img, "RGBA")
        for x in range(0, W, 96):
            d.line((x, 0, x, H), fill=(255, 255, 255, 7))
        for y in range(0, H, 96):
            d.line((0, y, W, y), fill=(255, 255, 255, 7))
        _BG = img
    return _BG.copy()


def rise(d: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, f, colour, t: float, t0: float, anchor: str = "mm", spacing: float = 0) -> None:
    """Text that fades in and rises 18 px, starting at t0."""
    k = ease((t - t0) / 0.6)
    if k <= 0:
        return
    x, y = xy[0], xy[1] + (1 - k) * 18
    if spacing:
        total = sum(d.textlength(ch, font=f) + spacing for ch in text) - spacing
        cx = x - total / 2
        for ch in text:
            d.text((cx, y), ch, font=f, fill=rgba(colour, k), anchor="lm")
            cx += d.textlength(ch, font=f) + spacing
    else:
        d.text((x, y), text, font=f, fill=rgba(colour, k), anchor=anchor)


def title_card(t: float, dur: float) -> Image.Image:
    img = background()
    d = ImageDraw.Draw(img, "RGBA")
    rise(d, (W / 2, 388), "MULTI-AGENT TECHNOLOGY RESEARCH  ·  SEALED ON NEAR", font(26, "mono"), MINT, t, 0.15, spacing=3)
    rise(d, (W / 2, 520), "FUTURESCOUT AI", font(148, "light"), INK, t, 0.35, spacing=6)
    k = ease((t - 0.8) / 0.7)
    if k > 0:
        d.line((W / 2 - 150 * k, 640, W / 2 + 150 * k, 640), fill=rgba(MINT, 0.9), width=3)
    rise(d, (W / 2, 702), "Find the next hot technology. Show the evidence.", font(44, "semilight"), (200, 208, 205), t, 1.0)
    rise(d, (W / 2, 968), "Product demo  ·  recorded from the live application  ·  NEAR mainnet", font(24, "regular"), DIM, t, 1.5)
    return img


def terminal_card(lines: list[str], command: str) -> Callable[[float, float], Image.Image]:
    def render(t: float, dur: float) -> Image.Image:
        img = background()
        d = ImageDraw.Draw(img, "RGBA")
        x0, y0, x1, y1 = 150, 120, W - 150, H - 230
        d.rounded_rectangle((x0, y0, x1, y1), radius=20, fill=(9, 12, 11, 245), outline=(52, 60, 57, 255), width=2)
        for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
            d.ellipse((x0 + 30 + i * 32, y0 + 26, x0 + 48 + i * 32, y0 + 44), fill=c)
        d.text((x0 + 150, y0 + 22), "backend  —  real output, read live from NEAR mainnet", font=font(22, "mono"), fill=DIM)
        d.line((x0, y0 + 68, x1, y0 + 68), fill=(40, 47, 45, 255), width=2)
        f, y = font(25, "mono"), y0 + 96
        typed = min(len(command), int(max(0.0, t - 0.25) * 60))
        d.text((x0 + 40, y), "> " + command[:typed] + ("▌" if typed < len(command) and int(t * 4) % 2 == 0 else ""), font=f, fill=MINT)
        y += 48
        t_lines = 0.25 + len(command) / 60 + 0.25
        for i, line in enumerate(lines):
            a = ease((t - (t_lines + i * 0.13)) / 0.25)
            if a <= 0:
                break
            colour = INK
            if "-> match" in line:
                colour = MINT
            elif "MISMATCH" in line:
                colour = RED
            elif line.startswith(("   computed", "   on chain", "  tx:")):
                colour = (190, 198, 195)
            d.text((x0 + 40, y), line[:108], font=f, fill=rgba(colour, a))
            if "MISMATCH" in line and a >= 1:
                pulse = 0.55 + 0.45 * math.sin((t - t_lines) * 5)
                wdt = d.textlength(line, font=f)
                d.rounded_rectangle((x0 + 28, y - 8, x0 + 52 + wdt, y + 40), radius=10, outline=rgba(RED, pulse), width=3)
            y += 37 if line.strip() else 18
        return img
    return render


def closing_card(t: float, dur: float) -> Image.Image:
    img = background()
    d = ImageDraw.Draw(img, "RGBA")
    rise(d, (W / 2, 150), "FUTURESCOUT AI", font(84, "light"), INK, t, 0.1, spacing=4)
    rise(d, (W / 2, 232), "Evidence-first technology research, sealed on NEAR", font(32, "semilight"), (200, 208, 205), t, 0.35)
    cols = [
        (150, "RUNS LIVE TODAY", MINT, [
            "Agent team on NEAR AI Cloud models: chief, science, risk,",
            "market, X, patent, price timing, company scout, investment",
            "Real sources: OpenAlex, arXiv, EPO patents, SEC EDGAR, X",
            "Every quote checked against its source",
            "Reports sold for $2-3 in NEAR, earnings staked for AI",
            "Report agent listed on NEAR Agent Market ($3 a hire)",
        ]),
        (1010, "SIMULATED OR LIMITED", (255, 196, 110), [
            "Topic funds and shadow trades use pretend money",
            "Scores are heuristics: no topic reaches 70% confidence",
            "Agent Market: one free test hire so far, no paid job yet",
            "Stock prices: free plan, 25 lookups a day",
            "Research activity is not commercial success",
            "Real trades: small budget, the agent approves in limits",
        ]),
    ]
    for ci, (x, head, colour, rows) in enumerate(cols):
        t0 = 0.7 + ci * 0.35
        a = ease((t - t0) / 0.5)
        if a <= 0:
            continue
        d.rounded_rectangle((x, 320, x + 760, 800), radius=18, fill=(10, 14, 13, int(225 * a)), outline=rgba((52, 60, 57), a), width=2)
        d.rectangle((x, 344, x + 5, 384), fill=rgba(colour, a))
        d.text((x + 34, 364), head, font=font(24, "mono"), fill=rgba(colour, a), anchor="lm")
        for i, row in enumerate(rows):
            ar = ease((t - (t0 + 0.25 + i * 0.1)) / 0.4)
            d.text((x + 34, 440 + i * 56), row, font=font(27, "regular"), fill=rgba(INK, ar), anchor="lm")
    rise(d, (W / 2, 880), "Built for the NEAR Hackathon", font(28, "semibold"), INK, t, 1.9)
    rise(d, (W / 2, 1052), "Voice generated with ElevenLabs", font(20, "regular"), DIM, t, 2.3)   # free-plan attribution
    return img


# ============================================================================= recorded takes
class Take:
    """Helper passed to a scene's choreography: timing relative to the take, highlights, and the browser."""

    def __init__(self, b: Browser, dur: float, sent: list[float]) -> None:
        self.b, self.dur, self.sent, self.hls = b, dur, sent, []

    async def until(self, seconds: float) -> None:
        wait = min(seconds, self.dur) - self.b.now()
        if wait > 0:
            await asyncio.sleep(wait)

    async def hl(self, rect, seconds: float = 2.6, pad: float = 8) -> None:
        if rect and -50 < rect[1] < 720 and rect[2] > 2:
            x, y, w, h = rect
            self.hls.append({"t0": self.b.now(), "t1": min(self.dur, self.b.now() + seconds), "rect": [x - pad, y - pad, w + 2 * pad, h + 2 * pad]})


def _cut(self: Take) -> None:
    """End every highlight now (call before scrolling: highlights are drawn at fixed screen positions)."""
    now = self.b.now()
    for h in self.hls:
        h["t1"] = min(h["t1"], now)


Take.cut = _cut  # def cut(self)


async def rec_home(k: Take) -> None:
    b = k.b
    await k.until(0.7)
    await b.hover("a.btn, .btn", text="heating up", seconds=0.9)
    await k.until(max(1.9, k.sent[1] + 1.6))
    await k.hl(await b.rect(".topbar-right .pill"), seconds=3.0, pad=6)
    await b.hover(".topbar-right .pill", seconds=0.9)
    await k.until(k.dur - 2.3)
    await b.hover(".radar-strip", seconds=0.8)
    await k.hl(await b.rect(".radar-strip"), seconds=2.0, pad=4)


async def rec_radar(k: Take) -> None:
    b = k.b
    await b.scroll_to(530, 1.3)
    await k.until(k.sent[1] + 0.2)
    th = await b.rect("th", text="this year so far")
    pt = await b.rect("th", text="patents")
    pa = await b.rect("th", text="papers")
    if pa and pt:
        await k.hl([pa[0], pa[1], pt[0] + pt[2] - pa[0], 470], seconds=max(3.0, k.sent[1 + 1] - k.sent[1] - 0.4), pad=4)
    if th:
        await b.move_mouse(th[0] + th[2] / 2, th[1] + 130, 0.9)
    await k.until(k.sent[2] - 0.5)
    await b.click("button.tab", text="semiconductors", seconds=0.8)
    await asyncio.sleep(0.9)
    await b.hover("table.radar-table tbody tr", index=1, seconds=0.7)


async def rec_agents(k: Take) -> None:
    b = k.b
    await b.scroll_to(640, 1.3)
    await b.hover("g.node", text="chief", seconds=0.7)
    await k.until(k.sent[1])
    span = max(2.0, k.sent[2] - k.sent[1] - 0.6)
    names = ["chief", "science", "risk", "patent", "X"]
    for i, name in enumerate(names):
        await k.until(k.sent[1] + span * i / len(names))
        await b.hover("g.node", text=name, seconds=0.55)
    await k.until(k.sent[2] + 0.3)
    await b.hover("g.node", text="market", seconds=0.8)
    await k.until(k.sent[3] - 0.1)
    await b.hover("g.node", text="science", seconds=0.6)
    await b.hover("g.node", text="risk", seconds=0.7)
    await k.until(k.sent[4] + 0.2)
    await b.hover("g.node", text="report agent", seconds=0.7)
    await k.until(k.sent[4] + (k.sent[5] - k.sent[4]) * 0.45)
    await b.hover("g.node", text="trading agent", seconds=0.7)
    await k.until(k.sent[5] + 0.2)
    await b.hover("g.node", text="near ai staking", seconds=0.7)
    await k.until(k.sent[6] + 0.2)
    await b.hover("g.node", text="report agent", seconds=0.6)
    await k.until(k.sent[6] + (k.dur - k.sent[6]) * 0.4)
    await b.hover("g.node", text="trading agent 2", seconds=0.8)


async def rec_report(k: Take) -> None:
    b = k.b
    await k.until(k.sent[1] - 0.1)
    await k.hl(await b.rect(".rv-gauge") or await b.rect(".rv-banner"), seconds=min(3.0, k.sent[2] - k.sent[1] - 1.2), pad=10)
    await b.hover(".rv-headline", seconds=0.8)
    await k.until(k.sent[2] - 1.25)
    await b.scroll_to_el(".rv-tiles", 1.1, offset=150)
    await k.until(k.sent[2] + 0.1)
    conf = await b.rect_text("Confidence", root=".rv-tiles")
    tile = await b.rect(".rv-tile", 3)
    await k.hl(tile or conf, seconds=max(2.4, k.sent[3] - k.sent[2] - 0.5))
    await b.hover(".rv-tile", 3, seconds=0.7)
    await k.until(k.sent[3] + 0.1)
    half = (k.sent[4] - k.sent[3] - 1.4) / 2
    await k.hl(await b.rect(".rv-tile", 0), seconds=half + 0.2)
    await b.hover(".rv-tile", 0, seconds=0.6)
    await k.until(k.sent[3] + half)
    await k.hl(await b.rect(".rv-tile", 1), seconds=half)
    await b.hover(".rv-tile", 1, seconds=0.6)
    await k.until(k.dur - 1.6)
    await b.scroll_to_el(".rv-bars", 1.1, offset=190)
    await b.hover(".rv-bar-row", 3, seconds=0.5)


async def rec_companies(k: Take) -> None:
    b = k.b
    r = await b.rect_text("Companies behind the evidence")
    if r:
        await b.scroll_to(await b.scroll_y() + r[1] - 130, 1.3)
    await k.hl(await b.rect(".rv-cos"), seconds=max(2.2, k.sent[1] - 1.9), pad=10)
    await b.hover(".rv-co", 0, seconds=0.7)
    await asyncio.sleep(0.5)
    await b.hover(".rv-co", 2, seconds=0.7)
    await k.until(k.sent[1] - 1.2)
    r = await b.rect_text("Has the market already moved?")
    if r:
        await b.scroll_to(await b.scroll_y() + r[1] - 130, 1.2)
    await k.until(k.sent[1] + 0.3)
    await k.hl(await b.rect(".rv-prices"), seconds=3.2, pad=10)
    for i in (0, 1, 2):
        await b.hover(".rv-price", i, seconds=0.6)
        await asyncio.sleep(0.5)


async def rec_scout(k: Take) -> None:
    b = k.b
    await b.scroll_to(300, 0.5)                                       # bring the view tabs on screen (a click needs them visible)
    for _ in range(4):                                                 # the scout table lives in the full report
        await b.click("button.tab", text="full report", seconds=0.3)
        await asyncio.sleep(0.35)
        if await b.rect("#scout"):
            break
    await b.scroll_to_el("#scout", 0.8, offset=70)
    await asyncio.sleep(0.3)
    await k.hl(await b.rect("#scout table"), seconds=max(2.4, k.sent[1] - 1.8), pad=8)
    await b.hover("#scout tbody tr", 0, seconds=0.7)
    await k.until(k.sent[1])
    for i in (0, 1, 2):
        await b.hover("#scout tbody tr", i, seconds=0.6)
        await asyncio.sleep(0.5)


async def rec_round(k: Take) -> None:
    b = k.b
    await b.scroll_to_el(".tr-log", 1.1, offset=260)
    await asyncio.sleep(0.3)
    await k.hl(await b.rect(".tr-log"), seconds=max(2.2, k.sent[1] - 1.6), pad=10)
    await b.hover(".tr-log li", 0, seconds=0.7)
    await k.until(k.sent[1] - 0.9)
    k.cut()
    await b.scroll_to_el(".tr-card", 1.1, offset=90, text="Agent economy")       # the report purchase
    await k.until(k.sent[1] + 0.2)
    await k.hl(await b.rect(".tr-card .stat", 0, text="paid for reports"), seconds=2.4, pad=8)
    await b.hover(".tr-mini > div", 0, seconds=0.7)
    await k.until(k.sent[2] - 0.9)
    k.cut()
    await b.scroll_to_el(".tr-card.live", 1.0, offset=110, index=0)            # the Intel buy, approved by the agent
    await k.until(k.sent[2] + 0.2)
    await k.hl(await b.rect(".tr-card.live .tr-head", 0), seconds=2.6, pad=8)
    await b.hover(".tr-card.live .tr-say", 0, seconds=0.8)
    await k.until(k.sent[3] - 0.9)
    k.cut()
    await b.scroll_to_el(".tr-card", 1.0, offset=90, text="Agent economy")       # staking and the kept pot
    await k.until(k.sent[3] + 0.2)
    await k.hl(await b.rect(".tr-card .stat", 0, text="staked for NEAR AI"), seconds=2.2, pad=8)
    await asyncio.sleep(1.4)
    await k.hl(await b.rect(".tr-card .stat", 0, text="kept pot"), seconds=2.0, pad=8)
    await k.until(k.sent[4] + 0.1)
    await k.hl(await b.rect(".tr-mini"), seconds=max(2.2, k.dur - k.sent[4] - 0.8), pad=8)  # reports priced in NEAR
    await b.hover(".tr-mini > div", 1, seconds=0.7)


async def rec_market(k: Take) -> None:
    """The public listing on market.near.ai (no sign-in): the top of the page, then the price and Hire box."""
    b = k.b
    await k.until(k.sent[1] - 0.6)
    try:
        await k.hl(await b.rect("button, a", 0, text="Hire FUTURESCOUT"), seconds=max(2.4, k.sent[2] - k.sent[1] - 0.6), pad=10)
    except Exception:  # noqa: BLE001  (the marketplace's page changed: the shot still shows the listing)
        pass
    await k.until(k.sent[2] + 0.2)
    await b.scroll_to(420, 1.4)
    await k.until(k.dur - 0.3)


async def rec_evidence(k: Take) -> None:
    b = k.b
    await b.scroll_to(300, 0.9)
    await b.click("button.tab", text="full report", seconds=0.7)
    await k.until(k.sent[1] - 1.0)
    await b.scroll_to_el("#trace", 1.2, offset=70)
    await b.move_mouse(640, 420, 0.8)
    await k.until(k.sent[2] - 1.6)
    await b.scroll_to_el("#evidence", 1.7, offset=70)
    await k.until(k.sent[2] + 0.2)
    await b.scroll_to_el(".finding", 0.9, offset=250)
    await k.hl(await b.rect(".finding", 0), seconds=max(2.4, k.sent[3] - k.sent[2] - 0.6), pad=10)
    await b.hover(".finding", 0, seconds=0.7)
    await k.until(k.sent[3] + 0.3)
    r = await b.rect("button.tab", text="unverified claim")
    if r and 60 < r[1] < 680:
        k.cut()
        await b.click("button.tab", text="x signals", seconds=0.6)          # posts are never verified facts: this view has findings
        await asyncio.sleep(0.3)
        await b.click("button.tab", text="unverified claim", seconds=0.6)
        await asyncio.sleep(0.5)
        for agent in ("risk", "market", "patents"):       # Science may have none: find an agent that does
            if await b.rect(".finding", 0):
                break
            await b.click("button.tab", text=agent, seconds=0.45)
            await asyncio.sleep(0.45)
        await k.hl(await b.rect(".finding", 0), seconds=2.2, pad=10)


async def rec_seal(k: Take) -> None:
    b = k.b
    await b.scroll_to(0, 1.0)
    await k.hl(await b.rect("a.pill.pill-on"), seconds=k.dur - 1.3, pad=7)
    await b.hover("a.pill.pill-on", seconds=0.9)


async def rec_funds(k: Take) -> None:
    b = k.b
    await b.scroll_to(430, 1.2)
    await k.hl(await b.rect(".tier-legend"), seconds=2.2, pad=8)
    await b.hover("a.fund-card", 0, seconds=0.7)
    await asyncio.sleep(0.4)
    await b.hover("a.fund-card", 2, seconds=0.7)
    await k.until(k.sent[2] - 1.5)
    k.cut()
    await b.click("a.tab", text="trading agent", seconds=0.7)       # same area, second sub-tab
    await asyncio.sleep(1.2)
    await b.scroll_to_el(".tp-pipe", 0.9, offset=370)
    await k.until(k.sent[2] + 0.2)
    await k.hl(await b.rect(".tp-pipe"), seconds=max(2.0, k.sent[3] - k.sent[2] - 0.6), pad=10)
    await b.hover(".tp-name", text="trading agent", seconds=0.7)
    await k.until(k.sent[3] + 0.1)
    span = k.sent[4] - k.sent[3] - 1.4
    for i, name in enumerate(["safety checks", "auto-approve", "near intents"]):
        await k.until(k.sent[3] + 0.1 + span * i / 3)
        await b.hover(".tp-name", text=name, seconds=0.6)
    await k.until(k.sent[4] - 1.2)
    k.cut()
    await b.scroll_to_el(".sp-grid", 1.1, offset=210)
    await k.until(k.sent[4] + 0.2)
    await k.hl(await b.rect(".sp-grid"), seconds=3.2, pad=12)
    await b.hover(".sp-row", 0, seconds=0.7)
    await k.until(k.sent[4] + (k.dur - k.sent[4]) * 0.6)
    await b.hover(".tr-agent", 1, seconds=0.8)


# ============================================================================= pieces (shots) of the timeline
@dataclass
class Piece:
    scene: Scene
    key: str
    kind: str                                   # "card" | "rec"
    start: float = 0.0                          # absolute seconds
    dur: float = 0.0
    card: Optional[Callable[[float, float], Image.Image]] = None
    prep: Optional[Callable[[Browser], Awaitable[None]]] = None
    action: Optional[Callable[[Take], Awaitable[None]]] = None
    meta: dict = field(default_factory=dict)    # recorded: frames, hls, track, clicks
    _times: list = field(default_factory=list)
    _cache: tuple = (None, None)

    def base(self, t: float) -> Image.Image:
        if self.kind == "card":
            return self.card(t, self.dur)
        frames = self.meta["frames"]
        if not self._times:
            self._times = [f[0] for f in frames]
        i = max(0, bisect.bisect_right(self._times, t) - 1)
        if self._cache[0] != i:
            img = Image.open(TAKES / self.key / frames[i][1]).convert("RGB")
            if img.size != (W, H):
                img = img.resize((W, H), Image.LANCZOS)
            self._cache = (i, img)
        return self._cache[1].copy()


def build_pieces(scenes: list[Scene], rid: str, tamper_lines: list[str]) -> list[Piece]:
    by = {s.key: s for s in scenes}
    report = f"{DASH}/runs/{rid}"

    def goto(url: str, wait: float):
        async def prep(b: Browser) -> None:
            await b.goto(url, wait=wait)
            await b.move_mouse(640, 380, 0.05)
        return prep

    async def nothing(b: Browser) -> None:
        return None

    s = by
    pieces: list[Piece] = []
    card1 = s["01_intro"].sent[0][1] + 0.25
    pieces += [Piece(s["01_intro"], "01_card", "card", dur=card1, card=title_card),
               Piece(s["01_intro"], "01_home", "rec", dur=s["01_intro"].dur - card1, prep=goto(f"{DASH}/", 2.0), action=rec_home)]
    pieces.append(Piece(s["02_radar"], "02_radar", "rec", dur=s["02_radar"].dur, prep=goto(f"{DASH}/radar", 1.8), action=rec_radar))
    pieces.append(Piece(s["03_agents"], "03_agents", "rec", dur=s["03_agents"].dur, prep=goto(f"{DASH}/about", 1.5), action=rec_agents))
    pieces.append(Piece(s["04_report"], "04_report", "rec", dur=s["04_report"].dur, prep=goto(report, 0.15), action=rec_report))
    pieces.append(Piece(s["05_companies"], "05_companies", "rec", dur=s["05_companies"].dur, prep=nothing, action=rec_companies))
    pieces.append(Piece(s["05b_scout"], "05b_scout", "rec", dur=s["05b_scout"].dur, prep=nothing, action=rec_scout))
    pieces.append(Piece(s["06_evidence"], "06_evidence", "rec", dur=s["06_evidence"].dur, prep=nothing, action=rec_evidence))
    seal_rec = s["07_seal"].sent[1][0] - 0.15
    pieces += [Piece(s["07_seal"], "07_badge", "rec", dur=seal_rec, prep=nothing, action=rec_seal),
               Piece(s["07_seal"], "07_tamper", "card", dur=s["07_seal"].dur - seal_rec,
                     card=terminal_card(tamper_lines, "python scripts\\tamper_demo.py --run " + rid[:8] + "…"))]
    pieces.append(Piece(s["09_funds"], "09_funds", "rec", dur=s["09_funds"].dur, prep=goto(f"{DASH}/funds", 2.0), action=rec_funds))
    pieces.append(Piece(s["10_round"], "10_round", "rec", dur=s["10_round"].dur, prep=goto(f"{DASH}/trading", 2.5), action=rec_round))
    pieces.append(Piece(s["11_market"], "11_market", "rec", dur=s["11_market"].dur,
                        prep=goto("https://market.near.ai/a/futurescout", 5.0), action=rec_market))
    pieces.append(Piece(s["10_close"], "10_close", "card", dur=s["10_close"].dur, card=closing_card))
    pieces = [p for p in pieces if p.scene in scenes]
    t = scenes[0].start
    for p in pieces:
        p.start = t
        t += p.dur
    return pieces


async def record(pieces: list[Piece], only: Optional[set[str]] = None) -> None:
    b = Browser()
    await b.start()
    try:
        for p in pieces:
            if p.kind != "rec":
                continue
            await p.prep(b)
            if only is not None and p.key not in only:
                continue                       # still ran prep so later takes start from the right page
            sent = [s0 - (p.start - p.scene.start) for s0, _ in p.scene.sent] + [p.dur]
            take = Take(b, p.dur, sent)
            await b.start_recording(TAKES / p.key)
            try:
                await asyncio.wait_for(p.action(take), timeout=p.dur + 6)
            except asyncio.TimeoutError:
                print(f"  {p.key}: choreography ran long and was cut at the scene end")
            await take.until(p.dur)
            await asyncio.sleep(0.25)
            frames = await b.stop_recording()
            p.meta = {"dur": p.dur, "frames": frames, "hls": take.hls, "track": list(b.track), "clicks": list(b.clicks)}
            (TAKES / p.key / "meta.json").write_text(json.dumps(p.meta), encoding="utf-8")
            print(f"  recorded {p.key}: {len(frames)} frames over {p.dur:.1f}s, {len(take.hls)} highlight(s)")
    finally:
        await b.close()


# ============================================================================= overlays and rendering
CURSOR = [(0, 0), (0, 17), (4.5, 13), (7.6, 20), (10.2, 18.8), (7.2, 12), (13, 12)]


def draw_highlights(d: ImageDraw.ImageDraw, p: Piece, t: float) -> None:
    for h in p.meta.get("hls", []):
        a = env(t, h["t0"], h["t1"])
        if a <= 0:
            continue
        x, y, w, hh = (v * SCALE for v in h["rect"])
        pulse = 0.5 + 0.5 * math.sin((t - h["t0"]) * 4.2)
        for grow, alpha, width in ((0, 1.0, 4), (5, 0.34 + 0.2 * pulse, 3), (10, 0.14 + 0.1 * pulse, 3)):
            d.rounded_rectangle((x - grow, y - grow, x + w + grow, y + hh + grow), radius=16 + grow, outline=rgba(MINT, a * alpha), width=width)


def draw_cursor(d: ImageDraw.ImageDraw, p: Piece, t: float) -> None:
    track = p.meta.get("track") or []
    if len(track) < 2:
        return
    times = [k[0] for k in track]
    i = bisect.bisect_right(times, t) - 1
    if i < 0:
        x, y = track[0][1], track[0][2]
    elif i >= len(track) - 1:
        x, y = track[-1][1], track[-1][2]
    else:
        (t0, x0, y0), (t1, x1, y1) = track[i], track[i + 1]
        k = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
        x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    px, py = x * SCALE, y * SCALE
    for ct, cx, cy in p.meta.get("clicks", []):
        k = (t - ct) / 0.45
        if 0 <= k <= 1:
            r = 10 + 34 * k
            d.ellipse((cx * SCALE - r, cy * SCALE - r, cx * SCALE + r, cy * SCALE + r), outline=rgba(MINT, 1 - k), width=4)
    pts = [(px + cxp * 1.7, py + cyp * 1.7) for cxp, cyp in CURSOR]
    d.polygon([(a + 2, b + 3) for a, b in pts], fill=(0, 0, 0, 90))
    d.polygon(pts, fill=(255, 255, 255, 255), outline=(20, 24, 23, 255))
    d.line(pts + [pts[0]], fill=(20, 24, 23, 255), width=2)


def draw_title(d: ImageDraw.ImageDraw, sc: Scene, t: float) -> None:
    """Section title: a short interstitial over a dark scrim while the next shot fades in (keeps the app unobstructed after)."""
    if not sc.title:
        return
    a = env(t, 0.0, 2.0, 0.3, 0.5)
    if a <= 0:
        return
    d.rectangle((0, 0, W, H), fill=(2, 4, 4, int(205 * a)))
    k = ease(t / 0.6)
    y = H / 2 - 30 + (1 - k) * 16
    d.text((W / 2, y - 78), sc.num, font=font(34, "monobold"), fill=rgba(MINT, a), anchor="mm")
    d.line((W / 2 - 70 * k, y - 40, W / 2 + 70 * k, y - 40), fill=rgba(MINT, a * 0.9), width=3)
    d.text((W / 2, y + 30), sc.title, font=font(92, "light"), fill=rgba(INK, a), anchor="mm")


def wrap(d: ImageDraw.ImageDraw, text: str, f, width: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def draw_caption(d: ImageDraw.ImageDraw, sc: Scene, t: float) -> None:
    for (cap, _), (s0, s1) in zip(sc.lines, sc.sent):
        a = env(t, s0 - 0.08, s1 + 0.22, 0.14, 0.16)
        if a <= 0:
            continue
        f = font(38, "semibold")
        lines = wrap(d, cap, f, 1380)
        if len(lines) == 2 and len(lines[1].split()) == 1:       # avoid a one-word last line
            lines = wrap(d, cap, f, int(max(d.textlength(lines[0], font=f) * 0.72, 600)))
        lh = 52
        bw = max(d.textlength(ln, font=f) for ln in lines) + 68
        bh = lh * len(lines) + 30
        x0, y0 = (W - bw) / 2, H - 56 - bh
        for i, ln in enumerate(lines):
            d.text((W / 2, y0 + 15 + lh * i + lh / 2), ln, font=f, fill=rgba((255, 255, 255), a), anchor="mm",
                   stroke_width=2, stroke_fill=(0, 0, 0, int(200 * a)))   # thin edge only: the page stays visible behind the words
        return


def render(scenes: list[Scene], pieces: list[Piece], out: Path, t_from: float, t_to: float) -> None:
    ff = ffmpeg_exe()
    proc = subprocess.Popen(
        [ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
        stdin=subprocess.PIPE)
    total = int(round((t_to - t_from) * FPS))
    starts = [p.start for p in pieces]
    black = Image.new("RGB", (W, H), (0, 0, 0))
    prev_last: Optional[Image.Image] = None
    cur_i, last_base = -1, None
    for n in range(total):
        t = t_from + n / FPS
        i = max(0, bisect.bisect_right(starts, t) - 1)
        p = pieces[i]
        if i != cur_i:
            prev_last, cur_i = last_base, i
        local = t - p.start
        img = p.base(min(local, p.dur))
        d = ImageDraw.Draw(img, "RGBA")
        if p.kind == "rec":
            draw_highlights(d, p, local)
            draw_cursor(d, p, local)
        last_base = img
        if local < XF and prev_last is not None:
            img = Image.blend(prev_last, img, ease(local / XF))
            d = ImageDraw.Draw(img, "RGBA")
        sc = p.scene
        st = t - sc.start
        draw_title(d, sc, st)
        draw_caption(d, sc, st)
        if t - t_from < 0.7:
            img = Image.blend(black, img, ease((t - t_from) / 0.7))
        if t_to - t < 1.0:
            img = Image.blend(black, img, ease((t_to - t) / 1.0))
        proc.stdin.write(img.tobytes())
        if n % 300 == 0:
            print(f"  rendering {n / FPS:5.1f}s / {total / FPS:.1f}s", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed while encoding the video")


def mux(video: Path, narration: Path, music: Path, total: float, out: Path) -> None:
    fc = (f"[2:a]atrim=0:{total:.2f},aformat=sample_rates=44100:channel_layouts=stereo,lowpass=f=3400,highpass=f=55,"
          f"aecho=0.6:0.45:380|760:0.28|0.16,volume=0.22,afade=t=in:d=2.5,afade=t=out:st={total - 3.2:.2f}:d=3.2[m];"
          "[1:a]aformat=sample_rates=44100:channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=9,asplit=2[n1][n2];"
          "[m][n1]sidechaincompress=threshold=0.03:ratio=5:attack=80:release=900[md];"
          "[md][n2]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.94[a]")
    run([ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(video), "-i", str(narration), "-stream_loop", "-1", "-i", str(music),
         "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.2f}",
         "-movflags", "+faststart", str(out)])


def write_text_outputs(scenes: list[Scene], total: float) -> None:
    def ts(x: float) -> str:
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    rows, n = [], 1
    for sc in scenes:
        for (cap, _), (s0, s1) in zip(sc.lines, sc.sent):
            rows.append(f"{n}\n{ts(sc.start + s0)} --> {ts(sc.start + s1 + 0.2)}\n{cap}\n")
            n += 1
    OUT.with_suffix(".srt").write_text("\n".join(rows), encoding="utf-8")
    md = ["# FUTURESCOUT AI: demo narration", "",
          f"Video: `{OUT.name}` · {int(total // 60)}:{int(total % 60):02d} · 1920x1080 · 30 fps. Voice: {VOICE}, generated with ElevenLabs (free plan; credit: ElevenLabs, elevenlabs.io).", "",
          "Every app shot is a live recording of the running dashboard. Cards, titles, captions, highlight rings, the mouse pointer, "
          "narration and music are added by `demo/make_video.py`.", "",
          "| Time | Section | Narration |", "|---|---|---|"]
    for sc in scenes:
        m = f"{int(sc.start // 60)}:{int(sc.start % 60):02d}"
        md.append(f"| {m} | {sc.num + ' ' if sc.num else ''}{sc.title or 'Close'} | {' '.join(c for c, _ in sc.lines)} |")
    (ROOT / "NARRATION.md").write_text("\n".join(md) + "\n", encoding="utf-8")


# ============================================================================= main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-record", action="store_true", help="reuse the recorded takes in demo/build_v4/takes")
    ap.add_argument("--skip-tts", action="store_true", help="reuse the narration WAVs")
    ap.add_argument("--scene", help="record and render only this scene key (silent test clip in demo/build_v4)")
    ap.add_argument("--rerecord", help="comma-separated take keys to record again (others reused)")
    args = ap.parse_args()
    for dpath in (TAKES, AUDIO):
        dpath.mkdir(parents=True, exist_ok=True)

    runs = get_json("/api/runs")
    rid = next(r["id"] for r in runs if r["topic"] == "high bandwidth memory" and r.get("score"))
    print("report on screen:", rid)
    narration = build_narration(SCENES, reuse=args.skip_tts or bool(args.scene) or args.skip_record)
    total = SCENES[-1].start + SCENES[-1].dur
    print(f"narration: {total:.1f}s total; scenes " + ", ".join(f"{s.key[:2]}:{s.dur:.1f}" for s in SCENES))

    backend = ROOT.parent / "backend"
    tp = subprocess.run([sys.executable, "scripts/tamper_demo.py", "--run", rid], cwd=backend, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=240, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    tamper_lines = [ln.rstrip() for ln in tp.stdout.splitlines()
                    if not any(x in ln for x in ("aiohttp", "Unclosed", "connector", "client_session"))]
    while tamper_lines and not tamper_lines[-1].strip():
        tamper_lines.pop()
    if not any("MISMATCH" in ln for ln in tamper_lines):
        raise RuntimeError("tamper demo did not produce its MISMATCH line; not faking it")

    scenes = [s for s in SCENES if not args.scene or s.key == args.scene]
    pieces = build_pieces(SCENES, rid, tamper_lines)
    if args.scene:   # prep of earlier scenes is needed for takes that continue on the same page
        all_pieces = build_pieces(SCENES, rid, tamper_lines)
        wanted = {p.key for p in all_pieces if p.scene.key == args.scene}
        asyncio.run(record(all_pieces, only=wanted))
        pieces = [p for p in all_pieces if p.key in wanted]
    elif args.skip_record or args.rerecord:
        again = set((args.rerecord or "").split(",")) - {""}
        if again:
            asyncio.run(record(pieces, only=again))
        for p in pieces:
            if p.kind == "rec" and not p.meta:
                p.meta = json.loads((TAKES / p.key / "meta.json").read_text(encoding="utf-8"))
    else:
        asyncio.run(record(pieces))

    if args.scene:
        test = BUILD / f"test_{args.scene}.mp4"
        render(scenes, pieces, test, pieces[0].start, pieces[-1].start + pieces[-1].dur)
        print("test clip:", test)
        return 0
    music = build_music_loop()
    silent = BUILD / "video_silent.mp4"
    render(SCENES, pieces, silent, 0.0, total)
    mux(silent, narration, music, total, OUT)
    write_text_outputs(SCENES, total)
    print(f"done: {OUT}  ({total:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
