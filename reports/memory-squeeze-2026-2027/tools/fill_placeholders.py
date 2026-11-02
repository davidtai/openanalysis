#!/usr/bin/env python3
"""Fill the {{M:<category>:<year>:<metric>}} placeholders in the research document.

Run from the project folder:  .venv/bin/python -I tools/fill_placeholders.py

1. Reads out/forecast_by_category.csv (written by model/forecast.py).
2. Writes out/placeholders.json: one formatted string for every key found in
   doc/ram-supply-2026-2027.src.md.
3. Replaces the keys in doc/ram-supply-2026-2027.md and writes
   doc/ram-supply-2026-2027.filled.md. The .src.md and .md files are not changed.

Formats: bn Gb to 4 significant digits, EB to 3 significant digits, percentages to one
decimal place with a % sign (yoy and gap carry a + or − sign). gap_bnGb = supply − demand,
negative when short. A key with no data maps to "n/a (no source)".
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "out" / "forecast_by_category.csv"
SRC_MD = ROOT / "doc" / "ram-supply-2026-2027.src.md"
DOC_MD = ROOT / "doc" / "ram-supply-2026-2027.md"
OUT_MD = ROOT / "doc" / "ram-supply-2026-2027.filled.md"
OUT_JSON = ROOT / "out" / "placeholders.json"

NA = "n/a (no source)"
MINUS = "−"                        # the document writes negatives with a true minus sign
KEY_RE = re.compile(r"\{\{M:([a-z0-9-]+):(\d{4}):([A-Za-z0-9_]+)\}\}")
TEMPLATE = "{{M:<category>:<year>:<metric>}}"   # the format description inside the document

CATEGORY = {"total": "total", "server-ecc": "server_ecc", "ddr5": "ddr5_total", "client-pc": "client_pc",
            "hbm": "hbm", "gddr": "gddr", "lpddr": "lpddr", "ddr4-legacy": "ddr4_legacy",
            "lpddr-phone": "lpddr_mob", "lpddr-server": "lpddr_lps", "lpddr-pc": "lpddr_pclp",
            "lpddr-other": "lpddr_auto", "lpddr-auto": "lpddr_auto", "other-consumer": "other_consumer"}
METRIC = {"median_bnGb": ("median_bn_gb", "bn"), "p10_bnGb": ("p10_bn_gb", "bn"), "p90_bnGb": ("p90_bn_gb", "bn"),
          "median_EB": ("median_eb", "eb"), "p10_EB": ("p10_eb", "eb"), "p90_EB": ("p90_eb", "eb"),
          "share_pct": ("share_median", "share"), "yoy_pct": ("yoy_median", "signed_pct"),
          "gap_bnGb": ("gap_median_bn_gb", "bn"), "gap_pct": ("gap_median", "signed_pct"),
          "p2_5_bnGb": ("p2_5_bn_gb", "bn"), "p97_5_bnGb": ("p97_5_bn_gb", "bn"),
          "yoy_p10_pct": ("yoy_p10", "signed_pct"), "yoy_p90_pct": ("yoy_p90", "signed_pct"),
          "suff_pct": ("gap_median", "signed_pct"), "suff_p10_pct": ("gap_p10", "signed_pct"),
          "suff_p90_pct": ("gap_p90", "signed_pct"), "demand_bnGb": ("demand_median_bn_gb", "bn")}


def sig(x: float, n: int) -> str:
    """Round to n significant digits, never in scientific notation."""
    if x == 0:
        return "0"
    digits = n - int(math.floor(math.log10(abs(x)))) - 1
    v = round(x, digits)
    s = f"{v:.{max(digits, 0)}f}"
    return s.replace("-", MINUS)


def fmt(x: float, kind: str) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return NA
    if kind == "bn":
        return sig(x, 4)
    if kind == "eb":
        return sig(x, 3)
    if kind == "share":
        return f"{100 * x:.1f}%"
    if kind == "signed_pct":
        v = round(100 * x, 1)
        return ("+" if v > 0 else MINUS if v < 0 else "") + f"{abs(v):.1f}%"
    raise ValueError(kind)


def value_for(df: pd.DataFrame, cat: str, year: int, metric: str) -> str:
    if cat not in CATEGORY or metric not in METRIC:
        return NA
    col, kind = METRIC[metric]
    rows = df[(df["category"] == CATEGORY[cat]) & (df["year"] == year)]
    if rows.empty or col not in rows.columns:
        return NA
    return fmt(float(rows.iloc[0][col]), kind)


def main() -> int:
    df = pd.read_csv(CSV)
    keys = sorted(set(KEY_RE.findall(SRC_MD.read_text())))
    mapping = {f"{{{{M:{c}:{y}:{m}}}}}": value_for(df, c, int(y), m) for c, y, m in keys}
    OUT_JSON.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n")

    text = DOC_MD.read_text()
    missing = sorted(set(m.group(0) for m in KEY_RE.finditer(text)) - set(mapping))
    if missing:
        print("keys in the .md that the .src.md does not have:", missing, file=sys.stderr)
        return 1
    filled = KEY_RE.sub(lambda m: mapping[m.group(0)], text)
    # The format description is not a key. Write it without braces so no "{{M:" remains.
    filled = filled.replace(TEMPLATE, "M:<category>:<year>:<metric>")
    OUT_MD.write_text(filled)
    left = filled.count("{{M:")
    na = sum(1 for v in mapping.values() if v == NA)
    print(f"keys: {len(mapping)}  n/a: {na}  replaced in doc: {len(KEY_RE.findall(text))}  '{{{{M:' left: {left}")
    return 0 if left == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
