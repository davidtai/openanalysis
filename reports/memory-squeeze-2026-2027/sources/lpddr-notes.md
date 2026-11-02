# LPDDR sources: notes for the modeler

Data file: `lpddr.csv` (193 rows). Collected 2026-10-30. Each row has a URL and a quote. Derived rows show the formula in `quote` and their inputs in `notes`.

## 1. Best series for LPDDR bits

No public source gives "total LPDDR bits by year" directly. Build the series from three parts:

LPDDR bits = smartphone bits + other mobile bits (tablets) + PC LPDDR bits + server LPDDR bits + auto LPDDR bits

1. **Mobile (phones), 2024-2030: Yole DRAM Market Monitor Q3/2025** (via the Comet CMD 2025 deck). Mobile DRAM demand is 9, 10, 11, 12, 14, 15 and 17 EB for 2024-2030. Total DRAM is 33 to 85 EB. This is the only consistent multi-year bit series in EB that I found. Mobile share falls from 27% to 20%. The mobile CAGR from the endpoints is 11.2%.
2. **Phones, 2015-2026: units x content.** IDC units (2014-2025 actuals, 2026-2028 forecasts) times GB per phone. Content points: Micron 3 GB (2018), 4 GB (2019), ~5 GB (2020); Counterpoint 5.3 GB (Q1 2021), 7.4 GB (Dec 2024), 8.4 GB (Dec 2025); TrendForce 8.5 GB (2026F). TrendForce YoY content growth fills 2022-2024: +3.9%, +17.5%, +14.1%. The derived check (IDC x Counterpoint) gives 9.2 EB for 2024 and 10.6 EB for 2025. Yole gives 9 and 10 EB. The two agree within about 5%.
3. **Server LPDDR (Grace, Vera, SOCAMM), 2024-2027: broker estimates.** LS Securities: 1.1 bn Gb (2024) and 6.0 bn Gb (2025) for AI-server LPDDR5X. Meritz: 24 bn Gb (3.0 EB) Nvidia SOCAMM2 in 2026, and 9,084 PB (9.1 EB) in 2027. Edgewater (third-hand): 21-23 bn in 2026 and 60-70 bn in 2027, unit probably Gb. These agree in size. TrendForce says suppliers can meet only ~60% of Nvidia's 2027 need. So treat 2027 demand as a ceiling, not as supply.
4. **PC LPDDR:** TrendForce says LPDDR is 30-35% of PC DRAM demand (2024). Apply this share to the PC DRAM bits from the other agents. Macs give a floor: 25.6 M units x 16 GB = 0.41 EB in 2025.
5. **Auto:** about 2-3% of DRAM bits (Omdia 2025: ~2%; TrendForce 2024F: >3%). Micron says the average car has ~16 GB of DRAM. Most automotive DRAM is LPDDR4/5, but I found no source that gives the LPDDR share.

## 2. Definition conflicts

- **"Mobile DRAM" is not the same as "smartphone".** TrendForce "mobile DRAM" (LPDRAM) revenue and bits include LPDDR5X sold to Nvidia for Grace (the 3Q24 report says so). Yole puts Grace/SOCAMM in "Data Center", not in "Mobile". Do not add TrendForce mobile bits to Yole data-center bits. That counts server LPDDR twice.
- **Mobile share of DRAM bits differs a lot by source.** TrendForce: 40% (2020), ~40% (2022F), 36.8% (2023F). KGI: 36% (2025) and 29% (2026F). Omdia: 28% (2025). Yole: 27% (2024) and 26% (2025). Mirae: 34% (2018). TrendForce and KGI use supply or bit output. Yole and Omdia use demand. Yole's total may also include HBM bits in data center. For the model, pick one basis (Yole demand) and keep the others as a range.
- **Content per phone: December value vs annual average.** Counterpoint gives the December value (8.4 GB in Dec 2025). TrendForce gives a calendar-year average: 8.5 GB in 2026 at +10% implies about 7.7 GB for 2025. The December value overstates the annual average by about 8%.
- **Shipments vs production.** IDC and Omdia count shipments. TrendForce counts production. IDC revises the prior year (2023: 1166.9 then 1164.1; 2024: 1238.8 then 1236.3). Omdia is about 1-1.5% lower than IDC. I kept every version as a separate row.
- **GB vs GiB.** Phone RAM "GB" is binary (GiB). Yole EB is decimal. The difference is about 7%. I did not correct for it.
- **Gb vs GB.** Broker server numbers are in gigabits. Divide by 8 to get GB.

