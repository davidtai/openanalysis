# Vendor x type DRAM mix: notes

Collected 2026-10-31. Data file: `sources/vendor-mix.csv` (163 rows). Raw downloads: `sources/raw-vendor-mix/dl/`. Text extracts: `sources/raw-vendor-mix/txt/`. Rendered slides: `sources/raw-vendor-mix/img/`. Build script: `tools/build_vendor_mix_csv.py`. Prior check: `tools/vendor_mix_ras_check.py`.

## 1. What we found

No source publishes a full vendor x application bit matrix. TrendForce, Omdia and Counterpoint sell the segment shares (mobile, server, graphics) in paid reports. Their public pages give only rankings. So the matrix must be built from three kinds of evidence:

1. Vendor share of one segment (HBM, SOCAMM2, GDDR, mobile).
2. A vendor's own revenue mix (SK hynix slides, Micron business units, CXMT prospectus, Nanya call).
3. Broker estimates of HBM bits per vendor.

### Strong evidence (company-reported or primary)

| Vendor | Evidence | Basis |
|---|---|---|
| SK hynix | DRAM revenue by application, 7 quarters 2024Q4-2026Q3, measured from the vector chart in the earnings slides. Categories: Server, Mobile, PC, Consumer, Graphics (incl. HBM). | revenue |
| Micron | Business-unit revenue (CMBU, CDBU, MCBU, AEBU) FQ4-25 to FQ4-26; DRAM share of revenue; HBM about USD 2 bn in FQ4-25 (~22% of DRAM revenue); "sole supplier of LPDRAM in the data center" in FY2025. | revenue |
| CXMT | Prospectus: LPDDR series 79/75/83/70/66% of revenue (2022, 2023, 2024, 1H25, 2025); DDR series (DDR4+DDR5) 18/20/13/28/32%. | revenue |
| Nanya | 3Q26 call: DDR5 ~10% of revenue; DDR4+LPDDR4 >60%; AI infrastructure >20%. | revenue |
| Samsung | Calls: HBM share "in line with overall DRAM market share" in 3Q26; HBM sales >3x in 2026; server bit portion at an all-time high in 2Q26 (no number). | qualitative |

SK hynix DRAM revenue by application (% of SK hynix DRAM revenue, measured from slide geometry, +/-0.3 pt):

| Quarter | Server | Graphics incl. HBM | Mobile | PC | Consumer |
|---|---|---|---|---|---|
| 2024Q4 | 33.7 | 42.6 | 11.9 | 9.9 | 2.0 |
| 2025Q2 | 31.0 | 45.4 | 12.1 | 9.8 | 1.8 |
| 2025Q3 | 32.9 | 42.1 | 13.7 | 9.3 | 2.0 |
| 2025Q4 | 36.0 | 34.0 | 15.0 | 12.0 | 3.0 |
| 2026Q1 | 47.7 | 21.8 | 16.4 | 10.2 | 3.9 |
| 2026Q2 | 48.7 | 17.9 | 17.7 | 10.5 | 5.1 |
| 2026Q3 | 55.8 | 15.7 | 13.5 | 9.8 | 5.3 |

The fall of the graphics/HBM share in 2026 is a price effect. Conventional DRAM prices rose about 3x, and HBM prices did not. It is not a fall in HBM bits. Investing.com read the same 3Q26 chart as server 50-55%, mobile 20-25%, graphics 10-15%. Its mobile figure conflicts with the measured 13.5%. Use the measured rows.

### Medium evidence (brokers and trackers, public pages)

- HBM share by vendor, revenue: Counterpoint 2026Q1 SK hynix 58 / Samsung 21 / Micron 21; 2026Q2 50 / 33 / 18.
- HBM share by vendor, bits: Samsung Securities 2025 SKH 58 / Samsung 21 / Micron 21, 2026F 52 / 26 / 22. Daishin 2025 57 / 22 / 21, 2026F 49 / 29 / 19, 2027F 39 / 39 / 18 (China remainder 3-4%). UBS 2027F Samsung 41 / SKH 39. Citi 2027F Samsung 42 / SKH 35 / Micron 22. JPMorgan SKH 60 (2025), 46 (2026), 41 (2027).
- HBM share of each vendor's own DRAM: Mirae Samsung 5.0 / 8.5 / 11.2% of bits (2025-2027), SK hynix 12.7 / 12.9 / 13.1%. LS Samsung 4.0% (2025) and 6.7% (2026). SK Securities SK hynix 13-14% of bits in 4Q24-1Q25.
- SOCAMM2 / server LPDDR share: KIS 2026-27 Samsung 35 / SKH 40 / Micron 25. BNK Samsung 50 / SKH 30 / Micron 20. KB Samsung ~50% of Nvidia demand. Daishin Nvidia AI-CPU DRAM 2026 (~23 bn Gb) Samsung low-to-mid 40s, SKH and Micron high 20s each.
- GDDR: Samsung 70% of GDDR7 in 2025 (TrendForce via Hankyung). All GDDR 2024: SKH 49%, Samsung 41% (source not named).
- Mobile: Omdia Samsung 57.9% of mobile DRAM in 1Q24, 54.8% in 2023. TrendForce 4Q25: "Big Four" Samsung, SK hynix, Micron, CXMT (shares paywalled).

