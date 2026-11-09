"""Build the automatic FUTURESCOUT AI demo video (narrated, subtitled, MP4).

Run from the repo root with the project venv while the API and dashboard are running:

    ..\\.venv\\Scripts\\python.exe demo\\build_demo.py              (from backend\\)
    python demo\\build_demo.py --skip-shots                        (reuse captured screenshots)
    python demo\\build_demo.py --voice "Microsoft David Desktop"    (another installed voice)
    set DEMO_API_URL=http://127.0.0.1:8001 / DEMO_DASHBOARD_URL=http://localhost:3001 to point at other ports

What it does (everything stays local, no secrets are read or shown):
  1. Headless Chrome screenshots of the running dashboard at 1280x720 (tall pages captured whole, then cropped).
  2. Cards drawn by code for things a browser cannot show: the NEAR record (live /verify result), the buyer bot
     (a real --dry-run plus the purchase already recorded on testnet) and the closing card.
  3. A title bar at the top of every frame and the spoken narration burned in as subtitles at the bottom,
     one chunk at a time, timed to the speech.
  4. Narration with Windows' built-in text-to-speech (System.Speech), one WAV per scene.
  5. ffmpeg (bundled by imageio-ffmpeg) joins the stills into clips: still frames, 0.5 s fades, no zoom or pan
     (earlier versions used a Ken Burns zoom, which looked like camera shake).

Output: demo/futurescout_demo.mp4 (1920x1080, H.264 + AAC). Intermediate files live in demo/build/ (git-ignored).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import wave
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
SHOTS, FRAMES, AUDIO, CLIPS = BUILD / "shots", BUILD / "frames", BUILD / "audio", BUILD / "clips"
OUT = ROOT / "futurescout_demo.mp4"

DASH = os.environ.get("DEMO_DASHBOARD_URL", "http://localhost:3000")
API = os.environ.get("DEMO_API_URL", "http://localhost:8000")
W, H = 1280, 720
FPS = 30
MIN_SCENE_SECONDS = 6.0
PAD_AFTER_SPEECH = 1.0
LEAD_IN = 0.4
SUB_MAX_CHARS = 150     # one subtitle chunk (about two lines)

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
FONT_DIR = Path(r"C:\Windows\Fonts")


@dataclass
class Scene:
    key: str
    title: str                 # short title shown at the top
    narration: str             # spoken and shown as subtitles
    url: str | None = None     # page to capture (None = synthetic card)
    scroll_y: int = 0          # crop offset inside the tall capture
    card: str | None = None    # near | buyer | closing
    optional: bool = False     # skip silently when the page/data is not there


# ----------------------------------------------------------------------------- data from the running API
def get_json(path: str, timeout: int = 30):
    return json.load(urllib.request.urlopen(f"{API}{path}", timeout=timeout))


def bought_report_id(topic: str = "high bandwidth memory") -> str:
    """The HBM report that has really been bought on testnet (used for the badge, verify and buyer scenes)."""
    runs = get_json("/api/runs")
    cands = sorted([r for r in runs if r["topic"] == topic and r.get("score")], key=lambda r: r["score"], reverse=True)
    for r in cands:
        try:
            if get_json(f"/api/market/{r['id']}/purchases"):
                return r["id"]
        except Exception:
            pass
    return cands[0]["id"] if cands else runs[0]["id"]


def scout_report_id() -> str | None:
    """Newest report whose Company Scout named at least one candidate."""
    for r in get_json("/api/runs"):
        try:
            rep = get_json(f"/api/runs/{r['id']}")["report"]
        except Exception:
            continue
        sc = rep.get("scout") or {}
        if sc.get("candidates"):
            return r["id"]
    return None


def other_sector_report_id() -> tuple[str, str, str] | None:
    """Newest report outside semiconductors: (run id, topic, sector), to show the platform is not chip-only."""
    for r in get_json("/api/runs"):
        sec = r.get("sector")
        if sec and sec != "semiconductors":
            return r["id"], r["topic"], sec.replace("_", " ")
    return None


def scenes(rid: str, scout_rid: str | None, other: tuple[str, str, str] | None = None) -> list[Scene]:
    rep = f"{DASH}/runs/{rid}"
    out = [
        Scene("01_home", "FUTURESCOUT AI · multi-agent semiconductor research",
              "FUTURESCOUT AI is a team of AI agents that finds the next hot semiconductor technology and shows the evidence. "
              "It reads papers, patents, SEC filings and X posts. Every claim carries a label and its sources, and every report is sealed on NEAR.",
              url=f"{DASH}/", scroll_y=57),
        Scene("02_radar", "Hot-topic radar · counted by code, no model involved",
              "The radar ranks topics by how fast papers and patent filings are growing, year over year. It is pure counting: no model, no opinion. "
              "Co-packaged optics and high bandwidth memory are the hottest right now.",
              url=f"{DASH}/radar", scroll_y=560),
        Scene("03_agents", "Eight agents, twelve steps, one sealed report · every model runs on NEAR AI Cloud",
              "A research run is twelve steps. The Chief plans the searches. Science, Risk, Market, X and Patent agents work in parallel. "
              "The Chief reviews, the Risk agent argues against the findings and checks how far prices have already run, "
              "the Company Scout finds the companies behind the evidence, and the Investment agent writes the report. "
              "Every model runs on NEAR AI Cloud.",
              url=f"{DASH}/", scroll_y=1640),
        Scene("04_watch", "Autonomous watch · research starts by itself, every decision logged",
              "It also runs on its own. Every two hours the X agent reads the approved accounts, counts which topics are rising, "
              "and may propose new ones tied to real posts. When a topic is hot and has no fresh report, a full research run starts automatically, "
              "within a daily budget. Every decision is logged with its reason.",
              url=f"{DASH}/", scroll_y=860),
        Scene("05_report", "A report · high bandwidth memory",
              "Here is a report on high bandwidth memory. Seven agents ran: forty-nine findings, sixty-nine sources. "
              "The green badge says the report is unchanged since it was recorded on NEAR testnet.",
              url=rep, scroll_y=0),
        Scene("06_score", "Technology Opportunity Score · confidence capped by the evidence",
              "The score is built dimension by dimension, and its confidence can never be higher than the confidence of the evidence it cites. "
              "Headlines and social posts never count as verified facts.",
              url=rep, scroll_y=2100),
        Scene("07_evidence", "Evidence · every finding labelled, with the exact quote",
              "Every finding carries a label: verified fact, interpretation, forecast, assumption or unverified claim, and the exact excerpt it came from. "
              "A verified fact must point to a real source and quote it exactly. A citation guard checks this in code, not in a prompt.",
              url=rep, scroll_y=6090),
    ]
    if scout_rid:
        out.append(Scene("08_scout", "Company Scout · the companies behind the evidence, not just the giants",
                         "Instead of only naming the big companies everyone knows, the Company Scout collects every company behind the evidence: "
                         "patent assignees, the employers of paper authors, and SEC filers. It matches them to the SEC ticker file, pulls their financials, "
                         "and scores smaller, growing, R&D-heavy names as possible next runners. A transparent heuristic, labelled as a forecast, never a recommendation.",
                         url=f"{DASH}/runs/{scout_rid}", scroll_y=9630, optional=True))
    if other:
        oid, otopic, osector = other
        out.append(Scene("08b_sector", f"Every technology sector · {otopic} ({osector})",
                         f"It is not only about chips. The radar watches nine technology sectors, from AI software and robotics to quantum, energy, "
                         f"space, biotech, cybersecurity and X R, and the same agents ran on {otopic}: each run reads the companies of its own sector "
                         f"and finds the ones behind the evidence.",
                         url=f"{DASH}/runs/{oid}", scroll_y=0, optional=True))
    out += [
        Scene("09_near", "Sealed on NEAR testnet · fingerprint stored on chain, re-checked live",
              "Sealing means the report's SHA-256 fingerprint is written to NEAR SocialDB on testnet. "
              "Anyone can recompute it and compare it with the chain, so a report cannot be quietly edited after the fact.",
              card="near"),
        Scene("09b_tamper", "Tamper check · change one word and the seal breaks",
              "Here is the proof. The stored report matches the fingerprint on chain. Change a single word of the summary, and the fingerprint no longer "
              "matches. The dashboard runs this check on every page load, so an edited report is caught at once.",
              card="tamper", optional=True),
        Scene("10_market", "Report market · summaries free, full evidence after a NEAR payment",
              "FUTURESCOUT is an agent that earns. Summaries and scores are free; the full evidence unlocks after a payment of zero point one NEAR to its account. "
              "The API reads the transfer from the chain before unlocking.",
              url=f"{DASH}/market", scroll_y=540),
        Scene("11_buyer", "Buyer bot · pays on testnet, downloads, verifies the fingerprint",
              "A separate buyer bot picks the hottest topic, pays on testnet, downloads the report and checks the fingerprint against NEAR. "
              "This purchase really happened on testnet; here is the transaction.",
              card="buyer"),
        Scene("12_treasury", "Treasury · an agent that pays for its own research",
              "The agent pays for its own work. Each report costs about twenty cents of model and data; buyers pay zero point one NEAR on testnet. "
              "The treasury shows what came in, what went out, and the account balance read live from the chain.",
              url=f"{DASH}/market", scroll_y=660, optional=True),
        Scene("13_portfolio", "Paper portfolio · a simulation, no money moves",
              "Does the research point at winners? The paper portfolio is a simulation: every sealed report buys its top scout candidates with pretend money "
              "at the first close after the report date, and tracks them against the S O X X semiconductor E T F. Nothing is traded. "
              "The positions come from reports fingerprinted on NEAR, so they cannot be backdated.",
              url=f"{DASH}/portfolio", scroll_y=560, optional=True),
        Scene("14_close", "FUTURESCOUT AI · built for the NEAR hackathon",
              "FUTURESCOUT AI: models on NEAR AI Cloud, reports sealed and sold on NEAR, and an agent that funds its own research. "
              "Testnet only, and not financial advice. Thank you.",
              card="closing"),
    ]
    return out


# ----------------------------------------------------------------------------- capture
def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    sys.exit("Chrome or Edge not found; install one or edit CHROME_CANDIDATES.")


def capture(chrome: str, url: str, out: Path, height: int) -> None:
    profile = BUILD / "chrome-profile"
    cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-prefers-reduced-motion",
           "--no-first-run", "--disable-extensions", f"--user-data-dir={profile}",
           f"--window-size={W},{height}", "--virtual-time-budget=12000", f"--screenshot={out}", url]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    if not out.exists():
        raise RuntimeError(f"no screenshot written for {url}")


def frame_from_page(chrome: str, sc: Scene) -> Image.Image:
    tall = SHOTS / f"{sc.key}.png"
    if not tall.exists():
        capture(chrome, sc.url, tall, height=min(sc.scroll_y + H, 16000))
    img = Image.open(tall).convert("RGB")
    y = min(sc.scroll_y, max(0, img.height - H))
    return img.crop((0, y, W, y + H))


# ----------------------------------------------------------------------------- drawing helpers
def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    name = "consola.ttf" if mono else ("segoeuib.ttf" if bold else "segoeui.ttf")
    for cand in (FONT_DIR / name, FONT_DIR / ("arialbd.ttf" if bold else "arial.ttf")):
        if cand.exists():
            return ImageFont.truetype(str(cand), size)
    return ImageFont.load_default()


def wrap(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def split_subtitles(text: str, max_chars: int = SUB_MAX_CHARS) -> list[str]:
    """Split the narration at sentence ends (then commas) into chunks a viewer can read in one go."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    chunks: list[str] = []
    for s in sentences:
        if len(s) <= max_chars:
            chunks.append(s)
            continue
        parts = [p.strip() for p in re.split(r"(?<=[,;:])\s+", s) if p.strip()]
        cur = ""
        for p in parts:
            if len(f"{cur} {p}".strip()) <= max_chars or not cur:
                cur = f"{cur} {p}".strip()
            else:
                chunks.append(cur)
                cur = p
        if cur:
            chunks.append(cur)
    # merge very short tails into the previous chunk
    merged: list[str] = []
    for c in chunks:
        if merged and len(c) < 40 and len(merged[-1]) + len(c) + 1 <= max_chars:
            merged[-1] = f"{merged[-1]} {c}"
        else:
            merged.append(c)
    return merged


