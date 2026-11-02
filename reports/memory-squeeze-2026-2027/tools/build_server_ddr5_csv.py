"""Build sources/server-ddr5.csv from hand-entered cited rows.

Every row carries a URL and a verbatim quote. Rows marked "SEARCH-SUMMARY" in
notes were seen only in a web-search summary (page not fetched or blocked);
treat them as unverified.
"""
import csv
import sys

OUT = sys.argv[1]
HDR = ["segment", "metric", "period", "value", "unit", "kind", "publisher",
       "title", "url", "pub_date", "quote", "notes"]

# ---- source shorthands -------------------------------------------------
MIRAE = ("Mirae Asset Securities", "[2026 Outlook Report] Semiconductors: Robust earnings cycle ahead",
         "https://securities.miraeasset.com/bbs/download/2141014.pdf?attachmentId=2141014", "2025-12-15")
KGI = ("KGI Securities", "Memory sector: Surge in general server procurement fueling a memory supercycle",
       "https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/memory-sector-17112025e.pdf", "2025-11-17")
IBK1 = ("IBK Securities (Omdia data)", "Memory Dynamics monthly: why Micron is hurrying (마이크론이 이렇게까지 서두르는 이유)",
        "https://m.ibks.com/iko/IKO01/download.do?attatchCd=ATTATCH1&menuCode=IKO010301&seq=6788", "2026-01")
IBK2 = ("IBK Securities (Omdia data)", "Memory Dynamics monthly: the answer is in memory LTAs (메모리 장기공급계약(LTA)에 해답이 있다)",
        "https://m.ibks.com/iko/IKO01/download.do?attatchCd=ATTATCH1&menuCode=IKO010301&seq=11657", "2026-05")
SSEC = ("Samsung Securities", "Tech (OVERWEIGHT): Inflection points in memory narrative",
        "https://www.bondweb.co.kr/Data/20261/28/menu01/2026012820.pdf", "2026-01-28")
MU_Q3 = ("Micron (earnings call)", "Micron FQ3 2026 earnings call transcript",
         "https://stockanalysis.com/stocks/mu/transcripts/609470-q3-2026/", "2026-06-24")
MU_Q4 = ("Micron (earnings call)", "Micron FQ4 2026 earnings call transcript",
         "https://stockanalysis.com/stocks/mu/transcripts/699706-q4-2026/", "2026-09-30")
SKH_CALL = ("SK hynix (earnings call)", "SK hynix Q3 2026 earnings call transcript",
            "https://www.fool.com/earnings/call-transcripts/2026/10/28/sk-hynix-skhy-q3-2026-earnings-call-transcript/", "2026-10-27")
SKH_NR = ("SK hynix", "SK hynix Announces 3Q26 Financial Results",
          "https://news.skhynix.com/en/q3-2026-business-results/", "2026-10-28")
RMBS = ("Rambus (earnings call)", "Rambus Q3 2026 earnings call transcript",
        "https://stockanalysis.com/stocks/rmbs/transcripts/716236-q3-2026/", "2026-10-26")


def tf(slug, title, date):
    return ("TrendForce", title, f"https://www.trendforce.com/presscenter/news/{slug}.html", date)


def apacer(year, pub):
    return ("Apacer (annual report, citing third-party research)", f"Apacer {year} Annual Report",
            f"https://www.apacer.com/upload/media/investor/financial/Annual_Report/{year}_Annual_Report_EN.pdf", pub)


rows = []


def add(seg, metric, period, value, unit, kind, src, quote, notes=""):
    pub, title, url, date = src
    rows.append([seg, metric, period, value, unit, kind, pub, title, url, date, quote, notes])


# ======================================================================
# 1. Server DRAM bits and share (Mirae table, KGI, TrendForce)
# ======================================================================
mirae_years = ["2023", "2024", "2025", "2026", "2027"]
mirae_kind = ["estimate", "estimate", "estimate", "forecast", "forecast"]
tbl = {
    ("server", "dram_bit_demand", "bn Gb"): ([76.9, 90.9, 115.2, 155.5, 190.9], "Server DRAM 76.9 90.9 115.2 155.5 190.9"),
    ("pc", "dram_bit_demand", "bn Gb"): ([24.6, 26.1, 28.9, 30.6, 35.9], "PC DRAM 24.6 26.1 28.9 30.6 35.9"),
    ("dram-total", "dram_bit_demand", "bn Gb"): ([209.5, 247.3, 301.2, 379.8, 462.1], "Total demand (bn Gb) 209.5 247.3 301.2 379.8 462.1"),
    ("server", "share_of_dram_bit_demand", "%"): ([36.7, 36.8, 38.2, 41.0, 41.3], "Server DRAM 36.7 36.8 38.2 41.0 41.3"),
    ("pc", "share_of_dram_bit_demand", "%"): ([11.7, 10.6, 9.6, 8.0, 7.8], "PC DRAM 11.7 10.6 9.6 8.0 7.8"),
    ("server", "dram_bit_demand_growth_yoy", "%"): ([10.2, 18.1, 26.7, 35.0, 22.7], "Server DRAM 10.2 18.1 26.7 35.0 22.7"),
    ("pc", "dram_bit_demand_growth_yoy", "%"): ([-1.1, 6.2, 10.7, 5.8, 17.5], "PC DRAM -1.1 6.2 10.7 5.8 17.5"),
    ("server", "shipments", "million units"): ([19, 19, 20, 22, 22], "Servers 19 19 20 22 22"),
    ("pc", "shipments", "million units"): ([229, 235, 244, 240, 246], "PCs 229 235 244 240 246"),
    ("server", "avg_dram_content", "GB/unit"): ([515, 597, 717, 903, 1065], "Server 515 597 717 903 1,065"),
    ("pc", "avg_dram_content", "GB/unit"): ([10.5, 11.8, 13.4, 14.7, 16.2], "PC 10.5 11.8 13.4 14.7 16.2"),
    ("server", "avg_dram_content_growth_yoy", "%"): ([14.6, 16.0, 20.1, 26.0, 18.0], "Server 14.6 16.0 20.1 26.0 18.0"),
}
mirae_note = {
    ("server", "shipments", "million units"): "Mirae unit count (19-22M) is larger than TrendForce (13.6-14.5M) and IDC; definition differs (likely includes white-box/ODM-direct). Content x units = bits: 515GB x 19M x 8 = 78 bn Gb ~ 76.9.",
    ("server", "dram_bit_demand", "bn Gb"): "Table page 16 'Servers to lead demand'. Mirae own model. Units are bn Gb (divide by 8 for bn GB). Graphics (HBM+GDDR) is a separate line, so server excludes HBM.",
    ("server", "share_of_dram_bit_demand", "%"): "Share of DRAM bit DEMAND; server excludes HBM (HBM sits in 'Graphics DRAM = HBM + GDDR').",
    ("server", "avg_dram_content", "GB/unit"): "Blended general + AI server, conventional DRAM (excl. HBM).",
}
for key, (vals, q) in tbl.items():
    seg, metric, unit = key
    for y, v, k in zip(mirae_years, vals, mirae_kind):
        add(seg, metric, y, v, unit, k, MIRAE, q,
            "Row from table with columns 2023 2024 2025F 2026F 2027F. " + mirae_note.get(key, ""))

# Mirae chart: server DRAM content YoY 2016-2026F (chart labels 16..26F)
chart_g = [34.4, 38.3, 24.0, 18.1, 18.6, 17.7, 14.1]
for y, g in zip(range(2016, 2023), chart_g):
    add("server", "avg_dram_content_growth_yoy", str(y), g, "%", "estimate", MIRAE,
        "34.4 38.3 24.0 18.1 18.6 17.7 14.1 14.6 16.0 20.1 26.0 ... 16 17 18 19 20 21 22 23 24 25F 26F Server DRAM content (L0 YoY (R)(GB) (%)",
        "Chart 'DRAM content per server: Trends and forecasts' (page 6). Values read from chart labels in order 2016..2026F; 2023-2026 match the page-16 table.")
