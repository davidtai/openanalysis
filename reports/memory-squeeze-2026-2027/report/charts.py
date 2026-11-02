"""Charts for the DRAM shortage report.

Run from the project folder:
    .venv/bin/python -I report/charts.py
Reads out/*.csv and sources/*.csv (read-only). Writes report/fig/*.svg.
"""
import csv
import pathlib

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402,F401

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
FIG = ROOT / "report" / "fig"
FIG.mkdir(parents=True, exist_ok=True)

# Palette: dataviz reference instance (light mode, validated 6-slot adjacent order).
S1, S2, S3, S4, S5, S6 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"
BLUE_250 = "#86b6ef"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
GRAY, GRAY_LT = "#a9a79f", "#d6d4cc"
SURFACE = "#ffffff"

plt.rcParams.update({
    "font.family": "Avenir Next",
    "font.size": 8.5,
    "axes.edgecolor": AXIS,
    "axes.labelcolor": INK2,
    "axes.linewidth": 0.8,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "svg.fonttype": "path",
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})

W = 6.7  # inches, full text width on A4 with 20 mm margins


def fbc():
    rows = list(csv.DictReader(open(OUT / "forecast_by_category.csv")))
    d = {}
    for r in rows:
        d[(r["category"], int(r["year"]))] = r
    return d


def f(x):
    return float(x) if x not in ("", None) else None


def source(fig, text, y=0.012):
    fig.text(0.012, y, text, ha="left", va="bottom", fontsize=6.8, color=MUTED, wrap=True)


def hgrid(ax):
    ax.yaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)


def save(fig, name):
    fig.savefig(FIG / f"{name}.svg")
    plt.close(fig)


# ---------------------------------------------------------------- (a) bits by category
def chart_bits():
    d = fbc()
    years = [2023, 2024, 2025, 2026, 2027]

    def med(cat, y):
        return f(d[(cat, y)]["median_bn_gb"])

    series = [
        ("Server ECC (RDIMM)", S1, lambda y: med("server_ecc", y)),
        ("HBM", S2, lambda y: med("hbm", y)),
        ("Server LPDDR (SOCAMM)", S3, lambda y: med("lpddr_lps", y)),
        ("Phone and tablet LPDDR", S4, lambda y: med("lpddr_mob", y)),
        ("PCs (DDR5/DDR4 + LPDDR)", S5, lambda y: med("client_pc", y) + med("lpddr_pclp", y)),
        ("GDDR, auto, consumer", S6, lambda y: med("gddr", y) + med("lpddr_auto", y) + med("other_consumer", y)),
    ]
    fig, ax = plt.subplots(figsize=(W, 3.3))
    fig.subplots_adjust(left=0.08, right=0.70, top=0.95, bottom=0.12)
    x = range(len(years))
    bottoms = [0.0] * len(years)
    bw = 0.5
    tops = {}
    for name, col, fn in series:
        vals = [fn(y) for y in years]
        ax.bar(x, vals, bw, bottom=bottoms, color=col, edgecolor=SURFACE, linewidth=1.2, label=name)
        tops[name] = [(b, v) for b, v in zip(bottoms, vals)]
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    for i, y in enumerate(years):
        tot = med("total", y)
        lab = f"{tot:.0f}" if y < 2026 else f"{tot:.0f}*"
        ax.text(i, bottoms[i] + 6, lab, ha="center", va="bottom", fontsize=8, color=INK, fontweight="demibold")
    # direct labels on the 2027 column, right side, with leader lines
    i = len(years) - 1
    label_y = []
    for name, col, fn in series:
        b, v = tops[name][i]
        label_y.append([name, b + v / 2, v, col])
    # spread labels to avoid collisions (min gap 21 bn Gb)
    gap = 21
    for k in range(1, len(label_y)):
        if label_y[k][1] - label_y[k - 1][1] < gap:
            label_y[k][1] = label_y[k - 1][1] + gap
    for name, ly, v, col in label_y:
        seg_mid = [tb + tv / 2 for (tb, tv) in [tops[name][i]]][0]
        ax.plot([i + bw / 2 + 0.03, i + 0.62, i + 0.72], [seg_mid, seg_mid, ly], color=AXIS, lw=0.7, clip_on=False)
        ax.text(i + 0.76, ly, f"{name}  {v:.0f}", va="center", ha="left", fontsize=7.6, color=INK2, clip_on=False)
    ax.set_xticks(list(x))
    ax.set_xticklabels([str(y) for y in years[:3]] + ["2026\nmodel", "2027\nmodel"])
    ax.set_ylabel("bn Gb (1 EB = 8 bn Gb)")
    ax.set_ylim(0, 500)
    ax.set_xlim(-0.5, 4.5)
    hgrid(ax)
    save(fig, "a_bits_by_category")


