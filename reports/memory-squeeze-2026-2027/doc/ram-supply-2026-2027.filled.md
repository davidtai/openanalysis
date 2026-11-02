# DRAM production and supply chain in 2026, and the 2027 outlook, by memory category

**Status: DRAFT, 2026-10-30. Model numbers come from model/forecast.py (50,000 draws, seed 20261030).** All other numbers come from the source CSV files in `sources/`.

**How to read this document**

- Each source figure has a tag: actual, estimate, forecast or derived, and the publish date of the source, for example "(forecast, 2025-12-15)". Where two vintages exist, this document uses the latest one.
- "Derived" means that this document calculated the value from cited figures. The formula is given in the text.
- "Model" means an output of `model/forecast.py`. The text names the file in `out/` that holds it.
- "(per source summary)" means that the cited row's quote does not hold the statement. The statement comes from the summary that the research pass wrote for that row.
- Units: "bn Gb" means billion gigabits. 1 EB = 10^9 GB = 8 bn Gb. "kwpm" means thousand 300 mm wafers per month.
- Bracket numbers such as [3] point to Section 7. Section 7 marks sources that came only from a search summary, or that are paywalled and seen only in summary.

---

## 1. Summary

### 1.1 Main points

1. **Total supply grows about 24% in 2026, and the market is still short.** The model gives 363.5 bn Gb (45.4 EB), +24.2% on 2025. TrendForce puts the 2026 sufficiency ratio at −1% to −2% (estimate, 2026-07-30) [1].
2. **Servers and HBM take most new bits.** HBM plus RDIMM is 51% of 2026 DRAM bit supply (forecast, 2026-08-25) [2]. Server DRAM without HBM is 41.0% of 2026 bit demand for Mirae (forecast, 2025-12-15) [3] and 47% for KGI (forecast, 2025-11-17) [4].
3. **HBM takes wafers out of all other categories.** HBM is 22% of DRAM wafer input at end-2026 but only 9% of bits (forecast, 2026-06-02) [5]. At end-2027 these values are 30% and 13% (forecast, 2026-06-02) [5]. This is the main reason why conventional DRAM stays short in 2027 (Section 3.3).
4. **Contract prices rose fastest in 1H26, and the rise now slows.** Conventional DRAM contract prices rose 93–98% in 1Q26 (actual, 2026-06-01) [6] and 58–63% in 2Q26 (forecast, 2026-03-31) [7]. TrendForce expects 13–18% in 3Q26 (forecast, 2026-07-03) [8] and 10–15% in 4Q26 (forecast, 2026-09-30) [9].
5. **New cleanroom space adds little bit output in 2027.** Substantial output from new fabs comes only in 2028 (forecast, 2026-07-30) [1]. The model gives 2027 total growth of +22.6%, inside the published range of low 20s % (Micron) (forecast, 2026-09-30) [10] to mid-20s % (SK hynix) (forecast, 2026-10-27) [11].
6. **Long-term agreements lock most 2027 supply.** SK hynix has LTAs for more than 50% of its 2027–2028 capacity (actual, 2026-10-28) [12]. Micron has more than 75% of its 2027 output committed (actual, 2026-09-30) [10]. Customers booked about 80% of Samsung's planned 2027 memory output (KB Securities estimate) (estimate, 2026-10-20) [13]. Buyers without LTAs pay most of the price increase (estimate, 2026-07-09) [14].
7. **PCs and phones cut units and memory per device.** IDC expects PC shipments of −11.3% in 2026 (forecast, 2026-06-02) [15] and smartphone shipments of −16.7% (forecast, 2026-08-26) [16]. Low-end phones go back to 4 GB (forecast, 2025-12-11) [17].
8. **The 2027 consensus is "tighter than 2026".** Views differ on duration (Samsung: into 2028 (forecast, 2026-10-29) [18]; SK hynix: through 2030 (forecast, 2026-10-27) [11]), about HBM per Rubin Ultra package (forecast, 2026-08-04) [19], and about how much LPDDR5X goes to servers (forecast, 2026-06-10) [20].

### 1.2 Summary table

The six buckets add to the total. DDR5 and DDR4 modules are overlays: they overlap Server ECC and Client PC, and they are not added. Section 6.2 gives the boundaries.

| Category | 2026 supply (bn Gb / EB) | Share of 2026 bits | 2026 YoY | 2027 projection, bn Gb [80% interval] | 2027 YoY | Main constraint | 2026 price trend |
|---|---|---|---|---|---|---|---|
| Total DRAM | 363.5 / 45.4 | 100% | +24.2% | 446.4 [402.0 to 496.0] | +22.6% | Cleanroom space; HBM wafer crowding [5, 21] | Sharp rise in 1H26, slower in 2H26 (Section 4.1) |
| Server ECC (RDIMM, MRDIMM) | 157.7 / 19.7 | 43.4% | +44.5% | 186.7 [177.1 to 196.8] | +18.2% | RDIMM bits +15–20% in 2027 against server CPUs +>40% [14, 22] | Server contract about +90% 1Q26, about +270% for 2026 (forecasts) [2, 23] |
| Client PC (non-LP) | 17.75 / 2.22 | 4.9% | −6.5% | 19.64 [15.23 to 24.66] | +10.7% | Suppliers move capacity to servers [9] | PC DRAM contract more than +100% 1Q26 (forecast) [23] |
| LPDDR (phone, tablet, PC, server, auto) | 135.5 / 16.9 | 37.3% | +9.6% | 165.3 [137.0 to 197.7] | +21.9% | Wafers moved to HBM and to server SOCAMM2 [24, 25] | LPDDR5X +78–83% 2Q26; mobile +0–5% 4Q26 (forecasts) [26, 27] |
| HBM | 32.52 / 4.07 | 8.9% | +53.9% | 52.22 [44.50 to 62.15] | +60.8% | DRAM wafers at a high trade ratio; TSV capacity (Section 3.3) | Annual contracts; HBM4 12-Hi 36 GB about 600 USD per stack [28] |
| GDDR | 8.466 / 1.06 | 2.3% | −1.5% | 9.217 [6.197 to 13.37] | +9.3% | Suppliers exit GDDR6 [9] | No 2026 contract % in text; RTX 50 card prices +19% in 3 months [29] |
| Other / consumer | 11.31 / 1.41 | 3.1% | −4.6% | 12.07 [8.449 to 16.65] | +7.4% | Legacy lines leave the big three (Section 2.7) | DDR2 contract +55–60% 2Q26 (estimate) [30] |
| DDR5 (overlay; not added) | 163.7 / 20.5 | 45.1% | n/a (no source) | 199.7 [188.1 to 212.0] | +21.8% | Same wafers as server and client; 1c node ramp [31] | DDR5 16Gb spot about 12.4× from Mar 2025 to Oct 2026 (derived) [32] |
| DDR4 modules (overlay; not added) | 11.70 / 1.46 | 3.2% | n/a (no source) | 6.425 [3.125 to 11.06] | −42.0% | End of life at Samsung, SK hynix and Micron [33] | DDR4 8Gb spot about 31.8× from Feb 2025 to Oct 2026 (derived) [34] |

Total sufficiency (supply / demand − 1): −4.3% in 2026 (−16.30 bn Gb) and −3.4% in 2027 (−15.70 bn Gb).

### 1.3 Model results

![DRAM bits by category, 2023–2027](../out/charts/01_bits_by_category.png)

![Supply against demand by category, 2026 and 2027](../out/charts/03_demand_vs_supply.png)

Values in bn Gb. Intervals: 80% (p10–p90) and 95% (p2.5–p97.5) of the draws. Sufficiency: supply / demand − 1 [80% range]. Source: `out/forecast_by_category.csv`.

| Category | 2026 median | 2026 80% | 2026 95% | 2027 median | 2027 80% | 2027 95% | Sufficiency 2026 | Sufficiency 2027 |
|---|---|---|---|---|---|---|---|---|
| Server ECC | 157.7 | 150.0–165.8 | 146.0–170.2 | 186.7 | 177.1–196.8 | 172.2–202.4 | +1.1% [−5.2%, +7.9%] | −3.1% [−16.4%, +15.1%] |
| Client PC | 17.75 | 16.61–18.90 | 16.03–19.52 | 19.64 | 15.23–24.66 | 12.75–28.18 | −14.1% [−19.3%, −8.8%] | −18.9% [−37.1%, +1.6%] |
| LPDDR | 135.5 | 128.5–142.8 | 124.9–146.7 | 165.3 | 137.0–197.7 | 120.7–221.2 | −14.5% [−19.5%, −9.1%] | −19.8% [−35.0%, −0.7%] |
| – phone + tablet | 94.46 | 88.90–100.1 | 86.06–103.1 | 103.1 | 80.25–128.9 | 66.98–147.3 | −18.3% [−24.2%, −11.9%] | −10.5% [−33.9%, +22.6%] |
| – server LPDDR | 23.26 | 21.23–25.94 | 20.39–27.21 | 40.35 | 39.24–42.15 | 39.06–42.88 | +0.4% [−4.2%, +5.3%] | −40.0% (set by the 60% fill rule) |
| HBM | 32.52 | 31.12–33.76 | 30.57–34.26 | 52.22 | 44.50–62.15 | 40.90–68.37 | −4.4% [−8.6%, −0.3%] | −9.9% [−23.3%, +7.3%] |
| GDDR | 8.466 | 6.272–11.24 | 5.369–12.93 | 9.217 | 6.197–13.37 | 4.931–16.07 | no demand source | no demand source |
| Other / consumer | 11.31 | 8.723–14.14 | 7.459–15.78 | 12.07 | 8.449–16.65 | 6.827–19.62 | +4.6% [−17.5%, +29.5%] | +24.1% [−11.8%, +70.2%] |
| **Total** | 363.5 | 348.7–378.9 | 341.1–387.1 | 446.4 | 402.0–496.0 | 377.9–531.1 | −4.3% [−8.2%, −0.2%] | −3.4% [−13.0%, +7.3%] |
| DDR5 (overlay) | 163.7 | 154.8–173.2 | 150.2–178.2 | 199.7 | 188.1–212.0 | 182.2–218.8 | – | – |
| DDR4 modules (overlay) | 11.70 | 7.067–16.32 | 5.056–18.41 | 6.425 | 3.125–11.06 | 1.994–13.88 | – | – |

**What sufficiency means here.** Sufficiency compares model supply with a published demand view. A negative value means short. The total uses Mirae demand of 379.8 bn Gb (2026) and 462.1 bn Gb (2027) (forecast, 2025-12-15) [3]. The phone, tablet and PC demand also comes from Mirae's December 2025 view, which was made before the 2026 price rise. So the phone and PC gaps mostly show demand lost to price, not orders that wait for memory. The server gap is probably understated. Server order fill rates were below 60% in 4Q25 and 66% in 1Q26 (estimate, 2026-01-28) [35]. Read the server sufficiency as an upper bound.

**How the model sets the 2027 total.** The model mixes three forecasts of 2027 growth (model, `out/combination_2027.csv`). A naive time-series model gives +24.1% [80%: 10.1% to 40.0%]. A supply model of wafers, HBM share, trade ratio and node gain gives +22.0% [16.2% to 29.2%]. Published guidance gives +22.4% [10.0% to 36.2%]. The model gives each forecast a weight of 1/3 and pools the draws. The result is +22.6% [12.1% to 35.0%], or 446.4 bn Gb. Inverse-variance weights would give the supply model a weight of 0.70 and the other two 0.13 and 0.17. That check gives +22.2% [14.9% to 31.3%]. The median hardly moves, but the interval is narrower. The model keeps equal weights, because the supply model has no track record.

**Main sensitivities.** The tornado chart moves one input from its p10 to its p90 (model, `out/sensitivity.csv`). For the supply model's 2027 total, the largest input is the node-migration bit gain (12.7% to 24.5%), with a swing of 44.3 bn Gb. Next come 2026 industry growth (21.9% to 25.8%), with 20.0 bn Gb, and the HBM trade ratio (3.18 to 4.28), with 15.6 bn Gb. CXMT 2027 capacity (348 to 399 kwpm) moves 11.5 bn Gb. Each new fab moves 4.3 bn Gb or less, because new fabs ramp only from mid-2027. For the 2027 HBM gap, the trade ratio dominates: it moves HBM sufficiency by 24.7 percentage points. The HBM wafer share moves it by 9.7 points, and Rubin Ultra HBM per package by 3.5 points.

![Tornado chart of 2027 sensitivities](../out/charts/04_tornado_2027.png)

---

## 2. Categories

### 2.0 Total DRAM (reference for all categories)

**2026 production.** The model starts from Mirae's 2025 production of 293.1 bn Gb (estimate, 2025-12-15) [3]. It applies the 2026 growth views published since June 2026. Micron raised its view from about 20% (forecast, 2025-12-17) [36] to mid-20s % (forecast, 2026-09-30) [10]. Mirae's own December 2025 forecast was 352.5 bn Gb (forecast, 2025-12-15) [3]. Yole gives 43 EB of 2026 demand (forecast, 2025-11-13) [37].

Model: 363.5 bn Gb, 80% interval 348.7 to 378.9 bn Gb (45.4 EB), YoY +24.2%.

Mirae bit production by vendor (bn Gb, 2025-12-15). 2025 is an estimate; 2026–2027 are forecasts.

| Vendor | 2025 | 2026 | 2027 |
|---|---|---|---|
| Samsung | 111.1 [3] | 122.0 [3] | 143.2 [3] |
| SK hynix | 84.7 [3] | 105.2 [3] | 125.1 [3] |
| Micron | 55.8 [3] | 63.7 [3] | 74.5 [3] |
| CXMT | 23.3 [3] | 29.5 [3] | 36.0 [3] |
| Nanya | 4.0 [3] | 4.3 [3] | 4.8 [3] |
| Industry total | 293.1 [3] | 352.5 [3] | 415.7 [3] |

The five vendors add to 324.7 bn Gb in 2026, 27.8 bn Gb below the industry total (derived). Mirae does not name the remainder. Revenue share in 2Q26 (actual, TrendForce 2026-09-07): Samsung 39.4% [38], SK hynix 24.9% [38], Micron 23.3% [38], CXMT 9.5% (estimate, search snippet only) [38], Nanya 1.7% (derived: 2.612 / 154.73) [38].

**Quarterly.** Only Samsung and SK hynix give quarterly bit guidance:

| Vendor | 2Q26 | 3Q26 | 4Q26 guide |
|---|---|---|---|
| Samsung | low teens % (actual, 2026-07-30) [39] | low to mid single digit % (actual, 2026-10-29) [18] | mid to high teens % (forecast, 2026-10-29) [18] |
| SK hynix | high single digit % (actual, 2026-07-29) [40] | about 10% (actual, 2026-10-27) [11] | mid-20s % (forecast, 2026-10-27) [11] |

The model turns these into industry quarters (model, `out/quarterly_2026.csv`): 77.5 bn Gb (1Q26), 85.4 (2Q26), 90.9 (3Q26) and 109.7 (4Q26). The 1Q26 value is a residual that makes the four quarters add to the year. No source gives 1Q26.

---

### 2.1 Server ECC DRAM (RDIMM, MRDIMM)