# ----------------------------------------------------------------------------- synthetic cards
def card_base(eyebrow: str, heading: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), (5, 7, 7))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((60, 50, W - 60, H - 50), radius=14, fill=(10, 13, 12), outline=(40, 46, 44))
    d.text((90, 76), eyebrow, fill=(0, 236, 151), font=font(16, mono=True))
    d.text((90, 104), heading, fill=(240, 243, 242), font=font(40, bold=True))
    return img, d


def near_card(run_id: str) -> Image.Image:
    v = get_json(f"/api/runs/{run_id}/verify", timeout=60)
    img, d = card_base("NEAR RECORD · SOCIALDB · TESTNET", "Report fingerprint, re-checked live by the API")
    ok = v.get("status") == "match"
    status = "MATCH — unchanged since it was recorded" if ok else f"status: {v.get('status')}"
    d.rounded_rectangle((90, 170, 90 + 24 + d.textlength(status, font=font(20, bold=True)), 206), radius=18,
                        fill=(0, 60, 40) if ok else (70, 40, 10), outline=(0, 236, 151) if ok else (255, 170, 60))
    d.text((102, 177), status, fill=(0, 236, 151) if ok else (255, 190, 90), font=font(20, bold=True))
    rows = [("report", run_id), ("sha256 (computed now)", v.get("sha256", "")), ("sha256 (on NEAR)", v.get("onchain_sha256", "")),
            ("account", v.get("account", "")), ("contract", v.get("contract", "")), ("network", v.get("network", "")),
            ("explorer", v.get("explorer_url", ""))]
    y = 240
    for k, val in rows:
        d.text((90, y), k, fill=(130, 140, 136), font=font(17, mono=True))
        d.text((340, y), str(val), fill=(220, 224, 222), font=font(18, mono=True))
        y += 40
    d.text((90, y + 14), "How: the API hashes the stored report JSON, reads the key from v1.social08.testnet over RPC and compares.",
           fill=(150, 160, 156), font=font(17))
    d.text((90, y + 40), "Mainnet is refused in code. Testnet tokens have no value.", fill=(150, 160, 156), font=font(17))
    return img