# ---------------------------------------------------------------- (b) HBM squeeze
def chart_hbm():
    years = ["End-2025", "End-2026", "End-2027"]
    wafers = [18, 22, 30]
    bits = [8, 9, 13]
    fig, ax = plt.subplots(figsize=(W, 2.6))
    fig.subplots_adjust(left=0.07, right=0.98, top=0.86, bottom=0.17)
    bw = 0.3
    xs = list(range(3))
    ax.bar([x - bw / 2 - 0.02 for x in xs], wafers, bw, color=S1, label="Share of DRAM wafer input")
    ax.bar([x + bw / 2 + 0.02 for x in xs], bits, bw, color=S2, label="Share of DRAM bit output")
    for x, w_, b_ in zip(xs, wafers, bits):
        ax.text(x - bw / 2 - 0.02, w_ + 0.6, f"{w_}%", ha="center", va="bottom", fontsize=8.5, color=INK, fontweight="demibold")
        ax.text(x + bw / 2 + 0.02, b_ + 0.6, f"{b_}%", ha="center", va="bottom", fontsize=8.5, color=INK, fontweight="demibold")
    ax.set_xticks(xs)
    ax.set_xticklabels([f"{y}\n{w_ / b_:.1f}× wafer share / bit share" for y, w_, b_ in zip(years, wafers, bits)])
    ax.set_ylim(0, 35)
    ax.set_xlim(-0.6, 2.6)
    ax.set_yticks([0, 10, 20, 30])
    ax.set_yticklabels(["0%", "10%", "20%", "30%"])
    hgrid(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.2), ncol=2, frameon=False, fontsize=8, handlelength=1.0)
    save(fig, "b_hbm_squeeze")


# ---------------------------------------------------------------- (c) 2027 shortfall by segment
def chart_gap():
    d = fbc()
    rows = [
        ("Server LPDDR (SOCAMM)", "lpddr_lps", "hi"),
        ("Phone and tablet LPDDR †", "lpddr_mob", "pre"),
        ("Server ECC (RDIMM)", "server_ecc", "base"),
        ("HBM", "hbm", "base"),
        ("Client PC (DDR5/DDR4) †", "client_pc", "pre"),
        ("PC LPDDR †", "lpddr_pclp", "pre"),
        ("Auto LPDDR", "lpddr_auto", "base"),
        ("Other / consumer", "other_consumer", "base"),
    ]
    data = []
    for name, cat, kind in rows:
        r = d[(cat, 2027)]
        data.append((name, f(r["gap_median_bn_gb"]), f(r["gap_p10_bn_gb"]), f(r["gap_p90_bn_gb"]), f(r["gap_median"]), kind))
    fig, ax = plt.subplots(figsize=(W, 3.2))
    fig.subplots_adjust(left=0.25, right=0.98, top=0.98, bottom=0.15)
    ys = list(range(len(data)))[::-1]
    for y, (name, g, lo, hi, pct, kind) in zip(ys, data):
        col = {"hi": S3, "base": GRAY, "pre": GRAY_LT}[kind]
        ax.barh(y, g, 0.52, color=col)
        lab = f"{g:+.1f}  ({pct * 100:+.0f}%)".replace("-", "\u2212")
        if kind == "hi":
            ax.text(g - 0.8, y, lab, ha="right", va="center", fontsize=8.2, color=INK, fontweight="demibold")
            ax.text(1.2, y, "Fixed at 60% of Nvidia's need (TrendForce)",
                    ha="left", va="center", fontsize=7, color=INK2)
        else:
            for xx in (lo, hi):
                ax.plot([xx, xx], [y - 0.13, y + 0.13], color=MUTED, lw=0.8)
            ax.plot([lo, hi], [y, y], color=MUTED, lw=0.8)
            ax.text(hi + 1.0, y, lab, ha="left", va="center", fontsize=7.6, color=INK2)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in data], fontsize=8, color=INK)
    ax.axvline(0, color=INK2, lw=0.8)
    ax.set_xlim(-50, 42)
    ax.set_xlabel("2027 supply minus demand, bn Gb (negative = short). Whiskers: 80% range of the model draws.", fontsize=7.6)
    ax.xaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    save(fig, "c_gap_2027")