#### 2026 production

- Model: 157.7 bn Gb, 80% interval 150.0 to 165.8 bn Gb (19.7 EB). Share 43.4%. YoY +44.5%.
- Mirae (forecast, 2025-12-15) [3]: 155.5 bn Gb of 2026 server demand, 41.0% of DRAM bits and +35.0% YoY [3]. Mirae server excludes HBM.
- KGI (forecast, 2025-11-17) [4]: 20.74 bn GB of 2026 server demand (165.9 bn Gb, derived: × 8), 47% of DRAM bits and +45% YoY [4].
- TrendForce: HBM plus RDIMM is 51% of 2026 DRAM bit supply (forecast, 2026-08-25) [2]. The model gives 52.3% for HBM plus server ECC (model, `out/checks.csv`).
- Server DDR5 is about 90% of server DRAM bits from 1Q25 (actual, 2025-05-28) [41]. The 2024 forecast for 2025 was 60–65% (forecast, 2024-07-22) [42].
- Vendors: no source gives server bits by vendor. SK hynix server DDR5 shipments grew more than 40% QoQ in 3Q26 (actual, 2026-10-27) [11].

#### Supply chain and constraints

- **Wafers.** In 1Q26, the wafer revenue of a 64 GB DDR5 RDIMM was higher than that of HBM (estimate, 2026-06-02) [5]. Suppliers therefore put server DDR5 first.
- **Fill rate.** Server order fill rates were below 60% in 4Q25 (estimate, 2026-01-28) [35] and 66% in 1Q26 (estimate, 2026-01-28) [35].
- **Module parts.** TrendForce cut its 2026 server forecast to about 13% in April 2026 (forecast, 2026-04-15) [43]. It cited PMIC lead times of 35–40 weeks and BMC lead times of 21–26 weeks (per source summary). Rambus set record product revenue of about 114 million USD in 3Q26 (actual, 2026-10-26) [44].
- **MRDIMM.** Rambus sizes MRDIMM at 600 million USD in total (forecast, 2026-10-26) [44].
- **CXL.** No source gives 2026 CXL memory volume.

#### Prices and contracts

| Quarter | Server DRAM contract change, QoQ | Source |
|---|---|---|
| 3Q25 | +3% to +8% | (forecast, 2025-07-07) [45] |
| 2H25 | +64% cumulative | (forecast, 2026-08-25) [2] |
| 1Q26 | more than +60% (first call); about +90% (revised) | (forecast, 2026-01-05) [46]; (forecast, 2026-02-02) [23] |
| 3Q26 | +13% to +18% | (forecast, 2026-07-09) [14] |
| 4Q26 | undersupplied; no % in text | (forecast, 2026-09-30) [9] |
| Full year 2026 | about +270% | (forecast, 2026-08-25) [2] |

- Omdia module prices for RDIMMs are in Section 4.3. An analyst on the June 2026 Micron call quoted about 1,500 USD for a 64 GB server module (estimate, 2026-06-24) [47]. That is 44.9% above the Omdia 2Q26 forecast (derived: 1,500 / 1,035 − 1) [48]. The analyst value probably reflects non-LTA pricing.
- RDIMM spot costs about 4.48× more per GB than client UDIMM spot (derived: 67.7 / 15.1) [49]. Section 4.2 has the module spot prices.
- LTA volumes are more than 30% of server DDR5 shipments in 2H26 (estimate, 2026-07-30) [50]. Some LTAs signed from 2Q26 carry price ceilings (estimate, 2026-08-25) [2].
- TrendForce expects server DRAM prices to rise each quarter through 2H27 (forecast, 2026-07-09) [14].

#### Demand drivers (units × content)

- **Units.** TrendForce raised its 2026 server shipment growth from 4% (forecast, 2025-10-29) [51] to 17% (estimate, 2026-07-30) [1]. Micron says high teens % for 2026 and 2027 (forecast, 2026-09-30) [10].
- **AI servers.** AI server shipments grow 32.2% in 2026 and about 36% in 2027 (forecast, 2026-10-14) [52]. AI servers are about 75% of 2026 server revenue (forecast, 2026-10-14) [52].
- **CPUs.** Server CPU shipments grow 31% in 2026 and more than 40% in 2027 (forecast, 2026-10-22) [22].
- **Content.** Mirae forecasts 903 GB per server in 2026 and 1,065 GB in 2027 (forecast, 2025-12-15) [3]. The model implies 847 GB in 2026 (model, `out/checks.csv`). Buyers moved some systems from 96 GB and 128 GB modules to 32 GB and 64 GB modules (estimate, 2026-07-09) [14]. CSPs and OEMs reduced RDIMM capacity per server in 1H26 (estimate, 2026-08-04) [19].
- **Buyer spend.** Memory takes 47% of CSP capex in 2026 and 68% in 2027 (forecast, 2026-08-25) [2].

#### 2027 outlook

- Model: 186.7 bn Gb, 80% interval 177.1 to 196.8 bn Gb, YoY +18.2%. Sufficiency −3.1% (−6.033 bn Gb).

| Source | Date | 2027 view | Model against the view |
|---|---|---|---|
| TrendForce | 2026-07-09 | RDIMM bit supply +15% to +20% [14] | Inside (+18.2%). This guide is a model input, so the match is by design. |
| TrendForce | 2026-08-25 | Server DRAM plus HBM bit supply +27% [2] | Slightly below: model +25.7% (`out/checks.csv`) |
| Mirae | 2025-12-15 | Server demand 190.9 bn Gb, +22.7% [3] | Below. Mirae's +22.7% is the cap of the model range. |

- **Disagreement.** Mirae demand (+22.7%) is above TrendForce RDIMM supply (+15% to +20%). The difference is the size of the 2027 server shortage. All views sit below server CPU growth of more than 40%.

#### Risks

- Server CPU supply. A CPU shortage delayed server builds in 2Q26, and US CSPs built DRAM stock (estimate, 2026-07-09) [14]. If CPUs stay short, RDIMM demand moves later.
- KGI's 47% share is the high case. It assumes US CSP general-purpose servers grow 50% in 2026 (forecast, 2025-11-17) [4].

---

### 2.2 DDR5 overall (server + client PC)

**This is an overlay. It overlaps Server ECC (Section 2.1) and Client PC (Section 2.3), and it is not added into the total.** The model builds it as server ECC × server DDR5 share plus client PC × PC DDR5 share.

#### 2026 production

- Model: 163.7 bn Gb, 80% interval 154.8 to 173.2 bn Gb (20.5 EB). Share 45.1%. YoY n/a (no source).
- No source gives DDR5 bits. Server DDR5 went from 40% of server bits in 2024 (forecast, 2024-07-22) [42] to about 90% in 1Q25 (Section 2.1). Older "adoption" figures count platforms, not bits (estimate, 2023-08-15) [53].
- Client PC DDR5 passed DDR4 in 2H24 (forecast, 2023-08-30) [54]. No source gives a 2025 or 2026 PC DDR5 share. The model assumes 60% to 95% (assumption A20 in `model/METHOD.md`).
- Node mix drives DDR5 bit growth. The 1c share of production rises from 10% to 34% at SK hynix during 2026 (estimate, 2026-09-07) [31], and from 16% to 31% at Samsung (estimate, 2026-09-07) [31]. These are media reports, not company data.

#### Supply chain and constraints

DDR5 shares the constraints of Sections 2.1 and 2.3. For DDR5, supply remains tight and suppliers allocate parts (per source summary) (actual, 2026-10-21) [34].

#### Prices and contracts

- DDR5 16Gb die contract price: 5.5 USD in 3Q25 and 17.2 USD forecast for 4Q26 (KGI) (estimate, 2025-11-17) [4].
- Mirae: DDR5 contract prices rose 123% in 2025 up to December (estimate, 2025-12-15) [3].
- DDR5 2Gx8 spot rose 307% from early September to 2025-11-18 (actual, 2025-11-19) [55]. The DDR5 16Gb spot rose about 12.4× from March 2025 to October 2026 (derived; the two price bases differ) [32]. Section 4.2 has the end points.

#### Demand drivers (units × content)

DDR5 demand is server units × server content (Section 2.1) plus non-LP client units × client content (Section 2.3).

#### 2027 outlook

- Model: 199.7 bn Gb, 80% interval 188.1 to 212.0 bn Gb, YoY +21.8%.
- No source gives a DDR5-only 2027 forecast, so no published range exists to compare. The model value follows from the server and client lines and the assumed DDR5 shares.

#### Risks

- 1c and 1-gamma yields. Substantial output from new fabs comes only in 2028 [1], so 2027 bit growth depends on node migration.

---

### 2.3 Client PC DRAM (non-LP)

#### 2026 production

- Model: 17.75 bn Gb, 80% interval 16.61 to 18.90 bn Gb (2.22 EB). Share 4.9%. YoY −6.5%.
- Mirae (forecast, 2025-12-15) [3]: PC DRAM demand of 30.6 bn Gb in 2026, 8.0% of DRAM bits and +5.8% YoY [3]. KGI also gives 8% (forecast, 2025-11-17) [4].
- The model takes LPDDR out of the PC line. TrendForce puts LPDDR at 30% to 35% of PC DRAM demand (2024) (forecast, 2024-01-17) [56].
- Vendors: no source gives client bits by vendor.
- Quarterly: IDC reports 62.7 million PCs in 3Q26, −20.1% YoY (actual, 2026-10-09) [57].

#### Supply chain and constraints

- PC DRAM supply could decline in 2027 as more capacity shifts to server use (forecast, 2026-09-30) [9].
- Tier-1 PC OEM DRAM inventory declined in 1Q26 (estimate, 2026-02-02) [23].
- Micron is winding down its Crucial consumer business (per source summary) [58].

#### Prices and contracts

| Quarter | PC DRAM contract change, QoQ | Source |
|---|---|---|
| 2Q25 | 0% | (forecast, 2025-03-25) [59] |
| 3Q25 | +8% to +13% | (forecast, 2025-07-07) [45] |
| 1Q26 | more than +100% | (forecast, 2026-02-02) [23] |

- The 16 GB DDR5 UDIMM contract price rises 3.89× from 3Q25 to 4Q26 (derived: 176.0 / 45.2; Section 4.3) [48, 60].
- DDR5 8 GB SO-DIMM contract average: 133.00 USD in the second half of September 2026 (actual, 2026-09-30) [61], or 16.6 USD per GB [61].

#### Demand drivers (units × content)

- **Units.** IDC counted 284.7 million PCs in 2025 (actual, 2026-01-14) [62]. IDC forecasts −11.3% in 2026 and ASP +17% (forecast, 2026-06-02) [15]. TrendForce forecasts notebooks at −9.4% in 2026 (forecast, 2026-09-04) [63]. Micron says PC and mobile units may fall by double digits (forecast, 2026-09-30) [10].
- **Content.** Mirae forecasts 14.7 GB per PC in 2026 and 16.2 GB in 2027 (forecast, 2025-12-15) [3]. TrendForce gave 11.8 GB per notebook for 2024 (forecast, 2024-06-25) [64]. Copilot+ PCs keep a 16 GB floor (per source summary) (estimate, 2026-01-05) [65].
- **Cost pressure.** CPU, DRAM and SSD were 45% of a 900 USD notebook BOM in 1Q25 and 68% in 3Q26 (estimate, 2026-09-04) [63]. A brand needs about an 80% price rise to hold margin (estimate, 2026-09-04) [63].

#### 2027 outlook

- Model: 19.64 bn Gb, 80% interval 15.23 to 24.66 bn Gb, YoY +10.7% [−12.7% to +37.3%].

| Source | Date | 2027 view | Model against the view |
|---|---|---|---|
| TrendForce | 2026-09-30 | PC DRAM supply could decline [9] | Median outside (above). The lower part of the 80% interval is a decline. |
| TrendForce | 2026-10-08 | Notebook units fall a low single digit %; high single digit % if brands pass on all costs [66] | The model uses these unit falls, with content growth on top |
| Mirae | 2025-12-15 | PC DRAM demand 35.9 bn Gb, +17.5% [3] | Below |

- **Why the model sits above the "decline" view.** The model sets HBM and server lines first, so client PC carries part of the error in the total (Section 6.1).

#### Risks

- More notebook production moves back to China: the share outside China falls from about 24% (2025) to 21% (2026) (forecast, 2026-10-28) [67].
- LPCAMM2 and LPDDR take share from SO-DIMM in notebooks (Section 2.6).

---

### 2.4 GPU memory: HBM

#### 2026 production

- Model: 32.52 bn Gb, 80% interval 31.12 to 33.76 bn Gb (4.07 EB). Share 8.9%. YoY +53.9%.
- Published 2026 values: TrendForce more than 30 bn Gb (forecast, 2025-05-22) [68]; UBS 32.9 bn Gb (forecast, 2026-05-13) [69]; TrendForce's 9% share × Mirae total = 31.7 bn Gb (derived) [5].
- **Share.** HBM is 8% of DRAM bit supply in 2025, 9% in 2026 and 13% in 2027 (estimate for 2025, forecasts for 2026–2027; 2026-06-02) [5].
- **Vendors.** UBS: SK hynix 17.7 bn Gb, Samsung 9.7 bn Gb (forecast, 2026-05-13) [69]. Mirae: SK hynix 16.1, Samsung 11.6 bn Gb (forecast, 2025-12-15) [3]. UBS gives SK hynix 48% of 2026 bits (forecast, 2026-08-10) [70]. No source gives Micron HBM bits.
- **Revenue share (Counterpoint).** SK hynix / Samsung / Micron: 50% / 33% / 18% in 2Q26 (actual, 2026-09-02) [71].
- **Quarterly (Mirae, forecast 2025-12-15).** Samsung: 2.1, 2.5, 3.1, 3.8 bn Gb for 1Q26–4Q26 [3]. SK hynix: 3.4, 3.9, 4.2, 4.6 bn Gb [3].
- **Generation.** SK hynix began HBM4 mass shipments in 2Q26 (actual, 2026-10-01) [28]. It expects HBM4 to pass HBM3E in volume and revenue in 4Q26 (forecast, 2026-10-28) [12]. HBM4 was 60% of Samsung HBM revenue in 3Q26 (actual, 2026-10-29) [72]. Nvidia began Vera Rubin production shipments in August 2026 (actual, 2026-08-26) [73].

#### Supply chain and constraints

- **Wafers.** Samsung says HBM takes about 20% of DRAM wafers now and close to 30% next year (estimate, 2026-10-01) [28]. Applied Materials said 15% in March 2026 (estimate, 2026-03-17) [74]. Section 3.3 explains the trade ratio.
- **TSV capacity, end-2026.** TrendForce (search snippet): Samsung 150, SK hynix 200, Micron 100 kwpm (forecast, 2025-08-05) [75]. KB Securities: HBM wafer output 250 kwpm, probably Samsung (forecast, 2026-01-04) [76]. These two values for Samsung disagree.
- **Yield.** Samsung HBM4 yield went from below 60% (February) to close to 80% (August), based on industry sources (estimate, 2026-08-10) [70].
- **Fabs and packaging.** M15X and the Singapore HBM facility are in Section 3.1. CoWoS, base dies and bonders are in Section 3.4.

