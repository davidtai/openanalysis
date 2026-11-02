# GPU memory (HBM and GDDR): source notes

Data: `hbm-gddr.csv` (296 rows). Builder: `../tools/build_hbm_gddr_csv.py`.
Collected 2026-10-30. Every row has a URL and a quote. Rows marked "Search-result snippet only" in `notes` were not fetched verbatim. Check them before you quote them in public.

## Units

- 1 GB = 8 Gb. 1 EB = 10^9 GB = 8 billion Gb.
- "kwpm" = thousand 300 mm wafers per month.
- TrendForce, UBS and Mirae report HBM bits in "billion Gb". Use that unit in the model.

## Best HBM bit series

No single public source gives a full 2018-2030 HBM bit series. Build it from these anchors:

| Year | HBM bits (billion Gb) | Source and kind |
|---|---|---|
| 2022 | ~1.45 | Derived from TrendForce 2023 demand / 1.6 |
| 2023 | 2.32 | TrendForce demand, 290 million GB |
| 2024 | ~9.5-11 | Greenberg/Yole 1,182 million GB; Mirae Samsung 5.1 + SK hynix 6.1 (Micron not included) |
| 2025 | 17.5-23 | UBS implied 17.5; TrendForce 8% x Mirae total supply = 23.4 |
| 2026 | 30-33 | TrendForce >30; UBS 32.9; TrendForce 9% share x Mirae supply = 31.7 |
| 2027 | 48-58 | TrendForce +50-60% on 2026; UBS 58.0; TrendForce 13% share = 54 |

Use the TrendForce bit-share series (8% / 9% / 13% for 2025-2027) times the total-DRAM series from the other agent. Then check the result against UBS (17.5 / 32.9 / 58.0) and the vendor sums. Before 2022, HBM was under about 1% of DRAM bits. No good public numbers exist for 2018-2021.

## Best HBM revenue series

- Actual and near-actual: 2022 ~$2.1B, 2023 $4-5.5B, 2024 $16-17B, 2025 ~$34-35B (TrendForce derived, BI, Yole, Micron).
- Forecasts: Micron says the TAM goes past $100B in 2027. Goldman Sachs: $56B (2026), $116B (2027), $168B (2028). Yole: $98B in 2030. SK hynix: about +30% a year to 2030.
- Revenue grows faster than bits in 2027. TrendForce expects the blended ASP to rise 121%. Do not turn revenue into bits with a fixed price.

## Best GDDR series

- No public GDDR-only bit series exists. TrendForce keeps the GDDR6/GDDR7 split in paid reports.
- Mirae (citing its own model) gives "graphics DRAM" = HBM + GDDR: 11.2 / 18.5 / 30.4 / 46.1 / 64.7 billion Gb for 2023-2027.
- GDDR = graphics minus HBM. This gives about 9 billion Gb in 2023 and about 13-16 in 2026. The result is noisy because the two terms come from different sources.
- Unit check: JPR add-in-board shipments were 44.3 million in 2025 (sum of quarters). JPR expects about -10% in 2026. Gaming GDDR volume is flat to down. Growth in GDDR7 bits comes from AI and workstation cards (RTX PRO 6000 at 96 GB).

## Definition conflicts

1. Bits vs wafers vs revenue. HBM was 8% of DRAM bits but 18% of wafer input in 2025 (TrendForce). Some articles say "share of DRAM" without the basis. Keep them apart.
2. Demand vs supply. TrendForce gives both demand growth and supply growth, and they differ (for example 2024: demand ~200%, supply 260%).
3. "Graphics DRAM" includes HBM in Mirae and TrendForce application splits. Do not add HBM and graphics.
4. GPU counts. Nvidia counts Blackwell and Rubin by die (2 per package) in some statements. Use packages for HBM content.
5. TSV capacity vs wafer input. TrendForce FMS capacity (450 kwpm top-3, end-2026) is above its 22% wafer-input share. Capacity is not full use.
6. Old forecasts are often far too low (Yole 2024: HBM 6% of bits in 2029; TrendForce 2023: HBM revenue $8.9B in 2024). Weight recent sources.