# derived GB/server back-cast from 2023 = 515 GB
c = 515.0
growth = dict(zip(range(2016, 2024), chart_g + [14.6]))
for y in range(2022, 2014, -1):
    c = c / (1 + growth[y + 1] / 100)
    add("server", "avg_dram_content", str(y), round(c, 1), "GB/unit", "derived", MIRAE,
        "Server 515 597 717 903 1,065",
        f"DERIVED: content({y}) = content({y+1}) / (1 + g{y+1}); anchor 2023 = 515 GB; g from Mirae page-6 chart YoY series.")

add("server", "avg_dram_content", "2026", 903, "GB/unit", "forecast", MIRAE,
    "average DRAM content per server is projected to reach 903GB (+26.0% YoY) in 2026", "Text page 6.")
add("dram-total", "dram_bit_demand_growth_yoy", "2026", 26.1, "%", "forecast", MIRAE,
    "DRAM bit growth is expected to accelerate to +26.1% in 2026 ... led by servers (+35%) and graphics/HBM (+52%)", "")

# KGI
add("server", "dram_bit_demand", "2026", 20.74, "bn GB", "forecast", KGI,
    "we raise our 2026F server DRAM bit demand forecast by 17% to 20.74bn GB (up 45% YoY)", "20.74 bn GB = 165.9 bn Gb, vs Mirae 155.5 bn Gb.")
add("server", "dram_bit_demand", "2025", round(20.74 / 1.45, 2), "bn GB", "derived", KGI,
    "we raise our 2026F server DRAM bit demand forecast by 17% to 20.74bn GB (up 45% YoY)", "DERIVED: 20.74 / 1.45. Compare Mirae 2025 115.2 bn Gb / 8 = 14.4 bn GB.")
add("server", "share_of_dram_bit_demand", "2025", 38, "%", "estimate", KGI,
    "increasing its share of total DRAM demand from 38% in 2025F to 47% in 2026F", "")
add("server", "share_of_dram_bit_demand", "2026", 47, "%", "forecast", KGI,
    "increasing its share of total DRAM demand from 38% in 2025F to 47% in 2026F", "Much higher than Mirae 41.0%; KGI assumes US CSP general server +50%.")
add("pc", "share_of_dram_bit_demand", "2025", 10, "%", "estimate", KGI,
    "We forecast the share of DRAM bit demand of smartphone and PC to decline from 36% and 10% this year to 29% and 8% in 2026F", "")
add("pc", "share_of_dram_bit_demand", "2026", 8, "%", "forecast", KGI,
    "We forecast the share of DRAM bit demand of smartphone and PC to decline from 36% and 10% this year to 29% and 8% in 2026F", "")
add("server-general", "shipments_growth_yoy_us_csp", "2026", 50, "%", "forecast", KGI,
    "We expect 2026F US CSP general server shipments to grow by 50% YoY", "US CSPs only, general-purpose servers.")
add("ddr5-total", "ddr5_16gb_die_contract_price", "3Q25", 5.5, "USD/die", "estimate", KGI,
    "We forecast DDR5 die contract prices to climb from US$5.5 in 3Q25 to US$17.2 by 4Q26F", "")
add("ddr5-total", "ddr5_16gb_die_contract_price", "4Q26", 17.2, "USD/die", "forecast", KGI,
    "We forecast DDR5 die contract prices to climb from US$5.5 in 3Q25 to US$17.2 by 4Q26F", "")

# TrendForce share-of-bits history
add("server", "share_of_dram_supply_bits", "2020", 34, "%", "estimate",
    tf("20201210-10590", "DRAM ASP to Recover from Decline in 1Q21, with Potential for Slight Growth", "2020-12-10"),
    "PC DRAM accounts for 13%, server DRAM 34%, mobile DRAM 40%, graphics DRAM 5%, and consumer DRAM (or specialty DRAM) 8%",
    "Share of DRAM supply bits; period is the time of writing (late 2020).")
add("pc", "share_of_dram_supply_bits", "2020", 13, "%", "estimate",
    tf("20201210-10590", "DRAM ASP to Recover from Decline in 1Q21, with Potential for Slight Growth", "2020-12-10"),
    "PC DRAM accounts for 13%, server DRAM 34%, mobile DRAM 40%, graphics DRAM 5%, and consumer DRAM (or specialty DRAM) 8%", "")
add("server", "share_of_dram_bit_output", "2023", 37.6, "%", "forecast",
    tf("20230220-11572", "Server DRAM Will Overtake Mobile DRAM in Supply in 2023 and Comprise 37.6% of Annual Total DRAM Bit Output", "2023-02-20"),
    "server DRAM is estimated to comprise around 37.6%, whereas mobile DRAM is estimated to comprise around 36.8%", "Share of bit OUTPUT (supply).")
add("server", "avg_dram_content_growth_yoy", "2023", 12.1, "%", "forecast",
    tf("20230220-11572", "Server DRAM Will Overtake Mobile DRAM in Supply in 2023", "2023-02-20"),
    "TrendForce projects that the average DRAM content of servers will increase by 12.1% YoY for 2023.", "")
add("server", "avg_dram_content_growth_yoy", "2023", 7, "%", "forecast",
    tf("20221018-11428", "Annual Growth of Server Shipments Forecast to Ebb to 3.7% in 2023", "2022-10-18"),
    "average annual content of server DRAM in 2023 is estimated to increase by only 7%", "Earlier forecast; superseded by 12.1% (Feb 2023). Release: first time below 10% since 2016.")
add("server", "shipments_growth_yoy", "2022", 5.1, "%", "estimate",
    tf("20221018-11428", "Annual Growth of Server Shipments Forecast to Ebb to 3.7% in 2023", "2022-10-18"),
    "the annual growth rate of server shipments in 2023 is estimated to be only 3.7%, which is lower than 5.1% in 2022.", "")
add("server", "avg_dram_content_growth_yoy", "2024", 17.3, "%", "forecast",
    tf("20240205-12021", "AI's Rocketing Demand to Drive Server DRAM—2024 Predictions Show a 17.3% Annual Increase in Content per Box", "2024-02-05"),
    "content per box for server DRAM projected to rise by 17.3% annually", "")
add("server", "avg_dram_content_growth_yoy", "2025", 15, "%", "estimate",
    ("SemiconSam (Jukan), summary of TrendForce Korea roadshow", "TrendForce Roadshow Korea Review", "https://www.semiconsam.com/p/trendforce-roadshow-korea-review", "2025-11-07"),
    "We are now seeing a 15% increase in memory content per server.", "Secondary summary of a TrendForce talk; year not explicit (likely 2025).")

# Yole
add("server", "dc_dram_bit_demand_cagr", "2023-2029", 25, "%", "forecast",
    ("Yole Group (via Edge AI and Vision Alliance)", "Generative AI & high-performance computing to fuel high-bandwidth memory market growth",
     "https://www.edge-ai-vision.com/2024/02/generative-ai-high-performance-computing-to-fuel-high-bandwidth-memory-market-growth/", "2024-02-13"),
    "data center DRAM bit demand could grow at a compound annual growth rate (CAGR) of 25% in 2023-2029", "Data center incl. HBM? Not stated; likely all DC DRAM.")
add("server-ai", "dram_bit_demand_cagr", "2023-2029", 39, "%", "forecast",
    ("Yole Group (via Edge AI and Vision Alliance)", "Generative AI & high-performance computing to fuel high-bandwidth memory market growth",
     "https://www.edge-ai-vision.com/2024/02/generative-ai-high-performance-computing-to-fuel-high-bandwidth-memory-market-growth/", "2024-02-13"),
    "driven by a 39% growth in DRAM for AI servers over that period", "")

# Micron industry guidance
add("dram-total", "industry_bit_shipments_growth", "2026", "mid-20s", "%", "forecast", MU_Q4,
    "In DRAM, for calendar 2026, we expect industry bit shipments to grow in the mid-20s percentage range.", "Qualitative range; ~24-26%.")