def buyer_card(run_id: str) -> Image.Image:
    backend = ROOT.parent / "backend"
    dry = subprocess.run([sys.executable, "scripts/buyer_bot.py", "--dry-run"], cwd=backend, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", timeout=120, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    lines = [l[:104] + ("…" if len(l) > 104 else "") for l in (dry.stdout or dry.stderr).splitlines() if l.strip()][:7]
    try:
        purchases = get_json(f"/api/market/{run_id}/purchases")
    except Exception:
        purchases = []
    img = Image.new("RGB", (W, H), (6, 8, 8))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((60, 50, W - 60, H - 50), radius=14, fill=(12, 14, 14), outline=(40, 46, 44))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse((84 + i * 22, 70, 96 + i * 22, 82), fill=c)
    d.text((160, 66), "backend  —  python scripts\\buyer_bot.py --dry-run", fill=(130, 140, 136), font=font(16, mono=True))
    y = 110
    d.text((90, y), "> python scripts\\buyer_bot.py --dry-run", fill=(0, 236, 151), font=font(19, mono=True)); y += 34
    for l in lines:
        d.text((90, y), l, fill=(220, 224, 222), font=font(18, mono=True)); y += 28
    if purchases:
        p = purchases[0]
        rec = p.get("sale_record") or {}
        y += 14
        d.text((90, y), "Recorded purchase of the high bandwidth memory report (NEAR testnet):", fill=(0, 236, 151), font=font(19, mono=True)); y += 34
        rows = [("buyer", p["buyer_account"]), ("paid", "0.1 NEAR (testnet)"), ("payment tx", p["tx_hash"]),
                ("explorer", f"https://testnet.nearblocks.io/txns/{p['tx_hash']}")]
        if rec.get("tx_hash"):
            rows.append(("sale record", f"{rec['contract']}  tx {rec['tx_hash']}"))
        for k, v in rows:
            d.text((90, y), f"{k:>12}: ", fill=(130, 140, 136), font=font(18, mono=True))
            d.text((90 + 15 * 11, y), v, fill=(220, 224, 222), font=font(18, mono=True)); y += 28
        y += 10
        d.text((90, y), "Fingerprint check: computed SHA-256 == value recorded on NEAR  ->  MATCH", fill=(0, 236, 151), font=font(18, mono=True))
    return img


def tamper_card(run_id: str) -> Image.Image:
    """Terminal-style card with the real output of scripts/tamper_demo.py (reads the chain; writes nothing)."""
    backend = ROOT.parent / "backend"
    out = subprocess.run([sys.executable, "scripts/tamper_demo.py", "--run", run_id], cwd=backend, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", timeout=180, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    lines = [l.rstrip() for l in (out.stdout or out.stderr).splitlines() if l.strip()]
    if not any("MISMATCH" in l for l in lines):
        raise RuntimeError("tamper demo did not produce a MISMATCH line")
    img = Image.new("RGB", (W, H), (6, 8, 8))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((60, 50, W - 60, H - 50), radius=14, fill=(12, 14, 14), outline=(40, 46, 44))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse((84 + i * 22, 70, 96 + i * 22, 82), fill=c)
    d.text((160, 66), "backend  —  python scripts\\tamper_demo.py", fill=(130, 140, 136), font=font(16, mono=True))
    y = 108
    d.text((90, y), "> python scripts\\tamper_demo.py", fill=(0, 236, 151), font=font(19, mono=True)); y += 34
    for l in lines[:16]:
        colour = (220, 224, 222)
        if l.strip().startswith("-> match"):
            colour = (0, 236, 151)
        elif "MISMATCH" in l:
            colour = (255, 110, 100)
        elif l.startswith(("1)", "2)")):
            colour = (240, 243, 242)
        d.text((90, y), l[:112], fill=colour, font=font(17 if len(l) > 95 else 18, mono=True)); y += 27
        if y > H - 90:
            break
    return img


def closing_card() -> Image.Image:
    img = Image.new("RGB", (W, H), (4, 6, 6))
    glow = Image.new("RGB", (W, H), (4, 6, 6))
    ImageDraw.Draw(glow).ellipse((W // 2 - 420, H // 2 - 260, W // 2 + 420, H // 2 + 260), fill=(0, 60, 40))
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(120)), 0.9)
    d = ImageDraw.Draw(img)
    title = font(72, bold=True)
    d.text(((W - d.textlength("FUTURESCOUT AI", font=title)) / 2, 170), "FUTURESCOUT AI", fill=(245, 247, 246), font=title)
    f2 = font(30)
    sub = "Find the next hot technology. Show the evidence."
    d.text(((W - d.textlength(sub, font=f2)) / 2, 270), sub, fill=(0, 236, 151), font=f2)
    rows = ["Models on NEAR AI Cloud  ·  Reports sealed on NEAR testnet  ·  Sold for NEAR, verified on chain",
            "Eight agents  ·  Nine technology sectors  ·  Company Scout  ·  Autonomous watch  ·  Paper portfolio",
            "Testnet only  ·  Not financial advice  ·  MIT licence"]
    f3 = font(22)
    y = 360
    for r in rows:
        d.text(((W - d.textlength(r, font=f3)) / 2, y), r, fill=(190, 198, 195), font=f3); y += 40
    return img


# ----------------------------------------------------------------------------- compositing
def add_title(img: Image.Image, title: str, idx: int, total: int) -> Image.Image:
    """Slim title bar across the top."""
    img = img.convert("RGBA")
    bar = Image.new("RGBA", (W, 44), (0, 0, 0, 215))
    img.alpha_composite(bar, (0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 12, 26, 32), radius=3, fill=(0, 236, 151))
    f = font(19, bold=True)
    while d.textlength(title, font=f) > W - 160 and f.size > 13:
        f = font(f.size - 1, bold=True)
    d.text((38, 11), title, fill=(240, 243, 242), font=f)
    d.text((W - 72, 13), f"{idx}/{total}", fill=(140, 150, 146), font=font(15, mono=True))
    return img.convert("RGB")


def add_subtitle(img: Image.Image, text: str) -> Image.Image:
    """Readable subtitle box at the bottom (two lines max, dark translucent background)."""
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    f = font(28)
    lines = wrap(d, text, f, W - 200)
    while len(lines) > 2 and f.size > 20:
        f = font(f.size - 2)
        lines = wrap(d, text, f, W - 200)
    line_h = f.size + 10
    box_h = line_h * len(lines) + 26
    box = Image.new("RGBA", (W - 120, box_h), (0, 0, 0, 190))
    img.alpha_composite(box, (60, H - box_h - 24))
    d = ImageDraw.Draw(img)
    y = H - box_h - 24 + 13
    for line in lines:
        d.text(((W - d.textlength(line, font=f)) / 2, y), line, fill=(248, 250, 249), font=f)
        y += line_h
    return img.convert("RGB")


# ----------------------------------------------------------------------------- narration
def tts(text: str, out: Path, voice: str | None) -> float:
    txt = BUILD / "tts.txt"
    txt.write_text(text, encoding="utf-8")
    ps = ("Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          + (f"try {{ $s.SelectVoice('{voice}') }} catch {{}}; " if voice else "")
          + f"$s.Rate = 0; $s.SetOutputToWaveFile('{out}'); "
          f"$s.Speak([IO.File]::ReadAllText('{txt}', [Text.Encoding]::UTF8)); $s.Dispose()")
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], check=True, timeout=120)
    with wave.open(str(out)) as w:
        return w.getnframes() / w.getframerate()


