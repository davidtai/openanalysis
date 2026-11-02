"""Build sources/supply-chain.csv from the rows below.

Every row was read from a fetched page on 2026-10-30. Quotes are the
excerpts that the fetch returned. Derived rows show the formula in notes.
"""
import csv
import os
import sys

HEADER = ["segment", "metric", "period", "value", "unit", "kind", "publisher",
          "title", "url", "pub_date", "quote", "notes"]

TF = "TrendForce"
TFP = "https://www.trendforce.com/presscenter/news/"
TFN = "https://www.trendforce.com/news/"

# Reused sources: (publisher, title, url, pub_date)
S = {
    "tf_1q25": (TF, "Passive Buyer Strategies Drive DRAM Contract Prices Down Across the Board in 1Q25", TFP + "20241230-12424.html", "2024-12-30"),
    "tf_2q25": (TF, "Downstream Inventory Reduction Eases DRAM Price Decline in 2Q25", TFP + "20250325-12528.html", "2025-03-25"),
    "tf_3q25": (TF, "Transition between DRAM Generations Drives Diverging 3Q25 Price Trends; Consumer DDR4 Prices Expected to Surge Over 40%", TFP + "20250707-12633.html", "2025-07-07"),
    "tf_4q25a": (TF, "DRAM Prices to Continue Rising in 4Q25, Server Demand Surges Ahead While Legacy Process Products See Steeper Increases", TFP + "20250924-12733.html", "2025-09-24"),
    "tf_4q25b": (TF, "Tight DRAM Supply to Boost DDR5 Contract Prices; Profitability in 2026 Expected to Surpass HBM3e", TFP + "20251029-12758.html", "2025-10-29"),
    "tf_rev3q25": (TF, "Global DRAM Revenue Jumps 30.9% in 3Q25, Micron's Market Share Climbs by 3.7 Percentage Points", TFP + "20251126-12802.html", "2025-11-26"),
    "tf_ddr5hbm": (TF, "Higher DDR5 Profitability Intensifies Capacity Crowding, Strengthening HBM3e Pricing Momentum in 2026", TFP + "20251218-12843.html", "2025-12-18"),
    "tf_oem1q26": (TF, "Memory Price Surge to Persist in 1Q26; Smartphone and Notebook Brands Begin Raising Prices and Downgrading Specs", TFP + "20251211-12831.html", "2025-12-11"),
    "tf_console": (TF, "Memory Price Surge Squeezes Game Console Margins; 2026 Shipment Forecast Revised Downward", TFP + "20251202-12811.html", "2025-12-02"),
    "tf_1q26a": (TF, "Memory Makers Prioritize Server Applications, Driving Across-the-Board Price Increases in 1Q26", TFP + "20260105-12860.html", "2026-01-05"),
    "tf_tongluo": (TF, "Micron's Acquisition of PSMC's Tongluo Fab Could Lift Global DRAM Supply Outlook in 2027", TFP + "20260119-12883.html", "2026-01-19"),
    "tf_memrev": (TF, "AI Architecture Evolution Set to Drive Memory Market Revenue to a New Peak in 2027, with Annual Growth Exceeding 50%", TFP + "20260122-12893.html", "2026-01-22"),
    "tf_1q26b": (TF, "Memory Price Outlook for 1Q26 Sharply Upgraded", TFP + "20260202-12911.html", "2026-02-02"),
    "tf_phone": (TF, "Memory Price Surge Intensifies Retail Pricing Pressure, Putting Global Smartphone Production at Risk of a Sharp Decline", TFP + "20260211-12922.html", "2026-02-11"),
    "tf_rev4q25": (TF, "Price Rally Drives 4Q25 DRAM Revenue Up 29.4%; Samsung Regains No. 1 Market Share", TFP + "20260226-12937.html", "2026-02-26"),
    "tf_nb40": (TF, "Rising Memory and CPU Prices Could Push Mainstream Notebook Prices Up by Nearly 40%", TFP + "20260310-12959.html", "2026-03-10"),
    "tf_2q26": (TF, "AI Server Demand to Drive Memory Contract Price Increases in 2Q26 as CSPs Secure Supply via Long-Term Agreements", TFP + "20260331-12995.html", "2026-03-31"),
    "tf_rev1q26": (TF, "Rapid Contract Price Surge Drives 1Q26 DRAM Industry Up 81% QoQ", TFP + "20260601-13070.html", "2026-06-01"),
    "tf_hbm27a": (TF, "Tight DRAM Supply Gives Suppliers Greater Pricing Power in HBM; HBM Contract Prices Expected to Surge Multiples Higher in 2027", TFP + "20260602-13074.html", "2026-06-02"),
    "tf_ddr2": (TF, "Consumer DRAM Shortages Extend to DDR2 Products with Contract Prices Expected to Continue Rising in 3Q26", TFP + "20260622-13112.html", "2026-06-22"),
    "tf_3q26": (TF, "AI Server Demand Continues to Support Memory Prices in 3Q26, but Gains Moderate as Consumer Demand Weakens and High Base Effects Take Hold", TFP + "20260703-13134.html", "2026-07-03"),
    "tf_srv3q26": (TF, "Long-Term Agreements Cap Price Increases; Server DRAM Contract Prices Expected to Rise 13-18% QoQ in 3Q26", TFP + "20260709-13140.html", "2026-07-09"),
    "tf_2027": (TF, "Diverging Memory Market Outlook in 2027 as DRAM Supply Remains Tight While NAND Flash Supply Conditions Ease", TFP + "20260730-13158.html", "2026-07-30"),
    "tf_rubin": (TF, "DRAM Supply to Remain Tight in 2027, Prompting NVIDIA to Lower HBM Configurations for Rubin Ultra", TFP + "20260804-13166.html", "2026-08-04"),
    "tf_ip18pro": (TF, "iPhone 18 Pro BOM Cost Expected to Surge Nearly 40%, Leaving Apple to Sacrifice Margins to Sustain Shipments", TFP + "20260810-13172.html", "2026-08-10"),
    "tf_cspmem": (TF, "Memory Prices Soar; DRAM and NAND Flash to Account for 68% of Major CSP CapEx in 2027", TFP + "20260825-13198.html", "2026-08-25"),
    "tf_ip18": (TF, "Memory Costs Drive Up iPhone 18 Series BOM; AI and Pricing to Shape Upgrade Demand", TFP + "20260903-13213.html", "2026-09-03"),
    "tf_nb26": (TF, "Improved CPU Supply Narrows 2026 Global Notebook Shipment Decline to 9.4%, but Brands Still Face Heavy Cost Pressure", TFP + "20260904-13217.html", "2026-09-04"),
    "tf_rev2q26": (TF, "DRAM Industry Revenue Rises 59.5% QoQ in 2Q26 as Supply Expansion Continues to Lag Demand Growth", TFP + "20260907-13219.html", "2026-09-07"),
    "tf_hbm27b": (TF, "HBM Supply Constraints Persist, 2027 Price Outlook Revised Upward with Blended ASP Forecast to Rise 121% YoY", TFP + "20260929-13255.html", "2026-09-29"),
    "tf_4q26": (TF, "AI Server Demand Sustains Memory Contract Price Increases in 4Q26, While Consumer-Side Pressure Persists", TFP + "20260930-13258.html", "2026-09-30"),
    "tf_nb27": (TF, "Rising Costs Threaten Notebook Demand in 2027, Raising Risks of Shipment Declines and Price Increases", TFP + "20261008-13264.html", "2026-10-08"),
    "tf_cspcapex": (TF, "CSP CapEx Projected to Exceed US$1.5 Trillion in 2027, with AI Server Revenue Growing Over 90% YoY", TFP + "20261014-13269.html", "2026-10-14"),
    "tf_contract_page": (TF, "DRAM Contract Price (price page, 2H Sep 2026)", "https://www.trendforce.com/price/dram/dram_contract", "2026-09-30"),
    "tf_spot_page": (TF, "DRAM Spot Price (DRAMeXchange price page)", "https://www.trendforce.com/price/dram/dram_spot", "2026-10-30"),
    "dx_home": ("TrendForce DRAMeXchange", "DRAMeXchange home page: Module Spot Price", "https://www.dramexchange.com/", "2026-10-26"),
    "sp_250205": (TF, "Memory Spot Price Update: DDR4 Prices Continue to Slide Due to CXMT's Abundant Supply", TFN + "2025/02/05/insights-memory-spot-price-update-ddr4-prices-continue-to-slide-due-to-cxmts-abundant-supply/", "2025-02-05"),
    "sp_250319": (TF, "Memory Spot Price Update: DDR4 & DDR3 Prices Rise Amid Strong DDR5 Rebound Led by SK hynix", TFN + "2025/03/19/insights-memory-spot-price-update-ddr4-ddr3-prices-rise-amid-strong-ddr5-rebound-led-by-sk-hynix/", "2025-03-19"),
    "sp_250924": (TF, "Memory Spot Price Update: DDR4 Drives DRAM Price Rally, Mainstream Chips Surge 6.88% This Week", TFN + "2025/09/24/insights-memory-spot-price-update-ddr4-drives-dram-price-rally-mainstream-chips-surge-6-88-this-week/", "2025-09-24"),
    "sp_251119": (TF, "Memory Spot Price Update: DDR5 Prices Up 307% Since September as Module Costs Poised to Surge", TFN + "2025/11/19/insights-memory-spot-price-update-ddr5-prices-up-307-since-september-as-module-costs-poised-to-surge/", "2025-11-19"),
    "sp_251231": (TF, "Memory Spot Price Update: DDR4 Spot Prices Climb as Samsung Holds EOL Line", TFN + "2025/12/31/insights-memory-spot-price-update-ddr4-spot-prices-climb-as-samsung-holds-eol-line", "2025-12-31"),
    "sp_260401": (TF, "Memory Spot Price Update: DDR3 Strength Contrasts Weak DDR4/DDR5 Amid High Prices, Soft Demand", TFN + "2026/04/01/insights-memory-spot-price-update-ddr3-strength-contrasts-weak-ddr4-and-ddr5-amid-high-prices-and-soft-demand/", "2026-04-01"),
    "sp_260617": (TF, "Memory Spot Price Update: DDR3 Strengthens While DDR4 Faces Constraints and Spec Downgrading", TFN + "2026/06/17/insights-memory-spot-price-update-ddr3-strengthens-while-ddr4-faces-constraints-and-spec-downgrading/", "2026-06-17"),
    "sp_260729": (TF, "Memory Spot Price Update: DRAM Spot Prices Rise Slightly as DDR3, DDR4 and DDR5 Inquiries Pick Up", TFN + "2026/07/29/insights-memory-spot-price-update-dram-spot-prices-rise-slightly-as-ddr3-ddr4-and-ddr5-inquiries-pick-up/", "2026-07-29"),
    "sp_261021": (TF, "Memory Spot Price Update: DDR5 Supply Tight, DDR4 Trading Subdued Despite 0.84% Gain in Mainstream Prices", TFN + "2026/10/21/insights-memory-spot-price-update-ddr5-supply-tight-ddr4-trading-subdued-despite-0-84-gain-in-mainstream-prices", "2026-10-21"),
    "mu_fq4": ("Micron", "Fiscal Q4 2026 Earnings Call Prepared Remarks", "https://s25.q4cdn.com/621799436/files/doc_financials/2026/q4/Q4-FY26-Prepared-Remarks.pdf", "2026-09-30"),
    "mu_fq4pr": ("Micron", "Micron Technology, Inc. Reports Record Fiscal Fourth Quarter and Full Year 2026 Results", "http://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results", "2026-09-30"),
    "mu_fq3": (TF, "Micron Profit Surges 15-Fold as Margin Nears 85%; HBM4 Revenue Exceeds $1B", TFN + "2026/06/25/news-micron-profit-surges-15-fold-as-margin-nears-85-hbm4-revenue-exceeds-1b/", "2026-06-25"),
    "mu_sca": (TF, "Decoding Micron's SCAs: Reportedly 20% of DRAM Output, Toward 50% of Long-Term Memory Revenue", TFN + "2026/06/25/news-decoding-microns-scas-reportedly-20-of-dram-output-toward-50-of-long-term-memory-revenue/", "2026-06-25"),
    "hx_1q26": ("SK hynix", "SK hynix Announces 1Q26 Financial Results", "https://news.skhynix.com/en/q1-2026-business-results/", "2026-04-23"),
    "hx_2q26": ("SK hynix", "SK hynix Announces 2Q26 Financial Results", "https://news.skhynix.com/en/q2-2026-business-results/", "2026-07-29"),
    "hx_3q26": ("SK hynix", "SK hynix Announces 3Q26 Financial Results", "https://news.skhynix.com/en/q3-2026-business-results/", "2026-10-28"),
    "ss_2q26": (TF, "Samsung's DS Unit Delivers 99.7% of Q2 Profit amid Memory Boom; HBM4 Revenue Reportedly to Triple in Q3", TFN + "2026/07/30/news-samsungs-ds-unit-delivers-99-7-of-q2-profit-amid-memory-boom-hbm4-revenue-reportedly-to-triple-in-q3/", "2026-07-30"),
    "ss_lta": (TF, "Samsung Targets 60-70% Capacity Under LTAs; Five Key Customers Reportedly Include AWS, Microsoft, Google", TFN + "2026/07/30/news-samsung-targets-60-70-capacity-under-ltas-five-key-customers-reportedly-include-aws-microsoft-google/", "2026-07-30"),
    "ss_3q26": (TF, "Samsung Says HBM Share Matches DRAM Standing as HBM4 Sales Triple; DS Margin Hits 72%, 10 LTA Clients Signed", TFN + "2026/10/29/news-samsung-says-hbm-share-matches-dram-standing-as-hbm4-sales-triple-ds-margin-hits-72-10-lta-clients-signed/", "2026-10-29"),
    "lam_slides": ("Lam Research", "September Quarter 2026 (Q1 FY2027) earnings slides", "https://filecache.investorroom.com/mr5ir_lamresearch2/1519/Q1_2027-slides-full_final.pdf", "2026-10-21"),
    "lam_pr": ("Lam Research", "Lam Research Corporation Reports Financial Results for the Quarter Ended September 27, 2026", "https://filecache.investorroom.com/mr5ir_lamresearch2/1524/LRCX_Exhibit_99.1_Q1_2027%2010212026%20.pdf", "2026-10-21"),
    "asml": (TF, "ASML Raises 2026 Sales Outlook to EUR36B-EUR40B on Memory, Logic Demand; South Korea Share Hits 45%", TFN + "2026/04/15/news-asml-raises-2026-sales-outlook-to-e36b-e40b-on-memory-and-logic-client-demand-south-korea-share-hits-45/", "2026-04-15"),
    "kr800": (TF, "Samsung, SK hynix 800 Trillion Won Expansion Strains Chipmaking Tool Supply, Potentially Pressures TSMC, Intel", TFN + "2026/06/30/news-samsung-sk-hynix-800-trillion-won-expansion-strains-chipmaking-tool-supply-potentially-pressures-tsmc-and-intel/", "2026-06-30"),
    "jsr": (TF, "JSR Reportedly Plans First Taiwan Production Plant to Supply Advanced EUV Photoresists to TSMC", TFN + "2026/05/05/news-jsr-reportedly-plans-first-taiwan-production-plant-to-supply-advanced-euv-photoresists-to-tsmc/", "2026-05-05"),
    "cx_ipo": (TF, "CXMT Confirms LPDDR5X Mass Production Began in May, High-speed Variant Under Customer Trials", TFN + "2025/10/29/news-cxmt-confirms-lpddr5x-mass-production-began-in-may-high-speed-variant-under-customer-trials/", "2025-10-29"),
    "cx_ipo0": (TF, "China's CXMT Reportedly Begins IPO Counselling, Aims to Be First Memory Chip Firm on A-Share", TFN + "2025/07/08/news-chinas-cxmt-reportedly-begins-ipo-counselling-aims-to-be-first-memory-chip-firm-on-a-share/", "2025-07-08"),
    "cx_hbm": (TF, "CXMT Reportedly Ships HBM3E Samples, Eyes Production Within 2 Months Despite 20-30% Yields", TFN + "2026/10/28/news-cxmt-reportedly-ships-hbm3e-samples-eyes-production-within-2-months-despite-20-30-yields/", "2026-10-28"),
    "cx_share": (TF, "Chinese Memory Makers, Led by CXMT, Advance in the DRAM Market, Challenging Samsung, SK Hynix, and Micron", TFN + "2025/01/16/news-chinese-memory-makers-led-by-cxmt-advance-in-the-dram-market-challenging-samsung-sk-hynix-and-micron/", "2025-01-16"),
    "cx_1260h": (TF, "U.S. Adds Tech Giants CXMT, Tencent, and CATL to List of Chinese Firms Linked to Military Support", TFN + "2025/01/07/news-u-s-adds-tech-giants-cxmt-tencent-and-catl-to-list-of-chinese-firms-linked-to-military-support/", "2025-01-07"),
    "bis": ("US Commerce BIS", "Commerce Strengthens Export Controls to Restrict China's Capability to Produce Advanced Semiconductors for Military Applications", "https://www.bis.gov/press-release/commerce-strengthens-export-controls-restrict-chinas-capability-produce-advanced-semiconductors-military", "2024-12-02"),
    "veu": (TF, "SK hynix Reportedly Seeks U.S. Chip Tool Approval for China Expansion to Fund Potential U.S. NAND Fab", TFN + "2026/10/15/news-sk-hynix-reportedly-seeks-u-s-chip-tool-approval-for-china-expansion-to-fund-potential-u-s-nand-fab/", "2026-10-15"),
    "s232": ("The White House", "Adjusting Imports of Semiconductors, Semiconductor Manufacturing Equipment, and Their Derivative Products into the United States", "https://www.whitehouse.gov/presidential-actions/2026/01/adjusting-imports-of-semiconductors-semiconductor-manufacturing-equipment-and-their-derivative-products-into-the-united-states/", "2026-01-14"),
    "tw20": (TF, "U.S. Slaps 20% Tariff on Taiwan: Foundries Unscathed, Downstream Burned; Section 232 Looms", TFN + "2025/08/01/news-u-s-slaps-20-tariff-on-taiwan-foundries-unscathed-downstream-takes-the-heat-section-232-looms/", "2025-08-01"),
    "suit": (TF, "Samsung, SK hynix, Micron Face U.S. Class-Action Lawsuit Over Alleged DRAM Supply Manipulation", TFN + "2026/06/29/news-samsung-sk-hynix-micron-face-u-s-class-action-lawsuit-over-alleged-dram-supply-manipulation/", "2026-06-29"),
    "xbox": (TF, "Apple Price Hikes Erode Neo's Cost Edge as Xbox Cites 2.5x Memory Surge for New Increase", TFN + "2026/06/26/news-apple-price-hikes-erode-neos-cost-edge-as-xbox-cites-2-5x-memory-surge-for-new-increase/", "2026-06-26"),
    "lenovo": (TF, "Lenovo Reportedly Sees Higher Memory Prices Becoming the New Normal Into 2030", TFN + "2026/06/26/news-lenovo-reportedly-sees-higher-memory-prices-becoming-the-new-normal-into-2030/", "2026-06-26"),
    "ces": (TF, "AI-Driven Memory Boom Ripples Through Hardware Markets, From Price Hikes to Product Delays", TFN + "2026/02/20/insights-ai-driven-memory-boom-ripples-through-hardware-markets-from-price-hikes-to-product-delays/", "2026-02-20"),
    "oppo": (TF, "Chinese Smartphone Price Hikes Begin; OPPO Adjusts From Mar. 16, Reportedly Up to CNY500", TFN + "2026/03/10/news-chinese-smartphone-price-hikes-begin-oppo-announces-increases-from-mar-16-reportedly-up-to-%c2%a5500/", "2026-03-10"),
    "surface": (TF, "Microsoft Expands Local AI Push With NVIDIA RTX Spark; Surface Ultra Priced Up to $5,899 as Memory Costs Rise", TFN + "2026/10/08/news-microsoft-expands-local-ai-push-with-nvidia-rtx-spark-surface-ultra-priced-up-to-5899-as-memory-costs-rise/", "2026-10-08"),
    "pcchina": (TF, "AI-Driven Component Costs Reportedly Push HP, ASUS, Acer to Shift Some PC Production Back to China", TFN + "2026/10/28/news-ai-driven-component-costs-reportedly-push-hp-asus-acer-to-shift-some-pc-production-back-to-china/", "2026-10-28"),
    "apple730": (TF, "Ahead of Cook's Final Apple Earnings Call: Rising Memory Costs and Potential Sep. iPhone Price Hike in Focus", TFN + "2026/07/30/news-ahead-of-cooks-final-apple-earnings-call-rising-memory-costs-and-potential-sep-iphone-price-hike-in-focus/", "2026-07-30"),
    "cp_soc": ("Counterpoint Research", "Smartphone OEMs Shift Focus to Profitability as SoC Shipments Fall 21% YoY in Q3 2026", "https://www.counterpointresearch.com/en/insights/smartphone-oems-shift-focus-to-profitability-as-soc-shipments-fall-21-percent-yoy", "2026-10-30"),
    "tf_list5": (TF, "Press Center listing page 5 (headline: Early Purchases Lift 2026 Smartphone Production Above Expectations; Full-Year Forecast Raised to 1.07 Billion Units)", TFP + "20260908-13222.html", "2026-09-08"),
    "tf_list1": (TF, "Server CPU Shipments Projected to Grow Over 40% YoY in 2027, with Arm-Based Products Continuing to Gain Market Share", TFP + "20261022-13279.html", "2026-10-22"),
    "tf_list15": (TF, "Press Center listing page 15 (headline: Agentic AI Drives Structural Expansion in Memory Demand, Global Memory Market Projected to Reach US$1.28 Trillion by 2027)", TFP + "20260529-13068.html", "2026-05-29"),
}