add("dram-total", "industry_bit_shipments_growth", "2027", "low 20s", "%", "forecast", MU_Q4,
    "For calendar 2027 and 2028, we expect industry DRAM bit shipments to grow approximately in the low 20s percentage range", "Also applies to 2028.")
add("server", "industry_units_growth", "2026", "high teens", "%", "forecast", MU_Q4,
    "We expect server unit growth in the high teens percentage range in both calendar 2026 and 2027.", "")
add("server", "industry_units_growth", "2027", "high teens", "%", "forecast", MU_Q4,
    "We expect server unit growth in the high teens percentage range in both calendar 2026 and 2027.", "Content growth 'modestly lower ... amid tight memory supply'.")
add("server-general", "industry_units_growth", "2026", "mid-teens", "%", "forecast", MU_Q3,
    "driven by mid-teens growth in traditional servers and even stronger growth in servers with AI accelerators", "")
add("server", "dc_dram_nand_bits_vs_2024", "2026", ">2x", "ratio", "forecast", MU_Q3,
    "industry data center DRAM and NAND bit shipments in calendar 2026 expected to more than double from two years ago.", "DRAM+NAND combined.")
add("dram-total", "achievable_demand_growth", "2027", "mid-20s", "%", "forecast", SKH_CALL,
    "achievable demand growth for 2027 is expected to be at a similar level to this year with growth rates of mid-20% for DRAM", "")

# ======================================================================
# 2. Server shipments
# ======================================================================
add("server", "shipments", "2023", 13.835, "million units", "forecast",
    tf("20230517-11673", "Server Shipments to Fall an Estimated 2.85% YoY in 2023", "2023-05-17"),
    "a 2.85% YoY decrease at 13.835 million units.", "Implies 2022 ~14.24M (derived).")
add("server", "shipments", "2024", 13.654, "million units", "forecast",
    tf("20240229-12048", "Global Server Shipments Expected to Increase by 2.05% in 2024, with AI Servers Accounting For Around 12.1%", "2024-02-29"),
    "Global server shipments are estimated to reach approximately. 13.654 million units in 2024, an increase of about 2.05% YoY.", "Implies 2023 actual ~13.38M (derived), lower than the May-2023 forecast.")
add("server-ai", "share_of_server_shipments", "2024", 12.1, "%", "forecast",
    tf("20240229-12048", "Global Server Shipments Expected to Increase by 2.05% in 2024", "2024-02-29"),
    "...with their shipment share estimated at around 12.1%.", "")
add("server-ai", "shipments_growth_yoy", "2024", 46, "%", "actual",
    tf("20250212-12469", "AI Server Growth in 2025 Faces Uncertainties, DeepSeek Effect to Boost AI Inference Share", "2025-02-12"),
    "global AI server shipments grew by 46% in 2024", "")
add("server", "shipments", "2025", 14.49, "million units", "estimate",
    ("Taipei Times (TrendForce data)", "Server shipments to grow 6%, AI servers to rise 24.1%", "https://www.taipeitimes.com/News/biz/archives/2025/11/18/2003847369", "2025-11-18"),
    "grow about 6 percent from last year to 14.49 million units.", "TrendForce Nov-2025 estimate for 2025.")
add("server-ai", "shipments", "2025", ">2.1", "million units", "estimate",
    ("Taipei Times (TrendForce data)", "Server shipments to grow 6%, AI servers to rise 24.1%", "https://www.taipeitimes.com/News/biz/archives/2025/11/18/2003847369", "2025-11-18"),
    "exceed 2.1 million units ... rising 24.1 percent year-on-year.", "AI share 2025 ~14.5% (derived 2.1/14.49).")
add("server", "shipments_growth_yoy", "2026", 4, "%", "forecast",
    tf("20251029-12758", "Tight DRAM Supply to Boost DDR5 Contract Prices—Profitability in 2026 Expected to Surpass HBM3e", "2025-10-29"),
    "global server shipments are expected to grow by around 4% annually", "Oct-2025 view; later raised to 12.8% (Jan 2026), 13% (Apr 2026), 17% (Jul 2026).")
add("server", "shipments_growth_yoy", "2026", 12.8, "%", "forecast",
    tf("20260120-12887", "Global AI Server Shipments Forecast to Grow Over 28% YoY in 2026, with a Rising Share of ASIC-Based Systems", "2026-01-20"),
    "Global server shipments are projected to grow 12.8% YoY in 2026", "")
add("server-ai", "shipments_growth_yoy", "2026", ">28", "%", "forecast",
    tf("20260120-12887", "Global AI Server Shipments Forecast to Grow Over 28% YoY in 2026", "2026-01-20"),
    "AI server shipments are expected to surge by more than 28% YoY", "ASIC-based share 27.8% of AI servers in 2026.")
add("server", "shipments_growth_yoy", "2026", 13, "%", "forecast",
    tf("20260415-13013", "Extended Component Lead Times Weigh on General Server Growth; 2026 Server Shipments Forecast to Grow 13% YoY", "2026-04-15"),
    "full-year server shipment growth—previously expected to approach 20% YoY—is now projected to remain around 13%",
    "Cut due to CPU/PCB lead times ~1 year, PMIC 35-40 wks, BMC 21-26 wks. AI ~28%.")
add("server", "shipments_growth_yoy", "2026", 17, "%", "estimate",
    tf("20260730-13158", "Diverging Memory Market Outlook in 2027 as DRAM Supply Remains Tight While NAND Flash Supply Conditions Ease", "2026-07-30"),
    "TrendForce forecasts global server shipments to grow faster in 2027 than the 17% YoY recorded in 2026.", "Conflicts with Apr-2026 13%; latest TrendForce view.")
add("server", "shipments_growth_yoy", "2027", ">17", "%", "forecast",
    tf("20260730-13158", "Diverging Memory Market Outlook in 2027", "2026-07-30"),
    "TrendForce forecasts global server shipments to grow faster in 2027 than the 17% YoY recorded in 2026.", "")
add("server-ai", "shipments_growth_yoy", "2026", 32.2, "%", "forecast",
    tf("20261014-13269", "CSP CapEx Projected to Exceed US$1.5 Trillion in 2027, with AI Server Revenue Growing Over 90% YoY", "2026-10-14"),
    "TrendForce now forecasts AI server shipments to grow 32.2% YoY in 2026 given the strong overall demand outlook.", "Latest (Oct 2026).")
add("server-ai", "shipments_growth_yoy", "2027", 36, "%", "forecast",
    tf("20261014-13269", "CSP CapEx Projected to Exceed US$1.5 Trillion in 2027", "2026-10-14"),
    "Consequently, AI server shipments are projected to increase by nearly 36% YoY.", "2027.")
add("server-ai", "revenue_share_of_server_market", "2026", 75, "%", "forecast",
    tf("20261014-13269", "CSP CapEx Projected to Exceed US$1.5 Trillion in 2027", "2026-10-14"),
    "This would account for nearly 75% of the projected $639.2 billion in total server market revenue", "AI server revenue ~$479B in 2026; ~81% / ~$920B in 2027.")
add("server", "cpu_shipments_growth_yoy", "2026", 31, "%", "forecast",
    tf("20261022-13279", "Server CPU Shipments Projected to Grow Over 40% YoY in 2027", "2026-10-22"),
    "Server CPU shipments are projected to increase 31% YoY in 2026.", "CPU sockets drive RDIMM count.")
add("server", "cpu_shipments_growth_yoy", "2027", ">40", "%", "forecast",
    tf("20261022-13279", "Server CPU Shipments Projected to Grow Over 40% YoY in 2027", "2026-10-22"),
    "drive server CPU shipments up by more than 40% YoY", "")
add("server-general", "shipments_growth_yoy", "2026", 1, "%", "forecast",
    ("SemiconSam (Jukan), summary of TrendForce Korea roadshow", "TrendForce Roadshow Korea Review", "https://www.semiconsam.com/p/trendforce-roadshow-korea-review", "2025-11-07"),
    "The shipment volume of general-purpose servers is expected to grow by only around 1%", "Nov-2025 view; superseded by CSP replacement wave.")
