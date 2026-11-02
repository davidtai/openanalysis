"""Build report/report.html from report/src.html.

Citation markers in src.html:
    [[total-dram.csv:556]]                 one source row (file:line, line as in the CSV, header = line 1)
    [[total-dram.csv:556; lpddr.csv:22]]   several rows
    [[M:forecast_by_category.csv]]         a model output file in out/
    [[M:METHOD.md]]                        the model method note
Rows from the same document (same URL and title) share one endnote number.
Notes are numbered in order of first use. The <!--NOTES--> placeholder receives the list.
<!--FIG:name--> inlines report/fig/name.svg.

Also writes report/citation-audit.txt: every marker with the sentence around it and each cited quote.

Run: .venv/bin/python -I report/build.py
"""
import csv
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REP = ROOT / "report"
SRC = ROOT / "sources"

rows = {}
for f in sorted(SRC.glob("*.csv")):
    with open(f, newline="") as fh:
        for i, r in enumerate(csv.DictReader(fh), start=2):
            rows[f"{f.name}:{i}"] = r

MODEL_DESC = {
    "METHOD.md": "Model method note, model/METHOD.md (run of 2026-10-30).",
}

text = (REP / "src.html").read_text()

note_keys = []      # ordered unique keys
note_body = {}      # key -> html
audit = []
errors = []

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fmt_date(d):
    d = (d or "").strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", d)
    if m:
        return f"{int(m.group(3))} {MONTHS[int(m.group(2)) - 1]} {m.group(1)}"
    m = re.fullmatch(r"(\d{4})-(\d{2})", d)
    if m:
        return f"{MONTHS[int(m.group(2)) - 1]} {m.group(1)}"
    return d or "n.d."


def flags(r):
    n = (r.get("notes") or "").lower()
    out = []
    if "snippet only" in n or "search-summary" in n or "search summary only" in n or "search-tool summary" in n:
        out.append("seen in a search summary; page not fetched")
    if "headline only" in n or n.startswith("headline"):
        out.append("headline only")
    if "paywalled" in n:
        out.append("paywalled; summary or title only")
    return out


def key_for(ref):
    ref = ref.strip()
    if ref.startswith("M:"):
        name = ref[2:]
        p = (ROOT / "model" / name) if name.endswith(".md") else (ROOT / "out" / name)
        if not p.exists():
            errors.append(f"missing model file {ref}")
        k = "M:" + name
        if k not in note_body:
            note_body[k] = MODEL_DESC.get(name, f"Model output, out/{name}. Run of model/forecast.py on 2026-10-30 "
                                                f"(50,000 Monte Carlo draws, seed 20261030).")
        return k, None
    if ref not in rows:
        errors.append(f"missing row {ref}")
        return None, None
    r = rows[ref]
    k = (r["url"].strip(), r["title"].strip())
    if k not in note_body:
        title = r["title"].strip() or r["metric"]
        url = r["url"].strip()
        fl = flags(r)
        body = (f"{html.escape(r['publisher'].strip())}, “{html.escape(title)}”, {fmt_date(r['pub_date'])}. "
                f"<span class=\"url\">{html.escape(url)}</span>")
        note_body[k] = body
        note_body[(k, "flags")] = set(fl)
    else:
        note_body[(k, "flags")] |= set(flags(r))
    return k, r


def plain(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(re.sub(r"\s+", " ", s))


def repl(m):
    refs = [x for x in m.group(1).split(";") if x.strip()]
    nums = []
    start = max(0, m.start() - 320)
    ctx = plain(re.sub(r"\[\[.*?\]\]", "", text[start:m.start()]))
    ctx = ctx[-260:]
    audit.append("=" * 100 + "\nCONTEXT: …" + ctx)
    for ref in refs:
        k, r = key_for(ref)
        if k is None:
            continue
        if k not in note_keys:
            note_keys.append(k)
        n = note_keys.index(k) + 1
        if n not in nums:
            nums.append(n)
        if r is not None:
            audit.append(f"  [{n}] {ref.strip()} | {r['publisher']} {r['pub_date']} | {r['metric']} | {r['period']} | "
                         f"{r['value']} {r['unit']} | {r['kind']}\n      Q: {r['quote']}\n      N: {r['notes']}")
        else:
            audit.append(f"  [{n}] {ref.strip()}")
    nums.sort()
    links = ",".join(f'<a href="#n{n}" id="r{n}-{len(audit)}">{n}</a>' for n in nums)
    return f'<sup class="cite">{links}</sup>'


body = re.sub(r"\[\[(.*?)\]\]", repl, text)


def fig(m):
    p = REP / "fig" / f"{m.group(1)}.svg"
    if not p.exists():
        p2 = ROOT / "out" / "charts" / f"{m.group(1)}.png"
        if p2.exists():
            return f'<img src="../out/charts/{m.group(1)}.png" alt="">'
        errors.append(f"missing figure {m.group(1)}")
        return ""
    svg = p.read_text()
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.S)
    svg = re.sub(r"<!DOCTYPE.*?>", "", svg, flags=re.S)
    svg = re.sub(r'<svg ([^>]*?)width="[^"]*"\s*height="[^"]*"', r'<svg \1', svg, count=1)
    return svg


