# Total DRAM supply: source notes

File: `total-dram.csv` (573 rows). Collected 2026-10-30.
Units: 1 EB = 8 billion Gb. "bn Gb" means billion gigabits.

## Best anchor for total bits (absolute units)

Use the Mirae Asset series in billion Gb. It is the only one that gives
absolute bits for supply and demand, by vendor and by application, over many years.

| Years | Source | What it gives |
|---|---|---|
| 2010-2013 | KDB Daewoo, Nov 2012, Table 11 | Supply and demand in million 1Gb units, by vendor, app mix |
| 2015-2021 | Mirae Asset Daewoo, Jun 2020, Table 4 | Supply (bn Gb) by vendor; demand for mobile, server, PC only |
| 2023-2027 | Mirae Asset, Dec 2025, p.16 | Supply and demand (bn Gb), by vendor, by app, wafer capacity |

Cross-checks agree well:
- 2010: KDB 15.3 bn Gb supply. iSuppli 15.9 bn Gb.
- 2018: Mirae 104.3 bn Gb supply. Nanya 27.4 bn 4Gb units = 109.6 bn Gb.
- 2020: Frost & Sullivan 155 bn Gb. Mirae 147.3 bn Gb (forecast).
- 2024: Mirae 247.3 bn Gb demand (30.9 EB). Frost & Sullivan 250 bn Gb (31.3 EB). Yole 33 EB.
- 2025-2026: KGI implies 37.6 EB and 44.1 EB. Yole gives 38 EB and 43 EB.

Gaps in absolute bits: 2014 and 2022. The CSV has derived rows for them.
A backcast chain from Mirae 2023 (209.5 bn Gb) with Mirae YoY growth gives
2016-2022 values. These are marked `derived`.

## Growth series (YoY %)

- 2006-2012: Micron 2011 analyst day (average of Gartner, IDC, iSuppli). The label order was inferred.
- 2012-2019: DRAMeXchange via Mirae, May 2020 (bit growth).
- 2015-2021: Mirae, Jun 2020 (supply growth).
- 2017-2026: Mirae, Dec 2025 (demand growth, plus growth without server/AI).
- 2022-2028: TrendForce, Micron, SK hynix, Omdia and Counterpoint forecasts. Each vintage is a separate row.

Forecasts change a lot between vintages. One example is 2023: TrendForce forecast
+14.1% supply in 2022, but Mirae reports -4.4% actual production. So use actual or
estimate rows for history. Use forecast rows only for the forecast years.

## Application mix: definition conflicts

The sources do not agree on what each category includes.
- **Mirae (Dec 2025)**: mobile, PC, server, graphics, other. Graphics = HBM + GDDR. Server excludes HBM.
- **Yole (via Comet)**: data center, mobile, PC, consumer, other. Data center most likely includes HBM.
  Small series are mapped by stack order, so PC, consumer and other are uncertain.
- **KDB (2012)**: PC, server, module, mobile, consumer, other. There is no graphics category.
- **Nanya (2018)**: PC + upgrade, server + workstation, mobile + tablet, consumer, auto. It mixes Gartner, IHS and DRAMeXchange.
- **TrendForce**: shares of bit *output* (2023: server 37.6%, mobile 36.8%). Other sources give shares of *demand*.
- **KGI (Nov 2025)**: server 38% (2025) and 47% (2026). This is much higher than Mirae (41%) because KGI includes general-server buying in 2026.

The 2018 server share shows the spread: Nanya 24%, Mirae 34%.

**Recommended mix series**: use Mirae for 2023-2027 (one set of definitions, sums to 100).
Use KDB for 2010-2013. Map module to PC. For 2015-2021, use the Mirae 2020 mobile, server and
PC bits. Assign the remainder (total supply minus these three) to graphics + consumer + other.
Treat Yole and KGI as checks. Do not mix their shares with Mirae shares in one series.

## Wafer capacity (kwpm, 300 mm equivalent)

- Nanya (DRAMeXchange, inSpectrum, IHS): industry wafer starts for 2010-2018 (1,304 down to 1,058, then 1,210).
- Mirae Dec 2025: 1,363 (2023), 1,645, 1,904, 2,052 (2026F), 2,237 (2027F), with per-vendor values.
- These two series do not join cleanly. Mirae shows -14.4% in 2023 because of cuts to wafer input,
  so it measures input, not installed capacity. Mirae also gives end-2026 values for Samsung (700)
  and SK hynix (605). These are higher than its table values (665, 586), which are most likely annual averages.
- CXMT: 320 kwpm now and 420 kwpm in 2027 (Commercial Times via TrendForce, Sep 2026).
  This is above Mirae's 298 and 328.

## Capex

- DRAM industry capex: TrendForce gives 53.7 (2025) and 61.3 (2026F, Nov 2025).
  Mirae gives 66.1 (2026F). Mirae 2019 Outlook gives 18.2 (2019F).
- Vendor guidance in 2026 is much higher than the Nov 2025 industry forecasts. See the next section.
- Gap: there is no clean annual industry capex series for 2010-2024.

## Revenue

There are point values only: KDB 2010-2013, Yole 2017-2018, TrendForce quarters for 4Q24-2Q26,
and TrendForce/Gartner forecasts. There is no single consistent annual series.
Use revenue only for context.

## Main gaps

- Absolute bits for 2014 and 2022 (derived only).
- Graphics and consumer bits for 2015-2022 (residual only).
- TrendForce full-year actual bit growth for 2024 and 2025. Its press releases give forecasts only.
- Paywalled: TrendForce 2027 DRAM Outlook (only the 24% headline), Yole DRAM Monitor, Omdia, Counterpoint.
- The web search budget ran out during the 2026 pass. Micron FQ3 2026 and Counterpoint rows are search summaries only, marked in notes.

