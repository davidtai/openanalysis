# DRAM supply chain and market mechanics, 2025 to 2027: notes

Status: DRAFT. Research pass of 2026-10-30. Every number here has a row in `supply-chain.csv` with a URL and a quote.

Scope: prices, inventory, contracts, equipment, China, policy, OEM effects, supplier financials and outlooks. Other files cover bit supply and fabs, server DDR5, HBM/GDDR and LPDDR in depth.

## Timeline of the shortage

- **1Q25.** The market is soft. TrendForce expects conventional DRAM contract prices to fall 8 to 13%. CXMT supply pushes DDR4 spot down. DDR4 8Gb spot is US$1.458 in early February.
- **2Q25.** Prices bottom out. Buyers pull orders forward because of US tariffs. DDR4 contract prices turn up 0 to 5%.
- **3Q25.** The big three announce DDR4 end of life. Consumer DDR4 contract prices jump 40 to 45%. Conventional DRAM rises 10 to 15%.
- **4Q25.** Cloud providers place large extra server orders. TrendForce raises its 4Q25 call three times, from 8 to 13% to 45 to 50%. Supplier inventories are "almost depleted". DDR5 spot rises 307% from early September to mid-November.
- **1Q26.** This is the largest quarterly rise on record. Conventional DRAM contract prices rise about 93 to 98%. PC DRAM prices more than double. OEMs send 5 to 15% price-hike notices after CES. Smartphone brands start to raise prices and cut specs.
- **2Q26.** Prices rise another 58 to 63% (forecast). Cloud providers sign multi-year LTAs. Micron, SK hynix and Samsung take cash deposits and prepayments. Spot prices go flat because buyers stop paying more. Console, Mac and iPad prices rise.
- **3Q26.** Increases slow to 13 to 18%. Consumer demand weakens and LTA price caps take effect. Samsung's DRAM ASP rises about 20%. SK hynix posts an 80% operating margin.
- **4Q26.** TrendForce expects 10 to 15%. Server DRAM stays undersupplied. Suppliers say 2027 will be tighter than 2026.

## Main constraints (all categories)

1. **Cleanroom space.** This is the first limit. Lam says cleanroom space and component supply limit how fast the industry can meet demand. Micron raises FY27 construction capex to bring cleanroom space forward to late 2028 and later. New fabs (Micron ID1 mid-2027, SK hynix Yongin early 2027, Micron Tongluo 2H27) add only a little output in 2027. TrendForce expects material new output in 2028.
2. **Wafer crowding by HBM.** HBM takes about 22% of DRAM wafer input at end-2026 and 30% at end-2027, but only 9 to 13% of bits. Each HBM bit uses more wafer area. This takes supply from conventional DRAM.
3. **Equipment.** WFE grows from the mid-US$150 billion range in 2026 to more than US$200 billion in 2027 (Lam). Korea took 45% of ASML's 1Q26 sales. Samsung secured about 20 EUV tools and SK hynix about 24. Tool lead times for the Korean build-out may also slow logic fabs. Japan makes about 80% of the world's photoresist, so supply of this material is concentrated.
4. **Contracts lock up supply.** SK hynix has LTAs that cover more than 50% of its 2027 to 2028 capacity. Samsung targets 60 to 70% by 2030. Micron has 26 SCAs, worth more than 35% of its revenue through 2030, with US$32 billion in customer commitments. Analysts expect nearly half of global DRAM capacity to be under LTAs by 2027. Less supply is left for spot and short-term buyers, so prices for them move more.
5. **Prepayments fund capacity.** Customers pay cash up front. Micron holds US$12.7 billion in customer deposits. Samsung has prepayments for about one quarter of its contracted volume. SK hynix's deals with Microsoft and Google reportedly include advance payments of 10 to 30% of contract value. TrendForce says suppliers ask CSPs for advance payments, and that this raises CSP capex.
6. **Inventory is near zero.** Suppliers' inventory is at "historic lows". Micron's DIO is 129 days, but that figure includes NAND and end-of-life build-ahead. TrendForce did not publish a weeks-of-inventory number in the releases we read. Only US cloud providers built DRAM stock in 2Q26, because a CPU shortage delayed server builds.
7. **Policy.** The US Section 232 tariff (25% from 2026-01-15) covers a narrow set of advanced computing chips. The proclamation text does not name memory. US HBM export controls (December 2024) and the end of the China fab tool waivers (September 2025) limit growth at Samsung's and SK hynix's China fabs. They get yearly approval only to run existing lines. CXMT is on the 1260H list. It is ramping DDR5 and LPDDR5X, and its HBM3E yield is 20 to 30%.