# ----------------------------------------------------------------------------- video
def ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        if shutil.which("ffmpeg"):
            return "ffmpeg"
        sys.exit("ffmpeg not found: pip install imageio-ffmpeg")


def make_clip(ff: str, frames: list[tuple[Path, float]], audio: Path, seconds: float, out: Path) -> None:
    """Stills with per-frame durations (concat demuxer) + narration; fades in and out; no motion."""
    lst = out.with_suffix(".txt")
    lines = []
    for p, dur in frames:
        lines.append(f"file '{p.as_posix()}'\nduration {dur:.3f}\n")
    lines.append(f"file '{frames[-1][0].as_posix()}'\n")   # concat demuxer needs the last file repeated
    lst.write_text("".join(lines), encoding="utf-8")
    vf = (f"fps={FPS},scale=1920:1080:flags=lanczos,format=yuv420p,"
          f"fade=t=in:st=0:d=0.5,fade=t=out:st={seconds - 0.5:.2f}:d=0.5")
    af = f"adelay={int(LEAD_IN * 1000)}|{int(LEAD_IN * 1000)},apad,atrim=0:{seconds:.2f},afade=t=out:st={seconds - 0.4:.2f}:d=0.4"
    cmd = [ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(audio),
           "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]", "-map", "[v]", "-map", "[a]",
           "-t", f"{seconds:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", str(out)]
    subprocess.run(cmd, check=True, timeout=600)