body = re.sub(r"<!--FIG:([\w\-]+)-->", fig, body)


def tables():
    fbc = {}
    with open(ROOT / "out" / "forecast_by_category.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            fbc[(r["category"], int(r["year"]))] = r
    order = [
        ("server_ecc", "Server ECC (RDIMM, MRDIMM)", ""),
        ("hbm", "HBM", ""),
        ("lpddr", "LPDDR, all", ""),
        ("lpddr_lps", "Server (SOCAMM, Grace)", "sub"),
        ("lpddr_mob", "Phone and tablet †", "sub"),
        ("lpddr_pclp", "PC †", "sub"),
        ("lpddr_auto", "Auto", "sub"),
        ("client_pc", "Client PC DDR5/DDR4 †", ""),
        ("gddr", "GDDR", ""),
        ("other_consumer", "Other / consumer", ""),
        ("total", "Total DRAM", "tot"),
        ("ddr5_total", "DDR5 (overlay)", "ov"),
        ("ddr4_legacy", "DDR4 modules (overlay)", "ov"),
    ]

    def n(x, d=1):
        if x in ("", None):
            return "–"
        v = float(x)
        return f"{v:,.{d}f}".replace("-", "−")

    def pct(x):
        if x in ("", None):
            return "–"
        return f"{float(x) * 100:+.0f}%".replace("-", "−")

    out = {}
    for y in (2026, 2027):
        h = [f'<div class="wrap-table"><p class="figtitle">Table A{1 if y == 2026 else 2}. {y}: supply, demand and gap by category (bn Gb)</p>',
             "<table><thead><tr><th>Category</th><th>Supply median</th><th>80% range</th><th>95% range</th>"
             "<th>YoY</th><th>Demand</th><th>Gap</th><th>Sufficiency</th></tr></thead><tbody>"]
        for cat, label, cls in order:
            r = fbc[(cat, y)]
            yoy = pct(r["yoy_median"]) if r["yoy_median"] else "–"
            if cat in ("ddr5_total", "ddr4_legacy") and y == 2026:
                yoy = "–"
            dem = n(r["demand_median_bn_gb"])
            if cat == "total":
                dem = n(r["demand_median_bn_gb"])
            h.append(
                f'<tr class="{cls}"><td>{label}</td><td>{n(r["median_bn_gb"])}</td>'
                f'<td>{n(r["p10_bn_gb"])}–{n(r["p90_bn_gb"])}</td><td>{n(r["p2_5_bn_gb"])}–{n(r["p97_5_bn_gb"])}</td>'
                f'<td>{yoy}</td><td>{dem}</td><td>{n(r["gap_median_bn_gb"])}</td><td>{pct(r["gap_median"])}</td></tr>')
        h.append("</tbody></table></div>")
        out[y] = "\n".join(h)
    return out


_t = tables()
body = body.replace("<!--TABLE:2026-->", _t[2026]).replace("<!--TABLE:2027-->", _t[2027])


def vendor_table():
    vt = {}
    with open(ROOT / "out" / "vendor_by_type.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            vt[(r["year"], r["vendor"], r["type"])] = r
    vendors = ["Samsung", "SK hynix", "Micron", "CXMT", "Nanya + others"]
    types = ["server_ecc", "hbm", "lpddr", "client_pc", "gddr", "other_consumer", "total"]
    heads = ["Server ECC", "HBM", "LPDDR", "Client PC", "GDDR", "Other", "Total"]

    def cell(r):
        m, lo, hi = float(r["median_bn_gb"]), float(r["p10"]), float(r["p90"])
        if hi < 0.05:
            return "0"
        return f'{m:.1f}<span class="rng">{lo:.1f}–{hi:.1f}</span>'

    h = ['<div class="wrap-table"><p class="figtitle">Table 1. DRAM output by company and memory type (bn Gb, median and 80% range)</p>',
         '<table class="vtab"><thead><tr><th>Company</th>' + "".join(f"<th>{x}</th>" for x in heads) + "</tr></thead><tbody>"]
    for y in ("2026", "2027"):
        h.append(f'<tr class="yr"><td colspan="8">{y}</td></tr>')
        for v in vendors:
            h.append(f"<tr><td>{v}</td>" + "".join(f"<td>{cell(vt[(y, v, t)])}</td>" for t in types) + "</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)


body = body.replace("<!--TABLE:VENDOR-->", vendor_table())

items = []
for i, k in enumerate(note_keys, start=1):
    b = note_body[k]
    fl = sorted(note_body.get((k, "flags"), set())) if not (isinstance(k, str)) else []
    if fl:
        b += f" <span class=\"flag\">Note: {'; '.join(fl)}.</span>"
    items.append(f'<li id="n{i}">{b}</li>')
notes_html = '<ol class="notes">\n' + "\n".join(items) + "\n</ol>"
body = body.replace("<!--NOTES-->", notes_html)

(REP / "report.html").write_text(body)
(REP / "citation-audit.txt").write_text("\n".join(audit))
print(f"notes: {len(note_keys)}; markers: {sum(1 for a in audit if a.startswith('='))}")
if errors:
    print("ERRORS:", *errors, sep="\n  ")
    sys.exit(1)