#### Prices and contracts

- HBM uses annual contracts. HBM wafer revenue fell below that of DDR5 64 GB RDIMM in 1Q26 (estimate, 2026-06-02) [5]. Micron raised its HBM prices for calendar 2027 "significantly", with a reset at the start of the year (actual, 2026-09-30) [77].
- HBM4 12-Hi 36 GB: about 600 USD per stack in 2026 (estimate, 2026-10-01) [28] and about 1,300 USD in 2027 (forecast, 2026-10-01) [28]. That is 2.08 USD per Gb and 4.51 USD per Gb (derived: price / 288 Gb).
- 2027: HBM contract prices +70% to +140% (forecast, 2026-08-25) [2]. Blended HBM ASP +121% (forecast, 2026-09-29) [78].
- Sold-out status: Micron agreed price and volume for all of its 2026 HBM (actual, 2025-12-17) [36]. Samsung sold out for 2027 (actual, 2026-10-29) [72]. SK hynix says DRAM and HBM are essentially sold out through 2029 (actual, 2026-10-28) [79]. Micron has contracted the bulk of 2027 HBM bits (actual, 2026-10-01) [28].

#### Demand drivers (units × content)

| Accelerator | HBM per package | 2026 units | 2027 units |
|---|---|---|---|
| Nvidia B300 | 288 GB [80] | Nvidia total 5.4 million (forecast, 2025-07-31) [81] | – |
| Nvidia Rubin | 288 GB [82] | Blackwell 71% of high-end GPU shipments [83] | – |
| Nvidia Rubin Ultra | 1,024 GB (GTC 2025) [84]; 768 GB (UBS) [69] | – | under review [19] |
| AMD MI455X | 432 GB [85] | revenue from 3Q26, big step in 4Q26 [86] | – |
| Google TPU (Ironwood) | 192 GiB [87] | 4.13 million [88] | 9.87 million [88] |
| AWS Trainium3 | 144 GB [89] | 1.8 million [90] | 2.8 million [90] |

- Bottom-up check for 2026: Nvidia about 10–12 bn Gb [81] plus TPU and Trainium3 about 8.4 bn Gb [88]. That covers about 60% of the model's 2026 HBM (model, `out/checks.csv`). No source explains the rest.

#### 2027 outlook

- Model: 52.22 bn Gb, 80% interval 44.50 to 62.15 bn Gb, YoY +60.8%. Sufficiency −9.9% (−5.769 bn Gb). HBM share of 2027 bits: 11.7% (model, `out/checks.csv`).

| Source | Date | 2027 view | Model against the view |
|---|---|---|---|
| TrendForce | 2026-08-04 | Bits +50% to +60% [19] | Slightly above (+60.8%) |
| UBS | 2026-05-13 | 58.0 bn Gb [69], +76.3% (derived: 58.0 / 32.9) | Below, in bits and in growth |
| TrendForce share × Mirae total | 2026-06-02 | 54.0 bn Gb (derived: 13% × 415.7) [5] | Below; the model share is 11.7%, not 13% |
| Morgan Stanley | 2026-08-06 | Embedded HBM demand more than +60% [91] | At the edge of the view |
| Goldman Sachs | 2026-06-01 | Supply-demand gap −6.0% [92] | The model gap is deeper (−9.9%) |

- **Disagreement.** UBS (+76.3%) is above TrendForce (+50% to +60%). The main swing is HBM per Rubin Ultra package. Nvidia started to evaluate lower-specification configurations in early 3Q26 (forecast, 2026-08-04) [19]. The candidates are 8-Hi HBM4E, 12-Hi HBM4 and 8-Hi HBM4 (per source summary). UBS already cut its assumption from 1 TB to 768 GB (forecast, 2026-05-13) [69]. The TrendForce view is the later one (August 2026).

#### Risks

- A lower Rubin Ultra configuration cuts GB per package. 8-Hi parts carry a 10% to 20% per-Gb premium over 12-Hi (forecast, 2026-09-29) [78].
- CXMT HBM: about 5 kwpm (end-2025), 30 kwpm (end-2026) and 55 kwpm (end-2027) (estimate, 2026-06-23) [93]. Its HBM3E yield is in Section 3.6.

---

### 2.5 GPU memory: GDDR

#### 2026 production

- Model: 8.466 bn Gb, 80% interval 6.272 to 11.24 bn Gb (1.06 EB). Share 2.3%. YoY −1.5%.
- No public source gives GDDR bits. Mirae "graphics DRAM" is HBM plus GDDR (forecast, 2025-12-15) [3]: 46.1 bn Gb in 2026, 12.1% of bits and +52% YoY [3].
- GDDR as a residual: 46.1 minus 30 to 32.9 bn Gb of HBM gives about 13–16 bn Gb in 2026 (derived) [3, 68, 69]. The two terms come from different sources, so the residual is noisy. The model uses the 2025 residual and then a growth range (Section 6.1).
- Vendors: Micron stopped 2 GB GDDR7 for gaming and moved to 3 GB parts for AI (actual, 2026) [94]. This leaves Samsung and SK hynix as the GDDR7 sources for RTX 50 cards (per source summary).
- Quarterly units: JPR counted 12.5 million add-in boards in 2Q26 (actual, 2026) [95].

#### Supply chain and constraints

- Suppliers scale back GDDR6 production and exit the market (forecast, 2026-09-30) [9]. GDDR7 demand comes mainly from AI chips (per source summary).
- Nvidia reportedly delayed the RTX 50 Refresh because of memory cost (per source summary) [58].

#### Prices and contracts

- GDDR6 contract: −8% to −3% in 2Q25 (forecast, 2025-03-25) [59]. The 2026 graphics price changes are in TrendForce chart images only.
- Card prices: Nvidia reportedly cut RTX 50 supply to partners by 15% to 20% in January 2026 (leak) (estimate, 2026-06-21) [29]. Newegg median prices rose up to 39% (estimate, 2026) [96].

#### Demand drivers (units × content)

- **Units.** JPR add-in-board shipments were 44.28 million in 2025 (derived: sum of quarters) [97]. JPR expects about −10% in 2026 (forecast, 2026-03-05) [97].
- **Content.** RTX PRO 6000: 96 GB GDDR7 (actual, 2025) [98]. Rubin CPX (128 GB GDDR7) (forecast, 2025-09-09) [99] left the roadmap at GTC 2026 (actual, 2026-03) [100]. Do not count CPX demand in 2026–2027.

#### 2027 outlook

- Model: 9.217 bn Gb, 80% interval 6.197 to 13.37 bn Gb, YoY +9.3%.
- No source gives a 2027 GDDR bit forecast, so no published range exists to compare. JPR expects add-in boards to fall 5.9% a year from 2024 to 2029 (forecast, 2026-03-05) [97]. The model median sits above that unit trend, because GB per AI card rises and GDDR shares the rest of the total (Section 2.3).

#### Risks

- GDDR is about 2% of bits in the model. Its error moves the total very little.

---

### 2.6 LPDDR (phone, tablet, PC, server SOCAMM/Grace, auto)

#### 2026 production

- Model: 135.5 bn Gb, 80% interval 128.5 to 142.8 bn Gb (16.9 EB). Share 37.3%. YoY +9.6%.
- Model parts: phone + tablet 94.46, server 23.26, PC 8.533, auto 9.086 bn Gb.
- No source gives total LPDDR bits. Published parts:

| Part | 2026 value | Basis |
|---|---|---|
| Phones (Yole) | 11 EB = 88 bn Gb [101] | Mobile demand, forecast 2025-11-13, before the price spike |
| Phones (units × content) | 9.1 EB = 72.8 bn Gb (derived: 1.07 bn units × 8.5 GB) [26, 102] | TrendForce production and content |
| Mirae "mobile DRAM" | 127.4 bn Gb = 15.9 EB [3] | Demand, forecast 2025-12-15; 11.2 GB per phone [3] |
| Server LPDDR (Nvidia SOCAMM2) | 24 bn Gb = 3.0 EB [103]; about 20 bn Gb [104] | Meritz; KB-derived |
| Auto | 2% to more than 3% of DRAM bits [105, 106] | Mostly LPDDR4/5 (per source summary) [107] |

- **Conflict.** Mirae mobile DRAM is far above Yole and units × content. Section 6.4 explains the content figures behind this.
- **Share.** Mobile share of DRAM bits in 2026: Mirae 33.5% (forecast, 2025-12-15) [3], KGI 29% (forecast, 2025-11-17) [4]. Omdia gives 28% for 2025 (estimate, 2026-08-21) [105].
- **Generation mix.** LPDDR4X was 42% of 2025 mobile bit output, and LPDDR5X the rest (forecast, 2025-07-17) [108]. LPDDR4 supply falls more than 40% in 2026 (forecast, 2026-06-01) [109]. LPDDR6 starts small: the first LPDDR6 phone targets 0.2–0.3 million units (estimate, 2026-08-31) [110].
- **Vendors.** No source gives LPDDR5X output by vendor. Micron reduced supply to smartphone brands in 2Q26 (actual, 2026-08-28) [111]. Mobile DRAM revenue rose 80% QoQ in 2Q26 (actual, 2026-08-28) [111], while bit shipments were flat (per source summary).

#### Supply chain and constraints

- **HBM takes wafers.** Samsung's view of the HBM wafer share is in Section 2.4. Conventional DRAM supply could be displaced at two to three times that pace (per source summary) [24].
- **Servers take LPDDR wafers.** Samsung puts 30,000–40,000 wafers per month into Nvidia SOCAMM2. That is about 5% of its DRAM output (estimate, 2025-12-03) [25].
- **SOCAMM2.** Samsung was first to mass-produce 192 GB modules (actual, 2026-03-11) [104]. SK hynix followed in April 2026 (actual, 2026-04-20) [112].
- **Allocation.** Nvidia halved SOCAMM capacity per Vera Rubin module in June 2026 (actual, 2026-06-10) [20]. Suppliers can meet only about 60% of Nvidia's estimated 2027 LPDRAM needs (forecast, 2026-06-10) [20].
- **LPDDR4 exit.** Samsung stopped new LPDDR4/4X orders on 2026-04-17 (actual, 2026-04-20) [113] and ends production in December 2026 (forecast, 2026-04-20) [113]. Micron keeps LPDDR4 for long-life products (actual, 2026-05-26) [114].

#### Prices and contracts

| Quarter | Value | Source |
|---|---|---|
| 1Q26 | LPDDR4X and LPDDR5X about +90% | (forecast, 2026-02-02) [23] |
| 2Q26 | LPDDR4X +70% to +75%; LPDDR5X +78% to +83% | (forecast, 2026-05-14) [26]; (forecast, 2026-05-14) [26] |
| 3Q26 | Mobile DRAM +8% to +13% (TrendForce); smartphone memory +5% to +10% (Counterpoint, actual) | (forecast, 2026-08-03) [115]; (actual, 2026-10-30) [116] |
| 4Q26 | Mobile +0% to +5% (TrendForce via Goldman); +3% to +4% (Goldman); +0% to +5% (CFM); +5% (Counterpoint) | (forecast, 2026-10-01) [27]; (forecast, 2026-10-01) [27]; (forecast, 2026-10-10) [117]; (forecast, 2026-10-30) [116] |
| 1Q27 | LPDDR5X +13% to +18%, LPDDR4X +5% to +10% (TrendForce via Goldman); LPDDR5X more than +20% (CFM) | (forecast, 2026-10-01) [27]; (forecast, 2026-10-01) [27]; (forecast, 2026-10-10) [117] |

- Mobile DRAM revenue was at least 29.6 bn USD in 2Q26 (derived lower bound: 10 × 1.645 × 1.80) [111, 118, 119].
- 4Q26 looks like a pause. Smartphone LPDRAM prices stay flat to slightly up in 4Q26 (forecast, 2026-10-30) [120], and then the 1Q27 forecasts rise again. Notebook LPDRAM rises more than phone LPDRAM in 4Q26 (forecast, 2026-10-30) [120].

#### Demand drivers (units × content)

- **Phones.** IDC counted 1,260.3 million phones in 2025 (actual, 2026-01-13) [121]. For 2026, IDC forecasts −16.7% (Section 1.1), Counterpoint 1,080 million (forecast, 2026-06-01) [109] and TrendForce production 1,070 million (forecast, 2026-09-08) [102]. Content is 8.5 GB in 2026 (forecast, 2026-05-14) [26]. In high-end phones, 12 GB becomes the main configuration and 16 GB use declines (estimate, 2026-05-14) [26]. IDC gives an example: a 12 GB + 256 GB phone may now ship as 8 GB + 128 GB (estimate, 2026-02-26) [122].
- **Server.** Vera Rubin NVL72 holds up to 54 TB LPDDR5X per rack (actual) [123], against 17 TB for GB200 and GB300 NVL72 (actual) [124, 125].
- **PC.** LPCAMM was forecast at 15% to 20% of notebook DRAM bits in 2026, before the price spike (forecast, 2025-03-26) [126].
- **Auto.** The average car holds about 16 GB of DRAM (estimate, 2026-03-18) [107].

#### 2027 outlook

- Model: 165.3 bn Gb, 80% interval 137.0 to 197.7 bn Gb, YoY +21.9%. Parts: phone + tablet 103.1 (+9.1%), server 40.35 (+74.0%), PC 9.458, auto 12.15 bn Gb. Server LPDDR gap: −26.90 bn Gb.

| Source | Date | 2027 view | Model against the view |
|---|---|---|---|
| Yole | 2025-11-13 | Mobile demand 12 EB [101] | Phone + tablet growth matches Yole's +9.1% (derived: 12 / 11); the model level (12.9 EB) is above |
| IDC; Counterpoint; Samsung | 2026-05 to 2026-10 | Phone units −1.1% [127]; SoC shipments −3% to −4% [116]; unit volumes decline [18] | Model bits grow more than units, because content rises |
| Meritz × TrendForce fill | 2026-05-22; 2026-06-10 | Nvidia SOCAMM2 need 72.7 bn Gb (derived: 9,084 PB × 8) [103]; about 60% met [20]; supply 43.6 bn Gb (derived: 72.7 × 0.60) | Below: the model need range also uses Edgewater's lower 60–70 bn Gb [128] |
| CFM | 2026-10-10 | Server LPDDR5X demand could double [117] | Below (+74.0%) |
| TrendForce | 2026-08-04 | LPDDR5X supply constrained through 2027 [19] | Consistent: server LPDDR sufficiency is negative |

- **Disagreement.** The size of server LPDDR. IDC (February 2026) expected phone units of +1.9% (forecast, 2026-02-26) [122]; its May view (−1.1%) supersedes it. No source gives 2027 GB per phone [129].

#### Risks

- Server LPDDR can pass phone LPDDR sooner than expected. CFM says this could happen in 2027 [117]. TrendForce says 2028–2030 (forecast, 2026-06-10) [20].
- Phone + tablet takes much of the error in the 2027 total, because the model sets HBM and servers first.

---

### 2.7 DDR4 and legacy

In the model, "DDR4 modules" is an overlay: the DDR4 part of server ECC and client PC. Discrete DDR4, DDR3 and DDR2 chips in consumer and industrial devices sit in the "Other / consumer" bucket. No source sizes them.