# ---------------------------------------------------------------- (d) prices
def chart_prices():
    q = ["1Q25", "2Q25", "3Q25", "4Q25", "1Q26", "2Q26", "3Q26", "4Q26"]
    lo = [-13, -5, 10, 45, 93, 58, 13, 10]
    hi = [-8, 0, 15, 50, 98, 63, 18, 15]
    actual = [False, False, False, True, True, False, False, False]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(W, 3.0), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.28))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.83, bottom=0.1)
    xs = range(len(q))
    for x, a, b, act in zip(xs, lo, hi, actual):
        m = (a + b) / 2
        ax1.bar(x, m, 0.55, color=S1 if act else BLUE_250)
        ax1.plot([x, x], [a, b], color=INK, lw=0.9)
        if a < 0:
            ax1.text(x, a - 3, f"\u2212{-a} to\n{'\u2212' if b < 0 else ''}{abs(b)}", ha="center", va="top", fontsize=6.4, color=INK2)
        else:
            ax1.text(x, b + 3, f"+{a}–{b}", ha="center", va="bottom", fontsize=6.4, color=INK2)
    ax1.axhline(0, color=INK2, lw=0.8)
    ax1.set_xticks(list(xs))
    ax1.set_xticklabels(q, fontsize=7.4)
    ax1.set_ylim(-36, 112)
    ax1.set_yticks([0, 25, 50, 75, 100])
    ax1.set_yticklabels(["0%", "+25%", "+50%", "+75%", "+100%"])
    hgrid(ax1)
    ax1.set_title("Conventional DRAM contract price, change vs prior quarter", fontsize=8.2, color=INK, loc="left", pad=16)
    from matplotlib.patches import Patch
    ax1.legend(handles=[Patch(color=S1, label="Reported"), Patch(color=BLUE_250, label="Forecast (latest)")],
               loc="upper left", bbox_to_anchor=(0, 1.1), ncol=2, frameon=False, fontsize=7.2, handlelength=1.0)

    import datetime as dt
    pts = [("2025-02-05", 1.458), ("2025-03-19", 1.486), ("2025-09-23", 5.947), ("2025-11-18", 12.757),
           ("2025-12-30", 23.746), ("2026-03-31", 33.96), ("2026-06-16", 35.8), ("2026-07-28", 42.08), ("2026-10-20", 46.357)]
    xd = [dt.date.fromisoformat(a) for a, _ in pts]
    yv = [b for _, b in pts]
    ax2.plot(xd, yv, color=S1, lw=2, solid_capstyle="round")
    ax2.scatter(xd, yv, s=16, color=S1, edgecolor=SURFACE, linewidth=1.2, zorder=3)
    d5 = [dt.date(2025, 3, 19), dt.date(2026, 10, 30)]
    ax2.scatter(d5, [4.95, 61.5], s=26, color=S2, edgecolor=SURFACE, linewidth=1.2, zorder=4, marker="D")
    ax2.set_yscale("log")
    ax2.set_yticks([1, 2, 5, 10, 20, 50, 100])
    ax2.set_yticklabels(["$1", "$2", "$5", "$10", "$20", "$50", "$100"])
    ax2.minorticks_off()
    ax2.set_ylim(0.9, 120)
    hgrid(ax2)
    ax2.text(xd[0] + dt.timedelta(days=10), 1.32, "DDR4 8Gb $1.46", fontsize=6.8, color=INK2, ha="left", va="top")
    ax2.text(xd[-1], 38, "$46.36\n(×32)", fontsize=6.8, color=INK2, ha="right", va="top")
    ax2.text(d5[0] - dt.timedelta(days=30), 6.2, "DDR5 16Gb $4.95", fontsize=6.8, color=INK2, ha="left", va="bottom")
    ax2.text(d5[1] - dt.timedelta(days=10), 75, "DDR5 16Gb $61.50", fontsize=6.8, color=INK2, ha="right", va="bottom")
    import matplotlib.dates as mdates
    ax2.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax2.tick_params(axis="x", labelsize=7.4)
    ax2.set_title("Spot price per chip (log scale)", fontsize=8.2, color=INK, loc="left", pad=16)
    from matplotlib.lines import Line2D
    ax2.legend(handles=[Line2D([], [], color=S1, lw=2, marker="o", ms=4, label="DDR4 8Gb, weekly average"),
                        Line2D([], [], color=S2, lw=0, marker="D", ms=4.5, label="DDR5 16Gb (two readings)")],
               loc="lower right", ncol=1, frameon=False, fontsize=7.0, handlelength=1.4)
    save(fig, "d_prices")