## 3. Gaps

- **No LPDDR bit share of total DRAM for 2015-2023.** I found mobile shares only for 2018, 2020, 2022F and 2023F. There is no clean annual series before 2024.
- **Content per phone for 2015-2017 and 2022-2023 in GB.** I found growth rates only. A TrendForce 2016 seminar deck exists, but its slides are images I could not read.
- **Annual mobile DRAM revenue.** I found quarterly values only: 4Q17 $8.0B, 2Q18 $8.869B, 3Q24 $6.442B, 4Q25 >$10B, then +64.5% and +80% QoQ in 2026. From these, 2Q26 is at least $29.6B (derived lower bound). The full TrendForce series is paywalled.
- **LPDDR6 share.** No public forecast. TrendForce says only "LPDDR6 to debut in 2H26 with low uptake". The first phone (Xiaomi 18 Fold, CXMT LPDDR6) targets only 0.2-0.3 M units. A Korean press figure of 3% (2027) and 9% (2028) came up in a search summary only. I could not open the source, so it is not in the CSV.
- **GB200/GB300 rack counts.** Public numbers are unreliable. I kept the Nvidia run rate (~1,000 NVL72 racks per week per major hyperscaler, May 2025) and the old TrendForce 60k NVL36 forecast. Get rack counts from the HBM/GDDR agent so that both use the same GPU volume.
- **Tablets and LPCAMM2 units.** I found tablet units (IDC 2025: 151.9 M) but no tablet DRAM content. LPCAMM figures are bit shares only (TrendForce via LS: 1% in 2024, 5-10% in 2025, 15-20% in 2026), and they predate the memory crisis.
- **Forecasts after 2028.** Only Yole (to 2030) and Omdia (server 71% of DRAM by 2030) go that far. No source gives a mobile or LPDDR forecast to 2030 that already includes the 2026 memory crisis. Yole's Q3/2025 view came before the crisis.

## 2026 / 2027

52 rows were added on 2026-10-30. Most are dated Jul–Oct 2026. Segments: `lpddr-supply`, `lpddr-price`, and new rows in `lpddr-server`, `smartphone` and `lpddr-pc`.

### Production and capacity moves
- No vendor publishes LPDDR5X wafer or bit output. I found no LPDDR5X production split by vendor. Use the capacity signals below instead.
- HBM takes wafers away from LPDDR. Samsung says HBM uses about 20% of industry DRAM wafer capacity now and will use nearly 30% in 2027. HBM needs about 3x the wafer area per bit. TrendForce says conventional DRAM loses supply at two to three times that pace.
- Samsung puts about 30,000–40,000 wafers per month of LPDDR5X into Nvidia SOCAMM2. That is about 5% of its DRAM output (Korean press, Dec 2025).
- Micron cut its supply to smartphone brands in 2Q26 (TrendForce). Its mobile bit shipments fell while its revenue rose.
- CFM (Oct 2026) says server LPDDR5X demand could double in 2027 and pass mobile demand. Suppliers may then move more LPDDR capacity to servers.
- SK hynix has long-term agreements for more than 50% of its 2027–2028 capacity. It expects demand above supply through 2030.

### Contract prices (QoQ)
| Quarter | Value | Source |
|---|---|---|
| 2Q26 | LPDDR4X +70–75%, LPDDR5X +78–83% | TrendForce, May 2026 |
| 4Q25 to 2Q26 | about 3x | Counterpoint, Jun 2026 |
| 3Q26 | mobile DRAM +8–13% (Samsung mid-single digit) | TrendForce, Aug 2026 |
| 3Q26 | smartphone memory +5–10% (actual) | Counterpoint, Oct 2026 |
| 4Q26 | mobile +0–5% (TrendForce, via Goldman); +3–4% (Goldman); LPDDR4X/5X +0–5% (CFM); +5% (Counterpoint) | Oct 2026 |
| 1Q27 | LPDDR5X +13–18%, LPDDR4X +5–10% (TrendForce, via Goldman); LPDDR5X >+20% (CFM) | Oct 2026 |

There is no public number for 1H27 as a whole. TrendForce (Jul 2026) says mobile DRAM supply stays tight in 2027. 4Q26 is a pause, not a peak: prices flatten in 4Q26 and rise again in 1Q27. Notebook LPDRAM rises faster than phone LPDRAM in 4Q26.