R = []


def add(seg, metric, period, value, unit, kind, src, quote, notes):
    pub, title, url, date = S[src]
    R.append([seg, metric, period, value, unit, kind, pub, title, url, date, quote, notes])


# ---------------- contract prices: conventional DRAM (all categories) ----------------
add("price-contract", "conventional DRAM contract price change", "1Q25", "-13 to -8", "% QoQ", "forecast", "tf_1q25",
    "Conventional DRAM prices are projected to drop by 8% to 13%.", "cat=all; excludes HBM")
add("price-contract", "DRAM contract price change incl. HBM", "1Q25", "-5 to 0", "% QoQ", "forecast", "tf_1q25",
    "However, if HBM products are included, the anticipated price decline will range from 0% to 5%.", "cat=all; blended with HBM; keep apart from conventional row")
add("price-contract", "conventional DRAM contract price change", "2Q25", "-5 to 0", "% QoQ", "forecast", "tf_2q25",
    "conventional DRAM prices are expected to decline by just 0–5% QoQ", "cat=all; excludes HBM")
add("price-contract", "DRAM contract price change incl. HBM", "2Q25", "3 to 8", "% QoQ", "forecast", "tf_2q25",
    "average DRAM pricing including HBM is forecast to rise by 3–8%, driven by increasing shipments of HBM3e 12hi.", "cat=all; blended with HBM. TF 2025-04-17 release said tariff stockpiling widened 2Q25 increases but its text gives no new figure (chart only)")