#### 2026 production

- Model, DDR4 modules: 11.70 bn Gb, 80% interval 7.067 to 16.32 bn Gb (1.46 EB). Share 3.2%.
- Model, Other / consumer: 11.31 bn Gb [8.723 to 14.14], YoY −4.6%.
- Mirae "other DRAM" (consumer, auto, industrial) is 20.3 bn Gb in 2026, 5.3% of bits (forecast, 2025-12-15) [3]. The model takes auto out of this line.
- DDR4 falls to about 7% of Micron's DRAM output in 2026 (forecast, 2026-05-26) [114].

#### Supply chain and constraints

- **End-of-life dates.** Samsung stopped DDR4 orders in June 2025 (actual, 2025-07-09) [33]. Micron made final mainstream shipments in 1Q26 (actual, 2025-07-09) [33]. SK hynix completes shipments in April 2026 (actual, 2025-07-09) [33]. Samsung delayed part of its exit through a contract with a server customer (actual, 2026) [130].
- **Micron Fab 6.** Fab 6 LPDDR4 and DDR4 supply grows 4× by 2027 (forecast, 2026-05-26) [114]. Micron's total LPDDR4 and DDR4 capacity does not grow (per source summary).
- **CXMT.** CXMT supply pushed DDR4 spot down in early 2025 (per source summary) (actual, 2025-02-05) [131].

#### Prices and contracts

| Item | Value | Source |
|---|---|---|
| Consumer DDR4 contract, 3Q25 | +40% to +45% (Jul 2025); revised to +85% to +90% (Aug 2025) | (forecast, 2025-07-07) [45]; (forecast, 2025-08-11) [132] |
| DDR2 contract, 3Q26 | +35% to +40% | (forecast, 2026-06-22) [30] |
| DDR4 8Gb weekly spot | 31.8× from Feb 2025 to Oct 2026 (derived; end points in Section 4.2) | [34] |
| DDR4 16Gb spot vs DDR5 16Gb spot, 2026-10-30 | DDR4 is 34.6% higher (derived: 82.796 / 61.50 − 1; Section 4.2) | [32] |
| DDR4 16 GB SO-DIMM contract, 2H Sep 2026 | 275.00 USD | (actual, 2026-09-30) [61] |
| DDR4 8Gb chip contract, 2H Sep 2026 | 26.00 USD | (actual, 2026-09-30) [61] |

- Omdia DDR4 RDIMM and UDIMM prices are in Section 4.3. Omdia's DDR4 8Gb component forecast (12.28 USD for 3Q26) conflicts with the TrendForce contract price of 26.00 USD in the table above (forecast, 2026-05) [48]. The basis and the vintage differ.
- In July 2025 an 8 GB PC DDR4 module cost more than DDR5 (per source summary) [132].

#### Demand drivers (units × content)

Long-life uses: industrial, auto, networking and older servers. No source gives units or content for these uses.

#### 2027 outlook

- Model, DDR4 modules: 6.425 bn Gb, 80% interval 3.125 to 11.06 bn Gb, YoY −42.0%.
- Model, Other / consumer: 12.07 bn Gb, YoY +7.4%.
- No source gives a 2027 DDR4 bit forecast, so no published range exists to compare. The model decline agrees in direction with the end-of-life dates. Mirae "other DRAM" is 21.3 bn Gb in 2027 (forecast, 2025-12-15) [3]. Omdia forecasts the DDR4 8Gb component flat at 12.77 USD in 1Q27 and 2Q27 (forecast, 2026-05) [48].

#### Risks

- More CXMT DDR4 supply could lower prices, as it did in early 2025 (per source summary) [131].

---

## 3. Shared constraints

### 3.1 Fab and cleanroom timelines

| Fab | Vendor | Start (date of statement) | kwpm | Status |
|---|---|---|---|---|
| M15X (Cheongju) | SK hynix | Maximum capacity by end-2026 for HBM4 (2026-10-28) [12] | +40 in 2026 (Mirae) [3]; about 50 at full use [76] | Pulled in (2026-07-29) [40] |
| Yongin Phase 1 | SK hynix | Cleanroom opens early 2027 [40]; full-scale operation in 2027 (2026-10-28) [12] | not published | On plan |
| P4 (Pyeongtaek) | Samsung | Operating (2026-10-20) [13] | +55 in 2026 (Mirae) [3] | Operating |
| P5 (Pyeongtaek) | Samsung | Operations in 2028 (2026-10-30, secondary source) [133] | not published | Pulled in by two years [133] |
| ID1 (Idaho) | Micron | Wafer output mid-2027 (2026-09-30) [10] | not published | On track (Micron) |
| Tongluo (Taiwan, ex-PSMC) | Micron | Meaningful shipments mid-2027 (2026-09-30) [10] | Phase 1 above 10% of Micron capacity in 2H27 [134] | On track |
| ID2 (Idaho) | Micron | Wafer output late 2028 [10] | not published | On track (Micron) |
| Singapore HBM | Micron | Ramp in 2027 [77] | not published | Timing only |

- TrendForce: substantial output from new fabs comes only in 2028 (forecast, 2026-07-30) [1]. Suppliers delay ramps to 2H27 (per source summary).
- Samsung: the 2027 capex increase is unlikely to give a meaningful boost to bit production in 2028 (forecast, 2026-10-29) [18].
- The model gives each new fab half of its step in 2027 (A12). Later fabs: Micron ID2 and Hiroshima in late 2028 [10], New York in 2030 [10]. CXMT is in Section 3.6. Each one moves the 2027 total by 4.3 bn Gb or less (Section 1.3).

### 3.2 Wafer capacity and node migration

Mirae wafer capacity (kwpm, forecast, 2025-12-15):

| Vendor | 2026 | 2027 |
|---|---|---|
| Samsung | 665 [3] | 735 [3] |
| SK hynix | 586 [3] | 646 [3] |
| Micron | 349 [3] | 369 [3] |
| CXMT | 298 [3] | 328 [3] |
| Nanya | 65 [3] | 70 [3] |
| Industry | 2,052 [3] | 2,237 [3] |

- Net additions are 184 kwpm in 2026 and 185 kwpm in 2027 (forecast, 2025-12-15) [3]. Capacity grows 7.8% in 2026, net of node-migration losses (forecast, 2025-12-15) [3].
- Mirae gives end-2026 values of 700 kwpm (Samsung) and 605 kwpm (SK hynix) (forecast, 2025-12-15) [3]. The table values are most likely annual averages.
- Most 2026 bit growth comes from node migration. The model backs out a node gain of 14.2% per standard wafer in 2026 (model, `out/checks.csv`).

### 3.3 The HBM wafer trade ratio

- Micron gives a 3:1 trade ratio of wafer area per bit for HBM against DDR5 (actual, 2025-12-17) [36]. The ratio rises with future HBM generations (forecast, 2026-09-30) [77]. Applied Materials gives 3× (estimate, 2026-03-17) [74]. Goldman Sachs gives 3× to 4× (estimate, 2026-06-01) [92]. The model draws 2.52 to 4.0 for 2026 and a 0% to 33% rise for 2027. Its 2027 median is 3.67 (model, `out/checks.csv`).
- **How HBM diverts wafers.** At end-2026, HBM and TSV capacity is about 480 kwpm across all vendors (derived: 150 + 200 + 100 + CXMT 30) [75]. At 3:1, these wafers give the bits of only 160 standard wafers. The output lost to standard DRAM is about 320 kwpm-equivalent (derived: 480 × (1 − 1/3)) [36]. In 2027, 30% of top-3 capacity is about 525 kwpm (derived) [5].
- **Result.** New fabs add little before mid-2027, so 2027 HBM growth takes wafers from standard DRAM.

### 3.4 CoWoS and bonders

- TSMC CoWoS: about 75 kwpm at end-2025 (forecast, 2025-07-31) [81], 120–140 kwpm in 2026 (forecast, 2026-06-15) [135], 190–200 kwpm at end-2027 (forecast, 2026-09-09) [136]. OSATs add 50–60 kwpm in 2026 (forecast, 2026-06-15) [135]. The CoWoS gap falls to about 10% by end-2026 (forecast, 2026-06-15) [135].
- HBM4 base dies: SK hynix uses TSMC (actual, 2024-04-19) [137]. Samsung uses its own 4 nm foundry (actual, 2026-02) [138]. Micron uses TSMC for HBM4E (actual, 2025-09-23) [139].
- Bonders: SK hynix had about 50 TC bonder sets for HBM4 in December 2025 (estimate, 2025-12-12) [140]. Hybrid bonding is not in volume HBM4 (estimate, 2025-02-07) [141].
- The CoWoS gap narrows while the HBM wafer share rises. This document infers that memory wafers, not packaging, are the tighter limit for 2027. AMD names wafers, HBM, packaging and substrates as tight (actual, 2026-09-08) [86].

### 3.5 Equipment (WFE, EUV) and capex

- WFE: mid-150s bn USD in 2026 and more than 200 bn USD in 2027 (Lam, all segments) (forecast, 2026-10-21) [21]. Memory is 46% of Lam systems revenue in the September 2026 quarter (actual, 2026-10-21) [21].
- EUV: Samsung secured about 20 EUV systems (estimate, 2026-04-15) [142]. SK hynix ordered about 24 over two years (estimate, 2026-04-15) [142].

| Company | 2026 capex | Source |
|---|---|---|
| Samsung (total) | 84.4 tn KRW; initial plan 60–70 tn KRW | (forecast, 2026-10-29) [18]; (forecast, 2026-10-30) [133] |
| SK hynix | high 40s tn KRW; 2027 "to increase significantly" | (forecast, 2026-07-29) [40]; (forecast, 2026-10-27) [11] |
| Micron | 27.37 bn USD net (FY2026); about 25 bn USD in 1H FY2027 | (actual, 2026-09-30) [143]; (forecast, 2026-09-30) [10] |
| Nanya | up to 50 bn NTD (13.4 bn NTD in 2025) | (forecast, 2026-01-19) [144]; (actual, 2026-01-19) [144] |
| Industry (Nov–Dec 2025 vintage) | 61.3 bn USD (TrendForce); 66.1 bn USD (Mirae) | (forecast, 2025-11-13) [145]; (forecast, 2025-12-15) [3] |

- Vendor guidance in 2026 runs above the 2025 industry forecasts.

### 3.6 China, CXMT and export controls

- CXMT revenue share: 7.6% in 1Q26 (actual, 2026-09-24) [146] and 9.5% in 2Q26 (Section 2.0).
- CXMT capacity is 320 kwpm now and 420 kwpm in 2027 (estimate, 2026-09-24) [146]. Mirae had 298 kwpm (2026) and 328 kwpm (2027) (Section 3.2). CXMT bits (Mirae): 29.5 bn Gb in 2026 and 36.0 bn Gb in 2027 (Section 2.0).
- CXMT mass-produces LPDDR5X at 8,533 and 9,600 Mbps (actual, 2025-10-29) [147]. Its HBM3E yield is 20% to 30% (estimate, 2026-10-28) [148].
- The US added CXMT to the Section 1260H list in January 2025 (actual, 2025-01-07) [149]. The US added HBM export controls and 140 Entity List entries in December 2024 (actual, 2024-12-02) [150].
- Samsung and SK hynix China fabs: the US granted a yearly approval for tool shipments in December 2025 (actual, 2026-10-15) [151]. The 2027 approval is not yet issued, and no capacity add is allowed (per source summary).

### 3.7 Tariffs

- The US Section 232 tariff of 25% ad valorem started on 2026-01-15 (actual, 2026-01-14) [152]. It covers a narrow set of advanced computing chips, the proclamation text does not name memory, and a broader phase 2 is possible (per source summary).
- US reciprocal tariffs: Japan, South Korea and the EU got 15% (actual, 2025-08-01) [153]. Taiwan got 20%, and ICs, servers and PC parts were largely excluded in 2025 (per source summary).
- US tariff increases led most brands to pull shipments forward into 1Q25 (estimate, 2025-03-25) [59].

---

## 4. Market mechanics

### 4.1 Contract prices by quarter

Conventional DRAM contract price change, quarter on quarter (TrendForce). The table uses the latest vintage for each quarter. Segment prices are in the category sections: server (2.1), PC (2.3), LPDDR (2.6), DDR4 and legacy (2.7).

| Quarter | Conventional DRAM | Latest kind and date | Including HBM |
|---|---|---|---|
| 1Q25 | −13% to −8% | (forecast, 2024-12-30) [154] | −5% to 0% [154] |
| 2Q25 | −5% to 0% | (forecast, 2025-03-25) [59] | +3% to +8% [59] |
| 3Q25 | +10% to +15% | (forecast, 2025-07-07) [45] | +15% to +20% [45] |
| 4Q25 | +45% to +50% | (actual, 2026-02-26) [155] | +50% to +55% [155] |
| 1Q26 | +93% to +98% | (Section 1.1) | +80% to +85% [155] |
| 2Q26 | +58% to +63% | (Section 1.1) | – |
| 3Q26 | +13% to +18% | (Section 1.1) | – |
| 4Q26 | +10% to +15% | (Section 1.1) | – |

- **Forecast revisions.** TrendForce raised its 4Q25 call from +8% to +13% [156] to +18% to +23% [51] and then +45% to +50% [157]. Its 1Q26 call went from +55% to +60% [46] to +90% to +95% [23].
- **Conflict for 4Q25.** TrendForce also gives +53% to +58% for 4Q25 in a January 2026 release (actual, 2026-01-22) [158]. Its basis is not stated. The February 2026 value (+45% to +50%) is conventional only.
- **Cumulative.** From 2Q25 to 4Q26 the index rises about 6.77× (derived: product of range midpoints; mixes actual and forecast) [9].
- **Blended ASP.** Samsung Securities forecast blended DRAM ASP of +43% in 1Q26 and +27% in 2Q26 (forecast, 2026-01-28) [35]. These are below contract quotes because they include LTA and HBM effects.
- **Vendor ASP.** Samsung DRAM ASP rose mid-40s % in 2Q26 (actual, 2026-07-30) [159] and about 20% in 3Q26 (actual, 2026-10-29) [160]. Micron DRAM prices rose high teens % in its June–August 2026 quarter (actual, 2026-09-30) [10].

### 4.2 Spot prices

| Item | Date | Price | Source |
|---|---|---|---|
| DDR4 8Gb 1Gx8 3200, weekly average | 2025-02-05 | 1.458 USD | (actual, 2025-02-05) [131] |
| DDR4 8Gb, weekly average | 2025-12-30 | 23.746 USD | (actual, 2025-12-31) [161] |
| DDR4 8Gb, weekly average | 2026-10-20 | 46.357 USD | (actual, 2026-10-21) [34] |
| DDR5 16Gb 2Gx8 5600 (SK hynix) | 2025-03-19 | 4.95 USD | (actual, 2025-03-19) [162] |
| DDR5 16Gb 2Gx8, session average | 2026-10-30 | 61.50 USD | (actual, 2026-10-30) [32] |
| DDR4 16Gb 2Gx8 3200, session average | 2026-10-30 | 82.796 USD | (actual, 2026-10-30) [32] |
| DDR5 RDIMM 32 GB module, weekly | 2026-10-26 | 2,165.00 USD (67.7 USD per GB) | (actual, 2026-10-26) [49] |
| DDR5 UDIMM 16 GB module, weekly | 2026-10-26 | 241.667 USD (15.1 USD per GB) | (actual, 2026-10-26) [49] |