## Gaps

- No verbatim TrendForce wafer table by vendor for 2025-2026. The FMS 2025 PDF returned 403. Values come from a search summary.
- No public Micron HBM bit numbers. Micron stopped giving HBM revenue in 2026.
- No GDDR-only bit data, no average VRAM per card from JPR.
- No 2018-2021 HBM bit or revenue numbers I could cite.
- Morgan Stanley HBM TAM numbers seen only in weak secondary sources. Not included.
- The web search budget ran out during the 2026/2027 pass. Some planned checks were not done (Micron FQ4 2026 HBM detail, SK hynix capacity by year, AMD unit counts).

## Recommendation to the modeler

1. Model HBM as a share of DRAM bits, driven by HBM wafer share and the trade ratio. Bit share = wafer share / trade ratio, scaled for the all-DRAM mix. TrendForce implies a ratio of about 2.3 vs the DRAM average (18%/8%, 22%/9%, 30%/13%).
2. Anchor 2023-2027 on the table above. Treat 2028-2030 as a scenario band: HBM wafer share 30-35%, trade ratio 3-4x vs DDR5 (Micron: rises with HBM4E).
3. Model GDDR as graphics (Mirae) minus HBM, and show a wide band. GDDR is 3-5% of DRAM bits. Its error does not move the total much.
4. Use the accelerator bottom-up only as a check. It explains about 60-70% of the top-down HBM bits in 2026. The rest is yield loss, inventory, ASICs not listed, and China parts.

## 2026 / 2027

### HBM production by vendor in 2026

- SK hynix: largest supplier. TrendForce expects it to keep a "dominant share" of 2026 bits. UBS: 48% of 2026 bits. HBM4 mass shipments began in 2Q26. M15X (about 50 kwpm at full use) goes to maximum capacity by end-2026. HBM4 passes HBM3E in volume and revenue in 4Q26. TSV capacity about 200 kwpm at end-2026 (TrendForce FMS, snippet).
- Samsung: first commercial HBM4 shipments in February 2026. HBM4 yield went from under 60% to about 80% by August (press, not Samsung). HBM4 was 60% of its HBM revenue in 3Q26. Samsung is the primary HBM4 supplier for AMD MI455X (MOU). Counterpoint: Samsung HBM revenue share rose to 33% in 2Q26. TSV capacity about 150 kwpm (TrendForce FMS) or a move to 250 kwpm by end-2026 (KB Securities). These two disagree.
- Micron: HBM4 36 GB 12-high in volume from CQ1-CQ2 2026. HBM4 12-high ramp is faster than HBM3E 12-high was. HBM share is about equal to its DRAM share (about 20%). Singapore HBM fab ramps in 2027. TSV capacity about 100 kwpm at end-2026 (snippet).
- CXMT: about 5 kwpm HBM at end-2025, about 30 at end-2026, 55 at end-2027 (SemiAnalysis). HBM3 yields about 25%. Not a factor for Nvidia or AMD.
- Mix: HBM3E was the main product in 1H26 because Nvidia raised B300/GB300 orders. HBM4 became the main product in 2H26.
- Qualification: TrendForce expected all three vendors to finish Nvidia HBM4 validation in 2Q26. Nvidia began Vera Rubin production shipments in August 2026.

### Sold-out status and prices

- 2026: Micron, SK hynix and Samsung all sold out. Contracts were annual and set in 2025.
- 2027: Samsung "sold out" (Oct 2026). Micron has contracted "the bulk" of 2027 bits at "significantly" higher prices. SK hynix says DRAM and HBM are "essentially sold out through 2029", with LTAs covering more than 50% of capacity for 2027 and 2028.
- Prices: HBM4 12-high 36 GB is about $600 per stack in 2026 and about $1,300 in 2027 (industry estimates). That is about $2.1/Gb going to $4.5/Gb. TrendForce: blended ASP +121% in 2027. Reason: annual HBM contracts lagged the quarterly DRAM price spike. HBM was less profitable than DDR5 64 GB RDIMM from 1Q26.

