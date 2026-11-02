"""Build sources/hbm-gddr.csv from hand-collected, cited rows (2026-10-30).

Every row carries the URL that was fetched (or the search-result snippet seen)
and a quote that holds the number. kind=derived rows show the formula in notes.
"""
import csv
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "sources", "hbm-gddr.csv")
HDR = ["segment", "metric", "period", "value", "unit", "kind", "publisher",
       "title", "url", "pub_date", "quote", "notes"]

# URLs
TF_2306 = "https://www.trendforce.com/presscenter/news/20230628-11734.html"
TF_2304 = "https://www.trendforce.com/presscenter/news/20230418-11647.html"
TF_2308 = "https://www.trendforce.com/presscenter/news/20230809-11785.html"
TF_2403 = "https://www.trendforce.com/presscenter/news/20240318-12081.html"
ASIAE = "https://view.asiae.co.kr/en/article/2024031817511235053"
TF_2405 = "https://www.trendforce.com/presscenter/news/20240506-12125.html"
TF_2409 = "https://www.trendforce.com/presscenter/news/20240930-12319.html"
TF_2502 = "https://www.trendforce.com/news/2025/02/07/news-where-is-the-spring-of-the-memory-market/"
TF_2505 = "https://www.trendforce.com/presscenter/news/20250522-12589.html"
TF_2510 = "https://www.trendforce.com/presscenter/news/20251030-12762.html"
TF_2512 = "https://www.trendforce.com/presscenter/news/20251218-12843.html"
TF_2601 = "https://www.trendforce.com/presscenter/news/20260120-12887.html"
TF_2604 = "https://www.trendforce.com/presscenter/news/20260408-13003.html"
TF_2606 = "https://www.trendforce.com/presscenter/news/20260602-13074.html"
TF_2609 = "https://www.trendforce.com/presscenter/news/20260929-13255.html"
TF_2609G = "https://www.trendforce.com/presscenter/news/20260930-13258.html"
TF_FMS25 = "https://files.futurememorystorage.com/proceedings/2025/20250805_BMKT-101-1_Avril-Wu.pdf"
YOLE_2402 = "https://www.edge-ai-vision.com/2024/02/generative-ai-high-performance-computing-to-fuel-high-bandwidth-memory-market-growth/"
YOLE_2506 = "https://www.edge-ai-vision.com/2025/06/memory-market-surges-beyond-expectations-almost-200-billion-in-2025-driven-by-hbm-ai/"
GREENBERG = "https://files.futurememorystorage.com/proceedings/2024/20240805_PDSC2_Intro_to_HBM_Greenberg.pdf"
BI = "https://assets.bbhub.io/professional/sites/41/Bloomberg-Intelligence-Gen-AI-Deep-Dive-2025.pdf"
MU_FQ1_25 = "https://investors.micron.com/static-files/21b50828-dd30-429f-9502-b1ebc452c6e3"
MU_FQ3_25 = "https://investors.micron.com/news/press-release/2025/Micron-Technology-Inc--Reports-Results-for-the-Third-Quarter-of-Fiscal-2025-06-25-2025/default.aspx"
MU_FQ4_25 = "https://storage.googleapis.com/magi-store/earnings/MU/2025-09-23_Q4_FY2025/03_outputs/transcript.html"
MU_FQ1_26 = "https://www.fool.com/earnings/call-transcripts/2025/12/17/micron-mu-q1-2026-earnings-call-transcript/"
MU_FQ3_26 = "https://stockanalysis.com/stocks/mu/transcripts/695617-q3-2026-post-call/"
MU_FQ4_26 = "https://www.fool.com/earnings/call-transcripts/2026/10/01/micron-mu-q4-2026-earnings-call-transcript/"
SKH_Q425 = "https://stockanalysis.com/quote/krx/000660/transcripts/397711-q4-2025/"
SKH_Q326 = "https://news.skhynix.com/en/q3-2026-business-results/"
MT_SKH = "https://www.mt.co.kr/en/industry/2026/10/28/2026102809411541123"
MT_SEC = "https://www.mt.co.kr/en/industry/2026/10/29/2026102911044261630"
SEC_Q425 = "https://irsvc.teletogether.com/sec/pdf/2025Q4_script_eng.pdf"
JOONG_SKH = "https://www.koreajoongangdaily.com/business/sk-hynix-expects-ai-memory-market-to-grow-30-a-year-to-2030/11945557"
JOONG_KB = "https://www.koreajoongangdaily.com/business/samsung-sk-hynix-dramatically-scaling-up-hbm-production-to-meet-rising-demand-recent-nvidia-deals/12391367"
UBS = "https://www.investing.com/news/stock-market-news/ubs-says-samsung-to-reach-market-share-parity-for-hbm-with-sk-hynix-by-2027-4684487"
GS = "https://www.itiger.com/news/1117469753"
MIRAE_DEC = "https://securities.miraeasset.com/bbs/download/2141014.pdf?attachmentId=2141014"
MIRAE_MAY = "https://img.securities.miraeasset.com/ezrlink/report/183/20260507085312437_en.pdf"
CP = "https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share"
SEMIA = "https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram"
ELEC = "https://www.thelec.net/news/articleView.html?idxno=5886"
NV_H200 = "https://www.nvidia.com/en-us/data-center/h200/"
NV_BWU = "https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era"
NV_RUBIN = "https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/"
NV_GTC25 = "https://s201.q4cdn.com/141608511/files/doc_downloads/2025/03/GTC2025_Keynote.pdf"
NV_CPX = "https://nvidianews.nvidia.com/news/nvidia-unveils-rubin-cpx-a-new-class-of-gpu-designed-for-massive-context-inference"
TH_CPX = "https://www.tomshardware.com/pc-components/gpus/nvidia-removes-rubin-cpx-accelerators-from-its-roadmap-groq-3-lpus-take-center-stage-as-cpx-is-removed"
NV_5090 = "https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/"
NV_PRO6000 = "https://www.nvidia.com/content/dam/en-zz/Solutions/data-center/rtx-pro-6000-blackwell-workstation-edition/workstation-blackwell-rtx-pro-6000-workstation-edition-nvidia-us-3519208-web.pdf"
AMD_325 = "https://ir.amd.com/news-events/press-releases/detail/1220/amd-delivers-leadership-ai-performance-with-amd-instinct-mi325x-accelerators"
AMD_400 = "https://www.amd.com/en/products/accelerators/instinct/mi400.html"
GOOG_IW = "https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack"
AWS_TRN3 = "https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-ec2-trn3-ultraservers/"
SKH_12H = "https://news.skhynix.com/en/sk-hynix-begins-volume-production-of-the-world-first-12-layer-hbm3e/"
TF_JEDEC = "https://www.trendforce.com/news/2025/04/21/news-jedec-finalizes-hbm4-standard-potentially-easing-pressure-on-hybrid-bonding-adoption/"
SILICON = "https://www.silicon.co.uk/cloud/ai/nvidia-ai-growth-604624"
NV_GTCDC = "https://www.nvidia.com/en-us/on-demand/session/gtcdc25-dc1204/"
DCD = "https://www.datacenterdynamics.com/en/news/nvidia-gpu-shipments-totaled-376m-in-2023-equating-to-a-98-market-share-report/"
JPR_Q424 = "https://www.jonpeddie.com/news/pc-aib-shipments-follow-seasonality-show-nominal-increase-for-q424/"
JPR_Q125 = "https://www.jonpeddie.com/news/q125-pc-graphics-add-in-board-shipments-increased-8-5-from-last-quarter-due-to-nvidias-blackwell-ramping-up/"
JPR_Q225 = "https://www.jonpeddie.com/news/q225-pc-graphics-add-in-board-shipments-increased-27-0-from-last-quarter/"
JPR_Q325 = "https://www.jonpeddie.com/news/global-add-in-board-market-8-8-billion-in-q325-with-a-cagr-of-0-7-to-2029/"
JPR_Q425 = "https://www.jonpeddie.com/news/q425-pc-graphics-aib-shipments-decreased-4-4-from-last-quarter-to-11-million-units-with-a-cagr-to-2029-of-5-9/"
JPR_Q226 = "https://www.jonpeddie.com/news/q226-pc-graphics-aib-shipments-increased-10-from-last-quarter-to-12-million-units/"
TH_2020 = "https://www.tomshardware.com/news/gpu-sales-report-q4-2020-jpr"
TS_2021 = "https://www.techspot.com/news/94070-graphics-card-shipments-surpassed-50-million-mark-last.html"
KGI = "https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/memory-sector-17112025e.pdf"

SNIP = "Search-result snippet only; source page not fetched verbatim."

R = []


def row(seg, metric, period, value, unit, kind, pub, title, url, date, quote, notes=""):
    R.append([seg, metric, period, value, unit, kind, pub, title, url, date, quote, notes])


# ---------------- HBM bits: share of DRAM bits ----------------
T = "HBM Prices to Increase by 5-10% in 2025, Accounting for Over 30% of Total DRAM Value, Says TrendForce"
q = "HBM's share of total DRAM bit capacity is estimated to rise from 2% in 2023 to 5% in 2024 and surpass 10% by 2025."
row("hbm", "share_of_dram_bit_capacity", "2023", "2", "%", "estimate", "TrendForce", T, TF_2405, "2024-05-06", q)
row("hbm", "share_of_dram_bit_capacity", "2024", "5", "%", "forecast", "TrendForce", T, TF_2405, "2024-05-06", q)
row("hbm", "share_of_dram_bit_capacity", "2025", ">10", "%", "forecast", "TrendForce", T, TF_2405, "2024-05-06", q,
    "Superseded: TrendForce 2026-06-02 puts 2025 at about 8% of bit supply.")
row("hbm", "share_of_dram_bit_output", "2025", "10", "%", "forecast", "TrendForce",
    "HBM3e 12-Hi Faces Yield Learning Curve and Customer Validation Challenges; 2025 HBM Supply Outlook Remains Uncertain, Says TrendForce",
    TF_2409, "2024-09-30", "HBM will account for 10% of total DRAM bit output in 2025, doubling its share in 2024")
T = "Tight DRAM Supply Gives Suppliers Greater Pricing Power in HBM, with HBM Contract Prices Expected to Surge Multiples Higher in 2027, Says TrendForce"
q = "HBM bit supply is expected to represent approximately 8%, 9%, and 13% of total DRAM bit supply"
for p, v in (("2025", "8"), ("2026", "9"), ("2027", "13")):
    row("hbm", "share_of_dram_bit_supply", p, v, "%", "estimate" if p == "2025" else "forecast", "TrendForce", T, TF_2606, "2026-06-02", q,
        "End-of-year basis, top three suppliers. Best current TrendForce bit-share series.")
q = "approximately 18%, 22%, and 30% of total DRAM wafer input by the end of 2025, 2026, and 2027, respectively"
for p, v in (("2025", "18"), ("2026", "22"), ("2027", "30")):
    row("hbm", "share_of_dram_wafer_input", p, v, "%", "estimate" if p == "2025" else "forecast", "TrendForce", T, TF_2606, "2026-06-02", q,
        "Top three suppliers, end of year. Wafer share / bit share gives implied trade ratio.")
row("hbm", "implied_wafer_per_bit_ratio_vs_dram_avg", "2025", "2.25", "x", "derived", "TrendForce", T, TF_2606, "2026-06-02",
    "approximately 18%, 22%, and 30% of total DRAM wafer input ... approximately 8%, 9%, and 13% of total DRAM bit supply",
    "Derived: 18/8 = 2.25 (2025); 22/9 = 2.44 (2026); 30/13 = 2.31 (2027). Ratio vs the all-DRAM average, so lower than the HBM-vs-DDR5 trade ratio.")
row("hbm", "share_of_dram_bit_shipments", "2023", "2", "%", "estimate", "Yole Group (via Edge AI and Vision Alliance)",
    "Generative AI, High Performance Computing to Fuel High Bandwidth Memory Market Growth", YOLE_2402, "2024-02-13",
    "The share of HBM in overall DRAM bit shipments is forecast to rise from approximately 2% in 2023 to 6% by 2029")
row("hbm", "share_of_dram_bit_shipments", "2029", "6", "%", "forecast", "Yole Group (via Edge AI and Vision Alliance)",
    "Generative AI, High Performance Computing to Fuel High Bandwidth Memory Market Growth", YOLE_2402, "2024-02-13",
    "The share of HBM in overall DRAM bit shipments is forecast to rise from approximately 2% in 2023 to 6% by 2029",
    "Old (Feb 2024) forecast. Far below TrendForce 13% for 2027. Treat as superseded.")
row("hbm", "share_of_dram_market", "2023-03", "1.5", "%", "estimate", "The Elec (citing TrendForce)",
    "HBM Becomes a 'Black Hole' for DRAM Capacity, Share Surges Tenfold in Three Years", ELEC, "2026-03-17",
    "HBM accounted for only about 1.5% of the overall DRAM market as of March 2023.", "Metric (bits vs revenue vs capacity) not stated.")
row("hbm", "share_of_dram_production", "2026-03", "15", "%", "estimate", "The Elec",
    "HBM Becomes a 'Black Hole' for DRAM Capacity, Share Surges Tenfold in Three Years", ELEC, "2026-03-17",
    "High-bandwidth memory (HBM) now accounts for about 15% of total DRAM production.",
    "Based on Applied Materials CFO remark on wafers; this is a wafer share, not a bit share.")
row("hbm", "share_of_dram_wafers", "2026-03", "15", "%", "estimate", "Applied Materials (CFO Bryce Hill, via The Elec)",
    "HBM Becomes a 'Black Hole' for DRAM Capacity, Share Surges Tenfold in Three Years", ELEC, "2026-03-17",
    "about 15% of DRAM wafers are now allocated to HBM production.", "Said at Cantor Fitzgerald conference 2026-03-10.")

