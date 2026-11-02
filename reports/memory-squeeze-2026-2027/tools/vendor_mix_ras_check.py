# Sanity check for the vendor x type prior in sources/vendor-mix-notes.md.
# Rows: Mirae vendor bit production scaled to the model total (others = Mirae residual).
# Columns: out/forecast_by_category.csv medians. Prior: % of each vendor's own bits.
# Prints the prior-implied column sums, then the RAS-fitted matrix (billion Gb) and fitted vendor mix (%).
import csv, sys

cols = ["server_ecc", "lpddr", "client_pc", "hbm", "gddr", "other_consumer"]
vendors = ["Samsung", "SK hynix", "Micron", "CXMT", "Nanya+others"]
mirae = {  # billion Gb: Samsung, SK hynix, Micron, CXMT, Nanya, industry total
    2025: (111.1, 84.7, 55.8, 23.3, 4.0, 293.1),
    2026: (122.0, 105.2, 63.7, 29.5, 4.3, 352.5),
    2027: (143.2, 125.1, 74.5, 36.0, 4.8, 415.7),
}
prior = {  # % of own bits: server, LPDDR, PC, HBM, GDDR, other
    2025: [(39, 46, 5, 4.5, 4.5, 1), (46, 26, 8, 14.5, 3, 2.5), (34, 42, 7, 8, 2, 7),
           (8, 66, 14, 0, 0, 12), (15, 30, 10, 0, 0, 45)],
    2026: [(44, 38, 3.5, 8, 4, 2.5), (50, 22, 7, 15.5, 2.5, 3), (40, 36, 5, 10, 1, 8),
           (15, 60, 13, 1, 0, 11), (25, 35, 15, 0, 0, 25)],
    2027: [(42, 36, 3, 14, 3.5, 1.5), (47, 25, 6, 16, 2.5, 3.5), (38, 37, 5, 13, 1, 6),
           (18, 55, 12, 4, 0, 11), (25, 35, 15, 0, 0, 25)],
}

def col_totals(path, year):
    t = {}
    lp = 0.0
    for r in csv.DictReader(open(path)):
        if int(r["year"]) != year:
            continue
        if r["category"] in cols:
            t[r["category"]] = float(r["median_bn_gb"])
        if r["category"] == "total":
            t["total"] = float(r["median_bn_gb"])
        if r["category"].startswith("lpddr_"):
            lp += float(r["median_bn_gb"])
    t.setdefault("lpddr", lp)
    return t

def ras(m, rows, colsum, it=500):
    m = [r[:] for r in m]
    for _ in range(it):
        for i, r in enumerate(m):
            s = sum(r); m[i] = [x * rows[i] / s for x in r] if s else r
        for j in range(len(colsum)):
            s = sum(m[i][j] for i in range(len(m)))
            if s:
                for i in range(len(m)):
                    m[i][j] *= colsum[j] / s
    return m

path = sys.argv[1]
for y in (2025, 2026, 2027):
    t = col_totals(path, y)
    s, k, mu, c, n, ind = mirae[y]
    f = t["total"] / ind
    rows = [s * f, k * f, mu * f, c * f, (ind - s - k - mu - c + n) * f]
    colsum = [t[c_] for c_ in cols]
    m0 = [[rows[i] * p / 100 for p in prior[y][i]] for i in range(5)]
    print(f"\n== {y}  model total {t['total']:.1f}  scale {f:.3f}")
    print("column      target  prior-implied")
    for j, c_ in enumerate(cols):
        print(f"{c_:14s} {colsum[j]:7.1f} {sum(m0[i][j] for i in range(5)):7.1f}")
    m = ras(m0, rows, colsum)
    print("fitted bn Gb / fitted % of own bits / share of column")
    for i, v in enumerate(vendors):
        print(f"{v:13s} " + " ".join(f"{x:6.1f}" for x in m[i]) + " | " +
              " ".join(f"{100*x/rows[i]:5.1f}" for x in m[i]) + " | " +
              " ".join(f"{100*m[i][j]/colsum[j]:5.1f}" for j in range(6)))