add("server-ai", "share_of_server_shipments", "2026", 17, "%", "forecast",
    ("SemiconSam (Jukan), summary of TrendForce Korea roadshow", "TrendForce Roadshow Korea Review", "https://www.semiconsam.com/p/trendforce-roadshow-korea-review", "2025-11-07"),
    "AI server share is increasing from 13% → 17% → approaching 20%", "Sequence likely 2025 -> 2026 -> 2027.")
add("server", "shipments_growth_yoy", "2024", 5.0, "%", "actual", apacer(2024, "2025-05"),
    "The global server shipments grew by 5.0% in 2024, recovering from the sharp decline in 2023.", "Apacer citing inSpectrum Jan 2025.")
add("server", "shipments_growth_yoy", "2025", 4.2, "%", "forecast", apacer(2024, "2025-05"),
    "The shipment of servers is expected to grow by 4.2% in 2025.", "inSpectrum Jan 2025.")
add("server", "shipments", "2015", 11.1, "million units", "actual",
    ("METI (citing Gartner)", "METI FY2021 report 000657", "https://www.meti.go.jp/meti_lib/report/2021FY/000657.pdf", "2022"),
    "about 11.1 million worldwide server shipments for full-year 2015", "SEARCH-SUMMARY: PDF blocked; quote is the search summary, not the document.")
add("server", "shipments", "2020", 12.11, "million units", "estimate",
    ("Communications Today (citing Gartner)", "A dynamic year ahead!", "https://www.communicationstoday.co.in/a-dynamic-year-ahead/", "2021"),
    "Gartner estimated 12.11 million server shipments worldwide in 2020", "SEARCH-SUMMARY: not fetched.")
add("server", "shipments", "2021", 13.539, "million units", "actual",
    ("CSET Georgetown (translation of China Compute Index 2022, citing IDC)", "China Compute Index 2022",
     "https://cset.georgetown.edu/wp-content/uploads/t0581_china_compute_index_2022_EN.pdf", "2022"),
    "2021 worldwide server shipments: 13.539 million units", "SEARCH-SUMMARY: not fetched. IDC definition.")

# ======================================================================
# 3. DDR5 penetration and DDR4 EOL
# ======================================================================
add("server-ddr5", "ddr5_share_of_server_platforms", "1Q23", 10, "%", "forecast",
    tf("20230109-11533", "QoQ Decline in DRAM ASP Will Moderate to Around 13~18% for 1Q23", "2023-01-09"),
    "the DDR5 penetration rate in the server DRAM segment is projected to reach just around 10% in 1Q23.", "")
add("pc-ddr5", "ddr5_share_of_pc_dram", "1Q23", 20, "%", "forecast",
    tf("20230109-11533", "QoQ Decline in DRAM ASP Will Moderate to Around 13~18% for 1Q23", "2023-01-09"),
    "the DDR5 penetration rate in the PC DRAM segment is projected to reach almost 20% in 1Q23", "")
add("server-ddr5", "ddr5_adoption_rate_server", "2023", 13.4, "%", "estimate",
    tf("20230815-11791", "Global Server Shipments for 2024 Projected to Undergo Constrained Growth, Estimated Annual Increase of 2.3%", "2023-08-15"),
    "the adoption rate of DDR5 for the entire year, across both CSP and OEM, will be around a mere 13.4%",
    "Platform adoption, not bit share. Heading: DDR5 penetration to surpass 50% only by 3Q24.")
add("server-ddr5", "ddr5_share_of_server_dram", "4Q23", 25, "%", "forecast", apacer(2022, "2023-05"),
    "The penetration rate is likely to be over 10% in the second half of the year, with the proportion reaching 25% in Q4.", "Apacer 2022 AR; industry view; basis not stated.")
add("pc-ddr5", "ddr5_share_of_pc_dram", "2H23", ">20", "%", "forecast", apacer(2022, "2023-05"),
    "The penetration rate is likely to be over 20% in the second half of the year.", "PC DDR5.")
add("server-ddr5", "ddr5_share_of_server_dram", "2024", 30, "%", "forecast", apacer(2023, "2024-05"),
    "The penetration rate of se rver DDR5 is expected to reach about 30% this year.", "Text break 'se rver' is in the PDF. Basis not stated.")
add("server-ddr5", "ddr5_share_of_server_dram_bits", "2024", 40, "%", "forecast",
    tf("20240722-12228", "Memory Industry Revenue Expected to Reach Record High in 2025 Due to Increasing Average Prices and the Rise of HBM and QLC", "2024-07-22"),
    "DDR5 will account for 40% of server DRAM bit shipments in 2024, increasing to 60–65% in 2025.", "Bit share. Fetched via dramexchange.com copy.")
add("server-ddr5", "ddr5_share_of_server_dram_bits", "2025", "60-65", "%", "forecast",
    tf("20240722-12228", "Memory Industry Revenue Expected to Reach Record High in 2025", "2024-07-22"),
    "DDR5 will account for 40% of server DRAM bit shipments in 2024, increasing to 60–65% in 2025.", "")
add("server-ddr5", "ddr5_share_of_server_dram_bits", "1Q25", 90, "%", "actual",
    ("TrendForce", "Bit Shipment Share of DDR5 Has Climbed to Around 90%, Boosting 1Q25 Server DRAM Revenue by 1.4% QoQ to US$10.688 Billion",
     "https://www.trendforce.com/research/download/RP250528SS", "2025-05-28"),
    "Bit Shipment Share of DDR5 Has Climbed to Around 90%", "Paywalled report; title only. Conflicts with the 60-65% 2025 forecast (much faster transition).")
add("pc-ddr5", "ddr5_overtakes_ddr4_pc", "2H24", ">50", "%", "forecast",
    tf("20230830-11812", "After a Low Base Year in 2023, DRAM and NAND Flash Bit Demand Expected to Increase by 13% and 16% Respectively in 2024", "2023-08-30"),
    "surpassing DDR4 in the latter half of 2024", "Qualitative crossover; value '>50' is our reading.")
add("server-ddr4", "eol_last_order", "2025-06", "Samsung", "date", "actual",
    ("TrendForce (news, citing Commercial Times)", "DDR4 Exit Timeline Unfolds for Top Memory Makers",
     "https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron/", "2025-07-09"),
    "Samsung is leading the transition, set to stop taking DDR4 orders by June 2025 and wrap up shipments by mid-December.", "Later partly delayed via an NCNR contract for a server customer (Tom's Hardware headline).")
add("server-ddr4", "eol_final_shipment", "1Q26", "Micron", "date", "actual",
    ("TrendForce (news, citing Commercial Times)", "DDR4 Exit Timeline Unfolds for Top Memory Makers",
     "https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron/", "2025-07-09"),
    "notified customers in June that DDR4 is entering end-of-life, with final shipments ending in Q1 2026.", "Mainstream DDR4; long-life DDR4 continues at Fab 6 (Manassas).")
add("server-ddr4", "eol_final_shipment", "2026-04", "SK hynix", "date", "actual",
    ("TrendForce (news, citing Commercial Times)", "DDR4 Exit Timeline Unfolds for Top Memory Makers",
     "https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron/", "2025-07-09"),
    "plans to stop orders in October 2025 and complete shipments by April 2026.", "")
add("server-ddr4", "eol_delay", "2026", "Samsung", "event", "actual",
    ("Tom's Hardware", "Samsung to delay its planned DDR4 end-of-life due to signing a long-term 'non-cancellable, non-returnable' contract with key customer",
     "https://www.tomshardware.com/pc-components/ddr4/samsung-to-delay-its-planned-ddr4-end-of-life-due-to-signing-a-long-term-non-cancellable-non-returnable-contract-with-key-customer-agreement-will-not-alleviate-consumer-shortage-supply-earmarked-for-server-clients", "2026"),
    "agreement will not alleviate consumer shortage, supply earmarked for server clients", "Headline only (body truncated); date not seen.")
