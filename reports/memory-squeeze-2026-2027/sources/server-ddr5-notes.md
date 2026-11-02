# Server DRAM and DDR5: source notes

Written 2026-10-30T22:49Z. Data file: `server-ddr5.csv` (266 rows). Builder: `../tools/build_server_ddr5_csv.py`. Raw PDFs and extracted text: `raw-server-ddr5/`.

Rows marked `SEARCH-SUMMARY` in `notes` come only from a web-search summary. Nobody fetched the page, so treat them as unverified. All other rows have a quote from a page or PDF that was fetched and read.

## Best consistent series

1. **Server DRAM bits, share and content (2023-2027): the Mirae table.** Mirae Asset, 2025-12-15, page 16. One model gives bits by application (bn Gb), share, growth, units and GB per unit. The parts agree with each other: 515 GB x 19M units x 8 is about 78 bn Gb, and the table says 76.9. Server excludes HBM, because HBM sits in "Graphics DRAM".
   - Server share of DRAM bit demand: 36.7% (2023), 36.8% (2024), 38.2% (2025), 41.0% (2026F), 41.3% (2027F).
   - GB per server: 515, 597, 717, 903, 1,065.
2. **Server content back to 2015.** Mirae's page 6 chart gives the yearly growth in GB per server for 2016-2026. We back-cast GB per server from the 2023 anchor of 515 GB. These rows have kind=derived: about 104 GB in 2015, 239 GB in 2018 and 449 GB in 2022.
3. **Cross-checks.** KGI (2025-11-17) puts server bits at 20.74 bn GB in 2026 (+45%) and server share at 47%. That is higher than Mirae's 41%. TrendForce point values (34% in 2020, 37.6% in 2023F) fit the Mirae level.
4. **Server DDR5 share.** No single clean series exists. The best sequence:
   - 1Q23: about 10% (TrendForce).
   - 2023: 13.4% platform adoption (TrendForce).
   - 4Q23: about 25% (industry view in Apacer).
   - 2024: 40% of bits (TrendForce, forecast made in Jul 2024).
   - 1Q25: about 90% of bits (TrendForce report title).

   Treat server DDR5 as about 90% or more from 2025 and about 95% or more in 2026. DDR4 is now a long-life niche.
5. **PC DDR5.** About 20% in 1Q23. It passed DDR4 in 2H24 (TrendForce). We found no published 2025 number in text form; Apacer's chart is an image only.

## Gaps

- **Server units have no single clean series for 2015-2022.** Gartner (11.1M in 2015, 12.11M in 2020) and IDC (13.54M in 2021) are search-summary only. TrendForce gives 13.835M (2023F), 13.654M (2024F) and 14.49M (2025E). Mirae uses 19-22M, which is a different definition. Do not mix the unit bases.
- **AI server versus general-purpose server DRAM content.** Only one value exists: the TrendForce FMS 2024 figure of about 2.1 TB per AI server in 2025. It is search-summary only.
- **Absolute server bits before 2023.** No source gives them directly. Use share x total from the total-DRAM agent's series, or units x content.
- **Server DRAM revenue.** We have quarterly TrendForce points only (1Q25: $10.688B), not a full annual series.
- **Segment-level quarterly contract price rises.** TrendForce puts these in chart images. We have the text-level conventional DRAM numbers for every quarter from 3Q25 to 4Q26, plus server and PC numbers for some quarters.

## Definition conflicts

- **Demand versus supply share.** Mirae and KGI give bit demand. TrendForce gives bit output or supply share. Mirae's server line excludes HBM. TrendForce's "HBM + RDIMM = 51% of bits" includes HBM.
- **DDR5 share measures.** "Adoption rate" (platforms) is not the same as "share of bit shipments". The 2023 figure of 13.4% is adoption, not bits.
- **Server units.** TrendForce counts about 14M "whole servers". Mirae counts about 20M. IDC and Gartner differ again. The 2026 growth forecasts also vary by date: TrendForce gave 4% (Oct 2025), 12.8% (Jan 2026), 13% (Apr 2026) and 17% (Jul 2026). Micron says "high teens".
- **PC units.** IDC counts traditional PCs. Gartner includes Chromebooks and ultramobiles. IDC restated 2022 from 292.3M to about 301.5M. Mirae's PC units (229-246M) are lower than IDC's.