### 4.3 Module contract prices (Omdia via IBK)

USD per module. 3Q25 and 4Q25 come from the January 2026 table. 1Q26 onward comes from the May 2026 table. 2Q26 onward are forecasts.

| Module | 3Q25 | 4Q25 | 1Q26 | 2Q26 | 3Q26 | 4Q26 | 1Q27 | 2Q27 |
|---|---|---|---|---|---|---|---|---|
| 64 GB DDR5 RDIMM | 265 [60] | 451 [60] | 766 [48] | 1,035 [48] | 1,086 [48] | 1,119 [48] | 1,130 [48] | 1,130 [48] |
| 128 GB DDR5 RDIMM | – | – | 2,146 [48] | 2,897 [48] | 3,042 [48] | 3,133 [48] | 3,165 [48] | 3,165 [48] |
| 32 GB DDR4 RDIMM | 131 [60] | 222 [60] | 399 [48] | 531 [48] | 558 [48] | 574 [48] | 580 [48] | 580 [48] |
| 16 GB DDR5 UDIMM | 45.2 [60] | 72.2 [60] | 122.8 [48] | 159.7 [48] | 170.8 [48] | 176.0 [48] | 177.7 [48] | 177.7 [48] |
| 16 GB DDR4 UDIMM | 48.1 [60] | 72.2 [60] | 122.7 [48] | 159.5 [48] | 170.6 [48] | 175.8 [48] | 177.5 [48] | 177.5 [48] |

- The January table forecast 699 USD for the 64 GB RDIMM in 1Q26 (forecast, 2026-01) [60]. The May table shows 766 USD.
- Omdia shows prices flat from 1Q27 to 2Q27. TrendForce expects server prices to rise each quarter through 2H27 (Section 2.1). The two views disagree on 2027.

### 4.4 Inventory

- Supplier inventories were almost depleted in 3Q25–4Q25 (estimate, 2025-11-26) [157] and at historic lows in 2Q26 (estimate, 2026-09-07) [38]. TrendForce published no weeks-of-inventory figure in text.
- Micron: 129 days of inventory at the end of FQ4 2026 (DRAM plus NAND) (actual, 2026-09-30) [163], 10.4 bn USD (actual, 2026-09-30) [163]. The rise includes build-ahead for end-of-life nodes (per source summary).

### 4.5 Long-term agreements and prepayments

| Supplier | Status | Source |
|---|---|---|
| Micron (Sep 2026) | 26 SCAs; about 150 bn USD remaining performance obligations; 32 bn USD customer commitments; 12.7 bn USD cash deposits | (actual, 2026-09-30) [163]; (actual, 2026-09-30) [163]; (actual, 2026-09-30) [163]; (actual, 2026-09-30) [163] |
| Micron SCA terms | Five years (three for auto); price cap tied to Apr–Jun 2026 prices (per source summary) | (actual, 2026-06-25) [164] |
| SK hynix | 14 LTA customers | (actual, 2026-10-28) [12] |
| SK hynix (Microsoft, Google) | Advance payments of 10% to 30% of contract value | (estimate, 2026-06-25) [164] |
| Samsung | 10 LTAs signed, 10 in talks; target 60% to 70% of capacity by 2030 | (actual, 2026-10-29) [160]; (forecast, 2026-10-29) [160] |
| Samsung | Upfront payments for about 25% of contracted volume | (estimate, 2026-07-30) [50] |
| Industry | Nearly half of global DRAM capacity under LTAs by 2027 | (forecast, 2026-07-30) [50] |

- The 2027 coverage of each supplier (SK hynix, Micron, Samsung) is in Section 1.1.
- Prepayments raise CSP capex. TrendForce names advance payments as one reason for its 2027 CSP capex revision (per source summary) [52].

### 4.6 Supplier revenue and margins

| Item | 3Q25 | 4Q25 | 1Q26 | 2Q26 | 3Q26 |
|---|---|---|---|---|---|
| DRAM industry revenue, bn USD (TrendForce, includes HBM) | 41.4 [157] | 53.58 [155] | 97 [6] | 154.73 [38] | – |
| SK hynix operating margin (company) | – | 58% [165] | 72% [165] | 76% [166] | 80% [12] |
| Samsung DS division operating margin | – | – | – | about 70% (per source summary) [159] | 72.4% [160] |

- Micron FQ4 2026: DRAM revenue 39.8 bn USD (actual, 2026-09-30) [163]; GAAP gross margin 86.8% and GAAP operating margin 80.7% (actual, 2026-09-30) [143]. FQ1 2027 revenue guide: 61.5 ± 1.5 bn USD (forecast, 2026-09-30) [143].

### 4.7 OEM responses

| Segment | Response | Source |
|---|---|---|
| PCs | Price-hike notices of 5% to 15% after CES 2026 | (actual, 2026-02-20) [58] |
| PCs | OEM price hikes of 15% to 20% | (estimate, 2026-01-05) [65] |
| Phones | Memory is 30% to 40% of BOM (1Q26) | (estimate, 2026-02-11) [167] |
| Consoles | Xbox price rises to 499 and 749 USD | (actual, 2026-06-26) [168] |
| Apple | MacBook Air 512 GB from 1,099 to 1,299 USD | (actual, 2026-06-26) [168] |
| Long-term view | Lenovo: high memory prices are a "new normal" into 2030 | (forecast, 2026-06-26) [169] |

---

## 5. 2027: consensus, disagreement, signposts

### 5.1 Published 2027 views for total DRAM, and the model

![Growth by category, 2026 and 2027](../out/charts/02_growth_by_category.png)

| Source | Date | 2027 view | Model (+22.6%) against the view |
|---|---|---|---|
| SK hynix | 2026-10-27 | Achievable demand +mid-20s % (read as 24–26%) [11] | Below |
| Samsung | 2026-10-29 | No number; tight supply into 2028 [18] | No number to compare |
| Micron | 2026-09-30 | Industry bit shipments +low 20s % (read as 20–23%) [10] | Inside |
| TrendForce | 2026-07-28 | Supply bits +24% (paywalled; heading only) [170] | Slightly below |
| Mirae | 2025-12-15 | Demand +21.7% [3]; production +17.9% [3] | Above both |
| Yole | 2025-11-13 | Demand 51 EB [37] | Above (55.8 EB) |

- Model: 446.4 bn Gb, 80% interval 402.0 to 496.0 bn Gb (55.8 EB, 50.3 to 62.0 EB). Every published growth figure above sits inside the model's 80% growth interval of 12.1% to 35.0% (model, `out/combination_2027.csv`).

### 5.2 Consensus

- 2027 is tighter than 2026. Micron expects conditions "much tighter" in 2027 and 2028 (forecast, 2026-09-30) [163]. TrendForce expects the gap to widen (per source summary) [1].
- New cleanroom space adds substantial output only in 2028 (Section 3.1).
- Contract prices stay broadly high in 2027 (forecast, 2026-08-25) [2].
- HBM bits grow 50% or more, and HBM stays short (Section 2.4).

### 5.3 Disagreement

| Topic | View A | View B |
|---|---|---|
| Duration of shortage | Samsung: tight into 2028 [18] | SK hynix: through 2030 [11]; Lenovo: into 2030 [169] |
| Memory price rise | TrendForce: LTA ceilings limit further increases [2] | Xbox: prices double again by fall 2027 [168] |
| Demand risk | Suppliers: demand above supply [11] | TrendForce and Counterpoint: phone and notebook units fall again [66, 116] |
| Oversupply | Omdia (Dec 2025): oversupply risk by 2028 [171] | SK hynix (Oct 2026): short through 2030 [11] |

### 5.4 Signposts for 4Q26 and 1Q27

| Signpost | What to look for | Why it matters |
|---|---|---|
| 4Q26 bit shipments | Samsung mid to high teens % QoQ; SK hynix mid-20s % QoQ (Section 2.0) | Tests the model's 4Q26 value |
| 1Q27 contract prices | TrendForce call in early January; LPDDR5X forecasts (Section 2.6) | Tests whether 4Q26 is only a pause |
| HBM 2027 contracts | Micron reset at the start of 2027; blended ASP +121% (Section 2.4) | Shows if HBM pricing catches up with DDR5 |
| Rubin Ultra HBM configuration | 12-Hi HBM4E against lower configurations [19] | Moves HBM demand and the HBM gap |
| HBM trade ratio | HBM4 and HBM4E yields and stack heights | Largest driver of the model's HBM gap (Section 1.3) |
| Yongin Phase 1 cleanroom | Opening in early 2027 (Section 3.1) | First new SK hynix space after M15X |
| Micron ID1 and Tongluo | Mid-2027 output (Section 3.1) | First new Micron bits |
| PC and phone units | IDC 4Q26 PCs about −20% (per source summary) [15]; Counterpoint 2027 SoC −3% to −4% (Section 2.6) | Shows how much consumer demand falls |
| CXMT | HBM3E production; capacity toward 420 kwpm (Section 3.6) | Main source of new supply outside the big three |

---

## 6. Method, data gaps and definition conflicts

### 6.1 Method summary

`model/METHOD.md` gives the full method and all 24 assumptions (A1–A24). The model splits DRAM bits into six buckets that add to the total (Section 6.2).

**2026.** The model starts from Mirae's 2025 production of 293.1 bn Gb, with a 3% error. It draws 2026 growth from 20%, 25% and 27%, the range of views published since June 2026. It then splits the total. It grows Mirae's 2025 lines with the latest unit and content forecasts, and it scales the lines to the total. HBM and server LPDDR come from pooled estimates.

**2027 total.** The model mixes three forecasts with equal weights: a time-series model, a supply model and published guidance (Section 1.3). The supply model uses wafer capacity, the HBM wafer share, the HBM trade ratio and a node gain per wafer. A rolling-origin backtest chose the time-series model. Six models forecast one year ahead for 2016–2025. The naive model (next year equals this year) was best, with a level error (MAPE) of 6.3%. ARIMA gave 8.9%, AR(1) 9.3%, and drift models 9.9% to 14.9%. Past one-year guidance misses had an RMSE of 8.2% in log growth. The model adds that error to the guidance forecast.

**2027 split.** The model sets the lines in priority order, because LTAs and prepayments put HBM and servers first. HBM comes first, from the supply model's HBM share. Server LPDDR comes next, at 60% of Nvidia's need. Server ECC follows, at the TrendForce RDIMM guide of +15% to +20%, capped by Mirae's +22.7%. An additive log-ratio model splits the rest across phone + tablet, PC LPDDR, client PC, GDDR, other / consumer and auto.

**Uncertainty.** A Monte Carlo run takes 50,000 seeded draws of every input range. All intervals in this document come from these draws.

**Weakest assumptions.** Five assumptions have the least support:

1. Rubin Ultra 2027 units (A18). No source gives them. They move only HBM demand.
2. The PC DDR5 share (A20). No source gives it after 2H24. It moves only the DDR5 overlay.
3. GDDR as a residual. No source gives GDDR bits.
4. New-fab capacity. No company gives kwpm for Yongin, ID1, Tongluo or P5.
5. The placement f of server LPDDR in Mirae's lines (A4). No source gives it. The model draws f from 0 to 1 (Section 6.2).

### 6.2 Category boundaries

These are the model's categories (`model/METHOD.md`, section 2). The six buckets add to the total.

| Bucket | What it holds | Built from |
|---|---|---|
| Server ECC | RDIMM and MRDIMM, DDR5 and DDR4. No HBM. No server LPDDR. | Mirae "server" line, minus the share of server LPDDR that sits in it |
| Client PC | Non-LP DDR5/DDR4 UDIMM and SODIMM | Mirae "PC" line × (1 − LPDDR share of PC) |
| LPDDR | Phone + tablet + PC LPDDR + server LPDDR (SOCAMM, Grace, Vera) + auto | Mirae "mobile" line (less any server LPDDR in it) + PC LPDDR + server LPDDR + auto |
| HBM | HBM stacks | Pooled HBM bit estimates for 2026; wafer model for 2027 |
| GDDR | Graphics memory without HBM | Mirae "graphics" minus HBM in 2025; growth rates after that |
| Other / consumer | TVs, networking, industrial, consoles and the rest | Mirae "other" line minus auto |

Two overlays are not added to the total:

- **DDR5** = server ECC × server DDR5 share + client PC × PC DDR5 share.
- **DDR4 modules** = the DDR4 part of server ECC and client PC. It leaves out discrete DDR4 chips in consumer and industrial devices, because no source sizes them.

**How the model avoids counting server LPDDR twice.** TrendForce counts Grace LPDDR in "mobile". Yole counts it in "data center". No source says where Mirae puts it. So the model draws a fraction f from U(0, 1):

1. A share f of server LPDDR sits in Mirae's server line, and 1 − f sits in its mobile line.
2. The model takes each share out of its line.
3. The model adds server LPDDR back once, as its own line.

The same split applies to demand.

### 6.3 Data gaps

- Only Mirae (December 2025), KGI (November 2025) and Yole (November 2025) give 2026 bits by application. All three predate the 2026 price spike.
- No DDR5-only, GDDR-only, DDR4-only or LPDDR-total bit series exists.
- No public Micron HBM bits. Micron stopped giving HBM revenue in 2026.
- No 2026 CXL memory volume. MRDIMM data is limited to Rambus and Montage.
- No 2027 GB per phone and no tablet DRAM content.
- No TrendForce weeks-of-inventory figure in text. Most TrendForce segment price figures for 2Q26 onward are in chart images.
- Several sources are paywalled or summary-only. Section 7 marks each one.

### 6.4 Definition conflicts

| Conflict | Values | Effect |
|---|---|---|
| TrendForce "mobile DRAM" includes Grace LPDDR5X | TrendForce counts Nvidia GB200-related LPDDR5X in mobile DRAM revenue (per source summary) [172]; Yole puts data center apart [37] | Do not add TrendForce mobile bits to server LPDDR. The model uses the f rule (Section 6.2). |
| Mirae graphics = HBM + GDDR | 46.1 bn Gb in 2026 (Section 2.5) | Do not add HBM to Mirae graphics |
| Server excludes HBM (Mirae) | Mirae 41.0% excludes HBM; TrendForce's 51% includes HBM (Section 1.1) | Shares are not comparable |
| Server unit counts: about 14 million vs about 20 million | TrendForce 14.49 million (2025) [173]; Mirae 20 million (2025) [3] | Do not mix unit bases with content figures |
| Demand vs supply shares | Mirae and KGI give demand; TrendForce gives bit output [4, 174] | KGI 47% vs Mirae 41.0% for 2026 server share (Section 2.1) |
| Phone content | Mirae 11.2 GB (Section 2.6) vs TrendForce 8.5 GB [26]; Counterpoint 8.4 GB is a December value [175] | Phone bits range from 9.1 to 15.9 EB in 2026 |
| Mirae production vs shipments by vendor | Production: Samsung 122.0, SK hynix 105.2 bn Gb in 2026 (Section 2.0). Quarterly shipment forecasts add to 136.0 and 125.0 bn Gb (derived: sum of 1Q26–4Q26) [3] | Different pages of the same report |
| PC units | IDC 284.7 million (2025) (Section 2.3) vs Mirae 244 million (2025) [3] | Different definitions |