add("ddr4-total", "ddr4_share_of_micron_dram_output", "2026", 7, "%", "forecast",
    tf("20260526-13061", "Micron's Fab 6 Starts LPDDR4 and DDR4 Production, but DDR4 Shortage Is Expected to Persist", "2026-05-26"),
    "TrendForce expects the share of DDR4 products in Micron's overall DRAM output to shrink to around 7% in 2026",
    "Fab 6 LPDDR4+DDR4 supply to quadruple by 2027 but no increase in Micron total LP4/DDR4 capacity; DDR4 short through 2026.")
add("ddr4-total", "micron_fab6_lp4_ddr4_supply_multiple", "2027", 4, "x vs 2026", "forecast",
    tf("20260526-13061", "Micron's Fab 6 Starts LPDDR4 and DDR4 Production, but DDR4 Shortage Is Expected to Persist", "2026-05-26"),
    "Micron has stated that the combined LPDDR4 and DDR4 supply from Fab 6 is projected to quadruple by 2027.",
    "Offset by OMT 1-alpha reductions: 'there are no plans to increase Micron's total production capacity for LPDDR4 and DDR4 DRAM.'")

# ======================================================================
# 4. Prices (TrendForce QoQ forecasts, Omdia module prices)
# ======================================================================
tf_px = [
    ("server", "server_dram_contract_price_qoq", "3Q25", "3-8", "20250707-12633", "Transition between DRAM Generations Drives Diverging 3Q25 Price Trends; Consumer DDR4 Prices Expected to Surge Over 40%", "2025-07-07",
     "with prices expected to rise by 3% to 8%.", ""),
    ("pc", "pc_dram_contract_price_qoq", "3Q25", "8-13", "20250707-12633", "Transition between DRAM Generations Drives Diverging 3Q25 Price Trends", "2025-07-07",
     "As a result, PC DRAM contract prices are expected to rise by 8% to 13% in the third quarter.", ""),
    ("ddr4-consumer", "consumer_ddr4_contract_price_qoq", "3Q25", "40-45", "20250707-12633", "Transition between DRAM Generations Drives Diverging 3Q25 Price Trends", "2025-07-07",
     "consumer DDR4 contract prices are forecast to surge by 40% to 45% in the third quarter.", "Later revised to 85-90% (Aug 2025)."),
    ("dram-conventional", "conventional_dram_contract_price_qoq", "3Q25", "10-15", "20250707-12633", "Transition between DRAM Generations Drives Diverging 3Q25 Price Trends", "2025-07-07",
     "average contract prices for conventional DRAM are projected to rise by 10% to 15% in 3Q25.", ""),
    ("ddr4-consumer", "consumer_ddr4_contract_price_qoq", "3Q25", "85-90", "20250811-12667", "DDR4 and LPDDR4 Supply Tightens Sharply in 2H25 as Structural Shortage Drives Strong Price Surge", "2025-08-11",
     "to a quarterly increase of 85–90%.", "Revision. Also: 8GB PC DDR4 module price exceeded DDR5 in July 2025 (price inversion)."),
    ("dram-conventional", "conventional_dram_contract_price_qoq", "4Q25", "8-13", "20250924-12733", "DRAM Prices to Continue Rising in 4Q25, Server Demand Surges Ahead While Legacy Process Products See Steeper Increases", "2025-09-24",
     "Overall, conventional DRAM prices are expected to rise 8–13% QoQ in 4Q25", "First forecast."),
    ("dram-conventional", "conventional_dram_contract_price_qoq", "4Q25", "18-23", "20251029-12758", "Tight DRAM Supply to Boost DDR5 Contract Prices—Profitability in 2026 Expected to Surpass HBM3e", "2025-10-29",
     "from an earlier forecast of 8–13% growth to 18–23%", "Revision; TrendForce said further upward revision likely."),
    ("dram-conventional", "conventional_dram_contract_price_qoq", "1Q26", "90-95", "20260202-12911", "Memory Price Outlook for 1Q26 Sharply Upgraded; QoQ Increases of All Product Categories to Hit Record Highs", "2026-02-02",
     "conventional DRAM contract prices has been revised upward, from a previous estimate of 55–60% to now 90–95%", ""),
    ("server", "server_dram_contract_price_qoq", "1Q26", 90, "20260202-12911", "Memory Price Outlook for 1Q26 Sharply Upgraded", "2026-02-02",
     "expected to drive server DRAM prices up by around 90% QoQ in 1Q26, marking the largest quarterly increase on record", ""),
    ("pc", "pc_dram_contract_price_qoq", "1Q26", ">100", "20260202-12911", "Memory Price Outlook for 1Q26 Sharply Upgraded", "2026-02-02",
     "PC DRAM prices in 1Q26 are projected to increase by over 100% QoQ, setting a new record for a quarterly surge.", ""),
    ("dram-conventional", "conventional_dram_contract_price_qoq", "2Q26", "58-63", "20260331-12995", "AI Server Demand to Drive Memory Contract Price Increases in 2Q26 as CSPs Secure Supply via Long-Term Agreements", "2026-03-31",
     "Conventional DRAM contract prices are projected to rise by 58–63% QoQ despite downside risks to end-market shipments.", "Server/PC split is in a chart image (not read)."),
    ("dram-conventional", "conventional_dram_contract_price_qoq", "3Q26", "13-18", "20260703-13134", "AI Server Demand Continues to Support Memory Prices in 3Q26, but Gains Moderate as Consumer Demand Weakens and High Base Effects Take Hold", "2026-07-03",
     "Conventional DRAM contract prices are forecast to rise 13–18% QoQ in 3Q26", ""),
    ("server", "server_dram_contract_price_qoq", "3Q26", "13-18", "20260709-13140", "Long-Term Agreements Cap Price Increases; Server DRAM Contract Prices Expected to Rise 13-18% QoQ in 3Q26", "2026-07-09",
     "Consequently, TrendForce predicts that server DRAM contract prices will rise by 13–18% quarter-over-quarter in 3Q26.", "LTAs cap gains; non-LTA buyers bear most of the increase."),
    ("dram-conventional", "conventional_dram_contract_price_qoq", "4Q26", "10-15", "20260930-13258", "AI Server Demand Sustains Memory Contract Price Increases in 4Q26, While Consumer-Side Pressure Persists", "2026-09-30",
     "Conventional DRAM contract prices are projected to grow 10–15% QoQ in 4Q26", "Latest. Segment split in chart image (not read)."),
    ("server", "server_dram_contract_price_cum", "2H25", 64, "20260825-13198", "Memory Prices Soar; DRAM and NAND Flash to Account for 68% of Major CSP CapEx in 2027", "2026-08-25",
     "Server DRAM—a key procurement category for CSPs—saw contract prices rise by a cumulative 64% in 2H25", ""),
    ("server", "server_dram_contract_price_yoy", "2026", 270, "20260825-13198", "Memory Prices Soar; DRAM and NAND Flash to Account for 68% of Major CSP CapEx in 2027", "2026-08-25",
     "with a further jump of approximately 270% expected in 2026", "Annual change; basis (avg-to-avg vs end-to-end) not stated."),
]
for seg, metric, per, val, slug, title, date, q, note in tf_px:
    add(seg, metric, per, val, "%", "forecast", tf(slug, title, date), q, note)

add("server", "server_dram_revenue", "1Q25", 10.688, "USD bn", "actual",
    ("TrendForce", "Bit Shipment Share of DDR5 Has Climbed to Around 90%, Boosting 1Q25 Server DRAM Revenue by 1.4% QoQ to US$10.688 Billion",
     "https://www.trendforce.com/research/download/RP250528SS", "2025-05-28"),
    "total server DRAM revenue for 1Q25 reached US$10.688 billion, marking a marginal QoQ growth of 1.4%", "Paywalled; summary only. Implies 4Q24 ~10.54 bn (derived).")
add("server", "server_dram_revenue_yoy", "4Q24", 84.4, "%", "actual",
    ("TrendForce", "QoQ 8.0% & YoY 84.4% in 4Q24 Server DRAM Revenue under Incessant Demand for DDR5",
     "https://www.trendforce.com/research/download/RP250307YR", "2025-03-07"),
    "server DRAM revenue grew by 8.0% QoQ and 84.4% YoY in 4Q24", "Paywalled; summary only.")