# ---------------- HBM bits: absolute ----------------
row("hbm", "demand_bits", "2023", "290", "million GB", "forecast", "TrendForce",
    "AI and HPC Demand Set to Boost HBM Volume by Almost 60% in 2023, Says TrendForce", TF_2306, "2023-06-28",
    "global demand for HBM will experience almost 60% growth annually in 2023, reaching 290 million GB",
    "Demand, not supply. = 2.32 billion Gb.")
row("hbm", "demand_bits", "2023", "2.32", "billion Gb", "derived", "TrendForce",
    "AI and HPC Demand Set to Boost HBM Volume by Almost 60% in 2023, Says TrendForce", TF_2306, "2023-06-28",
    "reaching 290 million GB", "Derived: 290 million GB x 8 Gb/GB = 2.32 billion Gb.")
row("hbm", "demand_bits", "2022", "181", "million GB", "derived", "TrendForce",
    "AI and HPC Demand Set to Boost HBM Volume by Almost 60% in 2023, Says TrendForce", TF_2306, "2023-06-28",
    "almost 60% growth annually in 2023, reaching 290 million GB", "Derived: 290 / 1.6 = 181 million GB (= 1.45 billion Gb). Approximate.")
row("hbm", "demand_growth_yoy", "2024", "30", "%", "forecast", "TrendForce",
    "AI and HPC Demand Set to Boost HBM Volume by Almost 60% in 2023, Says TrendForce", TF_2306, "2023-06-28",
    "with a further 30% growth in 2024.", "Superseded by ~200% (TrendForce 2024-05-06).")
row("hbm", "supply_bit_growth_yoy", "2024", "105", "%", "forecast", "TrendForce",
    "Suppliers Amp Up Production, HBM Bit Supply Projected to Soar by 105% in 2024", TF_2308, "2023-08-09",
    "a remarkable 105% annual increase in HBM bit supply by 2024.", "Superseded by 260% (2024-03-18).")
row("hbm", "supply_bit_growth_yoy", "2024", "260", "%", "forecast", "TrendForce",
    "HBM Supply Bit Growth Estimated to Reach 260%, Making Up 14% of DRAM Industry, Says TrendForce", TF_2403, "2024-03-18",
    "with an estimated annual supply bit growth of around 260%.")
row("hbm", "demand_bit_growth_yoy", "2024", "~200", "%", "forecast", "TrendForce", T, TF_2405, "2024-05-06",
    "the annual growth rate of HBM demand will approach 200% in 2024 and is expected to double in 2025.")
row("hbm", "demand_bit_growth_yoy", "2025", "~100", "%", "forecast", "TrendForce", T, TF_2405, "2024-05-06",
    "the annual growth rate of HBM demand will approach 200% in 2024 and is expected to double in 2025.",
    "'Double' read as about +100%.")
row("hbm", "demand_bit_growth_yoy", "2025", ">130", "%", "estimate", "TrendForce",
    "Strong Demand from CSPs and Sovereign Cloud to Drive Over 20% Growth in AI Server Shipments by 2026, Says TrendForce",
    TF_2510, "2025-10-30", "AI chip shipments in 2025 alone are projected to boost HBM demand by over 130%.")
row("hbm", "demand_bit_growth_yoy", "2026", ">70", "%", "forecast", "TrendForce",
    "Strong Demand from CSPs and Sovereign Cloud to Drive Over 20% Growth in AI Server Shipments by 2026, Says TrendForce",
    TF_2510, "2025-10-30", "In 2026, HBM usage will keep rising—still surpassing 70% annual growth")
row("hbm", "shipments_bits", "2026", ">30", "billion Gb", "forecast", "TrendForce",
    "HBM4 Raises the Bar on Manufacturing Complexity, Premium Expected to Exceed 30%, Says TrendForce", TF_2505, "2025-05-22",
    "TrendForce forecasts total HBM shipments to surpass 30 billion gigabits in 2026.", "Best TrendForce absolute anchor.")
row("hbm", "shipments_bits", "2024", "1182", "million GB", "estimate", "Marc Greenberg (FMS 2024; data likely Yole)",
    "Intro to HBM (FMS 2024 PDSC2)", GREENBERG, "2024-08-05",
    "2024: about 1,182 million GB, which is about 9.46 billion Gb",
    SNIP + " PDF fetch timed out. = 9.46 billion Gb. Source firm not confirmed.")
row("hbm", "shipments_bits", "2025", "1696", "million GB", "forecast", "Marc Greenberg (FMS 2024; data likely Yole)",
    "Intro to HBM (FMS 2024 PDSC2)", GREENBERG, "2024-08-05",
    "2025: about 1,696 million GB, which is about 13.57 billion Gb",
    SNIP + " PDF fetch timed out. = 13.57 billion Gb. Old forecast, likely too low.")
T = "UBS says Samsung to reach market share parity for HBM with SK Hynix by 2027"
row("hbm", "end_demand_bits", "2026", "32.9", "billion Gb", "forecast", "UBS (via Investing.com)", T, UBS, "2026-05-13",
    "total HBM end-demand forecast to 32.9 billion gigabits for 2026, up 88% year-on-year.")
row("hbm", "end_demand_bits", "2027", "58.0", "billion Gb", "forecast", "UBS (via Investing.com)", T, UBS, "2026-05-13",
    "58.0 billion gigabits for 2027, up 76%.")
row("hbm", "end_demand_bits", "2025", "17.5", "billion Gb", "derived", "UBS (via Investing.com)", T, UBS, "2026-05-13",
    "32.9 billion gigabits for 2026, up 88% year-on-year.", "Derived: 32.9 / 1.88 = 17.5 billion Gb.")
row("hbm-samsung", "shipments_bits", "2026", "9.7", "billion Gb", "forecast", "UBS (via Investing.com)", T, UBS, "2026-05-13",
    "HBM shipment forecasts for Samsung at 9.7 billion gigabits for 2026, representing 124% year-over-year growth.")
row("hbm-samsung", "shipments_bits", "2027", "23", "billion Gb", "forecast", "UBS (via Investing.com)", T, UBS, "2026-05-13",
    "raising its 2027 estimate to 23 billion gigabits, up 137% year-on-year")
row("hbm-skhynix", "shipments_bits", "2026", "17.7", "billion Gb", "forecast", "UBS (via Investing.com)", T, UBS, "2026-05-13",
    "lowering 2026 estimates to 17.7 billion gigabits from 18.4 billion previously.")
row("hbm-skhynix", "shipments_bits", "2027", "23.1", "billion Gb", "forecast", "UBS (via Investing.com)", T, UBS, "2026-05-13",
    "2027 estimates to 23.1 billion gigabits from 24.7 billion.")
row("hbm", "bit_share_by_vendor", "2027", "SKH ~40 / Samsung ~40 / Micron ~20", "%", "forecast", "UBS (via Investing.com)", T, UBS, "2026-05-13",
    "each hold approximately 40% of the HBM bit market share in 2027 ... Micron accounting for the remaining 20%.")
T = "Samsung, SK hynix dramatically scaling up HBM production to meet rising demand, recent Nvidia deals"
row("hbm-samsung", "shipments_bits", "2026", "11.2", "billion Gb", "forecast", "KB Securities (via Korea JoongAng Daily)", T, JOONG_KB, "2026-01-04",
    "Samsung's HBM bit shipments in 2026 are expected to triple year on year to 11.2 billion gigabits",
    "Also: HBM4 roughly half of Samsung 2026 shipments.")
# Mirae Dec 2025 vendor tables
T = "[2026 Outlook Report] Semiconductors: Robust earnings cycle ahead"
qs = "Shipments (bn Gb) 0.6 0.9 1.5 2.0 2.1 2.5 3.1 3.8 5.1 5.0 11.6 16.9 (columns 1Q25..4Q26F, 2024, 2025F, 2026F, 2027F)"
for p, v, k in (("2024", "5.1", "actual"), ("2025", "5.0", "estimate"), ("2026", "11.6", "forecast"), ("2027", "16.9", "forecast")):
    row("hbm-samsung", "shipments_bits", p, v, "billion Gb", k, "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15", qs,
        "Samsung HBM table, p.31. 2024 is Mirae's figure for a past year (company data + estimate).")
qk = "Bit shipments (bn Gb) 2.6 2.9 3.2 3.8 3.4 3.9 4.2 4.6 6.1 12.4 16.1 18.5 (HBM rows, columns 1Q25..4Q26F, 2024, 2025F, 2026F, 2027F)"
for p, v, k in (("2024", "6.1", "actual"), ("2025", "12.4", "estimate"), ("2026", "16.1", "forecast"), ("2027", "18.5", "forecast")):
    row("hbm-skhynix", "shipments_bits", p, v, "billion Gb", k, "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15", qk,
        "SK hynix assumptions by product, p.35.")
qs2 = "HBM Revenue (US$ bn) 1.0 1.3 2.1 2.9 2.7 3.3 4.5 6.1 6.8 7.3 16.6 26.7"
for p, v, k in (("2024", "6.8", "actual"), ("2025", "7.3", "estimate"), ("2026", "16.6", "forecast"), ("2027", "26.7", "forecast")):
    row("hbm-samsung", "revenue", p, v, "USD bn", k, "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15", qs2, "Samsung HBM table, p.31.")
qk2 = "HBM Revenue (US$ bn) 4.3 5.2 5.7 6.8 5.4 6.6 7.7 9.1 10.1 22.1 28.8 33.6"
for p, v, k in (("2024", "10.1", "actual"), ("2025", "22.1", "estimate"), ("2026", "28.8", "forecast"), ("2027", "33.6", "forecast")):
    row("hbm-skhynix", "revenue", p, v, "USD bn", k, "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15", qk2, "SK hynix table, p.35.")
row("hbm-skhynix", "asp_per_gb_bit", "2025", "1.8", "USD/Gb", "estimate", "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15",
    "ASP (US$/Gb) 1.70 1.83 1.79 1.79 1.61 1.69 1.86 1.95 1.7 1.8 1.8 1.8",
    "HBM ASP per gigabit. Compare SK hynix conventional DRAM ASP 0.37 USD/Gb in 2025 (same table).")

# ---------------- HBM wafer capacity ----------------
T = "HBM Supply Bit Growth Estimated to Reach 260%, Making Up 14% of DRAM Industry, Says TrendForce"
row("hbm", "tsv_wafer_capacity", "2024-12", "250", "kwpm", "forecast", "TrendForce", T, TF_2403, "2024-03-18",
    "the DRAM industry is expected to allocate approximately 250K/m (14%) of total capacity to producing HBM TSV",
    "End-2024; 14% of total DRAM capacity.")
row("hbm", "tsv_share_of_dram_capacity", "2024-12", "14", "%", "forecast", "TrendForce", T, TF_2403, "2024-03-18",
    "approximately 250K/m (14%) of total capacity to producing HBM TSV")
row("hbm-samsung", "tsv_wafer_capacity", "2024-12", "130", "kwpm", "forecast", "TrendForce", T, TF_2403, "2024-03-18",
    "Samsung's total HBM capacity is expected to reach around 130K (including TSV) by year-end; SK hynix is around 120K")
row("hbm-skhynix", "tsv_wafer_capacity", "2024-12", "120", "kwpm", "forecast", "TrendForce", T, TF_2403, "2024-03-18",
    "Samsung's total HBM capacity is expected to reach around 130K (including TSV) by year-end; SK hynix is around 120K",
    "Asia Business Daily version: 120,000-125,000.")