add("price-contract", "conventional DRAM contract price change", "3Q25", "10 to 15", "% QoQ", "forecast", "tf_3q25",
    "average contract prices for conventional DRAM are projected to rise by 10% to 15% in 3Q25.", "cat=all; excludes HBM")
add("price-contract", "DRAM contract price change incl. HBM", "3Q25", "15 to 20", "% QoQ", "forecast", "tf_3q25",
    "Including HBM, overall DRAM prices are expected to increase by 15% to 20%.", "cat=all; blended with HBM")
add("price-contract", "conventional DRAM contract price change", "4Q25", "8 to 13", "% QoQ", "forecast", "tf_4q25a",
    "Overall, conventional DRAM prices are expected to rise 8–13% QoQ in 4Q25", "cat=all; first 4Q25 call; revised up three times (see next rows)")
add("price-contract", "DRAM contract price change incl. HBM", "4Q25", "13 to 18", "% QoQ", "forecast", "tf_4q25a",
    "when HBM is included, the increase could widen to 13-18%.", "cat=all; blended with HBM; first 4Q25 call")
add("price-contract", "conventional DRAM contract price change (revised)", "4Q25", "18 to 23", "% QoQ", "forecast", "tf_4q25b",
    "from an earlier forecast of 8–13% growth to 18–23%, with a strong likelihood of further upward revision", "cat=all; second 4Q25 call")
add("price-contract", "conventional DRAM contract price change (revised)", "4Q25", "45 to 50", "% QoQ", "forecast", "tf_rev3q25",
    "conventional DRAM contract prices will rise by 45–50% QoQ.", "cat=all; third 4Q25 call, made late in the quarter")
add("price-contract", "conventional DRAM contract price change", "4Q25", "45 to 50", "% QoQ", "actual", "tf_rev4q25",
    "Conventional DRAM contract prices rose 45–50% QoQ", "cat=all; TF estimate of the realized change, published after the quarter")
add("price-contract", "conventional DRAM + HBM blended contract price change", "4Q25", "50 to 55", "% QoQ", "actual", "tf_rev4q25",
    "blended contract prices for conventional DRAM and HBM increased 50–55%", "cat=all; blended with HBM")
add("price-contract", "DRAM price change (alternate TF figure)", "4Q25", "53 to 58", "% QoQ", "actual", "tf_memrev",
    "last year's fourth quarter saw DRAM prices jump by 53–58% due to strong DDR5 demand.", "cat=all; conflicts with the 45-50% conventional figure in TF 2026-02-26; basis (blended or not) not stated; keep both")
add("price-contract", "conventional DRAM contract price change", "1Q26", "55 to 60", "% QoQ", "forecast", "tf_1q26a",
    "Conventional DRAM contract prices in 1Q26 are forecast to rise 55–60% QoQ", "cat=all; first 1Q26 call")
add("price-contract", "conventional DRAM contract price change (revised)", "1Q26", "90 to 95", "% QoQ", "forecast", "tf_1q26b",
    "revised upward, from a previous estimate of 55–60% to now 90–95%", "cat=all; second 1Q26 call")
add("price-contract", "conventional DRAM + HBM blended contract price change", "1Q26", "80 to 85", "% QoQ", "forecast", "tf_rev4q25",
    "conventional DRAM prices expected to surge 90–95% QoQ, and blended conventional DRAM + HBM pricing rising 80–85% QoQ.", "cat=all; blended with HBM; lower than conventional because HBM is on annual contracts")
add("price-contract", "conventional DRAM contract price change", "1Q26", "93 to 98", "% QoQ", "actual", "tf_rev1q26",
    "increased by approximately 93% to 98% QoQ.", "cat=all; TF estimate of the realized change")
add("price-contract", "conventional DRAM contract price change", "2Q26", "58 to 63", "% QoQ", "forecast", "tf_2q26",
    "Conventional DRAM contract prices are projected to rise by 58–63% QoQ despite downside risks to end-market shipments.", "cat=all; repeated in TF 2026-06-01; TF 2026-09-07 gives no realized 2Q26 figure")
add("price-contract", "conventional DRAM contract price change", "3Q26", "13 to 18", "% QoQ", "forecast", "tf_3q26",
    "Conventional DRAM contract prices are forecast to rise 13–18% QoQ in 3Q26.", "cat=all; repeated in TF 2026-09-07")
add("price-contract", "conventional DRAM contract price change", "4Q26", "10 to 15", "% QoQ", "forecast", "tf_4q26",
    "Conventional DRAM contract prices are projected to grow 10–15% QoQ in 4Q26", "cat=all; latest TF quarterly call")
add("price-contract", "cumulative conventional DRAM contract price index 2Q25 to 4Q26", "3Q25-4Q26", "6.8", "x (2Q25 level = 1)", "derived", "tf_4q26",
    "Conventional DRAM contract prices are projected to grow 10–15% QoQ in 4Q26",
    "cat=all; derived: product of TF range midpoints 1.125 (3Q25 fcst) x 1.475 (4Q25 act) x 1.955 (1Q26 act) x 1.605 (2Q26 fcst) x 1.155 (3Q26 fcst) x 1.125 (4Q26 fcst) = 6.77; mixes actual and forecast")

# ---------------- contract prices: by category ----------------
add("price-contract", "PC DRAM contract price change", "1Q25", "-13 to -8", "% QoQ", "forecast", "tf_1q25",
    "PC DRAM prices expected to drop by 8–13%; server DRAM by 5–10%", "cat=ddr5; PC DRAM = client DDR4/DDR5 mix; section heading")
add("price-contract", "server DRAM contract price change", "1Q25", "-10 to -5", "% QoQ", "forecast", "tf_1q25",
    "PC DRAM prices expected to drop by 8–13%; server DRAM by 5–10%", "cat=server-ecc; section heading")
add("price-contract", "LPDDR4X / LPDDR5X contract price change", "1Q25", "LPDDR4X -13 to -8; LPDDR5X -8 to -3", "% QoQ", "forecast", "tf_1q25",
    "contract price declines for LPDDR4X and LPDDR5X, falling by 8–13% and 3–8%, respectively", "cat=lpddr")
add("price-contract", "graphics DRAM contract price change", "1Q25", "-10 to -5", "% QoQ", "forecast", "tf_1q25",
    "TrendForce forecasts an average price decline of 5% to 10% for graphics DRAM in 1Q25.", "cat=gddr")
add("price-contract", "consumer DDR4 / DDR3 contract price change", "1Q25", "DDR4 -15 to -10; DDR3 -8 to -3", "% QoQ", "forecast", "tf_1q25",
    "Subsequently, prices for DDR3 and DDR4 are forecast to drop by 3%–8% and 10%–15%, respectively.", "cat=ddr4")
add("price-contract", "PC DRAM contract price change", "2Q25", "0", "% QoQ", "forecast", "tf_2q25",
    "As a result, PC DRAM prices are expected to remain flat QoQ in Q2.", "cat=ddr5")
add("price-contract", "GDDR6 contract price change", "2Q25", "-8 to -3", "% QoQ", "forecast", "tf_2q25",
    "GDDR6 prices are expected to decline by just 3–8%, supported by demand from DeepSeek's open-source AI model.", "cat=gddr")
add("price-contract", "consumer DDR4 contract price change", "2Q25", "0 to 5", "% QoQ", "forecast", "tf_2q25",
    "DDR4 contract prices are expected to rise 0–5% in 2Q25 with production slowing and demand rebounding.", "cat=ddr4; first quarter of the DDR4 turn")
add("price-contract", "consumer DDR4 contract price change", "3Q25", "40 to 45", "% QoQ", "forecast", "tf_3q25",
    "consumer DDR4 contract prices are forecast to surge by 40% to 45% in the third quarter.", "cat=ddr4; DDR4 EOL announcements drove restocking")
add("price-contract", "PC DRAM contract price change", "3Q25", "8 to 13", "% QoQ", "forecast", "tf_3q25",
    "As a result, PC DRAM contract prices are expected to rise by 8% to 13% in the third quarter.", "cat=ddr5")
add("price-contract", "server DRAM contract price change", "3Q25", "3 to 8", "% QoQ", "forecast", "tf_3q25",
    "with prices expected to rise by 3% to 8%.", "cat=server-ecc")
add("price-contract", "LPDDR4X / LPDDR5X contract price change", "3Q25", "LPDDR4X 23 to 28; LPDDR5X 5 to 10", "% QoQ", "forecast", "tf_3q25",
    "As a result, LPDDR4X contract prices are expected to surge by 23% to 28% in the third quarter.", "cat=lpddr; LPDDR5X quote: As such, LPDDR5X contract prices are expected to rise by 5% to 10%.")
add("price-contract", "LPDDR4X contract price change", "4Q25", ">10", "% QoQ", "forecast", "tf_4q25a",
    "pushing LPDDR4X prices to climb more than 10% QoQ in 4Q25.", "cat=lpddr")
add("price-contract", "server DRAM contract price change", "1Q26", ">60", "% QoQ", "forecast", "tf_1q26a",
    "As a result, server DRAM prices are expected to climb by more than 60% QoQ in 1Q26.", "cat=server-ecc; first 1Q26 call")
add("price-contract", "server DRAM contract price change (revised)", "1Q26", "~90", "% QoQ", "forecast", "tf_1q26b",
    "server DRAM prices up by around 90% QoQ in 1Q26, marking the largest quarterly increase on record", "cat=server-ecc")
