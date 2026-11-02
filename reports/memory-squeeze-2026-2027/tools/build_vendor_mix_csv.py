# Builds sources/vendor-mix.csv. Every row cites a fetched page, a downloaded PDF, or (flagged in notes) a search summary.
import csv, sys

H = "segment,metric,period,value,unit,kind,publisher,title,url,pub_date,quote,notes".split(",")
rows = []
def r(*a):
    assert len(a) == 12, a
    rows.append(a)

# ---------- sources ----------
CP_SED = ("Counterpoint Research (via Seoul Economic Daily)", "Samsung's HBM Market Share Jumps to 33%, Narrowing Gap With SK hynix",
          "https://en.sedaily.com/finance/2026/09/03/samsung-doubles-hbm-market-share-to-33-percent-narrowing", "2026-09-03")
VLSI = ("VLSI Korea (citing ChosunBiz, Counterpoint, JPMorgan, UBS, Bernstein)", "Samsung Ahead in Q3 HBM Revenue (Bernstein HBM crossover)",
        "https://www.vlsi.kr/en/bernstein-hbm-crossover-en/", "2026-10-25")
SSEC = ("Samsung Securities", "Tech sector update: Inflection points in memory narrative",
        "https://www.bondweb.co.kr/Data/20261/28/menu01/2026012820.pdf", "2026-01-27")
DAISHIN = ("Daishin Securities", "Semiconductors industry report: Breaking the rules",
           "https://stock.mk.co.kr/uploads/20260225/1771985434_3b4da2366163be8020e7.pdf", "2026-02-25")
CITI = ("Citi (via NeoTeo)", "Memory chip shortage 2027: Citi's HBM forecast",
        "https://www.neoteo.com/en/citi-forecasts-a-severe-memory-chip-shortage-in-2027", "2026-10-02")
MIRAE = ("Mirae Asset Securities", "[2026 Outlook Report] Semiconductors: Robust earnings cycle ahead (pp.29-35 company tables)",
         "https://securities.miraeasset.com/bbs/download/2141014.pdf?attachmentId=2141014", "2025-12-15")
LS = ("LS Securities", "Samsung Electronics company update: 2026 + 2027 = k + f(macro, AI profitability) (Table 3 DRAM estimates)",
      "https://file.alphasquare.co.kr/media/pdfs/company-report/_260415%20%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8_%EC%A0%95%EC%9A%B0%EC%84%B1_47_Online%20report%20_%206_10p_%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90.pdf", "2026-04-15")
SKSEC = ("SK Securities", "Semiconductors: Be strong (memory dual market)",
         "https://stock.mk.co.kr/uploads/20260420/1776661662_b73027c46e9060bfe9f8.pdf", "2026-04-20")
CP_SKH = ("Counterpoint Research", "SK hynix Beats Expectations With AI-driven Innovations",
          "https://counterpointresearch.com/en/insights/post-insight-research-notes-blogs-sk-hynix-beats-expectations-with-aidriven-innovations", "2025-04-24")
SKH_Q425T = ("SK hynix (transcript via StockAnalysis/Quartr)", "SK hynix Q4 2025 earnings call transcript",
             "https://stockanalysis.com/quote/krx/000660/transcripts/397711-q4-2025/", "2026-01-29")
SKH_Q326T = ("SK hynix (transcript via StockAnalysis/Quartr)", "SK hynix Q3 2026 earnings call transcript",
             "https://stockanalysis.com/quote/krx/000660/transcripts/717350-q3-2026/", "2026-10-28")
SEC_Q425T = ("Samsung Electronics (transcript via StockAnalysis/Quartr)", "Samsung Electronics Q4 2025 earnings call transcript",
             "https://stockanalysis.com/quote/krx/005930/transcripts/405206-q4-2025/", "2026-01-29")
SEC_Q226T = ("Samsung Electronics (transcript via StockAnalysis/Quartr)", "Samsung Electronics Q2 2026 earnings call transcript",
             "https://stockanalysis.com/quote/krx/005930/transcripts/645485-q2-2026/", "2026-07-30")
SEC_Q326T = ("Samsung Electronics (transcript via StockAnalysis/Quartr)", "Samsung Electronics Q3 2026 earnings call transcript",
             "https://stockanalysis.com/quote/krx/005930/transcripts/718820-q3-2026/", "2026-10-29")
MU_Q425 = ("Micron (transcript via StockAnalysis/Quartr)", "Micron FQ4 2025 earnings call transcript",
           "https://stockanalysis.com/stocks/mu/transcripts/388210-q4-2025/", "2025-09-23")
MU_Q126 = ("Micron (transcript via The Motley Fool)", "Micron MU Q1 2026 earnings call transcript",
           "https://www.fool.com/earnings/call-transcripts/2025/12/17/micron-mu-q1-2026-earnings-call-transcript/", "2025-12-17")
MU_Q226 = ("Micron (transcript via The Motley Fool)", "Micron MU Q2 2026 earnings call transcript",
           "https://www.fool.com/earnings/call-transcripts/2026/03/18/micron-mu-q2-2026-earnings-call-transcript/", "2026-03-18")
MU_Q326 = ("Micron (transcript via StockAnalysis/Quartr)", "Micron FQ3 2026 earnings call transcript",
           "https://stockanalysis.com/stocks/mu/transcripts/609470-q3-2026/", "2026-06-24")
MU_Q426 = ("Micron", "Micron Fiscal Q4 2026 Earnings Call Prepared Remarks",
           "https://s25.q4cdn.com/621799436/files/doc_financials/2026/q4/Q4-FY26-Prepared-Remarks.pdf", "2026-09-30")