### Weak evidence

- Samsung server share of its own bits: "close to half" in 2Q26 (Goldman via Yonhap). Seen only in a search-tool summary. The page could not be fetched.
- No public number for any vendor's PC DRAM share, server RDIMM share or Samsung application mix.
- Chart-label parses (Samsung Securities, Daishin HBM charts) are marked as weak in the CSV.

### Conflicts kept as separate rows

- Samsung HBM share of own bits 2025: Mirae 5.0% vs LS 4.0%. 2026: Mirae 8.5% vs LS 6.7%.
- SK hynix HBM share of own DRAM revenue 2026: Mirae 30.1% vs the company slide (graphics incl. HBM) 15.7-21.8%. The slide is actual data. Mirae's December 2025 forecast did not include the 2026 price surge.
- SOCAMM2 2026: KIS puts SK hynix first (40%); BNK, KB and Daishin put Samsung first (43-50%).
- HBM 2027: UBS and Daishin show a tie (~39-41% each); Citi shows Samsung ahead (42 vs 35); JPMorgan SKH 41%.

## 2. Recommended prior (bit basis, % of each vendor's own DRAM bits)

Columns match `out/forecast_by_category.csv`: server ECC (RDIMM/MRDIMM), LPDDR (phone, tablet, PC LP, server LP/SOCAMM, auto), client PC (non-LP DDR), HBM, GDDR, other/consumer.

### 2025

| Vendor | Server ECC | LPDDR | Client PC | HBM | GDDR | Other |
|---|---|---|---|---|---|---|
| Samsung | 39 | 46 | 5 | 4.5 | 4.5 | 1 |
| SK hynix | 46 | 26 | 8 | 14.5 | 3 | 2.5 |
| Micron | 34 | 42 | 7 | 8 | 2 | 7 |
| CXMT | 8 | 66 | 14 | 0 | 0 | 12 |
| Nanya + others | 15 | 30 | 10 | 0 | 0 | 45 |

### 2026

| Vendor | Server ECC | LPDDR | Client PC | HBM | GDDR | Other |
|---|---|---|---|---|---|---|
| Samsung | 44 | 38 | 3.5 | 8 | 4 | 2.5 |
| SK hynix | 50 | 22 | 7 | 15.5 | 2.5 | 3 |
| Micron | 40 | 36 | 5 | 10 | 1 | 8 |
| CXMT | 15 | 60 | 13 | 1 | 0 | 11 |
| Nanya + others | 25 | 35 | 15 | 0 | 0 | 25 |

### 2027

| Vendor | Server ECC | LPDDR | Client PC | HBM | GDDR | Other |
|---|---|---|---|---|---|---|
| Samsung | 42 | 36 | 3 | 14 | 3.5 | 1.5 |
| SK hynix | 47 | 25 | 6 | 16 | 2.5 | 3.5 |
| Micron | 38 | 37 | 5 | 13 | 1 | 6 |
| CXMT | 18 | 55 | 12 | 4 | 0 | 11 |
| Nanya + others | 25 | 35 | 15 | 0 | 0 | 25 |

### How each row was set

- **SK hynix.** Start from the slide revenue mix. The "Graphics incl. HBM" bucket is almost all HBM (Mirae: HBM 41% of 2025 DRAM revenue vs graphics 34-45%). Convert HBM to bits with the broker bit shares (12.7-14% in 2025; 13-16% in 2026-27; UBS 17.7 bn Gb of 105 bn Gb in 2026 = 17%). For conventional DRAM, assume bits follow revenue, with a small shift from server to mobile, because server DDR5 had the higher price per bit in 2H25-2026. The slide "Mobile" excludes PC LPDDR, so LPDDR = mobile + part of PC + SOCAMM.
- **Micron.** HBM is ~22% of DRAM revenue in FQ4-25 and ~8% of bits. Data-center DRAM (CMBU + CDBU minus data-center SSD) is ~61-65% of DRAM revenue in FY2026, including HBM and LP server DRAM. Micron was the only data-center LPDRAM supplier in 2025, so LP server bits sit in its LPDDR column. MCBU + AEBU DRAM (mobile, PC, auto, embedded) is the remaining ~35-40%. The split of MCBU between LPDDR and client PC is a judgment.
- **Samsung.** No company disclosure. The row is close to a residual: HBM from Mirae/LS/UBS, GDDR from the 70% GDDR7 share, SOCAMM2 from the 35-50% share range, server from the Goldman "close to half" (2Q26) reading, and LPDDR from its historical mobile lead (Omdia 55-58%, falling as CXMT grows).
- **CXMT.** Revenue: LPDDR 66%, DDR 32% (2025). DDR4 is cheaper per bit than DDR5, so DDR bits are a little above the revenue share. DDR goes to PCs, Chinese servers and consumer goods. HBM starts in 2026 (SemiAnalysis: 1% of HBM wafers in 2025, ~30 kwpm at end-2026).
- **Nanya + others.** Nanya, Winbond, PSMC and smaller Chinese makers. Nanya: DDR4+LPDDR4 >60%, DDR5 ~10%, AI infrastructure >20% of revenue. This row also carries Mirae's "others" residual (14 bn Gb in 2025, 28 in 2026, 32 in 2027). Its mix is unknown.