add("price-contract", "PC DRAM contract price change", "1Q26", ">100", "% QoQ", "forecast", "tf_1q26b",
    "PC DRAM prices in 1Q26 are projected to increase by over 100% QoQ, setting a new record for a quarterly surge.", "cat=ddr5")
add("price-contract", "LPDDR4X and LPDDR5X contract price change", "1Q26", "~90", "% QoQ", "forecast", "tf_1q26b",
    "Contract prices for LPDDR4X and LPDDR5X are both expected to surge by around 90% QoQ in 1Q26", "cat=lpddr")
add("price-contract", "smartphone 8GB+256GB memory contract price change", "1Q26", "~200", "% YoY", "estimate", "tf_phone",
    "estimated contract prices in 1Q26 have surged nearly 200% YoY—roughly tripling from the same period last year.", "cat=lpddr; DRAM+NAND bundle, not DRAM alone")
add("price-contract", "DDR2 contract price change", "2Q26", "55 to 60", "% QoQ", "estimate", "tf_ddr2",
    "Following strong gains in 1Q26, TrendForce estimates DDR2 contract prices will rise by approximately 55–60% in 2Q26", "cat=ddr4; legacy; OEMs downgrade DDR4 to DDR3 and DDR3 to DDR2")
add("price-contract", "DDR2 contract price change", "3Q26", "35 to 40", "% QoQ", "forecast", "tf_ddr2",
    "followed by a further 35–40% increase in 3Q26.", "cat=ddr4; legacy")
add("price-contract", "server DRAM contract price change", "3Q26", "13 to 18", "% QoQ", "forecast", "tf_srv3q26",
    "Consequently, TrendForce predicts that server DRAM contract prices will rise by 13–18% quarter-over-quarter in 3Q26.", "cat=server-ecc; LTAs cap increases for US CSPs")
add("price-contract", "server DRAM contract price change, full year", "2026", "~270", "% YoY (cumulative)", "forecast", "tf_cspmem",
    "a further jump of approximately 270%.", "cat=server-ecc; TF 2026-08-25; enterprise SSD cumulative 235% in same release")
add("price-contract", "server DRAM supply status", "4Q26", "undersupplied", "-", "forecast", "tf_4q26",
    "Server DRAM is therefore expected to remain undersupplied in 4Q26.", "cat=server-ecc; TF gives no 4Q26 server % in text (chart only)")
add("price-contract", "mobile DRAM contract price direction", "4Q26", "moderating growth", "-", "forecast", "tf_4q26",
    "growth is expected to moderate in 4Q26.", "cat=lpddr; no % in text")
add("price-contract", "smartphone memory contract price change", "3Q26", "5 to 10", "% QoQ", "estimate", "cp_soc",
    "Smartphone memory price growth slowed to 5%-10% in Q3 2026 compared with Q2 2026.", "cat=lpddr; Counterpoint; memory generally, not DRAM only")
add("price-contract", "smartphone memory contract price change", "4Q26", "5", "% QoQ", "forecast", "cp_soc",
    "expected to increase by another 5% QoQ in Q4 2026.", "cat=lpddr; Counterpoint")
add("price-contract", "HBM3e price premium over DDR5", "2Q25", ">4", "x", "estimate", "tf_4q25b",
    "as of 2Q25, HBM3e still commanded a price premium more than four times that of DDR5", "cat=hbm")
add("price-contract", "HBM3e vs server DDR5 price ratio", "end-2026", "1 to 2", "x", "forecast", "tf_ddr5hbm",
    "the gap is expected to narrow to one to two times by the end of 2026", "cat=hbm; prior gap: HBM3e prices were previously four to five times higher than server DDR5")
add("price-contract", "HBM vs DDR5 64GB RDIMM wafer revenue", "1Q26", "RDIMM above HBM", "-", "estimate", "tf_hbm27a",
    "HBM wafer revenue was overtaken by DDR5 64GB RDIMM in 1Q26.", "cat=server-ecc; why suppliers shift wafers to server DDR5")
add("price-contract", "HBM contract price change", "2027", "70 to 140", "% YoY", "forecast", "tf_cspmem",
    "HBM contract prices could still rise by 70–140% in 2027.", "cat=hbm")
add("price-contract", "HBM blended ASP change", "2027", "121", "% YoY", "forecast", "tf_hbm27b",
    "Blended ASP is now projected to jump 121% YoY.", "cat=hbm; revised up 2026-09-29")
add("price-contract", "HBM 8-Hi per-Gb premium over 12-Hi", "2027", "10 to 20", "%", "forecast", "tf_hbm27b",
    "TrendForce expects 8-Hi products to carry a roughly 10–20% price premium per Gb over 12-Hi products in 2027.", "cat=hbm")

# ---------------- contract price levels (TrendForce price page) ----------------
add("price-contract", "DDR5 8GB SO-DIMM contract price (average)", "2H Sep 2026", "133.00", "USD per module", "actual", "tf_contract_page",
    "DDR5 8GB SO-DIMM | 2H Sep | 141.00 | 118.00 | 133.00 | 0.00%", "cat=ddr5; high 141, low 118; Oct 2026 contract update is members-only")
add("price-contract", "DDR5 8GB SO-DIMM contract price per GB", "2H Sep 2026", "16.6", "USD per GB", "derived", "tf_contract_page",
    "DDR5 8GB SO-DIMM | 2H Sep | 141.00 | 118.00 | 133.00 | 0.00%", "cat=ddr5; derived: 133.00 / 8 = 16.63")
add("price-contract", "DDR4 16GB SO-DIMM contract price (average)", "2H Sep 2026", "275.00", "USD per module", "actual", "tf_contract_page",
    "DDR4 16GB SO-DIMM | 2H Sep | 295.00 | 255.00 | 275.00 | ▲1.85%", "cat=ddr4; DDR4 module costs more than DDR5 8GB per GB (17.2 vs 16.6 USD/GB) because of DDR4 EOL")
add("price-contract", "DDR4 8GB SO-DIMM contract price (average)", "2H Sep 2026", "148.00", "USD per module", "actual", "tf_contract_page",
    "DDR4 8GB SO-DIMM | 2H Sep | 151.00 | 132.00 | 148.00 | ▲4.23%", "cat=ddr4")
add("price-contract", "DDR4 16Gb 2Gx8 chip contract price (average)", "2H Sep 2026", "52.00", "USD per chip", "actual", "tf_contract_page",
    "DDR4 16Gb 2Gx8 | 2H Sep | 61.00 | 49.00 | 52.00 | ▲4.00%", "cat=ddr4")
add("price-contract", "DDR4 8Gb 1Gx8 chip contract price (average)", "2H Sep 2026", "26.00", "USD per chip", "actual", "tf_contract_page",
    "DDR4 8Gb 1Gx8 | 2H Sep | 35.50 | 23.50 | 26.00 | ▲4.00%", "cat=ddr4")
add("price-contract", "DDR3 4Gb 256Mx16 chip contract price (average)", "2H Sep 2026", "15.20", "USD per chip", "actual", "tf_contract_page",
    "DDR3 4Gb 256Mx16 | 2H Sep | 16.50 | 14.00 | 15.20 | 0.00%", "cat=ddr4; legacy")

# ---------------- spot prices ----------------
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2025-02-05 week", "1.458", "USD per chip", "actual", "sp_250205",
    "The average spot price of mainstream chips (i.e., DDR4 1Gx8 3200MT/s) has stayed at US$1.458 this week.", "cat=ddr4; trough; DDR4 spot sliding because of CXMT supply")
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2025-03-19 week", "1.486", "USD per chip", "actual", "sp_250319",
    "from US$1.461 last week to US$1.486 this week.", "cat=ddr4")
add("price-spot", "DDR5 16Gb 2Gx8 5600 spot transaction price (SK hynix)", "2025-03-19 week", "4.95", "USD per chip", "actual", "sp_250319",
    "Consequently, transaction prices have climbed to US$4.95.", "cat=ddr5; SK hynix DDR5 2Gx8 5600MT/s")
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2025-09-23 week", "5.947", "USD per chip", "actual", "sp_250924",
    "has increased by 6.88% from US$5.564 last week to US$5.947 this week.", "cat=ddr4")
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2025-11-18", "12.757", "USD per chip", "actual", "sp_251119",
    "from US$12.179 last week (November 12) to US$12.757 this week (November 18).", "cat=ddr4")
add("price-spot", "DDR5 2Gx8 spot cumulative rise since early Sep 2025", "2025-09 to 2025-11-18", "307", "% cumulative", "actual", "sp_251119",
    "the spot price of DDR5 2Gx8 chips has experienced sequential increases reaching 307%", "cat=ddr5")
add("price-spot", "DDR4 1Gx8 spot cumulative rise since early Sep 2025", "2025-09 to 2025-11-18", "158", "% cumulative", "actual", "sp_251119",
    "the spot price of DDR4 1Gx8 chips has experienced sequential increases reaching 158%", "cat=ddr4")
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2025-12-30", "23.746", "USD per chip", "actual", "sp_251231",
    "from US$22.235 last week (Dec. 24) to US$23.746 this week (Dec. 30).", "cat=ddr4; same release: supply will decline rapidly for DDR4 in 2026, leading to the highest per-Gb price")
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2026-03-31", "33.96", "USD per chip", "actual", "sp_260401",
    "slightly decreased by 0.12% from US$34.00 last week (March 25) to US$33.96 this week (March 31)", "cat=ddr4; spot flat while buyers wait for 2Q26 contract prices")
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2026-06-16", "35.8", "USD per chip", "actual", "sp_260617",
    "from US$35.9 last week (June 10) to US$35.8 this week (June 16).", "cat=ddr4; DDR4 cost forces consumer DRAM buyers to downgrade specs")
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2026-07-28", "42.08", "USD per chip", "actual", "sp_260729",
    "from US$41.50 last week (July 22) to US$42.08 this week (July 28).", "cat=ddr4")
add("price-spot", "DDR4 8Gb 1Gx8 3200 weekly average spot", "2026-10-20", "46.357", "USD per chip", "actual", "sp_261021",
    "has risen by 0.84% to US$46.357 this week (October 20).", "cat=ddr4; same release: For DDR5, supply remains tight and suppliers are clearly reluctant to sell.")
add("price-spot", "DDR5 16Gb 2Gx8 4800/5600 spot session average", "2026-10-30", "61.50", "USD per chip", "actual", "tf_spot_page",
    "DDR5 16Gb (2Gx8) 4800/5600 | 73.00 | 47.30 | 73.00 | 47.30 | 61.50 | ▲ 0.27 %", "cat=ddr5; daily high 73.00, low 47.30")
add("price-spot", "DDR5 16Gb 2Gx8 eTT spot session average", "2026-10-30", "29.80", "USD per chip", "actual", "tf_spot_page",
    "DDR5 16Gb (2Gx8) eTT | 30.50 | 28.90 | 30.50 | 28.90 | 29.80 | ▲ 0.34 %", "cat=ddr5; effectively-tested (lower grade) parts")