---

## 7. References

Model outputs: `model/forecast.py` and `model/METHOD.md` (run of 2026-10-30, 50,000 draws, seed 20261030); `out/forecast_by_category.csv`, `out/combination_2027.csv`, `out/sensitivity.csv`, `out/backtest.csv`, `out/checks.csv`, `out/quarterly_2026.csv`; charts in `out/charts/`.

Each source reference gives publisher, title, publish date and URL. A **Note** marks sources seen only in a search summary, paywalled sources seen only in summary or title, and headline-only sources.

1. TrendForce. "Diverging Memory Market Outlook in 2027 as DRAM Supply Remains Tight While NAND Flash Supply Conditions Ease". 2026-07-30. <https://www.trendforce.com/presscenter/news/20260730-13158.html>
2. TrendForce. "Memory Prices Soar; DRAM and NAND Flash to Account for 68% of Major CSP CapEx in 2027". 2026-08-25. <https://www.trendforce.com/presscenter/news/20260825-13198.html>
3. Mirae Asset Securities. "[2026 Outlook Report] Semiconductors: Robust earnings cycle ahead". 2025-12-15. <https://securities.miraeasset.com/bbs/download/2141014.pdf?attachmentId=2141014>
4. KGI Securities. "Memory sector: Surge in general server procurement fueling a memory supercycle". 2025-11-17. <https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/memory-sector-17112025e.pdf>
5. TrendForce. "Tight DRAM Supply Gives Suppliers Greater Pricing Power in HBM, with HBM Contract Prices Expected to Surge Multiples Higher in 2027, Says TrendForce". 2026-06-02. <https://www.trendforce.com/presscenter/news/20260602-13074.html>
6. TrendForce. "Rapid Contract Price Surge Drives 1Q26 DRAM Industry Up 81% QoQ". 2026-06-01. <https://www.trendforce.com/presscenter/news/20260601-13070.html>
7. TrendForce. "AI Server Demand to Drive Memory Contract Price Increases in 2Q26 as CSPs Secure Supply via Long-Term Agreements". 2026-03-31. <https://www.trendforce.com/presscenter/news/20260331-12995.html>
8. TrendForce. "AI Server Demand Continues to Support Memory Prices in 3Q26, but Gains Moderate as Consumer Demand Weakens and High Base Effects Take Hold". 2026-07-03. <https://www.trendforce.com/presscenter/news/20260703-13134.html>
9. TrendForce. "AI Server Demand Sustains Memory Contract Price Increases in 4Q26, While Consumer-Side Pressure Persists". 2026-09-30. <https://www.trendforce.com/presscenter/news/20260930-13258.html>
10. Micron. "Micron FQ4 2026 earnings call transcript". 2026-09-30. <https://stockanalysis.com/stocks/mu/transcripts/699706-q4-2026/>
11. SK hynix. "SK hynix Q3 2026 Earnings Call Transcript (Motley Fool)". 2026-10-27. <https://www.fool.com/earnings/call-transcripts/2026/10/28/sk-hynix-skhy-q3-2026-earnings-call-transcript/>
12. SK hynix. "SK hynix Announces 3Q26 Financial Results". 2026-10-28. <https://news.skhynix.com/en/q3-2026-business-results/>
13. EconoTimes (citing KB Securities). "Samsung Builds P5 Chip Plant Amid Forecast of Tight Memory Supply". 2026-10-20. <https://econotimes.com/Samsung-Builds-P5-Chip-Plant-Amid-Forecast-of-Tight-Memory-Supply-1758256>
14. TrendForce. "Long-Term Agreements Cap Price Increases; Server DRAM Contract Prices Expected to Rise 13-18% QoQ in 3Q26". 2026-07-09. <https://www.trendforce.com/presscenter/news/20260709-13140.html>
15. IDC. "PC Market Enters Volatile Territory as Memory Shortage Persists Through 2027". 2026-06-02. <https://www.idc.com/resource-center/blog/pc-market-enters-volatile-territory-as-memory-shortage-persists-through-2027/>
16. IDC. "Smartphone Shipments Set for Record 16.7% Drop in 2026 as the Memory Crisis Hits Full Force". 2026-08-26. <https://www.idc.com/resource-center/blog/smartphone-shipments-set-for-record-16-7-drop-in-2026-as-the-memory-crisis-hits-full-force/>
17. TrendForce. "Memory Price Surge to Persist in 1Q26; Smartphone and Notebook Brands Begin Raising Prices and Downgrading Specs". 2025-12-11. <https://www.trendforce.com/presscenter/news/20251211-12831.html>
18. Samsung Electronics. "Samsung Electronics Q3 2026 Earnings Call Transcript (StockAnalysis)". 2026-10-29. <https://stockanalysis.com/quote/krx/005930/transcripts/718820-q3-2026/>
19. TrendForce. "DRAM Supply to Remain Tight in 2027, Prompting NVIDIA to Lower HBM Configurations for Rubin Ultra, Says TrendForce". 2026-08-04. <https://www.trendforce.com/presscenter/news/20260804-13166.html>
20. TrendForce. "NVIDIA Cuts Vera CPU Memory Configuration, Highlighting Persistent LPDRAM Supply Constraints". 2026-06-10. <https://www.trendforce.com/presscenter/news/20260610-13090.html>
21. Lam Research. "September Quarter 2026 (Q1 FY2027) earnings slides". 2026-10-21. <https://filecache.investorroom.com/mr5ir_lamresearch2/1519/Q1_2027-slides-full_final.pdf>
22. TrendForce. "Server CPU Shipments Projected to Grow Over 40% YoY in 2027". 2026-10-22. <https://www.trendforce.com/presscenter/news/20261022-13279.html>
23. TrendForce. "Memory Price Outlook for 1Q26 Sharply Upgraded". 2026-02-02. <https://www.trendforce.com/presscenter/news/20260202-12911.html>
24. Samsung (Reuters, via TrendForce News). "Samsung Sees HBM Taking Nearly 30% of Industry DRAM Capacity in 2027, Up From 20% Currently". 2026-09-29. <https://www.trendforce.com/news/2026/09/29/news-samsung-sees-hbm-taking-nearly-30-of-industry-dram-capacity-in-2027-up-from-20-currently>
25. SamMobile (citing Korean press). "Samsung will supply half of SOCAMM2 DRAM chips needed by Nvidia". 2025-12-03. <https://www.sammobile.com/news/samsung-supply-half-socamm2-dram-chips-nvidia/>
26. TrendForce. "Mobile DRAM Contract Prices Continue Rising in 2Q26". 2026-05-14. <https://www.trendforce.com/presscenter/news/20260514-13044.html>
27. TrendForce (cited by Goldman Sachs, via Tiger Brokers). "Memory price rally far from over: Goldman says Q4 ASP forecasts beat expectations". 2026-10-01. <https://www.itiger.com/news/1111393487?lang=en_US&region=SGP>
28. Seoul Economic Daily (industry estimates). "HBM Prices to More Than Double Next Year as Shortage Persists". 2026-10-01. <https://en.sedaily.com/finance/2026/10/01/hbm-prices-to-more-than-double-next-year-as-shortage>
29. TechSpot (via TechTimes). "NVIDIA RTX 50 GPU Shortage: Supply Cut 20%, Prices Climbing, No Desktop Refresh Confirmed". 2026-06-21. <https://www.techtimes.com/articles/318772/20260621/nvidia-rtx-50-gpu-shortage-supply-cut-20-prices-climbing-no-desktop-refresh-confirmed.htm>
30. TrendForce. "Consumer DRAM Shortages Extend to DDR2 Products with Contract Prices Expected to Continue Rising in 3Q26". 2026-06-22. <https://www.trendforce.com/presscenter/news/20260622-13112.html>
31. TrendForce News (citing Chosun Biz). "SK hynix 1c DRAM Reportedly to Overtake 1b as Main Process in 1Q27 as It Prepares for HBM4E". 2026-09-07. <https://www.trendforce.com/news/2026/09/07/news-sk-hynix-1c-dram-reportedly-to-overtake-1b-as-main-process-in-1q27-as-it-prepares-for-hbm4e/>
32. TrendForce. "DRAM Spot Price (DRAMeXchange price page)". 2026-10-30. <https://www.trendforce.com/price/dram/dram_spot>
33. TrendForce (news, citing Commercial Times). "DDR4 Exit Timeline Unfolds for Top Memory Makers". 2025-07-09. <https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron/>
34. TrendForce. "Memory Spot Price Update: DDR5 Supply Tight, DDR4 Trading Subdued Despite 0.84% Gain in Mainstream Prices". 2026-10-21. <https://www.trendforce.com/news/2026/10/21/insights-memory-spot-price-update-ddr5-supply-tight-ddr4-trading-subdued-despite-0-84-gain-in-mainstream-prices>
35. Samsung Securities. "Tech (OVERWEIGHT): Inflection points in memory narrative". 2026-01-28. <https://www.bondweb.co.kr/Data/20261/28/menu01/2026012820.pdf>
36. Micron. "Micron FQ1 2026 earnings call transcript (Motley Fool)". 2025-12-17. <https://www.fool.com/earnings/call-transcripts/2025/12/17/micron-mu-q1-2026-earnings-call-transcript/>
37. Yole Group (via Comet Holding CMD 2025). "Comet Capital Markets Day 2025, slide 22 Memory Market Outlook". 2025-11-13. <https://comet.tech/getmedia/4363db0d-e447-4ea1-bfef-dec81a68884d/Comet-CMD-2025_presentation_final.pdf>
38. TrendForce. "DRAM Industry Revenue Rises 59.5% QoQ in 2Q26". 2026-09-07. <https://www.trendforce.com/presscenter/news/20260907-13219.html> **Note: page fetched; the CXMT 9.5% value was seen only in a search summary.**
39. Samsung Electronics (via earningsapi.io transcript, search summary). "Samsung Electronics Q2 2026 Earnings Call Transcript". 2026-07-30. <https://earningsapi.io/transcripts/samsung-electronics-co-ltd_a005930_earnings_call_transcript_2026-07-30> **Note: seen only in a search summary; page not fetched.**
40. SK hynix. "SK hynix Q2 2026 Earnings Call Transcript (StockAnalysis)". 2026-07-29. <https://stockanalysis.com/quote/krx/000660/transcripts/653208-q2-2026/>
41. TrendForce. "Bit Shipment Share of DDR5 Has Climbed to Around 90%, Boosting 1Q25 Server DRAM Revenue by 1.4% QoQ to US$10.688 Billion". 2025-05-28. <https://www.trendforce.com/research/download/RP250528SS> **Note: paywalled; seen in summary or title only.**
42. TrendForce. "Memory Industry Revenue Expected to Reach Record High in 2025". 2024-07-22. <https://www.trendforce.com/presscenter/news/20240722-12228.html>
43. TrendForce. "Extended Component Lead Times Weigh on General Server Growth; 2026 Server Shipments Forecast to Grow 13% YoY". 2026-04-15. <https://www.trendforce.com/presscenter/news/20260415-13013.html>
44. Rambus (earnings call). "Rambus Q3 2026 earnings call transcript". 2026-10-26. <https://stockanalysis.com/stocks/rmbs/transcripts/716236-q3-2026/>
45. TrendForce. "Transition between DRAM Generations Drives Diverging 3Q25 Price Trends; Consumer DDR4 Prices Expected to Surge Over 40%". 2025-07-07. <https://www.trendforce.com/presscenter/news/20250707-12633.html>
46. TrendForce. "Memory Makers Prioritize Server Applications, Driving Across-the-Board Price Increases in 1Q26". 2026-01-05. <https://www.trendforce.com/presscenter/news/20260105-12860.html>
47. Micron (earnings call). "Micron FQ3 2026 earnings call transcript". 2026-06-24. <https://stockanalysis.com/stocks/mu/transcripts/609470-q3-2026/>
48. IBK Securities (Omdia data). "Memory Dynamics monthly: the answer is in memory LTAs (메모리 장기공급계약(LTA)에 해답이 있다)". 2026-05. <https://m.ibks.com/iko/IKO01/download.do?attatchCd=ATTATCH1&menuCode=IKO010301&seq=11657>
49. TrendForce DRAMeXchange. "DRAMeXchange home page: Module Spot Price". 2026-10-26. <https://www.dramexchange.com/>
50. TrendForce. "Samsung Targets 60-70% Capacity Under LTAs; Five Key Customers Reportedly Include AWS, Microsoft, Google". 2026-07-30. <https://www.trendforce.com/news/2026/07/30/news-samsung-targets-60-70-capacity-under-ltas-five-key-customers-reportedly-include-aws-microsoft-google/>
51. TrendForce. "Tight DRAM Supply to Boost DDR5 Contract Prices—Profitability in 2026 Expected to Surpass HBM3e". 2025-10-29. <https://www.trendforce.com/presscenter/news/20251029-12758.html>
52. TrendForce. "CSP CapEx Projected to Exceed US$1.5 Trillion in 2027, with AI Server Revenue Growing Over 90% YoY". 2026-10-14. <https://www.trendforce.com/presscenter/news/20261014-13269.html>
53. TrendForce. "Global Server Shipments for 2024 Projected to Undergo Constrained Growth, Estimated Annual Increase of 2.3%". 2023-08-15. <https://www.trendforce.com/presscenter/news/20230815-11791.html>
54. TrendForce. "After a Low Base Year in 2023, DRAM and NAND Flash Bit Demand Expected to Increase by 13% and 16% Respectively in 2024". 2023-08-30. <https://www.trendforce.com/presscenter/news/20230830-11812.html>
55. TrendForce. "Memory Spot Price Update: DDR5 Prices Up 307% Since September as Module Costs Poised to Surge". 2025-11-19. <https://www.trendforce.com/news/2025/11/19/insights-memory-spot-price-update-ddr5-prices-up-307-since-september-as-module-costs-poised-to-surge/>
56. TrendForce. "2024年Copilot進入商轉，將同步帶動AI Server及終端AI PC發展". 2024-01-17. <https://www.trendforce.com.tw/presscenter/news/20240117-11998.html>
57. VenSearch (citing IDC preliminary). "IDC: PC shipments fell 20.1% in Q3 2026 as memory-driven price hikes hit demand". 2026-10-09. <https://www.vensearch.com/insights/idc-pc-shipments-fell-20-1-in-q3-2026-as-memory-driven-price-hikes-hit-demand>
58. TrendForce. "AI-Driven Memory Boom Ripples Through Hardware Markets, From Price Hikes to Product Delays". 2026-02-20. <https://www.trendforce.com/news/2026/02/20/insights-ai-driven-memory-boom-ripples-through-hardware-markets-from-price-hikes-to-product-delays/>
59. TrendForce. "Downstream Inventory Reduction Eases DRAM Price Decline in 2Q25". 2025-03-25. <https://www.trendforce.com/presscenter/news/20250325-12528.html>
60. IBK Securities (Omdia data). "Memory Dynamics monthly: why Micron is hurrying (마이크론이 이렇게까지 서두르는 이유)". 2026-01. <https://m.ibks.com/iko/IKO01/download.do?attatchCd=ATTATCH1&menuCode=IKO010301&seq=6788>
61. TrendForce. "DRAM Contract Price (price page, 2H Sep 2026)". 2026-09-30. <https://www.trendforce.com/price/dram/dram_contract> **Note: September 2026 values fetched; the October 2026 update is members-only.**
62. FoneArena (citing IDC). "Global PC Shipments up 9.6% YoY in Q4 2025; memory crisis to change market dynamics in 2026: IDC". 2026-01-14. <https://www.fonearena.com/blog/473498/global-pc-shipments-q4-2025.html>
63. TrendForce. "Improved CPU Supply Narrows 2026 Global Notebook Shipment Decline to 9.4%, but Brands Still Face Heavy Cost Pressure". 2026-09-04. <https://www.trendforce.com/presscenter/news/20260904-13217.html>
64. TrendForce. "CSPs to Expand into Edge AI, Driving Average NB DRAM Capacity Growth by at Least 7% in 2025". 2024-06-25. <https://www.trendforce.com/presscenter/news/20240625-12200.html>
65. IDC (via PCWorld). "Computer prices could go up by 20% due to RAM shortage, PC makers warn". 2026-01-05. <https://www.pcworld.com/article/3021660/computer-prices-could-go-up-by-20-due-to-ram-shortage-pc-makers-warn.html>
66. TrendForce. "Rising Costs Threaten Notebook Demand in 2027, Raising Risks of Shipment Declines and Price Increases". 2026-10-08. <https://www.trendforce.com/presscenter/news/20261008-13264.html>
67. TrendForce. "AI-Driven Component Costs Reportedly Push HP, ASUS, Acer to Shift Some PC Production Back to China". 2026-10-28. <https://www.trendforce.com/news/2026/10/28/news-ai-driven-component-costs-reportedly-push-hp-asus-acer-to-shift-some-pc-production-back-to-china/>
68. TrendForce. "HBM4 Raises the Bar on Manufacturing Complexity, Premium Expected to Exceed 30%, Says TrendForce". 2025-05-22. <https://www.trendforce.com/presscenter/news/20250522-12589.html>
69. UBS (via Investing.com). "UBS says Samsung to reach market share parity for HBM with SK Hynix by 2027". 2026-05-13. <https://www.investing.com/news/stock-market-news/ubs-says-samsung-to-reach-market-share-parity-for-hbm-with-sk-hynix-by-2027-4684487>
70. UBS (via Seoul Economic Daily). "Samsung Hits 80 Percent Yield on HBM4, Speeds Up HBM4E". 2026-08-10. <https://en.sedaily.com/finance/2026/08/10/samsung-hits-80-percent-yield-on-hbm4-speeds-up-hbm4e>
71. Counterpoint Research. "Global DRAM and HBM Market Share: Quarterly". 2026-09-02. <https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share>
72. Samsung (Q3 2026 call, via MoneyToday). "Samsung Electronics says HBM4 sales tripled quarter-on-quarter, next year's HBM supply fully booked". 2026-10-29. <https://www.mt.co.kr/en/industry/2026/10/29/2026102911044261630>
73. NVIDIA (Q2 FY2027 call). "NVIDIA Q2 FY2027 Earnings Call Transcript". 2026-08-26. <https://investor.nvidia.com/files/content_files/TRANSCRIPT_-NVIDIA-Corp-NVDA-US-Q2-2027-Earnings-Call-26-August-2026-5_00-PM-ET.pdf>
74. Applied Materials (CFO Bryce Hill, via The Elec). "HBM Becomes a 'Black Hole' for DRAM Capacity, Share Surges Tenfold in Three Years". 2026-03-17. <https://www.thelec.net/news/articleView.html?idxno=5886>
75. TrendForce. "TrendForce presentation at FMS 2025 (Avril Wu)". 2025-08-05. <https://files.futurememorystorage.com/proceedings/2025/20250805_BMKT-101-1_Avril-Wu.pdf> **Note: seen only in a search summary; page not fetched.**
76. KB Securities / Korean media (via Korea JoongAng Daily). "Samsung, SK hynix dramatically scaling up HBM production to meet rising demand, recent Nvidia deals". 2026-01-04. <https://www.koreajoongangdaily.com/business/samsung-sk-hynix-dramatically-scaling-up-hbm-production-to-meet-rising-demand-recent-nvidia-deals/12391367>
77. Micron (FQ4 2026 call). "Micron (MU) Q4 2026 Earnings Call Transcript". 2026-09-30. <https://www.fool.com/earnings/call-transcripts/2026/10/01/micron-mu-q4-2026-earnings-call-transcript/>
78. TrendForce. "HBM Supply Constraints Persist, 2027 Price Outlook Revised Upward with Blended ASP Forecast to Rise 121% YoY, Says TrendForce". 2026-09-29. <https://www.trendforce.com/presscenter/news/20260929-13255.html>
79. SK hynix (Q3 2026 call, via MoneyToday). "DRAM and HBM volumes essentially sold out through 2029". 2026-10-28. <https://www.mt.co.kr/en/industry/2026/10/28/2026102809411541123>
80. NVIDIA. "Inside NVIDIA Blackwell Ultra". 2025-08-22. <https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era>
81. Morgan Stanley (via SemiMedia). "Nvidia expected to take 60% of CoWoS wafer supply by 2026, TSMC to expand packaging in U.S.". 2025-07-31. <https://www.semimedia.cc/nvidia-expected-to-take-60-of-cowos-wafer-supply-by-2026-tsmc-to-expand-packaging-in-u-s/> **Note: the 75 kwpm end-2025 CoWoS value is a sidebar headline only; the 5.4 million unit figure was seen only in a search summary.**
82. NVIDIA. "Inside the NVIDIA Vera Rubin Platform: Six New Chips, One AI Supercomputer". 2026-01-05. <https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/>
83. TrendForce. "Rubin Faces Delay Risks Amid Ongoing Supply Chain Adjustments; Blackwell to Account for Over 70% of NVIDIA's High-End GPU Shipments in 2026, Says TrendForce". 2026-04-08. <https://www.trendforce.com/presscenter/news/20260408-13003.html>
84. NVIDIA (GTC 2025 keynote). "GTC 2025 Keynote". 2025-03-18. <https://s201.q4cdn.com/141608511/files/doc_downloads/2025/03/GTC2025_Keynote.pdf> **Note: seen only in a search summary; page not fetched.**
85. AMD. "AMD Instinct MI400 Series GPUs". 2026. <https://www.amd.com/en/products/accelerators/instinct/mi400.html> **Note: seen only in a search summary; page not fetched.**
86. AMD (Citi TMT conference). "AMD at Citi's 2026 Global TMT Conference". 2026-09-08. <https://www.investing.com/news/transcripts/amd-at-citis-2026-global-tmt-conference-ai-push-lifts-outlook-93CH-4891921>
87. Google Cloud. "From silicon to softmax: Inside the Ironwood AI stack". 2025-11-06. <https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack>
88. UBS (via The Buildout). "UBS forecasts Broadcom and MediaTek TPU shipment volumes for 2026 and 2027". 2026-05-18. <https://thebuildout.ai/intel/3bd003a5-04eb-44ba-ad8b-17129845d8a3>
89. AWS. "Announcing Amazon EC2 Trn3 UltraServers". 2025-12-02. <https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-ec2-trn3-ultraservers/>
90. UBS (via Money Weekly/Cnyes). "Money Weekly column (Hung Pao-shan) on Alchip/Trainium3". 2026-09-03. <https://news.cnyes.com/news/print/6593717>
91. Morgan Stanley (via MoneyToday). "Nvidia also faces rising HBM cost burdens". 2026-08-06. <https://www.mt.co.kr/en/industry/2026/08/06/2026080614030820066>
92. Goldman Sachs (via Tiger Brokers/Deep News). "Goldman Sachs Endorses Storage PE Valuation, Raises Price Targets for SK Hynix, Samsung, and Kioxia". 2026-06-01. <https://www.itiger.com/news/1117469753>
93. SemiAnalysis. "China's CXMT Is Set to Challenge DRAM Incumbents". 2026-06-23. <https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram> **Note: paywalled; seen in summary or title only.**
94. Tom's Hardware. "Micron discontinues 2GB GDDR7 chips for gaming GPUs as it pivots toward higher-density memory for AI". 2026. <https://www.tomshardware.com/pc-components/ram/micron-discontinues-2gb-gddr7-chips-for-gaming-gpus-as-it-pivots-toward-higher-density-memory-for-ai-chipmaker-reportedly-pivots-to-high-margin-3gb-silicon-for-ai-gpus> **Note: headline only; body not read.**
95. Jon Peddie Research. "Q2'26 PC graphics AIB shipments increased 10% from last quarter to 12 million units". 2026. <https://www.jonpeddie.com/news/q226-pc-graphics-aib-shipments-increased-10-from-last-quarter-to-12-million-units/> **Note: seen only in a search summary; page not fetched.**
96. Tom's Hardware. "GeForce RTX 50-series GPU prices spike as much as 39% as Blackwell price hikes hit the US". 2026. <https://www.tomshardware.com/pc-components/gpus/geforce-rtx-50-series-gpu-prices-spike-as-much-as-39-percent-as-blackwell-price-hikes-hit-the-us-rtx-5070-gets-a-36-percent-hike-rtx-5060-up-27-percent-at-the-median-of-newegg-listings> **Note: headline only; body not read.**
97. Jon Peddie Research. "Q4'25 PC graphics AIB shipments decreased -4.4% from last quarter to 11 million units, with a CAGR to 2029 of -5.9%". 2026-03-05. <https://www.jonpeddie.com/news/q425-pc-graphics-aib-shipments-decreased-4-4-from-last-quarter-to-11-million-units-with-a-cagr-to-2029-of-5-9/>
98. NVIDIA. "RTX PRO 6000 Blackwell Workstation Edition datasheet". 2025. <https://www.nvidia.com/content/dam/en-zz/Solutions/data-center/rtx-pro-6000-blackwell-workstation-edition/workstation-blackwell-rtx-pro-6000-workstation-edition-nvidia-us-3519208-web.pdf> **Note: seen only in a search summary; page not fetched.**
99. NVIDIA. "NVIDIA Unveils Rubin CPX". 2025-09-09. <https://nvidianews.nvidia.com/news/nvidia-unveils-rubin-cpx-a-new-class-of-gpu-designed-for-massive-context-inference>
100. Tom's Hardware. "Nvidia removes Rubin CPX accelerators from its roadmap - Groq 3 LPUs take center stage as CPX is removed". 2026-03. <https://www.tomshardware.com/pc-components/gpus/nvidia-removes-rubin-cpx-accelerators-from-its-roadmap-groq-3-lpus-take-center-stage-as-cpx-is-removed> **Note: seen only in a search summary; page not fetched; headline only; body not read.**
101. Yole Group (via Comet Holding CMD 2025). "Memory Market Outlook: DRAM demand projections (in exabytes); Source: Yole, DRAM Market Monitor Q3/2025". 2025-11-13. <https://comet.tech/getmedia/4363db0d-e447-4ea1-bfef-dec81a68884d/Comet-CMD-2025_presentation_final.pdf?disposition=attachment>
102. TrendForce. "Early Purchases Lift 2026 Smartphone Production Above Expectations; Full-Year Forecast Raised to 1.07 Billion Units". 2026-09-08. <https://www.trendforce.com/presscenter/news/20260908-13222.html>
103. Meritz Securities. "Vera CPU 톺아보기 (Feat. SoCAMM2, LPDDR)". 2026-05-22. <https://www.hankyung.com/koreamarket/consensus/pdf/2026-05-899cf1db5212b445c689fe92f4aa08ea>
104. Korea JoongAng Daily. "AI semiconductor market shifts focus from HBM to low-power DRAM module Socamm2". 2026-03-11. <https://www.koreajoongangdaily.com/business/tech-science/ai-semiconductor-market-shifts-focus-to-low-power-dram-module-socamm2/12614719>
105. Omdia (via CXMT IPO prospectus, reported by XenoSpectrum). "CXMT Ramps Up DRAM Output, But Global Shortage Persists Through 2027". 2026-08-21. <https://xenospectrum.com/en/cxmt-dram-supply-growth-2027/>
106. TrendForce. "Automotive Applications Projected to Account for More than 3% of Total DRAM Bit Consumption in 2024". 2021-03-10. <https://www.trendforce.com/news/2021/03/10/automotive-applications-projected-to-account-for-more-than-3-of-total-dram-bit-consumption-in-2024-owing-to-autonomous-vehicle-industry-growth/>
107. Micron. "Micron FQ2 2026 earnings call transcript (Motley Fool)". 2026-03-18. <https://www.fool.com/earnings/call-transcripts/2026/03/18/micron-mu-q2-2026-earnings-call-transcript/>
108. TrendForce. "Tightening of LPDDR4X Supply Drives Up Prices; Smartphone Brands to Accelerate Adoption of LPDDR5X". 2025-07-17. <https://www.trendforce.com/presscenter/news/20250717-12647.html>
109. Counterpoint. "2026 Smartphone Shipments to Post Worst Annual Decline on Record". 2026-06-01. <https://counterpointresearch.com/insights/2026-smartphone-shipments-to-post-worst-annual-decline-on-record-as-memory-crisis-and-geopolitical-shocks-converge>
110. Korea Herald (citing Reuters). "CXMT Announces LPDDR6 Mass Production Ahead of Samsung, SK hynix". 2026-08-31. <https://m.koreaherald.com/article/10857565>
111. TrendForce. "2Q26 Revenue Ranking among Mobile DRAM Suppliers". 2026-08-28. <https://www.trendforce.com/research/download/RP260827LM>
112. SK hynix. "SK hynix Begins Mass Production of 192GB SOCAMM2". 2026-04-20. <https://news.skhynix.com/en/mass-production-socamm2-192gb/>
113. Semicone. "Samsung Formally Halts New Orders for LPDDR4/4X". 2026-04-20. <https://www.semicone.com/article-431.html>
114. TrendForce (citing Micron). "Micron's Fab 6 Starts LPDDR4 and DDR4 Production". 2026-05-26. <https://www.trendforce.com/presscenter/news/20260526-13061.html>
115. TrendForce. "Mobile DRAM Contract Price 3Q26". 2026-08-03. <https://www.trendforce.com/research/download/RP260803NC>
116. Counterpoint. "Smartphone OEMs Shift Focus to Profitability as SoC Shipments Fall 21% YoY in Q3 2026". 2026-10-30. <https://counterpointresearch.com/en/insights/smartphone-oems-shift-focus-to-profitability-as-soc-shipments-fall-21-percent-yoy>
117. CFM (MemoryMarket). "Q3 2026 Global Memory Market Review and Q4 Outlook". 2026-10-10. <https://www.memorymarket.com/a/14963>
118. TrendForce. "4Q25 Revenue Ranking among Mobile DRAM Suppliers". 2026-03-05. <https://www.trendforce.com/research/download/RP260304MS> **Note: paywalled; seen in summary or title only.**
119. TrendForce. "1Q26 Revenue Ranking among Mobile DRAM Suppliers". 2026-05-27. <https://www.trendforce.com/research/download/RP260527WN> **Note: paywalled; seen in summary or title only.**
120. TrendForce. "2026年第四季Mobile DRAM合約價格 / Mobile DRAM Contract Price 4Q26". 2026-10-30. <https://www.trendforce.com.tw/research/download/RP261030PL>
121. IDC. "Worldwide Smartphone Market Grows 2.3% in Q4 2025 (IDC, via MarketScreener)". 2026-01-13. <https://www.marketscreener.com/news/worldwide-smartphone-market-grows-2-3-in-q4-2025-driven-by-strong-performances-from-samsung-and-ap-ce7e58d8df8cf120>
122. IDC. "Higher ASPs, Lower Unit Volumes: How the Memory Crisis Is Reshaping the PC and Smartphone Outlook". 2026-02-26. <https://www.idc.com/resource-center/blog/higher-asps-lower-unit-volumes-how-the-memory-crisis-is-reshaping-the-pc-and-smartphone-outlook/>
123. NVIDIA. "NVIDIA Vera Rubin NVL72". n.d.. <https://www.nvidia.com/en-au/data-center/vera-rubin-nvl72/>
124. NVIDIA. "GB200 NVL72". n.d.. <https://www.nvidia.com/en-us/data-center/gb200-nvl72/>
125. NVIDIA. "GB300 NVL72". n.d.. <https://www.nvidia.com/en-us/data-center/gb300-nvl72/>
126. LS Securities citing TrendForce. "Strong Physical, Strong AI". 2025-03-26. <https://msg.ls-sec.co.kr/eum/K_20250326_31565_230.pdf>
127. IDC. "Worldwide Smartphone Market to Decline 13.9% in 2026". 2026-05-26. <https://www.idc.com/resource-center/blog/worldwide-smartphone-market-to-decline-13-9-in-2026-as-memory-crisis-and-us-iran-war-constrain-growth/>
128. Edgewater Research (quoted by YK Research). "Samsung Electronics (005930.KS) | YK Research". 2026-04-15. <https://investments.chiayong.com/samsung/2026-04-15/>
129. none found. "". 2026-07-23. <https://www.trendforce.com/research/download/RP260723FP>
130. Tom's Hardware. "Samsung to delay its planned DDR4 end-of-life due to signing a long-term 'non-cancellable, non-returnable' contract with key customer". 2026. <https://www.tomshardware.com/pc-components/ddr4/samsung-to-delay-its-planned-ddr4-end-of-life-due-to-signing-a-long-term-non-cancellable-non-returnable-contract-with-key-customer-agreement-will-not-alleviate-consumer-shortage-supply-earmarked-for-server-clients> **Note: headline only; body not read.**
131. TrendForce. "Memory Spot Price Update: DDR4 Prices Continue to Slide Due to CXMT's Abundant Supply". 2025-02-05. <https://www.trendforce.com/news/2025/02/05/insights-memory-spot-price-update-ddr4-prices-continue-to-slide-due-to-cxmts-abundant-supply/>
132. TrendForce. "DDR4 and LPDDR4 Supply Tightens Sharply in 2H25 as Structural Shortage Drives Strong Price Surge". 2025-08-11. <https://www.trendforce.com/presscenter/news/20250811-12667.html>
133. vlsi.kr (secondary). "Market Bulletin: Chips Are 99% of Profit — Samsung Capex Rises to KRW 84.4 Trillion as DS Margin Hits 72.4%". 2026-10-30. <https://www.vlsi.kr/en/samsung-capex-84t-mb-en/>
134. TrendForce. "Micron's Acquisition of PSMC's Tongluo Fab Could Lift Global DRAM Supply Outlook in 2027". 2026-01-19. <https://www.trendforce.com/presscenter/news/20260119-12883.html>
135. Economic Daily News (via TrendForce). "TSMC CoWoS Supply-Demand Gap Reportedly Seen Narrowing from 20% to 10% by End-2026 as Capacity Expands". 2026-06-15. <https://www.trendforce.com/news/2026/06/15/news-tsmc-cowos-supply-demand-gap-reportedly-seen-narrowing-from-20-to-10-by-end-2026-as-capacity-expands>
136. J.P. Morgan (via Finvaulta). "Asia Semis: Key Takeaways from Semicon Taiwan". 2026-09-09. <https://finvaulta.com/research/jp-morgan/asia-semis-key-takeaways-from-semicon-taiwan-2026-09-09>
137. SK hynix. "SK hynix Partners with TSMC to Strengthen HBM Technological Leadership". 2024-04-19. <https://news.skhynix.com/en/sk-hynix-partners-with-tsmc-to-strengthen-hbm-technological-leadership/> **Note: seen only in a search summary; page not fetched.**
138. Samsung. "Samsung Ships Industry-First Commercial HBM4". 2026-02. <https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing> **Note: seen only in a search summary; page not fetched.**
139. Micron (FQ4 2025 call). "Micron FY2025 Q4 Earnings Call Transcript". 2025-09-23. <https://storage.googleapis.com/magi-store/earnings/MU/2025-09-23_Q4_FY2025/03_outputs/transcript.html>
140. TrendForce (news). "SK hynix Reportedly Places HBM4 TC Bonder Order With ASMPT Amid Hanmi-Hanwha Patent Clash". 2025-12-12. <https://www.trendforce.com/news/2025/12/12/news-sk-hynix-reportedly-places-hbm4-tc-bonder-order-with-asmpt-as-hanmi-hanwha-patent-clash-heats-up/>
141. TrendForce (news). "Where is the Spring of the Memory Market?". 2025-02-07. <https://www.trendforce.com/news/2025/02/07/news-where-is-the-spring-of-the-memory-market/>
142. TrendForce. "ASML Raises 2026 Sales Outlook to EUR36B-EUR40B on Memory, Logic Demand; South Korea Share Hits 45%". 2026-04-15. <https://www.trendforce.com/news/2026/04/15/news-asml-raises-2026-sales-outlook-to-e36b-e40b-on-memory-and-logic-client-demand-south-korea-share-hits-45/>
143. Micron. "Micron Technology, Inc. Reports Record Fiscal Fourth Quarter and Full Year 2026 Results". 2026-09-30. <http://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results>
144. Nanya Technology. "Nanya Q4 2025 Investor Conference". 2026-01-19. <https://www.nanya.com/en/Activity?Action=IR_investorcalendar_FileName&Id=4276&column=Presentation>
145. TrendForce. "Memory Industry to Maintain Cautious CapEx in 2026, with Limited Impact on Bit Supply Growth". 2025-11-13. <https://www.trendforce.com/presscenter/news/20251113-12780.html>
146. TrendForce. "CXMT, YMTC Ramp Memory Capacity (citing TrendForce 2026-09-07 release)". 2026-09-24. <https://www.trendforce.com/news/2026/09/24/news-cxmt-ymtc-ramp-memory-capacity-but-chinas-ai-cloud-boom-could-soak-up-new-supply-through-2027/>
147. TrendForce. "CXMT Confirms LPDDR5X Mass Production Began in May, High-speed Variant Under Customer Trials". 2025-10-29. <https://www.trendforce.com/news/2025/10/29/news-cxmt-confirms-lpddr5x-mass-production-began-in-may-high-speed-variant-under-customer-trials/>
148. TrendForce. "CXMT Reportedly Ships HBM3E Samples, Eyes Production Within 2 Months Despite 20-30% Yields". 2026-10-28. <https://www.trendforce.com/news/2026/10/28/news-cxmt-reportedly-ships-hbm3e-samples-eyes-production-within-2-months-despite-20-30-yields/>
149. TrendForce. "U.S. Adds Tech Giants CXMT, Tencent, and CATL to List of Chinese Firms Linked to Military Support". 2025-01-07. <https://www.trendforce.com/news/2025/01/07/news-u-s-adds-tech-giants-cxmt-tencent-and-catl-to-list-of-chinese-firms-linked-to-military-support/>
150. US Commerce BIS. "Commerce Strengthens Export Controls to Restrict China's Capability to Produce Advanced Semiconductors for Military Applications". 2024-12-02. <https://www.bis.gov/press-release/commerce-strengthens-export-controls-restrict-chinas-capability-produce-advanced-semiconductors-military>
151. TrendForce. "SK hynix Reportedly Seeks U.S. Chip Tool Approval for China Expansion to Fund Potential U.S. NAND Fab". 2026-10-15. <https://www.trendforce.com/news/2026/10/15/news-sk-hynix-reportedly-seeks-u-s-chip-tool-approval-for-china-expansion-to-fund-potential-u-s-nand-fab/>
152. The White House. "Adjusting Imports of Semiconductors, Semiconductor Manufacturing Equipment, and Their Derivative Products into the United States". 2026-01-14. <https://www.whitehouse.gov/presidential-actions/2026/01/adjusting-imports-of-semiconductors-semiconductor-manufacturing-equipment-and-their-derivative-products-into-the-united-states/>
153. TrendForce. "U.S. Slaps 20% Tariff on Taiwan: Foundries Unscathed, Downstream Burned; Section 232 Looms". 2025-08-01. <https://www.trendforce.com/news/2025/08/01/news-u-s-slaps-20-tariff-on-taiwan-foundries-unscathed-downstream-takes-the-heat-section-232-looms/>
154. TrendForce. "Passive Buyer Strategies Drive DRAM Contract Prices Down Across the Board in 1Q25". 2024-12-30. <https://www.trendforce.com/presscenter/news/20241230-12424.html>
155. TrendForce. "Price Rally Drives 4Q25 DRAM Revenue Up 29.4%; Samsung Regains No. 1 Market Share". 2026-02-26. <https://www.trendforce.com/presscenter/news/20260226-12937.html>
156. TrendForce. "DRAM Prices to Continue Rising in 4Q25, Server Demand Surges Ahead While Legacy Process Products See Steeper Increases". 2025-09-24. <https://www.trendforce.com/presscenter/news/20250924-12733.html>
157. TrendForce. "Global DRAM Revenue Jumps 30.9% in 3Q25, Micron's Market Share Climbs by 3.7 Percentage Points". 2025-11-26. <https://www.trendforce.com/presscenter/news/20251126-12802.html>
158. TrendForce. "AI Architecture Evolution Set to Drive Memory Market Revenue to a New Peak in 2027, with Annual Growth Exceeding 50%". 2026-01-22. <https://www.trendforce.com/presscenter/news/20260122-12893.html>
159. TrendForce. "Samsung's DS Unit Delivers 99.7% of Q2 Profit amid Memory Boom; HBM4 Revenue Reportedly to Triple in Q3". 2026-07-30. <https://www.trendforce.com/news/2026/07/30/news-samsungs-ds-unit-delivers-99-7-of-q2-profit-amid-memory-boom-hbm4-revenue-reportedly-to-triple-in-q3/>
160. TrendForce. "Samsung Says HBM Share Matches DRAM Standing as HBM4 Sales Triple; DS Margin Hits 72%, 10 LTA Clients Signed". 2026-10-29. <https://www.trendforce.com/news/2026/10/29/news-samsung-says-hbm-share-matches-dram-standing-as-hbm4-sales-triple-ds-margin-hits-72-10-lta-clients-signed/>
161. TrendForce. "Memory Spot Price Update: DDR4 Spot Prices Climb as Samsung Holds EOL Line". 2025-12-31. <https://www.trendforce.com/news/2025/12/31/insights-memory-spot-price-update-ddr4-spot-prices-climb-as-samsung-holds-eol-line>
162. TrendForce. "Memory Spot Price Update: DDR4 & DDR3 Prices Rise Amid Strong DDR5 Rebound Led by SK hynix". 2025-03-19. <https://www.trendforce.com/news/2025/03/19/insights-memory-spot-price-update-ddr4-ddr3-prices-rise-amid-strong-ddr5-rebound-led-by-sk-hynix/>
163. Micron. "Fiscal Q4 2026 Earnings Call Prepared Remarks". 2026-09-30. <https://s25.q4cdn.com/621799436/files/doc_financials/2026/q4/Q4-FY26-Prepared-Remarks.pdf>
164. TrendForce. "Decoding Micron's SCAs: Reportedly 20% of DRAM Output, Toward 50% of Long-Term Memory Revenue". 2026-06-25. <https://www.trendforce.com/news/2026/06/25/news-decoding-microns-scas-reportedly-20-of-dram-output-toward-50-of-long-term-memory-revenue/>
165. SK hynix. "SK hynix Announces 1Q26 Financial Results". 2026-04-23. <https://news.skhynix.com/en/q1-2026-business-results/>
166. SK hynix. "SK hynix Announces 2Q26 Financial Results". 2026-07-29. <https://news.skhynix.com/en/q2-2026-business-results/>
167. TrendForce. "Memory Price Surge Intensifies Retail Pricing Pressure, Putting Global Smartphone Production at Risk of a Sharp Decline". 2026-02-11. <https://www.trendforce.com/presscenter/news/20260211-12922.html>
168. TrendForce. "Apple Price Hikes Erode Neo's Cost Edge as Xbox Cites 2.5x Memory Surge for New Increase". 2026-06-26. <https://www.trendforce.com/news/2026/06/26/news-apple-price-hikes-erode-neos-cost-edge-as-xbox-cites-2-5x-memory-surge-for-new-increase/>
169. TrendForce. "Lenovo Reportedly Sees Higher Memory Prices Becoming the New Normal Into 2030". 2026-06-26. <https://www.trendforce.com/news/2026/06/26/news-lenovo-reportedly-sees-higher-memory-prices-becoming-the-new-normal-into-2030/>
170. TrendForce. "AI Wave & DRAM Deficits: 2027 Global DRAM Outlook (report TOC, paywalled)". 2026-07-28. <https://www.trendforce.com/research/download/RP260728GY> **Note: paywalled; seen in summary or title only; headline only; body not read.**
171. Omdia. "2026 Trends to Watch: Semiconductors (p.24)". 2025-12-05. <https://omdia.tech.informa.com/-/media/tech/omdia/assetfamily/2025/12/04/2026-trends-to-watch-semiconductors/2026-trends-to-watch-semiconductors-pdf.pdf>
172. TrendForce. "Apple's New Devices and Early Stocking of Memory for GB200 Supported Positive Revenue Growth in 3Q24". 2024-12-02. <https://img.trendforce.com/Report/2024/12/20241205_151919_RP241202GE_preview.pdf>
173. Taipei Times (TrendForce data). "Server shipments to grow 6%, AI servers to rise 24.1%". 2025-11-18. <https://www.taipeitimes.com/News/biz/archives/2025/11/18/2003847369>
174. TrendForce. "Server DRAM Will Overtake Mobile DRAM in Supply in 2023 and Comprise 37.6% of Annual Total DRAM Bit Output". 2023-02-20. <https://www.trendforce.com/presscenter/news/20230220-11572.html>
175. Counterpoint. "Global Smartphone Average DRAM Hits Record 8.4GB in 2025". 2026-02-26. <https://counterpointresearch.com/en/insights/Global-Smartphone-Average-DRAM-Hits-Record-8.4GB-in-2025>