# ---------------------------------------------------------------- (e) fab timeline
def chart_fabs():
    import datetime as dt
    D = dt.date
    rows = [
        # label, start, marker label, kind ('done','start','late'), note
        ("SK hynix M15X (Cheongju)", D(2026, 12, 31), "full capacity end-2026, for HBM4", "hbm"),
        ("Samsung P4 (Pyeongtaek)", D(2026, 10, 1), "operating", "now"),
        ("SK hynix Yongin Phase 1", D(2027, 2, 15), "cleanroom opens early 2027", "new"),
        ("Micron ID1 (Idaho)", D(2027, 7, 1), "wafer output mid-2027", "new"),
        ("Micron Tongluo (Taiwan)", D(2027, 7, 1), "meaningful shipments mid-2027", "new"),
        ("Samsung P5 (Pyeongtaek)", D(2028, 1, 1), "operations 2028*", "late"),
        ("Micron ID2 (Idaho)", D(2028, 10, 1), "wafer output late 2028", "late"),
        ("Micron Hiroshima expansion", D(2028, 10, 1), "initial output late 2028", "late"),
        ("Micron New York fab 1", D(2030, 6, 30), "initial output 2030", "late"),
    ]
    fig, ax = plt.subplots(figsize=(W, 3.4))
    fig.subplots_adjust(left=0.27, right=0.98, top=0.9, bottom=0.08)
    x0, x1 = D(2026, 1, 1), D(2031, 1, 1)
    ax.axvspan(D(2027, 7, 1), D(2028, 1, 1), color="#eef4fc", zorder=0)
    ax.axvspan(D(2028, 1, 1), D(2029, 1, 1), color="#dbe8f9", zorder=0)
    ax.text(D(2027, 12, 20), len(rows) + 0.05, "From mid-2027:\nfirst new output", ha="right", va="bottom", fontsize=6.8, color=INK2)
    ax.text(D(2028, 1, 12), len(rows) + 0.05, "2028: substantial new\noutput (TrendForce)", ha="left", va="bottom", fontsize=6.8, color=INK2)
    for i, (name, start, note, kind) in enumerate(rows):
        y = len(rows) - 1 - i
        col = {"hbm": S2, "now": GRAY, "new": S1, "late": BLUE_250}[kind]
        ax.plot([start, x1], [y, y], color=col, lw=2.0, alpha=0.35, solid_capstyle="butt")
        ax.scatter([start], [y], s=34, color=col, edgecolor=SURFACE, linewidth=1.4, zorder=3)
        ha = "left"
        tx = start + dt.timedelta(days=40)
        if start > D(2029, 6, 1):
            ha, tx = "right", start - dt.timedelta(days=40)
        ax.text(tx, y + 0.18, note, fontsize=6.9, color=INK2, ha=ha, va="bottom")
        ax.text(x0 - dt.timedelta(days=30), y, name, fontsize=7.8, color=INK, ha="right", va="center")
    ax.set_yticks([])
    ax.set_ylim(-0.6, len(rows) + 1.0)
    ax.set_xlim(x0, x1)
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.spines["left"].set_visible(False)
    ax.xaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([], [], color=S2, marker="o", lw=0, ms=5, label="HBM fab, already full"),
                       Line2D([], [], color=S1, marker="o", lw=0, ms=5, label="New space, first output in 2027"),
                       Line2D([], [], color=BLUE_250, marker="o", lw=0, ms=5, label="New space, 2028 or later")],
              loc="upper left", bbox_to_anchor=(-0.36, 1.13), ncol=3, frameon=False, fontsize=7.2, handlelength=0.8)
    save(fig, "e_fab_timeline")