add("price-spot", "DDR4 16Gb 2Gx8 3200 spot session average", "2026-10-30", "82.796", "USD per chip", "actual", "tf_spot_page",
    "DDR4 16Gb (2Gx8) 3200 | 116.00 | 45.60 | 116.00 | 45.60 | 82.796 | ▼ -0.15 %", "cat=ddr4; DDR4 16Gb spot is above DDR5 16Gb spot")
add("price-spot", "DDR4 8Gb 1Gx8 3200 spot session average", "2026-10-30", "46.864", "USD per chip", "actual", "tf_spot_page",
    "DDR4 8Gb (1Gx8) 3200 | 84.00 | 25.80 | 84.00 | 25.80 | 46.864 | — 0.00 %", "cat=ddr4")
add("price-spot", "DDR5 RDIMM 32GB 4800/5600 module spot (weekly)", "2026-10-26", "2165.00", "USD per module", "actual", "dx_home",
    "DDR5 RDIMM 32GB 4800/5600 | 2370.00 | 2100.00 | 2370.00 | 2100.00 | 2165.000 | 0.00%", "cat=server-ecc; derived per GB: 2165 / 32 = 67.7 USD/GB")
add("price-spot", "DDR5 UDIMM 16GB 4800/5600 module spot (weekly)", "2026-10-26", "241.667", "USD per module", "actual", "dx_home",
    "DDR5 UDIMM 16GB 4800/5600 | 275.00 | 220.00 | 275.00 | 220.00 | 241.667 | +0.70%", "cat=ddr5; derived per GB: 241.667 / 16 = 15.1 USD/GB")
add("price-spot", "DDR4 UDIMM 16GB 3200 module spot (weekly)", "2026-10-26", "164.20", "USD per module", "actual", "dx_home",
    "DDR4 UDIMM 16GB 3200 | 185.00 | 156.00 | 185.00 | 156.00 | 164.200 | -0.85%", "cat=ddr4")
add("price-spot", "DDR5 RDIMM 32GB module spot per GB", "2026-10-26", "67.7", "USD per GB", "derived", "dx_home",
    "DDR5 RDIMM 32GB 4800/5600 | 2370.00 | 2100.00 | 2370.00 | 2100.00 | 2165.000 | 0.00%", "cat=server-ecc; derived: 2165.000 / 32 = 67.66; about 4.5x the DDR5 UDIMM per-GB spot")
add("price-spot", "DDR5 UDIMM 16GB module spot per GB", "2026-10-26", "15.1", "USD per GB", "derived", "dx_home",
    "DDR5 UDIMM 16GB 4800/5600 | 275.00 | 220.00 | 275.00 | 220.00 | 241.667 | +0.70%", "cat=ddr5; derived: 241.667 / 16 = 15.10")
add("price-spot", "DDR4 8Gb weekly spot multiple, Feb 2025 to Oct 2026", "2025-02-05 to 2026-10-20", "31.8", "x", "derived", "sp_261021",
    "has risen by 0.84% to US$46.357 this week (October 20).", "cat=ddr4; derived: 46.357 / 1.458 (2025-02-05 week) = 31.8")
add("price-spot", "DDR5 16Gb spot multiple, Mar 2025 to Oct 2026", "2025-03-19 to 2026-10-30", "12.4", "x", "derived", "tf_spot_page",
    "DDR5 16Gb (2Gx8) 4800/5600 | 73.00 | 47.30 | 73.00 | 47.30 | 61.50 | ▲ 0.27 %", "cat=ddr5; derived: 61.50 / 4.95 = 12.4; bases differ (SK hynix 5600 transaction vs DRAMeXchange session average)")

# ---------------- inventory ----------------
add("inventory", "buyer inventory direction", "1Q25", "falling (frontloaded shipments)", "-", "estimate", "tf_2q25",
    "U.S. tariff hikes prompted most downstream brands to frontload shipments to 1Q25, accelerating inventory reduction", "cat=all; no weeks figure published in text")
add("inventory", "DRAM supplier inventory level", "3Q25-4Q25", "almost depleted", "-", "estimate", "tf_rev3q25",
    "DRAM suppliers' inventories are almost depleted.", "cat=all; TF gives no weeks figure")
add("inventory", "server DRAM supplier inventory level", "1Q26", "approaching depletion", "-", "estimate", "tf_1q26a",
    "suppliers' inventories approaching depletion and shipment growth reliant solely on wafer output increases", "cat=server-ecc")
add("inventory", "tier-1 PC OEM DRAM inventory direction", "1Q26", "declining", "-", "estimate", "tf_1q26b",
    "Even tier-1 PC OEMs with secured allocations from memory suppliers are experiencing declining inventory levels.", "cat=ddr5")
add("inventory", "US CSP server DRAM inventory direction", "2Q26", "building", "-", "estimate", "tf_srv3q26",
    "leading to a gradual buildup of DRAM inventories at U.S. CSPs during the second quarter.", "cat=server-ecc; CPU shortage delayed server assembly; buyers keep building stock ahead of a tight 2027")
add("inventory", "DRAM supplier inventory level", "2Q26", "historic lows", "-", "estimate", "tf_rev2q26",
    "suppliers' inventories remain at historic lows", "cat=all")
add("inventory", "Micron days of inventory (DIO)", "FQ4 2026 (to 2026-09-03)", "129", "days", "actual", "mu_fq4",
    "Ending inventory for fiscal Q4 was $10.4 billion, with days of inventory (DIO) at 129, an increase of nine", "cat=all; DRAM+NAND; rise includes node EOL build-ahead; Micron: inventory levels and supply remain extremely tight")
add("inventory", "Micron inventory value", "FQ4 2026", "10.4", "USD billion", "actual", "mu_fq4",
    "Ending inventory for fiscal Q4 was $10.4 billion", "cat=all; press release table: 10,372M vs 8,567M prior quarter")

# ---------------- contract structure, LTAs, prepayments ----------------
add("contract", "Micron strategic customer agreements (SCAs) signed", "to 2026-09-30", "26", "agreements", "actual", "mu_fq4",
    "To date, we have signed 26 SCAs, which we currently estimate to be over 35% of our revenue through", "cat=all; multi-year take-or-pay; most have floor and ceiling price bands; some extend into 2031")
add("contract", "Micron SCA customer financial commitments", "to 2026-09-30", "32", "USD billion", "actual", "mu_fq4",
    "financial commitments from customers have increased to $32 billion, the vast majority of which are cash deposits.", "cat=all; up from 22 USD billion in June 2026")
add("contract", "Micron remaining performance obligations (SCAs)", "to 2026-09-30", "~150", "USD billion", "actual", "mu_fq4",
    "our remaining performance obligations, or RPO, is", "cat=all; quote continues on next line: approximately $150 billion; RPO counts committed volumes at minimum prices")
add("contract", "Micron customer cash deposits on balance sheet", "FQ4 2026", "12.7", "USD billion", "actual", "mu_fq4",
    "Customer cash deposits on our balance sheet at the end of fiscal Q4 were $12.7 billion.", "cat=all; 12.3 USD billion received in FQ4; returned late in each agreement term")
add("contract", "Micron SCAs (June status)", "to 2026-06-25", "16 SCAs; ~20% of DRAM output", "-", "actual", "mu_sca",
    "the company has signed 16 SCAs, spanning roughly 20% of its DRAM output and about one-third of its NAND volumes", "cat=all; via Investing.com call transcript; commitments then 22 USD billion, RPO ~100 USD billion")
add("contract", "Micron SCA term and price cap", "2026", "5 years (3 automotive)", "years", "actual", "mu_sca",
    "lock in both volume and pricing over a five-year term (or three years in the automotive segment)", "cat=all; Yonhap/ZDNet via TF; cap tied to April-June 2026 market prices; HBM, DDR6, LPDDR6 priced separately")
add("contract", "SK hynix advance payments in Microsoft and Google deals", "2026", "10 to 30", "% of contract value", "estimate", "mu_sca",
    "include advance payments of around 10%–30% of total contract value", "cat=all; Green Economy News via TF; Microsoft three-year DDR5 deal; Google up to five years")
add("contract", "SK hynix LTA customers", "to 2026-07-29", "~10", "customers", "actual", "hx_2q26",
    "The company has finalized Long-Term Agreements (LTAs) with around 10 customers, including key strategic partners", "cat=all")
add("contract", "SK hynix LTA customers", "to 2026-10-28", "14", "customers", "actual", "hx_3q26",
    "signed LTAs with 14 major customers, including leading global cloud service providers (CSPs)", "cat=all; contract terms typically five years")
add("contract", "SK hynix LTA share of 2027-2028 capacity", "2027-2028", ">50", "% of total production capacity", "actual", "hx_3q26",
    "corresponds to more than 50% of total production capacity for 2027 and 2028", "cat=all")
add("contract", "Samsung LTA customers", "to 2026-10-29", "10 signed; 10 in talks", "customers", "actual", "ss_3q26",
    "finalized long-term memory supply agreements (LTAs) with 10 major customers and is negotiating with another 10.", "cat=all; Aju Business Daily via TF")
add("contract", "Samsung LTA capacity target", "by 2030", "60 to 70", "% of production capacity", "forecast", "ss_3q26",
    "securing LTAs covering 60–70% of production capacity by 2030.", "cat=all")
add("contract", "Samsung LTA upfront payments", "2026", "~25", "% of contracted volumes", "estimate", "ss_lta",
    "Samsung has already secured upfront payments covering roughly one-quarter of contracted volumes", "cat=all; ETNews via TF; rolling five-year LTAs renewed yearly; price floors for commodity memory")
add("contract", "LTA share of server DDR5 shipments", "2H26", ">30", "% of shipments", "estimate", "ss_lta",
    "LTA volumes are expected to account for more than 30% of server DDR5 shipments in H2 2026.", "cat=server-ecc; Invest Chosun via TF")
add("contract", "share of global DRAM capacity under LTAs", "2027", "~50", "% of capacity", "forecast", "ss_lta",
    "nearly half of global DRAM capacity could be locked under long-term agreements by 2027", "cat=all; analysts via Invest Chosun")
add("contract", "LTA price ceilings", "from 2Q26", "ceilings present", "-", "estimate", "tf_cspmem",
    "Some long-term agreements (LTAs) signed from 2Q26 onward have included price ceilings that could limit further increases.", "cat=all")
add("contract", "server DRAM price driver shift", "3Q26", "non-LTA buyers", "-", "estimate", "tf_srv3q26",
    "the primary source of server DRAM price increases will shift toward customers without LTAs", "cat=server-ecc; multi-year LTAs with US CSPs stop suppliers raising those prices")
add("contract", "RDIMM bit supply growth (preliminary supplier guidance)", "2027", "15 to 20", "% YoY", "forecast", "tf_srv3q26",
    "total RDIMM bit supply will grow by only 15–20% YoY, significantly lagging the projected growth in server CPU shipments.", "cat=server-ecc")
