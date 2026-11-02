# openanalysis

Open research reports. Each report ships with its sources, model and build scripts, so every number can be traced to a cited row and the analysis can be rerun.

## Reports

| Report | Published | Topic | PDF |
|---|---|---|---|
| [The Memory Squeeze](reports/memory-squeeze-2026-2027/) | October 2026 | DRAM supply and shortage forecast, 2026–2027 | [PDF](reports/memory-squeeze-2026-2027/report/dram-shortage-2026-2027.pdf) |

## Layout

Each report lives in its own folder under `reports/`:

```
reports/<report-slug>/
  README.md     summary, key findings, how to rebuild
  report/       the finished report (PDF, HTML) and the scripts that build it
  model/        the model code and METHOD.md, which explains the method and assumptions
  sources/      cited source data (CSV) with a notes file for each dataset
  out/          model outputs: tables, charts, checks
  tools/        scripts that turn raw downloads into the source CSVs
```

Raw third-party downloads (broker research, filings, slide decks) are not redistributed. The source CSVs and notes keep the URL, title, date and quote for each figure.

## Adding a report

1. Create `reports/<report-slug>/` with the layout above and a README.
2. Add a row to the table above.