## 2026 production / 2027 outlook

### 2026 bit output

- Industry bit shipment growth in 2026 is about **+25%**. Micron (Sep 2026) says mid-20s.
  SK hynix (Oct 2026) says achievable demand grows mid-20s. Earlier views were lower:
  Micron about 20% (Dec 2025) and low 20s (Mar 2026), Omdia about 20%, Mirae +20.3% production.
- Base: 2025 production was 293.1 bn Gb (Mirae). At +25%, 2026 is about **366 bn Gb (45.8 EB)** (derived).
- Supply is short of demand. TrendForce puts the 2026 sufficiency ratio at -1% to -2%.
- Quarter by quarter, by vendor (QoQ bit shipments):

| Vendor | 2Q26 | 3Q26 | 4Q26 guide |
|---|---|---|---|
| Samsung | low teens | low to mid single digit | mid to high teens |
| SK hynix | high single digit | about 10% | mid-20s |
| Nanya | - | - | full-year target: teens |

- Mirae (Dec 2025) has quarterly bn Gb forecasts for Samsung and SK hynix (rows in the CSV).
- HBM share: TrendForce says HBM takes 18% of wafer input at end-2025, 22% at end-2026 and 30% at end-2027,
  but only 8%, 9% and 13% of bits. HBM plus RDIMM is 51% of 2026 DRAM bits.
- Node mix (Chosun Biz via TrendForce): SK hynix 1c share is 10% (1Q26), 13% (2Q26),
  24% (3Q26F), 34% (4Q26F) and 35% (1Q27F). In 1Q27F, 1c passes 1b (33%).
  Samsung 1c is about 16% (2Q26) and 31% (4Q26F). Micron 1-gamma is about 19% (2Q26).
  Most 2026 bit growth comes from moving to new nodes, not from new fabs.
- Gap: no published industry utilization rate. No industry kwpm by quarter for 2026.

### Fabs that change 2027 output

| Fab | Status (date of statement) | Change |
|---|---|---|
| SK hynix M15X (Cheongju) | Mass production pulled forward (Jul 2026). Full capacity by end-2026 (Oct 2026). Mirae: +40 kwpm in 2026 | Pulled in |
| SK hynix Yongin Phase 1 | Cleanroom opens early 2027. Full-scale operation in 2027. Later cleanrooms open in phases (Oct 2026) | On plan; shell construction accelerated |
| SK hynix M16 | Mirae: +55 kwpm in 2026 | - |
| Samsung P4 | Operating (Oct 2026). Mirae: +55 kwpm in 2026 | - |
| Samsung P5 | Under construction. Operations in 2028, pulled forward by two years (vlsi.kr, Oct 2026) | Pulled in (secondary source) |
| Micron ID1 (Idaho) | First wafer output mid-2027 (Sep 2026). TrendForce (Nov 2025): not before 2027 | On plan |
| Micron ID2 | Wafer output late 2028 | On plan |
| Micron Japan (Hiroshima) expansion | Initial output late 2028 | - |
| Micron Taiwan Tongluo (ex-PSMC) | Meaningful shipments mid-2027 (Sep 2026). Earlier: fiscal 2028 (Mar 2026) | Pulled in |
| Micron New York | Initial output 2030 | - |
| CXMT | 320 kwpm now, 420 kwpm by 2027. Shanghai and Beijing fabs planned | Growing |
| Nanya new fab | Equipment move-in early 2027 | - |

TrendForce (Jul 2026): new fabs ramp from 2H27, and meaningful output comes only in 2028.
Gap: no kwpm figures for M15X, Yongin, P5, ID1 or Tongluo from the companies. Micron Taiwan A3/A5
and Hiroshima capacity were not found.

### 2026 capex and first 2027 guidance

- Samsung: 2026 total 84.4 tn KRW. DS division 76.8 tn KRW (+29.3 tn). Memory is not split out.
  The initial plan was 60-70 tn KRW.
- SK hynix: 2026 capex is in the high 40s tn KRW (Jul 2026). 2027 is "to increase significantly" (Oct 2026).
- Micron: FY2026 above 25 bn USD (Mar 2026). 1H FY2027 about 25 bn USD, and 2H FY2027 higher (Sep 2026).
- Nanya: 2026 up to 50 bn NTD (13.4 bn NTD in 2025).
- Industry (Nov 2025 vintage): TrendForce 61.3 bn USD, Mirae 66.1 bn USD for 2026. Vendor guidance now runs above these.
- Samsung and Micron say much of the 2027 capex buys cleanroom space. That spending adds bits in 2028 and later, not in 2027.

### Latest bit growth views for 2027

| Source | Date | 2027 view |
|---|---|---|
| SK hynix | 2026-10-27 | Achievable demand +mid-20s; supply short through 2030 |
| Samsung | 2026-10-29 | No number; tight into 2028 |
| Micron | 2026-09-30 | Industry bit shipments +low 20s in 2027 and 2028 |
| TrendForce | 2026-07-28 | Supply +24%; server DRAM + HBM bits +27% (Aug 2026); gap widens |
| Mirae | 2025-12-15 | Demand +21.7%, production +17.9% |

Recommended 2027 range for the modeler: **+20% to +25% bit supply**, central value +22% to +24%.
On a 2026 base of about 366 bn Gb, that gives about 440-460 bn Gb (55-57 EB) in 2027 (derived).