SKH_DECK = {
    "2026Q3": ("SK hynix", "SK hynix 3Q26 earnings presentation (p.17 Revenue by Application)", "https://irsvc.teletogether.com/hynix/pdf/hynix2026Q3_eng.pdf", "2026-10-28"),
    "2026Q2": ("SK hynix", "SK hynix 2Q26 earnings presentation (p.16 Revenue by Application)", "https://irsvc.teletogether.com/hynix/pdf/hynix2026Q2_eng.pdf", "2026-07-29"),
    "2025Q4": ("SK hynix", "SK hynix 4Q25 earnings presentation (p.18 Revenue by Application)", "https://irsvc.teletogether.com/hynix/pdf/hynix2025Q4_eng.pdf", "2026-01-29"),
}
INV_SKH = ("Investing.com", "SK hynix Q3 2026 slides: revenue tops 100T, 80% margin on AI boom",
           "https://www.investing.com/news/company-news/sk-hynix-q3-2026-slides-revenue-tops-100t-80-margin-on-ai-boom-93CH-4977357", "2026-10-27")
CXMT_REG = ("CXMT (ChangXin Technology Group)", "CXMT STAR Market IPO prospectus, registration draft (注册稿), 主营业务收入构成",
            "https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=12358280&stockid=688825", "2026 (registration draft; exact date not shown)")
CXMT_SB = ("CXMT (ChangXin Technology Group)", "CXMT STAR Market IPO prospectus, filing draft (申报稿)",
           "https://static.sse.com.cn/stock/disclosure/announcement/c/202512/002170_20251230_B8QS.pdf", "2025-12-30")
KIS = ("Korea Investment & Securities", "Simmtech (222800) report, Table 19: SoCAMM2 share and revenue estimates by company 2026-2027",
       "https://www.simmtech.com/upload/media/file/638972081688174181.pdf", "2025-10-27")
BNK = ("BNK Investment & Securities", "Semiconductor materials/parts/equipment industry analysis: memory supercycle (III-4 SOCAMM2)",
       "https://www.bondweb.co.kr/Data/20262/3/menu01/ratingBNK_886176.pdf", "2026-02-03")
KB_JA = ("KB Securities (via Korea JoongAng Daily)", "AI semiconductor market shifts focus from HBM to low-power DRAM module Socamm2",
         "https://www.koreajoongangdaily.com/business/ai-semiconductor-market-shifts-focus-from-hbm-to-low-power-dram-module-socamm2/12614719", "2026-03-11")
HK_GDDR = ("TrendForce (via Hankyung / Daum)", "그래픽D램도 잡았다…\"삼성, GDDR7 시장 70% 장악\"",
           "https://v.daum.net/v/20251203182738336", "2025-12-03")
KT_MOB = ("Omdia (via The Korea Times)", "Memory makers' race for AI servers expands to low-power chips",
          "https://www.koreatimes.co.kr/amp/business/tech-science/20251125/memory-makers-race-for-ai-servers-expands-to-low-power-chips", "2025-11-25")
TF_MOB = ("TrendForce", "4Q25 Revenue Ranking among Mobile DRAM Suppliers (report page)",
          "https://www.trendforce.com/research/download/RP260304MS", "2026-03-05")
TF_SRV = ("TrendForce", "2Q25 Revenue Ranking among Server DRAM Suppliers (report page)",
          "https://www.trendforce.com/research/download/RP250912IU", "2025-09-12")
TF_2Q26 = ("TrendForce", "DRAM Industry Revenue Rises 59.5% QoQ in 2Q26 as Supply Expansion Continues to Lag Demand Growth",
           "https://www.trendforce.com/presscenter/news/20260907-13219.html", "2026-09-07")
TF_DDR4 = ("TrendForce", "DDR4 Exit Timeline Unfolds for Top Memory Makers: Plans for Samsung, SK hynix and Micron",
           "https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron/", "2025-07-09")
NANYA_AM = ("Nanya Technology (transcript summary via AlphaMemo)", "南亞科 (2408) 2026/10/12 法說會逐字稿與重點摘要",
            "https://www.alphamemo.ai/free-transcripts/ebd9291c-4bc4-4822-b8ce-06e060432bea", "2026-10-12")
NANYA_FT = ("Focus Taiwan (CNA)", "Nanya Technology expects DRAM prices, margins to rise in Q4",
            "https://focustaiwan.tw/business/202610120025", "2026-10-12")
NANYA_IR = ("Nanya Technology", "南亞科技 2026 年第三季合併財務報告 (press release)",
            "https://www.nanya.com/tw/IR/16/%E6%96%B0%E8%81%9E%E7%A8%BF?IRId=14188", "2026-10-12")
EDAILY = ("Edaily (citing TrendForce)", "SamsungElectronics: \"DRAM Market Share to Exceed 40% Next Year\"... Confidence in AI Memory",
          "https://en.edaily.co.kr/news/eda202606245411/", "2026-06-24")
GS_YNA = ("Goldman Sachs (via Yonhap; search summary only)", "골드만, 삼전 목표가 '48만원→49만원'…\"펀더멘털 변화없어\"",
          "https://www.yna.co.kr/amp/view/AKR20260803112800008", "2026-08-03")
SEMI = ("SemiAnalysis", "China's CXMT Is Set to Challenge DRAM Incumbents",
        "https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram", "2026-06-23")
UBS = ("UBS (via Investing.com)", "UBS says Samsung to reach market share parity for HBM with SK Hynix by 2027",
       "https://www.investing.com/news/stock-market-news/ubs-says-samsung-to-reach-market-share-parity-for-hbm-with-sk-hynix-by-2027-4684487", "2026-05-13")

def S(seg, metric, period, value, unit, kind, src, quote, notes):
    r(seg, metric, period, value, unit, kind, src[0], src[1], src[2], src[3], quote, notes)