add("server", "server_dram_market_excl_hbm", "2026", 32.1, "USD bn", "forecast", apacer(2023, "2024-05"),
    "By 2026, the server DRAM (excluding HBM) market size is expected to reach USD 32.1 billion.", "Made before the 2025-26 price spike; now far too low. Original source not named.")

# Omdia module price tables (via IBK)
omdia_hdr_new = "1Q26 2Q26(F) 3Q26(F) 4Q26(F) 1Q27(F) 2Q27(F)"
omdia_hdr_old = "3Q25 4Q25 1Q26(F) 2Q26(F) 3Q26(F) 4Q26(F)"
px_new = {  # April-2026 Omdia table (IBK2)
    ("server-ddr5", "rdimm_64gb_ddr5_price"): ("64GB DDR5 $766 $1,035 $1,086 $1,119 $1,130 $1,130", [766, 1035, 1086, 1119, 1130, 1130]),
    ("server-ddr5", "rdimm_128gb_ddr5_price"): ("128GB DDR5 $2,146 $2,897 $3,042 $3,133 $3,165 $3,165", [2146, 2897, 3042, 3133, 3165, 3165]),
    ("server-ddr4", "rdimm_32gb_ddr4_price"): ("32GB DDR4 $399 $531 $558 $574 $580 $580", [399, 531, 558, 574, 580, 580]),
    ("pc-ddr5", "udimm_16gb_ddr5_price"): ("16GB DDR5 $122.8 $159.7 $170.8 $176.0 $177.7 177.7", [122.8, 159.7, 170.8, 176.0, 177.7, 177.7]),
    ("pc-ddr4", "udimm_16gb_ddr4_price"): ("16GB DDR4 $122.7 $159.5 $170.6 $175.8 $177.5 177.5", [122.7, 159.5, 170.6, 175.8, 177.5, 177.5]),
    ("ddr4-total", "ddr4_8gb_component_price"): ("8Gb DDR4 $7.65 $11.48 $12.28 $12.65 $12.77 $12.77", [7.65, 11.48, 12.28, 12.65, 12.77, 12.77]),
}
per_new = ["1Q26", "2Q26", "3Q26", "4Q26", "1Q27", "2Q27"]
for (seg, metric), (q, vals) in px_new.items():
    for p, v in zip(per_new, vals):
        kind = "estimate" if p == "1Q26" else "forecast"
        unit = "USD/die" if "component" in metric else "USD/module"
        add(seg, metric, p, v, unit, kind, IBK2, f"{omdia_hdr_new} ... {q}",
            "Omdia contract ASP table reproduced by IBK (표 1, p.10). pub_date approximate (chart through 26.5; Omdia Apr-2026 monthly).")
px_old = {  # Jan-2026 Omdia table (IBK1): keep 3Q25 & 4Q25 actuals + 1Q26F
    ("server-ddr5", "rdimm_64gb_ddr5_price"): ("64GB DDR5 $265 $451 $699 $839 $880 $907", [265, 451, 699]),
    ("server-ddr4", "rdimm_32gb_ddr4_price"): ("32GB DDR4 $131 $222 $355 $426 $447 $461", [131, 222, 355]),
    ("pc-ddr5", "udimm_16gb_ddr5_price"): ("16GB DDR5 $45.2 $72.2 $115.6 $138.7 $145.6 $150.0", [45.2, 72.2, 115.6]),
    ("pc-ddr4", "udimm_16gb_ddr4_price"): ("16GB DDR4 $48.1 $72.2 $115.5 $138.5 $145.5 $149.8", [48.1, 72.2, 115.5]),
    ("ddr4-total", "ddr4_8gb_component_price"): ("8Gb DDR4 $3.00 $4.50 $7.20 $8.64 $8.90 $8.99", [3.00, 4.50, 7.20]),
}
for (seg, metric), (q, vals) in px_old.items():
    for p, v in zip(["3Q25", "4Q25", "1Q26"], vals):
        kind = "forecast" if p == "1Q26" else "estimate"
        unit = "USD/die" if "component" in metric else "USD/module"
        note = "Omdia Jan-2026 table via IBK. "
        if p == "1Q26":
            note += "Jan forecast; the April table shows the 1Q26 outcome higher (revision upward)."
        add(seg, metric, p, v, unit, kind, IBK1, f"{omdia_hdr_old} ... {q}", note)
add("server-ddr5", "rdimm_64gb_ddr5_price", "2Q26", 1500, "USD/module", "estimate", MU_Q3,
    "If I try to plug in what a 64 GB server DRAM is, I can get, like, a $700 price for it compared to $1,500 today",
    "Analyst (TD Cowen) on the call, not Micron. Higher than Omdia 2Q26F $1,035; spot/no-LTA vs contract.")
add("dram-total", "dram_asp_qoq", "1Q26", 43, "%", "forecast", SSEC,
    "We revise up our outlook for DRAM price growth to 43% q-q in 1Q26 and 27% q-q in 2Q26", "Blended ASP (incl. LTA/HBM effects), lower than TrendForce contract quotes.")
add("dram-total", "dram_asp_qoq", "2Q26", 27, "%", "forecast", SSEC,
    "We revise up our outlook for DRAM price growth to 43% q-q in 1Q26 and 27% q-q in 2Q26", "Pace to slow below 10% q-q from 3Q26.")
add("ddr5-total", "ddr5_contract_price_change_ytd", "2025", 123, "%", "estimate", MIRAE,
    "DDR5 contract prices have already increased 123% YTD and are projected to continue rising throughout 2026", "As of Dec 2025. Further +45% upside by end-4Q26.")
add("dram-total", "micron_dram_price_qoq", "FQ4-2026", "high teens", "%", "actual", MU_Q4,
    "Prices increased high teens percentage range, driven by tight DRAM industry conditions.", "Micron fiscal Q4 (Jun-Aug 2026).")

# ======================================================================
# 5. Supply vs demand, allocation, LTAs
# ======================================================================
add("server", "order_fulfillment_rate", "1Q26", 66, "%", "estimate", SSEC,
    "the order fulfillment rate for server customers stands at 66% (vs below 60% in 4Q25)", "")
add("server", "order_fulfillment_rate", "4Q25", "<60", "%", "estimate", SSEC,
    "the order fulfillment rate for server customers stands at 66% (vs below 60% in 4Q25)", "")
add("server", "order_fulfillment_rate_us_cn", "late-2025", 70, "%", "estimate",
    ("Tom's Hardware", "Server DRAM prices surge up to 50% as AI-induced memory shortage hits hyperscaler supply - U.S. and Chinese customers only getting 70% order fulfillment",
     "https://www.tomshardware.com/pc-components/storage/server-dram-prices-surge-50-percent", "2025"),
    "U.S. and Chinese customers only getting 70% order fulfillment", "Headline only; body and date not seen.")
add("dram-total", "sufficiency_ratio", "2026", "-1 to -2", "%", "estimate",
    tf("20260730-13158", "Diverging Memory Market Outlook in 2027", "2026-07-30"),
    "TrendForce estimates the DRAM sufficiency ratio at approximately -1% to -2% in 2026.", "Gap widens in 2027.")
add("server", "hbm_plus_rdimm_share_of_dram_bit_supply", "2026", 51, "%", "forecast",
    tf("20260825-13198", "Memory Prices Soar; DRAM and NAND Flash to Account for 68% of Major CSP CapEx in 2027", "2026-08-25"),
    "HBM and RDIMM combined will account for 51% of DRAM bit supply in 2026", "")
add("server", "server_dram_plus_hbm_bit_supply_growth", "2027", 27, "%", "forecast",
    tf("20260825-13198", "Memory Prices Soar; DRAM and NAND Flash to Account for 68% of Major CSP CapEx in 2027", "2026-08-25"),
    "drive a 27% increase in combined server DRAM and HBM bit supply", "Driven by new fabs / migrations in 2H27.")