if __name__ == "__main__":
    chart_bits()
    chart_hbm()
    chart_gap()
    chart_prices()
    chart_fabs()
    print("wrote", sorted(p.name for p in FIG.glob("*.svg")))


# ---------------------------------------------------------------- (f) tornado from out/sensitivity.csv
def chart_tornado():
    rows = list(csv.DictReader(open(OUT / "sensitivity.csv")))
    rows = [r for r in rows if r["input"] != "g_srv27"]
    names = {
        "n27": "Node-migration bit gain", "g26": "2026 industry growth", "r27": "HBM wafer trade ratio",
        "cxmt27": "CXMT 2027 capacity", "h27": "HBM share of wafers", "yongin": "SK hynix Yongin Ph. 1",
        "samsung_add": "Samsung P4 ramp", "id1": "Micron ID1 (Idaho)", "tongluo": "Micron Tongluo (Taiwan)",
        "m15x": "SK hynix M15X pull-in", "ru_content": "Rubin Ultra HBM per package",
    }
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(W, 3.4), sharey=True, gridspec_kw=dict(wspace=0.12, width_ratios=[1.25, 1]))
    fig.subplots_adjust(left=0.25, right=0.98, top=0.78, bottom=0.08)
    ys = list(range(len(rows)))[::-1]
    for y, r in zip(ys, rows):
        b = f(r["supply_model_2027_base"])
        lo, hi = f(r["supply_model_2027_at_p10"]) - b, f(r["supply_model_2027_at_p90"]) - b
        a1.barh(y, lo, 0.55, color=S1)
        a1.barh(y, hi, 0.55, color=S2)
        hb = f(r["hbm_sufficiency_2027_base"])
        l2, h2 = (f(r["hbm_sufficiency_2027_at_p10"]) - hb) * 100, (f(r["hbm_sufficiency_2027_at_p90"]) - hb) * 100
        a2.barh(y, l2, 0.55, color=S1)
        a2.barh(y, h2, 0.55, color=S2)
    for ax in (a1, a2):
        ax.axvline(0, color=INK2, lw=0.8)
        ax.xaxis.grid(True, color=GRID, linewidth=0.7)
        ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False)
    a1.set_yticks(ys)
    a1.set_yticklabels([names[r["input"]] for r in rows], fontsize=7.8, color=INK)
    a1.set_xlim(-25, 25)
    a2.set_xlim(-15, 15)
    a1.set_title("2027 supply, supply-side model\nchange from base of 445.1 bn Gb", fontsize=8, color=INK, loc="left")
    a2.set_title("2027 HBM sufficiency\nchange from base of −9.9%, points", fontsize=8, color=INK, loc="left")
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=S1, label="Input at its 10th percentile"), Patch(color=S2, label="Input at its 90th percentile")],
               loc="upper left", bbox_to_anchor=(0.25, 1.0), ncol=2, frameon=False, fontsize=7.4, handlelength=1.0)
    save(fig, "f_tornado")


if __name__ == "__main__":
    chart_tornado()


# ---------------------------------------------------------------- (g) bits and capacity by company
def src_rows(fname, lines):
    rows = list(csv.DictReader(open(ROOT / "sources" / fname, newline="")))
    return [float(rows[n - 2]["value"].replace(",", "")) for n in lines]