## Recommendation to the modeler

1. Build server bits as **units x GB per unit** on the Mirae basis. Use Mirae units and content for 2023-2027 and the back-cast content for 2015-2022. Calibrate against server share x total DRAM bits from the total-DRAM agent.
2. Model server share of DRAM bits (without HBM) as rising from about 34% in 2020 to about 41% in 2026-2027. Treat KGI's 47% as the high case.
3. Treat DDR5 as about 100% of new server and PC DDR bits from 2026. DDR4 is a small, price-driven tail: about 7% of Micron's output in 2026.
4. For 2027 supply, use the supplier guides:
   - Micron: industry DRAM bits in the low 20s % in 2027 and 2028.
   - SK hynix: DRAM demand it can meet grows mid-20s % in 2027.
   - TrendForce: RDIMM bits +15-20% in 2027; server DRAM plus HBM bits +27% in 2027.

## 2026 / 2027

### Supply versus demand and allocation

- The market is short. TrendForce puts the 2026 DRAM sufficiency at -1% to -2%, and it expects the gap to widen in 2027.
- Fill rates for server orders: below 60% in 4Q25 and 66% in 1Q26 (Samsung Securities). A Tom's Hardware headline says US and Chinese customers got about 70%.
- HBM and RDIMM together take about 51% of DRAM bit supply in 2026 (TrendForce, Aug 2026).
- Server demand runs ahead of RDIMM supply:
  - TrendForce: server CPUs +31% in 2026 and more than 40% in 2027.
  - TrendForce: RDIMM bit supply only +15-20% in 2027.
  - Server DRAM plus HBM bit supply grows 27% in 2027, mostly from fabs that start in 2H27.
- Memory takes a growing share of CSP capex: 47% in 2026 and 68% in 2027 (TrendForce).

### Long-term agreements and prepayments

These are the core of the 2026-2027 supply chain.

- **Micron, Jun 2026:** 16 SCAs covering about 20% of DRAM shipments, with $22B committed, of which $18B is cash.
- **Micron, Sep 2026:**
  - 26 SCAs, more than 35% of revenue through 2030, and about $150B of remaining performance obligations.
  - $32B of customer financial commitments, and $12.7B of cash deposits on the balance sheet.
  - More than 75% of 2027 output is already committed.
- **SK hynix, Oct 2026:** LTAs with 14 customers cover more than 50% of 2027-2028 capacity. SK hynix expects demand to exceed supply through 2030.
- **Effect on prices:**
  - Volume under LTAs gets capped prices.
  - Buyers without LTAs carry most of the rise (TrendForce, Jul 2026).
  - Samsung Securities warns that LTA prices are rarely fixed. A "dual pricing" system appears for urgent orders.

### Prices by quarter

Conventional DRAM contract price change, quarter on quarter (TrendForce text):

| Quarter | Change |
|---|---|
| 3Q25 | +10-15% |
| 4Q25 | +18-23% |
| 1Q26 | +90-95% |
| 2Q26 | +58-63% |
| 3Q26 | +13-18% |
| 4Q26 | +10-15% |

- **Server DRAM:**
  - +3-8% (3Q25), about +90% (1Q26) and +13-18% (3Q26).
  - Cumulative +64% in 2H25.
  - About +270% for 2026 as a whole.
- **PC DRAM:** +8-13% (3Q25) and more than +100% (1Q26).
- **Consumer DDR4:** +85-90% in 3Q25. In July 2025, DDR4 cost more than DDR5 at the same capacity.

Omdia module prices (via IBK), in USD per module:

| Module | 3Q25 | 4Q25 | 1Q26 | 2Q26F | 3Q26F | 4Q26F | 1Q27F | 2Q27F |
|---|---|---|---|---|---|---|---|---|
| 64GB DDR5 RDIMM | 265 | 451 | 766 | 1,035 | 1,086 | 1,119 | 1,130 | 1,130 |
| 32GB DDR4 RDIMM | 131 | 222 | 399 | 531 | – | 574 | – | – |
| 16GB DDR5 PC UDIMM | 45.2 | 72.2 | 122.8 | – | – | 176.0 | – | – |

- The 64GB DDR5 RDIMM series shows the price flattening in 2027.
- An analyst on Micron's Jun 2026 call quoted about $1,500 for a 64GB server module. That is higher than the Omdia figure, likely because it reflects spot or non-LTA pricing.
- Omdia and IBK expect rises to fall to single digits after 3Q26, and prices to stay flat in 2Q27.
- TrendForce says prices keep rising through 2H27.

### DDR4 end of life

- **Dates set in 2025:**
  - Samsung: stopped orders in Jun 2025 and finished shipments in Dec 2025.
  - SK hynix: stopped orders in Oct 2025 and finishes shipments in Apr 2026.
  - Micron: final mainstream shipments in 1Q26.
- **Changes since:**
  - Samsung delayed part of its exit through a non-cancellable contract with a server customer.
  - Micron moved DDR4 and LPDDR4 to Fab 6 (Manassas, 1-alpha). Fab 6 output of these parts grows 4x by 2027, but Micron's total DDR4 and LPDDR4 capacity does not grow.
  - DDR4 falls to about 7% of Micron's output in 2026.
- **Outlook:** TrendForce says DDR4 stays short in 2026. Winbond (search summary) says the gap lasts to 2028 or later. Taiwanese DDR4 additions do not fill the gap. DDR4 prices track DDR5 prices.

### Server shipments

- **Total:** TrendForce says +17% in 2026 and faster in 2027. Micron says high teens in both 2026 and 2027, with traditional servers in the mid-teens in 2026.
- **AI servers:** +32.2% in 2026 and about +36% in 2027 (TrendForce, Oct 2026). AI servers are about 75% of 2026 server revenue ($479B of $639.2B).
- **General-purpose servers:** CSP replacement drives them. KGI expected US CSP general servers to grow 50% in 2026. Micron says content per server grows a little more slowly than planned because memory is short. Rambus sees "de-speccing", meaning fewer GB per module.

### Module supply chain

- **RCD:** Rambus set record product revenue in 3Q26 (about $114M), led by RCDs. It guided more than 30% year-on-year growth for 4Q26. Supply is tight going into 2027.
- **PMIC and BMC lead times:** these lengthened in 2026 (PMIC 35-40 weeks, BMC 21-26 weeks), and they limited server builds (TrendForce, Apr 2026).
- **MRDIMM:** Shipments are still qualification and pre-production in 2026. Rambus expects a shallow ramp on a $600M opportunity. Montage's Gen2 MRDIMM chips are in broad trials, and more platforms adopt them from 2H26 to 2027 (search summary).
- **CXL:** We found no 2026 volume data.

### Effects on PCs

- **IDC:**
  - 2026 shipments -11.3% (Jun 2026), with ASP +17%.
  - 3Q26 actual: 62.7M units, -20.1% year on year.
- **TrendForce, notebooks:**
  - Shipments -9.4% in 2026.
  - Shipments fall by a low-single-digit % in 2027, or by a high-single-digit % if brands pass all costs to buyers.
  - CPU, DRAM and SSD rose from 45% of a $900 notebook's BOM in 1Q25 to 68% in 3Q26. A comparable notebook needs about an 80% price rise to hold margin.
- **Micron:** PC and mobile units may fall by double digits in 2026.
- **PC share of DRAM bits:** this drops to about 8% in 2026 (Mirae 8.0%, KGI 8%).