# ================= HBM: vendor share of the HBM segment =================
q = "Samsung held a 33% revenue share of the HBM market in the second quarter"
S("hbm", "Samsung HBM market share", "2026Q2", "33", "% of HBM revenue", "estimate", CP_SED, q, "vendor=Samsung; basis=revenue; Counterpoint quarterly tracker as reported by Seoul Economic Daily.")
S("hbm", "SK hynix HBM market share", "2026Q2", "50", "% of HBM revenue", "estimate", CP_SED, "The figure still trails SK hynix at 50%", "vendor=SK hynix; basis=revenue; Counterpoint.")
S("hbm", "Micron HBM market share", "2026Q2", "18", "% of HBM revenue", "estimate", CP_SED, "Micron's share slipped 3 percentage points to 18% over the same period", "vendor=Micron; basis=revenue; Counterpoint.")
S("hbm", "Samsung HBM market share", "2026Q1", "21", "% of HBM revenue", "estimate", CP_SED, "That marks a 12 percentage-point jump from 21% in the previous quarter.", "vendor=Samsung; basis=revenue; Counterpoint.")
S("hbm", "SK hynix HBM market share", "2026Q1", "58", "% of HBM revenue", "estimate", VLSI, "SK hynix's HBM revenue share falling from 58% in Q1 2026 to 50% in Q2", "vendor=SK hynix; basis=revenue; Counterpoint via ChosunBiz via VLSI.")
S("hbm", "Micron HBM market share", "2026Q1", "21", "% of HBM revenue", "derived", CP_SED, "Micron's share slipped 3 percentage points to 18% over the same period", "vendor=Micron; basis=revenue; derived 18 + 3 = 21. Matches Counterpoint table row in hbm-gddr.csv.")
S("hbm", "SK hynix HBM market share", "2025Q2", "64", "% of HBM revenue", "estimate",
  ("Counterpoint Research", "Global DRAM and HBM Market Share: Quarterly", "https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share", "2026-09-02"),
  "In Q2 2026, SK Hynix maintained its top position with 50%, but showed a decline compared to 64% in the same period of the previous year.",
  "vendor=SK hynix; basis=revenue; quote reused from hbm-gddr.csv. Same tracker gives Samsung 15 / Micron 21 for 2025Q2 (table values, not in quote).")
S("hbm", "Samsung HBM market share", "2025", "21", "% of HBM shipments", "estimate", SSEC, "we forecast SEC's HBM market share will rise from 21% in 2025 to 26% in 2026", "vendor=Samsung; basis=bit (chart titled 'HBM shipments: Market share, by supplier').")
S("hbm", "Samsung HBM market share", "2026", "26", "% of HBM shipments", "forecast", SSEC, "we forecast SEC's HBM market share will rise from 21% in 2025 to 26% in 2026", "vendor=Samsung; basis=bit.")
S("hbm", "SK hynix HBM market share", "2025", "58", "% of HBM shipments", "estimate", SSEC, "36 46 37 21 26 48 51 54 58 52 16 4 8 21 22", "vendor=SK hynix; basis=bit; chart data labels read as Samsung/SKH/Micron for 2022-2026; mapping inferred from the 21/26 Samsung text and column sums of 100. Weak (chart parse).")
S("hbm", "SK hynix HBM market share", "2026", "52", "% of HBM shipments", "forecast", SSEC, "36 46 37 21 26 48 51 54 58 52 16 4 8 21 22", "vendor=SK hynix; basis=bit; chart parse, see 2025 row.")
S("hbm", "Micron HBM market share", "2025", "21", "% of HBM shipments", "estimate", SSEC, "36 46 37 21 26 48 51 54 58 52 16 4 8 21 22", "vendor=Micron; basis=bit; chart parse.")
S("hbm", "Micron HBM market share", "2026", "22", "% of HBM shipments", "forecast", SSEC, "36 46 37 21 26 48 51 54 58 52 16 4 8 21 22", "vendor=Micron; basis=bit; chart parse.")
S("hbm", "Samsung HBM bit growth", "2026", "91", "% YoY", "forecast", SSEC, "SEC should see 91% bit growth in HBM in 2026", "vendor=Samsung; basis=bit. Same note: SK hynix +39%.")
dq = "40 49 41 22 29 39 49 49 52 57 49 39 10 2 8 21 19 18"
for v, vals in (("Samsung", ("22", "29", "39")), ("SK hynix", ("57", "49", "39")), ("Micron", ("21", "19", "18"))):
    for yr, val in zip(("2025", "2026", "2027"), vals):
        S("hbm", f"{v} HBM market share", yr, val, "% of HBM shipments", "estimate" if yr == "2025" else "forecast", DAISHIN, dq,
          f"vendor={v}; basis=bit (chart 59 note: 출하량 기준). Labels read as 2022-2027 series for Samsung, SKH, Micron; remainder = China (~3% 2026, ~4% 2027, derived). Weak (chart parse).")
