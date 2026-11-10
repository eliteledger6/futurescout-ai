"""Natural voiceover with ElevenLabs (owner 2026-11-10: free plan). Scene-based audio files from VOICEOVER_SCRIPT.md.

  python demo\\voice.py --voices              list the voices this key can use (names only)
  python demo\\voice.py --sample              the 15-20 s approval sample -> demo/voiceover/sample.wav
  python demo\\voice.py --sample --voice Brian
  python demo\\voice.py --all                 every scene -> demo/voiceover/<scene>.wav (only after the owner approves)

Needs ELEVENLABS_API_KEY in the project's .env (the owner adds it; it is never printed). Free plan: 10,000 credits a month,
no commercial licence, attribution to ElevenLabs required (the video's end card and NARRATION.md credit it).
Every paragraph is cached by a hash of its text and the voice settings, so re-running never pays for the same audio twice.
Pauses: a blank line between paragraphs = 0.35 s, `[pause]` = 0.8 s. Each request passes the neighbouring text
(previous_text / next_text) so the intonation flows across paragraphs.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "demo" / "VOICEOVER_SCRIPT.md"
OUT = ROOT / "demo" / "voiceover"
CACHE = OUT / "cache"
API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"          # supports previous_text/next_text for steady intonation across requests
DEFAULT_VOICE = "Eric"                    # premade voice: warm, smooth, trustworthy presenter
SETTINGS = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True, "speed": 1.0}
SEED = 1110                               # same seed every request: a steadier voice across scenes
SHORT, LONG = 0.35, 0.8                   # seconds of silence: between paragraphs, at [pause]
RATE = 44100


def api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    env = ROOT / ".env"
    if not key and env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("ELEVENLABS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        sys.exit("ELEVENLABS_API_KEY is not set in .env (make it at elevenlabs.io -> Developers -> API keys)")
    return key


def scenes() -> dict[str, list[str]]:
    """{scene key: [paragraph, ...]}; '[pause]' stays inside a paragraph and is split later."""
    out: dict[str, list[str]] = {}
    key = None
    for line in SCRIPT.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\S+)", line)
        if m:
            key = m.group(1)
            out[key] = []
        elif key and line.strip() and not line.startswith(("---", "#")):
            out[key].append(line.strip())
    return out


def clean(text: str) -> str:
    return text.replace("**", "").strip()


def pieces(paragraphs: list[str]) -> list[tuple[str, float]]:
    """[(text, silence after)] with [pause] splits."""
    out = []
    for p in paragraphs:
        parts = [clean(x) for x in p.split("[pause]")]
        for i, part in enumerate(parts):
            if part:
                out.append((part, LONG if i < len(parts) - 1 else SHORT))
    return out


def to_pcm(mp3: bytes) -> bytes:
    import imageio_ffmpeg
    res = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", "pipe:0", "-f", "s16le", "-ac", "1",
                          "-ar", str(RATE), "pipe:1"], input=mp3, capture_output=True, check=True)
    return res.stdout


def voice_id(client: httpx.Client, name: str) -> str:
    voices = client.get(f"{API}/voices").json().get("voices", [])
    for v in voices:
        if v.get("name", "").split(" ")[0].lower() == name.lower():
            return v["voice_id"]
    sys.exit(f"voice {name!r} not found; run with --voices to see the list")


def speak(client: httpx.Client, vid: str, text: str, prev: str, nxt: str) -> bytes:
    tag = hashlib.sha1(json.dumps([vid, MODEL, SETTINGS, SEED, text, prev, nxt]).encode()).hexdigest()[:12]
    path = CACHE / f"{tag}.mp3"
    if not path.is_file():
        r = client.post(f"{API}/text-to-speech/{vid}", params={"output_format": "mp3_44100_128"},
                        json={"text": text, "model_id": MODEL, "voice_settings": SETTINGS, "seed": SEED,
                              "previous_text": prev or None, "next_text": nxt or None})
        if r.status_code != 200:
            sys.exit(f"ElevenLabs refused ({r.status_code}): {r.text[:300]}")
        CACHE.mkdir(parents=True, exist_ok=True)
        path.write_bytes(r.content)
        print(f"  generated {len(text)} characters")
    return to_pcm(path.read_bytes())


def render(client: httpx.Client, vid: str, paragraphs: list[str], out: Path) -> float:
    parts = pieces(paragraphs)
    pcm = io.BytesIO()
    for i, (text, gap) in enumerate(parts):
        prev = parts[i - 1][0] if i else ""
        nxt = parts[i + 1][0] if i + 1 < len(parts) else ""
        pcm.write(speak(client, vid, text, prev, nxt))
        if i + 1 < len(parts):
            pcm.write(b"\x00\x00" * int(RATE * gap))
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.getvalue())
    return len(pcm.getvalue()) / 2 / RATE


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--voices", action="store_true")
    g.add_argument("--sample", action="store_true")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    args = ap.parse_args()
    client = httpx.Client(headers={"xi-api-key": api_key()}, timeout=120)
    if args.voices:
        for v in client.get(f"{API}/voices").json().get("voices", []):
            labels = v.get("labels") or {}
            print(f"{v.get('name', '')[:40]:40} {labels.get('gender', ''):7} {labels.get('accent', ''):12} {labels.get('description', '') or labels.get('descriptive', '')}")
        return 0
    sc = scenes()
    vid = voice_id(client, args.voice)
    if args.sample:
        secs = render(client, vid, sc["sample"], OUT / "sample.wav")
        print(f"sample: {OUT / 'sample.wav'}  ({secs:.1f} s, voice {args.voice})")
        return 0
    total = 0.0
    for key, paragraphs in sc.items():
        if key == "sample":
            continue
        secs = render(client, vid, paragraphs, OUT / f"{key}.wav")
        total += secs
        print(f"{key:14} {secs:5.1f} s")
    print(f"total {total:.0f} s, voice {args.voice}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
