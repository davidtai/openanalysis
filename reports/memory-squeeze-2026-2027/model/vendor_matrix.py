#!/usr/bin/env python3
"""DRAM bits by vendor x RAM type, 2025-2027.

Run from the project folder:  .venv/bin/python -I model/vendor_matrix.py

It imports model/forecast.py and reuses its Monte Carlo draws (same seed), so the
column totals here are the category draws of the main model. Steps per draw:

1. Rows: Mirae vendor bit-production shares (total-dram.csv) x the model total.
   "Nanya + others" = Mirae industry production minus Samsung, SK hynix, Micron, CXMT.
2. Columns: the six model buckets.
3. HBM cells first: vendor HBM bit shares drawn from the broker rows (vendor-mix.csv,
   hbm-gddr.csv), normalised to 1, times the HBM column.
4. Other cells: the prior mix (sources/vendor-mix-notes.md section 2) with per-cell
   gamma noise (weak cells noisier), then RAS/IPF to the residual row and column sums.

Writes out/vendor_by_type.csv, out/vendor_by_type_sensitivity.csv,
out/inputs_used_vendor.csv and out/charts/05_vendor_by_type.png.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forecast as F  # noqa: E402  (runs the source loading and backtest; main() is not called)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

VM = "vendor-mix"
F.T[VM] = pd.read_csv(F.SRC_DIR / "vendor-mix.csv", dtype=str, keep_default_na=False)
F.USED.clear()                      # record only the rows this script reads
TD, HG, MIRAE = F.TD, F.HG, F.MIRAE
YEARS = (2025, 2026, 2027)
VENDORS = ["Samsung", "SK hynix", "Micron", "CXMT", "Nanya + others"]
TYPES = ["server_ecc", "lpddr", "client_pc", "hbm", "gddr", "other_consumer"]
NONHBM = [t for t in TYPES if t != "hbm"]
N = F.N_DRAWS

# --------------------------------------------------------------------------
# Assumptions for this step (also listed in METHOD.md section 17).
# --------------------------------------------------------------------------
V_ASSUMPTIONS = {
    "prior_mix": dict(
        value="sources/vendor-mix-notes.md section 2 (bit basis, % of own bits)",
        reason="No source publishes a vendor x application bit matrix. The researcher built the prior "
               "from the vendor-mix.csv rows (SK hynix slides, Micron business units, CXMT prospectus, "
               "Nanya call, broker HBM/SOCAMM/GDDR shares). We use it as given, with noise."),
    "prior_noise_concentration": dict(
        value={"strong": 100, "medium": 25, "weak": 6},
        reason="Each non-HBM prior cell gets gamma noise with mean = prior and CV = 1/sqrt(k): 10% "
               "(strong), 20% (medium), 41% (weak). A plain Dirichlet cannot give cells of one row "
               "different precision without moving the mean, so we draw independent gammas and then "
               "renormalise the row (the same construction as a Dirichlet when all k are equal)."),
    "hbm_share_draw": dict(
        value="per vendor tri(min, median, max) over broker points, then normalised to 1",
        reason="Brokers disagree (2027: Samsung 39-42%, SK hynix 35-41%). The normalisation absorbs "
               "rounding and the China remainder."),
    "cxmt_hbm_share": dict(
        value="the remainder each broker leaves after Samsung, SK hynix and Micron",
        reason="Daishin's chart leaves ~3% (2026) and ~4% (2027) for China; Samsung Securities, Citi "
               "and UBS leave 0-1%. SemiAnalysis: CXMT had 1% of HBM wafers in 2025 at low yield."),
    "rows_fixed_shares": dict(
        value="Mirae Dec 2025 vendor production shares, no noise",
        reason="Mirae is the only source with bits by vendor for 2025-2027. The shipment-page split "
               "is run as a sensitivity instead of as noise."),
}

# Cell confidence (notes section 2, with the coordinator's override: PC and Other weak for
# every vendor; SK hynix server/LPDDR and CXMT LPDDR strong).
CONF = {
    "Samsung":        dict(server_ecc="weak", lpddr="weak", client_pc="weak", gddr="medium", other_consumer="weak"),
    "SK hynix":       dict(server_ecc="strong", lpddr="strong", client_pc="weak", gddr="weak", other_consumer="weak"),
    "Micron":         dict(server_ecc="medium", lpddr="medium", client_pc="weak", gddr="weak", other_consumer="weak"),
    "CXMT":           dict(server_ecc="weak", lpddr="strong", client_pc="weak", gddr="weak", other_consumer="weak"),
    "Nanya + others": dict(server_ecc="weak", lpddr="weak", client_pc="weak", gddr="weak", other_consumer="weak"),
}

# Prior mix, % of each vendor's own bits: server ECC, LPDDR, client PC, HBM, GDDR, other.
# Source: sources/vendor-mix-notes.md section 2 "Recommended prior" (researcher judgment
# built from the vendor-mix.csv rows; see the "How each row was set" bullets there).
PRIOR = {
    2025: {"Samsung": (39, 46, 5, 4.5, 4.5, 1), "SK hynix": (46, 26, 8, 14.5, 3, 2.5),
           "Micron": (34, 42, 7, 8, 2, 7), "CXMT": (8, 66, 14, 0, 0, 12), "Nanya + others": (15, 30, 10, 0, 0, 45)},
    2026: {"Samsung": (44, 38, 3.5, 8, 4, 2.5), "SK hynix": (50, 22, 7, 15.5, 2.5, 3),
           "Micron": (40, 36, 5, 10, 1, 8), "CXMT": (15, 60, 13, 1, 0, 11), "Nanya + others": (25, 35, 15, 0, 0, 25)},
    2027: {"Samsung": (42, 36, 3, 14, 3.5, 1.5), "SK hynix": (47, 25, 6, 16, 2.5, 3.5),
           "Micron": (38, 37, 5, 13, 1, 6), "CXMT": (18, 55, 12, 4, 0, 11), "Nanya + others": (25, 35, 15, 0, 0, 25)},
}

# --------------------------------------------------------------------------
# Row shares: Mirae vendor bit production (total-dram.csv, Mirae 2025-12-15 p.16).
# --------------------------------------------------------------------------


def mirae_row_shares(y):
    ind = F.num(TD, "total", "bit production", str(y), MIRAE)
    v = {k: F.num(TD, "total", f"{k} bit production", str(y), MIRAE) for k in ("Samsung", "SK hynix", "Micron", "CXMT")}
    v["Nanya + others"] = ind - sum(v.values())          # Nanya 4.0-4.8 plus Mirae's unnamed residual
    return {k: x / ind for k, x in v.items()}


ROW_SHARE = {y: mirae_row_shares(y) for y in YEARS}
F.num(TD, "total", "Nanya bit production", "2026", MIRAE)  # cited: part of the residual row


def shipment_row_shares(y):
    """Sensitivity: split Samsung + SK hynix by Mirae's quarterly shipment pages instead.

    The shipment pages exist for 2025Q1-2026Q4; 2027 uses the 2026 split.
    """
    yy = min(y, 2026)
    sam = sum(F.num(TD, "total", "Samsung DRAM bit shipments", f"{yy}Q{q}", MIRAE) for q in (1, 2, 3, 4))
    skh = sum(F.num(TD, "total", "SK hynix DRAM bit shipments", f"{yy}Q{q}", MIRAE) for q in (1, 2, 3, 4))
    s = dict(ROW_SHARE[y])
    both = s["Samsung"] + s["SK hynix"]
    s["Samsung"], s["SK hynix"] = both * sam / (sam + skh), both * skh / (sam + skh)
    return s


# --------------------------------------------------------------------------
# HBM vendor bit-share points (%), by year. Order: Samsung, SK hynix, Micron, CXMT.
# --------------------------------------------------------------------------
SS, DS = "Samsung Securities", "Daishin Securities"
CITI, VLSI = "Citi (via NeoTeo)", "VLSI Korea"


def vm(metric, period, publisher):
    d = F.T[VM]
    hit = d[(d["metric"] == metric) & (d["period"] == period) & d["publisher"].str.startswith(publisher)]
    if len(hit) != 1:
        raise KeyError(f"{metric} {period} {publisher}: {len(hit)} rows")
    i = int(hit.index[0])
    F.USED[(VM, i)] = hit.loc[i]
    return hit.loc[i]


def vmn(metric, period, publisher):
    return F.parse_num(vm(metric, period, publisher)["value"])


def full_set(pub, y):
    s, k, m = (vmn(f"{v} HBM market share", str(y), pub) for v in ("Samsung", "SK hynix", "Micron"))
    return [s, k, m, max(0.0, 100 - s - k - m)]


HBM_PTS = {y: {v: [] for v in VENDORS[:4]} for y in YEARS}
for y in YEARS:
    sets = [full_set(SS, y)] if y <= 2026 else []
    sets.append(full_set(DS, y))
    for st in sets:
        for v, x in zip(VENDORS[:4], st):
            HBM_PTS[y][v].append(x)
# JPMorgan SK hynix 60 / 46 / 41 (the 2025 value is in the quote of the 2026 row).
_jpm = vm("SK hynix HBM market share", "2026", VLSI)
HBM_PTS[2025]["SK hynix"].append(float(re.search(r"from (\d+)% in 2025", _jpm["quote"]).group(1)))
HBM_PTS[2026]["SK hynix"].append(F.parse_num(_jpm["value"]))
HBM_PTS[2027]["SK hynix"].append(vmn("SK hynix HBM market share", "2027", VLSI))
# Citi: Samsung 30 (2026), 42/35/22 (2027); SK hynix 47 in 2026 and Micron "remain at 22%".
_citi_sk = vm("SK hynix HBM market share", "2027", CITI)
HBM_PTS[2026]["Samsung"].append(vmn("Samsung HBM market share", "2026", CITI))
HBM_PTS[2026]["SK hynix"].append(float(re.search(r"estimated (\d+)%", _citi_sk["quote"]).group(1)))
HBM_PTS[2026]["Micron"].append(vmn("Micron HBM market share", "2027", CITI))
_c27 = [vmn("Samsung HBM market share", "2027", CITI), F.parse_num(_citi_sk["value"]),
        vmn("Micron HBM market share", "2027", CITI)]
for v, x in zip(VENDORS[:4], _c27 + [max(0.0, 100 - sum(_c27))]):
    HBM_PTS[2027][v].append(x)
# UBS: SK hynix 48% of 2026 bits; 2027 Samsung 41 / SK hynix 39 / Micron ~20.
HBM_PTS[2026]["SK hynix"].append(F.num(HG, "hbm-skhynix", "bit_share", "2026", "UBS (via Seoul Economic Daily)"))
HBM_PTS[2027]["Samsung"].append(vmn("Samsung HBM market share", "2027", VLSI))
_ubs = F.src(HG, "hbm", "bit_share_SKH/Samsung", "2027", "UBS (via Seoul Economic Daily)")["value"]
HBM_PTS[2027]["SK hynix"].append(float(_ubs.split("/")[0]))
_ubs_mu = float(re.search(r"Micron ~(\d+)", F.src(HG, "hbm", "bit_share_by_vendor", "2027", "UBS (via Investing.com)")["value"]).group(1))
HBM_PTS[2027]["Micron"].append(_ubs_mu)
HBM_PTS[2027]["CXMT"].append(max(0.0, 100 - 41 - float(_ubs.split("/")[0]) - _ubs_mu))
# Cross-checks only (revenue basis): Counterpoint 2Q26 50/33/18; CXMT 1% of HBM wafers (2025).
CP_2Q26 = {v: vmn(f"{v} HBM market share", "2026Q2", "Counterpoint Research (via Seoul") for v in ("Samsung", "SK hynix", "Micron")}
vm("CXMT share of global HBM wafer supply", "2025", "SemiAnalysis")

# Rows cited as the basis of the prior (notes section 2) and for checks.
for metric, period, pub in [
    ("Samsung GDDR7 market share", "2025", "TrendForce"), ("Samsung GDDR market share", "2024", "TrendForce"),
    ("SK hynix GDDR market share", "2024", "TrendForce"), ("Samsung mobile DRAM market share", "2024Q1", "Omdia"),
    ("CXMT LPDDR series share of main-business revenue", "2025", "CXMT"),
    ("CXMT DDR series (DDR4+DDR5) share of main-business revenue", "2025", "CXMT"),
    ("Nanya DDR4 + LPDDR4 share of revenue", "2026Q3", "Nanya"), ("Nanya DDR5 share of revenue", "2026Q3", "Focus Taiwan"),
    ("Samsung server share of own DRAM bits", "2026Q2", "Goldman"),
    ("SK hynix Server share of own DRAM revenue", "2026Q3", "SK hynix"),
    ("SK hynix Mobile share of own DRAM revenue", "2026Q3", "SK hynix"),
    ("SK hynix PC share of own DRAM revenue", "2026Q3", "SK hynix"),
    ("SK hynix Graphics (incl. HBM) share of own DRAM revenue", "2026Q3", "SK hynix"),
    ("SK hynix Consumer share of own DRAM revenue", "2026Q3", "SK hynix"),
    ("Micron data-center DRAM share of own DRAM revenue", "FQ4-2026", "Micron"),
    ("Micron share of data center LPDRAM", "FY2025", "Micron"),
    ("Samsung SOCAMM2 share", "2026", "BNK"), ("SK hynix SOCAMM2 share", "2026", "BNK"),
    ("Samsung SOCAMM2 share", "2026-2027", "Korea Investment"), ("SK hynix SOCAMM2 share", "2026-2027", "Korea Investment"),
    ("Samsung HBM share vs its DRAM share", "2026Q3", "Samsung Electronics"),
    ("Industry DDR4 share of DDR market", "2024", "CXMT"),
]:
    vm(metric, period, pub)


# --------------------------------------------------------------------------
# Fit
# --------------------------------------------------------------------------
KAPPA = V_ASSUMPTIONS["prior_noise_concentration"]["value"]


def ras(seed, rows, cols, iters=400):
    """Vectorised RAS. seed (N,V,T) >= 0; rows (N,V); cols (N,T). Returns fitted and max rel. error."""
    m = seed.copy()
    for _ in range(iters):
        rs = m.sum(2)
        m *= np.where(rs > 0, rows / np.where(rs > 0, rs, 1), 0)[:, :, None]
        cs = m.sum(1)
        m *= np.where(cs > 0, cols / np.where(cs > 0, cs, 1), 0)[:, None, :]
    err_r = np.abs(m.sum(2) - rows) / np.maximum(rows, 1e-9)
    err_c = np.abs(m.sum(1) - cols) / np.maximum(cols, 1e-9)
    return m, float(max(err_r.max(), err_c.max()))


def fit_year(base, y, row_share, rng):
    cat = base["cat"][y]
    total = cat["total"]
    rows = np.stack([total * row_share[v] for v in VENDORS], 1)                     # (N,V)
    # HBM shares
    hs = np.zeros((N, len(VENDORS)))
    for j, v in enumerate(VENDORS[:4]):
        lo, md, hi = F.pooled(HBM_PTS[y][v])
        hs[:, j] = F.tri_ppf(rng.random(N), lo, md, hi)
    hs /= hs.sum(1, keepdims=True)
    hbm = hs * cat["hbm"][:, None]
    # Residual rows and non-HBM columns
    rrows = rows - hbm
    cols = np.stack([cat[t] for t in NONHBM], 1)                                   # (N,T5)
    # Noisy prior seed
    seed = np.zeros((N, len(VENDORS), len(NONHBM)))
    for i, v in enumerate(VENDORS):
        p = np.array([PRIOR[y][v][TYPES.index(t)] for t in NONHBM], float)
        for j, t in enumerate(NONHBM):
            if p[j] <= 0:
                continue
            k = KAPPA[CONF[v][t]]
            seed[:, i, j] = rng.gamma(k, p[j] / k, N)
        seed[:, i, :] /= seed[:, i, :].sum(1, keepdims=True)
        seed[:, i, :] *= rrows[:, i:i + 1]
    fit, err = ras(seed, rrows, cols)
    full = np.zeros((N, len(VENDORS), len(TYPES)))
    for j, t in enumerate(TYPES):
        full[:, :, j] = hbm if t == "hbm" else fit[:, :, NONHBM.index(t)]
    neg_rows = float(np.mean((rrows <= 0).any(1)))
    return dict(m=full, rows=rows, cols=np.stack([cat[t] for t in TYPES], 1), err=err, neg_rows=neg_rows,
                hbm_share=hs)


def run(base, row_fn, seed_offset=0):
    rng = np.random.default_rng(F.SEED + 7 + seed_offset)
    return {y: fit_year(base, y, row_fn(y), rng) for y in YEARS}


def table(res):
    out = []
    for y in YEARS:
        r = res[y]
        m, rows, cols = r["m"], r["rows"], r["cols"]
        for i, v in enumerate(VENDORS):
            for j, t in enumerate(TYPES):
                x = m[:, i, j]
                qq = F.q(x)
                prior = PRIOR[y][v][j] / 100
                sv = x / rows[:, i]
                out.append(dict(year=y, vendor=v, type=t, median_bn_gb=qq["median"], p10=qq["p10"], p90=qq["p90"],
                                p2_5=qq["p2_5"], p97_5=qq["p97_5"], median_eb=qq["median"] / F.BNGB_PER_EB,
                                share_of_type=np.median(x / cols[:, j]),
                                share_of_type_p10=np.percentile(x / cols[:, j], 10),
                                share_of_type_p90=np.percentile(x / cols[:, j], 90),
                                share_of_vendor=np.median(sv), prior_share=prior,
                                fitted_over_prior=np.median(sv / prior) if prior > 0 else np.nan,
                                confidence="pinned (broker HBM shares)" if t == "hbm" else CONF[v][t]))
            qq = F.q(rows[:, i])
            out.append(dict(year=y, vendor=v, type="total", median_bn_gb=qq["median"], p10=qq["p10"], p90=qq["p90"],
                            p2_5=qq["p2_5"], p97_5=qq["p97_5"], median_eb=qq["median"] / F.BNGB_PER_EB,
                            share_of_type=np.median(rows[:, i] / rows.sum(1)), share_of_vendor=1.0, prior_share=1.0,
                            fitted_over_prior=1.0, confidence="Mirae row share"))
        for j, t in enumerate(TYPES):
            qq = F.q(cols[:, j])
            implied = sum(PRIOR[y][v][j] / 100 * np.median(rows[:, i]) for i, v in enumerate(VENDORS))
            out.append(dict(year=y, vendor="All vendors", type=t, median_bn_gb=qq["median"], p10=qq["p10"], p90=qq["p90"],
                            p2_5=qq["p2_5"], p97_5=qq["p97_5"], median_eb=qq["median"] / F.BNGB_PER_EB,
                            share_of_type=1.0, share_of_vendor=np.median(cols[:, j] / rows.sum(1)),
                            prior_share=implied / np.median(rows.sum(1)),
                            fitted_over_prior=qq["median"] / implied if implied > 0 else np.nan,
                            confidence="model column"))
    df = pd.DataFrame(out)
    num = df.select_dtypes("number").columns.drop("year")
    df[num] = df[num].round(4)
    return df


# --------------------------------------------------------------------------
# Chart 05
# --------------------------------------------------------------------------
TYPE_LABEL = {"server_ecc": "Server ECC", "lpddr": "LPDDR", "client_pc": "Client PC", "hbm": "HBM", "gddr": "GDDR",
              "other_consumer": "Other / consumer"}


def chart(df, path):
    fig = F.new_fig(10.0, 9.4)
    F.title(fig, "DRAM bits by vendor and type, 2026 and 2027",
            "Top: bn Gb, median, stacked by type; whisker = 80% interval of the vendor total. "
            "Bottom: each vendor's share of each type (median).")
    ax = fig.add_axes([0.08, 0.50, 0.66, 0.37])
    F.style_ax(ax)
    xs, labels = [], []
    for i, v in enumerate(VENDORS):
        for k, y in enumerate((2026, 2027)):
            x = i * 2.6 + k * 1.0
            xs.append(x)
            labels.append(str(y))
            bottom = 0.0
            for t in F.CATS:
                val = float(df[(df.year == y) & (df.vendor == v) & (df.type == t)]["median_bn_gb"].iloc[0])
                ax.bar(x, val, width=0.8, bottom=bottom, color=F.CAT_COLOR[t], edgecolor=F.SURF, linewidth=1.0)
                bottom += val
            tot = df[(df.year == y) & (df.vendor == v) & (df.type == "total")].iloc[0]
            ax.vlines(x, tot["p10"], tot["p90"], color=F.INK, linewidth=1.5)
            ax.text(x, tot["p90"] + 3, f"{tot['median_bn_gb']:.0f}", ha="center", va="bottom", fontsize=8, color=F.INK)
        ax.text(i * 2.6 + 0.5, -24, v, ha="center", va="top", fontsize=9, color=F.INK, weight="bold")
    ax.set_xticks(xs, labels)
    ax.set_ylabel("bn Gb", color=F.INK2)
    ax.set_ylim(0, df[(df.type == "total") & (df.vendor.isin(VENDORS)) & (df.year >= 2026)]["p90"].max() * 1.12)
    for jj, t in enumerate(reversed(F.CATS)):
        yy = 0.84 - jj * 0.05
        fig.patches.append(plt.Rectangle((0.77, yy - 0.009), 0.016, 0.02, transform=fig.transFigure,
                                         color=F.CAT_COLOR[t], figure=fig))
        fig.text(0.795, yy + 0.001, TYPE_LABEL[t], color=F.INK, fontsize=9, va="center")
    # Heatmaps: vendor share of each type
    ramp = matplotlib.colors.LinearSegmentedColormap.from_list("blue", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
    for p, y in enumerate((2026, 2027)):
        hx = fig.add_axes([0.14 + p * 0.45, 0.07, 0.36, 0.30])
        mat = np.array([[float(df[(df.year == y) & (df.vendor == v) & (df.type == t)]["share_of_type"].iloc[0])
                         for t in F.CATS] for v in VENDORS])
        hx.imshow(mat, cmap=ramp, vmin=0, vmax=0.7, aspect="auto")
        for i in range(len(VENDORS)):
            for j in range(len(F.CATS)):
                val = mat[i, j]
                hx.text(j, i, f"{100 * val:.0f}%", ha="center", va="center", fontsize=8.5,
                        color="#ffffff" if val > 0.32 else F.INK)
        hx.set_xticks(range(len(F.CATS)), [TYPE_LABEL[t].replace(" / ", "/\n") for t in F.CATS], fontsize=8)
        hx.set_yticks(range(len(VENDORS)), VENDORS if p == 0 else [""] * len(VENDORS), fontsize=8.5)
        hx.tick_params(length=0, colors=F.INK2)
        for s in hx.spines.values():
            s.set_visible(False)
        hx.set_title(f"{y}: vendor share of each type", fontsize=9.5, color=F.INK, loc="left")
    fig.text(0.02, 0.012, "Rows: Mirae vendor production shares x model total. HBM: broker bit shares. Other cells: "
             "prior mix fitted by RAS. Table: out/vendor_by_type.csv.", color=F.MUTED, fontsize=7.5)
    fig.savefig(path, facecolor=F.SURF)
    plt.close(fig)


def main():
    F.CHARTS.mkdir(parents=True, exist_ok=True)
    base = F.simulate()
    res = run(base, lambda y: ROW_SHARE[y])
    df = table(res)
    cols = ["year", "vendor", "type", "median_bn_gb", "p10", "p90", "share_of_type", "share_of_vendor", "prior_share",
            "fitted_over_prior", "p2_5", "p97_5", "median_eb", "share_of_type_p10", "share_of_type_p90", "confidence"]
    df[cols].to_csv(F.OUT / "vendor_by_type.csv", index=False)

    alt = table(run(base, shipment_row_shares))
    sens = df[["year", "vendor", "type", "median_bn_gb", "share_of_type", "share_of_vendor"]].merge(
        alt[["year", "vendor", "type", "median_bn_gb", "share_of_type", "share_of_vendor"]],
        on=["year", "vendor", "type"], suffixes=("_production", "_shipment_split"))
    sens.to_csv(F.OUT / "vendor_by_type_sensitivity.csv", index=False)

    chart(df, F.CHARTS / "05_vendor_by_type.png")
    F.inputs_used().to_csv(F.OUT / "inputs_used_vendor.csv", index=False)
    pd.DataFrame([dict(name=k, value=str(v["value"]), reason=v["reason"]) for k, v in V_ASSUMPTIONS.items()]).to_csv(
        F.OUT / "assumptions_vendor.csv", index=False)

    pd.set_option("display.width", 220)
    for y in YEARS:
        print(f"{y}: RAS max rel. error {res[y]['err']:.2e}; draws with a negative residual row {100 * res[y]['neg_rows']:.2f}%")
        print("HBM points", {v: HBM_PTS[y][v] for v in VENDORS[:4]})
    print("row shares", {y: {k: round(v, 4) for k, v in ROW_SHARE[y].items()} for y in YEARS})
    print("shipment split", {y: {k: round(v, 4) for k, v in shipment_row_shares(y).items()} for y in YEARS})
    print(df[df.year >= 2026][["year", "vendor", "type", "median_bn_gb", "p10", "p90", "share_of_type", "share_of_vendor",
                               "prior_share", "fitted_over_prior"]].to_string(index=False))
    s = sens[(sens.type.isin(["hbm", "server_ecc", "lpddr", "total"])) & (sens.vendor.isin(["Samsung", "SK hynix"]))]
    print(s.round(3).to_string(index=False))
    print(f"inputs cited: {len(F.USED)}")


if __name__ == "__main__":
    main()