def concat(ff: str, clips: list[Path], out: Path) -> None:
    lst = BUILD / "clips.txt"
    lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", "-movflags", "+faststart", str(out)], check=True, timeout=600)


def write_srt(entries: list[tuple[float, float, str]], path: Path) -> None:
    def ts(t: float) -> str:
        h, rem = divmod(t, 3600)
        m, s = divmod(rem, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
    path.write_text("".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(entries, 1)), encoding="utf-8")


# ----------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-shots", action="store_true", help="reuse screenshots already in demo/build/shots")
    ap.add_argument("--voice", default="Microsoft Zira Desktop")
    ap.add_argument("--frames-only", action="store_true", help="stop after writing the frames (no audio, no video)")
    args = ap.parse_args()

    for d in (SHOTS, FRAMES, AUDIO, CLIPS):
        d.mkdir(parents=True, exist_ok=True)
    if not args.skip_shots:
        for f in SHOTS.glob("*.png"):
            f.unlink()
    for f in FRAMES.glob("*.png"):
        f.unlink()

    rid = bought_report_id()
    scout_rid = scout_report_id()
    other = other_sector_report_id()
    scs = scenes(rid, scout_rid, other)
    chrome = find_chrome()
    print(f"bought report {rid}; scout report {scout_rid}; other sector {other}; {len(scs)} scenes; chrome: {chrome}")

    # ---- frames: one base image per scene, then one image per subtitle chunk
    bases: list[tuple[Scene, Image.Image]] = []
    for sc in scs:
        try:
            if sc.card == "buyer":
                img = buyer_card(rid)
            elif sc.card == "near":
                img = near_card(rid)
            elif sc.card == "tamper":
                img = tamper_card(rid)
            elif sc.card == "closing":
                img = closing_card()
            else:
                img = frame_from_page(chrome, sc)
        except Exception as exc:  # noqa: BLE001
            if sc.optional:
                print(f"  skip {sc.key}: {type(exc).__name__}: {exc}")
                continue
            raise
        bases.append((sc, img))
        print(f"  frame {sc.key}")
    total = len(bases)

    ff = ffmpeg_exe()
    clips: list[Path] = []
    srt: list[tuple[float, float, str]] = []
    t0 = 0.0
    for i, (sc, base) in enumerate(bases, 1):
        base = add_title(base, sc.title, i, total)
        chunks = split_subtitles(sc.narration)
        frames: list[tuple[Path, float]] = []
        if args.frames_only:
            p = FRAMES / f"{sc.key}.png"
            add_subtitle(base, chunks[0]).save(p)
            continue
        wav = AUDIO / f"{sc.key}.wav"
        speech = tts(sc.narration, wav, args.voice)
        seconds = max(MIN_SCENE_SECONDS, LEAD_IN + speech + PAD_AFTER_SPEECH)
        weights = [len(c) for c in chunks]
        t = 0.0
        for j, (c, wgt) in enumerate(zip(chunks, weights)):
            dur = speech * wgt / sum(weights)
            if j == 0:
                dur += LEAD_IN
            if j == len(chunks) - 1:
                dur = seconds - t
            p = FRAMES / f"{sc.key}_{j + 1:02d}.png"
            add_subtitle(base, c).save(p)
            frames.append((p, dur))
            srt.append((t0 + t, t0 + t + dur, c))
            t += dur
        clip = CLIPS / f"{sc.key}.mp4"
        make_clip(ff, frames, wav, seconds, clip)
        clips.append(clip)
        t0 += seconds
        print(f"  clip {sc.key}: speech {speech:.1f}s -> {seconds:.1f}s, {len(chunks)} subtitle(s)")
    if args.frames_only:
        return 0
    concat(ff, clips, OUT)
    write_srt(srt, OUT.with_suffix(".srt"))
    print(f"done: {OUT} ({t0 / 60:.1f} min) + subtitles {OUT.with_suffix('.srt').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
