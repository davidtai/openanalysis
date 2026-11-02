# DRAM bit supply by category, 2026 and 2027: method

DRAFT. Model run of 2026-10-30. Script: `model/forecast.py`. Run it with
`.venv/bin/python -I model/forecast.py` from the project folder. It takes about two minutes.
Seed 20261030, 50,000 draws. A rerun gives the same numbers.

## 1. What the model does

The model estimates how many DRAM bits the industry makes in 2026 and 2027. It splits
the bits into six categories that do not overlap. It also compares supply with demand
where a demand source exists.

Units:

- We give bits in billion gigabits (bn Gb).
- 1 GB = 8 Gb. 1 EB = 10^9 GB = 8 bn Gb. This is the decimal convention that Mirae Asset and Yole use.
- DRAM "GB" is really binary (2^30 bytes), and "Gb" is binary too. The sources do not correct for this, and neither do we. Read Mirae bn Gb against Yole EB with a margin of about 7%.
- Supply means production. Supplier stock was "almost depleted" in 4Q25 and at "historic lows" in 2Q26 (TrendForce, supply-chain.csv). So production and shipments are almost the same thing, and we treat them as equal.

## 2. Categories

The six buckets add up to total DRAM bits.

| Bucket | What it holds | Built from |
|---|---|---|
| Server ECC | RDIMM and MRDIMM, DDR5 and DDR4. No HBM. No server LPDDR. | Mirae "server" line, minus the share of server LPDDR that sits in it |
| Client PC | Non-LP DDR5/DDR4 UDIMM and SODIMM | Mirae "PC" line x (1 - LPDDR share of PC) |
| LPDDR | Phone + tablet + PC LPDDR + server LPDDR (SOCAMM, Grace, Vera) + auto | Mirae "mobile" line (less any server LPDDR in it) + PC LPDDR + server LPDDR + auto |
| HBM | HBM stacks | Pooled HBM bit estimates for 2026; wafer model for 2027 |
| GDDR | Graphics memory without HBM | Mirae "graphics" minus HBM in 2025; growth rates after that |
| Other / consumer | TVs, networking, industrial, consoles and the rest | Mirae "other" line minus auto |

Two overlays are not added to the total:

- **DDR5 total** = server ECC x server DDR5 share + client PC x PC DDR5 share.
- **DDR4 legacy (modules)** = the DDR4 part of server ECC and client PC. It leaves out discrete DDR4 chips in consumer and industrial devices, because no source sizes them.

**How we avoid counting bits twice.** Server LPDDR is the trap. TrendForce counts Grace LPDDR in "mobile". Yole counts it in "data center". No source says where Mirae puts it. So we draw a fraction f from U(0, 1):

1. A share f of server LPDDR sits in Mirae's server line, and 1 − f sits in its mobile line.
2. We take each share out of its line.
3. We add server LPDDR back once, as its own line.

The same split applies to demand.

## 3. Step 1: the 2026 total

- **2025 base.** Mirae puts 2025 production at 293.1 bn Gb. We add a 3% log-normal error (assumption A3).
- **2026 growth.** We draw a triangle of 20 / 25 / 27%:
  - Low, 20%: the lowest number in any view published since June 2026 (Micron, Jun 2026, "low-to-mid 20s").
  - Mode, 25%: the centre of the latest view (Micron, Sep 2026, "mid-20s").
  - High, 27%: the top of any 2026-dated view (Counterpoint, Mar 2026, "~26%").
- SK hynix (Jul 2026) also says "mid-20s".
- We do not use the older views (Mirae 20.3%, Micron ~20% in Dec 2025, Omdia ~20%). We cite them for context only.

Result: 2026 total = **363.5 bn Gb [80%: 348.7–378.9]**, or 45.4 EB. That is +24% on 2025.

## 4. Step 2: the 2026 split by category

We start from Mirae's 2025 demand by line. That keeps one set of definitions. We then grow each line by the latest unit forecast and the latest content forecast:

| Line | Unit growth 2026 (triangle: min / median / max of the sources) | Content growth 2026 |
|---|---|---|
| Server | 13 / 17 / 19% (TrendForce Apr and Jul 2026, Micron "high teens") | 15 / 20.1 / 26% (TrendForce 2025 pace, Mirae 2025 pace, Mirae 2026 plan) |
| Phone + tablet | −20 / −15.1 / −13.5% (Counterpoint SoC −20%, IDC −16.7%, TrendForce production, Counterpoint, IDC May) | 0 / 10 / 13.5% (freeze floor A6, TrendForce 7.73→8.5 GB, Counterpoint Dec-24→Dec-25) |
| PC | −20.1 / −11.3 / −9.4% (IDC 3Q26 actual, IDC full year, TrendForce notebooks) | 0 / 4.9 / 9.7% (freeze floor, Mirae plan) |

The other lines:

- **Server LPDDR 2026**: a triangle over Meritz (24), KB-derived (20), Edgewater (21–23) and the TrendForce News figure divided by 10 (28). That gives 20 / 23 / 28 bn Gb.
- **HBM 2026**: a triangle over five estimates: TrendForce ">30", UBS 32.9, TrendForce 9% x our total, Mirae's Samsung + SK hynix bits divided by (1 − Micron share), and the floor. That gives about 30 / 32.9 / 34.6 bn Gb. Micron's share comes from Counterpoint revenue shares (18–21%) and UBS (~20%).
- **GDDR 2026**: the 2025 GDDR value x a growth triangle −20 / −12.5 / +37%. The sources are the RTX 50 supply cut of 15–20% (TechTimes, citing a leak), JPR's −10% for add-in-board units, and Mirae's own graphics-minus-HBM growth. Mirae's view predates the removal of Rubin CPX (Tom's Hardware, Mar 2026), so it is only the upper point.
- **Other**: Mirae's 2026 "other" with a 10% log error (A8).
- **Auto**: 2–3% of total bits (Omdia 2%, TrendForce >3%). We take it out of "other" (A9).
- **PC LPDDR**: 30–35% of PC bits (TrendForce).

**Raking.** The lines above are a units x content build-up. Their sum need not equal supply. So we scale every line except HBM by one factor, which makes the lines add to the 2026 total. HBM stays fixed, because its estimates already count supply. The build-up comes out 0.4% above supply before scaling. TrendForce puts the 2026 sufficiency ratio at −1 to −2%, so the two agree.

## 5. Step 3: the 2027 total

Three forecasts, mixed with stated weights.

### 5a. Time series

**History.** The series is industry bit growth for 2006–2025, 20 years:

| Years | Source |
|---|---|
| 2006–09 | Micron 2011 analyst day (average of Gartner, IDC and iSuppli) |
| 2010–11 | KDB Daewoo 2012 (actual supply growth) |
| 2012–19 | DRAMeXchange via Mirae, May 2020 |
| 2020–22 | Derived (no source gives actual supply growth for these years) |
| 2023–25 | Mirae, Dec 2025 |

How we derive 2020–2022:

1. We take Mirae's 2019 supply (125.6 bn Gb).
2. We take the 2022 level implied by Mirae's 2023 production and its −4.4% change.
3. We spread the gap between them over the three years in the year-to-year shape of Mirae's actual demand growth.

The result is 18.2%, 23.4% and 14.3%. See `out/history_growth.csv`.

**Models tested.** Six models forecast the next year's log growth:

- naive: next year = this year
- drift: the mean of all past years
- drift over the last 10 years
- AR(1)
- AR(1) over the last 10 years
- ARIMA with the order chosen by AICc

**Backtest.** We use a rolling origin. Each model trains on 10 or more years and forecasts one year ahead, for 2016–2025 (10 forecasts). The error is measured on the level of bits.

| Model | MAPE (level) | MAE (growth, pp) | RMSE (log) |
|---|---|---|---|
| **naive** | **6.3%** | 6.4 | 0.093 |
| ARIMA, AICc | 8.9% | 8.6 | 0.107 |
| AR(1) | 9.3% | 8.8 | 0.106 |
| AR(1), last 10 years | 9.4% | 9.0 | 0.107 |
| drift, last 10 years | 9.9% | 9.3 | 0.113 |
| drift | 14.9% | 13.7 | 0.154 |

**Choice.** The naive model wins, so it is the time-series part. It forecasts 2027 growth equal to the 2026 draw.

**Error.** The noise is normal, with sd equal to the backtest RMSE, 0.093 in log growth.

The other models lose because 2006–2011 growth (40–87%) belongs to a different era. That history pulls mean-reverting models up. On the full sample, AICc picks ARIMA(0,1,1), which is close to exponential smoothing.

### 5b. Supply-side model

**Formula.** Standard-equivalent wafers = W x (1 − h) + W x h / r, where:

- W is the wafer capacity.
- h is the HBM share of wafers.
- r is the trade ratio (wafers per HBM bit, against a standard bit).

Bits = standard-equivalent wafers x bits per standard wafer. HBM bits = W x b x h / r. We use the formula in growth form and calibrate it to the 2026 HBM share of bits:

    S27/S26  = (W27/W26) x (1+n) x [ (1-s26)(1-h27)/(1-h26) + s26 (h27/h26)(r26/r27) ]
    HBM27    = HBM26 x (W27/W26) x (1+n) x (h27/h26) x (r26/r27)

Here s26 is the 2026 HBM share of bits and n is the bit gain per wafer from moving to new nodes.

**Wafers, W** (kwpm, annual average):

| Vendor | 2026 | 2027 |
|---|---|---|
| Samsung | 665 (Mirae) | 700 (Mirae end-2026) + P4 ramp tri(0, 35, 35). P5 runs only from 2028 (EconoTimes, vlsi.kr). |
| SK hynix | 586 | 605 (Mirae end-2026) + Yongin tri(0, 20.5, 41) + M15X pull-in tri(0, 10, 10) |
| Micron | 349 | 349 + ID1 tri(0, 10, 20) + Tongluo tri(0, 17.5, 17.5) |
| CXMT | tri(298, 309, 320) | tri(328, 370, 420) |
| Nanya | 65 | 65 + tri(0, 2.5, 5) |
| Others | 89 | 89 |

Where the 2027 terms come from:

- **SK hynix Yongin**: 41 is Mirae's 646 minus SK hynix's end-2026 605.
- **M15X pull-in**: 10 is the 50 kwpm at full use (Korea JoongAng Daily) minus the 40 Mirae counted in 2026.
- **Micron ID1**: 20 is Mirae's 2027 step for Micron.
- **Micron Tongluo**: 17.5 = 0.5 x 10% x 349. TrendForce says Tongluo Phase 1 is above 10% of Micron's capacity in 2H27.
- **CXMT**: 298 and 328 are Mirae's figures. 320 "now" and 420 "by 2027" come from Commercial Times via TrendForce.
- **Others**: Mirae's industry total minus its five vendors (derived).

The mode for each new fab is half of its step. TrendForce (Jul 2026) says new fabs ramp from 2H27 and give material output only in 2028. Micron gives mid-2027 for ID1 and Tongluo (assumption A12). Lam (Oct 2026) says cleanroom space is the binding limit, which supports a slow ramp.

