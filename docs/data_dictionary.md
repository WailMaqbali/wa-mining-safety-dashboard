# Data dictionary

All figures are transcribed from WorkSafe WA (Department of Energy, Mines, Industry Regulation and Safety) publications:

- *Safety performance in the WA mineral industry 2023-24* (annual report)
- *Quarterly performance snapshot* for the WA minerals sector, nine quarters from 1 April 2022 to 30 June 2024 (1 April - 30 June 2023 not yet added)

Every row carries a `source` and `page` so any value can be checked against the PDF. `scripts/build_data.py` regenerates every file and runs a reconciliation (sums, rate recalculation from counts and hours) before writing.

## Terms

| Term | Meaning |
|---|---|
| LTI | Lost time injury |
| RWI | Restricted work injury |
| LTIFR / RWIFR | LTIs / RWIs per million hours worked |
| Frequency (quarterly snapshots) | LTIs + RWIs combined, per million hours |
| FIFR | Fatal injury frequency rate, per million hours |
| Duration rate | Average days lost (or restricted) per injury |
| Injury index | Duration rate x frequency rate |

## Files

### `quarterly_summary.csv` (9 rows, one per quarter)
| Column | Description |
|---|---|
| fiscal_year, fy_quarter | WA financial year and quarter (Q4 = Apr-Jun) |
| quarter_start, quarter_end | Dates |
| fatalities, ltis, rwis, total_injuries | Counts as first reported; total = LTIs + RWIs |
| injury_rate_first_reported | Combined frequency in that quarter's own snapshot |
| injury_rate_revised | Same quarter's rate as quoted in a later snapshot |
| revised_from | Snapshot the revised figure came from |
| snapshot_issued | Month the snapshot was published |
| source, notes | Provenance and caveats |

### `quarterly_commodity.csv` (40 rows)
Top five commodities by hours in each quarter: `hours_millions` and combined `injury_frequency`.

### `annual_commodity_2023_24.csv` (13 rows)
Annual Tables 2.1-2.3: hours, LTIs, RWIs, rates, days lost/restricted, duration rates and injury indices by commodity. `small_sample` = 1 where counts are too low for rates to be meaningful.

### `annual_regions_2023_24.csv` (11 rows)
Appendices 6-10: hours and rates by region. `ltis_implied` and `rwis_implied` are derived (rate x hours), not published.

### `fatalities.csv` (33 rows)
Fatalities by year, commodity and incident type, with `of_which_exploration`.

## Caveats
1. **Quarterly totals do not equal annual totals.** The four 2023-24 quarters sum to 512 LTIs and 917 RWIs; the annual report (mining) has 569 and 942. Quarterlies are first-reported and are later revised for late returns. Use annual figures for headlines and quarterlies for trend only.
2. **First-reported vs revised rates are separate columns.** Revisions to date: Jul-Sep 2023 4.6 to 4.8, Oct-Dec 2023 4.9 to 5.3, Jan-Mar 2024 6.1 to 6.4. The latest quarter (Apr-Jun 2024, 5.6) has not been revised and is likely understated.
3. **Missing quarter.** 1 April - 30 June 2023 is blank in `quarterly_summary.csv` apart from the revised rate (5.4) quoted in the Jul-Sep 2023 snapshot.
4. **Regions are mining only** (269.7 M hours) while commodity and summary tables include exploration (278.0 M hours).
5. **Fatality breakdowns by year and incident type were read from chart bars** (integers). They reconcile to the published total of 23, with 2 in exploration.
6. **Comparability:** the WHS Act commenced 31 March 2022, so only Apr-Jun 2022 onwards is comparable.
7. **Small samples:** commodities and regions with few injuries are flagged; avoid ranking on their rates.

## Spot-check list
Open the PDFs and confirm these against the data:
- Annual report p.4: fatality charts (10-year total 23)
- Annual report pp.8-11: iron ore 125.7 M hours, 322 LTIs, 411 RWIs
- Jan-Mar 2024 snapshot: 149 LTIs, 259 RWIs, rate 6.1
- Oct-Dec 2022 snapshot: 2 fatalities, 131 LTIs, 212 RWIs