S("hbm", "SK hynix HBM4 market share", "2026", "44", "% of HBM4 shipments", "forecast", DAISHIN, "2026년 HBM4 시장 점유율 (출하량 기준)의 경우, SK하이닉스 44%, 삼성전자 38%, Micron Technology 18%", "vendor=SK hynix; basis=bit; HBM4 only. Samsung 38, Micron 18 in same sentence.")
S("hbm", "Samsung HBM market share", "2026", "30", "% of HBM market", "forecast", CITI, "Citi's estimates put Samsung's share of the HBM market at about 30% in 2026 and forecast about 42% in 2027.", "vendor=Samsung; basis=unstated (bit vs revenue not given).")
S("hbm", "Samsung HBM market share", "2027", "42", "% of HBM market", "forecast", CITI, "Citi's HBM market-share forecast for 2027 puts Samsung at about 42%, SK hynix at 35% and Micron at 22%.", "vendor=Samsung; basis=unstated.")
S("hbm", "SK hynix HBM market share", "2027", "35", "% of HBM market", "forecast", CITI, "The forecast puts SK hynix at 35%, down from an estimated 47%, while Micron is projected to remain at 22%.", "vendor=SK hynix; basis=unstated; 47% is Citi 2026 estimate.")
S("hbm", "Micron HBM market share", "2027", "22", "% of HBM market", "forecast", CITI, "The forecast puts SK hynix at 35%, down from an estimated 47%, while Micron is projected to remain at 22%.", "vendor=Micron; basis=unstated.")
S("hbm", "SK hynix HBM market share", "2026", "46", "% of HBM market", "forecast", VLSI, "JPMorgan expects SK hynix's HBM share to step down from 60% in 2025 to 46% in 2026 and 41% in 2027.", "vendor=SK hynix; basis=unstated; JPMorgan via ChosunBiz via VLSI. 2025 = 60, 2027 = 41.")
S("hbm", "SK hynix HBM market share", "2027", "41", "% of HBM market", "forecast", VLSI, "JPMorgan expects SK hynix's HBM share to step down from 60% in 2025 to 46% in 2026 and 41% in 2027.", "vendor=SK hynix; basis=unstated; JPMorgan.")
S("hbm", "Samsung HBM market share", "2027", "41", "% of HBM bit shipments", "forecast", VLSI, "UBS's 2027 bit-shipment framework has Samsung at 41% and SK hynix at 39%.", "vendor=Samsung; basis=bit; UBS. Earlier UBS note (hbm-gddr.csv) says ~40/~40/~20.")
S("hbm", "Samsung HBM revenue", "2026Q3", "8.7", "USD bn", "estimate", VLSI, "Bernstein's October 22, 2026 estimates put Samsung's Q3 HBM revenue at $8.7B (+33% QoQ), ahead of SK hynix's $7.6B (+11%).", "vendor=Samsung; basis=revenue; Bernstein model on export data, not company-reported. SK hynix 7.6.")
S("hbm", "Samsung HBM share vs its DRAM share", "2026Q3", "in line", "qualitative", "actual", SEC_Q326T, "bringing HBM market share in line with our overall DRAM market share already in the third quarter", "vendor=Samsung; basis=unstated (company). With TrendForce 2Q26 DRAM share 39.4% this implies Samsung HBM share ~35-40% in 3Q26.")
S("hbm", "Micron HBM share vs its DRAM share", "CY2025Q3", "in line", "qualitative", "actual", MU_Q425, "our HBM share is on track to grow again and be in line with our overall DRAM share in this calendar Q3", "vendor=Micron; basis=unstated. Micron DRAM revenue share ~22-26% in 2025 (TrendForce/Counterpoint).")
S("hbm", "CXMT share of global HBM wafer supply", "2025", "1", "% of HBM wafers", "estimate", SEMI, "This would increase the company's share of global HBM wafer supply from 1% in 2025 to 12% in 2028.", "vendor=CXMT; basis=wafer; partly paywalled. Quote reused from hbm-gddr.csv.")
S("hbm", "Samsung TSV (HBM) capacity", "2026-12", "250", "k wafers/month", "forecast", BNK, "TSV 공정 Capa(k/월): 26년말 250k(1cnm 기반 HBM4만 130k) Vs. SK하이닉스 210k", "vendor=Samsung; basis=wafer; SK hynix 210k at end-2026 in same line.")
# vendor HBM mix (HBM share of own DRAM)
mq = "% ofDRAM 3.0 4.0 5.5 6.8 6.8 7.6 9.0 10.4 5.8 5.0 8.5 11.2"
for yr, val in (("2025", "5.0"), ("2026", "8.5"), ("2027", "11.2")):
    S("hbm", "Samsung HBM share of own DRAM bit shipments", yr, val, "% of vendor DRAM bits", "estimate" if yr == "2025" else "forecast", MIRAE, mq, "vendor=Samsung; basis=bit; HBM block, shipments row; annual columns 2024-2027.")
mq = "% of DRAM 10.6 12.8 15.8 15.4 12.5 13.6 17.0 21.3 17.1 14.1 16.4 24.0"
for yr, val in (("2025", "14.1"), ("2026", "16.4"), ("2027", "24.0")):
    S("hbm", "Samsung HBM share of own DRAM revenue", yr, val, "% of vendor DRAM revenue", "estimate" if yr == "2025" else "forecast", MIRAE, mq, "vendor=Samsung; basis=revenue.")
mq = "% ofDRAM 13.0 11.8 12.3 13.7 11.6 12.3 13.1 14.3 7.7 12.7 12.9 13.1"
for yr, val in (("2025", "12.7"), ("2026", "12.9"), ("2027", "13.1")):
    S("hbm", "SK hynix HBM share of own DRAM bit shipments", yr, val, "% of vendor DRAM bits", "estimate" if yr == "2025" else "forecast", MIRAE, mq, "vendor=SK hynix; basis=bit.")
mq = "% of DRAM 44.7 42.6 41.6 38.3 27.0 27.4 30.8 34.2 30.7 41.3 30.1 32.4"
for yr, val in (("2025", "41.3"), ("2026", "30.1"), ("2027", "32.4")):
    S("hbm", "SK hynix HBM share of own DRAM revenue", yr, val, "% of vendor DRAM revenue", "estimate" if yr == "2025" else "forecast", MIRAE, mq, "vendor=SK hynix; basis=revenue.")