add("contract", "server module capacity mix shift", "1H26-3Q26", "96/128GB to 32/64GB", "GB per module", "estimate", "tf_srv3q26",
    "some systems shifting from 96 GB and 128 GB modules to 32 GB and 64 GB modules.", "cat=server-ecc; buyers cut capacity per server to stretch supply")
add("contract", "CSP CapEx (nine largest CSPs)", "2026", "957", "USD billion", "forecast", "tf_cspcapex",
    "Combined CapEx among the world's nine leading CSPs is projected to surge 106% YoY to US$957 billion in 2026.", "cat=all; demand-side funding of memory")
add("contract", "CSP CapEx (nine largest CSPs)", "2027", ">1500", "USD billion", "forecast", "tf_cspcapex",
    "In 2027, this figure is expected to surpass $1.5 trillion, representing a further 60% YoY increase.", "cat=all; one reason for the revision: advance payments required by some component suppliers to secure supply")
add("contract", "memory (DRAM+NAND) share of CSP CapEx", "2026", "47", "% of CSP capex", "forecast", "tf_cspmem",
    "DRAM and NAND Flash combined will account for 47% of CSPs' total CapEx in 2026", "cat=all")
add("contract", "memory (DRAM+NAND) share of CSP CapEx", "2027", "68", "% of CSP capex", "forecast", "tf_cspmem",
    "will push memory's share of CSP capex to 68% in 2027.", "cat=all")

# ---------------- equipment, capex, cleanroom, materials ----------------
add("equipment", "WFE market size (Lam view)", "2026", "mid-150s", "USD billion", "forecast", "lam_slides",
    "WFE: CY26 mid-$150B range | Preliminary CY27 >$200B", "cat=all; all segments, not DRAM only")
add("equipment", "WFE market size (Lam view)", "2027", ">200", "USD billion", "forecast", "lam_slides",
    "WFE: CY26 mid-$150B range | Preliminary CY27 >$200B", "cat=all; preliminary")
add("equipment", "industry constraint cited by Lam", "2026", "cleanroom space; component supply", "-", "estimate", "lam_slides",
    "Cleanroom space availability and supply chain constraints for certain components limiting", "cat=all; slide continues: industry's ability to fully meet end demand")
add("equipment", "Lam memory share of systems revenue", "Sep quarter 2026", "46", "% of systems revenue", "actual", "lam_slides",
    "Memory 46%", "cat=all; DRAM+NAND")
add("equipment", "Lam China share of revenue", "Sep quarter 2026", "35", "% of revenue", "actual", "lam_pr",
    "China 35%", "cat=all; Korea 20%, Taiwan 18%")
add("equipment", "ASML 2026 sales outlook", "2026", "36 to 40", "EUR billion", "forecast", "asml",
    "now expects sales to reach €36 billion to €40 billion (US$42–47 billion)", "cat=all; raised from 34-39 on memory and logic demand (ASML press release via TF)")
add("equipment", "South Korea share of ASML sales", "1Q26", "45", "% of sales", "actual", "asml",
    "the region contributing 45% of its Q1 sales, up from 22% in 4Q25", "cat=all; Korea = Samsung and SK hynix memory")
add("equipment", "Samsung EUV systems secured", "2026", "~20", "EUV systems", "estimate", "asml",
    "securing around 20 EUV systems from ASML for sub-10nm advanced process nodes", "cat=all; SeDaily via TF; total lithography orders ~70, mainly Pyeongtaek P5 Line 1")
add("equipment", "SK hynix EUV systems ordered", "two years to 2027", "~24", "EUV systems", "estimate", "asml",
    "the order is understood to cover about 24 EUV systems, based on industry estimates of roughly 500 billion won per unit", "cat=all; The Elec via TF; ~12 trillion won over two years; Bloomberg: ~8 USD billion on ASML tools through 2027")
add("equipment", "China share of ASML sales", "1Q26", "19", "% of sales", "actual", "asml",
    "China accounted for just 19% of ASML's 1Q26 sales, down sharply from 36% in 4Q25", "cat=all")
add("equipment", "Japan share of global photoresist supply", "2025", "~80", "% of supply", "estimate", "jsr",
    "According to Nikkei, Japanese companies collectively account for roughly 80% of global photoresist supply.", "cat=all; materials concentration risk; a related TF headline flags a Japan photoresist shortage risk from >40% Middle East naphtha reliance (headline only, not read)")
add("capex", "Samsung + SK hynix new-fab investment (Korea southwest)", "multi-year", "800", "KRW trillion", "forecast", "kr800",
    "the two memory giants will jointly deploy 800 trillion won to build four new fabs in the country's southwest", "cat=all; The Elec/Chosun Biz via TF; also 81 trillion won packaging hub; tool supply strain")
add("capex", "Korea government DRAM capacity goal", "within five years", "2", "x domestic DRAM capacity", "forecast", "kr800",
    "plans to double domestic DRAM production capacity within five years", "cat=all; policy target; SK hynix Yongin fourth fab moved to 2033 from 2045")
add("capex", "Micron net capex", "FY2026", "27.37", "USD billion", "actual", "mu_fq4pr",
    "$27.37 billion for the full year of 2026", "cat=all; net of government incentives; gross PP&E 30.71 USD billion")
add("capex", "Micron capex guidance", "FQ1 FY2027 / 1H FY2027", "~11.5 / ~25", "USD billion", "forecast", "mu_fq4",
    "In fiscal Q1, we project capex of around $11.5 billion and anticipate first-half fiscal 2027 capex to be approximately $25 billion.", "cat=all; 2H FY27 higher; construction capex grows faster than equipment capex")
add("capex", "Micron new DRAM fab output timing", "2027-2030", "ID1 mid-2027; ID2 late 2028; NY 2030", "calendar timing", "forecast", "mu_fq4",
    "Our ID1 fab is on track to commence wafer output in mid-calendar 2027, and ID2 is on track to commence wafer", "cat=all; Japan DRAM expansion late 2028; Tongluo shipments mid-2027; Singapore HBM packaging early 2027")
add("capex", "Micron Tongluo fab purchase price", "2026", "1.8", "USD billion", "actual", "tf_tongluo",
    "Micron intends to acquire PSMC's Tongluo fab in Taiwan (excluding production equipment) for US$1.8 billion", "cat=all; buys cleanroom, not tools")
add("capex", "Tongluo Phase 1 capacity vs Micron global capacity", "2H27", ">10", "% of Micron capacity", "forecast", "tf_tongluo",
    "The capacity from Phase 1 at Tongluo in the second half of 2027 is projected to surpass 10% of Micron's global capacity.", "cat=all")
add("capex", "SK hynix Yongin Phase 1 cleanroom opening", "early 2027", "early 2027", "timing", "forecast", "hx_2q26",
    "following the opening of the Yongin Phase 1 cleanroom in early 2027.", "cat=all; 3Q26 release: Yongin Phase 1 enters full-scale operation next year; M15X to max capacity by end-2026 for HBM4")
add("capex", "HBM share of DRAM wafer input", "end-2025 / end-2026 / end-2027", "18 / 22 / 30", "% of DRAM wafer input", "forecast", "tf_hbm27a",
    "approximately 18%, 22%, and 30% of total DRAM wafer input by the end of 2025, 2026, and 2027, respectively", "cat=hbm; HBM bit share only 8%/9%/13%; crowding-out of conventional DRAM")
add("capex", "new DRAM capacity contribution timing", "2027-2028", "ramp 2H27; material output 2028", "timing", "forecast", "tf_2027",
    "substantial output contributions are not expected to materialize until 2028.", "cat=all; several suppliers bring capacity online in 2027 but delay ramps to 2H27")

# ---------------- China and export controls ----------------
add("china", "CXMT capacity-equivalent share of global DRAM output", "2024", "~10", "% of global output (capacity basis)", "estimate", "cx_share",
    "Based solely on its wafer production capacity, CXMT could produce the equivalent of approximately 10% of the global DRAM chip", "cat=all; Nikkei via TF; actual share lower because of yields")
add("china", "Chinese suppliers' combined DRAM market share", "2025", "10", "% share", "forecast", "cx_share",
    "the combined market share of all Chinese players could surge to 10% in 2025, doubling from 5% last year.", "cat=all; TF estimate")
add("china", "CXMT IPO valuation sought", "2026 (IPO as early as 1Q26)", "up to 300", "CNY billion", "estimate", "cx_ipo",
    "seeking a valuation of up to RMB 300 billion (US$42 billion).", "cat=all; Reuters via TF; IPO counselling began July 2025 (CICC, CSC Financial); 2026 listing status not verified in this pass")
add("china", "CXMT registered capital", "2025", "60.19", "CNY billion", "actual", "cx_ipo0",
    "CXMT Corporation has a registered capital of RMB 60.19 billion.", "cat=all; STCN via TF")
add("china", "CXMT LPDDR5X mass production", "since May 2025", "8533 and 9600", "Mbps", "actual", "cx_ipo",
    "its 8533Mbps and 9600Mbps products entered mass production in May", "cat=lpddr; 10667Mbps in customer trials")
add("china", "CXMT HBM3E yield", "2026-10", "20 to 30", "% yield", "estimate", "cx_hbm",
    "CXMT's HBM3E yields currently stand at just 20% to 30%, well below the approximately 70%", "cat=hbm; Reuters via TF; limited production expected within two months; products could reach market in 2027")
add("china", "CXMT Section 1260H listing", "2025-01", "added", "-", "actual", "cx_1260h",
    "The annually updated \"Section 1260H list\" of Chinese military-linked companies now includes 134 firms", "cat=all; CXMT added; it was excluded from the December 2024 chip curbs")
add("china", "US HBM export controls and Entity List additions", "2024-12-02", "140", "entities added", "actual", "bis",
    "Addition of 140 entities to the Entity List, in addition to 14 modifications", "cat=hbm; same rule: New controls on high-bandwidth memory (HBM); License Exception HBM; compliance date 2024-12-31")
add("china", "US approval for tools to Samsung/SK hynix China fabs", "2026", "annual approval granted Dec 2025", "-", "actual", "veu",
    "In December 2025, Washington granted annual approval for U.S. chipmaking equipment shipments", "cat=all; VEU-type authorizations revoked Sep 2025; 2027 approval not yet issued; no capacity add allowed")

# ---------------- policy and tariffs ----------------
add("policy", "Section 232 semiconductor tariff rate", "from 2026-01-15", "25", "% ad valorem", "actual", "s232",
    "imports of Covered Products will be subject to a 25 percent _ad valorem_ duty rate.", "cat=all; narrow scope: certain advanced computing chips; memory/DRAM not named in the proclamation text; US data-center and other uses exempt; a broader phase 2 is possible")
