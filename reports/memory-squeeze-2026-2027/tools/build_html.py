"""Build the HTML artifact page from the filled markdown document.

Usage: .venv/bin/python -I tools/build_html.py doc/ram-supply-2026-2027.filled.md doc/ram-supply-2026-2027.html
Images referenced as ../out/charts/*.png (relative to doc/) are embedded as data URIs.
"""
import base64
import pathlib
import re
import sys

import markdown

src = pathlib.Path(sys.argv[1]).resolve()
dst = pathlib.Path(sys.argv[2]).resolve()
text = src.read_text()

# The page header carries the title; drop the markdown H1.
text = re.sub(r"\A# .*\n", "", text)

md = markdown.Markdown(extensions=["tables", "toc", "sane_lists"],
                       extension_configs={"toc": {"toc_depth": "2-3", "permalink": False}})
body = md.convert(text)
toc = re.sub(r"^\s*<div class=\"toc\">\s*|\s*</div>\s*$", "", md.toc)


def embed(m):
    path = (src.parent / m.group(1)).resolve()
    data = base64.b64encode(path.read_bytes()).decode()
    return f'src="data:image/png;base64,{data}"'


body = re.sub(r'src="([^"]+\.png)"', embed, body)
body = re.sub(r"<img ", '<img loading="eager" ', body)
body = re.sub(r"<p>(<img [^>]*>)</p>", r'<figure class="chart">\1</figure>', body)
body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
body = re.sub(r'href="(https?://)', r'target="_blank" rel="noopener" href="\1', body)

page = f"""<title>DRAM Supply 2026–2027</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Layout: report column (~72ch) with a sticky contents rail on wide screens; tables scroll in place. */
:root {{
  --bg: #f6f7f9; --surface: #ffffff; --fg: #1b2129; --muted: #5a6573;
  --rule: #d9dee5; --accent: #1f5fa8; --accent-soft: #e6eef8; --chart-bg: #fbfbf9;
  --f-display: "Archivo", "Helvetica Neue", Arial, sans-serif;
  --f-body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #12161b; --surface: #181d23; --fg: #e3e7ec; --muted: #9aa5b1;
  --rule: #2c343e; --accent: #7fb2ec; --accent-soft: #1d2a3a; --chart-bg: #fbfbf9; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #12161b; --surface: #181d23; --fg: #e3e7ec; --muted: #9aa5b1;
  --rule: #2c343e; --accent: #7fb2ec; --accent-soft: #1d2a3a; --chart-bg: #fbfbf9; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--fg); font: 17px/1.6 var(--f-body); }}
.wrap {{ max-width: 1240px; margin: 0 auto; padding-block: 40px 80px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; grid-template-columns: minmax(0, 1fr); gap: 40px; }}
@media (min-width: 1080px) {{ .wrap {{ grid-template-columns: 250px minmax(0, 1fr); }} }}
header.mast {{ grid-column: 1 / -1; display: grid; gap: 10px; border-bottom: 2px solid var(--fg); padding-bottom: 20px; }}
.eyebrow {{ font: 500 12px/1 var(--f-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}
h1 {{ font: 700 clamp(28px, 4.2vw, 44px)/1.1 var(--f-display); margin: 0; text-wrap: balance; letter-spacing: -.01em; }}
.dek {{ color: var(--muted); max-width: 70ch; margin: 0; }}
nav.toc {{ font-size: 14px; line-height: 1.35; }}
@media (min-width: 1080px) {{ nav.toc {{ position: sticky; top: calc(env(safe-area-inset-top, 0px) + 16px);
  max-height: calc(100vh - 32px); overflow-y: auto; }} }}
nav.toc ul {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }}
nav.toc ul ul {{ padding-left: 12px; margin-top: 6px; gap: 4px; }}
nav.toc ul ul a {{ color: var(--muted); }}
nav.toc a {{ color: var(--fg); text-decoration: none; }}
nav.toc a:hover, nav.toc a:focus-visible {{ color: var(--accent); text-decoration: underline; }}
nav.toc .label {{ font: 600 12px/1 var(--f-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin-bottom: 12px; }}
article {{ min-width: 0; }}
article > * {{ max-width: 72ch; }}
article > .tw, article > figure, article > hr {{ max-width: none; }}
h2 {{ font: 700 28px/1.2 var(--f-display); margin: 56px 0 12px; padding-top: 12px; border-top: 1px solid var(--rule); text-wrap: balance; }}
h3 {{ font: 600 21px/1.25 var(--f-display); margin: 36px 0 8px; text-wrap: balance; }}
h4 {{ font: 600 13px/1.3 var(--f-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin: 26px 0 6px; }}
p, li {{ margin: 0 0 12px; }}
a {{ color: var(--accent); }}
a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
code {{ font: 0.86em var(--f-mono); background: var(--accent-soft); padding: 1px 5px; border-radius: 3px; overflow-wrap: anywhere; }}
strong {{ font-weight: 600; }}
hr {{ border: 0; border-top: 1px solid var(--rule); margin: 32px 0; }}
.tw {{ overflow-x: auto; margin: 16px 0 24px; border: 1px solid var(--rule); background: var(--surface); }}
table {{ border-collapse: collapse; width: 100%; font-size: 14.5px; line-height: 1.4; font-variant-numeric: tabular-nums; }}
th {{ font: 600 12.5px/1.3 var(--f-body); text-align: left; color: var(--muted); background: var(--accent-soft);
  border-bottom: 1px solid var(--rule); padding: 8px 10px; vertical-align: bottom; }}
td {{ padding: 7px 10px; border-bottom: 1px solid var(--rule); vertical-align: top; }}
tr:last-child td {{ border-bottom: 0; }}
td:first-child {{ font-weight: 600; min-width: 9em; }}
figure.chart {{ margin: 20px 0 28px; background: var(--chart-bg); border: 1px solid var(--rule); padding: 8px; }}
figure.chart img {{ display: block; width: 100%; height: auto; max-width: 100%; }}
article > ol:last-of-type li, article > ul:last-of-type li {{ overflow-wrap: anywhere; }}
@media (max-width: 600px) {{ body {{ font-size: 16px; }} h2 {{ font-size: 23px; }} h3 {{ font-size: 19px; }} }}
</style>
<div class="wrap">
  <header class="mast">
    <div class="eyebrow">Research report · DRAFT · 2026-10-30 · bn Gb = billion gigabits · 1 EB = 8 bn Gb</div>
    <h1>DRAM production and supply chain in 2026, and the 2027 outlook, by memory category</h1>
    <p class="dek">Server ECC, DDR5, client PC, HBM, GDDR, LPDDR and DDR4. Each figure is cited, with its kind (actual, estimate, forecast, derived) and the publish date. Model numbers are medians with 80% and 95% intervals from a 50,000-draw Monte Carlo.</p>
  </header>
  <nav class="toc" aria-label="Contents"><div class="label">Contents</div>{toc}</nav>
  <article>
{body}
  </article>
</div>
"""
dst.write_text(page)
print(dst, f"{len(page)/1e6:.2f} MB")