lq = "HBM Bit Supply Ratio 1.9% 3.1% 5.3% 5.7% 5.6% 6.4% 7.0% 7.8% 4.0% 6.7%"
S("hbm", "Samsung HBM share of own DRAM bit supply", "2025", "4.0", "% of vendor DRAM bits", "estimate", LS, lq, "vendor=Samsung; basis=bit. Conflicts with Mirae 5.0%; keep both.")
S("hbm", "Samsung HBM share of own DRAM bit supply", "2026", "6.7", "% of vendor DRAM bits", "forecast", LS, lq, "vendor=Samsung; basis=bit. Mirae 8.5%.")
lq = "HBM Revenue Ratio 9.6% 14.7% 18.8% 13.7% 6.5% 8.1% 9.7% 11.7% 14.5% 9.0%"
S("hbm", "Samsung HBM share of own DRAM revenue", "2025", "14.5", "% of vendor DRAM revenue", "estimate", LS, lq, "vendor=Samsung; basis=revenue.")
S("hbm", "Samsung HBM share of own DRAM revenue", "2026", "9.0", "% of vendor DRAM revenue", "forecast", LS, lq, "vendor=Samsung; basis=revenue; low because conventional DRAM ASP rose ~3x in 2026 (LS table).")
S("hbm", "SK hynix HBM share of own DRAM sales volume", "4Q24-1Q25", "13-14", "% of vendor DRAM bits", "estimate", SKSEC, "당시 SK하이닉스의 HBM 비중은 판매 기준 13~14%, DRAM 내 매출액 기준 40% 초중반 수준이었다.", "vendor=SK hynix; basis=bit (판매 기준). Revenue basis low-to-mid 40s % in same sentence.")
S("hbm", "SK hynix HBM share of own DRAM revenue", "2025Q1", "44", "% of vendor DRAM revenue", "estimate", CP_SKH, "HBM contributed 14% of DRAM volume but accounted for 44% of revenue and an impressive 54% of DRAM operating profit", "vendor=SK hynix; basis=revenue (bit share 14% in same sentence).")
S("hbm", "SK hynix HBM revenue growth", "2025", ">100", "% YoY", "actual", SKH_Q425T, "HBM revenue more than doubled year-over-year, driven by a significant increase in HBM3E 12-Hi sales", "vendor=SK hynix; basis=revenue.")
S("hbm", "Samsung HBM sales growth", "2026", ">200", "% YoY", "forecast", SEC_Q425T, "we expect 2026 HBM sales to improve substantially, increasing by more than threefold year-on-year", "vendor=Samsung; basis=revenue (sales); 'more than threefold' = >+200%.")
S("hbm", "Samsung HBM4 share of own HBM sales", "2026Q3", "60", "% of vendor HBM sales", "actual", SEC_Q326T, "Also HBM4 mix increased to 60% of total HBM sales.", "vendor=Samsung; basis=revenue.")
S("hbm", "Micron HBM revenue", "FQ4-2025", "~2", "USD bn per quarter", "actual", MU_Q425, "In fiscal Q4, our HBM revenue grew to nearly $2 billion, implying an annualized run rate of nearly $8 billion", "vendor=Micron; basis=revenue.")
S("hbm", "Micron HBM share of own DRAM revenue", "FQ4-2025", "~22", "% of vendor DRAM revenue", "derived", MU_Q425, "Fiscal Q4 DRAM revenue was a record $9 billion, up 69% year-over-year and represented 79% of total revenue.", "vendor=Micron; basis=revenue; derived = ~2.0 / 9.0 = 22% (upper bound; 'nearly $2 billion').")
S("hbm", "SK hynix HBM proportion of bit shipments vs peers", "2026Q2", "highest of top 3", "qualitative", "estimate", TF_2Q26, "HBM accounted for the highest proportion of its total bit shipments among the top three suppliers", "vendor=SK hynix; basis=bit.")

# ================= SK hynix DRAM revenue by application (company slide; measured) =================
# Segment heights in PDF points from the vector bar chart; bar height = 361.6 pt = 100%.
skh = {  # period: (deck, PC, Server, Graphics incl HBM, Consumer, Mobile) in pt
    "2024Q4": ("2025Q4", 35.8, 121.8, 154.0, 7.2, 43.0),
    "2025Q2": ("2026Q2", 35.4, 112.0, 164.2, 6.4, 43.8),
    "2025Q3": ("2026Q3", 33.7, 118.8, 152.4, 7.3, 49.4),
    "2025Q4": ("2025Q4", 43.3, 130.3, 122.9, 10.9, 54.2),
    "2026Q1": ("2026Q2", 36.8, 172.4, 79.0, 14.0, 59.4),
    "2026Q2": ("2026Q3", 38.0, 176.3, 64.7, 18.5, 64.2),
    "2026Q3": ("2026Q3", 35.4, 201.7, 56.6, 19.2, 48.7),
}
segmap = (("pc", "PC", 1), ("server", "Server", 2), ("graphics-gddr", "Graphics (incl. HBM)", 3), ("all", "Consumer", 4), ("mobile-lpddr", "Mobile", 5))
for per, t in skh.items():
    tot = sum(t[1:])
    for seg, lab, i in segmap:
        S(seg, f"SK hynix {lab} share of own DRAM revenue", per, f"{100*t[i]/tot:.1f}", "% of vendor DRAM revenue", "derived", SKH_DECK[t[0]],
          f"Revenue by Application ... DRAM ... {lab}",
          f"vendor=SK hynix; basis=revenue; company chart without data labels; derived = segment height / bar height from PDF vector rectangles ({t[i]:.1f}/{tot:.1f} pt), +/-0.3 pt. Graphics bucket includes HBM (slide legend).")
S("server", "SK hynix server share of own DRAM revenue (secondary reading)", "2026Q3", "50-55", "% of vendor DRAM revenue", "estimate", INV_SKH, "server memory remained the largest segment at approximately 50-55% of DRAM revenue", "vendor=SK hynix; basis=revenue; secondary reading of the same chart; conflicts on mobile (says 20-25%; vector measure 13.5%). Prefer vector rows.")
S("mobile-lpddr", "SK hynix mobile share of own DRAM revenue (secondary reading)", "2026Q3", "20-25", "% of vendor DRAM revenue", "estimate", INV_SKH, "followed by mobile at 20-25%, graphics (including HBM) at 10-15%", "vendor=SK hynix; basis=revenue; conflicts with vector measure (13.5%).")
S("all", "SK hynix DRAM share of total revenue", "2026Q3", "75", "% of company revenue", "actual", SKH_DECK["2026Q3"], "Revenue by Product ... 75% ... 24%", "vendor=SK hynix; basis=revenue (KRW); NAND 24%. 2026Q2 73%, 2025Q3 78% on same slide.")
S("server", "SK hynix server DDR5 shipment growth", "2026Q3", ">40", "% QoQ", "actual", SKH_Q326T, "shipments of server DDR5 increased by over 40% compared to Q2, driving overall growth in DRAM bit shipments", "vendor=SK hynix; basis=bit.")