**HBM wafer share, h** (top-3 share, made into an industry share with CXMT's HBM wafers):

- 2026: tri(15, 20, 22)%. Applied Materials gave 15% in Mar 2026. Samsung gave ~20% in Oct 2026. TrendForce gives 22% at end-2026.
- 2027: tri(25, 26, 30)%. These are annual averages: the midpoint of the end-2026 and end-2027 values. The low end uses Samsung's 20% → 30%. The mode uses TrendForce's 22% → 30%. The high end reads Samsung's "~30% in 2027" as a full-year level.

**Trade ratio, r:**

- 2026: tri(2.52, 3.0, 4.0). The 2.52 is the ratio that TrendForce's 18% wafer share and 8% bit share imply for 2025. The 3.0 comes from Micron and Applied Materials. The 4.0 is the top of Goldman's 3–4 range.
- 2027: r26 x (1 + ρ), with ρ = tri(0, 1/6, 1/3). Micron (Sep 2026) says the ratio rises with HBM4 and HBM4E, so ρ is not negative. Goldman's 3–4 against 3 gives the +33% ceiling.

**Node gain, n** (bit gain per standard wafer):

- We back out n from the data. We take the change in total bits and remove the change in wafers and the change in HBM mix.
- This gives n25 = 10.9% and n26 = 14.2% (medians).
- We draw n27 = tri(min(n25, n26), n26, 30%). The 30% is TrendForce's full-node gain for 1-alpha. No fleet reaches that in one year.
- The 1c share data supports a fast migration. SK hynix goes from 10% in 1Q26 to 35% in 1Q27, and Samsung from 16% to 31% across 2026. The EUV counts (Samsung ~20, SK hynix ~24, TrendForce) support it too.

Result: supply model 2027 growth = **+22.0% [80%: 16.2–29.2%]**.

### 5c. Published guidance

**Centre.** A triangle over the source endpoints: 17.9 / 23.5 / 26%. The sources are:

- TrendForce +24% (Jul 2026)
- Micron "low 20s", read as 20–23% (Sep 2026)
- SK hynix "mid-20s", read as 24–26% (Oct 2026)
- Mirae +17.9% (Dec 2025)

**Error.** Guidance has been wrong before, so we add its own track record. We took every forecast in the CSVs that was published in year T−1 for year T and compared it with the history:

| Target | Forecast | Actual | Error (pp) |
|---|---|---|---|
| 2011 | TrendForce 50 | 39 | +11.0 |
| 2012 | Micron 48 | 28.6 | +19.4 |
| 2013 | KDB 28 | 26.6 | +1.4 |
| 2021 | Mirae 20.7 / 20.6 | 23.4 (derived) | −2.7 / −2.8 |
| 2022 | TrendForce 17.9 / 18.6 | 14.3 (derived) | +3.6 / +4.3 |
| 2023 | TrendForce 14.1 | −4.4 | +18.5 |
| 2025 | TrendForce 25 | 24.7 | +0.3 |

The RMSE of the log errors is 0.082. We add normal noise of that size. The errors lean positive: guidance has over-forecast in downturns. We do not correct the bias, because a downturn in 2027 is unlikely while LTAs cover more than 50% of capacity.

### 5d. Weights

We use equal weights: 1/3 for each of the three forecasts.

- The supply model has no track record, so we cannot estimate its error variance. Its spread across draws covers only input uncertainty.
- With so few data points, equal weights usually beat estimated weights.

**How we combine.** We use a linear pool. Each draw takes one of the three forecasts at random, with these weights. We do not average them within a draw. Averaging would assume the three errors are independent, but all three start from the same 2026 base.

| Forecast | 2027 growth median [80%] | sd (log) | Weight | Inverse-variance weight (check) |
|---|---|---|---|---|
| Time series (naive) | +24.1% [10.1, 40.0] | 0.094 | 1/3 | 0.13 |
| Supply model | +22.0% [16.2, 29.2] | 0.040 | 1/3 | 0.70 |
| Guidance | +22.4% [10.0, 36.2] | 0.083 | 1/3 | 0.17 |
| **Combined** | **+22.6% [12.1, 35.0]** | 0.076 | | |
| Inverse-variance check | +22.2% [14.9, 31.3] | 0.059 | | |

The median hardly changes with the weights. The interval does: equal weights give a wider interval than inverse-variance weights.

Result: 2027 total = **446.4 bn Gb [80%: 402.0–496.0]**, or 55.8 EB.

## 6. Step 4: the 2027 split by category

We split the combined 2027 total in priority order. Suppliers serve HBM and servers first:

- SK hynix has LTAs for more than 50% of its 2027–2028 capacity.
- Micron has more than 75% of its 2027 output committed.
- Customers pay up front.

So the lines are set in this order. The combined total does not change.

1. **HBM** = the 2027 total x the HBM share from the supply model (step 5b).
2. **Server LPDDR** = 60% x Nvidia's 2027 need. TrendForce (Jun 2026) says suppliers can meet only ~60%. The need is a triangle over Edgewater 60–70 and Meritz 72.7 bn Gb.
3. **Server ECC** = 2026 server ECC x (1 + g), with g ~ tri(15, 17.5, 22.7)%.
   - The low end and the mode come from TrendForce's RDIMM bit-supply guide of +15–20% for 2027 (Jul 2026). This is the most specific supply source for this line.
   - The high end is Mirae's server demand growth (+22.7%). Supply cannot run far ahead of the demand view.
   - We do not rescale this line after the draw.
4. **The rest.** What is left of the total is split with an additive log-ratio (ALR) model across six lines: phone + tablet, PC LPDDR, client PC, GDDR, other / consumer and auto. The reference is other / consumer:

        z_k(2027) = z_k(2026) + ln((1 + g_k) / (1 + g_ref)),   z_k = ln(x_k / x_ref)

   The shares come back as exp(z) / Σexp(z). They always sum to 1, so the lines always sum to the rest. Each g_k is a source-based growth view. It only sets the relative drift; the size of the rest decides the level.

The rest grows 10.8% (median) on its 2026 value. It never reaches zero in any draw.

The growth views for the rest:

| Line | g, 2027 (triangle) | Source |
|---|---|---|
| Phone + tablet | units −4 / −3 / −1.1% x content 0 / 2.5 / 5% | Counterpoint SoC −3 to −4%, IDC −1.1%; content A7 |
| PC LPDDR and client PC | units −9 / −2 / 0% x content 0 / 5.1 / 10.2% | TrendForce notebooks (low-single-digit fall; −9% if costs pass through), IDC flat; Mirae content plan |
| GDDR | −10 / 0 / +10% | assumption A10 |
| Other | −10 / 0 / +4.9% | assumption A11; Mirae +4.9% is the max |
| Auto | total growth of the same draw | Auto keeps its 2–3% share of total bits (Omdia, TrendForce) |

PC LPDDR and client PC share one growth draw, so the 30–35% LPDDR share of PC holds.

The result: server ECC grows in line with its guide. Phones, PCs, GDDR and other take the bits that are left. Those lines now carry most of the uncertainty in the total. Their 2027 intervals are wide, for example phone + tablet at −14% to +35%.

## 7. Step 5: demand and the gap

Demand comes from the published demand forecasts, mapped into the six buckets in the same way as supply.

| Bucket | Demand source |
|---|---|
| Total | Mirae Dec 2025 (379.8 and 462.1 bn Gb). Yole gives 43 and 51 EB as a lower view. |
| Server ECC | Mirae server, minus the server LPDDR share f, updated for the latest server unit growth. Mirae assumed +7.1% (2026) and +4.0% (2027). We use TrendForce/Micron 13–19% (2026) and 17–19% (2027). |
| LPDDR | Mirae mobile (pre-shock) + PC LPDDR + server LPDDR need (2026 pooled; 2027 Edgewater/Meritz) + auto |
| Client PC | Mirae PC x (1 − LPDDR share). Pre-shock. |
| HBM | 2026: UBS 32.9 and Mirae's vendor sum. 2027: UBS 58.0, adjusted for Rubin Ultra content. |
| GDDR | **No source.** Mirae's graphics minus HBM is noise, and Mirae's figure still holds Rubin CPX. Reported as blank. |
| Other | Mirae other minus auto |

We report the gap as the **sufficiency ratio**, supply / demand − 1. Negative means short.

We also report the gap in bn Gb, as supply − demand. Negative means short.

The phone, tablet and PC demand comes from Mirae's Dec 2025 view, which was made before the 2026 price rise. So the shortfalls there (−10% to −20% in 2027) mostly show demand lost to price. Buyers are not left waiting for that memory. The server, HBM and server-LPDDR demand figures are newer.

**Server ECC: the sufficiency ratio understates the shortage.** On the Mirae demand base, updated for units, server ECC shows +1% in 2026 and −3% in 2027: close to balance. Order fill rates tell a different story. Samsung Securities put server order fill rates below 60% in 4Q25 and at 66% in 1Q26 (server-ddr5.csv). That points to a real shortage, which the Mirae demand base does not capture. Two possible reasons:

- Mirae's content per server (903 GB in 2026) predates the AI-driven upgrades.
- Buyers order more than they need when supply is short, so the orders behind fill rates are inflated.

Neither can be sized from the sources. So read the server sufficiency as an upper bound: the real gap is likely larger.

## 8. Step 6: Monte Carlo and sensitivity

- **Monte Carlo.** We take 50,000 draws, seeded. Every triangle and normal above is drawn independently, except where a line says otherwise (r27 builds on r26; n27 builds on the n26 of the same draw). Every percentile in `out/forecast_by_category.csv` comes from these draws.
- **Tornado.** We set one input to its own 10th percentile, then to its 90th. Everything else keeps its draws. We report the change in the median.
  - We show the supply model's 2027 total, because the combined total dilutes wafer inputs to 1/3.
  - We show HBM sufficiency, because the Rubin Ultra content moves only HBM demand.
  - `out/sensitivity.csv` also has the combined total, non-HBM bits, HBM bits, phone + tablet and client PC.
  - Server ECC growth (16.4% → 20.7%) changes no total. It moves 4.2 bn Gb between server ECC and phone + tablet, and 0.8 bn Gb for client PC, so it sits in the CSV but not in the chart.

| Input (p10 → p90) | Supply model 2027 swing (bn Gb) | Combined total swing | HBM sufficiency swing (pp) |
|---|---|---|---|
| Node gain n27 (12.7% → 24.5%) | 44.3 | 25.1 | 3.5 |
| 2026 growth (21.9% → 25.8%) | 20.0 | 20.4 | 1.9 |
| Trade ratio r27 (3.18 → 4.28) | 15.6 | 7.0 | 24.7 |
| CXMT 2027 (348 → 399 kwpm) | 11.5 | 5.4 | 1.4 |
| HBM wafer share h27 (25.7% → 28.6%) | 6.1 | 2.8 | 9.7 |
| Yongin Phase 1 (9 → 32 kwpm) | 4.3 | 2.0 | 0.5 |
| Samsung P4 ramp (11 → 33 kwpm) | 4.2 | 2.0 | 0.5 |
| Micron ID1 (4 → 16 kwpm) | 2.1 | 0.9 | 0.3 |
| Micron Tongluo (6 → 17 kwpm) | 2.1 | 0.9 | 0.3 |
| M15X pull-in (3 → 9 kwpm) | 1.2 | 0.6 | 0.1 |
| Rubin Ultra HBM (626 → 909 GB) | 0 | 0 | 3.5 |

The top three for 2027 supply are the node gain, the 2026 base and the HBM trade ratio. The new fabs matter little in 2027, because they ramp only from mid-year. CXMT is the largest capacity item. For the HBM gap, the trade ratio dominates.

## 9. Step 7: quarterly 2026

Only Samsung and SK hynix give 2026 quarterly bit guidance:

| Quarter | Samsung | SK hynix |
|---|---|---|
| 2Q26 | "low teens" | "high single digit" |
| 3Q26 | "low to mid single digit" | ~10% |
| 4Q26 | "mid to high teens" | "mid-20s" |

The method:

1. We take the bit-weighted average QoQ of the two vendors. Each word becomes a range, then a triangle.
2. We solve 1Q26 so that the four quarters add to the annual total.
3. For 2025, we spread Mirae's 293.1 bn Gb in the quarterly shape of Mirae's Samsung + SK hynix shipments.

| Quarter | bn Gb median [80%] | QoQ | YoY |
|---|---|---|---|
| 1Q26 | 77.5 [74.3–80.8] | −8.8% (solved) | +30% |
| 2Q26 | 85.4 [81.9–89.0] | +10.2% | +22% |
| 3Q26 | 90.9 [87.2–94.8] | +6.5% | +17% |
| 4Q26 | 109.7 [105.3–114.4] | +20.7% | +29% |

The 1Q26 drop is a residual, not data. No source gives 1Q26. Micron, CXMT and Nanya may not follow the Korean path.

## 10. Results

All figures are bn Gb, median [80% interval]. The 95% intervals and EB figures are in `out/forecast_by_category.csv`.

| Category | 2025 | 2026 | 2027 | 2027 EB | 2027 share |
|---|---|---|---|---|---|
| Server ECC | 109.2 | 157.7 [150.0–165.8] | 186.7 [177.1–196.8] | 23.3 | 41.9% |
| LPDDR | 123.6 | 135.5 [128.5–142.8] | 165.3 [137.0–197.7] | 20.7 | 37.0% |
| – phone + tablet | 101.3 | 94.5 [88.9–100.1] | 103.1 [80.3–128.9] | 12.9 | 23.1% |
| – PC LPDDR | 9.1 | 8.5 [7.9–9.2] | 9.5 [7.3–11.9] | 1.2 | 2.1% |
| – server LPDDR | 5.8 | 23.3 [21.2–25.9] | 40.4 [39.2–42.2] | 5.0 | 9.1% |
| – auto | 7.3 | 9.1 [8.0–10.2] | 12.2 [8.6–16.9] | 1.5 | 2.7% |
| Client PC | 19.0 | 17.7 [16.6–18.9] | 19.6 [15.2–24.7] | 2.5 | 4.4% |
| HBM | 21.2 | 32.5 [31.1–33.8] | 52.2 [44.5–62.2] | 6.5 | 11.7% |
| GDDR | 8.5 | 8.5 [6.3–11.2] | 9.2 [6.2–13.4] | 1.2 | 2.1% |
| Other / consumer | 11.8 | 11.3 [8.7–14.1] | 12.1 [8.4–16.7] | 1.5 | 2.7% |
| **Total** | **293.1** | **363.5 [348.7–378.9]** | **446.4 [402.0–496.0]** | **55.8** | 100% |
| DDR5 total (overlay) | – | 163.7 [154.8–173.2] | 199.7 [188.1–212.0] | 25.0 | 44.8% |
| DDR4 modules (overlay) | – | 11.7 [7.1–16.3] | 6.4 [3.1–11.1] | 0.8 | 1.4% |

| Category | YoY 2026 | YoY 2027 | Sufficiency 2026 | Sufficiency 2027 | Gap 2026 / 2027 (bn Gb) |
|---|---|---|---|---|---|
| Server ECC | +44% [40, 49] | +18% [16, 21] | +1% [−5, +8] | −3% [−16, +15] | +1.7 / −6.0 |
| LPDDR | +10% [6, 13] | +22% [2, 45] | −14% [−20, −9] | −20% [−35, −1] | −22.9 / −40.5 |
| – phone + tablet | −7% [−10, −3] | +9% [−14, +35] | −18% [−24, −12] | −10% [−34, +23] | −21.2 / −12.0 |
| – server LPDDR | +298% | +74% [56, 92] | 0% [−4, +5] | −40% (by construction) | +0.1 / −26.9 |
| Client PC | −6% [−11, −2] | +11% [−13, +37] | −14% [−19, −9] | −19% [−37, +2] | −2.9 / −4.6 |
| HBM | +54% [43, 71] | +61% [38, 91] | −4% [−9, 0] | −10% [−23, +7] | −1.5 / −5.8 |
| GDDR | −2% [−14, +17] | +9% [−14, +36] | no source | no source | – |
| Other / consumer | −5% [−25, +18] | +7% [−15, +33] | +5% [−18, +30] | +24% [−12, +70] | +0.5 / +2.3 |
| Total | +24% [22, 26] | +23% [12, 35] | −4% [−8, 0] | −3% [−13, +7] | −16.3 / −15.7 |

## 11. Checks against sources not used as inputs

`out/checks.csv` has the full list.

| Check | Model | Source |
|---|---|---|
| 2026 build-up vs supply | +0.4% over | TrendForce sufficiency −1 to −2% |
| 2026 HBM + server ECC share | 52.3% | TrendForce HBM + RDIMM 51% |
| 2026 server order fill rate | server sufficiency +1% | Samsung Securities: <60% (4Q25), 66% (1Q26). A real shortage that the Mirae demand base misses. |
| 2026 server ECC per server | 847 GB | Mirae plan 903 GB; Micron says content grows more slowly than planned |
| 2026 HBM covered by accelerator bottom-up | 60% | 60–70% (Nvidia 10–12 + TPU/Trainium 8.4 bn Gb) |
| 2026 server LPDDR | 23.3 | Meritz 24 |
| 2026 phone + tablet | 11.8 EB | Yole mobile 11 EB (pre-shock). Phones alone (IDC x TrendForce 8.5 GB) are 72 bn Gb, 24% below our line, because Mirae's basis is wider. |
| 2027 HBM growth | +61% | TrendForce +50–60%; UBS +76% |
| 2027 HBM bits | 52.2 | UBS 58.0 end demand |
| 2027 HBM share of bits | 11.7% | TrendForce 13% |
| 2027 HBM trade ratio | 3.67 | Goldman 3–4; TrendForce-implied 2.87 (against the all-DRAM average) |
| 2027 HBM sufficiency | −10% | Goldman −6% |
| 2027 server ECC growth | +18.2% | TrendForce RDIMM +15–20% (now an input, see section 6) |
| 2027 server ECC + HBM growth | +25.7% | TrendForce +27% |
| 2027 server ECC per server (Mirae units) | 1,061 GB | Mirae 1,065 GB |
| 2027 server LPDDR | 40.4 | Meritz need x 60% = 43.6 |
| 2027 total | 55.8 EB | Yole demand 51 EB (Nov 2025 view) |
| 2026 DDR4 module share | 3.2% | Micron DDR4 ~7% of its output (TrendForce) |

## 12. Assumptions

These have no direct source row. `out/assumptions.csv` holds the same list as the `ASSUMPTIONS` dict.

| ID | Assumption | Value | Reason |
|---|---|---|---|
| A1 | Words to numbers | low 20s = 20–23, mid-20s = 24–26, high teens = 17–19, and so on | The total-dram notes give 24–26 and 20–23 for Micron's words. The others use the same split. |
| A2 | "~X%" | X ± 1 pp | Convention. |
| A3 | 2025 base error | 3% log sd | KGI and Yole put 2025 within 1–1.5% of Mirae. 3% also covers the gap between production and demand definitions. |
| A4 | Where Mirae puts server LPDDR | f ~ U(0, 1) | No source. This keeps the bits counted once. |
| A5 | 2023 server LPDDR | 0 | LS Securities gives 1.1 bn Gb for 2024, so 2023 was small. |
| A6 | Content freeze floor | 0% growth | Spec cuts and frozen configurations are reported, but no floor number. |
| A7 | 2027 phone content | 0 / 2.5 / 5% | The LPDDR notes suggest flat to +5%. No source. |
| A8 | 2026 "other" error | 10% log sd | No second source on Mirae's basis. |
| A9 | Auto comes out of Mirae "other" and counts as LPDDR | – | The brief puts auto in LPDDR. No source gives the LPDDR share of auto DRAM. |
| A10 | 2027 GDDR growth | −10 / 0 / +10% | No GDDR bit source. Card units fall while GB per AI card rises. |
| A11 | 2027 other growth | −10 / 0 / +4.9% | Mirae +4.9% is the max. The min matches the 2026 fall in consumer units. |
| A12 | New fab gives half a year | mode = 0.5 x step | TrendForce: ramp from 2H27. Micron: ID1 and Tongluo mid-2027. |
| A13 | HBM share is an annual average of year-end values | (end of prior year + end of year) / 2 | TrendForce gives year-end shares only. |
| A14 | CXMT HBM wafers ramp in a straight line | annual = midpoint | SemiAnalysis gives year-end values only. |
| A15 | Trade ratio rises in 2027 | ρ ~ tri(0, 1/6, 1/3) | Micron: it rises. Goldman: 3–4x. r25 = r26. |
| A16 | HBM bits per wafer gain as fast as standard bits | same n | Same DRAM nodes. No source splits the two. |
| A17 | Node gain ceiling | 30% (TrendForce 1-alpha full node) | One full node step for the whole fleet in one year. |
| A18 | Rubin Ultra 2027 units | 0.5 / 1.0 / 1.5 M packages | **Unsupported.** About half of Rubin's 2026 launch volume (1.5–2.4 M). Moves HBM demand only. |
| A19 | Server DDR5 share | 2026 tri(0.90, 0.95, 1.0), rising in 2027 | TrendForce ~90% in 1Q25. DDR4 server end of life at all three majors. |
| A20 | PC DDR5 share | 2026 tri(0.60, 0.80, 0.95), rising in 2027 | **Unsupported** beyond "passed 50% in 2H24". |
| A21 | Equal combination weights | 1/3 each | See 5d. |
| A22 | Backtest training length | 10 years | Gives 10 one-step forecasts. |
| A23 | Quarterly path | Samsung + SK hynix bit-weighted QoQ | Only these two give quarterly guidance. |
| A24 | 2027 priority allocation | HBM → server LPDDR → server ECC → ALR for the rest; auto keeps its share of the total | LTAs, prepayments and supplier statements put HBM and servers first. The server ECC max of 22.7% (Mirae demand) caps supply at the demand view. |

## 13. Derived numbers

These are computed from source rows. They are not quoted from a source.

- History growth for 2020–2022 (section 5a). The 2022 actual used in the guidance track record is one of them.
- 2025 GDDR = Mirae graphics x scale − HBM. The GDDR history for 2023–2025 is the same.
- The 2023–2025 category split: Mirae's demand mix x Mirae production. Only HBM uses its own estimates.
- Trade ratios implied by TrendForce: 2.52 (2025) and 2.87 (2027).
- Node gains n25 and n26.
- "Others" capacity of 89 kwpm, and every new-fab kwpm term in 5b.
- Micron's HBM bit share, taken from revenue shares.
- 2026 server LPDDR from KB (10 / 0.5 = 20) and from TrendForce News (280 / 10 = 28).
- The 2027 server LPDDR need in bn Gb (Meritz 9,084 PB x 8 / 1000 = 72.7).
- Rubin Ultra 8-Hi content of 512 GB (768 x 8 / 12) and the TrendForce package value of 768 GB (384 GB per GPU x 2).
- Mirae's implied server unit growth: (1 + bit growth) / (1 + content growth) − 1.
- Every figure in sections 9–11.

## 14. Weak points

1. **The total depends on Mirae's 2025 base and the 2026 guidance.** All 2026 values scale with 293.1 bn Gb. No second absolute production series exists for 2025.
2. **The 2027 interval is wide (±11%).** The time-series and guidance errors come from history that includes the 2023 cut (−4.4% against +14% forecast) and the 2011–2012 over-forecasts. A sold-out market with LTAs makes such a miss less likely, but we keep the honest history. The inverse-variance check gives a narrower +15% to +31%.
3. **The node gain is backed out, not measured.** It is the largest driver of the supply model. It takes up any error in the wafer figures (Mirae's capacity measures wafer input, not tools) and in h.
4. **There are no kwpm figures for new fabs.** Yongin, ID1, Tongluo and P5 have no company capacity numbers. We build the bounds from Mirae's steps and timing statements.
5. **HBM wafer shares are mixed.** They mix top-3 and industry, end-of-year and annual. Applied Materials (15%) and TrendForce (22%) differ widely for 2026.
6. **Mirae's mobile line is wider than phones.** Phones alone (IDC x TrendForce) give about 76% of it, and Yole's pre-shock mobile figure gives about 93%. The LPDDR level depends on Mirae's definition.
7. **GDDR has no bit source.** It comes from a residual and assumed growth. It is only about 2% of bits.
8. **Phones, PCs, GDDR and other absorb all of the total's uncertainty.** Server ECC is set by its guide (A24), so every error in the 2027 total lands on the rest. Phone + tablet runs from −14% to +35% (80%). If the total comes in low, consumer lines fall. TrendForce says PC DRAM supply "could decline" in 2027, which fits the low side. The server sufficiency (−3%) also understates the shortage: fill rates were below 60% in 4Q25 and 66% in 1Q26.
9. **The demand for phones, PCs and other is pre-shock** (Mirae, Dec 2025). The −14% to −23% gaps there are mostly demand lost to price, not unmet orders. "Other" shows surplus. This is an artifact of taking auto out of Mirae's "other" on both sides.
10. **1Q26 is a residual** (−8.8% QoQ). It is not data.
11. **Some inputs are unverified.** The Samsung 2Q26 QoQ comes from a search summary only (earningsapi.io). The Edgewater figures are third-hand, with an unclear unit. The TrendForce News SOCAMM orders carry a likely 10x unit error. The RTX 50 cut is a leak.
12. **The Rubin Ultra 2027 units and the PC DDR5 share are unsupported** (A18, A20).
13. **Prices do not enter the bit model.** We use the supply-chain file (WFE, EUV, LTAs, inventory) only as context for timing and for the gap section.

## 15. Source key (publisher, period, url)

`out/inputs_used.csv` lists all 250 cited rows with file, row number, value and url. These are the main ones:

| Publisher | Date | Used for | URL |
|---|---|---|---|
| Mirae Asset Securities | 2025-12-15 | Production, demand and app mix 2023–2027; vendor bits; wafer capacity; server and PC units and content; quarterly shipments; HBM vendor bits | https://securities.miraeasset.com/bbs/download/2141014.pdf?attachmentId=2141014 |
| Mirae Asset Daewoo (DRAMeXchange) | 2020-05-13 | Bit growth 2012–2019 | https://securities.miraeasset.com/bbs/download/2074906.pdf?attachmentId=2074906 |
| Mirae Asset Daewoo | 2020-06-05 | 2019 supply level; 2021 forecast | https://securities.miraeasset.com/bbs/download/2075339.pdf?attachmentId=2075339 |
| KDB Daewoo | 2012-11-13 | 2010–2011 growth; 2013 forecast | https://securities.miraeasset.com/bbs/download/166426.pdf?attachmentId=166426 |
| Micron (avg Gartner/IDC/iSuppli) | 2011-02-21 | 2006–2009 growth; 2012 forecast | https://users.cs.utah.edu/~rajeev/pubs/Micron_2011_Winter_Analyst_Conference_FINAL.pdf |
| Micron | 2026-09-30 | 2026 mid-20s, 2027 low 20s; server units; ID1 timing | https://stockanalysis.com/stocks/mu/transcripts/699706-q4-2026/ |
| Micron | 2026-06-24 | 2026 low-to-mid 20s | https://investors.micron.com/static-files/631b1a32-5537-46ae-8f40-82e42fc79dfe |
| Micron | 2026-03-18 | 2026 low 20s | https://www.fool.com/earnings/call-transcripts/2026/03/18/micron-mu-q2-2026-earnings-call-transcript/ |
| Micron | 2025-12-17 | Trade ratio 3x | https://www.fool.com/earnings/call-transcripts/2025/12/17/micron-mu-q1-2026-earnings-call-transcript/ |
| Micron | 2026-09-30 | Trade ratio rising | https://www.fool.com/earnings/call-transcripts/2026/10/01/micron-mu-q4-2026-earnings-call-transcript/ |
| SK hynix | 2026-10-27 | 2027 mid-20s; 4Q26 QoQ; M15X | https://www.fool.com/earnings/call-transcripts/2026/10/28/sk-hynix-skhy-q3-2026-earnings-call-transcript/ |
| SK hynix | 2026-07-29 | 2026 mid-20s; Yongin; 2Q26 QoQ | https://stockanalysis.com/quote/krx/000660/transcripts/653208-q2-2026/ |
| Samsung Electronics | 2026-10-29 | 3Q26 and 4Q26 QoQ | https://stockanalysis.com/quote/krx/005930/transcripts/718820-q3-2026/ |
| Samsung (via Seoul Economic Daily) | 2026-10-01 | HBM ~20% of wafers now, ~30% in 2027 | https://en.sedaily.com/finance/2026/10/01/hbm-prices-to-more-than-double-next-year-as-shortage |
| TrendForce | 2026-07-28 | 2027 supply +24% | https://www.trendforce.com/research/download/RP260728GY |
| TrendForce | 2026-06-02 | HBM wafer 18/22/30%, bit 8/9/13%; Rubin Ultra 384 GB/GPU | https://www.trendforce.com/presscenter/news/20260602-13074.html |
| TrendForce | 2026-07-30 | Sufficiency −1 to −2%; server +17%; new fabs 2H27/2028 | https://www.trendforce.com/presscenter/news/20260730-13158.html |
| TrendForce | 2026-08-04 | HBM bits +50–60%; Rubin Ultra configs | https://www.trendforce.com/presscenter/news/20260804-13166.html |
| TrendForce | 2026-08-25 | HBM + RDIMM 51%; server + HBM +27% | https://www.trendforce.com/presscenter/news/20260825-13198.html |
| TrendForce | 2026-07-09 | RDIMM bits +15–20% in 2027 | https://www.trendforce.com/presscenter/news/20260709-13140.html |
| Samsung Securities | 2026-01-28 | Server order fill rates <60% (4Q25), 66% (1Q26) | https://www.bondweb.co.kr/Data/20261/28/menu01/2026012820.pdf |
| TrendForce | 2026-06-10 | Nvidia gets ~60% of LPDRAM need; SOCAMM cut | https://www.trendforce.com/presscenter/news/20260610-13090.html |
| TrendForce | 2026-01-19 | Tongluo > 10% of Micron capacity in 2H27 | https://www.trendforce.com/presscenter/news/20260119-12883.html |
| TrendForce News (Commercial Times) | 2026-09-24 | CXMT 320 → 420 kwpm | https://www.trendforce.com/news/2026/09/24/news-cxmt-ymtc-ramp-memory-capacity-but-chinas-ai-cloud-boom-could-soak-up-new-supply-through-2027/ |
| TrendForce | 2024-11-06, 2022-08-03, 2021-10-12, 2021-11-04, 2010-11-25 | Guidance track record | trendforce.com press center (see inputs_used.csv) |
| Counterpoint (via ChosunBiz) | 2026-03-12 | 2026 ~26% | https://biz.chosun.com/en/en-it/2026/03/12/O3YVAPAO4ZB4NL7QOKX7SE476I/ |
| Counterpoint | 2026-10-30 | SoC units −20% (2026), −3 to −4% (2027) | https://counterpointresearch.com/en/insights/smartphone-oems-shift-focus-to-profitability-as-soc-shipments-fall-21-percent-yoy |
| Counterpoint | 2026-09-02 | HBM revenue shares | https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share |
| UBS (via Investing.com) | 2026-05-13 | HBM 17.5 / 32.9 / 58.0; Rubin Ultra 768 GB | https://www.investing.com/news/stock-market-news/ubs-says-samsung-to-reach-market-share-parity-for-hbm-with-sk-hynix-by-2027-4684487 |
| Goldman Sachs (via Tiger Brokers) | 2026-06-01 | Trade ratio 3–4x; HBM gap −6% | https://www.itiger.com/news/1117469753 |
| Applied Materials (via The Elec) | 2026-03-17 | HBM 15% of wafers; 3x area | https://www.thelec.net/news/articleView.html?idxno=5886 |
| Korea JoongAng Daily | 2026-01-04 | M15X 50 kwpm | https://www.koreajoongangdaily.com/business/samsung-sk-hynix-dramatically-scaling-up-hbm-production-to-meet-rising-demand-recent-nvidia-deals/12391367 |
| SemiAnalysis | 2026-06-23 | CXMT HBM wafers | https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram |
| Meritz Securities | 2026-05-22 | SOCAMM2 24 bn Gb (2026), 9,084 PB (2027) | https://www.hankyung.com/koreamarket/consensus/pdf/2026-05-899cf1db5212b445c689fe92f4aa08ea |
| Edgewater (via YK Research) | 2026-04-15 | Nvidia LPDDR 21–23 / 60–70 | https://investments.chiayong.com/samsung/2026-04-15/ |
| LS Securities | 2025-03-26 | Server LPDDR 1.1 / 6.0 | https://msg.ls-sec.co.kr/eum/K_20250326_31565_230.pdf |
| IDC | 2026-08-26 | Phones −16.7% (2026) | https://www.idc.com/resource-center/blog/smartphone-shipments-set-for-record-16-7-drop-in-2026-as-the-memory-crisis-hits-full-force/ |
| IDC | 2026-05-26 | Phones 1.09 B (2026), −1.1% (2027) | https://www.idc.com/resource-center/blog/worldwide-smartphone-market-to-decline-13-9-in-2026-as-memory-crisis-and-us-iran-war-constrain-growth/ |
| IDC | 2026-06-02 | PCs −11.3% | https://www.idc.com/resource-center/blog/pc-market-enters-volatile-territory-as-memory-shortage-persists-through-2027/ |
| TrendForce | 2026-05-14 | 8.5 GB per phone (2026) | https://www.trendforce.com/presscenter/news/20260514-13044.html |
| TrendForce | 2026-09-04, 2026-10-08 | Notebooks −9.4% (2026), low-single-digit fall (2027) | https://www.trendforce.com/presscenter/news/20260904-13217.html, https://www.trendforce.com/presscenter/news/20261008-13264.html |
| Yole (via Comet) | 2025-11-13 | Total and mobile demand in EB (checks) | https://comet.tech/getmedia/4363db0d-e447-4ea1-bfef-dec81a68884d/Comet-CMD-2025_presentation_final.pdf |
| KGI Securities | 2025-11-17 | Server bits 2026 (check) | https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/memory-sector-17112025e.pdf |
| Jon Peddie Research | 2026-03-05 | AIB −10% (2026) | https://www.jonpeddie.com/news/q425-pc-graphics-aib-shipments-decreased-4-4-from-last-quarter-to-11-million-units-with-a-cagr-to-2029-of-5-9/ |
| Lam Research (supply-chain.csv) | 2026-10-21 | Cleanroom space is the binding limit (context) | see supply-chain.csv |

## 16. Output files

| File | Contents |
|---|---|
| `out/forecast_by_category.csv` | Category x year: median, p10, p90, p2.5, p97.5 (bn Gb and EB), share, YoY, demand, sufficiency |
| `out/backtest.csv` | Summary per model, then every rolling-origin forecast |
| `out/sensitivity.csv` | Tornado: p10/p90 input values and the median of five outputs at each |
| `out/quarterly_2026.csv` | 2025 and 2026 quarters with QoQ and YoY |
| `out/combination_2027.csv` | The three 2027 forecasts, weights, the combined result and the inverse-variance check |
| `out/checks.csv` | Cross-checks against sources not used as inputs |
| `out/guidance_track_record.csv`, `out/history_growth.csv` | Guidance errors; the growth history |
| `out/assumptions.csv`, `out/inputs_used.csv` | All assumptions; all 250 cited source rows with url |
| `out/placeholders.json` | Every `M:<category>:<year>:<metric>` key in `doc/ram-supply-2026-2027.src.md`, formatted. ddr5 and ddr4-legacy 2026 YoY are "n/a (no source)", because no 2025 overlay exists. |
| `tools/fill_placeholders.py` | Writes `out/placeholders.json` and `doc/ram-supply-2026-2027.filled.md` from `doc/ram-supply-2026-2027.md`. Run it after the model. |
| `out/charts/01–04_*.png` | Stacked bits, growth, demand vs supply, tornado |
| `model/vendor_matrix.py` | Vendor x type matrix (section 17). Imports `forecast.py` and reuses its draws. Run: `.venv/bin/python -I model/vendor_matrix.py` (about 30 s). |
| `out/vendor_by_type.csv` | Year x vendor x type: median, p10, p90 (also p2.5, p97.5, EB), vendor share of the type, share of the vendor's own bits, prior share, fitted/prior ratio, cell confidence. "total" rows are vendor totals; "All vendors" rows are the model columns. |
| `out/vendor_by_type_sensitivity.csv` | The same cells with the Samsung / SK hynix split from Mirae's shipment pages |
| `out/inputs_used_vendor.csv`, `out/assumptions_vendor.csv` | The 83 source rows and the assumptions of the vendor step |
| `out/charts/05_vendor_by_type.png` | Bits by vendor and type (2026, 2027), and each vendor's share of each type |

## 17. Production by company and by RAM type

### 17.1 What we built

A matrix for each year from 2025 to 2027:

- The **rows** are five vendors: Samsung, SK hynix, Micron, CXMT, and "Nanya + others".
- The **columns** are the six buckets of this model.
- Each **cell** is the bits that one vendor makes of one type.

The script is `model/vendor_matrix.py`. It reuses the 50,000 draws of `forecast.py` (same seed). Each draw gets its own matrix, so every cell has a median and an 80% interval. The full table is in `out/vendor_by_type.csv`.

No source publishes such a matrix. TrendForce, Omdia and Counterpoint sell segment shares, but only in paid reports. So we build the matrix from vendor totals, type totals, broker HBM shares and a prior mix. The prior mix is the researcher's judgment, built from the vendor-mix rows.

### 17.2 Method

1. **Vendor totals (rows).** We take each vendor's share of Mirae's bit production and apply it to the model total in each draw. "Nanya + others" is Mirae's industry production minus the four named vendors. It holds Nanya (4.0–4.8 bn Gb) and Mirae's unnamed residual (Winbond, PSMC, smaller Chinese makers).

   | Year | Samsung | SK hynix | Micron | CXMT | Nanya + others |
   |---|---|---|---|---|---|
   | 2025 | 37.9% | 28.9% | 19.0% | 8.0% | 6.2% |
   | 2026 | 34.6% | 29.8% | 18.1% | 8.4% | 9.1% |
   | 2027 | 34.5% | 30.1% | 17.9% | 8.7% | 8.9% |

   The researcher's check script (`tools/vendor_mix_ras_check.py`) adds Nanya to this residual a second time. We count Nanya once.
2. **Type totals (columns).** The six bucket draws of the main model.
3. **HBM cells first.**
   - Each vendor's share of HBM bits is a triangle over the broker figures (min, median, max). We then scale the four shares to sum to 1, and multiply by the HBM total.
   - CXMT gets the remainder each broker leaves.
   - Counterpoint's 2Q26 revenue shares (50 / 33 / 18) are a check, not an input. Revenue shares are not bit shares.

   | Year | Samsung points | SK hynix points | Micron points | CXMT (remainder) |
   |---|---|---|---|---|
   | 2025 | 21, 22 | 58, 57, 60 | 21, 21 | 0, 0 |
   | 2026 | 26, 29, 30 | 52, 49, 46, 47, 48 | 22, 19, 22 | 0, 3 |
   | 2027 | 39, 42, 41 | 39, 41, 35, 39 | 18, 22, 20 | 4, 1, 0 |

   Where the points come from:
   - Samsung Securities (2025, 2026) and Daishin (2025–2027): bit shares from chart labels.
   - JPMorgan: SK hynix 60 / 46 / 41.
   - Citi: Samsung 30 (2026); 42 / 35 / 22 (2027); SK hynix 47 (2026); Micron "remains at 22%".
   - UBS: SK hynix 48% of 2026 bits; 41 / 39 / ~20 in 2027.
4. **The other cells.**
   - **Prior.** The prior is the mix in `sources/vendor-mix-notes.md` section 2: % of each vendor's own bits, for each year.
   - **Noise.** In each draw, every non-HBM prior cell gets gamma noise. The mean is the prior and the spread depends on how well the cell is supported (coefficient of variation 10% strong, 20% medium, 41% weak). Then each row is rescaled to its residual: vendor total minus its HBM.
   - **Why not a plain Dirichlet.** A Dirichlet cannot give cells of one row different precision without moving their means. With equal precision, our construction is a Dirichlet.
   - **Fit.** RAS (iterative proportional fitting, 400 rounds) then scales the cells until every row matches its residual and every column matches the model. The largest error left after the fit is 4e-4 in 2025 and 1e-15 in 2026–2027. No draw gives a negative residual row.
5. **Cell confidence.**

   | | Server ECC | LPDDR | Client PC | GDDR | Other |
   |---|---|---|---|---|---|
   | Samsung | weak | weak | weak | medium | weak |
   | SK hynix | strong (slides) | strong (slides) | weak | weak | weak |
   | Micron | medium | medium | weak | weak | weak |
   | CXMT | weak | strong (prospectus) | weak | weak | weak |
   | Nanya + others | weak | weak | weak | weak | weak |

   PC and Other are weak for every vendor. GDDR is zero in the prior for CXMT and Nanya + others, and HBM is zero for Nanya + others.
6. **Sensitivity.** We also run the matrix with the Samsung / SK hynix split taken from Mirae's quarterly shipment pages. Their combined share stays the same. 2027 uses the 2026 split. The results are in `out/vendor_by_type_sensitivity.csv`.

### 17.3 Results (bn Gb, median [80% interval])

**2026**

| Vendor | Server ECC | LPDDR | Client PC | HBM | GDDR | Other | Total |
|---|---|---|---|---|---|---|---|
| Samsung | 56.9 [43.9–69.9] | 49.7 [36.9–62.4] | 3.0 [1.6–5.1] | 9.3 [8.8–9.7] | 5.1 [3.5–7.3] | 1.4 [0.7–2.6] | 125.8 [120.7–131.1] |
| SK hynix | 57.5 [50.4–64.6] | 25.6 [19.8–32.0] | 5.1 [3.1–7.4] | 15.9 [15.1–16.6] | 2.5 [1.4–4.2] | 1.4 [0.7–2.4] | 108.5 [104.1–113.1] |
| Micron | 28.0 [22.2–34.0] | 25.3 [19.6–31.3] | 2.2 [1.2–3.6] | 6.9 [6.5–7.2] | 0.6 [0.3–1.2] | 2.3 [1.2–3.8] | 65.7 [63.0–68.5] |
| CXMT | 4.8 [2.7–7.5] | 20.5 [17.6–23.2] | 2.8 [1.6–4.3] | 0.5 [0.2–0.8] | 0 | 1.5 [0.8–2.6] | 30.4 [29.2–31.7] |
| Nanya + others | 10.1 [6.0–14.9] | 14.3 [9.4–19.1] | 4.0 [2.3–6.2] | 0 | 0 | 4.3 [2.6–6.4] | 33.1 [31.8–34.5] |

**2027**

| Vendor | Server ECC | LPDDR | Client PC | HBM | GDDR | Other | Total |
|---|---|---|---|---|---|---|---|
| Samsung | 66.3 [50.7–81.5] | 56.2 [38.7–76.2] | 3.0 [1.5–5.5] | 21.1 [17.9–25.1] | 5.2 [3.2–8.1] | 0.9 [0.4–1.9] | 153.8 [138.5–170.9] |
| SK hynix | 67.6 [58.9–76.5] | 35.7 [25.9–47.5] | 5.2 [2.9–8.3] | 19.9 [16.9–23.7] | 3.0 [1.6–5.2] | 1.9 [0.9–3.5] | 134.3 [121.0–149.3] |
| Micron | 32.4 [25.7–39.4] | 31.3 [22.8–40.8] | 2.6 [1.4–4.4] | 10.4 [8.8–12.4] | 0.7 [0.3–1.4] | 1.9 [1.0–3.5] | 80.0 [72.1–88.9] |
| CXMT | 7.7 [4.5–11.7] | 24.5 [19.7–29.6] | 3.2 [1.8–5.2] | 0.8 [0.3–1.5] | 0 | 1.9 [0.9–3.3] | 38.7 [34.8–43.0] |
| Nanya + others | 12.4 [7.4–18.2] | 17.1 [11.0–23.6] | 4.7 [2.6–7.5] | 0 | 0 | 4.9 [2.8–7.6] | 39.6 [35.7–44.0] |

**Vendor share of each type** (median [80%]):

| Type | Year | Samsung | SK hynix | Micron | CXMT | Nanya + others |
|---|---|---|---|---|---|---|
| HBM | 2026 | 28.5% [27.4–29.4] | 48.9% [47.8–50.1] | 21.2% [20.2–21.9] | 1.5% [0.7–2.3] | 0 |
| HBM | 2027 | 40.4% [39.4–41.4] | 38.1% [36.8–39.2] | 19.9% [18.9–20.8] | 1.5% [0.6–2.9] | 0 |
| Server ECC | 2026 | 36.1% [28.0–44.1] | 36.5% [32.3–40.6] | 17.8% [14.1–21.4] | 3.0% [1.8–4.8] | 6.4% [3.8–9.4] |
| Server ECC | 2027 | 35.5% [27.3–43.4] | 36.2% [31.9–40.6] | 17.4% [13.9–21.0] | 4.1% [2.4–6.2] | 6.6% [4.0–9.7] |
| LPDDR | 2026 | 36.7% [27.4–45.9] | 18.9% [14.7–23.5] | 18.7% [14.6–22.9] | 15.2% [13.1–17.0] | 10.5% [7.0–14.0] |
| LPDDR | 2027 | 34.1% [25.1–43.2] | 21.6% [17.2–26.3] | 18.9% [14.9–22.9] | 14.8% [12.5–17.2] | 10.3% [6.9–13.9] |

Other column shares: Samsung holds 61% of GDDR in 2026 and 58% in 2027 (TrendForce: 70% of GDDR7 in 2025). "Nanya + others" holds 38–41% of other / consumer and 23–24% of client PC. Each vendor's own mix is the `share_of_vendor` column.

Checks against the segment evidence:

- **HBM 2026.** Samsung 28.5% of bits sits below Counterpoint's 2Q26 revenue share (33%). Samsung's share rose through the year; Samsung Securities, Daishin and Citi put the full-year 2026 figure at 26–30%.
- **Leaders.** Samsung leads LPDDR and GDDR. SK hynix and Samsung split server ECC about evenly.
- **CXMT** has 15% of LPDDR. The notes expected 10–15%.
- **Server LPDDR** (SOCAMM, Grace) sits inside the LPDDR column. The matrix does not split it by vendor. The SOCAMM2 shares (Samsung 35–50%, SK hynix 30–40%, Micron 20–25%) are evidence for the prior only.

### 17.4 Which cells are least certain

**Widest in bn Gb:**
1. Samsung LPDDR 2027: 38.7–76.2.
2. Samsung server ECC 2027: 50.7–81.5.
3. Samsung server ECC 2026: 43.9–69.9.
4. Samsung LPDDR 2026: 36.9–62.4.
5. SK hynix LPDDR 2027: 25.9–47.5.

Samsung discloses no mix. So its server-vs-LPDDR split is the main unknown of the whole matrix: ±13 bn Gb in 2026, ±16–19 bn Gb in 2027.

**Widest relative to the median:** Samsung other (2027), Micron GDDR and CXMT HBM. Each interval is more than 1.4 times its median, but all of these cells are below 2 bn Gb.

**CXMT HBM 2027** fits at 2.1% of CXMT bits against a prior of 4% (0.52x), because three of the four brokers leave China 0–1% of HBM.

**HBM cells are narrow** (±5% in 2026, ±15–20% in 2027). Most of that width comes from the model's HBM total, not from the vendor split.

### 17.5 Prior against fit: the tension

The prior and the model do not agree on two columns. Prior-implied column totals against model column totals:

| Type | 2026 prior / model (bn Gb) | Model / prior | 2027 prior / model (bn Gb) | Model / prior |
|---|---|---|---|---|
| Other / consumer | 23.3 / 11.3 | 0.49 | 26.0 / 12.1 | 0.46 |
| Client PC | 24.2 / 17.7 | 0.73 | 27.2 / 19.6 | 0.72 |
| Server ECC | 148.6 / 157.7 | 1.06 | 175.0 / 186.7 | 1.07 |
| LPDDR | 125.1 / 135.5 | 1.08 | 153.6 / 165.3 | 1.08 |
| HBM | 33.7 / 32.5 | 0.96 | 55.0 / 52.2 | 0.95 |
| GDDR | 8.4 / 8.5 | 1.01 | 9.5 / 9.2 | 0.97 |

The prior-implied totals are the prior shares x the median vendor totals.

The fit keeps the totals of this model. So in every row it cuts "other" to 0.40–0.51x the prior and client PC to 0.64–0.81x. It gives the freed bits to server ECC and LPDDR:

| Row | Server ECC | LPDDR | Client PC | Other |
|---|---|---|---|---|
| Nanya + others | 1.22–1.25x | 1.23x | 0.79–0.81x | 0.49–0.51x |
| CXMT | 1.05–1.11x | 1.13–1.16x | about 0.70x | about 0.44x |
| Samsung, SK hynix, Micron | 1.03–1.07x | 1.02–1.07x | 0.64–0.69x | 0.40–0.44x |

`out/vendor_by_type.csv` has the fitted/prior ratio for every cell.

**What this means.**

- **Where the legacy bits sit.** The vendor evidence shows many legacy and consumer bits at Nanya, Winbond, PSMC and CXMT. Examples:
  - Nanya: DDR4 + LPDDR4 above 60% of revenue, DDR5 only ~10%.
  - CXMT: DDR series 32% of 2025 revenue.
  - DDR4: 45% of the DDR market in 2024 (CXMT prospectus, citing Omdia).

  This model's "other / consumer" bucket is small (about 3% of bits) because it is Mirae's "other" line minus auto. Mirae sorts bits by end market. So legacy DDR4 for TVs, networking and industrial uses, and DDR4 sold into PCs and Chinese servers, most likely sits inside this model's server, PC and mobile lines. The same bits sit in "other" in the vendor-side prior. The two views count the same bits under different labels, so the totals are not wrong. The labels differ.
- **What to read with care.**
  - The "Nanya + others" row: its server ECC and LPDDR cells are larger than its business supports. Read them as "legacy DDR4/LPDDR4 used in servers, PCs and devices", not as RDIMM DDR5 or LPDDR5X.
  - The DDR4 overlay (section 2) likely understates DDR4. It counts only the DDR4 inside server ECC and client PC, and uses vendor-blind DDR5 shares.
- **What we did not change.** We kept the category totals. A fix would need a source that sizes legacy and consumer DRAM by end market. No source in the CSVs does.

### 17.6 Sensitivity: shipment pages instead of production

Mirae's quarterly shipment pages give Samsung and SK hynix almost the same bits in 2025 (98.7 and 97.6 bn Gb). Mirae's production table instead gives 111.1 and 84.7. With the shipment split:

- **SK hynix's share of server ECC** rises by 1.3 pp in 2026 (36.5% → 37.8%) and 1.0 pp in 2027.
- **Samsung's share** falls by the same amount.
- **LPDDR shares** move under 1 pp in 2026–2027.
- **HBM** does not move, because its cells come from broker shares.
- **2025** moves the most: Samsung's server ECC share goes from 40.1% to 34.6%.

The production table is the base case, because it is the one Mirae uses for its annual totals.

### 17.7 Weak points of the vendor matrix

1. **The prior is judgment.** No public source gives any vendor's PC, server RDIMM or "other" share. Samsung discloses no mix. The Samsung server reading ("close to half", Goldman via Yonhap) comes only from a search summary.
2. **The HBM shares come from chart-label parses.** The Samsung Securities and Daishin figures are read from chart labels. The Citi and JPMorgan figures do not say whether they are bit or revenue shares.
3. **The row shares come from one source.** They are Mirae's Dec 2025 vendor forecasts. Samsung's and SK hynix's 2026 quarterly guidance (section 9) suggests a different split; the sensitivity covers part of that.
4. **"Nanya + others" is mostly an unnamed residual.** 28–32 bn Gb of it has no mix data at all.
5. **Server LPDDR is not split by vendor.** It sits inside the LPDDR column.

### 17.8 Sources for this section (publisher, period, url)

`out/inputs_used_vendor.csv` lists all 83 rows with their row numbers.

| Publisher | Date | Rows | Used for | URL |
|---|---|---|---|---|
| Mirae Asset Securities | 2025-12-15 | total-dram 197–223, 508–531 | Vendor bit production 2025–2027; quarterly shipment pages (sensitivity) | https://securities.miraeasset.com/bbs/download/2141014.pdf?attachmentId=2141014 |
| Samsung Securities | 2026-01-27 | vendor-mix 7–12 | HBM bit shares 2025, 2026 | https://www.bondweb.co.kr/Data/20261/28/menu01/2026012820.pdf |
| Daishin Securities | 2026-02-25 | vendor-mix 14–22 | HBM bit shares 2025–2027; China remainder | https://stock.mk.co.kr/uploads/20260225/1771985434_3b4da2366163be8020e7.pdf |
| Citi (via NeoTeo) | 2026-10-02 | vendor-mix 24–27 | HBM shares 2026–2027 | https://www.neoteo.com/en/citi-forecasts-a-severe-memory-chip-shortage-in-2027 |
| VLSI Korea (JPMorgan, UBS) | 2026-10-25 | vendor-mix 28–30 | SK hynix 60/46/41 (JPMorgan); Samsung 41% 2027 (UBS) | https://www.vlsi.kr/en/bernstein-hbm-crossover-en/ |
| UBS (via Seoul Economic Daily) | 2026-08-10 | hbm-gddr 231, 232 | SK hynix 48% (2026); 39/41 (2027) | https://en.sedaily.com/finance/2026/08/10/samsung-hits-80-percent-yield-on-hbm4-speeds-up-hbm4e |
| UBS (via Investing.com) | 2026-05-13 | hbm-gddr 36 | Micron ~20% (2027) | https://www.investing.com/news/stock-market-news/ubs-says-samsung-to-reach-market-share-parity-for-hbm-with-sk-hynix-by-2027-4684487 |
| Counterpoint (via Seoul Economic Daily) | 2026-09-03 | vendor-mix 0–2 | 2Q26 HBM revenue shares (check) | https://en.sedaily.com/finance/2026/09/03/samsung-doubles-hbm-market-share-to-33-percent-narrowing |
| SemiAnalysis | 2026-06-23 | vendor-mix 34 | CXMT 1% of HBM wafers (2025) | https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram |
| SK hynix | 2026-10-28 | vendor-mix 90–94 | DRAM revenue mix by application (prior) | https://irsvc.teletogether.com/hynix/pdf/hynix2026Q3_eng.pdf |
| Micron | 2026-09-30; 2025-09-23 | vendor-mix 125, 139 | Data-center DRAM share; sole data-center LPDRAM supplier (prior) | https://s25.q4cdn.com/621799436/files/doc_financials/2026/q4/Q4-FY26-Prepared-Remarks.pdf ; https://stockanalysis.com/stocks/mu/transcripts/388210-q4-2025/ |
| CXMT prospectus | 2025-12-30; 2026 | vendor-mix 147, 155, 156 | LPDDR 66% / DDR 32% of revenue; DDR4 45% of DDR market (prior, tension) | https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=12358280&stockid=688825 ; https://static.sse.com.cn/stock/disclosure/announcement/c/202512/002170_20251230_B8QS.pdf |
| Nanya (AlphaMemo; Focus Taiwan) | 2026-10-12 | vendor-mix 158, 159 | DDR4 + LPDDR4 >60%, DDR5 ~10% (prior, tension) | https://www.alphamemo.ai/free-transcripts/ebd9291c-4bc4-4822-b8ce-06e060432bea ; https://focustaiwan.tw/business/202610120025 |
| TrendForce (via Hankyung) | 2025-12-03 | vendor-mix 148–150 | GDDR7 70% Samsung; GDDR 2024 41/49 (prior, check) | https://v.daum.net/v/20251203182738336 |
| Omdia (via Korea Times) | 2025-11-25 | vendor-mix 140 | Samsung 57.9% of mobile DRAM (prior) | https://www.koreatimes.co.kr/amp/business/tech-science/20251125/memory-makers-race-for-ai-servers-expands-to-low-power-chips |
| KIS; BNK | 2025-10-27; 2026-02-03 | vendor-mix 131, 132, 134, 135 | SOCAMM2 shares (prior) | https://www.simmtech.com/upload/media/file/638972081688174181.pdf ; https://www.bondweb.co.kr/Data/20262/3/menu01/ratingBNK_886176.pdf |
| Goldman Sachs (via Yonhap; search summary only) | 2026-08-03 | vendor-mix 99 | Samsung server "close to half" of bits (prior; weak) | https://www.yna.co.kr/amp/view/AKR20260803112800008 |
| Samsung Electronics | 2026-10-29 | vendor-mix 32 | HBM share "in line" with DRAM share (check) | https://stockanalysis.com/quote/krx/005930/transcripts/718820-q3-2026/ |
| Researcher prior | 2026-10-31 | – | Prior mix and cell confidence | `sources/vendor-mix-notes.md`, section 2 |