add("policy", "US reciprocal tariff rates: Taiwan vs Korea/Japan", "from 2025-08-07", "Taiwan 20; Korea/Japan/EU 15", "%", "actual", "tw20",
    "Japan, South Korea and the EU secured more favorable rates at 15% through investment commitments.", "cat=all; ICs, servers, PC components largely excluded in 2025")
add("policy", "US class action share claim and price claim", "filed 2026", ">90 share; ~700 price rise", "%", "estimate", "suit",
    "driving prices up by about 700% over the past four years.", "cat=all; plaintiffs' allegation, not a finding; case 3:26-cv-06345 N.D. Cal.")

# ---------------- OEM effects ----------------
add("oem", "Xbox console price increase", "Aug 2026", "+100 to 499; +150 to 749", "USD", "actual", "xbox",
    "raise the price of its entry-level console by $100 to $499, while a higher-storage variant will increase by $150 to $749.", "cat=all; BBC via TF; second hike in under a year; cumulative ~30-40%")
add("oem", "Xbox statement on memory cost", "2026-06", "2.5", "x rise in recent months", "actual", "xbox",
    "storage and memory prices have surged 2.5x in recent months and are expected to double again by fall 2027.", "cat=all; Xbox blog via TF; also a 2027 outlook signal")
add("oem", "Apple price increases (Mac, iPad)", "mid-2026", "MacBook Air 512GB 1099 to 1299; MacBook Pro 1TB 1699 to 1999; iPad Air 599 to 749; Neo 599 to 699", "USD", "actual", "xbox",
    "MacBook Air (512GB) increasing to $1,299 from $1,099", "cat=all; Reuters/BBC via TF; BBC: roughly 20% on select laptops and tablets")
add("oem", "Sony PS5 price", "since launch to 2026", "Digital 400 to 600; Pro 900", "USD", "actual", "xbox",
    "Sony has increased the PlayStation 5 Digital Edition from $400 to $600 since launch", "cat=all; Forbes via TF")
add("oem", "Nintendo Switch 2 price", "2026", "450 to 500", "USD", "actual", "xbox",
    "raising the Switch 2 price by $50 from $450 to $500.", "cat=lpddr; Forbes via TF; Switch 2 uses LPDDR")
add("oem", "console memory share of hardware cost", "2026", "Nintendo 21-23; Sony/Microsoft >35", "% of BOM", "forecast", "tf_console",
    "Memory modules are projected to account for 21–23% of total hardware costs in 2026.", "cat=all; Sony and Microsoft anticipate that memory costs will make up over 35% of the total BOM costs by 2026")
add("oem", "game console shipments", "2026", "-4.4", "% YoY", "forecast", "tf_console",
    "the global game console market will decline 4.4% YoY in 2026", "cat=all")
add("oem", "iPhone 18 series retail price change", "3Q26 launch", "10 to 20", "%", "forecast", "tf_ip18",
    "Prices for the new models are projected to rise by around 10–20%", "cat=lpddr; TF view; Apple absorbs part of the cost")
add("oem", "iPhone 18 Pro 256GB memory cost change", "3Q26", "~400", "% YoY", "estimate", "tf_ip18",
    "For the 256 GB Pro model, memory costs in 3Q26 are expected to be nearly 400% higher than a year earlier.", "cat=lpddr; DRAM+NAND")
add("oem", "iPhone Pro 256GB memory share of BOM", "3Q26 / 1H27", "~34 / >40", "% of BOM", "forecast", "tf_ip18pro",
    "from around 10% a year ago to approximately 34% in 3Q26, and is expected to exceed 40% in 1H27", "cat=lpddr; BOM +38% YoY; memory prices up five- to sevenfold since the beginning of 2025")
add("oem", "smartphone memory share of BOM", "1Q26", "30 to 40", "% of BOM", "estimate", "tf_phone",
    "Memory, which historically accounted for around 10–15% of a smartphone's BOM, has now surged to 30–40%.", "cat=lpddr")
add("oem", "low-end smartphone base RAM", "2026", "4", "GB", "forecast", "tf_oem1q26",
    "The most affected will be the low-end smartphone market, where base models are likely to return to 4GB in 2026.", "cat=lpddr; spec cut")
add("oem", "global smartphone production", "2026", "-10 (1.135B units)", "% YoY", "forecast", "tf_phone",
    "Total output is forecast to decline 10% YoY to approximately 1.135 billion units.", "cat=lpddr; bear case -15% or more")
add("oem", "global smartphone production (revised)", "2026", "-16.2 (1.051B units)", "% YoY", "forecast", "apple730",
    "TrendForce forecasts global smartphone production to decline approximately 16.2% YoY to 1.051 billion units in 2026.", "cat=lpddr; TF figure quoted in a 2026-07-30 news item")
add("oem", "global smartphone production (revised up)", "2026", "1.07", "billion units", "forecast", "tf_list5",
    "Early Purchases Lift 2026 Smartphone Production Above Expectations; Full-Year Forecast Raised to 1.07 Billion Units", "cat=lpddr; headline only (seen on listing page), body not read")
add("oem", "China smartphone price rises (OPPO/OnePlus; upcoming models)", "Mar 2026", "OnePlus +300 to 500; new models +600 to 1,000; flagships +2,000 to 3,000", "CNY", "estimate", "oppo",
    "price increases for OnePlus, a sub-brand of OPPO, are expected to range from 300 to 500 yuan", "cat=lpddr; Jiemian/ijiwei via TF; Xiaomi named only as tag, no figure")
add("oem", "Samsung mobile (MX) operating result", "2Q26", "-0.7", "KRW trillion", "actual", "ss_2q26",
    "posted a KRW 700 billion operating loss, marking its first quarterly loss on record", "cat=lpddr; Reuters via TF; memory cost squeeze on Samsung's own phone unit")
add("oem", "smartphone SoC shipments", "3Q26 / 2026 / 2027", "-21 / -20 / -3 to -4", "% YoY", "forecast", "cp_soc",
    "Global smartphone SoC shipments are expected to decline by 20% YoY in 2026 and another 3%-4% YoY in 2027.", "cat=lpddr; Counterpoint; Q3 2026 actual -21%; price volatility to moderate in 2027")
add("oem", "notebook CPU+DRAM+SSD share of BOM (900 USD model)", "1Q25 / 3Q26", "45 / 68", "% of BOM", "estimate", "tf_nb26",
    "this share had risen to 68% by 3Q26", "cat=ddr5; 1Q25 base: core components including the CPU, DRAM, and SSD accounted for approximately 45%")
add("oem", "notebook price rise needed to hold margin", "3Q26 vs 1Q25", "~80", "%", "estimate", "tf_nb26",
    "by 3Q26, brands would need to raise the price of a comparable 1Q25 product by approximately 80%", "cat=ddr5")
add("oem", "notebook retail price rise from memory alone", "1Q26", ">30 (memory); ~40 (memory+CPU)", "%", "estimate", "tf_nb40",
    "surging memory prices alone could raise retail prices by more than 30%", "cat=ddr5; DRAM+SSD share of notebook BOM >30% in 1Q26 vs ~15% normal")
add("oem", "global notebook shipments", "2026", "-9.4", "% YoY", "forecast", "tf_nb26",
    "As a result, the decline in global notebook shipments for full-year 2026 is expected to narrow to 9.4% YoY.", "cat=ddr5; earlier TF calls: -14.8% (Mar 2026), -13.6% (Jul 2026)")
add("oem", "global notebook shipments", "2027", "low-single-digit decline", "% YoY", "forecast", "tf_nb27",
    "Global notebook shipments are currently projected to decline by a low-single-digit percentage in 2027.", "cat=ddr5; high-single-digit decline if DRAM and CPU costs are passed on")
add("oem", "PC OEM channel price-hike notices after CES", "1Q26", "5 to 15", "%", "actual", "ces",
    "Following CES, OEMs issued price-hike notices to channel partners, with increases of 5%–15%.", "cat=ddr5; TechNews via TF; NVIDIA reportedly delayed RTX 50 Refresh on GDDR cost; Micron winding down Crucial")
add("oem", "Lenovo view on memory prices", "to 2030", "new normal into 2030", "-", "forecast", "lenovo",
    "sees higher memory pricing as potentially settling into a 'new normal' well into 2030 and beyond.", "cat=all; Lenovo ISC 2026 slide via Wccftech/Computer Base; assumes new capacity from ~2028")
add("oem", "NVIDIA DGX Spark price", "2026-10", "6950 (~75% above launch)", "USD", "actual", "surface",
    "Its 128 GB DGX Spark now costs $6,950, about 75% above its launch price.", "cat=lpddr; The Register via TF; LPDDR5X unified memory")
add("oem", "notebook production share outside China", "2025 / 2026 / 2027", "24 / 21 / <20", "% of production", "forecast", "pcchina",
    "the share of global notebook production outside China will decline from approximately 24% in 2025 to 21% in 2026", "cat=ddr5; cost pressure pushes HP, ASUS, Acer (and possibly Dell) back to China")
add("oem", "server memory configuration cuts", "1H26", "RDIMM capacity reduced", "-", "estimate", "tf_rubin",
    "CSPs and server OEMs reduced RDIMM capacities for server configurations during the first half of 2026", "cat=server-ecc; NVIDIA also halved SOCAMM capacity for Vera Rubin")

# ---------------- supplier financials ----------------
for period, val, pct, src, q in [
    ("3Q25", "41.4", "", "tf_rev3q25", "drove the global DRAM industry revenue to US$41.4 billion in 3Q25, marking a strong 30.9% QoQ growth."),
    ("4Q25", "53.58", "", "tf_rev4q25", "lifting total DRAM industry revenue to $53.58 billion in 4Q25, up 29.4% QoQ."),
    ("1Q26", "97", "", "tf_rev1q26", "This surge contributed to an overall industry revenue increase of 81% QoQ, reaching $97 billion."),
    ("2Q26", "154.73", "", "tf_rev2q26", "a 59.5% QoQ increase in total DRAM industry revenue, reaching nearly US$154.73 billion in 2Q26."),
]:
    add("financials", "global DRAM industry revenue", period, val, "USD billion", "actual", src, q, "cat=all; TF estimate; includes HBM")