add("server-ddr5", "rdimm_bit_supply_growth", "2027", "15-20", "%", "forecast",
    tf("20260709-13140", "Long-Term Agreements Cap Price Increases; Server DRAM Contract Prices Expected to Rise 13-18% QoQ in 3Q26", "2026-07-09"),
    "total RDIMM bit supply will grow by only 15–20% YoY, significantly lagging the projected growth in server CPU shipments", "Compare server CPU +40% 2027.")
add("server", "memory_share_of_csp_capex", "2026", 47, "%", "forecast",
    tf("20260825-13198", "Memory Prices Soar; DRAM and NAND Flash to Account for 68% of Major CSP CapEx in 2027", "2026-08-25"),
    "DRAM and NAND Flash combined will account for 47% of CSPs' total CapEx in 2026", "")
add("server", "memory_share_of_csp_capex", "2027", 68, "%", "forecast",
    tf("20260825-13198", "Memory Prices Soar; DRAM and NAND Flash to Account for 68% of Major CSP CapEx in 2027", "2026-08-25"),
    "will push memory's share of CSP capex to 68% in 2027", "")
add("server", "micron_sca_count", "2026-06", 16, "agreements", "actual",
    ("Seoul Economic Daily", "Micron Locks in Revenue With Supply-Driven SCAs", "https://en.sedaily.com/international/2026/06/25/micron-locks-in-at-least-100-billion-in-dram-nand-revenue", "2026-06-25"),
    "We have signed 16 SCAs across AI data centers and consumer products.", "SCAs ~20% of DRAM shipments; $22B committed ($18B cash) at that time.")
add("server", "micron_sca_share_of_dram_shipments", "2026-06", 20, "%", "actual",
    ("Seoul Economic Daily", "Micron Locks in Revenue With Supply-Driven SCAs", "https://en.sedaily.com/international/2026/06/25/micron-locks-in-at-least-100-billion-in-dram-nand-revenue", "2026-06-25"),
    "The SCAs represent about 20% of DRAM shipments and 33% of NAND flash shipments", "Machine-translated Korean article.")
add("server", "micron_sca_count", "2026-09", 26, "agreements", "actual", MU_Q4,
    "To date, we have signed 26 SCAs, which we currently estimate to be over 35% of our revenue through 2030.", "")
add("server", "micron_sca_rpo", "2026-09", 150, "USD bn", "actual", MU_Q4,
    "our remaining performance obligations, or RPO, is approximately $150 billion.", "Only SCAs with a set pricing framework.")
add("server", "micron_customer_financial_commitments", "2026-09", 32, "USD bn", "actual", MU_Q4,
    "For the 26 signed SCAs and extensions, financial commitments from customers have increased to $32 billion", "Mostly cash deposits.")
add("server", "micron_customer_cash_deposits_on_balance_sheet", "2026-09", 12.7, "USD bn", "actual", MU_Q4,
    "Customer cash deposits on our balance sheet at the end of fiscal Q4 were $12.7 billion.", "$12.3B received in FQ4.")
add("server", "micron_output_committed", "2027", ">75", "%", "actual", MU_Q4,
    "2027, more than 75% of our output is already committed for 2027.", "SCA + non-SCA.")
add("server", "skhynix_lta_share_of_capacity", "2027-2028", ">50", "%", "actual", SKH_NR,
    "The LTA volume secured to date corresponds to more than 50% of total production capacity for 2027 and 2028.", "14 customers incl. CSPs; terms typically five years.")
add("server", "skhynix_lta_customers", "2026-10", 14, "customers", "actual", SKH_NR,
    "The company has currently signed LTAs with 14 major customers, including leading global cloud service providers (CSPs)", "")
add("server-ddr5", "skhynix_server_ddr5_shipments_qoq", "3Q26", ">40", "%", "actual", SKH_CALL,
    "shipments of server DDR5 increased by over 40% compared to Q2, driving overall growth in DRAM bit shipments", "Total DRAM bits ~+10% QoQ 3Q26; 4Q26 guided mid-20% QoQ.")
add("dram-total", "skhynix_dram_bit_shipments_qoq", "4Q26", "mid-20s", "%", "forecast", SKH_CALL,
    "fourth quarter shipment volume is expected to grow meaningfully by mid-20% sequentially.", "")

# ======================================================================
# 6. Module supply chain: RCD/PMIC/MRDIMM/CXL
# ======================================================================
add("server-ddr5", "rambus_product_revenue", "3Q26", 114, "USD mn", "actual", RMBS,
    "We delivered a new all-time high in quarterly product revenue, reaching approximately $114 million", "RCD-led; Q4 guided >30% YoY.")
add("server-mrdimm", "mrdimm_tam_rambus", "multi-year", 600, "USD mn", "forecast", RMBS,
    "we still size at $600 million in total.", "'MRDIMM remains very modest'; qual/pre-production shipments in 2026; shallower ramp.")
add("server-ddr5", "memory_channels_per_cpu", "2026-2027", "8 to 12-16", "channels", "estimate", RMBS,
    "DDR-based server platforms are expanding from eight memory channels to 12- 16 channels", "More DIMMs per socket; Rambus also sees 'memory de-speccing' (lower GB per module).")
add("server-mrdimm", "montage_new_interconnect_products_revenue", "1H26", 538, "RMB mn", "actual",
    ("Montage Technology (interim report via FinancialFilings)", "Montage Technology 2026 Interim Results Announcement",
     "https://financialfilings.com/filings/montage-technology-co-ltd/interim-quarterly-report/2026/60312233/", "2026-08-29"),
    "Four newer products (MRCD/MDB, PCIe Retimer, CKD and CXL MXC) brought in RMB 538M, up 80.7%",
    "SEARCH-SUMMARY: not fetched. Interconnect chips RMB 3.111B (+26.4%). Gen2 MRDIMM in broad trials, not full mass production.")

# ======================================================================
# 7. PCs
# ======================================================================
add("pc", "shipments", "2018", 259.583, "million units", "actual",
    ("IDC (via MarketScreener)", "Traditional PC Volumes Close Out an Impressive 2019 with Fourth Quarter Growth of 4.8%, According to IDC",
     "https://www.marketscreener.com/news/latest/Traditional-PC-Volumes-Close-Out-an-Impressive-2019-with-Fourth-Quarter-Growth-of-4-8-According-to-29831194/", "2020-01-13"),
    "Total 266,690 100% 259,583 100% 2.7%", "Thousands of units; traditional PC (desktop, notebook, workstation).")
add("pc", "shipments", "2019", 266.690, "million units", "actual",
    ("IDC (via MarketScreener)", "Traditional PC Volumes Close Out an Impressive 2019 with Fourth Quarter Growth of 4.8%, According to IDC",
     "https://www.marketscreener.com/news/latest/Traditional-PC-Volumes-Close-Out-an-Impressive-2019-with-Fourth-Quarter-Growth-of-4-8-According-to-29831194/", "2020-01-13"),
    "Total 266,690 100% 259,583 100% 2.7%", "Preliminary.")
add("pc", "shipments", "2021", 348.8, "million units", "actual",
    ("PCWorld (citing IDC)", "Roaring 2021 sales proved the PC isn't even close to dead",
     "https://www.pcworld.com/article/605424/the-pcs-2021-sales-proved-again-that-the-pc-isnt-even-close-to-dead.html", "2022-01-14"),
    "IDC reported even sharper growth: 14.8 percent, up to 348.8 million units.", "IDC preliminary.")
add("pc", "shipments", "2021", 339.8, "million units", "actual",
    ("PCWorld (citing Gartner)", "Roaring 2021 sales proved the PC isn't even close to dead",
     "https://www.pcworld.com/article/605424/the-pcs-2021-sales-proved-again-that-the-pc-isnt-even-close-to-dead.html", "2022-01-14"),
    "According to Gartner, PC shipments surged 9.9 percent in 2021 to 339.8 million units.", "Gartner definition includes Chromebooks/ultramobiles.")