## By category

### Server ECC (RDIMM, MRDIMM)

- **Constraints.** Suppliers put server DDR5 first. In 1Q26, the wafer revenue of a 64GB RDIMM was higher than HBM's. Server DRAM rises about 270% in 2026. US cloud providers pay LTA prices with caps. Buyers without an LTA pay the increases. Module spot for a 32GB DDR5 RDIMM is about US$2,165 (about US$68 per GB). That is about 4.5 times the per-GB spot price of client DDR5. Buyers cut module sizes from 96/128GB to 32/64GB.
- **2027.** RDIMM bit supply grows only 15 to 20%, while server CPU shipments grow more than 40%. TrendForce expects server DRAM prices to rise each quarter through 2H27.

### DDR5 (client)

- **Constraints.** PC DRAM more than doubled in 1Q26. CPU, DRAM and SSD were 45% of a US$900 notebook's BOM in 1Q25 and 68% in 3Q26. To keep its margin, a brand would need to raise prices by about 80%. The contract price for a DDR5 8GB SO-DIMM is US$133 (about US$16.6 per GB). DDR5 16Gb spot is US$61.50, about 12 times the March 2025 level.
- **2027.** PC DRAM supply could fall as capacity moves to servers. Notebook shipments fall by a low single-digit percentage. If brands pass costs on, the fall is high single digits.

### HBM

- **Constraints.** The HBM3e premium over DDR5 falls from more than 4 times to 1 to 2 times by end-2026. CXMT is years behind on HBM.
- **2027.** HBM contract prices rise 70 to 140%, and blended HBM ASP rises 121%. Bits grow 50 to 60%, which is still short of demand. Samsung says its 2027 HBM supply is sold out.

### GDDR

- **Constraints.** We found few figures. GDDR6 fell 3 to 8% in 2Q25. NVIDIA reportedly delayed the RTX 50 Refresh because of graphics memory cost.
- **2027.** We found no figure in this pass.

### LPDDR

- **Constraints.** Memory went from 10 to 15% of smartphone BOM to 30 to 40%. Low-end phones go back to 4GB. The iPhone 18 costs 10 to 20% more. Samsung's phone unit made its first loss in 2Q26. Smartphone memory prices rose only 5 to 10% in 3Q26 (Counterpoint).
- **2027.** NVIDIA expects LPDDR5X to stay tight through 2027. Counterpoint expects smaller price swings in 2027.

### DDR4 and legacy

- **Constraints.** End of life at the big three drove the turn. DDR4 8Gb spot went from US$1.458 (February 2025) to US$46.357 (October 2026), about 32 times. DDR4 16Gb spot (US$82.80) is above DDR5 16Gb spot (US$61.50). Buyers move down to DDR3 and DDR2. DDR2 rose 55 to 60% in 2Q26.
- **2027.** Nanya and Winbond have pricing power. CXMT DDR4 supply is the main thing that could ease prices.

## 2027: consensus and disagreement

**Consensus.** All three suppliers, TrendForce and Micron say 2027 is tighter than 2026. New cleanroom space adds material output only in 2028. Industry DRAM bits grow in the low 20s percent (Micron). Price increases slow but do not reverse. Contract prices stay high through 2027.

**Disagreement.**
- *How long the shortage lasts.* Samsung says through 2028. SK hynix says through 2030. Lenovo calls high prices a "new normal" into 2030. Micron has "no line of sight" to balance.
- *How fast prices rise.* TrendForce sees slower quarterly increases, and LTA price caps limit the gains. Xbox expects memory prices to double again by fall 2027.
- *Size of the market.* In January 2026, TrendForce put the 2027 memory market at US$842.7 billion. A May 2026 headline says US$1.28 trillion.
- *Demand risk.* TrendForce and Counterpoint expect phone and notebook volumes to fall again in 2027. Suppliers do not see demand as a risk.

## Gaps in this pass

- The web search budget ran out early. We fetched only known primary pages.
- **Not found:** TrendForce weeks-of-inventory figures; DRAM-only WFE figures from SEMI, Applied or TEL (their sites blocked the fetch); ASML EUV shipment counts to DRAM makers; Morgan Stanley, Goldman Sachs and Bernstein 2027 views; CXMT's 2026 IPO status and wafer capacity; neon supply; Korean, Japanese and US subsidy amounts.
- Samsung's newsroom timed out. Samsung figures come from TrendForce news items that cite Reuters and the Samsung earnings deck.
- Most TrendForce category figures (2Q26 and later) are in chart images, so we could not read them. Only the text figures are in the CSV.