for sup, rows in {
    "Samsung": [("3Q25", "13.5", "tf_rev3q25", "raising its quarterly revenue to $13.5 billion, a 30.4% rise QoQ", "32.6% share"),
                ("4Q25", "19.30", "tf_rev4q25", "Samsung's 4Q25 revenue climbed to $19.30 billion, up 43% QoQ", "36% share; ASP ~+40% QoQ"),
                ("1Q26", "37.32", "tf_rev1q26", "driving quarterly revenue up 93.4% QoQ to $37.32 billion and increasing market share to 38.5%.", "38.5% share"),
                ("2Q26", "60.98", "tf_rev2q26", "lifted Samsung's quarterly revenue to $60.98 billion, up 63.4% QoQ.", "39.4% share")],
    "SK hynix": [("3Q25", "13.75", "tf_rev3q25", "revenue grow by 12.4% QoQ to $13.75 billion", "33.2% share"),
                 ("4Q25", "17.22", "tf_rev4q25", "SK hynix posted revenue of $17.22 billion, up 25.2% QoQ", "32.1% share; ASP mid-20s % QoQ"),
                 ("1Q26", "27.98", "tf_rev1q26", "The company posted 1Q26 revenue of $27.98 billion, up 62.5% QoQ, ranking second with a 28.8% market share.", "28.8% share"),
                 ("2Q26", "38.59", "tf_rev2q26", "Its 2Q26 revenue increased 37.9% QoQ to $38.59 billion, while market share edged down to 24.9%.", "24.9% share; HBM-heavy mix limits ASP growth")],
    "Micron": [("3Q25", "10.65", "tf_rev3q25", "Its revenue jumped to $10.65 billion, reflecting a 53.2% QoQ increase.", "25.7% share"),
               ("4Q25", "11.98", "tf_rev4q25", "Micron reported revenue of $11.98 billion, up 12.4% QoQ", "22.4% share; ASP ~+17% QoQ; contracts set earlier at lower prices"),
               ("1Q26", "21.75", "tf_rev1q26", "with quarterly revenue surging 81.6% QoQ to $21.75 billion, while maintaining a stable 22.4% market share", "22.4% share"),
               ("2Q26", "36.0", "tf_rev2q26", "Revenue rose 65.5% QoQ to $36.0 billion in 2Q26, lifting its market share slightly to 23.3%.", "23.3% share")],
}.items():
    for period, val, src, q, extra in rows:
        add("financials", f"{sup} DRAM revenue (TrendForce)", period, val, "USD billion", "actual", src, q, f"cat=all; calendar quarter; {extra}")

add("financials", "DRAM industry revenue multiple 4Q25 to 2Q26", "4Q25-2Q26", "2.89", "x", "derived", "tf_rev2q26",
    "a 59.5% QoQ increase in total DRAM industry revenue, reaching nearly US$154.73 billion in 2Q26.", "cat=all; derived: 154.73 / 53.58 = 2.89")
add("financials", "SK hynix revenue / operating profit / margin", "4Q25", "32.8267 / 19.1696 / 58", "KRW trillion / KRW trillion / %", "actual", "hx_1q26",
    "4Q2025 Revenue: 32.8267 trillion won / 4Q2025 Operating Profit: 19.1696 trillion won", "cat=all; company total (DRAM+NAND); margin 58% from results table")
add("financials", "SK hynix revenue / operating profit / margin", "1Q26", "52.5763 / 37.6103 / 72", "KRW trillion / KRW trillion / %", "actual", "hx_1q26",
    "recorded 52.5763 trillion won in revenue, 37.6103 trillion won in operating profit (with an operating margin of 72%)", "cat=all; company total")
add("financials", "SK hynix revenue / operating profit / margin", "2Q26", "79.3187 / 60.5426 / 76", "KRW trillion / KRW trillion / %", "actual", "hx_2q26",
    "79.3187 trillion won in revenues, 60.5426 trillion won in operating profit (with an operating margin of 76%)", "cat=all; company total")
add("financials", "SK hynix revenue / operating profit / margin", "3Q26", "104.6155 / 83.3338 / 80", "KRW trillion / KRW trillion / %", "actual", "hx_3q26",
    "recorded 104.6155 trillion won in revenues, 83.3338 trillion won in operating profit (with an operating margin of 80%)", "cat=all; company total; capex amount not disclosed; spending to rise sharply in 2027")
add("financials", "Samsung DS division operating profit / margin", "2Q26", "89.2 / ~70", "KRW trillion / %", "actual", "ss_2q26",
    "generated KRW 89.2 trillion in operating profit", "cat=all; DS = memory + LSI + foundry; margin nearly 70% vs 65.7% in 1Q26; DS = 99.7% of group operating profit")
add("financials", "Samsung DRAM ASP change", "2Q26", "mid-40s", "% QoQ", "actual", "ss_2q26",
    "Samsung's ASPs climbed by the mid-40% range for DRAM and the high-60% range for NAND", "cat=all; Newspim via TF; DRAM shipments >10% QoQ; SK hynix DRAM ASP +30% QoQ")
add("financials", "Samsung DS division sales / operating profit / margin", "3Q26", "147.1 / 106.5 / 72.4", "KRW trillion / KRW trillion / %", "actual", "ss_3q26",
    "delivering KRW 147.1 trillion in sales and KRW 106.5 trillion in operating profit, translating into a 72.4% margin.", "cat=all; Samsung deck via TF; group OP KRW 107.4T, revenue KRW 195.3T")
add("financials", "Samsung DRAM ASP change", "3Q26", "~20", "% QoQ", "actual", "ss_3q26",
    "DRAM average selling prices (ASPs) climbed around 20% QoQ in 3Q26, while NAND gained a high-teens percentage.", "cat=all; News 1 via TF; DRAM bits low- to mid-single-digit % QoQ")
add("financials", "Micron revenue / gross margin", "FQ3 2026 (to ~2026-05-28)", "41.46 / 84.9", "USD billion / %", "actual", "mu_fq3",
    "Gross margin climbed to a record 84.9%, well above the company's 81% forecast", "cat=all; CNBC via TF; revenue 41.46 USD billion")
add("financials", "Micron DRAM revenue", "FQ4 2026 (to 2026-09-03)", "39.8", "USD billion", "actual", "mu_fq4",
    "Fiscal Q4 DRAM revenue was a record $39.8 billion, up 343% year over year, and represented 73% of total", "cat=all; +27% QoQ; DRAM prices up high-teens %; bits up mid-single-digit %")
add("financials", "Micron total revenue / GAAP gross margin / GAAP operating margin", "FQ4 2026", "54.23 / 86.8 / 80.7", "USD billion / % / %", "actual", "mu_fq4pr",
    "Revenue of $54.23 billion versus $41.46 billion for the prior quarter and $11.32 billion for the same period last year", "cat=all")
add("financials", "Micron revenue guidance", "FQ1 2027", "61.5 +/- 1.5", "USD billion", "forecast", "mu_fq4pr",
    "$61.5 billion ± $1.5 billion", "cat=all; non-GAAP GM ~86.25%; Micron: FQ1 is the floor for FY27 gross margin, then slower price rises")
add("financials", "Micron fiscal-year DRAM revenue", "FY2026", ">100", "USD billion", "actual", "mu_fq4",
    "for the fiscal year 2026 surpassed $100 billion.", "cat=all; sentence starts: Micron's DRAM revenue")

# ---------------- 2027 outlook ----------------
add("outlook", "Micron view of 2027-2028 tightness", "2027-2028", "much tighter than 2026", "-", "forecast", "mu_fq4",
    "We expect memory and storage supply-demand conditions to be much tighter in calendar 2027 and 2028", "cat=all; we do not have line of sight to when supply and demand will return to balance")
add("outlook", "Micron industry DRAM bit shipment growth", "2026 / 2027-2028", "mid-20s / low-20s", "% YoY", "forecast", "mu_fq4",
    "In DRAM, for calendar 2026, we expect industry bit shipments to grow in the mid-20s percentage range.", "cat=all; 2027-28 low-20s and supply constrained in both years; HBM bits grow faster")
add("outlook", "SK hynix view on demand exceeding supply", "to 2030", "persists through 2030", "-", "forecast", "hx_3q26",
    "it expects the structure in which demand exceeds supply to persist through 2030", "cat=all")
add("outlook", "Samsung view on 2027 supply", "2027-2028", "tighter in 2027; imbalance through 2028", "-", "forecast", "ss_2q26",
    "the imbalance expected to persist through 2028", "cat=all; Yonhap via TF; Reuters 2026-10-29: Samsung expects chip supply to tighten further in 2027; 2027 HBM supply effectively sold out")
add("outlook", "server CPU shipment growth", "2027", ">40", "% YoY", "forecast", "tf_list1",
    "Server CPU Shipments Projected to Grow Over 40% YoY in 2027, with Arm-Based Products Continuing to Gain Market Share", "cat=server-ecc; headline only (listing page), body not read; compare RDIMM bit supply +15-20%")
add("outlook", "DRAM sufficiency ratio", "2026", "-1 to -2", "%", "estimate", "tf_2027",
    "TrendForce estimates the DRAM sufficiency ratio at approximately -1% to -2% in 2026.", "cat=all; gap expected to widen further in 2027")
add("outlook", "server DRAM price path", "2H26-2H27", "rising each quarter", "-", "forecast", "tf_srv3q26",
    "continue rising quarterly from the second half of 2026 through the second half of 2027", "cat=server-ecc; gains may slow; a server DRAM shortage is already anticipated for 2027")
add("outlook", "PC DRAM supply", "2027", "could decline", "-", "forecast", "tf_4q26",
    "the PC DRAM supply could decline in 2027 as more capacity shifts to server applications.", "cat=ddr5")
add("outlook", "LPDDR5X supply (NVIDIA planning view)", "2027", "constrained through 2027", "-", "forecast", "tf_rubin",
    "LPDDR5X supply constraints are likely to continue through 2027", "cat=lpddr; NVIDIA halved SOCAMM capacity for Vera Rubin")
add("outlook", "HBM bit shipment growth", "2027", "50 to 60", "% YoY", "forecast", "tf_rubin",
    "HBM bit shipments are projected to grow by 50–60% YoY in 2027", "cat=hbm; still short of demand; HBM supply-constrained in 2027")
add("outlook", "memory contract prices", "2027", "broadly elevated", "-", "forecast", "tf_cspmem",
    "memory contract prices to remain broadly elevated in 2027.", "cat=all")
add("outlook", "memory market revenue", "2026 / 2027", "551.6 / 842.7", "USD billion", "forecast", "tf_memrev",
    "projects the memory market to be worth $551.6 billion in 2026 and to surge to a peak of $842.7 billion in 2027.", "cat=all; Jan 2026 view; DRAM 2026 revenue could reach 404.3 USD billion (+144%)")
add("outlook", "memory market revenue (later TF view)", "2027", "1280", "USD billion", "forecast", "tf_list15",
    "Agentic AI Drives Structural Expansion in Memory Demand, Global Memory Market Projected to Reach US$1.28 Trillion by 2027", "cat=all; headline only (listing page), body not read; supersedes 842.7 figure")
add("outlook", "smartphone memory price volatility", "2027", "moderates", "-", "forecast", "cp_soc",
    "Price volatility is likely to moderate next year compared with 2026.", "cat=lpddr; Counterpoint")
add("outlook", "Xbox expectation for memory prices", "by fall 2027", "2", "x further rise", "forecast", "xbox",
    "storage and memory prices have surged 2.5x in recent months and are expected to double again by fall 2027.", "cat=all; OEM view, not a market forecast")

out = sys.argv[1]
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADER)
    for r in R:
        assert len(r) == 12, r
        assert r[11].startswith("cat="), r
        w.writerow(r)
print(len(R), "rows ->", os.path.abspath(out))
