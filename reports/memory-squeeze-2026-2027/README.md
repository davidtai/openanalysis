# The Memory Squeeze

*The AI build-out has already bought 2027's DRAM. The rest of the market is bidding for the leftovers.*

DRAM market report, October 2026. **[Read the PDF](report/dram-shortage-2026-2027.pdf)** (22 pages).

## Key findings

- **55.8 EB of DRAM output in 2027, up 23% on 2026** (model median; 80% range 402–496 bn Gb). 2026 output is 45.4 EB, up 24% on 2025.
- **AI servers take the new bits first.** In 2026, server ECC output rises 44% and HBM 54%, while phone LPDDR falls 7% and PC memory 6%.
- **Server LPDDR has the largest 2027 gap: about 40%.** Nvidia's 2027 need is 8.4 EB against 5.0 EB of supply. HBM is about 10% short.
- **Phones and PCs absorb the shortage** through higher prices and smaller memory specs.
- **No real relief before 2028**, when the new fabs add meaningful output.

The report also breaks out production by company (Samsung, SK hynix, Micron, CXMT, Nanya and others) and by memory type.

## Method

The model is a Monte Carlo supply model (50,000 draws, fixed seed) built on 1,493 cited source rows. [`model/METHOD.md`](model/METHOD.md) covers the categories, units, assumptions, backtest and sensitivity analysis.

Units: exabytes (EB) in the text and billion gigabits (bn Gb) in tables. 1 EB = 8 bn Gb.

## Contents

| Path | What it holds |
|---|---|
| `report/dram-shortage-2026-2027.pdf` | The finished report |
| `report/src.html` → `report/report.html` | Report source with citation markers, and the built HTML |
| `report/build.py`, `report/charts.py` | Resolve the citations into endnotes and draw the figures |
| `report/citation-audit.txt` | Every citation with its sentence and the quote it cites |
| `model/forecast.py`, `model/vendor_matrix.py` | The supply model and the company-by-type matrix |
| `sources/*.csv`, `sources/*-notes.md` | Source data; each row has its URL, date and quote |
| `out/` | Model outputs: forecasts, sensitivity, backtest, checks, charts |
| `tools/` | Builders that turn raw downloads into the source CSVs |
| `doc/` | Earlier long-form draft of the analysis (Markdown and HTML) |

The notes files refer to `sources/raw-*/` folders of downloaded PDFs and text extracts. Those folders are not in this repo because they hold third-party material. Each CSV row keeps the source's URL, so you can download a document again if you need it.

## Rebuild

```sh
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -I model/forecast.py        # about 2 minutes; writes out/
.venv/bin/python -I report/charts.py         # figures in report/fig/
.venv/bin/python -I report/build.py          # report/report.html + citation audit
```

The PDF is printed from `report/report.html`.