# ================= Server =================
S("server", "Samsung server share of own DRAM bits", "2026Q2", "~50", "% of vendor DRAM bits", "estimate", GS_YNA, "(search summary) 2026년 2분기 서버용 DRAM이 전체 DRAM 비트의 절반 가까이 됐을 것으로 추정", "vendor=Samsung; basis=bit; WEAK: Yonhap page could not be fetched; value seen only in a search-tool summary, not a verbatim article quote. Unclear whether HBM is included.")
S("server", "Samsung server share of own DRAM bit sales", "2026Q2", "all-time high", "qualitative", "actual", SEC_Q226T, "the bit sale portion of server application also reached an all-time high", "vendor=Samsung; basis=bit; no number disclosed.")
S("server", "Samsung server DRAM rank", "2025Q2", "1", "rank by server DRAM revenue", "estimate", TF_SRV, "Samsung led in market share, SK hynix had the largest revenue growth", "vendor=Samsung; basis=revenue; percentages paywalled (USD 25,000 report).")
mu_bu = [
    ("FQ4-2025", MU_Q425, (("CMBU", "4.5", "40", "Cloud Memory Business Unit revenue was $4.5 billion and represented 40% of total company revenue."),
                           ("CDBU", "1.6", "14", "Core Data Center Business Unit revenue was $1.6 billion and represented 14% of total company revenue."),
                           ("MCBU", "3.8", "33", "Mobile Client Business Unit revenue was $3.8 billion and represented 33% of total company revenue."),
                           ("AEBU", "1.4", "13", "Automotive and Embedded Business Unit revenue was $1.4 billion and represented 13% of total company revenue."))),
    ("FQ1-2026", MU_Q126, (("CMBU", "5.3", "39", "Cloud Memory Business Unit revenue was a record $5.3 billion and represented 39% of total company revenue."),
                           ("CDBU", "2.4", "17", "Core Data Center Business Unit revenue was a record $2.4 billion and represented 17% of total company revenue."),
                           ("MCBU", "4.3", "31", "Mobile and Client Business Unit revenue was a record $4.3 billion and represented 31% of total company revenue."),
                           ("AEBU", "1.7", "13", "Automotive and Embedded Business Unit revenue was a record $1.7 billion and represented 13% of total company revenue."))),
    ("FQ2-2026", MU_Q226, (("CMBU", "7.7", "32", "Cloud Memory Business Unit revenue was a record $7,700,000,000 and represented 32% of total company revenue."),
                           ("CDBU", "5.7", "24", "Core Data Center Business Unit revenue was a record $5,700,000,000 and represented 24% of total company revenue."),
                           ("MCBU", "7.7", "32", "Mobile and Client Business Unit revenue was a record $7,700,000,000 and represented 32% of total company revenue."),
                           ("AEBU", "2.7", "11", "Automotive and Embedded Business Unit revenue was a record $2,700,000,000 and represented 11% of total company revenue."))),
    ("FQ3-2026", MU_Q326, (("CMBU", "13.8", "33", "Cloud Memory Business Unit revenue was a record $13.8 billion and represented 33% of total company revenue."),
                           ("CDBU", "11.5", "28", "Core Data Center Business Unit revenue was a record $11.5 billion and represented 28% of total company revenue."),
                           ("MCBU", "11.5", "28", "Mobile and Client Business Unit revenue was a record $11.5 billion and represented 28% of total company revenue."),
                           ("AEBU", "4.6", "11", "Automotive and Embedded Business Unit revenue was a record $4.6 billion and represented 11% of total company revenue."))),
    ("FQ4-2026", MU_Q426, (("CMBU", "16.3", "30", "Cloud Memory Business Unit (CMBU) revenue was a record $16.3 billion and represented 30% of total"),
                           ("CDBU", "18.0", "33", "Core Data Center Business Unit (CDBU) revenue was a record $18.0 billion and represented 33% of total"),
                           ("MCBU", "13.1", "24", "Mobile and Client Business Unit (MCBU) revenue was a record $13.1 billion and represented 24% of total"),
                           ("AEBU", "6.8", "13", "Automotive and Embedded Business Unit (AEBU) revenue was a record $6.8 billion and represented 13%"))),
]
bu_seg = {"CMBU": "server", "CDBU": "server", "MCBU": "mobile-lpddr", "AEBU": "all"}
bu_note = {"CMBU": "hyperscale DRAM incl. HBM, LP server DRAM and data center SSD", "CDBU": "OEM/enterprise server DRAM and SSD",
           "MCBU": "mobile and client (PC) DRAM and NAND", "AEBU": "auto, industrial, embedded DRAM/NAND/NOR"}
for per, src, bus in mu_bu:
    for bu, usd, pct, quote in bus:
        S(bu_seg[bu], f"Micron {bu} share of company revenue", per, pct, "% of company revenue (DRAM+NAND)", "actual", src, quote,
          f"vendor=Micron; basis=revenue; BU = {bu_note[bu]}; includes NAND, so not a DRAM-only mix. BU revenue USD {usd} bn.")
for per, src, val, quote in (("FQ1-2026", MU_Q126, "79", "Fiscal Q1 DRAM revenue was a record $10.8 billion, up 69% year over year, and represented 79% of total revenue."),
                             ("FQ3-2026", MU_Q326, "76", "Fiscal Q3 DRAM revenue was a record $31.3 billion, up 343% year-over-year, and represented 76% of total revenue."),
                             ("FQ4-2026", MU_Q426, "73", "Fiscal Q4 DRAM revenue was a record $39.8 billion, up 343% year over year, and represented 73% of total")):
    S("all", "Micron DRAM share of company revenue", per, val, "% of company revenue", "actual", src, quote, "vendor=Micron; basis=revenue.")
S("server", "Micron data-center DRAM share of own DRAM revenue", "FQ4-2026", "~61", "% of vendor DRAM revenue", "derived", MU_Q426,
  "Data center SSD revenue in fiscal Q4 was nearly $10 billion, more than 10 times the year-ago quarter",
  "vendor=Micron; basis=revenue; derived = (CMBU 16.3 + CDBU 18.0 - DC SSD ~10) / DRAM 39.8 = 61%. Includes HBM and LP server DRAM. Approximate ('nearly $10 billion').")