TA = "TrendForce \"HBM Share in DRAM Sales to Rise to 20% This Year\""
qa = "based on wafer capacity, HBM production capacity was 45,000 wafers per month each for Samsung Electronics and SK Hynix"
row("hbm-samsung", "wafer_capacity", "2023", "45", "kwpm", "estimate", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18", qa)
row("hbm-skhynix", "wafer_capacity", "2023", "45", "kwpm", "estimate", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18", qa)
row("hbm-micron", "wafer_capacity", "2023", "3", "kwpm", "estimate", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18",
    "3,000 wafers per month for Micron")
row("hbm-micron", "wafer_capacity", "2024", "20", "kwpm", "forecast", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18",
    "Micron's to 20,000 wafers per month")
T2 = "HBM3e 12-Hi Faces Yield Learning Curve and Customer Validation Challenges; 2025 HBM Supply Outlook Remains Uncertain, Says TrendForce"
row("hbm-samsung", "tsv_wafer_capacity", "2025-12", "170", "kwpm", "forecast", "TrendForce", T2, TF_2409, "2024-09-30",
    "increase its TSV production from 120K wafers per month at the end of 2024 to 170K wafers by the end of 2025",
    "Note: end-2024 Samsung given as 120K here vs 130K in March 2024 release.")
row("hbm-skhynix", "tsv_capacity_growth", "2025", "25", "%", "forecast", "TrendForce", T2, TF_2409, "2024-09-30",
    "SK hynix, in turn, is planning a 25% capacity increase over the same period.")
TY = "Generative AI, High Performance Computing to Fuel High Bandwidth Memory Market Growth"
qy = "increased from 44,000 wafers per month (WPM) in 2022 to 74K WPM in 2023 and could grow to 151K WPM in 2024."
for p, v, k in (("2022", "44", "actual"), ("2023", "74", "estimate"), ("2024", "151", "forecast")):
    row("hbm", "wafer_production", p, v, "kwpm", k, "Yole Group (via Edge AI and Vision Alliance)", TY, YOLE_2402, "2024-02-13", qy,
        "Industry HBM wafer production; Yole basis differs from TrendForce TSV capacity (TrendForce end-2024 ~250K).")
TF = "TrendForce presentation at FMS 2025 (Avril Wu)"
qf = "Samsung | ~655k | ~150k (~23%) | ~670k | ~150k (~22%); SK hynix | ~545k | ~150k (~28%) | ~600k | ~200k (~33%); Micron | ~340k | ~55k (~16%) | ~360k | ~100k (~28%)"
nf = SNIP + " PDF returned 403/timeout. Columns: total DRAM end-2025, HBM/TSV end-2025, total end-2026, HBM/TSV end-2026."
for seg, p, v in (("hbm-samsung", "2025-12", "150"), ("hbm-samsung", "2026-12", "150"),
                  ("hbm-skhynix", "2025-12", "150"), ("hbm-skhynix", "2026-12", "200"),
                  ("hbm-micron", "2025-12", "55"), ("hbm-micron", "2026-12", "100")):
    row(seg, "tsv_wafer_capacity", p, v, "kwpm", "estimate" if p == "2025-12" else "forecast", "TrendForce", TF, TF_FMS25, "2025-08-05", qf, nf)
row("hbm", "tsv_wafer_capacity_top3", "2025-12", "355", "kwpm", "derived", "TrendForce", TF, TF_FMS25, "2025-08-05", qf,
    "Derived: 150+150+55. 2026-12: 150+200+100 = 450. " + SNIP)
row("hbm", "tsv_wafer_capacity_top3", "2026-12", "450", "kwpm", "derived", "TrendForce", TF, TF_FMS25, "2025-08-05", qf,
    "Derived: 150+200+100. " + SNIP)
T = "Samsung, SK hynix dramatically scaling up HBM production to meet rising demand, recent Nvidia deals"
row("hbm-samsung", "hbm_wafer_output", "2026-12", "250", "kwpm", "forecast", "KB Securities / Korean media (via Korea JoongAng Daily)", T, JOONG_KB, "2026-01-04",
    "Until the end of 2026, HBM wafer monthly output is expected to reach 250,000 units",
    "Article context is Samsung; 'a more than 47 percent jump compared to the current 170,000 level'. Ambiguous whether Samsung-only.")
row("hbm-skhynix", "m15x_wafer_capacity", "2027-06", "50", "kwpm", "forecast", "Korea JoongAng Daily", T, JOONG_KB, "2026-01-04",
    "Full utilization of the plant is projected by mid-2027, with monthly output estimated at around 50,000 wafers",
    "M15X total wafers; M15X is the SK hynix HBM fab.")
T = "China's CXMT Is Set to Challenge DRAM Incumbents"
q = "By the end of 2025, we believe only ~5 kwspm of CXMT's ~265 kwspm of capacity is allocated to HBM."
row("hbm-cxmt", "hbm_wafer_capacity", "2025-12", "5", "kwpm", "estimate", "SemiAnalysis", T, SEMIA, "2026-06-23", q, "Partly paywalled.")
q = "We think this figure will increase to nearly ~30 kwspm and ~55kwspm by the end of 2026 and 2027 respectively."
row("hbm-cxmt", "hbm_wafer_capacity", "2026-12", "30", "kwpm", "forecast", "SemiAnalysis", T, SEMIA, "2026-06-23", q)
row("hbm-cxmt", "hbm_wafer_capacity", "2027-12", "55", "kwpm", "forecast", "SemiAnalysis", T, SEMIA, "2026-06-23", q)
row("hbm-cxmt", "hbm_wafer_capacity", "2028-12", "100", "kwpm", "forecast", "SemiAnalysis", T, SEMIA, "2026-06-23",
    "We estimate CXMT's HBM wafer capacity will reach 55kwspm and 100kwspm in 2027 and 2028, respectively.")
row("hbm-cxmt", "share_of_global_hbm_wafer_supply", "2028", "12", "%", "forecast", "SemiAnalysis", T, SEMIA, "2026-06-23",
    "This would increase the company's share of global HBM wafer supply from 1% in 2025 to 12% in 2028.",
    "Implies global HBM wafers ~833 kwpm in 2028 (100/0.12) and ~500 kwpm in 2025 (5/0.01); the 2025 implied value is above TrendForce top-3 ~355 kwpm, so rounding is coarse.")
T = "Goldman Sachs Endorses Storage PE Valuation, Raises Price Targets for SK Hynix, Samsung, and Kioxia"
row("hbm", "share_of_cleanroom_capacity", "2026-2030", "30", "%", "forecast", "Goldman Sachs (via Tiger Brokers/Deep News)", T, GS, "2026-06-01",
    "Between 2026 and 2030, approximately 30% of the combined available cleanroom capacity of the three major manufacturers (about 1.39 million to 1.54 million wafers per month) will be mandatorily allocated for HBM production",
    "Secondary report of a GS note. Implies ~420-460 kwpm for HBM.")

# ---------------- trade ratio ----------------
row("hbm", "wafer_trade_ratio_vs_ddr5", "2025", "3", "x", "actual", "Micron (FQ1 2026 call)", "Micron (MU) Q1 2026 Earnings Call Transcript",
    MU_FQ1_26, "2025-12-17", "the three-to-one trade ratio with DDR5, and this trade ratio only increases with future generations of HBM")
row("hbm", "wafer_trade_ratio_vs_ddr5", "2027", ">3 (rising with HBM4/HBM4E)", "x", "forecast", "Micron (FQ4 2026 call)",
    "Micron (MU) Q4 2026 Earnings Call Transcript", MU_FQ4_26, "2026-09-30",
    "shifting from HBM3 to HBM4 and then towards later in the year in '27 HBM4E and these are increasing trade ratio",
    "No number given; qualitative.")
row("hbm", "wafer_area_ratio_vs_conventional", "2026", "3", "x", "estimate", "Applied Materials (via The Elec)",
    "HBM Becomes a 'Black Hole' for DRAM Capacity, Share Surges Tenfold in Three Years", ELEC, "2026-03-17",
    "producing HBM with the same capacity as conventional DRAM requires about three times more wafer area.")
row("hbm", "wafer_ratio_vs_standard_dram", "2026", "3-4", "x", "estimate", "Goldman Sachs (via Tiger Brokers)",
    "Goldman Sachs Endorses Storage PE Valuation, Raises Price Targets for SK Hynix, Samsung, and Kioxia", GS, "2026-06-01",
    "HBM production requires 3-4 times the wafer capacity of standard DRAM.")
row("hbm", "yield_gap_vs_ddr5", "2024", "20-30", "% lower", "estimate", "TrendForce",
    "HBM Supply Bit Growth Estimated to Reach 260%, Making Up 14% of DRAM Industry, Says TrendForce", TF_2403, "2024-03-18",
    "The yield rate (including TSV packaging) for HBM is approximately 20–30% lower than that of DDR5")

# ---------------- HBM revenue / TAM ----------------
TA = "TrendForce \"HBM Share in DRAM Sales to Rise to 20% This Year\""
qa = "the proportion of HBM in total DRAM sales is expected to rise from 2.6% in 2022 and 8.4% in 2023 to 20.1% this year"
qd = "$80 billion in 2022 and $51.8 billion in 2023 ... will increase to $84.2 billion by the end of 2024"
row("hbm", "share_of_dram_revenue", "2022", "2.6", "%", "actual", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18", qa)
row("hbm", "share_of_dram_revenue", "2023", "8.4", "%", "estimate", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18", qa)
row("hbm", "share_of_dram_revenue", "2024", "20.1", "%", "forecast", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18", qa)
row("hbm", "revenue", "2022", "2.08", "USD bn", "derived", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18", qd,
    "Derived: 2.6% x $80B = $2.08B.")
row("hbm", "revenue", "2023", "4.35", "USD bn", "derived", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18", qd,
    "Derived: 8.4% x $51.8B = $4.35B.")
row("hbm", "revenue", "2024", "16.9", "USD bn", "derived", "TrendForce (via Asia Business Daily)", TA, ASIAE, "2024-03-18", qd,
    "Derived forecast: 20.1% x $84.2B = $16.9B (Mar 2024 view).")
row("hbm", "share_of_dram_value", "2025", ">30", "%", "forecast", "TrendForce",
    "HBM Prices to Increase by 5-10% in 2025, Accounting for Over 30% of Total DRAM Value, Says TrendForce", TF_2405, "2024-05-06",
    "more than 20% of the total DRAM market value starting in 2024, potentially exceeding 30% by 2025.")
row("hbm", "revenue", "2024", "8.9", "USD bn", "forecast", "TrendForce",
    "Suppliers Amp Up Production, HBM Bit Supply Projected to Soar by 105% in 2024", TF_2308, "2023-08-09",
    "total HBM revenue to a whopping US$8.9 billion in 2024—a 127% YoY increase.",
    "Aug 2023 view; far below later 2024 estimates ($14-17B). Implies 2023 = 8.9/2.27 = $3.9B.")
TY = "Generative AI, High Performance Computing to Fuel High Bandwidth Memory Market Growth"
row("hbm", "revenue", "2023", "5.5", "USD bn", "estimate", "Yole Group (via Edge AI and Vision Alliance)", TY, YOLE_2402, "2024-02-13",
    "after having soared by more than 150% year on year from around $5.5 billion in 2023.")
row("hbm", "revenue", "2024", "14", "USD bn", "forecast", "Yole Group (via Edge AI and Vision Alliance)", TY, YOLE_2402, "2024-02-13",
    "the share is anticipated to climb from $14 billion in 2024 to $38 billion in 2029")
row("hbm", "revenue", "2029", "38", "USD bn", "forecast", "Yole Group (via Edge AI and Vision Alliance)", TY, YOLE_2402, "2024-02-13",
    "the share is anticipated to climb from $14 billion in 2024 to $38 billion in 2029", "Superseded by Yole 2025 ($98B in 2030).")
TY2 = "Memory Market Surges Beyond Expectations: Almost $200B in 2025, Driven by HBM and AI"
row("hbm", "revenue", "2025", "34", "USD bn", "forecast", "Yole Group (via Edge AI and Vision Alliance)", TY2, YOLE_2506, "2025-06-19",
    "In 2025, HBM revenue is set to nearly double to ~$34 billion.", "Implies 2024 ~ $17B.")
row("hbm", "revenue", "2030", "98", "USD bn", "forecast", "Yole Group (via Edge AI and Vision Alliance)", TY2, YOLE_2506, "2025-06-19",
    "HBM expected to nearly double revenue in 2025, projected to reach approximately $98 billion by 2030.")
row("hbm", "revenue_cagr", "2025-2030", "33", "%", "forecast", "Yole Group (via Edge AI and Vision Alliance)", TY2, YOLE_2506, "2025-06-19",
    "Yole Group projects a 33% CAGR for HBM through 2030, with revenue exceeding 50% of the DRAM market.")
row("hbm", "share_of_dram_revenue", "2030", ">50", "%", "forecast", "Yole Group (via Edge AI and Vision Alliance)", TY2, YOLE_2506, "2025-06-19",
    "Yole Group projects a 33% CAGR for HBM through 2030, with revenue exceeding 50% of the DRAM market.")
row("hbm-skhynix", "share_of_hbm_revenue_and_bits", "2024", "54", "%", "estimate", "Yole Group (via Edge AI and Vision Alliance)", TY2, YOLE_2506, "2025-06-19",
    "SK hynix leads with ~54% market share in HBM revenue and bit shipments")
TB = "Generative AI 2025 Outlook (Bloomberg Intelligence Gen AI Deep Dive)"
qb = "can grow at a compound annual rate exceeding 40% to reach sales of $130 billion in 2033, from just $4 billion in 2023 , based on our scenario analysis."
row("hbm", "revenue", "2023", "4", "USD bn", "estimate", "Bloomberg Intelligence", TB, BI, "2025-03-24", qb)
row("hbm", "revenue", "2033", "130", "USD bn", "forecast", "Bloomberg Intelligence", TB, BI, "2025-03-24", qb, "Scenario analysis; CAGR >40% 2023-2033.")
row("hbm", "tam", "2024", "16", "USD bn", "estimate", "Micron (FQ1 2025 call)", "Micron FQ1 2025 earnings materials", MU_FQ1_25, "2024-12-18",
    "In 2028, we expect the HBM total addressable market (TAM) to grow four times from the $16 billion level in 2024 and to exceed $100 billion by 2030.",
    SNIP + " Micron static file redirects; quote as returned by search.")
row("hbm", "tam", "2030", ">100", "USD bn", "forecast", "Micron (FQ1 2025 call)", "Micron FQ1 2025 earnings materials", MU_FQ1_25, "2024-12-18",
    "In 2028, we expect the HBM total addressable market (TAM) to grow four times from the $16 billion level in 2024 and to exceed $100 billion by 2030.",
    SNIP + " Superseded twice.")
row("hbm", "tam", "2025", "35", "USD bn", "estimate", "Micron (FQ1 2026 call)", "Micron (MU) Q1 2026 Earnings Call Transcript", MU_FQ1_26, "2025-12-17",
    "from approximately $35 billion in 2025 to around $100 billion in 2028")
row("hbm", "tam", "2028", "100", "USD bn", "forecast", "Micron (FQ1 2026 call)", "Micron (MU) Q1 2026 Earnings Call Transcript", MU_FQ1_26, "2025-12-17",
    "from approximately $35 billion in 2025 to around $100 billion in 2028")
row("hbm", "tam_cagr", "2025-2028", "40", "%", "forecast", "Micron (FQ1 2026 call)", "Micron (MU) Q1 2026 Earnings Call Transcript", MU_FQ1_26, "2025-12-17",
    "We forecast an HBM TAM CAGR of approximately 40% through calendar 2028")
row("hbm", "tam", "2027", ">100", "USD bn", "forecast", "Micron (FQ3 2026 call, CFO Mark Murphy)", "Micron Q3 2026 post-earnings call transcript", MU_FQ3_26, "2026-06-24",
    "We see that now, the HBM TAM easily crossing $100 billion in 2027.", "Latest Micron view; not updated on FQ4 2026 call.")
T = "Goldman Sachs Endorses Storage PE Valuation, Raises Price Targets for SK Hynix, Samsung, and Kioxia"
q = "the HBM market size for 2026, 2027, and 2028 to reach $56 billion, $116 billion, and $168 billion"
for p, v in (("2026", "56"), ("2027", "116"), ("2028", "168")):
    row("hbm", "tam", p, v, "USD bn", "forecast", "Goldman Sachs (via Tiger Brokers/Deep News)", T, GS, "2026-06-01", q,
        "Secondary report of GS note; 2027 revised up 54%.")
row("hbm-samsung", "revenue", "2027", "44", "USD bn", "forecast", "Goldman Sachs (via Tiger Brokers/Deep News)", T, GS, "2026-06-01",
    "Its HBM revenue is expected to surge to approximately $44 billion by 2027.")
row("hbm", "supply_demand_gap", "2027", "-6.0", "%", "forecast", "Goldman Sachs (via Tiger Brokers/Deep News)", T, GS, "2026-06-01",
    "HBM: The shortage is most critical, with gaps projected at -5.4%, -6.0%, and -4.3%, respectively.", "2026 -5.4%, 2027 -6.0%, 2028 -4.3%.")
row("hbm", "market_cagr", "2025-2030", "30", "%", "forecast", "SK hynix (Choi Joon-yong, via Reuters/Korea JoongAng Daily)",
    "SK hynix expects AI memory market to grow 30% a year to 2030", JOONG_SKH, "2025-08-11",
    "will grow 30 percent a year until 2030")
row("hbm-skhynix", "revenue", "2026", "54", "KRW tn", "forecast", "Mirae Asset Securities", "SK Hynix: Rising toward where it belongs", MIRAE_MAY, "2026-05-07",
    "we forecast to reach W54tr (+72% YoY) in 2026 and W75t r (+W21tr YoY) in 2027 ( 2027 HBM ASP growth projected at + 19.7 %)",
    "HBM revenue (word dropped in PDF text extraction).")
row("hbm-skhynix", "revenue", "2027", "75", "KRW tn", "forecast", "Mirae Asset Securities", "SK Hynix: Rising toward where it belongs", MIRAE_MAY, "2026-05-07",
    "we forecast to reach W54tr (+72% YoY) in 2026 and W75t r (+W21tr YoY) in 2027")
row("hbm-micron", "revenue_quarter", "FQ4-2025", "~2", "USD bn", "actual", "Micron (FQ4 2025 call)", "Micron FY2025 Q4 Earnings Call Transcript", MU_FQ4_25, "2025-09-23",
    "In fiscal Q4, our HPM revenue grew to nearly $2 billion, implying an annualized run rate of nearly $8 billion",
    "Transcript renders HBM as HPM.")
row("hbm-micron", "revenue_run_rate", "FQ3-2025", ">6", "USD bn/yr", "actual", "Micron", "Micron Reports Results for the Third Quarter of Fiscal 2025", MU_FQ3_25, "2025-06-25",
    "HBM annualized revenue run rate was more than $6 billion", SNIP + " HBM revenue grew nearly 50% QoQ.")
q = "In Q2 2026, SK Hynix maintained its top position with 50%, but showed a decline compared to 64% in the same period of the previous year."
for p, s, m, mu in (("2025Q2", "64", "15", "21"), ("2025Q3", "56", "23", "21"), ("2025Q4", "57", "22", "21"),
                    ("2026Q1", "58", "21", "21"), ("2026Q2", "50", "33", "18")):
    row("hbm", "revenue_share_SKH/Samsung/Micron", p, f"{s}/{m}/{mu}", "%", "actual", "Counterpoint Research",
        "Global DRAM and HBM Market Share: Quarterly", CP, "2026-09-02", q, "Table values; quote covers 2026Q2 and 2025Q2 SK hynix.")
row("hbm", "vendor_share_SKH/Samsung/Micron", "2022", "50/40/10", "%", "actual", "TrendForce",
    "HBM Supply Leader SK Hynix's Market Share to Exceed 50% in 2023 Due to Demand for AI Servers, Says TrendForce", TF_2304, "2023-04-18",
    "the top three HBM suppliers in 2022 were SK hynix, Samsung, and Micron, with 50%, 40%, and 10% market share, respectively")

# ---------------- prices ----------------
row("hbm", "price_multiple_vs_ddr5", "2024", "~5", "x", "estimate", "TrendForce",
    "HBM Prices to Increase by 5-10% in 2025, Accounting for Over 30% of Total DRAM Value, Says TrendForce", TF_2405, "2024-05-06",
    "HBM's unit sales price is several times higher than that of conventional DRAM and about five times that of DDR5.")
row("hbm", "price_multiple_vs_server_ddr5", "2026-12", "1-2", "x", "forecast", "TrendForce",
    "Higher DDR5 Profitability Intensifies Capacity Crowding, Strengthening HBM3e Pricing Momentum in 2026, Says TrendForce", TF_2512, "2025-12-18",
    "HBM3e prices were previously four to five times higher than server DDR5 ... the gap is expected to narrow to one to two times by the end of 2026")
row("hbm", "blended_asp_growth", "2027", "121", "%", "forecast", "TrendForce",
    "HBM Supply Constraints Persist, 2027 Price Outlook Revised Upward with Blended ASP Forecast to Rise 121% YoY, Says TrendForce", TF_2609, "2026-09-29",
    "Blended ASP is now projected to jump 121% YoY.", "Matters for revenue-to-bits conversion in 2027.")
row("hbm", "hbm4_price_premium_vs_hbm3e", "2026", ">30", "%", "forecast", "TrendForce",
    "HBM4 Raises the Bar on Manufacturing Complexity, Premium Expected to Exceed 30%, Says TrendForce", TF_2505, "2025-05-22",
    "HBM4's harder production is expected to drive premiums above 30%.")
row("hbm", "8hi_price_premium_per_gb_vs_12hi", "2027", "10-20", "%", "forecast", "TrendForce",
    "HBM Supply Constraints Persist, 2027 Price Outlook Revised Upward with Blended ASP Forecast to Rise 121% YoY, Says TrendForce", TF_2609, "2026-09-29",
    "TrendForce expects 8-Hi products to carry a roughly 10–20% price premium per Gb over 12-Hi products in 2027.",
    "Vendors may move from 12-Hi to 8-Hi in 2027, cutting HBM GB per device.")

# ---------------- generation mix ----------------
row("hbm", "hbm3_share_of_demand", "2023", "50", "%", "forecast", "TrendForce",
    "Suppliers Amp Up Production, HBM Bit Supply Projected to Soar by 105% in 2024", TF_2308, "2023-08-09",
    "the primary demand is shifting from HBM2e to HBM3 in 2023, with an anticipated demand ratio of approximately 50% and 39%, respectively.",
    "HBM2e 39% in 2023.")
row("hbm", "hbm3_share_of_demand", "2024", "60", "%", "forecast", "TrendForce",
    "Suppliers Amp Up Production, HBM Bit Supply Projected to Soar by 105% in 2024", TF_2308, "2023-08-09",
    "demand in 2024 will heavily lean toward HBM3 and eclipse HBM2e with a projected share of 60%.")
row("hbm", "hbm3e_share_of_bit_demand", "2025", ">80", "%", "forecast", "TrendForce", T2, TF_2409, "2024-09-30",
    "more than 80% of the total HBM bit demand in 2025 will be for HBM3e, with over half of this coming from 12-Hi models")
row("hbm", "12hi_share_of_hbm3e_demand", "2025", ">50", "%", "forecast", "TrendForce", T2, TF_2409, "2024-09-30",
    "more than 80% of the total HBM bit demand in 2025 will be for HBM3e, with over half of this coming from 12-Hi models")
row("hbm", "hbm4_mainstream_timing", "2026H2", "HBM4 overtakes HBM3e", "text", "forecast", "TrendForce",
    "HBM4 Raises the Bar on Manufacturing Complexity, Premium Expected to Exceed 30%, Says TrendForce", TF_2505, "2025-05-22",
    "ultimately overtaking HBM3e as the mainstream solution by the second half of 2026.")
row("hbm-samsung", "hbm4_share_of_hbm_revenue", "2026Q3", "60", "%", "actual", "Samsung (Q3 2026 call, via MoneyToday)",
    "Samsung Electronics says HBM4 sales tripled quarter-on-quarter, next year's HBM supply fully booked", MT_SEC, "2026-10-29",
    "HBM4 accounts for 60% of total HBM revenue.")
row("hbm-skhynix", "hbm4_overtakes_hbm3e", "2026Q4", "HBM4 > HBM3E in volume and revenue", "text", "forecast", "SK hynix",
    "SK hynix Announces 3Q26 Financial Results", SKH_Q326, "2026-10-28",
    "HBM4 to surpass HBM3E in both shipment volume and revenue in the fourth quarter")
row("nvidia", "blackwell_share_of_high_end_gpu_shipments", "2026", "71", "%", "forecast", "TrendForce",
    "Rubin Faces Delay Risks Amid Ongoing Supply Chain Adjustments; Blackwell to Account for Over 70% of NVIDIA's High-End GPU Shipments in 2026, Says TrendForce",
    TF_2604, "2026-04-08", "the Blackwell series is projected to grow markedly from 61% to 71%",
    "Rubin 29% -> 22%; Hopper 10% -> 7% (same release). Rubin delay partly from HBM4 validation.")

# ---------------- stack capacity ----------------
row("hbm", "stack_capacity_hbm3e_12hi", "2024", "36", "GB/stack", "actual", "SK hynix", "SK hynix Begins Volume Production of the World's First 12-Layer HBM3E",
    SKH_12H, "2024-09-26", "world's first 12-layer HBM3E ... 36GB per stack", SNIP)
row("hbm", "stack_capacity_hbm4_16hi_max", "2025", "64", "GB/stack", "actual", "TrendForce (JEDEC JESD270-4)",
    "JEDEC Finalizes HBM4 Standard, Potentially Easing Pressure on Hybrid Bonding Adoption", TF_JEDEC, "2025-04-21",
    "stacks 4, 8, 12 or 16 dies high, using either 24 Gb or 32 Gb dies",
    SNIP + " Derived: 16 x 32 Gb = 512 Gb = 64 GB; 16 x 24 Gb = 48 GB.")

# ---------------- accelerators: HBM per device ----------------
row("accelerator", "hbm_per_gpu_H100", "2023", "80", "GB", "actual", "NVIDIA", "Inside NVIDIA Blackwell Ultra", NV_BWU, "2025-08-22",
    "Hopper H100 (80 GB), Hopper H200 (141 GB), Blackwell (192 GB), and Blackwell Ultra (288 GB)")
row("accelerator", "hbm_per_gpu_H200", "2024", "141", "GB", "actual", "NVIDIA", "NVIDIA H200 product page", NV_H200, "2024",
    "the first GPU to offer 141 gigabytes (GB) of HBM3e memory at 4.8 terabytes per second (TB/s)")
row("accelerator", "hbm_per_gpu_B200", "2025", "192", "GB", "actual", "NVIDIA", "Inside NVIDIA Blackwell Ultra", NV_BWU, "2025-08-22",
    "\"192 GB HBM3E\" for Blackwell")
row("accelerator", "hbm_per_gpu_B300", "2025", "288", "GB", "actual", "NVIDIA", "Inside NVIDIA Blackwell Ultra", NV_BWU, "2025-08-22",
    "With 288 GB of HBM3e per GPU, it offers 3.6x more on-package memory than H100 and 50% more than Blackwell",
    "12-Hi stacks; article conflicts on stack count (8 vs 12).")
row("accelerator", "hbm_per_gpu_Rubin", "2026", "288", "GB", "actual", "NVIDIA", "Inside the NVIDIA Vera Rubin Platform: Six New Chips, One AI Supercomputer",
    NV_RUBIN, "2026-01-05", "Up to 288 GB of HBM4 per GPU")
row("accelerator", "hbm_per_package_RubinUltra", "2027", "1024", "GB", "forecast", "NVIDIA (GTC 2025 keynote)", "GTC 2025 Keynote", NV_GTC25, "2025-03-18",
    "Each package is four reticle-sized GPU dies with 1 TB of HBM4e and 100 PFLOPS FP4.",
    SNIP + " UBS (2026-05-13) now assumes 768 GB (12-Hi); TrendForce (2026-06-02) says 384GB per GPU.")
row("accelerator", "hbm_per_package_RubinUltra_ubs", "2027", "768", "GB", "forecast", "UBS (via Investing.com)",
    "UBS says Samsung to reach market share parity for HBM with SK Hynix by 2027", UBS, "2026-05-13",
    "768 gigabytes of HBM4E memory in a 12-Hi stack configuration.", "Down from 1 TB 16-Hi assumption.")
row("accelerator", "hbm_per_gpu_RubinUltra_tf", "2027", "384", "GB", "forecast", "TrendForce",
    "Tight DRAM Supply Gives Suppliers Greater Pricing Power in HBM, with HBM Contract Prices Expected to Surge Multiples Higher in 2027, Says TrendForce",
    TF_2606, "2026-06-02", "In 2027, NVIDIA's Rubin Ultra platform is expected to further increase HBM capacity per GPU to 384GB.",
    "Per GPU die-pair basis presumably; differs from 1 TB per 4-die package.")
row("accelerator", "hbm_per_ai_chip_trend", "2026", "216/288", "GB", "forecast", "TrendForce",
    "Tight DRAM Supply Gives Suppliers Greater Pricing Power in HBM, with HBM Contract Prices Expected to Surge Multiples Higher in 2027, Says TrendForce",
    TF_2606, "2026-06-02", "HBM capacity per AI chip increasing significantly from 96GB/192GB to 216GB/288GB")
row("accelerator", "hbm_per_gpu_MI300X", "2023", "192", "GB", "actual", "AMD", "AMD Delivers Leadership AI Performance with AMD Instinct MI325X Accelerators",
    AMD_325, "2024-10-10", "8x AMD Instinct MI300X (192GB, 750W) GPUs")
row("accelerator", "hbm_per_gpu_MI325X", "2024", "256", "GB", "actual", "AMD", "AMD Delivers Leadership AI Performance with AMD Instinct MI325X Accelerators",
    AMD_325, "2024-10-10", "256GB of HBM3E supporting 6.0TB/s")
row("accelerator", "hbm_per_gpu_MI350", "2025", "288", "GB", "actual", "AMD", "AMD Delivers Leadership AI Performance with AMD Instinct MI325X Accelerators",
    AMD_325, "2024-10-10", "up to 288GB of HBM3E memory per accelerator", "MI350 series incl. MI355X.")
row("accelerator", "hbm_per_gpu_MI455X", "2026", "432", "GB", "actual", "AMD", "AMD Instinct MI400 Series GPUs", AMD_400, "2026",
    "432GB HBM4", SNIP + " Page fetch timed out.")
row("accelerator", "hbm_per_chip_TPU_Ironwood", "2025", "192", "GiB", "actual", "Google Cloud", "From silicon to softmax: Inside the Ironwood AI stack",
    GOOG_IW, "2025-11-06", "each chip has eight stacks of HBM3E, with a peak HBM bandwidth of 7.4 TB/s and capacity of 192 GiB.")
row("accelerator", "hbm_per_chip_TPU_8t_8i", "2026", "216/288", "GB", "actual", "Mirae Asset Securities", "SK Hynix: Rising toward where it belongs",
    MIRAE_MAY, "2026-05-07", "Google s 8t TPU features 216GB of HBM3E , a 13% increa se over the previous generation , while its 8i TPU increases HBM3E capacity by 50% to 288GB")
row("accelerator", "hbm_per_chip_Trainium3", "2025", "144", "GB", "actual", "AWS", "Announcing Amazon EC2 Trn3 UltraServers", AWS_TRN3, "2025-12-02",
    "increases the memory capacity by 1.5x and bandwidth by 1.7x over Trainium2 to 144 GB of HBM3e memory",
    "Implies Trainium2 = 96 GB.")
row("accelerator", "hbm_per_gpu_A100", "2022", "80", "GB", "actual", "TrendForce",
    "HBM Supply Leader SK Hynix's Market Share to Exceed 50% in 2023 Due to Demand for AI Servers, Says TrendForce", TF_2304, "2023-04-18",
    "with NVIDIA A100 80 GB configurations of four or eight, HBM usage would be around 320–640 GB")

# ---------------- accelerator / AI server units ----------------
row("accelerator", "datacenter_accelerator_units", "2023", ">4", "million units", "estimate", "Yole Group (via Edge AI and Vision Alliance)",
    "Generative AI, High Performance Computing to Fuel High Bandwidth Memory Market Growth", YOLE_2402, "2024-02-13",
    "Demand for data center accelerators exceeded four million units in 2023 and is poised to nearly double in 2024.")
row("accelerator", "nvidia_dc_gpu_shipments", "2023", "3.76", "million units", "estimate", "TechInsights (via DatacenterDynamics)",
    "Nvidia data center GPU shipments totaled 3.76m in 2023", DCD, "2024", "Nvidia shipped about 3.76 million data center GPUs",
    SNIP + " Page returned 403.")
row("accelerator", "hopper_bought_top4_csp", "2024", "1.3", "million units", "actual", "NVIDIA (Jensen Huang, via Silicon UK)",
    "Nvidia Promises Continued AI Chip Demand At Developer Event", SILICON, "2025-03-19",
    "bought 1.3 million older-generation Hopper AI chips last year", "Top 4 US CSPs only.")
row("accelerator", "blackwell_bought_top4_csp_ytd", "2025-03", "3.6", "million GPUs", "actual", "NVIDIA (Jensen Huang, via Silicon UK)",
    "Nvidia Promises Continued AI Chip Demand At Developer Event", SILICON, "2025-03-19",
    "so far this year have already purchased 3.6 million of the newer Blackwell processors.",
    "Orders by mid-March 2025; Blackwell counted as 2 dies per package.")
row("accelerator", "blackwell_rubin_gpus_through_2026", "2025-2026", "20", "million GPUs", "forecast", "NVIDIA (GTC DC keynote)",
    "NVIDIA GTC Washington, D.C. Keynote", NV_GTCDC, "2025-10-28",
    "20 million GPUs: expected total shipments of Blackwell plus early Rubin GPUs", SNIP + " With ~$500B of bookings; GPU = die count.")
row("accelerator", "ai_server_shipments", "2023", "~1.2", "million units", "forecast", "TrendForce",
    "AI and HPC Demand Set to Boost HBM Volume by Almost 60% in 2023, Says TrendForce", TF_2306, "2023-06-28",
    "will reach nearly 1.2 million units in 2023, marking an annual growth rate of almost 38%.")
row("accelerator", "ai_server_shipment_growth", "2025", "~24", "%", "estimate", "TrendForce",
    "Strong Demand from CSPs and Sovereign Cloud to Drive Over 20% Growth in AI Server Shipments by 2026, Says TrendForce", TF_2510, "2025-10-30",
    "slightly lower its growth forecast to about 24%.")
row("accelerator", "ai_server_shipment_growth", "2026", "~31", "%", "forecast", "TrendForce",
    "AI Server Shipments Forecast Raised to Nearly 31% YoY in 2026", "https://www.trendforce.com/presscenter/news/20260803-13161.html", "2026-08-03",
    "TrendForce has therefore revised its 2026 AI server shipment forecast upward from 28% to nearly 31% YoY.")
row("accelerator", "asic_share_of_ai_servers", "2026", "27.8", "%", "forecast", "TrendForce",
    "Global AI Server Shipments Forecast to Grow Over 28% YoY in 2026, with a Rising Share of ASIC-Based Systems, Says TrendForce", TF_2601, "2026-01-20",
    "The share of ASIC-based AI servers is expected to reach 27.8% by 2026, the highest since 2023", "GPU share 69.7%.")
row("accelerator", "nvidia_ai_chip_share", "2025", "~70", "%", "estimate", "TrendForce",
    "Strong Demand from CSPs and Sovereign Cloud to Drive Over 20% Growth in AI Server Shipments by 2026, Says TrendForce", TF_2510, "2025-10-30",
    "TrendForce estimates that NVIDIA will maintain approximately 70% of the AI chip market share in 2025.")
row("accelerator", "bottom_up_hbm_check", "2023", "2.6", "billion Gb", "derived", "Yole Group / NVIDIA",
    "Bottom-up check: accelerators x HBM per unit", YOLE_2402, "2024-02-13",
    "Demand for data center accelerators exceeded four million units in 2023",
    "Derived: ~4.0 million units x ~80 GB (H100/A100 80 GB) = 320 million GB = 2.56 billion Gb. Close to TrendForce 2023 demand 2.32 billion Gb.")

# ---------------- sold-out statements ----------------
row("hbm-micron", "sold_out", "2026", "sold out", "text", "actual", "Micron (FQ1 2026 call)", "Micron (MU) Q1 2026 Earnings Call Transcript", MU_FQ1_26, "2025-12-17",
    "completed agreements on price and volume for our entire calendar 2026 HBM supply")
row("hbm-micron", "demand_vs_supply", "2027-2028", "demand above supply", "text", "actual", "Micron (FQ3 2026 call, Sumit Sadana)",
    "Micron Q3 2026 post-earnings call transcript", MU_FQ3_26, "2026-06-24",
    "our demand for HBM, not just in 2027, but even 2028, is well above our ability to supply across all the different HBM flavors.")
row("hbm-skhynix", "sold_out", "2027-2029", "sold out", "text", "actual", "SK hynix (Q3 2026 call, via MoneyToday)",
    "DRAM and HBM volumes essentially sold out through 2029", MT_SKH, "2026-10-28",
    "DRAM and High Bandwidth Memory (HBM) volumes for the next three years, through 2029, are essentially all sold out.",
    "LTAs cover >50% of capacity for 2027 and 2028.")
row("hbm-samsung", "sold_out", "2027", "sold out", "text", "actual", "Samsung (Q3 2026 call, via MoneyToday)",
    "Samsung Electronics says HBM4 sales tripled quarter-on-quarter, next year's HBM supply fully booked", MT_SEC, "2026-10-29",
    "the supply is already sold out", "Refers to 2027 ('next year').")
row("hbm-samsung", "hbm_sales_growth", "2026", ">3x", "x", "forecast", "Samsung (Q4 2025 call)", "Samsung Electronics 2025 Q4 Earnings Call",
    SEC_Q425, "2026-01-29", "HBM sales should rise more than threefold year over year in 2026.", SNIP + " PDF text not extractable.")
row("hbm-skhynix", "hbm_revenue_growth", "2025", ">100", "%", "actual", "SK hynix (Q4 2025 call)", "SK hynix FY2025 Q4 Earnings Call Transcript", SKH_Q425, "2026-01-29",
    "HBM revenue more than doubled year-over-year, driven by a significant increase in HBM3E 12-Hi sales")

# ---------------- graphics / GDDR ----------------
T = "[2026 Outlook Report] Semiconductors: Robust earnings cycle ahead"
qg = "Total demand (bn Gb) 209.5 247.3 301.2 379.8 462.1 ... Graphics DRAM 11.2 18.5 30.4 46.1 64.7 (2023 2024 2025F 2026F 2027F); Note: Graphics DRAM = HBM + GDDR"
for p, v, k in (("2023", "11.2", "actual"), ("2024", "18.5", "actual"), ("2025", "30.4", "estimate"), ("2026", "46.1", "forecast"), ("2027", "64.7", "forecast")):
    row("graphics", "bit_demand_hbm_plus_gddr", p, v, "billion Gb", k, "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15", qg,
        "Graphics DRAM includes HBM. Do not add to HBM.")
qg2 = "Bit share (%) ... Graphics DRAM 5.3 7.5 10.1 12.1 14.0 (2023 2024 2025F 2026F 2027F)"
for p, v, k in (("2023", "5.3", "actual"), ("2024", "7.5", "actual"), ("2025", "10.1", "estimate"), ("2026", "12.1", "forecast"), ("2027", "14.0", "forecast")):
    row("graphics", "share_of_dram_bit_demand_hbm_plus_gddr", p, v, "%", k, "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15", qg2)
row("graphics", "bit_demand_growth", "2026", "52", "%", "forecast", "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15",
    "Growth is expected to be led by servers (+35%) and graphics/HBM (+52%)")
qg3 = "Shipments (mn) ... Graphics 284 278 287 295 307; Avg. DRAM content (GB) ... Graphics 4.9 8.3 13.2 19.5 26.3"
for p, u, c in (("2023", "284", "4.9"), ("2024", "278", "8.3"), ("2025", "287", "13.2"), ("2026", "295", "19.5"), ("2027", "307", "26.3")):
    row("graphics", "device_shipments", p, u, "million units", "actual" if p < "2025" else "forecast", "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15", qg3,
        "Graphics device count incl. HBM accelerators; definition not given.")
    row("graphics", "avg_dram_content", p, c, "GB/unit", "actual" if p < "2025" else "forecast", "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15", qg3)
row("gddr", "bits_residual", "2023", "8.9", "billion Gb", "derived", "Mirae Asset Securities / TrendForce", T, MIRAE_DEC, "2025-12-15", qg,
    "Derived: Mirae graphics 11.2 - TrendForce HBM demand 2.32 (290 million GB) = 8.9 billion Gb. Mixed sources.")
row("gddr", "bits_residual", "2026", "~13-16", "billion Gb", "derived", "Mirae Asset Securities / TrendForce / UBS", T, MIRAE_DEC, "2025-12-15", qg,
    "Derived: Mirae graphics 46.1 - HBM 30 (TrendForce >30) to 32.9 (UBS) = 13.2-16.1 billion Gb. Mixed sources; noisy.")
row("graphics", "share_of_dram_bit_demand", "2019", "5", "%", "estimate", "KGI (Memory sector report)", "Memory sector (Taiwan industry report)", KGI, "2025-11-17",
    "Graphics | 5% | 6% | 6% (2019 2020 2021)", SNIP + " Chart is an image in the PDF; text extraction did not confirm. Omdia data puts graphics at 1.4-1.8%.")
row("graphics", "share_of_dram_bit_demand", "2020", "6", "%", "estimate", "KGI (Memory sector report)", "Memory sector (Taiwan industry report)", KGI, "2025-11-17",
    "Graphics | 5% | 6% | 6% (2019 2020 2021)", SNIP + " See 2019 row.")
row("graphics", "share_of_dram_bit_demand", "2021", "6", "%", "estimate", "KGI (Memory sector report)", "Memory sector (Taiwan industry report)", KGI, "2025-11-17",
    "Graphics | 5% | 6% | 6% (2019 2020 2021)", SNIP + " See 2019 row.")
row("gddr", "market_direction", "2026Q4", "GDDR6 exiting; GDDR7 driven by AI chips", "text", "forecast", "TrendForce",
    "AI Server Demand Sustains Memory Contract Price Increases in 4Q26, While Consumer-Side Pressure Persists, Says TrendForce", TF_2609G, "2026-09-30",
    "On the supply side, suppliers continue to scale back GDDR6 production while gradually exiting the market.",
    "Same release: 'GDDR7 demand, meanwhile, continues to be driven primarily by AI chips'.")
row("gddr", "gddr7_per_card_RubinCPX", "2026", "128", "GB", "forecast", "NVIDIA", "NVIDIA Unveils Rubin CPX", NV_CPX, "2025-09-09",
    "It features 128GB of cost-efficient GDDR7 memory to accelerate the most demanding context-based workloads.",
    "Tom's Hardware later headline: 'Nvidia removes Rubin CPX accelerators from its roadmap' (" + TH_CPX + "); treat as at risk.")
row("gddr", "gddr7_per_card_RTX5090", "2025", "32", "GB", "actual", "NVIDIA", "GeForce RTX 5090 product page", NV_5090, "2025",
    "32 GB GDDR7")
row("gddr", "gddr7_per_card_RTX_PRO_6000", "2025", "96", "GB", "actual", "NVIDIA", "RTX PRO 6000 Blackwell Workstation Edition datasheet", NV_PRO6000, "2025",
    "96 GB of GDDR7 with ECC", SNIP)
# JPR AIB
row("gddr", "aib_shipments_quarter", "2024Q4", "8.4", "million units", "actual", "Jon Peddie Research", "PC AIB shipments follow seasonality, show nominal increase for Q4'24",
    JPR_Q424, "2025-03-05", "the global PC-based graphics add-in board market reached 8.4 million units in Q4'24")
row("gddr", "aib_shipments_quarter", "2025Q1", "9.2", "million units", "actual", "Jon Peddie Research", "Q1'25 PC graphics add-in board shipments increased 8.5% from last quarter",
    JPR_Q125, "2025", "Q1'25: about 9.2 million units", SNIP)
row("gddr", "aib_shipments_quarter", "2025Q2", "11.6", "million units", "actual", "Jon Peddie Research", "Q2'25 PC graphics add-in board shipments increased 27.0% from last quarter",
    JPR_Q225, "2025", "Q2'25: about 11.6 million units", SNIP)
row("gddr", "aib_shipments_quarter", "2025Q3", "12.0", "million units", "actual", "Jon Peddie Research", "Global add-in board market: $8.8 billion in Q3'25, with a CAGR of -0.7% to 2029",
    JPR_Q325, "2025", "12.0 million PC graphics add-in boards (AIBs) shipped worldwide in Q3 2025", SNIP)
row("gddr", "aib_shipments_quarter", "2025Q4", "11.48", "million units", "actual", "Jon Peddie Research",
    "Q4'25 PC graphics AIB shipments decreased -4.4% from last quarter to 11 million units, with a CAGR to 2029 of -5.9%", JPR_Q425, "2026-03-05",
    "Total AIB shipments decreased from the previous quarter to 11.48 million units.", "YoY +36.0%.")
row("gddr", "aib_shipments_year", "2025", "44.28", "million units", "derived", "Jon Peddie Research", "Sum of JPR quarterly AIB releases", JPR_Q425, "2026-03-05",
    "Total AIB shipments decreased from the previous quarter to 11.48 million units.",
    "Derived: 9.2 + 11.6 + 12.0 + 11.48 = 44.28 million (matches the 44.28M figure that secondary sites credit to JPR).")
row("gddr", "aib_shipments_quarter", "2026Q2", "12.5", "million units", "actual", "Jon Peddie Research",
    "Q2'26 PC graphics AIB shipments increased 10% from last quarter to 12 million units", JPR_Q226, "2026",
    "12.5 million PC graphics add-in boards (AIBs) worldwide in Q2'26", SNIP + " +6.6% YoY.")
row("gddr", "aib_market_forecast", "2026", "~-10", "%", "forecast", "Jon Peddie Research",
    "Q4'25 PC graphics AIB shipments decreased -4.4% from last quarter to 11 million units, with a CAGR to 2029 of -5.9%", JPR_Q425, "2026-03-05",
    "the PC and AIB market will decline almost 10% in 2026")
row("gddr", "aib_cagr", "2024-2029", "-5.9", "%", "forecast", "Jon Peddie Research",
    "Q4'25 PC graphics AIB shipments decreased -4.4% from last quarter to 11 million units, with a CAGR to 2029 of -5.9%", JPR_Q425, "2026-03-05",
    "AIBs will have a compound annual growth rate of -5.9% from 2024 to 2028", "Headline says to 2029, body says 2024-2028.")
row("gddr", "aib_shipments_year", "2020", "~41.5", "million units", "estimate", "Jon Peddie Research (via Tom's Hardware)",
    "Despite PC Boom, Discrete GPU Sales Did Not Skyrocket in 2020", TH_2020, "2021",
    "2020: ~41.5-42 million (often rounded to 42M)", SNIP)
row("gddr", "aib_shipments_year", "2021", "~49.15", "million units", "estimate", "Jon Peddie Research (via TechSpot)",
    "Graphics card shipments surpassed the 50 million mark last year", TS_2021, "2022",
    "2021: ~49.15-50 million (TechSpot's headline says it passed 50M)", SNIP + " Page returned 403.")

# ---------------- DRAM context used for derivations ----------------
row("dram", "industry_bit_shipment_growth", "2026", "~20", "%", "forecast", "Micron (FQ1 2026 call)", "Micron (MU) Q1 2026 Earnings Call Transcript", MU_FQ1_26, "2025-12-17",
    "We expect both DRAM and NAND calendar 2026 industry bit shipments to increase around 20% from 2025 levels.")
row("dram", "total_production_bits", "2025", "293.1", "billion Gb", "estimate", "Mirae Asset Securities", T, MIRAE_DEC, "2025-12-15",
    "Total production (bn Gb) 200.2 235.0 293.1 352.5 415.7 (2023 2024 2025F 2026F 2027F)", "Context for HBM share math.")
row("hbm", "bits_from_share", "2025", "23.4", "billion Gb", "derived", "TrendForce / Mirae Asset Securities",
    "Derived: TrendForce HBM bit share x Mirae DRAM production", TF_2606, "2026-06-02",
    "HBM bit supply is expected to represent approximately 8%, 9%, and 13% of total DRAM bit supply",
    "Derived: 8% x 293.1 = 23.4 (2025); 9% x 352.5 = 31.7 (2026); 13% x 415.7 = 54.0 (2027) billion Gb. Mixed sources; cross-check with UBS 17.5/32.9/58.0.")
row("hbm", "bits_from_share", "2026", "31.7", "billion Gb", "derived", "TrendForce / Mirae Asset Securities",
    "Derived: TrendForce HBM bit share x Mirae DRAM production", TF_2606, "2026-06-02",
    "HBM bit supply is expected to represent approximately 8%, 9%, and 13% of total DRAM bit supply", "Derived: 9% x 352.5.")
row("hbm", "bits_from_share", "2027", "54.0", "billion Gb", "derived", "TrendForce / Mirae Asset Securities",
    "Derived: TrendForce HBM bit share x Mirae DRAM production", TF_2606, "2026-06-02",
    "HBM bit supply is expected to represent approximately 8%, 9%, and 13% of total DRAM bit supply", "Derived: 13% x 415.7.")

# =====================================================================
# 2026 / 2027 focus rows (added 2026-10-30 after change of focus)
# =====================================================================
TF_2601b = "https://www.trendforce.com/presscenter/news/20260108-12869.html"
TF_2602 = "https://www.trendforce.com/presscenter/news/20260213-12929.html"
TF_2608 = "https://www.trendforce.com/presscenter/news/20260804-13166.html"
SED_YLD = "https://en.sedaily.com/finance/2026/08/10/samsung-hits-80-percent-yield-on-hbm4-speeds-up-hbm4e"
SED_PRC = "https://en.sedaily.com/finance/2026/10/01/hbm-prices-to-more-than-double-next-year-as-shortage"
MT_COST = "https://www.mt.co.kr/en/industry/2026/08/06/2026080614030820066"
TF_COWOS = "https://www.trendforce.com/news/2026/06/15/news-tsmc-cowos-supply-demand-gap-reportedly-seen-narrowing-from-20-to-10-by-end-2026-as-capacity-expands"
JPM_SEMI = "https://finvaulta.com/research/jp-morgan/asia-semis-key-takeaways-from-semicon-taiwan-2026-09-09"
SEMIMEDIA = "https://www.semimedia.cc/nvidia-expected-to-take-60-of-cowos-wafer-supply-by-2026-tsmc-to-expand-packaging-in-u-s/"
TF_ASMPT = "https://www.trendforce.com/news/2025/12/12/news-sk-hynix-reportedly-places-hbm4-tc-bonder-order-with-asmpt-as-hanmi-hanwha-patent-clash-heats-up/"
YNA_HANMI = "https://en.yna.co.kr/view/AEN20260608012500320"
SKH_TSMC = "https://news.skhynix.com/en/sk-hynix-partners-with-tsmc-to-strengthen-hbm-technological-leadership/"
TSMC_NL = "https://pr.tsmc.com/static/campaign/2025august/tsmc_na/quarter.html"
SEC_HBM4 = "https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing"
SEC_AMD = "https://semiconductor.samsung.com/news-events/news/samsung-and-amd-expand-strategic-collaboration-on-next-generation-ai-memory-solutions/"
AMD_CITI = "https://www.investing.com/news/transcripts/amd-at-citis-2026-global-tmt-conference-ai-push-lifts-outlook-93CH-4891921"
NV_Q2FY27 = "https://investor.nvidia.com/files/content_files/TRANSCRIPT_-NVIDIA-Corp-NVDA-US-Q2-2027-Earnings-Call-26-August-2026-5_00-PM-ET.pdf"
BUILDOUT = "https://thebuildout.ai/intel/3bd003a5-04eb-44ba-ad8b-17129845d8a3"
CNYES = "https://news.cnyes.com/news/print/6593717"
AMZN_Q4 = "https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx"
TECHT = "https://www.techtimes.com/articles/318772/20260621/nvidia-rtx-50-gpu-shortage-supply-cut-20-prices-climbing-no-desktop-refresh-confirmed.htm"
TH_PRICE = "https://www.tomshardware.com/pc-components/gpus/geforce-rtx-50-series-gpu-prices-spike-as-much-as-39-percent-as-blackwell-price-hikes-hit-the-us-rtx-5070-gets-a-36-percent-hike-rtx-5060-up-27-percent-at-the-median-of-newegg-listings"
TH_MU_GDDR7 = "https://www.tomshardware.com/pc-components/ram/micron-discontinues-2gb-gddr7-chips-for-gaming-gpus-as-it-pivots-toward-higher-density-memory-for-ai-chipmaker-reportedly-pivots-to-high-margin-3gb-silicon-for-ai-gpus"
NV_VR = "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/"

# --- 1. vendor HBM production, mix, qualification, yields ---
row("hbm", "hbm4_mass_production_start", "2026Q1-Q2", "late 1Q26 to early 2Q26", "text", "forecast", "TrendForce",
    "HBM4 Mass Production Delayed to End of 1Q26 By Spec Upgrades and Nvidia Strategy Adjustments", TF_2601b, "2026-01-08",
    "mass production of HBM4 across suppliers will most likely commence between late 1Q26 and early 2Q26.",
    "Cause: Nvidia raised Rubin HBM4 pin speed to above 11 Gbps in 3Q25; Nvidia raised B300/GB300 targets and HBM3e orders for 1H26.")
row("hbm-skhynix", "share_of_hbm_supply_bits", "2026", "dominant", "text", "forecast", "TrendForce",
    "HBM4 Mass Production Delayed to End of 1Q26 By Spec Upgrades and Nvidia Strategy Adjustments", TF_2601b, "2026-01-08",
    "expected to retain a dominant share of total HBM supply bits in 2026.")
row("hbm", "hbm4_nvidia_validation", "2026Q2", "all three suppliers complete validation", "text", "forecast", "TrendForce",
    "HBM4 Validation Expected in 2Q26; Three Major Suppliers Poised to Shape NVIDIA Supply Landscape, Says TrendForce", TF_2602, "2026-02-13",
    "are now in the final stages of HBM4 validation, with completion anticipated by 2Q26",
    "Samsung likely first (1c DRAM, 4nm base die); Micron 'relatively slower pace' but also by 2Q26.")
row("hbm-samsung", "hbm4_first_shipment", "2026-02", "Feb 2026", "text", "actual", "Seoul Economic Daily",
    "Samsung Hits 80 Percent Yield on HBM4, Speeds Up HBM4E", SED_YLD, "2026-08-10",
    "began shipping the sixth generation of HBM (HBM4) in February this year")
row("hbm-samsung", "hbm4_yield", "2026-02", "<60", "%", "estimate", "Seoul Economic Daily (industry sources)",
    "Samsung Hits 80 Percent Yield on HBM4, Speeds Up HBM4E", SED_YLD, "2026-08-10",
    "In the early stages of mass production in February this year, its yield struggled below 60%", "Not disclosed by Samsung.")
row("hbm-samsung", "hbm4_yield", "2026-08", "~80", "%", "estimate", "Seoul Economic Daily (industry sources)",
    "Samsung Hits 80 Percent Yield on HBM4, Speeds Up HBM4E", SED_YLD, "2026-08-10",
    "Samsung Electronics' HBM4 yield recently came close to the 80% mark.", "Not disclosed by Samsung.")
row("hbm-samsung", "hbm4e_reliability_test_yield", "2026-06", ">70", "%", "estimate", "Seoul Economic Daily (Samsung CTO Song Jai-hyuk)",
    "Samsung Hits 80 Percent Yield on HBM4, Speeds Up HBM4E", SED_YLD, "2026-08-10",
    "the reliability-test yield for HBM4E has risen to a level above 70%", "12-layer HBM4E samples sent late May 2026.")
row("hbm", "bit_share_SKH/Samsung", "2027", "39/41", "%", "forecast", "UBS (via Seoul Economic Daily)",
    "Samsung Hits 80 Percent Yield on HBM4, Speeds Up HBM4E", SED_YLD, "2026-08-10",
    "next year Samsung Electronics will take 41% and narrowly edge out SK hynix at 39%",
    "UBS: SK hynix 48% of bit shipments in 2026. Differs from UBS May 2026 (~40/40/20).")
row("hbm-skhynix", "bit_share", "2026", "48", "%", "forecast", "UBS (via Seoul Economic Daily)",
    "Samsung Hits 80 Percent Yield on HBM4, Speeds Up HBM4E", SED_YLD, "2026-08-10",
    "UBS sees SK hynix keeping first place this year with 48% of bit shipments")
row("hbm-samsung", "hbm4_share_of_hbm_revenue", "2026H2", ">60", "%", "forecast", "Samsung (via Seoul Economic Daily)",
    "Samsung Hits 80 Percent Yield on HBM4, Speeds Up HBM4E", SED_YLD, "2026-08-10",
    "in the second half, HBM4 revenue will comfortably exceed 60% of total HBM revenue")
row("hbm-skhynix", "hbm4_mass_production_shipments", "2026Q2", "started", "text", "actual", "Seoul Economic Daily",
    "HBM Prices to More Than Double Next Year as Shortage Persists", SED_PRC, "2026-10-01",
    "mass-production shipments of HBM4 in the second quarter", "SK hynix 3Q26 release: M15X to max capacity by end-2026 for HBM4.")
row("hbm-skhynix", "m15x_ramp", "2026-12", "maximum capacity", "text", "forecast", "SK hynix",
    "SK hynix Announces 3Q26 Financial Results", SKH_Q326, "2026-10-28",
    "ramp up M15X to maximum capacity by the end of the year to increase HBM4 production", "M15X ~50 kwpm at full use (Korea JoongAng Daily).")
row("hbm-micron", "singapore_hbm_facility_ramp", "2027", "ramp next year", "text", "forecast", "Micron (FQ4 2026 call)",
    "Micron (MU) Q4 2026 Earnings Call Transcript", MU_FQ4_26, "2026-09-30",
    "We are also preparing for the ramp of our HBM facility in Singapore next year.")
row("hbm-micron", "hbm4e_custom_nvidia", "2027", "NV HBM co-design, foundry base die", "text", "forecast", "Micron (FQ4 2026 call)",
    "Micron (MU) Q4 2026 Earnings Call Transcript", MU_FQ4_26, "2026-09-30",
    "We've been working with NVIDIA for over a year on HBM4E, what's called NV HBM.")
row("hbm-micron", "hbm4_ramp_note", "2026", "HBM4 12-high ramp 2x faster than HBM3E 12-high", "text", "actual", "Micron (via search summary of FQ4 2026 coverage)",
    "Micron Technology Reports Record Fiscal Fourth-Quarter and Full-Year 2026 Results",
    "https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/", "2026-09-30",
    "the HBM4 12-high ramp was reportedly moving twice as fast as HBM3E 12-high did", SNIP)
row("hbm-micron", "hbm4_cumulative_revenue", "2026-06", ">1", "USD bn", "actual", "Micron (via search summary of FQ3 2026)",
    "Micron Q3 2026 results", MU_FQ3_26, "2026-06-24", "shipped more than $1B of HBM4 revenue in total", SNIP)

# --- 2. sold-out status, contract and pricing terms ---
row("hbm-micron", "contracted_2027", "2027", "bulk of 2027 HBM bit supply contracted", "text", "actual", "Micron (via Seoul Economic Daily)",
    "HBM Prices to More Than Double Next Year as Shortage Persists", SED_PRC, "2026-10-01",
    "it had completed contracts with customers for the bulk of its 2027 HBM bit supply", "At prices above 2026 levels.")
row("hbm-micron", "price_2027_vs_2026", "2027", "significantly higher", "text", "actual", "Micron (FQ4 2026 call)",
    "Micron (MU) Q4 2026 Earnings Call Transcript", MU_FQ4_26, "2026-09-30",
    "we have increased that pricing significantly for calendar year '27, which will reset at the beginning of the calendar year",
    "HBM prices are annual; reset on 2027-01-01.")
row("hbm-skhynix", "contract_status_2027", "2027", "negotiating", "text", "actual", "Seoul Economic Daily",
    "HBM Prices to More Than Double Next Year as Shortage Persists", SED_PRC, "2026-10-01",
    "negotiating 2027 HBM volumes and prices with major customers", "SK hynix 3Q26 call (2026-10-28) then said DRAM and HBM essentially sold out through 2029.")
row("hbm", "hbm4_12hi_36gb_stack_price", "2026", "~600", "USD/stack", "estimate", "Seoul Economic Daily (industry estimates)",
    "HBM Prices to More Than Double Next Year as Shortage Persists", SED_PRC, "2026-10-01",
    "a 12-high 36-gigabyte HBM4 stack is expected to more than double to around $1,300 next year ... from about $600 this year",
    "Derived: $600/36 GB = $16.7/GB = $2.08/Gb.")
row("hbm", "hbm4_12hi_36gb_stack_price", "2027", "~1300", "USD/stack", "forecast", "Seoul Economic Daily (industry estimates)",
    "HBM Prices to More Than Double Next Year as Shortage Persists", SED_PRC, "2026-10-01",
    "a 12-high 36-gigabyte HBM4 stack is expected to more than double to around $1,300 next year",
    "Derived: $1300/36 GB = $36.1/GB = $4.51/Gb.")
row("hbm", "hbm_contract_pricing_model", "2026-2027", "annual pricing lags quarterly DRAM", "text", "estimate", "TrendForce",
    "Tight DRAM Supply Gives Suppliers Greater Pricing Power in HBM, with HBM Contract Prices Expected to Surge Multiples Higher in 2027, Says TrendForce",
    TF_2606, "2026-06-02", "HBM wafer revenue was overtaken by DDR5 64GB RDIMM in 1Q26.",
    "HBM uses annual contracts; 2027 HBM4 talks began 2Q26. HBM profitability fell below DDR5 64GB RDIMM since 1Q26.")
row("hbm", "hbm4_cost_to_gpu_maker", "2026", "31-32", "USD/GB", "estimate", "Fubon Research (via MoneyToday)",
    "Nvidia also faces rising HBM cost burdens", MT_COST, "2026-08-06",
    "the cost of HBM4 used in Nvidia GPU manufacturing will rise to $31–$32 per gigabyte (GB)",
    "HBM3E was $17-18/GB; non-Nvidia buyers $35-36/GB. Bill-of-materials cost, not supplier contract price.")
row("hbm", "embedded_bit_demand_growth", "2027", ">60", "%", "forecast", "Morgan Stanley (via MoneyToday)",
    "Nvidia also faces rising HBM cost burdens", MT_COST, "2026-08-06",
    "Morgan Stanley expects GPU/ASIC-embedded HBM demand to grow over 60% next year", "Paraphrase of MS view in article; bits basis.")
row("hbm", "bit_shipment_growth", "2027", "50-60", "%", "forecast", "TrendForce",
    "DRAM Supply to Remain Tight in 2027, Prompting NVIDIA to Lower HBM Configurations for Rubin Ultra, Says TrendForce", TF_2608, "2026-08-04",
    "HBM bit shipments are projected to grow by 50–60% YoY in 2027", "Key 2027 bit-growth anchor.")
row("hbm", "supply_tightness", "2027", "DRAM shortage limits HBM wafers", "text", "forecast", "TrendForce",
    "DRAM Supply to Remain Tight in 2027, Prompting NVIDIA to Lower HBM Configurations for Rubin Ultra, Says TrendForce", TF_2608, "2026-08-04",
    "the overall DRAM shortage expected in 2027 will limit the wafer capacity that memory suppliers can allocate to HBM production")
row("accelerator", "rubin_ultra_hbm_config_review", "2027", "8-Hi HBM4e / 12-Hi HBM4 / 8-Hi HBM4 under evaluation", "text", "forecast", "TrendForce",
    "DRAM Supply to Remain Tight in 2027, Prompting NVIDIA to Lower HBM Configurations for Rubin Ultra, Says TrendForce", TF_2608, "2026-08-04",
    "beginning in early 3Q26, the company started evaluating lower-specification alternatives.",
    "Baseline was 12-Hi HBM4e through 1H26. Lower configs cut GB per Rubin Ultra.")

# --- 3. packaging ---
row("packaging", "tsmc_cowos_capacity", "2026", "120-140", "kwpm", "forecast", "Economic Daily News (via TrendForce)",
    "TSMC CoWoS Supply-Demand Gap Reportedly Seen Narrowing from 20% to 10% by End-2026 as Capacity Expands", TF_COWOS, "2026-06-15",
    "TSMC's monthly CoWoS capacity could reach a record 120,000 to 140,000 wafers in 2026.")
row("packaging", "cowos_osat_added_capacity", "2026", "50-60", "kwpm", "forecast", "Economic Daily News (via TrendForce)",
    "TSMC CoWoS Supply-Demand Gap Reportedly Seen Narrowing from 20% to 10% by End-2026 as Capacity Expands", TF_COWOS, "2026-06-15",
    "Including an additional 50,000 to 60,000 wafers of new capacity from OSAT partners", "Total industry could approach 200 kwpm.")
row("packaging", "cowos_supply_demand_gap", "2026-12", "~10", "%", "forecast", "Economic Daily News (via TrendForce)",
    "TSMC CoWoS Supply-Demand Gap Reportedly Seen Narrowing from 20% to 10% by End-2026 as Capacity Expands", TF_COWOS, "2026-06-15",
    "the CoWoS supply-demand gap is expected to narrow significantly from around 20% currently to about 10% by the end of 2026.")
row("packaging", "tsmc_cowos_capacity_growth", "2027", ">60", "%", "forecast", "TrendForce",
    "TSMC CoWoS Supply-Demand Gap Reportedly Seen Narrowing from 20% to 10% by End-2026 as Capacity Expands", TF_COWOS, "2026-06-15",
    "TSMC's plan to expand CoWoS capacity by more than 60% by 2027.")
row("packaging", "tsmc_cowos_capacity", "2027-12", "190-200", "kwpm", "forecast", "J.P. Morgan (via Finvaulta)",
    "Asia Semis: Key Takeaways from Semicon Taiwan", JPM_SEMI, "2026-09-09",
    "Estimated TSMC CoWoS capacity by end-2027 reaching ~190-200k wfpm.")
row("packaging", "tsmc_cowos_capacity", "2025-12", "75", "kwpm", "forecast", "SemiMedia (sidebar headline)",
    "TSMC's CoWoS capacity to reach 75,000 wafers/month by end-2025", SEMIMEDIA, "2025-07-31",
    "TSMC's CoWoS capacity to reach 75,000 wafers/month by end-2025", "Sidebar headline only.")
row("packaging", "cowos_demand_total", "2026", "1000", "k wafers/yr", "forecast", "Morgan Stanley (via SemiMedia)",
    "Nvidia expected to take 60% of CoWoS wafer supply by 2026, TSMC to expand packaging in U.S.", SEMIMEDIA, "2025-07-31",
    "Global demand for CoWoS (Chip-on-Wafer-on-Substrate) packaging wafers is forecast to reach 1 million units by 2026")
row("packaging", "cowos_nvidia_wafers", "2026", "595", "k wafers/yr", "forecast", "Morgan Stanley (via SemiMedia)",
    "Nvidia expected to take 60% of CoWoS wafer supply by 2026, TSMC to expand packaging in U.S.", SEMIMEDIA, "2025-07-31",
    "The report projects that Nvidia will require approximately 595,000 CoWoS wafers in 2026",
    "~510K at TSMC, ~80K at Amkor/ASE; 60% of total.")
row("packaging", "hbm4_base_die_skhynix", "2026", "TSMC logic process", "text", "actual", "SK hynix",
    "SK hynix Partners with TSMC to Strengthen HBM Technological Leadership", SKH_TSMC, "2024-04-19",
    "SK hynix ... will use TSMC's logic process for HBM4 base dies", SNIP + " Industry reports name TSMC 12nm-class (N12).")
row("packaging", "hbm4_base_die_tsmc_nodes", "2026-2027", "N12 (HBM4), N3P (custom HBM4E)", "text", "actual", "TSMC",
    "TSMC Customer Newsletter (Aug 2025) / OIP", TSMC_NL, "2025-08",
    "N12 for HBM4 and N3P for custom HBM4E", SNIP)
row("packaging", "hbm4_base_die_samsung", "2026", "Samsung Foundry 4nm", "text", "actual", "Samsung",
    "Samsung Ships Industry-First Commercial HBM4", SEC_HBM4, "2026-02",
    "base die in its own foundry on 4nm (SF4) and pairs it with 1c DRAM", SNIP)
row("packaging", "hbm4e_base_die_micron", "2027", "TSMC", "text", "actual", "Micron (FQ4 2025 call)",
    "Micron FY2025 Q4 Earnings Call Transcript", MU_FQ4_25, "2025-09-23",
    "We are partnering with TSMC for manufacturing the HVM four e base logic die", "Micron HBM4 uses in-house base die.")
row("packaging", "tc_bonder_order_asmpt", "2025-11", "7", "units", "actual", "TrendForce (news)",
    "SK hynix Reportedly Places HBM4 TC Bonder Order With ASMPT Amid Hanmi-Hanwha Patent Clash", TF_ASMPT, "2025-12-12",
    "SK hynix placed an order last month with ASMPT for seven TC bonder systems, each equipped with two bonding heads.",
    "~4 bn won each, ~30 bn won total.")
row("packaging", "tc_bonders_in_use_skhynix_hbm4", "2025-12", "~50", "sets", "estimate", "TrendForce (news)",
    "SK hynix Reportedly Places HBM4 TC Bonder Order With ASMPT Amid Hanmi-Hanwha Patent Clash", TF_ASMPT, "2025-12-12",
    "Currently, SK hynix is using about fifty sets of TC bonders for HBM4 production, with roughly half supplied by ASMPT")
row("packaging", "tc_bonder_order_expected", "2026-03", "~100", "units", "forecast", "TrendForce (news)",
    "SK hynix Reportedly Places HBM4 TC Bonder Order With ASMPT Amid Hanmi-Hanwha Patent Clash", TF_ASMPT, "2025-12-12",
    "SK hynix is likely to place an order for roughly 100 TC bonder units in March next year for HBM4 production")
row("packaging", "tc_bonder_order_hanmi", "2026-06", "44.2", "KRW bn", "actual", "Yonhap",
    "SK hynix orders new equipment worth 44.2 bln won for next-gen HBM4", YNA_HANMI, "2026-06-08",
    "SK hynix orders new equipment worth 44.2 bln won for next-gen HBM4",
    SNIP + " Hanmi TC Bonder 4.5; delivery through 2026-09-02. Jan 2026 orders ~9.7 bn won each to Hanmi and Hanwha (Asia Business Daily, Seoul Economic Daily).")
row("packaging", "hybrid_bonding_hbm", "2026", "not in HBM4 volume", "text", "estimate", "TrendForce (news)",
    "Where is the Spring of the Memory Market?", TF_2502, "2025-02-07",
    "the three major HBM manufacturers are considering whether to adopt Hybrid Bonding for HBM4 16hi ... have already decided to implement this technology in HBM5 20hi",
    "All documented 2026 HBM4 tool orders are TC bonders.")

# --- 4. accelerator shipments 2026 and 2027 ---
row("accelerator", "nvidia_ai_chip_shipments", "2026", "5.4", "million units", "forecast", "Morgan Stanley (via SemiMedia)",
    "Nvidia expected to take 60% of CoWoS wafer supply by 2026, TSMC to expand packaging in U.S.", SEMIMEDIA, "2025-07-31",
    "Total shipments of Nvidia chips could reach 5.4 million units that year, including 2.4 million Rubin-based chips.",
    "Mid-2025 view; Rubin share later cut (TrendForce Apr 2026: Rubin 22%). KeyBanc ~Apr 2026: 5.5-6.0M Blackwell, 1.5M Rubin, 1M Hopper (" + SNIP + ").")
row("accelerator", "nvidia_rubin_production_shipments", "2026-08", "started", "text", "actual", "NVIDIA (Q2 FY2027 call)",
    "NVIDIA Q2 FY2027 Earnings Call Transcript", NV_Q2FY27, "2026-08-26",
    "We commenced production shipments of Vera Rubin earlier this month.")
row("accelerator", "rubin_share_of_dc_revenue", "FQ3-2027", "~20", "%", "forecast", "NVIDIA (Q2 FY2027 call)",
    "NVIDIA Q2 FY2027 Earnings Call Transcript", NV_Q2FY27, "2026-08-26",
    "We see Vera Rubin accounting for about 20% of data center revenue in Q3.", "Nvidia FQ3 2027 = Aug-Oct 2026.")
row("accelerator", "nvidia_revenue_growth_fy2028", "FY2028", "~70", "%", "forecast", "NVIDIA (Q2 FY2027 call)",
    "NVIDIA Q2 FY2027 Earnings Call Transcript", NV_Q2FY27, "2026-08-26",
    "we expect supply to remain a bottleneck at least through the end of fiscal year 2028.",
    "Same call: 'We expect to grow revenue by approximately 70% in fiscal 2028. This is a supply - constrained outlook.' FY2028 ~ Feb 2027-Jan 2028.")
row("accelerator", "nvidia_memory_price_comment", "2026-2027", "memory prices extreme, higher into 2027", "text", "actual", "NVIDIA (Q2 FY2027 call)",
    "NVIDIA Q2 FY2027 Earnings Call Transcript", NV_Q2FY27, "2026-08-26",
    "The magnitude of the price increase has exceeded our prior expecta tions and are headed even higher into next year.")
row("accelerator", "aws_nvidia_gpus", "2026Q3-2028Q2", "2", "million GPUs", "forecast", "NVIDIA (Q2 FY2027 call)",
    "NVIDIA Q2 FY2027 Earnings Call Transcript", NV_Q2FY27, "2026-08-26",
    "AWS is deploying an additional 2 million GPUs starting this quarter throug h the second quarter of fiscal 2029.")
row("accelerator", "tpu_shipments", "2026", "4.13", "million units", "forecast", "UBS (via The Buildout)",
    "UBS forecasts Broadcom and MediaTek TPU shipment volumes for 2026 and 2027", BUILDOUT, "2026-05-18",
    "Total TPU volumes are expected to rise from 4.13 million units in 2026 to 9.87 million units in 2027.",
    "Broadcom 3.68M + MediaTek 0.45M.")
row("accelerator", "tpu_shipments", "2027", "9.87", "million units", "forecast", "UBS (via The Buildout)",
    "UBS forecasts Broadcom and MediaTek TPU shipment volumes for 2026 and 2027", BUILDOUT, "2026-05-18",
    "Total TPU volumes are expected to rise from 4.13 million units in 2026 to 9.87 million units in 2027.",
    "Broadcom 6.76M + MediaTek 3.11M.")
row("accelerator", "trainium3_shipments", "2026", "1.8", "million units", "forecast", "UBS (via Money Weekly/Cnyes)",
    "Money Weekly column (Hung Pao-shan) on Alchip/Trainium3", CNYES, "2026-09-03",
    "瑞銀預估2026年Trainium3總出貨量受到三奈米、CoWoS與載板產能限制，約180萬顆，2027年280萬顆，年增約55%",
    "UBS: 2026 ~1.8M limited by N3, CoWoS, substrate; 2027 ~2.8M (+55%).")
row("accelerator", "trainium3_shipments", "2027", "2.8", "million units", "forecast", "UBS (via Money Weekly/Cnyes)",
    "Money Weekly column (Hung Pao-shan) on Alchip/Trainium3", CNYES, "2026-09-03",
    "瑞銀預估2026年Trainium3總出貨量受到三奈米、CoWoS與載板產能限制，約180萬顆，2027年280萬顆，年增約55%")
row("accelerator", "trainium2_landed", "2025-12", "1.4", "million chips", "actual", "Amazon",
    "Amazon.com Announces Fourth Quarter Results", AMZN_Q4, "2026-02-05",
    "Trainium2 is fully subscribed with 1.4 million chips landed", "Cumulative.")
row("accelerator", "amd_mi450_ramp", "2026Q3-2027", "start end Q3 2026, big step Q4, again Q1 2027", "text", "forecast", "AMD (Citi TMT conference)",
    "AMD at Citi's 2026 Global TMT Conference", AMD_CITI, "2026-09-08",
    "We expect revenue in Q3, but Q4 we'll see a very significant step up.",
    "'The demand and the volume for 2027 has certainly go above our original initial expectation.' No unit counts disclosed.")
row("accelerator", "amd_supply_constraints", "2026-2027", "wafers, HBM, packaging, substrate tight", "text", "actual", "AMD (Citi TMT conference)",
    "AMD at Citi's 2026 Global TMT Conference", AMD_CITI, "2026-09-08",
    "There are multiple areas, not only wafers, advanced process node, HBM tight packaging, substrate.")
row("hbm-samsung", "amd_mi455x_primary_hbm4", "2026", "primary HBM4 supplier (MOU)", "text", "actual", "Samsung",
    "Samsung and AMD Expand Strategic Collaboration on Next-Generation AI Memory Solutions", SEC_AMD, "2026-03-18",
    "Samsung and AMD will align on primary HBM4 supply for the next-generation AMD AI accelerator, the AMD Instinct MI455X GPU",
    "MOU, not a contract. Samsung already primary HBM3E partner for MI350X/MI355X.")
row("accelerator", "hbm_bottom_up_tpu_trainium", "2026", "8.4", "billion Gb", "derived", "UBS / Google / AWS",
    "Bottom-up: TPU and Trainium3 units x HBM per chip", BUILDOUT, "2026-05-18",
    "Total TPU volumes are expected to rise from 4.13 million units in 2026",
    "Derived: TPU 4.13M x 192 GB (Ironwood) = 0.79 EB; Trainium3 1.8M x 144 GB = 0.26 EB; sum 1.05 EB = 8.4 billion Gb. Installed GB, before yield loss; TPU mix may include smaller older parts.")
row("accelerator", "hbm_bottom_up_nvidia", "2026", "~10-12", "billion Gb", "derived", "Morgan Stanley / NVIDIA / TrendForce",
    "Bottom-up: Nvidia units x HBM per package", SEMIMEDIA, "2025-07-31",
    "Total shipments of Nvidia chips could reach 5.4 million units that year",
    "Derived: 5.4M packages x ~240-288 GB (B300 288, B200 192, Rubin 288; Hopper 141) = ~1.3-1.55 EB = ~10.4-12.4 billion Gb. Compare TrendForce >30 billion Gb and UBS 32.9 billion Gb total 2026.")

# --- 5. GDDR7 2026 ---
row("gddr", "rtx50_supply_cut_to_partners", "2026-01", "15-20", "%", "estimate", "TechTimes (citing leaker MEGAsizeGPU via Tom's Hardware)",
    "NVIDIA RTX 50 GPU Shortage: Supply Cut 20%, Prices Climbing, No Desktop Refresh Confirmed", TECHT, "2026-06-21",
    "NVIDIA cut shipments to its manufacturing partners by 15 to 20 percent in January 2026", "Leak, not Nvidia statement.")
row("gddr", "rtx50_avg_price_change_3mo", "2026-02", "+19", "%", "estimate", "TechSpot (via TechTimes)",
    "NVIDIA RTX 50 GPU Shortage: Supply Cut 20%, Prices Climbing, No Desktop Refresh Confirmed", TECHT, "2026-06-21",
    "the average RTX 50 series price had risen by 19 percent over three months")
row("gddr", "rtx50_price_change_newegg_median", "2026", "up to +39", "%", "estimate", "Tom's Hardware",
    "GeForce RTX 50-series GPU prices spike as much as 39% as Blackwell price hikes hit the US", TH_PRICE, "2026",
    "GeForce RTX 50-series GPU prices spike as much as 39% as Blackwell price hikes hit the US",
    "Headline only; RTX 5070 +36%, RTX 5060 +27%. Date not visible.")
row("gddr", "micron_2gb_gddr7_eol", "2026", "Micron exits 2GB GDDR7 for gaming; pivots to 3GB for AI", "text", "actual", "Tom's Hardware",
    "Micron discontinues 2GB GDDR7 chips for gaming GPUs as it pivots toward higher-density memory for AI", TH_MU_GDDR7, "2026",
    "Micron discontinues 2GB GDDR7 chips for gaming GPUs as it pivots toward higher-density memory for AI",
    "Headline. RTX 50 cards left with Samsung and SK hynix as GDDR7 sources (Hardware Busters).")
row("gddr", "gaming_demand_memory_cost", "2026", "memory cost hurts gaming demand", "text", "actual", "AMD (Citi TMT conference)",
    "AMD at Citi's 2026 Global TMT Conference", AMD_CITI, "2026-09-08",
    "the memory cost is pretty high right now, which also impact the demand side.")
row("gddr", "rubin_cpx_status", "2026-03", "removed from roadmap at GTC 2026", "text", "actual", "Tom's Hardware",
    "Nvidia removes Rubin CPX accelerators from its roadmap - Groq 3 LPUs take center stage as CPX is removed", TH_CPX, "2026-03",
    "Nvidia removes Rubin CPX accelerators from its roadmap — Groq 3 LPUs take center stage as CPX is removed",
    "Headline only; date from search summary (GTC 2026, Mar 16-19). So the 128 GB GDDR7 per CPX demand likely does not appear in 2026-2027.")

# --- 6. standard DRAM wafers taken by HBM ---
row("hbm", "share_of_global_dram_wafers", "2026-10", "~20", "%", "estimate", "Samsung (Kim Tae-woo, via Seoul Economic Daily)",
    "HBM Prices to More Than Double Next Year as Shortage Persists", SED_PRC, "2026-10-01",
    "wafers allocated to HBM production would rise from about 20% of global DRAM capacity now to close to 30% next year")
row("hbm", "share_of_global_dram_wafers", "2027", "~30", "%", "forecast", "Samsung (Kim Tae-woo, via Seoul Economic Daily)",
    "HBM Prices to More Than Double Next Year as Shortage Persists", SED_PRC, "2026-10-01",
    "wafers allocated to HBM production would rise from about 20% of global DRAM capacity now to close to 30% next year",
    "Matches TrendForce 30% end-2027.")
row("hbm", "share_of_industry_capacity_trend", "2026-2028", "rising", "text", "forecast", "Micron (FQ4 2026 call)",
    "Micron (MU) Q4 2026 Earnings Call Transcript", MU_FQ4_26, "2026-09-30",
    "grow as a portion of the industry's capacity here through 2028", "HBM growing faster than conventional DRAM through 2028.")
row("hbm", "dram_wafers_diverted_to_hbm", "2026-12", "480", "kwpm", "derived", "TrendForce (FMS 2025) / SemiAnalysis",
    "Derived: HBM/TSV wafer capacity of all vendors", TF_FMS25, "2025-08-05",
    "~150k ... ~200k ... ~100k (HBM/TSV end-2026: Samsung, SK hynix, Micron)",
    "Derived: 150+200+100 (TrendForce FMS 2025, search snippet) + CXMT 30 (SemiAnalysis) = 480 kwpm. Top-3 total DRAM end-2026 per same deck 1630 kwpm, so 450/1630 = 28%, above TrendForce 22% wafer-input share (TSV capacity > actual wafer input).")
row("hbm", "standard_dram_bit_output_foregone", "2026-12", "320", "kwpm standard-wafer equivalent", "derived", "TrendForce / Micron",
    "Derived: diverted wafers x (1 - 1/trade ratio)", MU_FQ1_26, "2025-12-17",
    "the three-to-one trade ratio with DDR5, and this trade ratio only increases with future generations of HBM",
    "Derived: 480 kwpm x (1 - 1/3) = 320 kwpm. The 480 HBM wafers give the bits of 160 standard wafers.")
row("hbm", "dram_wafers_diverted_to_hbm", "2027-12", "~525", "kwpm", "derived", "TrendForce / Mirae Asset Securities",
    "Derived: TrendForce 30% wafer share x top-3 capacity", TF_2606, "2026-06-02",
    "approximately 18%, 22%, and 30% of total DRAM wafer input by the end of 2025, 2026, and 2027, respectively",
    "Derived: 30% x (Samsung 735 + SK hynix 646 + Micron 369 = 1750 kwpm, Mirae 2027F capacity) = 525 kwpm. At 3:1 that forgoes ~350 kwpm of standard-DRAM bit output; at 4:1 (HBM4E) ~394.")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(HDR)
    for r in R:
        assert len(r) == len(HDR), r
        w.writerow(r)
print(len(R), "rows ->", os.path.abspath(OUT))
