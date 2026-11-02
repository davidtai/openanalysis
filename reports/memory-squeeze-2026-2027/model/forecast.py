#!/usr/bin/env python3
"""DRAM bit supply by category, 2023-2027, with a 2026 quarterly table.

Run from the project folder:  .venv/bin/python -I model/forecast.py

Every number comes from a row in sources/*.csv. The `src()` lookup finds the
row by (file, segment, metric, period, publisher[, pub_date]) and records it.
At the end the script writes out/inputs_used.csv: one line per cited row with
publisher, period, value and url. Values that no row supports sit in the
ASSUMPTIONS dict, each with a reason. Unit convention: 1 GB = 8 Gb and
1 EB = 1e9 GB = 8 bn Gb (decimal, as Mirae Asset and Yole use them).
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "sources"
OUT = ROOT / "out"
CHARTS = OUT / "charts"
N_DRAWS = 50_000
SEED = 20261030
GB_TO_GB = 8.0          # gigabits per gigabyte
BNGB_PER_EB = 8.0       # 1 EB = 1e9 GB = 8e9 Gb = 8 bn Gb

# --------------------------------------------------------------------------
# Assumptions: values that no source row gives directly. Each has a reason.
# METHOD.md lists all of them.
# --------------------------------------------------------------------------
ASSUMPTIONS = {
    "label_ranges": dict(
        value={"low single digit": (1, 3), "low to mid single digit": (2, 5),
               "high single digit": (7, 9), "low teens": (11, 13),
               "mid to high teens": (15, 19), "high teens": (17, 19),
               "low 20s": (20, 23), "low-to-mid 20s": (20, 26), "mid-20s": (24, 26)},
        reason="Vendors give words, not numbers. The total-dram notes read 'mid-20s' as about "
               "24-26% and 'low 20s' as about 20-23% (Micron call notes); the other words use "
               "the same three-point split of a decade."),
    "approx_halfwidth_pp": dict(value=1.0, reason="A '~X%' value is read as X +/- 1 pp."),
    "base_2025_log_sd": dict(
        value=0.03,
        reason="Mirae's 2025 production (293.1 bn Gb) is an estimate made in Dec 2025. KGI (37.6 EB) "
               "and Yole (38 EB) put 2025 demand within 1-1.5% of Mirae's demand; 3% also covers the "
               "gap between production and demand definitions."),
    "mirae_server_lp_split": dict(
        value="uniform(0,1)",
        reason="No source says whether Mirae counts Grace/Vera LPDDR in 'server' or in 'mobile'. "
               "TrendForce counts it in mobile; Yole in data center. We draw the fraction f that "
               "sits in Mirae's server line from U(0,1) and remove it from that line only, so the "
               "bits are never counted twice."),
    "server_lp_2023": dict(value=0.0, reason="No 2023 figure; LS Securities gives 1.1 bn Gb for 2024, "
                                             "so 2023 was small. Set to 0."),
    "mobile_includes_tablets": dict(
        value=True,
        reason="Mirae's 'mobile' line implies about 1.4 bn devices at 11.2 GB, more than phones "
               "alone, so it holds tablets too. Tablets get the phone unit and content growth; "
               "no tablet content figure exists."),
    "content_freeze_floor_pct": dict(
        value=0.0,
        reason="Phone, PC and 2027 mobile content growth: the low end is a full freeze (0%). "
               "TrendForce, IDC and Micron report spec cuts and frozen configurations in 2026, "
               "but no source gives a number for the floor."),
    "mobile_content_2027_pct": dict(
        value=(0.0, 2.5, 5.0),
        reason="No source gives 2027 GB per phone. The LPDDR notes recommend flat to +5% from the "
               "2026 value; we use a triangle 0 / 2.5 / 5%."),
    "other_2026_log_sd": dict(
        value=0.10,
        reason="Mirae 'other' (20.3 bn Gb) has no second source on the same basis. 10% covers a "
               "consumer-unit swing of the size seen elsewhere in 2026 (AIB cards -10%, JPR)."),
    "auto_from_mirae_other": dict(
        value=True,
        reason="Auto DRAM (2-3% of bits) is taken out of Mirae's 'other' line. The brief puts auto "
               "in LPDDR; no source gives the LPDDR share of auto DRAM."),
    "gddr_2027_growth_pct": dict(
        value=(-10.0, 0.0, 10.0),
        reason="No GDDR bit forecast exists. Gaming card units fall (JPR -10% in 2026, -5.9% CAGR) "
               "while GB per AI card rises (RTX PRO 6000 96 GB). We take a flat centre, +/-10%."),
    "other_2027_growth_pct": dict(
        value=(-10.0, 0.0, 4.9),
        reason="Max is Mirae's +4.9% for 'other'. Min -10% matches the consumer-unit fall seen in "
               "2026 (JPR AIB). Mode flat. No direct source."),
    "hbm_share_annual_average": dict(
        value="h(year) = (h(end of prior year) + h(end of year)) / 2",
        reason="TrendForce gives HBM wafer shares at year ends (18/22/30%); the bit model needs annual "
               "averages. 2026 uses AMAT (Mar 2026, 15%) as the low end and Samsung (Oct 2026, ~20%) as "
               "the mode."),
    "new_fab_half_year": dict(
        value=0.5,
        reason="TrendForce (Jul 2026): new fabs ramp from 2H27; Micron: ID1 and Tongluo output from "
               "mid-2027. A fab that starts mid-year adds about half its year-end capacity to the "
               "annual average, so the mode of each new-fab addition is half of Mirae's 2027 step."),
    "cxmt_hbm_linear_ramp": dict(
        value=True,
        reason="CXMT HBM wafers are given at year ends (SemiAnalysis: 5, 30, 55 kwpm). The annual "
               "average is the midpoint of the start and end values."),
    "priority_allocation_2027": dict(
        value="HBM -> server LPDDR -> server ECC -> ALR for the rest",
        reason="LTAs, prepayments and supplier statements put HBM and server first. Server ECC grows at "
               "its own supply guide (TrendForce RDIMM +15-20%, Mirae +22.7% as max) and is not "
               "renormalised; phone, PC, GDDR, other and auto share what is left. Auto keeps its share "
               "of total bits."),
    "trade_ratio_rise_2027": dict(
        value="r27 = r26 x (1 + rho), rho ~ tri(0, 1/6, 1/3)",
        reason="Micron (Sep 2026) says the trade ratio rises with HBM4/HBM4E, so rho >= 0. Goldman "
               "(Jun 2026) gives 3-4x against Micron's 3x: the top of that range is +33%, the "
               "midpoint +17%. r(2025) = r(2026): no source gives a 2025-2026 change."),
    "hbm_node_gain_equals_standard": dict(
        value=True,
        reason="HBM core dies use the same DRAM nodes (1b, 1c), so HBM bits per wafer grow at the "
               "same node-migration rate n as standard DRAM. No source splits the two."),
    "node_gain_ceiling": dict(
        value="TrendForce 1-alpha full-node gain (~30%)",
        reason="The upper end of the 2027 node gain is one full node step for the whole fleet in "
               "one year, which no year has reached."),
    "rubin_ultra_units_2027_m": dict(
        value=(0.5, 1.0, 1.5),
        reason="UNSUPPORTED. No source gives 2027 Rubin Ultra package units. Rubin's own launch "
               "year (2026) was 1.5-2.4 M chips (KeyBanc, Morgan Stanley; hbm-gddr notes). Rubin "
               "Ultra ships from 2H27, so we take about half that, widened to 0.5-1.5 M. Used only "
               "to move HBM demand, not supply."),
    "server_ddr5_share": dict(
        value="2026: tri(0.90, 0.95, 1.0); 2027: tri(s26, (s26+1)/2, 1)",
        reason="TrendForce puts DDR5 at ~90% of server bits in 1Q25. DDR4 server parts reached end "
               "of life at Samsung (Dec 2025), SK hynix (Apr 2026) and Micron (1Q26), so the share "
               "only rises. No 2026 number exists."),
    "pc_ddr5_share": dict(
        value="2026: tri(0.60, 0.80, 0.95); 2027: tri(s26, (s26+1)/2, 1)",
        reason="UNSUPPORTED beyond 'DDR5 passed 50% of PC DRAM in 2H24' (TrendForce). No later "
               "figure exists in text form (Apacer's chart is an image)."),
    "combination_weights": dict(
        value=(1 / 3, 1 / 3, 1 / 3),
        reason="Equal weights for time series, supply model and guidance. The supply model has no "
               "track record, so we cannot estimate its error variance; with few data points equal "
               "weights usually beat estimated ones (the 'forecast combination puzzle'). We report "
               "the inverse-variance result as a check."),
    "ts_min_train_years": dict(value=10, reason="Rolling-origin backtest starts after 10 years of data."),
    "quarterly_vendor_path": dict(
        value=True,
        reason="Only Samsung and SK hynix give 2026 quarterly QoQ bit guidance. The industry path "
               "uses their bit-weighted QoQ; 1Q26 is solved so the four quarters sum to the annual "
               "total."),
}

LABELS = ASSUMPTIONS["label_ranges"]["value"]
HALF = ASSUMPTIONS["approx_halfwidth_pp"]["value"]

# --------------------------------------------------------------------------
# Source access
# --------------------------------------------------------------------------
FILES = ["total-dram", "server-ddr5", "hbm-gddr", "lpddr", "supply-chain"]
T = {}
for _f in FILES:
    _p = SRC_DIR / f"{_f}.csv"
    if _p.exists():
        T[_f] = pd.read_csv(_p, dtype=str, keep_default_na=False)
USED: dict = {}


def src(file, segment, metric, period, publisher=None, pub_date=None, unit=None):
    """Return the one source row that matches; record it as used."""
    d = T[file]
    m = (d["segment"] == segment) & (d["metric"] == metric) & (d["period"] == period)
    if unit is not None:
        m &= d["unit"] == unit
    if publisher is not None:
        m &= d["publisher"] == publisher
    if pub_date is not None:
        m &= d["pub_date"] == pub_date
    hit = d[m]
    if hit.empty:
        raise KeyError(f"no row: {file} | {segment} | {metric} | {period} | {publisher} | {pub_date}")
    if hit["value"].nunique() > 1:
        raise ValueError(f"ambiguous rows: {file} {segment} {metric} {period}: {hit['value'].tolist()}")
    i = int(hit.index[0])
    USED[(file, i)] = hit.loc[i]
    return hit.loc[i]


def parse_num(v: str) -> float:
    s = str(v).replace(",", "").replace("%", "").strip()
    s = re.sub(r"^[~><+≈]\s*", "", s)
    return float(s)


def label_range(v: str) -> tuple[float, float]:
    s = str(v).strip().lower().replace("%", "")
    if s in LABELS:
        return tuple(float(x) for x in LABELS[s])
    m = re.match(r"^~?\s*([-+]?\d+(?:\.\d+)?)\s*(?:-|to)\s*([-+]?\d+(?:\.\d+)?)$", s)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return (min(a, b), max(a, b))
    if s.startswith("~"):
        x = parse_num(s)
        return (x - HALF, x + HALF)
    x = parse_num(s)
    return (x, x)


def num(*a, **k) -> float:
    return parse_num(src(*a, **k)["value"])


def rng_of(*a, **k) -> tuple[float, float]:
    return label_range(src(*a, **k)["value"])


# --------------------------------------------------------------------------
# Sampling helpers
# --------------------------------------------------------------------------
def tri_ppf(u, lo, mode, hi):
    """Inverse CDF of a triangular distribution; lo/mode/hi may be arrays."""
    lo, mode, hi = (np.broadcast_to(np.asarray(x, float), np.shape(u)) for x in (lo, mode, hi))
    width = hi - lo
    safe = np.where(width > 0, width, 1.0)
    fc = np.where(width > 0, (mode - lo) / safe, 0.5)
    left = lo + np.sqrt(np.clip(u * safe * (mode - lo), 0, None))
    right = hi - np.sqrt(np.clip((1 - u) * safe * (hi - mode), 0, None))
    return np.where(width > 0, np.where(u < fc, left, right), lo)


def pooled(points):
    """Triangle from source points: (min, median, max)."""
    p = np.asarray(points, float)
    return float(p.min()), float(np.median(p)), float(p.max())


def pooled_arr(arrs):
    """Per-draw (min, median, max) when some points are arrays."""
    st = np.vstack([np.broadcast_to(np.asarray(a, float), (N_DRAWS,)) for a in arrs])
    return st.min(0), np.median(st, 0), st.max(0)


def q(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return dict(median=np.nan, p10=np.nan, p90=np.nan, p2_5=np.nan, p97_5=np.nan)
    p = np.percentile(x, [50, 10, 90, 2.5, 97.5])
    return dict(median=p[0], p10=p[1], p90=p[2], p2_5=p[3], p97_5=p[4])


# ==========================================================================
# 1. Fixed inputs read from the sources
# ==========================================================================
MIRAE = "Mirae Asset Securities"
TD, SD, HG, LP, SC = "total-dram", "server-ddr5", "hbm-gddr", "lpddr", "supply-chain"
YEARS = [2023, 2024, 2025, 2026, 2027]

# Mirae Asset, Dec 2025, p.16: production, demand and application demand (bn Gb).
PROD = {y: num(TD, "total", "bit production", str(y), MIRAE) for y in YEARS}
DEM = {y: num(TD, "total", "bit demand", str(y), MIRAE) for y in YEARS}
MIR = {y: dict(
    mobile=num(TD, "mobile", "bit demand (mobile DRAM)", str(y), MIRAE),
    pc=num(TD, "pc", "bit demand (PC DRAM)", str(y), MIRAE),
    server=num(TD, "server", "bit demand (server DRAM)", str(y), MIRAE),
    graphics=num(TD, "graphics", "bit demand (graphics DRAM = HBM + GDDR)", str(y), MIRAE),
    other=num(TD, "other", "bit demand (other DRAM)", str(y), MIRAE)) for y in YEARS}

# Mirae server units and content (server-ddr5.csv), used to split growth into units x content.
SRV_UNITS = {y: num(SD, "server", "shipments", str(y), MIRAE) for y in YEARS}
SRV_GB = {y: num(SD, "server", "avg_dram_content", str(y), MIRAE) for y in YEARS}
SRV_DEM_G = {y: num(SD, "server", "dram_bit_demand_growth_yoy", str(y), MIRAE) for y in (2026, 2027)}
SRV_GB_G = {y: num(SD, "server", "avg_dram_content_growth_yoy", str(y), MIRAE) for y in (2025, 2026, 2027)}
# Mirae's implied server unit growth = (1 + bit growth) / (1 + content growth) - 1
MIRAE_SRV_UNIT_G = {y: (1 + SRV_DEM_G[y] / 100) / (1 + SRV_GB_G[y] / 100) - 1 for y in (2026, 2027)}
PC_UNITS_25 = num(SD, "pc", "shipments", "2025", MIRAE)
PC_GB = {y: num(SD, "pc", "avg_dram_content", str(y), MIRAE) for y in (2025, 2026, 2027)}

# Wafer capacity, Mirae Dec 2025 (kwpm, annual average) and later revisions.
W_IND = {y: num(TD, "total", "wafer capacity (industry)", str(y), MIRAE) for y in YEARS}
W_V = {v: {y: num(TD, "total", f"{v} wafer capacity", str(y), MIRAE) for y in (2026, 2027)}
       for v in ["Samsung", "SK hynix", "Micron", "CXMT", "Nanya"]}
W_OTHERS = W_IND[2026] - sum(W_V[v][2026] for v in W_V)       # vendors outside the five (derived)
SAMSUNG_END26 = num(TD, "total", "Samsung wafer capacity (end of year)", "2026 end", MIRAE)
SKH_END26 = num(TD, "total", "SK hynix wafer capacity (end of year)", "2026 end", MIRAE)
M15X_ADD_26 = num(TD, "total", "SK hynix M15X capacity addition", "2026", MIRAE)
M15X_FULL = num(HG, "hbm-skhynix", "m15x_wafer_capacity", "2027-06", "Korea JoongAng Daily")
CXMT_NOW = num(TD, "total", "CXMT wafer capacity", "2026 (current)", "TrendForce News (citing Commercial Times)")
CXMT_27 = num(TD, "total", "CXMT wafer capacity", "2027", "TrendForce News (citing Commercial Times)")
TONGLUO_SHARE = num(SC, "capex", "Tongluo Phase 1 capacity vs Micron global capacity", "2H27", "TrendForce") / 100
# Timing statements (cited; used for the half-year rule and the bounds).
src(SC, "capex", "new DRAM capacity contribution timing", "2027-2028", "TrendForce")
src(SC, "capex", "Micron new DRAM fab output timing", "2027-2030", "Micron")
src(SC, "capex", "SK hynix Yongin Phase 1 cleanroom opening", "early 2027", "SK hynix")
src(TD, "total", "Samsung Pyeongtaek status", "2026-10", "EconoTimes")
src(TD, "total", "SK hynix M15X fab status", "2026 end", "SK hynix")
CXMT_HBM = {e: num(HG, "hbm-cxmt", "hbm_wafer_capacity", f"{e}-12", "SemiAnalysis") for e in (2025, 2026, 2027)}
NODE_FULL_STEP = num(TD, "total", "bits per wafer gain from node migration", "1-alpha", "TrendForce") / 100

# HBM wafer and bit shares.
TF = "TrendForce"
H_END = {e: num(TD, "hbm", "HBM share of DRAM wafer input (top 3)", f"{e} end", TF) / 100 for e in (2025, 2026, 2027)}
S_TF = {y: num(TD, "hbm", "HBM share of DRAM bit supply (top 3)", str(y), TF) / 100 for y in (2025, 2026, 2027)}
H_AMAT_MAR26 = num(HG, "hbm", "share_of_dram_wafers", "2026-03", "Applied Materials (CFO Bryce Hill, via The Elec)") / 100
H_SAMSUNG_OCT26 = num(HG, "hbm", "share_of_global_dram_wafers", "2026-10", "Samsung (Kim Tae-woo, via Seoul Economic Daily)") / 100
H_SAMSUNG_27 = num(HG, "hbm", "share_of_global_dram_wafers", "2027", "Samsung (Kim Tae-woo, via Seoul Economic Daily)") / 100
H_TSV_DEC24 = num(HG, "hbm", "tsv_share_of_dram_capacity", "2024-12", TF) / 100
HBM_WAFERS_24 = num(HG, "hbm", "wafer_production", "2024", "Yole Group (via Edge AI and Vision Alliance)")
# Trade ratio points.
R_MICRON = num(HG, "hbm", "wafer_trade_ratio_vs_ddr5", "2025", "Micron (FQ1 2026 call)")
R_AMAT = num(HG, "hbm", "wafer_area_ratio_vs_conventional", "2026", "Applied Materials (via The Elec)")
R_GS = rng_of(HG, "hbm", "wafer_ratio_vs_standard_dram", "2026", "Goldman Sachs (via Tiger Brokers)")
src(HG, "hbm", "wafer_trade_ratio_vs_ddr5", "2027", "Micron (FQ4 2026 call)")       # ">3, rising"


def tf_implied_ratio(h, s):
    """Trade ratio vs the average standard wafer implied by a wafer share h and bit share s."""
    return h * (1 - s) / (s * (1 - h))


R_TF25 = tf_implied_ratio(H_END[2025], S_TF[2025])
R_TF27 = tf_implied_ratio(H_END[2027], S_TF[2027])

# HBM bits (bn Gb).
HBM23 = num(HG, "hbm", "demand_bits", "2023", TF, unit="billion Gb")
HBM24_GREENBERG = num(HG, "hbm", "shipments_bits", "2024", "Marc Greenberg (FMS 2024; data likely Yole)") * GB_TO_GB / 1000
MIR_HBM = {y: (num(HG, "hbm-samsung", "shipments_bits", str(y), MIRAE),
               num(HG, "hbm-skhynix", "shipments_bits", str(y), MIRAE)) for y in (2024, 2025, 2026, 2027)}
UBS_HBM = {y: num(HG, "hbm", "end_demand_bits", str(y), "UBS (via Investing.com)") for y in (2025, 2026, 2027)}
TF_HBM_26_FLOOR = num(HG, "hbm", "shipments_bits", "2026", TF)
TF_HBM_27_GROWTH = rng_of(HG, "hbm", "bit_shipment_growth", "2027", TF)
GS_HBM_GAP_27 = num(HG, "hbm", "supply_demand_gap", "2027", "Goldman Sachs (via Tiger Brokers/Deep News)") / 100
# Micron HBM bit share: Counterpoint revenue shares (2025Q2-2026Q2) and UBS 2027 bit share.
_mu_shares = []
for _p in ["2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"]:
    _mu_shares.append(float(src(HG, "hbm", "revenue_share_SKH/Samsung/Micron", _p, "Counterpoint Research")["value"].split("/")[2]))
_ubs_mu = src(HG, "hbm", "bit_share_by_vendor", "2027", "UBS (via Investing.com)")["value"]
_mu_shares.append(float(re.search(r"Micron ~(\d+)", _ubs_mu).group(1)))
MU_SHARE = tuple(x / 100 for x in pooled(_mu_shares))

# Rubin Ultra HBM per package (GB).
RU_NV = num(HG, "accelerator", "hbm_per_package_RubinUltra", "2027", "NVIDIA (GTC 2025 keynote)")
RU_UBS = num(HG, "accelerator", "hbm_per_package_RubinUltra_ubs", "2027", "UBS (via Investing.com)")
RU_TF = num(HG, "accelerator", "hbm_per_gpu_RubinUltra_tf", "2027", TF) * 2   # per GPU = 2 dies; 4-die package
src(HG, "accelerator", "rubin_ultra_hbm_config_review", "2027", TF)            # 8-Hi options under review
RU_8HI = RU_UBS * 8 / 12                                                      # derived: 12-Hi -> 8-Hi
# Accelerator bottom-up checks.
TPU = {y: num(HG, "accelerator", "tpu_shipments", str(y), "UBS (via The Buildout)") for y in (2026, 2027)}
TRN3 = {y: num(HG, "accelerator", "trainium3_shipments", str(y), "UBS (via Money Weekly/Cnyes)") for y in (2026, 2027)}
TPU8_GB = [float(x) for x in src(HG, "accelerator", "hbm_per_chip_TPU_8t_8i", "2026", MIRAE)["value"].split("/")]
TRN3_GB = num(HG, "accelerator", "hbm_per_chip_Trainium3", "2025", "AWS")
NV_BU_26 = rng_of(HG, "accelerator", "hbm_bottom_up_nvidia", "2026", "Morgan Stanley / NVIDIA / TrendForce")
ASIC_BU_26 = num(HG, "accelerator", "hbm_bottom_up_tpu_trainium", "2026", "UBS / Google / AWS")
GDDR_AIB_26 = num(HG, "gddr", "aib_market_forecast", "2026", "Jon Peddie Research")
_mir_gddr = {y: MIR[y]["graphics"] - sum(MIR_HBM[y]) / (1 - MU_SHARE[1]) for y in (2025, 2026)}
GDDR26_G_PTS = [GDDR_AIB_26,
                *[-x for x in rng_of(HG, "gddr", "rtx50_supply_cut_to_partners", "2026-01",
                                     "TechTimes (citing leaker MEGAsizeGPU via Tom's Hardware)")],
                100 * (_mir_gddr[2026] / _mir_gddr[2025] - 1)]                  # Mirae graphics minus Mirae HBM
src(HG, "gddr", "rubin_cpx_status", "2026-03", "Tom's Hardware")                  # CPX GDDR7 removed

# Server LPDDR (SOCAMM / Grace / Vera), bn Gb.
LPS_24 = num(LP, "lpddr-server", "ai_server_lpddr5x_demand", "2024", "LS Securities")
LPS_25 = num(LP, "lpddr-server", "ai_server_lpddr5x_demand", "2025", "LS Securities")
LPS_26_PTS = [num(LP, "lpddr-server", "nvidia_socamm2_demand", "2026", "Meritz Securities"),
              num(LP, "lpddr-server", "nvidia_socamm2_demand", "2026", "derived"),          # KB 10 / 50%
              *rng_of(LP, "lpddr-server", "nvidia_dram_demand", "2026", "Edgewater Research (quoted by YK Research)"),
              sum(num(LP, "lpddr-server", f"socamm_orders_{v}", "2026", "TrendForce News (citing Korean press)")
                  for v in ("samsung", "skhynix", "micron")) / 10]                          # 10x unit error, notes
LPS_27_PTS = [num(LP, "lpddr-server", "nvidia_socamm2_demand", "2027", "Meritz Securities") * GB_TO_GB / 1000,  # PB->bn Gb
              *rng_of(LP, "lpddr-server", "nvidia_dram_demand", "2027", "Edgewater Research (quoted by YK Research)")]
LPS_FILL_27 = num(LP, "lpddr-server", "nvidia_lpdram_need_met", "2027", TF) / 100
src(LP, "lpddr-server", "vera_socamm_capacity_cut", "2026-06", TF)
src(LP, "lpddr-supply", "server_lpddr5x_demand_growth", "2027", "CFM (MemoryMarket)")

# Phones (lpddr.csv).
PH25 = num(LP, "smartphone", "shipments", "2025", "IDC")
PH26_G_PTS = [num(LP, "smartphone", "shipments_yoy_forecast", "2026", "IDC"),
              num(LP, "smartphone", "shipments_forecast", "2026", "IDC") / PH25 * 100 - 100,
              num(LP, "smartphone", "shipments_forecast", "2026", "Counterpoint") / PH25 * 100 - 100,
              num(LP, "smartphone", "production_forecast", "2026", TF) / PH25 * 100 - 100,
              num(LP, "smartphone", "soc_shipments_yoy", "2026", "Counterpoint")]
_cp_soc = src(SC, "oem", "smartphone SoC shipments", "3Q26 / 2026 / 2027", "Counterpoint Research")["value"]
PH27_G_PTS = [num(LP, "smartphone", "shipments_yoy_forecast", "2027", "IDC", "2026-05-26"),
              *label_range(_cp_soc.split("/")[2])]                                      # Counterpoint "-3 to -4"
src(LP, "smartphone", "soc_shipments_yoy", "2027", "Counterpoint")
PH_GB = {2025: num(LP, "smartphone", "avg_dram_per_phone", "2025", "TrendForce (derived)"),
         2026: num(LP, "smartphone", "avg_dram_per_phone", "2026", TF)}
PH_GB_DEC = {2024: num(LP, "smartphone", "avg_dram_per_phone", "2024-12", "Counterpoint"),
             2025: num(LP, "smartphone", "avg_dram_per_phone", "2025-12", "Counterpoint")}
TABLETS_25 = num(LP, "lpddr-tablet", "tablet_shipments", "2025", "IDC")
YOLE_MOBILE = {y: num(LP, "mobile", "dram_bit_demand", str(y), "Yole Group (via Comet Holding CMD 2025)") for y in (2026, 2027)}
_lp_pc = src(LP, "lpddr-pc", "lpddr_share_of_pc_dram_demand", "2024", TF)
LP_PC_SHARE = tuple(float(x) / 100 for x in re.search(r"\((\d+)-(\d+)%\)", _lp_pc["unit"]).groups())
MAC_FLOOR_EB = num(LP, "lpddr-pc", "mac_lpddr_bits_floor", "2025", "derived")
AUTO_PTS = [num(LP, "auto", "share_of_dram_consumption", "2024", TF),
            num(LP, "auto", "share_of_dram_demand", "2025", "Omdia (via CXMT IPO prospectus, reported by XenoSpectrum)")]

# PC (server-ddr5.csv).
PC26_G_PTS = [num(SD, "pc", "shipments_growth_yoy", "2026", "IDC"),
              num(SD, "pc", "notebook_shipments_growth_yoy", "2026", TF)]
_q3 = src(SD, "pc", "shipments", "3Q26", "VenSearch (citing IDC preliminary)")
PC26_G_PTS.append(-float(re.search(r"fell ([\d.]+)%", _q3["quote"]).group(1)))      # 3Q26 actual -20.1%
_nb27 = src(SD, "pc", "notebook_shipments_growth_yoy", "2027", TF)                    # low-single-digit decline
PC27_G_PTS = [-LABELS["low single digit"][0], -LABELS["low single digit"][1],          # -1, -3
              -LABELS["high single digit"][1]]                                         # -9 if costs passed on (row note)
src(LP, "smartphone", "shipments_yoy_forecast", "2027", "IDC", "2026-02-26")          # superseded, cited for context

# Server units growth.
SRV26_G_PTS = [num(SD, "server", "shipments_growth_yoy", "2026", TF, "2026-07-30"),
               num(SD, "server", "shipments_growth_yoy", "2026", TF, "2026-04-15"),
               *rng_of(SD, "server", "industry_units_growth", "2026", "Micron (earnings call)")]
SRV27_G_PTS = [num(SD, "server", "shipments_growth_yoy", "2027", TF),
               *rng_of(SD, "server", "industry_units_growth", "2027", "Micron (earnings call)")]
SRV_GB26_G_PTS = [num(SD, "server", "avg_dram_content_growth_yoy", "2025",
                      "SemiconSam (Jukan), summary of TrendForce Korea roadshow"),
                  SRV_GB_G[2025], SRV_GB_G[2026]]
RDIMM27 = rng_of(SD, "server-ddr5", "rdimm_bit_supply_growth", "2027", TF)
# Server ECC 2027 supply growth: TrendForce RDIMM bit supply 15-20% (min, and midpoint as mode);
# Mirae server demand growth +22.7% as the max (supply cannot outgrow the demand view by much).
SRV27_SUPPLY_G = (RDIMM27[0], float(np.mean(RDIMM27)), SRV_DEM_G[2027])
# Order fill rates (Samsung Securities): evidence of a real server shortage that Mirae demand misses.
FILL_4Q25 = src(SD, "server", "order_fulfillment_rate", "4Q25", "Samsung Securities")["value"]
FILL_1Q26 = num(SD, "server", "order_fulfillment_rate", "1Q26", "Samsung Securities")
SRV_HBM27_G = num(SD, "server", "server_dram_plus_hbm_bit_supply_growth", "2027", TF)
HBM_RDIMM_SHARE26 = num(SD, "server", "hbm_plus_rdimm_share_of_dram_bit_supply", "2026", TF) / 100
KGI_SRV26 = num(SD, "server", "dram_bit_demand", "2026", "KGI Securities") * GB_TO_GB
SRV_DDR5_1Q25 = num(SD, "server-ddr5", "ddr5_share_of_server_dram_bits", "1Q25", TF) / 100
MU_DDR4_26 = num(SD, "ddr4-total", "ddr4_share_of_micron_dram_output", "2026", TF) / 100

# Guidance and checks.
SUFF26 = rng_of(SC, "outlook", "DRAM sufficiency ratio", "2026", TF)
YOLE_TOT = {y: num(TD, "total", "bit demand", str(y), "Yole Group (via Comet Holding CMD 2025)") for y in (2026, 2027)}

# ==========================================================================
# 2. Long history of bit-supply growth (for the time-series model)
# ==========================================================================


def build_history():
    rows = []
    for y in range(2006, 2010):
        rows.append((y, num(TD, "total", "bit supply growth YoY", str(y),
                            "Micron Technology (avg of Gartner, IDC, iSuppli)"), "Micron 2011 (avg Gartner/IDC/iSuppli)"))
    for y in (2010, 2011):
        rows.append((y, num(TD, "total", "bit supply growth YoY", str(y), "KDB Daewoo Securities Research"), "KDB Daewoo 2012"))
    for y in range(2012, 2020):
        rows.append((y, num(TD, "total", "bit growth YoY", str(y), "Mirae Asset Daewoo Research (citing DRAMeXchange)"),
                     "DRAMeXchange via Mirae 2020"))
    # 2020-2022: no actual supply growth. Benchmark the three years to the two supply levels
    # (Mirae 2019 supply; 2022 = Mirae 2023 production / (1 + 2023 growth)) and give them the
    # year-to-year shape of Mirae's actual demand growth.
    l19 = num(TD, "total", "bit supply", "2019", "Mirae Asset Daewoo Research") / 1000
    l22 = PROD[2023] / (1 + num(TD, "total", "bit production growth YoY", "2023", MIRAE) / 100)
    shape = np.log1p(np.array([num(TD, "total", "bit demand growth YoY", str(y), MIRAE) for y in (2020, 2021, 2022)]) / 100)
    c = (np.log(l22 / l19) - shape.sum()) / 3
    for y, s in zip((2020, 2021, 2022), shape):
        rows.append((y, 100 * np.expm1(s + c), "derived: benchmarked to Mirae supply levels"))
    for y in (2023, 2024, 2025):
        rows.append((y, num(TD, "total", "bit production growth YoY", str(y), MIRAE), "Mirae Dec 2025"))
    h = pd.DataFrame(rows, columns=["year", "growth_pct", "source"]).sort_values("year").reset_index(drop=True)
    h["y"] = np.log1p(h["growth_pct"] / 100)
    return h


HIST = build_history()

# Guidance track record: forecasts published in year T-1 for year T, against HIST.
GUIDE_TRACK = [
    (2025, (TD, "total", "bit output growth YoY", "2025", TF)),
    (2023, (TD, "total", "bit supply growth YoY", "2023", TF)),
    (2022, (TD, "total", "bit supply growth YoY", "2022", TF, "2021-10-12")),
    (2022, (TD, "total", "bit supply growth YoY", "2022", TF, "2021-11-04")),
    (2011, (TD, "total", "bit supply growth YoY", "2011", "TrendForce (DRAMeXchange)")),
    (2012, (TD, "total", "bit supply growth YoY", "2012", "Micron Technology (avg of Gartner, IDC, iSuppli)")),
    (2013, (TD, "total", "bit supply growth YoY", "2013", "KDB Daewoo Securities Research")),
    (2021, (TD, "total", "bit supply growth YoY", "2021", "Mirae Asset Daewoo Research (citing DRAMeXchange)")),
    (2021, (TD, "total", "bit supply growth YoY", "2021", "Mirae Asset Daewoo Research")),
]


def guidance_track():
    out = []
    for yr, key in GUIDE_TRACK:
        r = src(*key)
        f = parse_num(r["value"])
        a = float(HIST.loc[HIST.year == yr, "growth_pct"].iloc[0])
        out.append(dict(target_year=yr, publisher=r["publisher"], pub_date=r["pub_date"], forecast_pct=f,
                        actual_pct=a, error_pp=f - a, log_error=np.log1p(f / 100) - np.log1p(a / 100)))
    return pd.DataFrame(out)


GTRACK = guidance_track()
SIGMA_GUIDE = float(np.sqrt(np.mean(GTRACK["log_error"] ** 2)))

# 2026 and 2027 guidance.
G26_SOURCES = [
    ("Micron", "2026-09-30", rng_of(TD, "total", "bit shipment growth YoY", "2026", "Micron", "2026-09-30")),
    ("Micron", "2026-06-24", rng_of(TD, "total", "bit shipment growth YoY", "2026", "Micron", "2026-06-24")),
    ("SK hynix", "2026-07-29", rng_of(TD, "total", "bit demand growth YoY (SK hynix view)", "2026", "SK hynix")),
    ("Counterpoint", "2026-03-12", rng_of(TD, "total", "bit supply growth YoY", "2026", "Counterpoint Research (via ChosunBiz)")),
    ("Micron", "2026-03-18", rng_of(TD, "total", "bit shipment growth YoY", "2026", "Micron", "2026-03-18")),
]
# Older 2026 views, cited for context only (superseded).
src(TD, "total", "bit production growth YoY", "2026", MIRAE)
src(TD, "total", "bit shipment growth YoY", "2026", "Micron", "2025-12-17")
src(TD, "total", "bit supply growth YoY", "2026", "Omdia")
G26_TRI = (min(lo for _, d, (lo, hi) in G26_SOURCES if d >= "2026-06-01"),
           float(np.mean(G26_SOURCES[0][2])),
           max(hi for _, d, (lo, hi) in G26_SOURCES))

G27_SOURCES = [
    ("TrendForce", "2026-07-28", rng_of(TD, "total", "bit supply growth YoY", "2027", TF)),
    ("Micron", "2026-09-30", rng_of(TD, "total", "bit shipment growth YoY", "2027", "Micron")),
    ("SK hynix", "2026-10-27", rng_of(TD, "total", "achievable bit demand growth YoY", "2027", "SK hynix")),
    ("Mirae", "2025-12-15", rng_of(TD, "total", "bit production growth YoY", "2027", MIRAE)),
]
G27_TRI = pooled([x for _, _, r in G27_SOURCES for x in sorted(set(r))])

# Quarterly guidance (QoQ bit shipments, %).
QQ = {
    "Samsung": {q: rng_of(TD, "total", "Samsung DRAM bit shipment growth QoQ", f"2026Q{q}",
                          "Samsung Electronics (via earningsapi.io transcript, search summary)" if q == 2 else "Samsung Electronics")
                for q in (2, 3, 4)},
    "SK hynix": {q: rng_of(TD, "total", "SK hynix DRAM bit shipment growth QoQ", f"2026Q{q}", "SK hynix") for q in (2, 3, 4)},
}
VEND_BITS26 = {"Samsung": num(TD, "total", "Samsung bit production", "2026", MIRAE),
               "SK hynix": num(TD, "total", "SK hynix bit production", "2026", MIRAE)}
Q25 = {q: num(TD, "total", "Samsung DRAM bit shipments", f"2025Q{q}", MIRAE) +
       num(TD, "total", "SK hynix DRAM bit shipments", f"2025Q{q}", MIRAE) for q in (1, 2, 3, 4)}

# ==========================================================================
# 3. Time-series model and rolling-origin backtest
# ==========================================================================


def aicc(res, n):
    k = len(res.params)
    return res.aic + 2 * k * (k + 1) / max(n - k - 1, 1e-9)


ARIMA_GRID = [((0, 0, 0), "c"), ((1, 0, 0), "c"), ((2, 0, 0), "c"), ((0, 0, 1), "c"), ((1, 0, 1), "c"), ((0, 1, 1), "n")]


def fit_best_arima(y):
    best = None
    for order, trend in ARIMA_GRID:
        try:
            res = ARIMA(y, order=order, trend=trend).fit()
        except Exception:
            continue
        a = aicc(res, len(y))
        if np.isfinite(a) and (best is None or a < best[0]):
            best = (a, order, trend, res)
    return best


def ts_forecast(name, y):
    """One-step-ahead mean forecast of next log growth from history y (array)."""
    y = np.asarray(y, float)
    if name == "naive":
        return y[-1]
    if name == "drift":
        return y.mean()
    if name == "drift_10y":
        return y[-10:].mean()
    if name in ("ar1", "ar1_10y"):
        yy = y if name == "ar1" else y[-10:]
        res = ARIMA(yy, order=(1, 0, 0), trend="c").fit()
        return float(res.forecast(1)[0])
    if name == "arima_aicc":
        return float(fit_best_arima(y)[3].forecast(1)[0])
    raise ValueError(name)


TS_MODELS = ["naive", "drift", "drift_10y", "ar1", "ar1_10y", "arima_aicc"]


def backtest():
    min_train = ASSUMPTIONS["ts_min_train_years"]["value"]
    yrs, y = HIST["year"].to_numpy(), HIST["y"].to_numpy()
    rows = []
    for i in range(min_train, len(y)):
        for m in TS_MODELS:
            f = ts_forecast(m, y[:i])
            rows.append(dict(model=m, origin=int(yrs[i - 1]), target=int(yrs[i]), actual_growth_pct=100 * np.expm1(y[i]),
                             forecast_growth_pct=100 * np.expm1(f), log_error=f - y[i],
                             ape_level_pct=100 * abs(np.exp(f) - np.exp(y[i])) / np.exp(y[i])))
    bt = pd.DataFrame(rows)
    summ = bt.groupby("model").agg(n=("target", "size"), mape_level_pct=("ape_level_pct", "mean"),
                                   mae_growth_pp=("log_error", lambda e: 100 * np.mean(np.abs(e))),
                                   rmse_log=("log_error", lambda e: float(np.sqrt(np.mean(np.square(e))))),
                                   bias_log=("log_error", "mean")).reset_index()
    return bt, summ.sort_values("mape_level_pct").reset_index(drop=True)


BT, BT_SUMMARY = backtest()
TS_BEST = BT_SUMMARY.iloc[0]["model"]
SIGMA_TS = float(BT_SUMMARY.iloc[0]["rmse_log"])
FULL_ARIMA = fit_best_arima(HIST["y"].to_numpy())          # reported: order chosen by AICc on full sample


def ts_2027_linear():
    """2027 forecast as a linear function of the 2026 log growth: a + b * y26.

    All candidate models are linear in the data, so two evaluations fix a and b.
    """
    y = HIST["y"].to_numpy()
    y26a, y26b = np.log1p(0.20), np.log1p(0.30)
    fa = ts_forecast(TS_BEST, np.append(y, y26a))
    fb = ts_forecast(TS_BEST, np.append(y, y26b))
    b = (fb - fa) / (y26b - y26a)
    return fa - b * y26a, b


TS_A, TS_B = ts_2027_linear()

# ==========================================================================
# 4. Monte Carlo
# ==========================================================================


def simulate(ov: dict | None = None):
    """Run every draw. `ov` fixes named inputs to constants (for the tornado)."""
    ov = ov or {}
    rng = np.random.default_rng(SEED)
    n = N_DRAWS

    def U():
        return rng.random(n)

    def tri(lo, mode, hi):
        return tri_ppf(U(), lo, mode, hi)

    def put(name, x):
        return np.full(n, float(ov[name])) if name in ov else x

    o = {}
    # ---- totals 2025-2026 -------------------------------------------------
    s25 = PROD[2025] * np.exp(rng.normal(0, ASSUMPTIONS["base_2025_log_sd"]["value"], n))
    g26 = put("g26", tri(*G26_TRI) / 100)
    s26 = s25 * (1 + g26)

    # ---- shared mapping draws --------------------------------------------
    f = U()                                               # share of server LPDDR inside Mirae 'server'
    lp_pc = tri(LP_PC_SHARE[0], np.mean(LP_PC_SHARE), LP_PC_SHARE[1])
    auto_sh = tri(*pooled(AUTO_PTS)) / 100
    mu = tri(*MU_SHARE)

    # ---- HBM levels -------------------------------------------------------
    hbm24 = tri(*pooled([HBM24_GREENBERG, sum(MIR_HBM[2024]), sum(MIR_HBM[2024]) / (1 - MU_SHARE[1])]))
    hbm25 = tri(*pooled([UBS_HBM[2025], S_TF[2025] * PROD[2025], sum(MIR_HBM[2025]) / (1 - MU_SHARE[1])]))
    hbm26 = tri(*pooled_arr([TF_HBM_26_FLOOR, UBS_HBM[2026], S_TF[2026] * s26, sum(MIR_HBM[2026]) / (1 - mu)]))

    # ---- history 2023-2025 by category (Mirae mix x production) ----------
    lps_hist = {2023: ASSUMPTIONS["server_lp_2023"]["value"], 2024: LPS_24, 2025: LPS_25}
    hbm_hist = {2023: np.full(n, HBM23), 2024: hbm24, 2025: hbm25}
    cat = {}
    for y in (2023, 2024, 2025):
        tot = s25 if y == 2025 else np.full(n, PROD[y])
        sc = tot / DEM[y]
        m = MIR[y]
        lps = lps_hist[y] * sc
        srv = (m["server"] - f * lps_hist[y]) * sc
        mob = (m["mobile"] - (1 - f) * lps_hist[y]) * sc
        pc = m["pc"] * sc
        auto = auto_sh * tot
        oth = m["other"] * sc - auto
        hbm = hbm_hist[y]
        gddr = m["graphics"] * sc - hbm
        cat[y] = dict(server_ecc=srv, client_pc=pc * (1 - lp_pc), lpddr=mob + pc * lp_pc + lps + auto, hbm=hbm,
                      gddr=gddr, other_consumer=oth, _mob=mob, _pclp=pc * lp_pc, _lps=lps, _auto=auto, _pc=pc)
        cat[y]["total"] = tot

    # ---- 2026 baseline: Mirae 2025 lines x latest unit and content growth --
    m25 = MIR[2025]
    gu_s = tri(*pooled(SRV26_G_PTS)) / 100
    gc_s = tri(*pooled(SRV_GB26_G_PTS)) / 100
    ff = ASSUMPTIONS["content_freeze_floor_pct"]["value"]
    gu_p = tri(*pooled(PH26_G_PTS)) / 100
    gc_p = tri(*pooled([ff, (PH_GB[2026] / PH_GB[2025] - 1) * 100, (PH_GB_DEC[2025] / PH_GB_DEC[2024] - 1) * 100])) / 100
    gu_pc = tri(*pooled(PC26_G_PTS)) / 100
    gc_pc = tri(*pooled([ff, (PC_GB[2026] / PC_GB[2025] - 1) * 100])) / 100
    raw = dict(
        server_ecc=(m25["server"] - f * LPS_25) * (1 + gu_s) * (1 + gc_s),
        _mob=(m25["mobile"] - (1 - f) * LPS_25) * (1 + gu_p) * (1 + gc_p),
        _pc=m25["pc"] * (1 + gu_pc) * (1 + gc_pc),
        gddr=cat[2025]["gddr"] * (1 + tri(*pooled(GDDR26_G_PTS)) / 100),
        _oth=MIR[2026]["other"] * np.exp(rng.normal(0, ASSUMPTIONS["other_2026_log_sd"]["value"], n)),
        _lps=tri(*pooled(LPS_26_PTS)),
    )
    raw_sum = sum(raw.values())
    k26 = (s26 - hbm26) / raw_sum                       # rake factor to the supply total
    o["rake26"] = k26
    o["raw_over_supply26"] = (raw_sum + hbm26) / s26 - 1
    srv26, mob26, pc26 = raw["server_ecc"] * k26, raw["_mob"] * k26, raw["_pc"] * k26
    gddr26, lps26 = raw["gddr"] * k26, raw["_lps"] * k26
    auto26 = auto_sh * s26
    oc26 = raw["_oth"] * k26 - auto26
    cat[2026] = dict(server_ecc=srv26, client_pc=pc26 * (1 - lp_pc), lpddr=mob26 + pc26 * lp_pc + lps26 + auto26,
                     hbm=hbm26, gddr=gddr26, other_consumer=oc26, _mob=mob26, _pclp=pc26 * lp_pc, _lps=lps26,
                     _auto=auto26, _pc=pc26, total=s26)
    o["gu_s26"], o["gu_p26"] = gu_s, gu_p

    # ---- 2027 supply model: wafers x bits per wafer, HBM diversion ---------
    half = ASSUMPTIONS["new_fab_half_year"]["value"]
    cx26 = tri(W_V["CXMT"][2026], (W_V["CXMT"][2026] + CXMT_NOW) / 2, CXMT_NOW)
    sam_add = put("samsung_add", tri(0, W_V["Samsung"][2027] - SAMSUNG_END26, W_V["Samsung"][2027] - SAMSUNG_END26))
    sk_step = W_V["SK hynix"][2027] - SKH_END26
    yongin = put("yongin", tri(0, half * sk_step, sk_step))
    m15x = put("m15x", tri(0, M15X_FULL - M15X_ADD_26, M15X_FULL - M15X_ADD_26))
    mu_step = W_V["Micron"][2027] - W_V["Micron"][2026]
    id1 = put("id1", tri(0, half * mu_step, mu_step))
    tong_max = half * TONGLUO_SHARE * W_V["Micron"][2026]
    tongluo = put("tongluo", tri(0, tong_max, tong_max))
    cx27 = put("cxmt27", tri(W_V["CXMT"][2027], (CXMT_NOW + CXMT_27) / 2, CXMT_27))
    nan_add = tri(0, half * (W_V["Nanya"][2027] - W_V["Nanya"][2026]), W_V["Nanya"][2027] - W_V["Nanya"][2026])
    top3_26 = W_V["Samsung"][2026] + W_V["SK hynix"][2026] + W_V["Micron"][2026]
    top3_27 = (SAMSUNG_END26 + sam_add) + (SKH_END26 + yongin + m15x) + (W_V["Micron"][2026] + id1 + tongluo)
    w26 = top3_26 + cx26 + W_V["Nanya"][2026] + W_OTHERS
    w27 = top3_27 + cx27 + W_V["Nanya"][2026] + nan_add + W_OTHERS
    o["w26"], o["w27"] = w26, w27

    h24 = tri(HBM_WAFERS_24 / W_IND[2024], (HBM_WAFERS_24 / W_IND[2024] + H_TSV_DEC24) / 2, H_TSV_DEC24)
    h25 = tri(H_TSV_DEC24, (H_TSV_DEC24 + H_END[2025]) / 2, H_END[2025])
    h26t = put("h26", tri(H_AMAT_MAR26, H_SAMSUNG_OCT26, H_END[2026]))
    # Annual average 2027 = midpoint of the end-2026 and end-2027 shares. Low: Samsung's ~20% as the
    # end-2026 value; mode: TrendForce 22% -> 30%; high: Samsung's "~30% in 2027" read as a full-year level.
    h27t = put("h27", tri((H_SAMSUNG_OCT26 + H_SAMSUNG_27) / 2, (H_END[2026] + H_END[2027]) / 2, H_SAMSUNG_27))
    h26 = (h26t * top3_26 + (CXMT_HBM[2025] + CXMT_HBM[2026]) / 2) / w26
    h27 = (h27t * top3_27 + (CXMT_HBM[2026] + CXMT_HBM[2027]) / 2) / w27
    r26 = tri(R_TF25, np.median([R_MICRON, R_AMAT]), R_GS[1])
    rho_max = R_GS[1] / R_GS[0] - 1                      # Goldman 4 / 3 - 1
    r27 = put("r27", r26 * (1 + tri(0.0, rho_max / 2, rho_max)))
    o["h26"], o["h27"], o["r26"], o["r27"] = h26, h27, r26, r27

    def mix_factor(s_prev, h_prev, h_cur, r_prev, r_cur):
        return (1 - s_prev) * (1 - h_cur) / (1 - h_prev) + s_prev * (h_cur / h_prev) * (r_prev / r_cur)

    s24, s25b, s26b = hbm24 / PROD[2024], hbm25 / s25, hbm26 / s26
    n25 = (s25 / PROD[2024]) / (W_IND[2025] / W_IND[2024]) / mix_factor(s24, h24, h25, r26, r26) - 1
    n26 = (s26 / s25) / (w26 / W_IND[2025]) / mix_factor(s25b, h25, h26, r26, r26) - 1
    n27 = put("n27", tri_ppf(U(), np.minimum(n25, n26), n26, np.maximum(NODE_FULL_STEP, n26)))
    o["n25"], o["n26"], o["n27"] = n25, n26, n27
    ratio_w = w27 / w26
    s27_sm = s26 * ratio_w * (1 + n27) * mix_factor(s26b, h26, h27, r26, r27)
    hbm27_sm = hbm26 * ratio_w * (1 + n27) * (h27 / h26) * (r26 / r27)
    o["s27_supply_model"] = s27_sm
    hbm_share27 = hbm27_sm / s27_sm

    # ---- 2027 combination: time series, supply model, guidance ------------
    y26 = np.log1p(g26)
    c_ts = TS_A + TS_B * y26 + rng.normal(0, SIGMA_TS, n)
    c_sm = np.log(s27_sm / s26)
    c_gd = np.log1p(tri(*G27_TRI) / 100) + rng.normal(0, SIGMA_GUIDE, n)
    w = np.asarray(ov.get("weights", ASSUMPTIONS["combination_weights"]["value"]), float)
    pick = rng.choice(3, size=n, p=w / w.sum())
    y27 = np.choose(pick, [c_ts, c_sm, c_gd])
    s27 = s26 * np.exp(y27)
    o["c_ts"], o["c_sm"], o["c_gd"] = c_ts, c_sm, c_gd

    # ---- 2027 by category: priority allocation, then additive log-ratio ----
    # Suppliers serve HBM and server first (LTAs, prepayments). So, in order:
    # (a) HBM from the wafer model; (b) server LPDDR = 60% of need; (c) server ECC grows at its
    # own supply guidance, not renormalised; (d) the rest of the combined total is split by ALR.
    lps_d27 = tri(*pooled(LPS_27_PTS))
    lps27 = LPS_FILL_27 * lps_d27                                          # (b)
    hbm27 = hbm_share27 * s27                                              # (a)
    g_srv = put("g_srv27", tri(*SRV27_SUPPLY_G) / 100)
    srv27 = srv26 * (1 + g_srv)                                            # (c)
    rest_raw = s27 - hbm27 - lps27 - srv27
    o["rest_clipped_share"] = float(np.mean(rest_raw <= 0))
    rest = np.maximum(rest_raw, 1e-6)
    g_mob = (1 + tri(*pooled(PH27_G_PTS)) / 100) * (1 + tri(*ASSUMPTIONS["mobile_content_2027_pct"]["value"]) / 100) - 1
    g_pc = (1 + tri(*pooled(PC27_G_PTS + [0.0])) / 100) * (1 + tri(*pooled([ff, (PC_GB[2027] / PC_GB[2026] - 1) * 100])) / 100) - 1
    g_gddr = tri(*ASSUMPTIONS["gddr_2027_growth_pct"]["value"]) / 100
    g_oth = tri(*ASSUMPTIONS["other_2027_growth_pct"]["value"]) / 100
    g_auto = s27 / s26 - 1                       # auto keeps its 2-3% share of total bits (Omdia, TrendForce)
    base = dict(_mob=mob26, _pclp=pc26 * lp_pc, client_pc=pc26 * (1 - lp_pc), gddr=gddr26,
                other_consumer=oc26, _auto=auto26)
    grow = dict(_mob=g_mob, _pclp=g_pc, client_pc=g_pc, gddr=g_gddr, other_consumer=g_oth, _auto=g_auto)
    # ALR: z_k = ln(x_k / x_ref); z_k(2027) = z_k(2026) + ln((1+g_k)/(1+g_ref)); close on `rest`.  (d)
    ref = "other_consumer"
    z = {k: np.log(base[k] / base[ref]) + np.log((1 + grow[k]) / (1 + grow[ref])) for k in base}
    ez = {k: np.exp(v) for k, v in z.items()}
    den = sum(ez.values())
    x27 = {k: rest * ez[k] / den for k in base}
    o["rest_growth27"] = rest / (s26 - hbm26 - lps26 - srv26) - 1
    cat[2027] = dict(server_ecc=srv27, client_pc=x27["client_pc"],
                     lpddr=x27["_mob"] + x27["_pclp"] + lps27 + x27["_auto"], hbm=hbm27, gddr=x27["gddr"],
                     other_consumer=x27["other_consumer"], _mob=x27["_mob"], _pclp=x27["_pclp"],
                     _lps=lps27, _auto=x27["_auto"], _pc=x27["_pclp"] + x27["client_pc"], total=s27)

    # ---- demand ----------------------------------------------------------
    ru_units = tri(*ASSUMPTIONS["rubin_ultra_units_2027_m"]["value"])
    ru_gb = put("ru_content", tri(*pooled([RU_8HI, RU_UBS, RU_TF, RU_NV])))
    hbm_d = {2026: tri(*pooled([UBS_HBM[2026], sum(MIR_HBM[2026]) / (1 - MU_SHARE[1])])),
             2027: UBS_HBM[2027] + ru_units * (ru_gb - RU_UBS) * GB_TO_GB / 1000}
    lps_d = {2026: raw["_lps"], 2027: lps_d27}
    gu_s27 = tri(*pooled(SRV27_G_PTS)) / 100
    srv_rev = {2026: (1 + gu_s) / (1 + MIRAE_SRV_UNIT_G[2026])}
    srv_rev[2027] = srv_rev[2026] * (1 + gu_s27) / (1 + MIRAE_SRV_UNIT_G[2027])
    dem = {}
    for y in (2026, 2027):
        m = MIR[y]
        auto_d = auto_sh * DEM[y]
        dem[y] = dict(server_ecc=(m["server"] - f * lps_d[y]) * srv_rev[y],
                      client_pc=m["pc"] * (1 - lp_pc),
                      lpddr=(m["mobile"] - (1 - f) * lps_d[y]) + m["pc"] * lp_pc + lps_d[y] + auto_d,
                      hbm=hbm_d[y], gddr=np.full(n, np.nan), other_consumer=m["other"] - auto_d,
                      total=np.full(n, DEM[y]),
                      _lps=lps_d[y], _mob=m["mobile"] - (1 - f) * lps_d[y], _pclp=m["pc"] * lp_pc, _auto=auto_d)
    o["hbm_gap27"] = cat[2027]["hbm"] / dem[2027]["hbm"] - 1

    # ---- overlays: DDR5 and DDR4 -----------------------------------------
    s5s26 = tri(SRV_DDR5_1Q25, (SRV_DDR5_1Q25 + 1) / 2, 1.0)
    s5s27 = tri(s5s26, (s5s26 + 1) / 2, 1.0)
    s5p26 = tri(0.60, 0.80, 0.95)
    s5p27 = tri(s5p26, (s5p26 + 1) / 2, 1.0)
    for y, a, b in ((2026, s5s26, s5p26), (2027, s5s27, s5p27)):
        cat[y]["ddr5_total"] = cat[y]["server_ecc"] * a + cat[y]["client_pc"] * b
        cat[y]["ddr4_legacy"] = cat[y]["server_ecc"] * (1 - a) + cat[y]["client_pc"] * (1 - b)

    # ---- quarterly 2026 ----------------------------------------------------
    wS = VEND_BITS26["Samsung"] / sum(VEND_BITS26.values())
    qoq = {}
    for qq in (2, 3, 4):
        a = tri(QQ["Samsung"][qq][0], np.mean(QQ["Samsung"][qq]), QQ["Samsung"][qq][1])
        b = tri(QQ["SK hynix"][qq][0], np.mean(QQ["SK hynix"][qq]), QQ["SK hynix"][qq][1])
        qoq[qq] = (wS * a + (1 - wS) * b) / 100
    idx = {1: 1.0}
    for qq in (2, 3, 4):
        idx[qq] = idx[qq - 1] * (1 + qoq[qq])
    q1 = s26 / sum(idx.values())
    quarters = {qq: q1 * idx[qq] for qq in (1, 2, 3, 4)}
    q25sum = sum(Q25.values())
    quarters25 = {qq: s25 * Q25[qq] / q25sum for qq in (1, 2, 3, 4)}

    o.update(cat=cat, dem=dem, quarters=quarters, quarters25=quarters25, s25=s25, s26=s26, s27=s27,
             hbm_share27=hbm_share27, inputs=dict(g_srv27=g_srv, g26=g26, h26=h26t, h27=h27t, r27=r27, n27=n27, yongin=yongin,
                                                  m15x=m15x, id1=id1, tongluo=tongluo, cxmt27=cx27,
                                                  samsung_add=sam_add, ru_content=ru_gb),
             lps_d27=lps_d27, pick=pick)
    return o


# ==========================================================================
# 5. Outputs
# ==========================================================================
CATS = ["server_ecc", "lpddr", "client_pc", "hbm", "gddr", "other_consumer"]
LABEL = {"server_ecc": "Server ECC (RDIMM/MRDIMM)", "lpddr": "LPDDR (phone, tablet, PC, server, auto)",
         "client_pc": "Client PC (DDR5/DDR4 non-LP)", "hbm": "HBM", "gddr": "GDDR",
         "other_consumer": "Other / consumer", "total": "Total DRAM",
         "ddr5_total": "DDR5 total (overlay)", "ddr4_legacy": "DDR4 legacy, modules (overlay)",
         "_mob": "LPDDR: phone + tablet", "_pclp": "LPDDR: PC", "_lps": "LPDDR: server (SOCAMM/Grace)",
         "_auto": "LPDDR: auto"}
SHORT = {"server_ecc": "Server ECC", "lpddr": "LPDDR", "client_pc": "Client PC", "hbm": "HBM", "gddr": "GDDR",
         "other_consumer": "Other / consumer", "total": "Total"}


def category_table(o):
    rows = []
    cat, dem = o["cat"], o["dem"]
    for y in YEARS:
        for k in CATS + ["total", "ddr5_total", "ddr4_legacy", "_mob", "_pclp", "_lps", "_auto"]:
            if k not in cat[y]:
                continue
            x = cat[y][k]
            kind = ("bucket" if k in CATS else "total" if k == "total" else
                    "overlay (not additive)" if k.startswith("ddr") else "component of LPDDR")
            r = dict(category=k.lstrip("_") if not k.startswith("_") else "lpddr_" + k.lstrip("_"),
                     label=LABEL[k], kind=kind, year=y)
            for nm, v in q(x).items():
                r[f"{nm}_bn_gb"] = v
            for nm, v in q(x / BNGB_PER_EB).items():
                r[f"{nm}_eb"] = v
            r["share_median"] = np.median(x / cat[y]["total"])
            if (y - 1) in cat and k in cat[y - 1]:
                g = q(x / cat[y - 1][k] - 1)
                r["yoy_median"], r["yoy_p10"], r["yoy_p90"] = g["median"], g["p10"], g["p90"]
            if y in dem and k in dem[y] and not np.all(np.isnan(dem[y][k])):
                d = q(dem[y][k])
                gp = q(x / dem[y][k] - 1)
                gb = q(x - dem[y][k])
                r.update(gap_median_bn_gb=gb["median"], gap_p10_bn_gb=gb["p10"], gap_p90_bn_gb=gb["p90"])
                r.update(demand_median_bn_gb=d["median"], demand_p10_bn_gb=d["p10"], demand_p90_bn_gb=d["p90"],
                         gap_median=gp["median"], gap_p10=gp["p10"], gap_p90=gp["p90"])
            rows.append(r)
    df = pd.DataFrame(rows)
    num_cols = df.select_dtypes("number").columns.drop("year")
    df[num_cols] = df[num_cols].round(4)
    return df


def quarterly_table(o):
    rows = []
    for yr, qs in ((2025, o["quarters25"]), (2026, o["quarters"])):
        for qq in (1, 2, 3, 4):
            x = qs[qq]
            r = dict(quarter=f"{yr}Q{qq}", basis="Mirae shipment shape x annual total" if yr == 2025
                     else "Samsung/SK hynix QoQ guidance, 1Q solved to the annual total")
            for nm, v in q(x).items():
                r[f"{nm}_bn_gb"] = v
            for nm, v in q(x / BNGB_PER_EB).items():
                r[f"{nm}_eb"] = v
            prev = qs[qq - 1] if qq > 1 else (o["quarters25"][4] if yr == 2026 else None)
            if prev is not None:
                g = q(x / prev - 1)
                r["qoq_median"], r["qoq_p10"], r["qoq_p90"] = g["median"], g["p10"], g["p90"]
            if yr == 2026:
                g = q(x / o["quarters25"][qq] - 1)
                r["yoy_median"], r["yoy_p10"], r["yoy_p90"] = g["median"], g["p10"], g["p90"]
            r["share_of_year_median"] = np.median(x / (o["s26"] if yr == 2026 else o["s25"]))
            rows.append(r)
    return pd.DataFrame(rows).round(4)


TORNADO_INPUTS = [
    ("h27", "HBM wafer share 2027 (top 3)"),
    ("r27", "HBM trade ratio 2027"),
    ("n27", "Node-migration bit gain 2027"),
    ("yongin", "SK hynix Yongin Ph.1 timing (kwpm)"),
    ("m15x", "SK hynix M15X pull-in (kwpm)"),
    ("id1", "Micron ID1 timing (kwpm)"),
    ("tongluo", "Micron Tongluo timing (kwpm)"),
    ("cxmt27", "CXMT 2027 capacity (kwpm)"),
    ("samsung_add", "Samsung 2027 add, P4 ramp (kwpm)"),
    ("ru_content", "Rubin Ultra HBM per package (GB)"),
    ("g26", "2026 industry bit growth"),
    ("g_srv27", "Server ECC 2027 growth (RDIMM guide)"),
]


def sensitivity(base):
    def metrics(o):
        c27 = o["cat"][2027]
        return dict(total_2027=np.median(o["s27"]), supply_model_2027=np.median(o["s27_supply_model"]),
                    non_hbm_2027=np.median(c27["total"] - c27["hbm"]), hbm_2027=np.median(c27["hbm"]),
                    phone_tablet_2027=np.median(c27["_mob"]), client_pc_2027=np.median(c27["client_pc"]),
                    hbm_sufficiency_2027=np.median(o["hbm_gap27"]))
    b = metrics(base)
    rows = []
    for key, lab in TORNADO_INPUTS:
        lo, hi = np.percentile(base["inputs"][key], [10, 90])
        ml, mh = metrics(simulate({key: lo})), metrics(simulate({key: hi}))
        r = dict(input=key, label=lab, p10_value=lo, p90_value=hi)
        for k in b:
            r[f"{k}_base"] = b[k]
            r[f"{k}_at_p10"] = ml[k]
            r[f"{k}_at_p90"] = mh[k]
            r[f"{k}_swing"] = abs(mh[k] - ml[k])
        rows.append(r)
    df = pd.DataFrame(rows).sort_values("supply_model_2027_swing", ascending=False).reset_index(drop=True)
    return df.round(5)


def checks_table(o):
    cat, dem = o["cat"], o["dem"]
    md = lambda x: float(np.median(x))  # noqa: E731
    rows = []

    def add(name, model, ref, ref_src, note=""):
        rows.append(dict(check=name, model_median=round(model, 3), reference=ref, reference_source=ref_src,
                         note=note))
    c26, c27 = cat[2026], cat[2027]
    add("2026 raw demand-side sum vs supply total (%)", 100 * md(o["raw_over_supply26"]), f"{SUFF26}",
        "TrendForce 2026-07-30 sufficiency ratio", "Positive = the units x content build-up exceeds supply.")
    add("2026 total vs Mirae demand: sufficiency (%)", 100 * md(o["s26"] / DEM[2026] - 1), f"{SUFF26}",
        "TrendForce 2026-07-30", "Mirae demand predates the 2026 price shock.")
    add("2026 HBM + server ECC share of bits (%)", 100 * md((c26["hbm"] + c26["server_ecc"]) / c26["total"]),
        100 * HBM_RDIMM_SHARE26, "TrendForce 2026-08-25 (HBM + RDIMM)")
    add("2026 server order fill rate (%)", FILL_1Q26, f"<60 (4Q25: {FILL_4Q25})",
        "Samsung Securities 2026-01-28",
        "Fill rates of <60% (4Q25) and 66% (1Q26) show a real server shortage that the Mirae demand base "
        "(server sufficiency ~0%) does not capture.")
    add("2027 growth of the ALR remainder (%)", 100 * md(o["rest_growth27"]), "",
        "derived", f"Share of draws where the remainder hit zero: {100 * o['rest_clipped_share']:.2f}%")
    add("2026 server ECC per server (GB)",
        md(c26["server_ecc"] / (SRV_UNITS[2025] * (1 + o["gu_s26"])) * 1000 / GB_TO_GB), SRV_GB[2026],
        "Mirae Dec 2025 content plan", "Our units = Mirae 2025 units x latest growth.")
    add("2026 server bits vs KGI (bn Gb)", md(c26["server_ecc"] + c26["_lps"]), KGI_SRV26, "KGI 2025-11-17 (20.74 bn GB)",
        "KGI is the high case; it includes general-server buying.")
    ph26 = PH25 * (1 + o["gu_p26"]) * PH_GB[2026] * GB_TO_GB / 1000
    add("2026 phones only, IDC units x TrendForce GB (bn Gb)", md(ph26), md(c26["_mob"]),
        "model phone+tablet line", "Mirae's mobile basis holds about 30-40% more bits than phones alone.")
    add("2026 phone+tablet vs Yole mobile (EB)", md(c26["_mob"]) / BNGB_PER_EB, YOLE_MOBILE[2026],
        "Yole via Comet 2025-11-13 (pre-shock)")
    add("2026 HBM: accelerator bottom-up coverage (%)", 100 * (np.mean(NV_BU_26) + ASIC_BU_26) / md(c26["hbm"]),
        "60-70", "hbm-gddr notes (Morgan Stanley, UBS, TrendForce)")
    add("2026 server LPDDR vs Meritz (bn Gb)", md(c26["_lps"]), LPS_26_PTS[0], "Meritz 2026-05-22")
    add("2026 PC LPDDR vs Mac floor (EB)", md(c26["_pclp"]) / BNGB_PER_EB, MAC_FLOOR_EB, "IDC Mac units x 16 GB (lpddr.csv)")
    add("2026 total (EB) vs Yole demand", md(c26["total"]) / BNGB_PER_EB, YOLE_TOT[2026], "Yole via Comet 2025-11-13")
    add("2026 implied node gain n26 (%)", 100 * md(o["n26"]), "most 2026 growth from node migration",
        "TrendForce News citing Chosun Biz (1c share rows)")
    add("2025 implied node gain n25 (%)", 100 * md(o["n25"]), "", "derived")
    add("2027 server ECC growth (%)", 100 * md(c27["server_ecc"] / c26["server_ecc"] - 1), f"{RDIMM27}",
        "TrendForce 2026-07-09 RDIMM bit supply")
    add("2027 server ECC + HBM growth (%)",
        100 * md((c27["server_ecc"] + c27["hbm"]) / (c26["server_ecc"] + c26["hbm"]) - 1), SRV_HBM27_G,
        "TrendForce 2026-08-25")
    add("2027 HBM growth (%)", 100 * md(c27["hbm"] / c26["hbm"] - 1), f"{TF_HBM_27_GROWTH}", "TrendForce 2026-08-04")
    add("2027 HBM bits (bn Gb)", md(c27["hbm"]), UBS_HBM[2027], "UBS 2026-05-13 end demand")
    add("2027 HBM share of bits (%)", 100 * md(o["hbm_share27"]), 100 * S_TF[2027], "TrendForce 2026-06-02")
    add("2027 HBM trade ratio r27 (x)", md(o["r27"]), round(R_TF27, 3),
        "TrendForce-implied from 30% wafers / 13% bits (2026-06-02)", "TrendForce's ratio is vs the all-DRAM average.")
    add("2027 HBM sufficiency (%)", 100 * md(o["hbm_gap27"]), 100 * GS_HBM_GAP_27, "Goldman Sachs 2026-06-01")
    asic27 = (TPU[2027] * np.mean(TPU8_GB) + TRN3[2027] * TRN3_GB) * GB_TO_GB / 1000
    add("2027 HBM: TPU + Trainium3 bottom-up (bn Gb)", asic27, md(c27["hbm"]), "model HBM",
        "Nvidia and AMD 2027 units are not in the sources, so this covers ASICs only.")
    add("2027 server LPDDR supply = 60% of need (bn Gb)", md(c27["_lps"]), LPS_27_PTS[0] * LPS_FILL_27,
        "Meritz need x TrendForce 60% fill")
    add("2027 server ECC per server (GB, Mirae units)", md(c27["server_ecc"]) / SRV_UNITS[2027] * 1000 / GB_TO_GB,
        SRV_GB[2027], "Mirae Dec 2025")
    add("2027 total (EB) vs Yole demand", md(c27["total"]) / BNGB_PER_EB, YOLE_TOT[2027], "Yole via Comet 2025-11-13")
    add("2026 DDR4 module share of total bits (%)", 100 * md(c26["ddr4_legacy"] / c26["total"]), 100 * MU_DDR4_26,
        "TrendForce 2026-05-26 (Micron only)", "Micron's DDR4 share; CXMT and Nanya hold more DDR4.")
    add("1Q26 implied QoQ vs 4Q25 (%)", 100 * md(o["quarters"][1] / o["quarters25"][4] - 1), "", "derived",
        "Solved residual; no source gives 1Q26.")
    return pd.DataFrame(rows)


def inputs_used():
    rows = []
    for (f, i), r in sorted(USED.items()):
        rows.append(dict(file=f"{f}.csv", row=i, segment=r["segment"], metric=r["metric"], period=r["period"],
                         value=r["value"], unit=r["unit"], kind=r["kind"], publisher=r["publisher"],
                         pub_date=r["pub_date"], url=r["url"]))
    return pd.DataFrame(rows)


# ==========================================================================
# 6. Charts (dataviz skill: fixed categorical order, thin marks, hairline grid)
# ==========================================================================
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURF = "#e1e0d9", "#c3c2b7", "#fcfcfb"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]   # slots 1-6, validated
CAT_COLOR = dict(zip(CATS, SERIES))


def style_ax(ax, grid_axis="y"):
    ax.set_facecolor(SURF)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def new_fig(w, h):
    plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"], "font.size": 9})
    fig = plt.figure(figsize=(w, h), dpi=200, facecolor=SURF)
    return fig


def title(fig, t, sub):
    fig.text(0.02, 0.975, t, ha="left", va="top", fontsize=13, color=INK, weight="bold")
    fig.text(0.02, 0.93, sub, ha="left", va="top", fontsize=9, color=INK2)


def chart_stack(o, path):
    fig = new_fig(8.0, 5.2)
    title(fig, "DRAM bit supply by category, 2023-2027",
          "Billion Gb. Bars: median. Whiskers on 2026-2027 totals: 80% (thick) and 95% (thin) intervals.")
    ax = fig.add_axes([0.08, 0.10, 0.62, 0.72])
    style_ax(ax)
    x = np.arange(len(YEARS))
    bottom = np.zeros(len(YEARS))
    for k in CATS:
        vals = np.array([np.median(o["cat"][y][k]) for y in YEARS])
        ax.bar(x, vals, width=0.5, bottom=bottom, color=CAT_COLOR[k], edgecolor=SURF, linewidth=1.0, label=SHORT[k])
        bottom += vals
    for i, y in enumerate(YEARS):
        t = q(o["cat"][y]["total"])
        if y >= 2026:
            ax.vlines(i, t["p2_5"], t["p97_5"], color=INK, linewidth=1.0)
            ax.vlines(i, t["p10"], t["p90"], color=INK, linewidth=3.0)
            top = t["p97_5"]
        else:
            top = t["median"]
        ax.text(i, top + 8, f"{t['median']:.0f}", ha="center", va="bottom", color=INK, fontsize=9, weight="bold")
    ax.set_xticks(x, ["2023", "2024", "2025E", "2026E", "2027F"])
    ax.set_ylabel("bn Gb", color=INK2)
    ax.set_ylim(0, max(np.percentile(o["cat"][2027]["total"], 97.5) * 1.12, 100))
    # legend right, in stack order (top first), with 2027 shares as direct labels
    lx = 0.73
    for j, k in enumerate(reversed(CATS)):
        yy = 0.78 - j * 0.075
        fig.patches.append(plt.Rectangle((lx, yy - 0.012), 0.018, 0.028, transform=fig.transFigure,
                                         color=CAT_COLOR[k], figure=fig))
        sh = np.median(o["cat"][2027][k] / o["cat"][2027]["total"])
        fig.text(lx + 0.027, yy + 0.002, SHORT[k], color=INK, fontsize=9, va="center")
        fig.text(lx + 0.027, yy - 0.026, f"2027 share {100 * sh:.0f}%", color=INK2, fontsize=8, va="center")
    fig.text(0.02, 0.02, "1 EB = 8 bn Gb. 2023-2025: Mirae application mix x production. "
             "Source: model/forecast.py; table in out/forecast_by_category.csv.", color=MUTED, fontsize=7.5)
    fig.savefig(path, facecolor=SURF)
    plt.close(fig)


def dot_interval(ax, yv, d, color, size=36):
    ax.hlines(yv, d["p2_5"], d["p97_5"], color=color, linewidth=1.0, alpha=0.9)
    ax.hlines(yv, d["p10"], d["p90"], color=color, linewidth=3.5, alpha=0.9)
    ax.scatter([d["median"]], [yv], s=size, color=color, edgecolor=SURF, linewidth=1.5, zorder=3)


def chart_growth(o, path):
    fig = new_fig(8.0, 5.0)
    title(fig, "Bit growth by category, 2026 and 2027",
          "Year-on-year change in supply. Dot: median. Thick line: 80% interval. Thin line: 95% interval.")
    ax = fig.add_axes([0.24, 0.12, 0.72, 0.70])
    style_ax(ax, "x")
    rows = CATS + ["total"]
    for i, k in enumerate(rows):
        base_y = len(rows) - 1 - i
        for j, (y, col) in enumerate(((2026, SERIES[0]), (2027, SERIES[1]))):
            d = q(100 * (o["cat"][y][k] / o["cat"][y - 1][k] - 1))
            dot_interval(ax, base_y + (0.17 if j == 0 else -0.17), d, col)
    ax.axvline(0, color=AXIS, linewidth=1.0)
    ax.set_yticks(range(len(rows)), [SHORT[k] for k in reversed(rows)])
    ax.set_xlabel("YoY growth (%)", color=INK2)
    ax.set_xlim(-40, 120)
    for j, (lab, col) in enumerate((("2026 vs 2025", SERIES[0]), ("2027 vs 2026", SERIES[1]))):
        fig.text(0.24 + j * 0.18, 0.865, "●", color=col, fontsize=11, va="center")
        fig.text(0.26 + j * 0.18, 0.865, lab, color=INK, fontsize=9, va="center")
    fig.text(0.02, 0.02, "Supply growth, not demand. Values in out/forecast_by_category.csv.", color=MUTED, fontsize=7.5)
    fig.savefig(path, facecolor=SURF)
    plt.close(fig)


def chart_demand(o, path):
    fig = new_fig(9.0, 5.0)
    title(fig, "Supply against demand by category",
          "Billion Gb. Dot: median, line: 80% interval. Label: sufficiency (supply / demand - 1).")
    rows = CATS
    for p, y in enumerate((2026, 2027)):
        ax = fig.add_axes([0.17 + p * 0.42, 0.15, 0.37, 0.65])
        style_ax(ax, "x")
        for i, k in enumerate(rows):
            yy = len(rows) - 1 - i
            s = q(o["cat"][y][k])
            dd = o["dem"][y][k]
            ax.hlines(yy + 0.14, s["p10"], s["p90"], color=SERIES[0], linewidth=3)
            ax.scatter([s["median"]], [yy + 0.14], s=34, color=SERIES[0], edgecolor=SURF, linewidth=1.5, zorder=3)
            if np.all(np.isnan(dd)):
                ax.text(s["p90"] + 6, yy - 0.14, "no demand source", color=MUTED, fontsize=7.5, va="center")
                continue
            d = q(dd)
            ax.hlines(yy - 0.14, d["p10"], d["p90"], color=SERIES[1], linewidth=3)
            ax.scatter([d["median"]], [yy - 0.14], s=34, color=SERIES[1], edgecolor=SURF, linewidth=1.5, zorder=3)
            gap = np.median(o["cat"][y][k] / dd - 1)
            ax.text(max(s["p90"], d["p90"]) + 6, yy, f"{100 * gap:+.0f}%", color=INK, fontsize=8, va="center")
        ax.set_yticks(range(len(rows)), [SHORT[k] for k in reversed(rows)] if p == 0 else [""] * len(rows))
        ax.set_xlim(0, 290)
        ax.set_title(str(y), color=INK, fontsize=10, loc="left")
        ax.set_xlabel("bn Gb", color=INK2)
    for j, (lab, col) in enumerate((("Supply (model)", SERIES[0]), ("Demand (sources)", SERIES[1]))):
        fig.text(0.17 + j * 0.18, 0.865, "●", color=col, fontsize=11, va="center")
        fig.text(0.19 + j * 0.18, 0.865, lab, color=INK, fontsize=9, va="center")
    fig.text(0.02, 0.045, "Demand: Mirae Dec 2025 by line, server units updated to TrendForce/Micron, HBM from UBS, "
             "server LPDDR from Meritz/Edgewater. GDDR has no demand source.", color=MUTED, fontsize=7.5)
    fig.text(0.02, 0.015, f"Server order fill rates of {FILL_4Q25}% (4Q25) and {FILL_1Q26:.0f}% (1Q26), Samsung Securities, "
             "point to a server shortage larger than the Mirae demand base shows.", color=MUTED, fontsize=7.5)
    fig.savefig(path, facecolor=SURF)
    plt.close(fig)


def chart_tornado(sens, path):
    fig = new_fig(9.0, 5.4)
    title(fig, "What moves 2027 supply",
          "Change in the median when one input goes from its 10th to its 90th percentile; all else as drawn.")
    panels = (("supply_model_2027", "Supply-side model, 2027 total (bn Gb)", 1.0),
              ("hbm_sufficiency_2027", "HBM 2027 sufficiency (pp)", 100.0))
    order = sens[sens["input"] != "g_srv27"].sort_values("supply_model_2027_swing", ascending=True)
    for p, (m, lab, scale) in enumerate(panels):
        ax = fig.add_axes([0.30 + p * 0.36, 0.10, 0.30, 0.62])
        style_ax(ax, "x")
        base = order[f"{m}_base"].iloc[0] * scale
        for i, (_, r) in enumerate(order.iterrows()):
            lo = r[f"{m}_at_p10"] * scale - base
            hi = r[f"{m}_at_p90"] * scale - base
            ax.barh(i, lo, height=0.5, color=SERIES[0], edgecolor=SURF, linewidth=1)
            ax.barh(i, hi, height=0.5, color=SERIES[1], edgecolor=SURF, linewidth=1)
        ax.axvline(0, color=INK2, linewidth=1)
        ax.set_yticks(range(len(order)), list(order["label"]) if p == 0 else [""] * len(order))
        ax.set_title(f"{lab}\nbase median {base:.1f}", color=INK, fontsize=9, loc="left")
        lim = max(1e-6, np.nanmax(np.abs(np.r_[order[f"{m}_at_p10"], order[f"{m}_at_p90"]] * scale - base))) * 1.15
        ax.set_xlim(-lim, lim)
    for j, (lab, col) in enumerate((("Input at its 10th percentile", SERIES[0]), ("Input at its 90th percentile", SERIES[1]))):
        fig.text(0.30 + j * 0.30, 0.865, "■", color=col, fontsize=11, va="center")
        fig.text(0.32 + j * 0.30, 0.865, lab, color=INK, fontsize=9, va="center")
    fig.text(0.02, 0.02, "Rubin Ultra content changes HBM demand only, so it shows in the right panel. "
             "Server ECC growth moves only the phone/PC split; see out/sensitivity.csv.", color=MUTED, fontsize=7.5)
    fig.savefig(path, facecolor=SURF)
    plt.close(fig)


# ==========================================================================
def main():
    OUT.mkdir(exist_ok=True)
    CHARTS.mkdir(exist_ok=True)
    base = simulate()

    cat_df = category_table(base)
    cat_df.to_csv(OUT / "forecast_by_category.csv", index=False)

    bt_out = BT.copy()
    bt_out.insert(0, "row_type", "forecast")
    summ = BT_SUMMARY.copy()
    summ.insert(0, "row_type", "summary")
    summ["selected"] = summ["model"] == TS_BEST
    pd.concat([summ, bt_out], ignore_index=True).round(4).to_csv(OUT / "backtest.csv", index=False)

    quarterly_table(base).to_csv(OUT / "quarterly_2026.csv", index=False)
    sens = sensitivity(base)
    sens.to_csv(OUT / "sensitivity.csv", index=False)
    checks_table(base).to_csv(OUT / "checks.csv", index=False)

    # Combination components and weights.
    comp = []
    s26 = base["s26"]
    for nm, c in (("time_series_" + TS_BEST, base["c_ts"]), ("supply_model", base["c_sm"]), ("guidance", base["c_gd"])):
        g = q(100 * np.expm1(c))
        comp.append(dict(component=nm, growth_median_pct=g["median"], growth_p10_pct=g["p10"], growth_p90_pct=g["p90"],
                         sd_log=float(np.std(c)), level_2027_median_bn_gb=float(np.median(s26 * np.exp(c)))))
    comp = pd.DataFrame(comp)
    iv = 1 / comp["sd_log"] ** 2
    comp["weight_used"] = ASSUMPTIONS["combination_weights"]["value"]
    comp["weight_inverse_variance"] = iv / iv.sum()
    alt = simulate({"weights": tuple(comp["weight_inverse_variance"])})
    comb = q(100 * (base["s27"] / s26 - 1))
    comp.loc[len(comp)] = dict(component="combined (equal weights, linear pool)", growth_median_pct=comb["median"],
                               growth_p10_pct=comb["p10"], growth_p90_pct=comb["p90"],
                               sd_log=float(np.std(np.log(base["s27"] / s26))),
                               level_2027_median_bn_gb=float(np.median(base["s27"])), weight_used=1.0,
                               weight_inverse_variance=np.nan)
    ca = q(100 * (alt["s27"] / alt["s26"] - 1))
    comp.loc[len(comp)] = dict(component="combined (inverse-variance weights, check)", growth_median_pct=ca["median"],
                               growth_p10_pct=ca["p10"], growth_p90_pct=ca["p90"],
                               sd_log=float(np.std(np.log(alt["s27"] / alt["s26"]))),
                               level_2027_median_bn_gb=float(np.median(alt["s27"])), weight_used=np.nan,
                               weight_inverse_variance=1.0)
    comp.round(4).to_csv(OUT / "combination_2027.csv", index=False)
    GTRACK.round(4).to_csv(OUT / "guidance_track_record.csv", index=False)
    HIST.round(5).to_csv(OUT / "history_growth.csv", index=False)
    pd.DataFrame([dict(name=k, value=str(v["value"]), reason=v["reason"]) for k, v in ASSUMPTIONS.items()]).to_csv(
        OUT / "assumptions.csv", index=False)

    chart_stack(base, CHARTS / "01_bits_by_category.png")
    chart_growth(base, CHARTS / "02_growth_by_category.png")
    chart_demand(base, CHARTS / "03_demand_vs_supply.png")
    chart_tornado(sens, CHARTS / "04_tornado_2027.png")
    inputs_used().to_csv(OUT / "inputs_used.csv", index=False)

    # Console summary.
    pd.set_option("display.width", 200)
    print(f"draws={N_DRAWS} seed={SEED}  TS model={TS_BEST} sigma_ts={SIGMA_TS:.4f} sigma_guide={SIGMA_GUIDE:.4f}")
    print(f"full-sample AICc ARIMA order: {FULL_ARIMA[1]} trend={FULL_ARIMA[2]}")
    print(f"G26_TRI={G26_TRI} G27_TRI={G27_TRI}")
    print(BT_SUMMARY.round(4).to_string(index=False))
    print(comp.round(4).to_string(index=False))
    show = cat_df[cat_df.year.isin([2025, 2026, 2027])][["category", "year", "median_bn_gb", "p10_bn_gb", "p90_bn_gb",
                                                         "median_eb", "share_median", "yoy_median",
                                                         "demand_median_bn_gb", "gap_median"]]
    print(show.round(3).to_string(index=False))
    print(sens[["input", "p10_value", "p90_value", "supply_model_2027_swing", "total_2027_swing",
                "hbm_sufficiency_2027_swing"]].to_string(index=False))
    print(checks_table(base).to_string(index=False))
    print(quarterly_table(base)[["quarter", "median_bn_gb", "p10_bn_gb", "p90_bn_gb", "qoq_median", "yoy_median"]].to_string(index=False))
    print(f"inputs cited: {len(USED)} rows")


if __name__ == "__main__":
    main()
