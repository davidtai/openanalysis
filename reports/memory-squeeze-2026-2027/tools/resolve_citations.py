"""Resolve CSV row tokens in the report source into numbered references.

Usage: python3 -I tools/resolve_citations.py doc/ram-supply-2026-2027.src.md doc/ram-supply-2026-2027.md

Tokens in the source:
  [[td:200]]          -> [n]           (row 200 of sources/total-dram.csv, 1-based file line)
  [[td:200|sd:5]]     -> [n, m]
  [[!td:200]]         -> (forecast, 2025-12-15) [n]   kind and pub_date of the first row
  <!--REFS-->         -> numbered reference list
Placeholders {{M:...}} pass through unchanged and are listed on stderr.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "td": "total-dram.csv",
    "sd": "server-ddr5.csv",
    "hg": "hbm-gddr.csv",
    "lp": "lpddr.csv",
    "sc": "supply-chain.csv",
}
TOKEN = re.compile(r"\[\[(!?)([a-z]{2}:\d+(?:\|[a-z]{2}:\d+)*)\]\]")
PLACEHOLDER = re.compile(r"\{\{M:[^}]+\}\}")
SEARCH = re.compile(r"SEARCH-SUMMARY|search-tool summary|search-result snippet|search snippet|seen only in a search|search summary", re.I)
PAYWALL = re.compile(r"paywall|members-only|title only", re.I)
# Notes that mention a search summary or headline for a different item; checked by hand.
OVERRIDES = {
    "20260610-13090": "",
    "jsr-reportedly-plans": "",
    "20260907-13219": "page fetched; the CXMT 9.5% value was seen only in a search summary",
    "price/dram/dram_contract": "September 2026 values fetched; the October 2026 update is members-only",
    "semimedia.cc/nvidia-expected": "the 75 kwpm end-2025 CoWoS value is a sidebar headline only; the 5.4 million unit figure was seen only in a search summary",
}
HEADLINE = re.compile(r"headline only|^headline\b|sidebar headline|TOC heading|listing page", re.I)


def load():
    rows = {}
    for key, name in FILES.items():
        with open(ROOT / "sources" / name, newline="") as fh:
            for i, row in enumerate(csv.DictReader(fh)):
                rows[f"{key}:{i + 2}"] = row
    return rows


def main(src, dst):
    rows = load()
    text = Path(src).read_text()
    refs = {}  # url -> dict
    order = []

    def ref_for(rid):
        if rid not in rows:
            sys.exit(f"unknown row token {rid}")
        row = rows[rid]
        url = row["url"].strip() or f"nourl:{rid}"
        if url not in refs:
            refs[url] = {"rows": [], "num": len(order) + 1}
            order.append(url)
        refs[url]["rows"].append(row)
        return refs[url]["num"]

    def sub(m):
        bang, ids = m.group(1), m.group(2).split("|")
        nums = sorted({ref_for(r) for r in ids})
        cite = "[" + ", ".join(str(n) for n in nums) + "]"
        if bang:
            row = rows[ids[0]]
            kind = row["kind"].strip()
            if "derived" in row["publisher"].lower():
                kind = "derived"
            date = row["pub_date"].strip()
            tag = f"({kind}, {date})" if date else f"({kind})"
            return f"{tag} {cite}"
        return cite

    body = TOKEN.sub(sub, text)

    lines = []
    for url in order:
        r = refs[url]
        cand = [x for x in r["rows"] if x["kind"] != "derived" and "derived" not in x["publisher"].lower()] or r["rows"]
        head = cand[0]
        flags = []
        blob = " ".join(x["notes"] + " " + x["publisher"] for x in r["rows"])
        if SEARCH.search(blob):
            flags.append("seen only in a search summary; page not fetched")
        if PAYWALL.search(blob):
            flags.append("paywalled; seen in summary or title only")
        if HEADLINE.search(blob):
            flags.append("headline only; body not read")
        for key, text in OVERRIDES.items():
            if key in url:
                flags = [text] if text else []
        flag = f" **Note: {'; '.join(flags)}.**" if flags else ""
        link = url if not url.startswith("nourl:") else "(no URL)"
        date = head["pub_date"].strip() or "n.d."
        lines.append(f"{r['num']}. {head['publisher'].strip()}. \"{head['title'].strip()}\". {date}. <{link}>{flag}")
    body = body.replace("<!--REFS-->", "\n".join(lines))
    Path(dst).write_text(body)

    keys = sorted(k for k in set(PLACEHOLDER.findall(body)) if "<" not in k)
    words = len(re.findall(r"\S+", body))
    print(f"references: {len(order)}", file=sys.stderr)
    print(f"words: {words}", file=sys.stderr)
    print(f"placeholders: {len(keys)}", file=sys.stderr)
    for k in keys:
        print(k, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