def chart_vendors():
    years = [2023, 2024, 2025, 2026, 2027]
    # Mirae Asset, 15 Dec 2025, p.16 table. total-dram.csv rows (header = line 1).
    sam = src_rows("total-dram.csv", range(202, 207))
    skh = src_rows("total-dram.csv", range(207, 212))
    mu = src_rows("total-dram.csv", range(212, 217))
    # Industry total production 2023-2027 from the quote of hbm-gddr.csv:222.
    tot = [200.2, 235.0, 293.1, 352.5, 415.7]
    oth = [t - a - b - c for t, a, b, c in zip(tot, sam, skh, mu)]
    k_sam = src_rows("total-dram.csv", range(237, 242))
    k_skh = src_rows("total-dram.csv", range(242, 247))
    k_mu = src_rows("total-dram.csv", range(247, 252))
    k_tot = src_rows("total-dram.csv", range(232, 237))
    k_oth = [t - a - b - c for t, a, b, c in zip(k_tot, k_sam, k_skh, k_mu)]

    names = ["Samsung", "SK hynix", "Micron", "Others (CXMT, Nanya and others)"]
    cols = [S1, S2, S3, S4]
    label_ink = [SURFACE, INK, INK, INK]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(W, 3.25), gridspec_kw=dict(width_ratios=[1, 1], wspace=0.22))
    fig.subplots_adjust(left=0.07, right=0.99, top=0.80, bottom=0.10)
    x = list(range(len(years)))
    bw = 0.62

    def stack(ax, series, totals, unit_fmt, share_labels):
        bottoms = [0.0] * len(years)
        for (vals, col, name, ink) in series:
            ax.bar(x, vals, bw, bottom=bottoms, color=col, edgecolor=SURFACE, linewidth=1.2, label=name)
            if share_labels:
                for i, (b, v) in enumerate(zip(bottoms, vals)):
                    sh = v / totals[i] * 100
                    if v / max(totals) > 0.045:
                        ax.text(i, b + v / 2, f"{sh:.0f}%", ha="center", va="center", fontsize=6.6, color=ink)
                    else:
                        ax.text(i + bw / 2 + 0.04, b + v / 2, f"{sh:.0f}%", ha="left", va="center", fontsize=6.6,
                                color=INK2)
            bottoms = [b + v for b, v in zip(bottoms, vals)]
        for i, t in enumerate(totals):
            ax.text(i, t + max(totals) * 0.015, unit_fmt(t), ha="center", va="bottom", fontsize=7.6,
                    color=INK, fontweight="demibold")
        ax.set_xticks(x)
        ax.set_xticklabels([str(y) if y < 2026 else f"{y}F" for y in years])
        ax.set_xlim(-0.55, len(years) - 0.45)
        hgrid(ax)

    stack(a1, list(zip([sam, skh, mu, oth], cols, names, label_ink)), tot, lambda t: f"{t:.0f}", True)
    a1.set_ylim(0, 450)
    a1.set_title("Bit output, bn Gb, with share of industry bits", loc="left", fontsize=8, color=INK2, pad=6)

    stack(a2, list(zip([k_sam, k_skh, k_mu, k_oth], cols, names, label_ink)), k_tot,
          lambda t: f"{t:,.0f}", True)
    a2.set_ylim(0, 2420)
    a2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    a2.set_title("Wafer capacity, thousand wafers a month, with share", loc="left", fontsize=8, color=INK2, pad=6)

    h, l = a1.get_legend_handles_labels()
    fig.legend(h, l, loc="upper left", bbox_to_anchor=(0.06, 1.0), ncol=4, frameon=False, fontsize=7.6,
               handlelength=1.0, handleheight=0.8, columnspacing=1.4)
    save(fig, "g_vendors")
    return dict(tot=tot, oth=oth, k_oth=k_oth, k_tot=k_tot, sam=sam, skh=skh, mu=mu)


if __name__ == "__main__":
    v = chart_vendors()
    for k, vals in v.items():
        print(k, [round(x, 1) for x in vals])