S("server", "Micron data-center DRAM share of own DRAM revenue", "FQ3-2026", "~65", "% of vendor DRAM revenue", "derived", MU_Q326,
  "Our data center SSD revenue exceeded $5 billion, more than doubling sequentially.",
  "vendor=Micron; basis=revenue; derived = (CMBU 13.8 + CDBU 11.5 - DC SSD >5) / DRAM 31.3 <= 65%. Includes HBM and LP server.")
S("server", "Micron data-center DRAM share of own DRAM revenue", "FQ1-2026", "~62", "% of vendor DRAM revenue", "derived", MU_Q126,
  "Our data center NAND portfolio revenue exceeded $1 billion in fiscal Q1",
  "vendor=Micron; basis=revenue; derived = (CMBU 5.3 + CDBU 2.4 - DC NAND >1.0) / DRAM 10.8 <= 62%.")
S("server", "Micron data center share of company revenue", "FY2025", "56", "% of company revenue", "actual", MU_Q425,
  "Micron 's data center business reached a record 56% of total company revenue, with gross margins of 52%", "vendor=Micron; basis=revenue; DRAM+NAND.")
S("server", "Micron HBM + high-capacity DIMM + LP server DRAM revenue", "FY2025", "10", "USD bn", "actual", MU_Q425,
  "The combined revenue from HBM, high-capacity DIMMs, and LP server DRAM reached $10 billion", "vendor=Micron; basis=revenue; FY2025 total revenue USD 37.38 bn, so ~27% of company revenue (derived).")
S("server", "Nanya AI infrastructure share of revenue", "2026Q3", ">20", "% of company revenue", "actual", NANYA_IR,
  "本公司AI基礎設施(含伺服器、網路、儲存及系統管理)占營收超過20%", "vendor=Nanya; basis=revenue; includes networking, storage, system management, not server DRAM only. Target 40-50% by 2029-2030 (AlphaMemo summary).")

# ================= LPDDR server / SOCAMM2 =================
kq = "삼성전자 35% 17.5 33.6 ... SK 하이닉스 40% 19.9 38.4 ... Micron 25% 12.5 24.0"
for v, val in (("Samsung", "35"), ("SK hynix", "40"), ("Micron", "25")):
    S("lpddr-server", f"{v} SOCAMM2 share", "2026-2027", val, "% of SoCAMM2 market", "forecast", KIS, kq,
      f"vendor={v}; basis=unstated (used to split module-PCB revenue); same share applied to 2026 and 2027.")
bq = "SOCAMM2 밴더: 삼성 50%, SK하이닉스 30%, 마이크론 20% 점유 예상"
for v, val in (("Samsung", "50"), ("SK hynix", "30"), ("Micron", "20")):
    S("lpddr-server", f"{v} SOCAMM2 share", "2026", val, "% of SOCAMM2 supply", "forecast", BNK, bq, f"vendor={v}; basis=unstated (Nvidia SOCAMM2 supply).")
S("lpddr-server", "Samsung SOCAMM2 share of Nvidia demand", "2026", "50", "% of Nvidia SOCAMM2 demand", "estimate", KB_JA,
  "which accounts for about 50 percent of Nvidia's Socamm2 demand", "vendor=Samsung; basis=bit (10 billion Gb). 'SK hynix has secured more orders than Micron.' Already in lpddr.csv.")
S("lpddr-server", "Samsung share of Nvidia AI-CPU DRAM", "2026", "low-to-mid 40s", "% of Nvidia AI-CPU DRAM bits", "forecast", DAISHIN,
  "삼성전자가 40% 초중반, SK하이닉스와 Micron Technology가 20% 후반의 점유율을 차지할 것이라는 판단이다.",
  "vendor=Samsung; basis=bit; TAM ~23 bn Gb in 2026 (Grace + Vera CPU DRAM, '230억 Gb 내외'). SK hynix and Micron each high-20s %.")
S("lpddr-server", "Micron share of data center LPDRAM", "FY2025", "sole supplier", "qualitative", "actual", MU_Q425,
  "Micron has been the sole supplier of LPDRAM in the data center", "vendor=Micron; basis=unstated; implies ~100% of 2025 server LPDDR. Also: LPDDR5 for servers >50% QoQ growth in FQ4-25.")

# ================= Mobile / LPDDR =================
S("mobile-lpddr", "Samsung mobile DRAM market share", "2024Q1", "57.9", "% of mobile DRAM market", "estimate", KT_MOB,
  "According to market tracker Omdia, Samsung Electronics claimed 57.9 percent of the global mobile DRAM market", "vendor=Samsung; basis=revenue (Omdia, assumed). 54.8% in 2023 in same sentence.")
S("mobile-lpddr", "Samsung mobile DRAM market share", "2023", "54.8", "% of mobile DRAM market", "estimate", KT_MOB,
  "which includes LPDDR, in the first quarter of last year, up from 54.8 percent in 2023.", "vendor=Samsung; basis=revenue (Omdia, assumed).")
S("mobile-lpddr", "Mobile DRAM supplier structure", "2025Q4", "Big Four: Samsung, SK hynix, Micron, CXMT", "qualitative", "estimate", TF_MOB,
  "a highly concentrated 'Big Four' landscape", "vendor=all; basis=revenue; shares paywalled (USD 18,000). CXMT 'revenue share has steadily climbed'; Nanya and Winbond 'overall market share remains limited'. 2Q25 report: Samsung 1st, SK hynix 2nd.")
cq = "LPDDR 系列 1,061,681.86 69.74% 1,979,825.86 82.74% 675,607.25 74.54% 641,662.23 79.37%"
for per, val in (("2022", "79.37"), ("2023", "74.54"), ("2024", "82.74"), ("2025H1", "69.74")):
    S("mobile-lpddr", "CXMT LPDDR series share of main-business revenue", per, val, "% of vendor main-business revenue", "actual", CXMT_SB, cq,
      "vendor=CXMT; basis=revenue; LPDDR4X + LPDDR5/5X; mostly phones and tablets (prospectus).")