add("pc", "shipments", "2022", 292.3, "million units", "actual",
    ("InfoTechLead (citing IDC)", "PC shipments in 2022 drop 16.5% to 292.3 mn: IDC",
     "https://infotechlead.com/devices/pc-shipments-in-2022-drop-16-5-to-292-3-mn-idc-76212", "2023-01"),
    "PC shipments in 2022 drop 16.5% to 292.3 mn: IDC", "Headline. IDC later restated 2022 (search summary says 301.5M in the Jan-2024 release).")
add("pc", "shipments", "2023", 259.5, "million units", "actual",
    ("IDC (via StreetInsider/Business Wire)", "Worldwide PC Shipments Declined 2.7% Year Over Year in the Fourth Quarter of 2023 but Visions of Growth Lie Ahead, According to IDC",
     "https://www.streetinsider.com/Business%2BWire/Worldwide%2BPC%2BShipments%2BDeclined%2B2.7%25%2BYear%2BOver%2BYear%2Bin%2Bthe%2BFourth%2BQuarter%2Bof%2B2023%2Bbut%2BVisions%2Bof%2BGrowth%2BLie%2BAhead%2C%2BAccording%2Bto%2BIDC/22618032.html", "2024-01-10"),
    "259.5 million units, down 13.9% year over year from 301.5 million units in 2022", "SEARCH-SUMMARY: page returned 403.")
add("pc", "shipments", "2025", 284.7, "million units", "actual",
    ("FoneArena (citing IDC)", "Global PC Shipments up 9.6% YoY in Q4 2025; memory crisis to change market dynamics in 2026: IDC",
     "https://www.fonearena.com/blog/473498/global-pc-shipments-q4-2025.html", "2026-01-14"),
    "total shipments reaching 284.7 million in 2025, an increase of 8.1% compared to 2024.", "Implies 2024 ~263.4M (derived).")
add("pc", "shipments_growth_yoy", "2026", -11.3, "%", "forecast",
    ("IDC", "PC Market Enters Volatile Territory as Memory Shortage Persists Through 2027",
     "https://www.idc.com/resource-center/blog/pc-market-enters-volatile-territory-as-memory-shortage-persists-through-2027/", "2026-06-02"),
    "IDC now forecasts global PC shipments will decline 11.3% for the full year", "Q4 2026 seen -20% YoY.")
add("pc", "asp_growth", "2026", 17, "%", "forecast",
    ("IDC", "PC Market Enters Volatile Territory as Memory Shortage Persists Through 2027",
     "https://www.idc.com/resource-center/blog/pc-market-enters-volatile-territory-as-memory-shortage-persists-through-2027/", "2026-06-02"),
    "IDC forecasts ASP growth of 17% in 2026", "No relief before end-2027.")
add("pc", "shipments", "3Q26", 62.7, "million units", "actual",
    ("VenSearch (citing IDC preliminary)", "IDC: PC shipments fell 20.1% in Q3 2026 as memory-driven price hikes hit demand",
     "https://www.vensearch.com/insights/idc-pc-shipments-fell-20-1-in-q3-2026-as-memory-driven-price-hikes-hit-demand", "2026-10-09"),
    "Worldwide PC shipments fell 20.1% year over year in the third quarter of 2026, to 62.7 million units", "IDC preliminary 2026-10-08.")
add("pc", "notebook_shipments_growth_yoy", "2026", -9.4, "%", "forecast",
    tf("20260904-13217", "Improved CPU Supply Narrows 2026 Global Notebook Shipment Decline to 9.4%, but Brands Still Face Heavy Cost Pressure", "2026-09-04"),
    "the decline in global notebook shipments for full-year 2026 is expected to narrow to 9.4% YoY", "Was -14.8% in Mar 2026.")
add("pc", "notebook_core_components_share_of_bom", "3Q26", 68, "%", "estimate",
    tf("20260904-13217", "Improved CPU Supply Narrows 2026 Global Notebook Shipment Decline to 9.4%", "2026-09-04"),
    "this share had risen to 68% by 3Q26", "CPU+DRAM+SSD for a US$900 notebook; 45% in 1Q25.")
add("pc", "notebook_price_rise_needed_vs_1q25", "3Q26", 80, "%", "estimate",
    tf("20260904-13217", "Improved CPU Supply Narrows 2026 Global Notebook Shipment Decline to 9.4%", "2026-09-04"),
    "by 3Q26, brands would need to raise the price of a comparable 1Q25 product by approximately 80%", "To hold margin.")
add("pc", "notebook_shipments_growth_yoy", "2027", "low-single-digit decline", "%", "forecast",
    tf("20261008-13264", "Rising Costs Threaten Notebook Demand in 2027, Raising Risks of Shipment Declines and Price Increases", "2026-10-08"),
    "Global notebook shipments are currently projected to decline by a low-single-digit percentage in 2027.", "High-single-digit decline if costs fully passed through.")
add("pc", "unit_decline_2026", "2026", "double-digit", "%", "forecast", MU_Q4,
    "despite potential double-digit overall unit declines in both markets.", "PC and mobile.")
add("pc", "avg_notebook_dram_content", "2023", 10.5, "GB/unit", "actual",
    tf("20240625-12200", "CSPs to Expand into Edge AI, Driving Average NB DRAM Capacity Growth by at Least 7% in 2025", "2024-06-25"),
    "the average NB DRAM capacity will grow from 10.5 GB in 2023 to 11.8 GB in 2024, marking a 12% increase", "Notebook only.")
add("pc", "avg_notebook_dram_content", "2024", 11.8, "GB/unit", "forecast",
    tf("20240625-12200", "CSPs to Expand into Edge AI, Driving Average NB DRAM Capacity Growth by at Least 7% in 2025", "2024-06-25"),
    "the average NB DRAM capacity will grow from 10.5 GB in 2023 to 11.8 GB in 2024, marking a 12% increase", "")
add("pc", "avg_notebook_dram_content", "2025", 12.6, "GB/unit", "derived",
    tf("20240625-12200", "CSPs to Expand into Edge AI, Driving Average NB DRAM Capacity Growth by at Least 7% in 2025", "2024-06-25"),
    "the overall average capacity is expected to grow by 0.8 GB, for an increase of at least 7%", "DERIVED: 11.8 + 0.8. Pre-shortage forecast; 2026 content likely cut (de-speccing).")
add("pc", "laptop_shipments", "2026", 180, "million units", "forecast", MIRAE,
    "laptop shipments are projected to decline 2.6% YoY to 180mn units.", "Dec-2025 view, before deeper cuts.")

# ---- search-summary-only rows (source PDF blocked by Cloudflare) -------
FMS = ("TrendForce (Mark Liu, FMS 2024 talk)", "FMS 2024 ASIA-202-1 presentation",
       "https://files.futurememorystorage.com/proceedings/2024/20240807_ASIA-202-1_Mark_Liu.pdf", "2024-08-07")
for seg, per, val, kind in [("server", "2024", 718, "estimate"), ("server", "2025", 853, "forecast"),
                            ("server-ai", "2024", 1792, "estimate"), ("server-ai", "2025", 2098, "forecast")]:
    add(seg, "avg_dram_content", per, val, "GB/unit", kind, FMS,
        "All servers combined: 718 GB in 2024, rising to 853 GB in 2025; AI/HPC servers: 1,792 GB in 2024, rising to 2,098 GB in 2025",
        "SEARCH-SUMMARY: PDF download blocked; numbers not verified. Higher than Mirae (597/717): different basis (maybe incl. HBM for AI).")
add("server", "server_market_revenue", "2025", 444.1, "USD bn", "actual",
    ("IDC", "Worldwide Server Market Finished 2025 With an All-Time Record of $444 Billion",
     "https://www.idc.com/resource-center/blog/press-release-type/tracker-press-release/", "2026-03"),
    "Worldwide Server Market Finished 2025 With an All-Time Record of $444 Billion",
    "Title seen in search results; +80.4% YoY per summary. Not fetched.")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(HDR)
    w.writerows(rows)
print(len(rows), "rows")