# ---------------------------------------------------------------- (h) company x memory type
def chart_vendor_type():
    import matplotlib.colors as mcolors
    rows = list(csv.DictReader(open(OUT / "vendor_by_type.csv", newline="")))
    vt = {(r["year"], r["vendor"], r["type"]): r for r in rows}
    vendors = ["Samsung", "SK hynix", "Micron", "CXMT", "Nanya + others"]
    vlabel = ["Samsung", "SK hynix", "Micron", "CXMT", "Nanya +\nothers"]
    # stacked segments: report category colours (Figure 2)
    segs = [
        ("Server ECC", S1, ["server_ecc"]),
        ("HBM", S2, ["hbm"]),
        ("LPDDR (all uses)", S4, ["lpddr"]),
        ("Client PC", S5, ["client_pc"]),
        ("GDDR and other", S6, ["gddr", "other_consumer"]),
    ]
    fig = plt.figure(figsize=(W, 2.9))
    a1 = fig.add_axes([0.07, 0.17, 0.50, 0.62])
    a2 = fig.add_axes([0.655, 0.06, 0.335, 0.77])
    bw = 0.36
    for vi, v in enumerate(vendors):
        for yi, y in enumerate(["2026", "2027"]):
            xpos = vi + (yi - 0.5) * (bw + 0.04)
            b = 0.0
            for name, col, types in segs:
                val = sum(float(vt[(y, v, t)]["median_bn_gb"]) for t in types)
                a1.bar(xpos, val, bw, bottom=b, color=col, edgecolor=SURFACE, linewidth=0.9,
                       label=name if (vi == 0 and yi == 0) else None)
                b += val
            a1.text(xpos, b + 2, f"{float(vt[(y, v, 'total')]['median_bn_gb']):.0f}", ha="center", va="bottom", fontsize=6.6, color=INK)
            a1.text(xpos, -4, "'" + y[2:], ha="center", va="top", fontsize=6.6, color=MUTED)
    a1.set_xticks(range(len(vendors)))
    a1.set_xticklabels(vlabel, fontsize=7.6)
    a1.tick_params(axis="x", pad=13)
    a1.set_ylim(0, 172)
    a1.set_xlim(-0.6, len(vendors) - 0.4)
    a1.set_ylabel("bn Gb", fontsize=7.6)
    hgrid(a1)
    a1.set_title("Output by memory type, 2026 and 2027 (bn Gb)", loc="left", fontsize=8, color=INK2, pad=4)
    h, l = a1.get_legend_handles_labels()
    fig.legend(h, l, loc="upper left", bbox_to_anchor=(0.06, 1.0), ncol=5, frameon=False, fontsize=7.2,
               handlelength=1.0, handleheight=0.8, columnspacing=1.1)

    # heat table: share of each type, 2026 -> 2027
    cols = [("server_ecc", "Server\nECC"), ("hbm", "HBM"), ("lpddr", "LPDDR"), ("client_pc", "Client\nPC"),
            ("gddr", "GDDR"), ("other_consumer", "Other")]
    cmap = mcolors.LinearSegmentedColormap.from_list("seq", ["#f2f6fc", "#9cc3ef", "#2a78d6", "#123d73"])
    a2.set_xlim(0, len(cols))
    a2.set_ylim(len(vendors), -1.15)
    a2.axis("off")
    for ci, (t, lab) in enumerate(cols):
        a2.text(ci + 0.5, -0.12, lab, ha="center", va="bottom", fontsize=6.8, color=INK2)
    for vi, v in enumerate(vendors):
        a2.text(-0.08, vi + 0.5, vlabel[vi].replace("\n", " ") if v != "Nanya + others" else "Nanya +\nothers",
                ha="right", va="center", fontsize=6.8, color=INK2)
        for ci, (t, lab) in enumerate(cols):
            s26 = float(vt[("2026", v, t)]["share_of_type"]) * 100
            s27 = float(vt[("2027", v, t)]["share_of_type"]) * 100
            col = cmap(min(s27 / 65, 1.0))
            a2.add_patch(plt.Rectangle((ci + 0.03, vi + 0.04), 0.94, 0.92, color=col, lw=0))
            ink = SURFACE if s27 >= 40 else INK
            txt = "0" if (s26 < 0.05 and s27 < 0.05) else f"{s26:.0f} › {s27:.0f}"
            a2.text(ci + 0.5, vi + 0.5, txt, ha="center", va="center", fontsize=6.5, color=ink)
    a2.text(-1.25, -1.1, "Share of each type, 2026 › 2027 (%)", ha="left", va="bottom", fontsize=8, color=INK2)
    save(fig, "h_vendor_type")


if __name__ == "__main__":
    chart_vendor_type()
