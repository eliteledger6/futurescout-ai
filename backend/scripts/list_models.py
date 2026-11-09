"""Compare model_config.yaml with the LIVE NEAR AI catalogue.

Usage (from the backend folder, venv active):
    python scripts/list_models.py

Reports, for every model in the config: whether it still exists, whether its price
or advertised features changed. Needs internet. The catalogue endpoint is public;
NEAR_AI_API_KEY is sent if set but is not required here.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.models.config import load_model_config  # noqa: E402


def main() -> int:
    settings = get_settings()
    config = load_model_config()
    headers = {}
    if settings.near_ai_api_key:
        headers["Authorization"] = f"Bearer {settings.near_ai_api_key.get_secret_value()}"
    url = settings.near_ai_base_url.rstrip("/") + "/models"
    try:
        response = httpx.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"Could not read the model catalogue from {url}: {type(exc).__name__}")
        return 1

    catalogue = {m["id"]: m for m in response.json().get("data", [])}
    print(f"Catalogue: {len(catalogue)} models. Config prices verified on {config.prices_verified_on}.\n")
    problems = 0
    for alias, spec in config.models.items():
        live = catalogue.get(spec.id)
        if live is None:
            print(f"MISSING  {alias:22} {spec.id}  (not in live catalogue)")
            problems += 1
            continue
        pricing = live.get("pricing") or {}
        live_in, live_out = pricing.get("input"), pricing.get("output")
        features = live.get("supported_features") or []
        notes = []
        if live_in is None and live_out is None:
            notes.append("price check skipped (no pricing fields found in catalogue entry)")
        if live_in is not None and abs(float(live_in) - spec.input_per_m) > 1e-9:
            notes.append(f"input price {spec.input_per_m} -> {live_in}")
        if live_out is not None and abs(float(live_out) - spec.output_per_m) > 1e-9:
            notes.append(f"output price {spec.output_per_m} -> {live_out}")
        if ("structured_outputs" in features) != spec.structured_outputs:
            notes.append(f"structured_outputs config={spec.structured_outputs} live={'structured_outputs' in features}")
        if ("json_mode" in features) != spec.json_mode:
            notes.append(f"json_mode config={spec.json_mode} live={'json_mode' in features}")
        status = "OK      " if not notes else "CHANGED "
        problems += bool(notes)
        print(f"{status} {alias:22} {spec.id}  {'; '.join(notes)}")
    print("\nEverything matches." if not problems else f"\n{problems} model(s) need attention in config/model_config.yaml.")
    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