S("mobile-lpddr", "CXMT LPDDR series share of main-business revenue", "2025", "66.43", "% of vendor main-business revenue", "actual", CXMT_REG,
  "LPDDR 4,070,354.50 66.43%", "vendor=CXMT; basis=revenue; page text mis-encoded (GBK); numbers legible; row label inferred as LPDDR系列. Amount in 10k CNY.")

# ================= Graphics / GDDR =================
S("graphics-gddr", "Samsung GDDR7 market share", "2025", "70", "% of GDDR7 market", "estimate", HK_GDDR,
  "3일 시장조사업체 트렌드포스에 따르면 삼성전자의 올해 GDDR7 점유율은 70%로 추산됐다.", "vendor=Samsung; basis=unstated; TrendForce via Hankyung. GDDR7 only.")
S("graphics-gddr", "Samsung GDDR market share", "2024", "41", "% of GDDR market", "estimate", HK_GDDR,
  "지난해 전체 GDDR 시장에서 삼성전자는 점유율 41%로 SK하이닉스(49%)에 밀렸지만", "vendor=Samsung; basis=unstated; source of 41/49 not named in article.")
S("graphics-gddr", "SK hynix GDDR market share", "2024", "49", "% of GDDR market", "estimate", HK_GDDR,
  "지난해 전체 GDDR 시장에서 삼성전자는 점유율 41%로 SK하이닉스(49%)에 밀렸지만", "vendor=SK hynix; basis=unstated.")
S("graphics-gddr", "Micron GDDR market share", "2024", "~10", "% of GDDR market", "derived", HK_GDDR,
  "지난해 전체 GDDR 시장에서 삼성전자는 점유율 41%로 SK하이닉스(49%)에 밀렸지만", "vendor=Micron; basis=unstated; derived = 100 - 41 - 49 = 10 (assumes three suppliers).")

# ================= DDR4 / legacy =================
cq = "DDR 系列 423,548.37 27.82% 317,397.33 13.26% 182,716.69 20.16% 147,481.67 18.24%"
for per, val in (("2023", "20.16"), ("2024", "13.26"), ("2025H1", "27.82")):
    S("ddr4-legacy", "CXMT DDR series (DDR4+DDR5) share of main-business revenue", per, val, "% of vendor main-business revenue", "actual", CXMT_SB, cq,
      "vendor=CXMT; basis=revenue; DDR series = DDR4 + DDR5 (DDR5 mass production end-2024, ramp 2025); serves PC, server, consumer.")
S("ddr4-legacy", "CXMT DDR series (DDR4+DDR5) share of main-business revenue", "2025", "31.87", "% of vendor main-business revenue", "actual", CXMT_REG,
  "DDR 1,953,128.56 31.87%", "vendor=CXMT; basis=revenue; rise driven by DDR5 ('2024 年底，公司 DDR5 产品量产，并于 2025 年开始迅速放量').")
S("ddr4-legacy", "Industry DDR4 share of DDR market", "2024", "45", "% of DDR market", "estimate", CXMT_SB,
  "2024 年 DDR4 和 DDR5 产品在 DDR 产品领域市场占有率分别达到 45%和 52%", "vendor=industry; basis=unstated (Omdia-sourced section). LPDDR4 46% / LPDDR5 53% of LPDDR in 2024, same page.")
S("all", "CXMT global DRAM market share", "2025Q2", "3.97", "% of DRAM revenue", "estimate", CXMT_SB,
  "按2025 年第二季度 DRAM 销售额统计， 长鑫科技的全球市场份额已增至3.97%", "vendor=CXMT; basis=revenue (Omdia). Omdia 2024: Samsung 40.35, SK hynix 33.19, Micron 20.73 (same page).")
S("ddr4-legacy", "Nanya DDR5 share of revenue", "2026Q3", "~10", "% of vendor revenue", "actual", NANYA_FT,
  "DDR5 products account for about 10 percent of revenue", "vendor=Nanya; basis=revenue; can rise to 40% if needed (Nextapple).")
S("ddr4-legacy", "Nanya DDR4 + LPDDR4 share of revenue", "2026Q3", ">60", "% of vendor revenue", "actual", NANYA_AM,
  "Q3 產品組合：DDR5 約佔 10%，DDR4 與低功耗 DDR4 合計超過 60%，DDR3 未計入此數字。", "vendor=Nanya; basis=revenue (assumed); AI-generated call summary; DDR3 excluded from the figure.")
S("ddr4-legacy", "Nanya revenue growth on DDR4/DDR3 prices", "2026Q2", "68.3", "% QoQ", "actual", TF_2Q26,
  "Significant increases in DDR4 and DDR3 contract prices drove Nanya's revenue up 68.3% QoQ to $2.612 billion.", "vendor=Nanya; basis=revenue; Winbond +75.8% QoQ to $998M; PSMC DRAM $115M (consumer DRAM).")
S("ddr4-legacy", "Samsung / Micron / SK hynix DDR4 end of shipments", "2025-12 / 2026Q1 / 2026-04", "EOL", "event", "forecast", TF_DDR4,
  "Samsung, SK hynix, and Micron are set to end DDR4 shipments between late 2025 and early 2026.", "vendor=Samsung, Micron, SK hynix; basis=n/a; Samsung mid-Dec 2025, Micron Q1 2026, SK hynix April 2026; some schedules later delayed.")

# ================= All-DRAM context =================
S("all", "Samsung DRAM market share target", "2027", ">40", "% of DRAM market", "forecast", EDAILY,
  "SamsungElectronics' DRAM market share will exceed 40% next year.", "vendor=Samsung; basis=revenue (TrendForce context: 38.5% in 1Q26).")

w = csv.writer(open(sys.argv[1], "w", newline=""))
w.writerow(H)
for row in rows:
    w.writerow(row)
print(len(rows), "rows")