### Confidence by cell

| | Server ECC | LPDDR | Client PC | HBM | GDDR | Other |
|---|---|---|---|---|---|---|
| Samsung | weak | weak | weak | strong | medium | weak |
| SK hynix | strong | medium | medium | strong | weak | medium |
| Micron | medium | medium | weak | medium | weak | weak |
| CXMT | weak | medium | weak | medium | n/a | weak |
| Nanya + others | weak | weak | weak | n/a | n/a | weak |

## 3. How to fill the matrix

1. **Row sums (vendor totals).** Use Mirae bit production by vendor (`total-dram.csv`). Mirae's industry total (293.1, 352.5, 415.7 bn Gb) differs from our model total (293.1, 363.5, 446.4). Scale each Mirae vendor row by model total / Mirae total. Put Nanya plus Mirae's "others" residual in the Nanya + others row.
2. **Column sums (type totals).** Use the medians in `out/forecast_by_category.csv`. LPDDR = lpddr_mob + lpddr_pclp + lpddr_lps + lpddr_auto.
3. **Seed.** Seed cell = row total x prior share above.
4. **Fit.** Run iterative proportional fitting (RAS): scale rows to the row sums, then columns to the column sums, and repeat until both match. 500 iterations is more than enough.
5. **Pin the strong cells.** Before RAS, fix HBM cells to broker bit shares x HBM total (2025 SKH 57-58 / Samsung 21-22 / Micron 21; 2026 ~50 / 29 / 19 / CXMT 1; 2027 ~39 / 39 / 19 / CXMT 3). Then fit only the free cells to the residual row and column sums. Do the same for LP server (SOCAMM) if the model keeps it as a separate column: 2026 about Samsung 43 / SKH 29 / Micron 28.
6. **Check.** Compare the fitted vendor shares of each column with the segment evidence in the CSV (Samsung GDDR > 50%, Samsung largest in LPDDR, CXMT ~10-15% of LPDDR, SK hynix server share > Samsung's own share of its bits).
7. **Uncertainty.** Run the fit for the p10 and p90 column totals as well. Perturb the weak cells by +/-30% and report the spread.

### Result of the check run (`tools/vendor_mix_ras_check.py`)

The prior is close to the column totals, with two gaps:

- **Other/consumer.** The prior asks for 20, 24 and 27 bn Gb (2025-2027). The model has 11.8, 11.3 and 12.1. RAS cuts "other" by about half in every row. Either the model's "other" bucket is too small (legacy DDR4/DDR3 for TV, networking, industrial at Nanya, Winbond, PSMC and CXMT), or those bits are in the model's PC and server buckets. Check this before you trust the Nanya + others row.
- **Client PC.** The prior asks for 22-28 bn Gb; the model has 18-20. Same cause: legacy DDR4 for PCs is in the vendor evidence but small in the model.

Fitted shares of each column after RAS (no pinning), for reference:

| Year | Column | Samsung | SK hynix | Micron | CXMT | Nanya + others |
|---|---|---|---|---|---|---|
| 2025 | Server ECC | 39.8 | 36.4 | 18.0 | 1.8 | 3.9 |
| 2025 | LPDDR | 41.6 | 18.2 | 19.8 | 13.4 | 7.0 |
| 2025 | HBM | 22.6 | 56.5 | 20.9 | 0 | 0 |
| 2025 | GDDR | 57.2 | 29.6 | 13.2 | 0 | 0 |
| 2026 | Server ECC | 35.8 | 35.9 | 17.7 | 3.2 | 7.3 |
| 2026 | LPDDR | 36.1 | 18.4 | 18.6 | 15.0 | 12.0 |
| 2026 | HBM | 29.2 | 49.9 | 19.9 | 1.0 | 0 |
| 2027 | Server ECC | 35.5 | 35.6 | 17.3 | 4.2 | 7.5 |
| 2027 | LPDDR | 34.0 | 21.1 | 18.8 | 14.3 | 11.7 |
| 2027 | HBM | 38.4 | 39.3 | 19.2 | 3.0 | 0 |

These shares fit the segment evidence: HBM matches the broker bit shares, Samsung leads GDDR and LPDDR, and SK hynix and Samsung split server about evenly.

## 4. Gaps worth buying or asking for

1. TrendForce quarterly mobile DRAM and server DRAM supplier rankings (paid). They fill the Samsung server and LPDDR cells and the CXMT LPDDR cell.
2. TrendForce "Graphics DRAM (GDDR) Market Data" (RP260407FS) for GDDR shares.
3. A Korean broker table of Samsung DRAM bits by application. The SK Securities report of 2026-04-20 has an HBM-in-DRAM chart for both Korean vendors, but no application split.