### Packaging

- TSMC CoWoS: about 75 kwpm at end-2025, 120-140 kwpm in 2026, 190-200 kwpm at end-2027 (J.P. Morgan). OSATs add 50-60 kwpm. The CoWoS gap falls from about 20% to about 10% by end-2026.
- Nvidia needs about 595k CoWoS wafers in 2026, 60% of the total (Morgan Stanley, July 2025).
- HBM4 base dies: SK hynix uses TSMC (12 nm class). Samsung uses its own 4 nm. Micron uses its own die for HBM4 and TSMC for HBM4E.
- Bonders: HBM4 uses TC bonders. SK hynix splits orders among ASMPT, Hanmi and Hanwha. Hybrid bonding is expected for HBM4E 16-high or HBM5, not for volume HBM4.
- Packaging is no longer the main limit in 2027. Memory wafers are. Nvidia says supply stays a bottleneck at least to end of fiscal 2028 (January 2028).

### Accelerators and HBM need

- Nvidia 2026: about 5.4 million packages (Morgan Stanley, 2025 view). Blackwell is about 71% of high-end shipments, Rubin about 22% (TrendForce, April 2026). Bottom-up need: about 10-12 billion Gb.
- Google TPU: 4.13 million in 2026, 9.87 million in 2027 (UBS).
- AWS Trainium3: 1.8 million in 2026, 2.8 million in 2027 (UBS).
- AMD MI450/MI455X (432 GB HBM4): ramp starts end of 3Q26, big steps in 4Q26 and 1Q27. No unit counts.
- TPU + Trainium3 bottom-up: about 8.4 billion Gb in 2026.
- 2027: HBM bits +50-60% (TrendForce) or +76% (UBS). Nvidia is looking at smaller HBM for Rubin Ultra (8-Hi or HBM4 instead of 12-Hi HBM4E). UBS cut its Rubin Ultra assumption from 1 TB to 768 GB. Watch this. It is the largest single swing in 2027 HBM GB.

### GDDR7 in 2026

- Supply is tight. Suppliers are leaving GDDR6. Micron dropped 2 GB GDDR7 for gaming and moved to 3 GB parts for AI. TrendForce: GDDR7 demand comes mostly from AI chips. Graphics DRAM prices keep rising in 4Q26.
- Effect on cards: Nvidia cut RTX 50 supply to partners by 15-20% in January 2026 (leak). Average RTX 50 prices rose 19% in three months. Newegg medians rose up to 39%. JPR expects about -10% AIB units in 2026.
- Rubin CPX (128 GB GDDR7) was removed from Nvidia's roadmap at GTC 2026 (March). Do not count CPX GDDR7 demand in 2026-2027. RTX PRO 6000 (96 GB GDDR7) carries the AI GDDR7 demand instead.

### Standard DRAM wafers taken by HBM

- HBM share of DRAM wafers: 18% (end-2025), about 20-22% (2026), about 30% (2027). Sources: TrendForce, Samsung (Oct 2026), Applied Materials (15% in March 2026).
- In wafers: about 480 kwpm of HBM/TSV capacity at end-2026 (all vendors). At a 3:1 trade ratio, that removes the bit output of about 320 kwpm of standard DRAM.
- 2027: about 525 kwpm (30% of top-3 capacity). At 3:1 it removes about 350 kwpm-equivalent. HBM4E has a higher ratio (Micron: "increasing trade ratio"), so the loss is larger.
- New fabs do not add much before mid-2027 (Micron Idaho first wafers) or 2028 (SK hynix, Samsung P5). So in 2027 HBM growth comes mostly from standard DRAM. This is the main reason standard DRAM stays short in 2027.