### SOCAMM2 for Vera Rubin
- Qualification and production: Samsung was first to mass-produce 192 GB modules (1b, by Mar 2026). Micron's 192 GB module is in high-volume production (Mar 2026), and Micron sampled 256 GB modules in Mar 2026. SK hynix began mass production of 192 GB modules (1c) in Apr 2026.
- Vendor volumes are estimates only. Nvidia publishes none.
  - KB Securities: Samsung supplies about 10 bn Gb, about 50% of Nvidia's 2026 SOCAMM2 demand. That puts total demand at about 20 bn Gb. Meritz gives 24 bn Gb.
  - SK hynix has more orders than Micron (JoongAng, Mar 2026).
  - TrendForce News (Oct 2025) gives 100 / 110 / 70 bn Gb for Samsung / SK hynix / Micron. These are probably 10x too high (a Korean unit error). Divided by 10, they total 28 bn Gb.
- In Jun 2026 Nvidia halved SOCAMM capacity per Vera Rubin module, because LPDRAM supply was short.
- I found no SOCAMM2 vendor-share update dated Jul–Oct 2026.

### OEM spec and price moves
- Phones:
  - High-end phones settle at 12 GB, and 16 GB use declines. Mid-range phones go back to 8 GB and entry phones to about 4 GB (TrendForce, May 2026).
  - IDC gives an example: a phone that had 12 GB + 256 GB a year ago may now ship with 8 GB + 128 GB.
  - Galaxy S26: +4.7% in the US for the base model and +10% for the Plus.
  - Xiaomi Japan: up to +¥20,000 per device from Sep 2026, with RAM kept at 12 GB.
  - IDC expects the smartphone ASP to reach $581 in 2026 (+27.6%).
- PCs: OEMs plan price hikes of 15–20% (Asus 10–30%). Copilot+ PCs keep a 16 GB floor.

### 2027 outlook
- Units: the newest forecasts point down. Counterpoint (Oct 30) says smartphone SoC shipments fall 3–4% in 2027. IDC (May) says phone units fall 1.1%. Samsung (Oct 29) expects unit volumes to decline. The older IDC forecast of +1.9% (Feb) is superseded. Model 2027 phone units at about 0% to −4% versus 2026.
- GB per phone: no source publishes a 2027 number. Configurations froze in 2026, with high-end phones at 12 GB. Assume flat to +5% from the 2026 value of 8.5 GB. This is an assumption.

### LPDDR4 end of supply
- Samsung stopped taking new LPDDR4/4X orders on 2026-04-17, finishes existing orders by end-2026, and converts the lines from 1Q27. This comes from trade press, not from a Samsung release.
- I found no date for SK hynix.
- Micron keeps LPDDR4 for long-life products: Fab 6 supply of LPDDR4 + DDR4 is set to quadruple by 2027. CXMT still sells LPDDR4X.
- Counterpoint expects LPDDR4 supply to fall more than 40% in 2026.
- For the model: LPDDR4X phone supply ends in 2027. A small long-life LPDDR4 tail (auto, industrial) continues from Micron and CXMT.

## 4. Recommendation

1. Use **Yole mobile EB (2024-2030)** as the base for phones. Lower 2026-2027 for the memory crisis: IDC now sees 2026 units at -16.7% and 2027 at -1.1%, and TrendForce sees content at +10% in 2026. Units x content then gives about 8.9-9.1 EB for phones in 2026, below Yole's 11 EB. Return to Yole's path from 2028, when IDC and Counterpoint expect the rebound.
2. Backcast phones for 2015-2023 with IDC units x content. Interpolate content in log space between the anchor points. Mark these years as modeled, not observed.
3. Model **server LPDDR as its own line**: 0.14 EB (2024), 0.75 EB (2025), about 3 EB (2026), and 7.5-9 EB of 2027 demand capped at ~60% fill. TrendForce expects AI servers to pass smartphones as the largest LPDRAM market in 2028-2030. Use that as a check: server LPDDR should cross phone LPDDR (about 12-17 EB) within that window.
4. PC LPDDR = 30-35% of PC DRAM bits, rising with AI PCs and LPCAMM2. Auto = 2-3% of DRAM bits, mostly LPDDR.
5. For the generation mix: LPDDR5/5X is 50% of mobile bits in 2024 and about 58-60% in 2025. LPDDR4X falls by double digits in 2026 (Counterpoint: LPDDR4 supply down >40%). Keep LPDDR6 below 5% until 2027, then let it ramp. This last step is an assumption, not a sourced number.
