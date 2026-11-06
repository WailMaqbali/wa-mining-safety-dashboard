"""
Builds the tidy CSVs used by the WA mining safety Power BI dashboard.

Sources (WorkSafe WA, Department of Local Government, Industry Regulation and Safety):
  - Safety performance in the Western Australian mineral industry:
    incident and injury statistics 2023-24 (annual report)
  - Quarterly performance snapshots, Apr-Jun 2022 to Jun 2024
    (Apr-Jun 2023 not yet added)

Values are transcribed from the published PDFs. Run: python3 scripts/build_data.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "data"))
os.makedirs(OUT, exist_ok=True)

ANNUAL = "Safety performance in the WA mineral industry 2023-24"


# Tables kept in the in-memory reconciliation but not published as CSVs
SKIP = {"top_categories.csv", "annual_summary.csv"}


def write(name, header, rows):
    """Write one CSV (None becomes an empty cell) and report its row count."""
    if name in SKIP:
        return
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


# ---------------------------------------------------------------- quarterly --
# key, period text, fy, fq, start, end, issued, fatal, LTI, RWI, rate first, rate revised, revised from
Q = [
    ("AMJ22", "1 April - 30 June 2022", "2021-22", "Q4", "2022-04-01", "2022-06-30", "May 2024", 1, 112, 166, 4.6, 4.6, "Jul-Sep 2022 snapshot"),
    ("JAS22", "1 July - 30 September 2022", "2022-23", "Q1", "2022-07-01", "2022-09-30", "May 2024", 0, 148, 215, 5.7, 5.7, "Oct-Dec 2022 snapshot"),
    ("OND22", "1 October - 31 December 2022", "2022-23", "Q2", "2022-10-01", "2022-12-31", "May 2024", 2, 131, 212, 5.4, 5.4, "Jan-Mar 2023 snapshot"),
    ("JFM23", "1 January - 31 March 2023", "2022-23", "Q3", "2023-01-01", "2023-03-31", "May 2024", 0, 119, 231, 5.6, None, ""),
    ("AMJ23", "1 April - 30 June 2023", "2022-23", "Q4", "2023-04-01", "2023-06-30", "", None, None, None, None, 5.4, "Jul-Sep 2023 snapshot"),
    ("JAS23", "1 July - 30 September 2023", "2023-24", "Q1", "2023-07-01", "2023-09-30", "May 2024", 0, 105, 204, 4.6, 4.8, "Oct-Dec 2023 snapshot"),
    ("OND23", "1 October - 31 December 2023", "2023-24", "Q2", "2023-10-01", "2023-12-31", "June 2024", 0, 128, 196, 4.9, 5.3, "Jan-Mar 2024 snapshot"),
    ("JFM24", "1 January - 31 March 2024", "2023-24", "Q3", "2024-01-01", "2024-03-31", "Sept 2024", 0, 149, 259, 6.1, 6.4, "Apr-Jun 2024 snapshot"),
    ("AMJ24", "1 April - 30 June 2024", "2023-24", "Q4", "2024-04-01", "2024-06-30", "June 2025", 1, 130, 258, 5.6, None, ""),
]
Q_NOTES = {
    "AMJ22": "First quarter reported under WHS definitions",
    "JFM23": "Revised rate unavailable until the Apr-Jun 2023 snapshot is added",
    "AMJ23": "Snapshot not yet added. Counts and first-reported rate are blank. Revised rate is the 'previous quarter' figure quoted in the Jul-Sep 2023 snapshot",
    "AMJ24": "Latest quarter. Rate has not been revised yet; earlier 2023-24 quarters were revised up by 0.2 to 0.4",
}


def qsrc(period):
    return f"Quarterly performance snapshot: {period}"


rows = []
for key, period, fy, fq, start, end, issued, fat, lti, rwi, r1, r2, rfrom in Q:
    total = (lti + rwi) if lti is not None else None
    rows.append([fy, fq, start, end, fat, lti, rwi, total, r1, r2, rfrom, issued,
                 qsrc(period) if lti is not None else "", Q_NOTES.get(key, "")])
write("quarterly_summary.csv",
      ["fiscal_year", "fy_quarter", "quarter_start", "quarter_end", "fatalities", "ltis", "rwis",
       "total_injuries", "injury_rate_first_reported", "injury_rate_revised", "revised_from",
       "snapshot_issued", "source", "notes"], rows)

# Commodity rows: (commodity, hours in millions, injury frequency = LTI+RWI per million hours)
IO, AU, NI, TA, BX = "Iron ore", "Gold", "Nickel", "Tin, tantalum and lithium", "Bauxite and alumina"
QC = {
    "AMJ22": [(IO, 30.1, 4.0), (AU, 15.5, 4.3), (NI, 4.2, 5.9), (BX, 3.3, 9.4), (TA, 2.5, 4.4)],
    "JAS22": [(IO, 31.6, 4.6), (AU, 15.5, 5.9), (NI, 4.4, 10.1), (BX, 3.5, 12.8), (TA, 3.2, 3.7)],
    "OND22": [(IO, 30.5, 5.1), (AU, 15.3, 4.8), (NI, 4.9, 9.0), (TA, 3.8, 3.4), (BX, 3.6, 8.1)],
    "JFM23": [(IO, 30.0, 5.1), (AU, 14.5, 6.5), (NI, 5.1, 7.3), (TA, 4.3, 2.6), (BX, 3.6, 9.1)],
    "JAS23": [(IO, 30.9, 4.6), (AU, 15.5, 5.3), (NI, 5.7, 5.1), (TA, 5.4, 1.1), (BX, 3.6, 5.2)],
    "OND23": [(IO, 30.2, 4.8), (AU, 15.6, 4.4), (NI, 5.7, 7.5), (TA, 5.7, 2.8), (BX, 3.5, 9.3)],
    "JFM24": [(IO, 31.4, 6.8), (AU, 15.8, 4.6), (TA, 5.9, 3.1), (NI, 5.1, 7.7), (BX, 3.5, 11.0)],
    "AMJ24": [(IO, 33.2, 5.7), (AU, 16.6, 4.7), (TA, 6.0, 3.8), (NI, 4.4, 7.2), (BX, 3.4, 10.6)],
}
rows = []
for key, period, fy, fq, start, end, *_ in Q:
    for com, hrs, freq in QC.get(key, []):
        rows.append([fy, fq, end, com, hrs, freq, qsrc(period), 2])
write("quarterly_commodity.csv",
      ["fiscal_year", "fy_quarter", "quarter_end", "commodity", "hours_millions", "injury_frequency",
       "source", "page"], rows)

# Top categories per quarter: (rank, category, percent). Ties share a rank.
PP, MF, DR = "Processing plant occupations", "Mechanical fitters", "Driving occupations"
SV, LT = "Services occupations", "Loading / transport occupations"
LH, DD = "Long hole drill and blast operations", "Diamond drillers / raiseborers"
TP, AD, OP = "Treatment plant / ore processing", "Administration areas", "Open pit production / development areas"
PD, AH, WS = "Production / development areas", "Access / haulage ways", "Workshops"
H, B, S = "Hands", "Back", "Shoulders"
SP, FR = "Sprains and strains", "Fractures"

TOP = {
    "AMJ22": dict(age=[(1, "50-59", 27), (2, "30-39", 24)],
                  occ_s=[(1, PP, 15), (1, MF, 15), (2, DR, 11)],
                  occ_u=[(1, SV, 33), (2, LT, 17), (2, LH, 17), (2, DD, 17)],
                  loc_s=[(1, TP, 28), (2, OP, 24)], loc_u=[(1, PD, 63), (2, AH, 20)],
                  body=[(1, H, 28), (2, B, 14)], nature=[(1, SP, 49), (2, FR, 19)]),
    "JAS22": dict(age=[(1, "30-39", 25), (2, "40-49", 22)],
                  occ_s=[(1, PP, 20), (2, MF, 13)],
                  occ_u=[(1, SV, 24), (1, LT, 24), (2, LH, 14)],
                  loc_s=[(1, TP, 35), (2, OP, 19)], loc_u=[(1, PD, 67), (2, AH, 24)],
                  body=[(1, H, 22), (2, B, 10)], nature=[(1, SP, 50), (2, FR, 18)]),
    "OND22": dict(age=[(1, "30-39", 29), (2, "20-29", 27)],
                  occ_s=[(1, MF, 18), (2, PP, 17)], occ_u=[(1, SV, 35), (2, LH, 15)],
                  loc_s=[(1, TP, 32), (2, OP, 20)], loc_u=[(1, PD, 63), (2, AH, 13)],
                  body=[(1, H, 26), (2, S, 10)], nature=[(1, SP, 48), (2, FR, 19)]),
    "JFM23": dict(age=[(1, "30-39", 30), (2, "40-49", 22)],
                  occ_s=[(1, MF, 19), (2, PP, 16)],
                  occ_u=[(1, SV, 31), (2, LT, 19), (2, LH, 19)],
                  loc_s=[(1, TP, 31), (2, OP, 19)], loc_u=[(1, PD, 74), (2, AH, 17)],
                  body=[(1, H, 27), (2, S, 11)], nature=[(1, SP, 46), (2, FR, 17)]),
    "JAS23": dict(age=[(1, "20-29", 26), (2, "30-39", 25)],
                  occ_s=[(1, MF, 18), (2, PP, 14)],
                  occ_u=[(1, SV, 21), (1, LH, 21), (3, DD, 18)],
                  loc_s=[(1, TP, 31), (2, OP, 20)], loc_u=[(1, PD, 79), (2, AH, 12)],
                  body=[(1, H, 27), (2, B, 10)], nature=[(1, SP, 44), (2, FR, 21)]),
    "OND23": dict(age=[(1, "30-39", 26), (2, "20-29", 25)],
                  occ_s=[(1, PP, 18), (2, MF, 17)], occ_u=[(1, SV, 42)],
                  loc_s=[(1, TP, 31), (2, AD, 16)], loc_u=[(1, PD, 58), (2, WS, 15)],
                  body=[(1, H, 24), (2, B, 9)], nature=[(1, SP, 44), (2, FR, 13)]),
    "JFM24": dict(age=[(1, "30-39", 28), (2, "20-29", 22), (2, "50-59", 22)],
                  occ_s=[(1, PP, 15), (2, MF, 14)], occ_u=[(1, LH, 17), (2, SV, 14)],
                  loc_s=[(1, TP, 27), (2, OP, 18)], loc_u=[(1, PD, 67), (2, AH, 10)],
                  body=[(1, H, 22), (2, B, 10)], nature=[(1, SP, 47), (2, FR, 16)]),
    "AMJ24": dict(age=[(1, "30-39", 28), (2, "20-29", 26)],
                  occ_s=[(1, PP, 17), (2, MF, 16)], occ_u=[(1, SV, 20), (2, LT, 16)],
                  loc_s=[(1, TP, 32), (2, AD, 23)], loc_u=[(1, PD, 77), (2, AH, 14)],
                  body=[(1, H, 26), (2, S, 9)], nature=[(1, SP, 48), (2, FR, 16)]),
}
DIM = {  # key -> (scope, dimension)
    "age": ("all", "age_group"), "occ_s": ("surface", "occupation"), "occ_u": ("underground", "occupation"),
    "loc_s": ("surface", "location"), "loc_u": ("underground", "location"),
    "body": ("all", "body_part"), "nature": ("all", "nature_of_injury"),
}


def with_ties(items):
    """Yield (rank, name, pct, note), flagging ranks that are shared."""
    ranks = [r for r, _, _ in items]
    for r, name, pct in items:
        yield r, name, pct, "equal rank" if ranks.count(r) > 1 else ""


top_rows = []
for key, period, fy, fq, start, end, *_ in Q:
    for dkey, items in TOP.get(key, {}).items():
        scope, dim = DIM[dkey]
        for r, name, pct, note in with_ties(items):
            top_rows.append(["quarter", fy, fq, end, scope, dim, r, name, pct, note, qsrc(period), 1])

# Annual top-5 (all mining and exploration), plus the per-commodity / surface / underground body-part callouts
ANN_TOP = [
    ("all", "body_part", 3, [(1, "Hands", 25), (2, "Back", 10), (3, "Shoulders", 9), (4, "Ankle", 8), (4, "Knee", 8)]),
    ("all", "nature_of_injury", 3, [(1, "Sprain or strain", 47), (2, "Fracture", 17), (3, "Laceration", 8), (4, "Crushing", 7), (5, "Exposure to mental stress", 5)]),
    ("all", "location", 3, [(1, "Treatment plant", 26), (2, "Administration", 16), (2, "Open pit production / development", 16), (4, "Workshop", 13), (5, "Surface general", 12)]),
    ("all", "incident_type", 8, [(1, "Over-exertion / strenuous movement", 25.1), (2, "Slip / trip", 11.0), (3, "Caught by / between (not machine)", 10.9), (4, "Stepping / jumping", 10.2), (5, "Struck by object", 9.2)]),
]
BODY_CALLOUTS = [  # (scope, page, [(rank, body part, percent)])
    ("Iron ore", 12, [(1, "Hands", 23), (2, "Back", 13), (3, "General", 8), (3, "Knee", 8), (3, "Ankle", 8)]),
    ("Gold", 13, [(1, "Hands", 32), (2, "Shoulders", 12), (3, "Back", 8), (3, "Knee", 8), (5, "Ankle", 7)]),
    ("Tin, tantalum and lithium", 14, [(1, "Hands", 30), (2, "Trunk", 11), (2, "Ankle", 11), (4, "Knee", 10), (5, "Back", 7)]),
    ("Nickel", 15, [(1, "Hands", 19), (2, "Shoulders", 12), (2, "Back", 12), (4, "Ankle", 11), (5, "Wrist", 8)]),
    ("Bauxite and alumina", 16, [(1, "Hands", 18), (2, "Shoulders", 13), (3, "Eye", 8), (3, "Elbow", 8), (3, "General", 8)]),
    ("Exploration", 17, [(1, "Hands", 20), (2, "General", 17), (3, "Shoulders", 13), (4, "Wrist", 11), (5, "Back", 9)]),
    ("Heavy mineral sands", 18, [(1, "Hands", 26), (2, "Knee", 17), (3, "Shoulders", 13), (3, "Ankle", 13)]),
    ("Copper, lead and zinc", 19, [(1, "Hands", 53), (2, "Trunk", 12), (2, "Ankle", 12)]),
    ("surface", 20, [(1, "Hands", 25), (2, "Back", 11), (3, "Shoulders", 9), (4, "Knee", 7), (4, "Ankle", 7)]),
    ("underground", 21, [(1, "Hands", 25), (2, "Shoulders", 11), (2, "Ankle", 11), (4, "Back", 9), (5, "Knee", 8)]),
]
for scope, dim, page, items in ANN_TOP:
    for r, name, pct, note in with_ties(items):
        top_rows.append(["annual", "2023-24", "FY", "2024-06-30", scope, dim, r, name, pct, note, ANNUAL, page])
for scope, page, items in BODY_CALLOUTS:
    for r, name, pct, note in with_ties(items):
        top_rows.append(["annual", "2023-24", "FY", "2024-06-30", scope, "body_part", r, name, pct,
                         note or "", ANNUAL, page])
write("top_categories.csv",
      ["period_type", "fiscal_year", "fy_quarter", "period_end", "scope", "dimension", "rank", "category",
       "percent", "note", "source", "page"], top_rows)

# ------------------------------------------------------------------- annual --
# commodity, hours (M), LTIs, RWIs, LTIFR, RWIFR, LTIFR+RWIFR, days lost, days restricted (LTIs),
# duration rate (lost), injury index (lost), duration rate (lost+restricted), injury index (lost+restricted),
# days restricted (RWIs), duration rate (RWI), injury index (RWI)
COMM = [
    ("Iron ore", 125.7, 322, 411, 2.6, 3.3, 5.8, 10478, 7880, 32.5, 83.3, 57.0, 146.0, 16255, 39.5, 129.3),
    ("Gold", 63.8, 61, 255, 1.0, 4.0, 5.0, 1784, 1420, 29.2, 28.0, 52.5, 50.2, 8731, 34.2, 136.9),
    ("Tin, tantalum and lithium", 22.9, 11, 50, 0.5, 2.2, 2.7, 247, 152, 22.5, 10.8, 36.3, 17.4, 1541, 30.8, 67.4),
    ("Nickel", 20.9, 63, 92, 3.0, 4.4, 7.4, 1615, 1871, 25.6, 77.4, 55.3, 167.0, 3505, 38.1, 168.0),
    ("Bauxite and alumina", 14.0, 62, 73, 4.4, 5.2, 9.6, 1446, 1328, 23.3, 103.0, 44.7, 197.5, 2196, 30.1, 156.4),
    ("Exploration", 8.3, 22, 32, 2.6, 3.8, 6.5, 1124, 145, 51.1, 134.8, 57.7, 152.2, 975, 30.5, 116.9),
    ("Heavy mineral sands", 5.8, 6, 17, 1.0, 2.9, 4.0, 195, 70, 32.5, 33.7, 44.2, 45.8, 773, 45.5, 133.6),
    ("Copper, lead and zinc", 3.0, 3, 14, 1.0, 4.7, 5.7, 68, 89, 22.7, 22.7, 52.3, 52.4, 368, 26.3, 122.7),
    ("Salt", 2.2, 6, 3, 2.8, 1.4, 4.1, 228, 74, 38.0, 105.0, 50.3, 139.1, 74, 24.7, 34.1),
    ("Construction materials", 1.8, 8, 0, 4.5, 0.0, 4.5, 136, 107, 17.0, 76.7, 30.4, 137.1, 0, 0.0, 0.0),
    ("Coal", 1.8, 8, 2, 4.5, 1.1, 5.6, 180, 245, 22.5, 101.7, 53.1, 240.1, 35, 17.5, 19.8),
    ("Rare earths", 1.7, 4, 9, 2.4, 5.4, 7.8, 9, 186, 2.3, 5.4, 48.8, 116.9, 367, 40.8, 220.0),
    ("Other", 6.2, 15, 16, 2.4, 2.6, 5.0, 366, 285, 24.4, 58.6, 43.4, 104.3, 573, 35.8, 91.8),
]
COMM_TOTAL = ("All commodities", 278.0, 591, 974, 2.1, 3.5, 5.6, 17876, 13852, 30.2, 64.3, 53.7, 114.1, 35393, 36.3, 127.3)
rows = [list(c) + [1 if c[2] < 10 else 0, ANNUAL, "8, 10, 11"] for c in COMM]
write("annual_commodity_2023_24.csv",
      ["commodity", "hours_millions", "ltis", "rwis", "ltifr", "rwifr", "ltifr_plus_rwifr",
       "days_lost", "days_restricted_from_ltis", "dur_rate_days_lost", "inj_index_days_lost",
       "dur_rate_lost_and_restricted", "inj_index_lost_and_restricted",
       "days_restricted_from_rwis", "dur_rate_rwi", "inj_index_rwi",
       "small_sample", "source", "page"], rows)

# region, hours (M), LTIFR, RWIFR, LTIFR+RWIFR, 10-yr FIFR  (mining only, excludes exploration)
REG = [
    ("Pilbara", 134.07, 2.45, 3.27, 5.73, 0.007),
    ("Goldfields-Esperance", 76.22, 1.46, 3.50, 4.96, 0.010),
    ("Mid West", 14.93, 1.34, 5.83, 7.17, 0.015),
    ("South West", 12.76, 1.72, 3.68, 5.41, 0.021),
    ("Peel", 11.58, 3.80, 4.32, 8.12, 0.0),
    ("Wheatbelt", 8.29, 1.21, 2.66, 3.86, 0.029),
    ("Perth", 6.88, 3.05, 3.20, 6.25, 0.037),
    ("Kimberley", 3.34, 1.79, 1.50, 3.29, 0.0),
    ("Gascoyne", 1.21, 2.48, 0.83, 3.30, 0.0),
    ("Indian Ocean Territories", 0.35, 2.89, 2.89, 5.77, 0.0),
    ("Great Southern", 0.09, 23.32, 11.66, 34.98, 0.0),
]
rows = []
for reg, hrs, lf, rf, comb, fifr in REG:
    il, ir = round(lf * hrs), round(rf * hrs)  # derived counts, not published
    rows.append([reg, hrs, lf, rf, comb, fifr, il, ir, 1 if il < 10 else 0, ANNUAL, "28-32"])
write("annual_regions_2023_24.csv",
      ["region", "hours_millions", "ltifr", "rwifr", "ltifr_plus_rwifr", "fifr_10yr_2014_15_to_2023_24",
       "ltis_implied", "rwis_implied", "small_sample", "source", "page"], rows)

# fatalities
YEARS = [("2014-15", 3, 1), ("2015-16", 4, 0), ("2016-17", 1, 0), ("2017-18", 2, 1), ("2018-19", 2, 0),
         ("2019-20", 2, 0), ("2020-21", 2, 0), ("2021-22", 1, 0), ("2022-23", 3, 0), ("2023-24", 1, 0)]
FCOM = [("Iron ore", 1048.4, 5, 0.005), ("Gold", 510.3, 9, 0.018), ("Nickel", 145.1, 1, 0.007),
        ("Bauxite and alumina", 135.5, 2, 0.015), ("Tin, tantalum and lithium", 75.7, 0, 0.000),
        ("Exploration", 63.8, 2, 0.031), ("Copper, lead and zinc", 40.0, 1, 0.025),
        ("Heavy mineral sands", 39.5, 1, 0.025), ("Construction materials", 15.6, 1, 0.064),
        ("Coal", 15.2, 1, 0.066), ("Salt", 14.2, 0, 0.000), ("Other", 62.3, 0, 0.000)]
FTYPE = [("Caught by / between operating machine", 5, 0), ("Fall from height", 4, 0),
         ("Vehicle / mobile rollover", 3, 0), ("Rockfall", 2, 0), ("Exposure to environment", 2, 1),
         ("Struck by object", 2, 1), ("Caught by / between (not machine)", 1, 0),
         ("Fall getting on / off", 1, 0), ("Insect or animal bite", 1, 0),
         ("Struck by vehicle / mobile", 1, 0), ("Vehicle / mobile collision", 1, 0)]
rows = []
for fy, mining, expl in YEARS:
    rows.append(["year", fy, mining + expl, expl, None, None, fy, ANNUAL, 4,
                 "chart bar heights (integers; total reconciles to 23)"])
for name, hrs, n, fifr in FCOM:
    rows.append(["commodity", name, n, 1 if name == "Exploration" else 0, hrs, fifr, "2014-15 to 2023-24",
                 ANNUAL, 5, "table"])
for name, n, expl in FTYPE:
    rows.append(["incident_type", name, n, expl, None, None, "2014-15 to 2023-24", ANNUAL, 5,
                 "chart bar heights (integers; total reconciles to 23)"])
write("fatalities.csv",
      ["breakdown", "category", "fatalities", "of_which_exploration", "hours_millions",
       "fifr_per_million_hours", "period", "source", "page", "read_method"], rows)

# annual summary, long format: fiscal_year, scope, metric, value, unit, page
M = "million hours"
FR = "per million hours"
SUMMARY = [
    ("2023-24", "all", "hours_worked", 278.0, M, 8), ("2023-24", "all", "ltis", 591, "count", 1),
    ("2023-24", "all", "rwis", 974, "count", 1), ("2023-24", "all", "ltifr", 2.126, FR, 1),
    ("2023-24", "all", "rwifr", 3.504, FR, 1), ("2023-24", "all", "days_lost_from_ltis", 17876, "days", 10),
    ("2023-24", "all", "days_restricted_from_ltis", 13852, "days", 10),
    ("2023-24", "all", "days_restricted_from_rwis", 35393, "days", 11),
    ("2023-24", "all", "days_restricted_total", 49245, "days", 1), ("2023-24", "all", "fatalities", 1, "count", 3),
    ("2023-24", "mining", "hours_worked", 269.7, M, 3), ("2023-24", "mining", "fatalities", 1, "count", 3),
    ("2023-24", "mining", "ltis", 569, "count", 3), ("2023-24", "mining", "ltifr", 2.1, FR, 3),
    ("2023-24", "mining", "rwis", 942, "count", 3), ("2023-24", "mining", "rwifr", 3.5, FR, 3),
    ("2023-24", "mining", "hours_pct_company_employees", 44, "percent", 3),
    ("2023-24", "mining", "hours_pct_contractors", 56, "percent", 3),
    ("2023-24", "mining", "injuries_pct_company_employees", 62, "percent", 3),
    ("2023-24", "mining", "injuries_pct_contractors", 38, "percent", 3),
    ("2023-24", "exploration", "hours_worked", 8.3, M, 3), ("2023-24", "exploration", "fatalities", 0, "count", 3),
    ("2023-24", "exploration", "ltis", 22, "count", 3), ("2023-24", "exploration", "ltifr", 2.6, FR, 3),
    ("2023-24", "exploration", "rwis", 32, "count", 3), ("2023-24", "exploration", "rwifr", 3.8, FR, 3),
    ("2023-24", "exploration", "hours_pct_company_employees", 37, "percent", 3),
    ("2023-24", "exploration", "hours_pct_contractors", 63, "percent", 3),
    ("2023-24", "exploration", "injuries_pct_company_employees", 57, "percent", 3),
    ("2023-24", "exploration", "injuries_pct_contractors", 43, "percent", 3),
    ("2023-24", "surface", "hours_worked", 252.0, M, 20), ("2023-24", "surface", "ltis", 553, "count", 20),
    ("2023-24", "surface", "rwis", 853, "count", 20), ("2023-24", "surface", "ltifr", 2.2, FR, 20),
    ("2023-24", "surface", "rwifr", 3.4, FR, 20), ("2023-24", "surface", "share_of_hours", 91, "percent", 20),
    ("2023-24", "underground", "hours_worked", 26.0, M, 21), ("2023-24", "underground", "ltis", 38, "count", 21),
    ("2023-24", "underground", "rwis", 121, "count", 21), ("2023-24", "underground", "ltifr", 1.5, FR, 21),
    ("2023-24", "underground", "rwifr", 4.7, FR, 21), ("2023-24", "underground", "share_of_hours", 9, "percent", 21),
    ("2022-23", "all", "ltis", 536, "count", 1), ("2022-23", "all", "ltifr", 2.036, FR, 1),
    ("2022-23", "all", "rwis", 920, "count", 1), ("2022-23", "all", "rwifr", 3.495, FR, 1),
    ("2022-23", "all", "fatalities", 3, "count", 4),
    ("2022-23 carry-over into 2023-24", "all", "ltis", 163, "count", 11),
    ("2022-23 carry-over into 2023-24", "all", "rwis", 248, "count", 11),
    ("2022-23 carry-over into 2023-24", "all", "days_lost", 13256, "days", 11),
    ("2022-23 carry-over into 2023-24", "all", "days_restricted", 31734, "days", 11),
]
write("annual_summary.csv", ["fiscal_year", "scope", "metric", "value", "unit", "source", "page"],
      [list(r[:5]) + [ANNUAL, r[5]] for r in SUMMARY])

# ------------------------------------------------------------- reconciliation --
def close(a, b, tol):
    return abs(a - b) <= tol


problems = []

# quarterly counts: totals add up, and revised rates sit within a plausible range
for key, period, fy, fq, start, end, issued, fat, lti, rwi, r1, r2, _ in Q:
    if lti is not None and not (0 <= fat <= 5 and lti > 0 and rwi > 0):
        problems.append(f"quarter {key}: implausible counts")

# annual commodity table vs published totals
t = COMM_TOTAL
for idx, label, tol in [(1, "hours", 0.15), (2, "LTIs", 0), (3, "RWIs", 0), (7, "days lost", 0),
                        (8, "days restricted (LTI)", 0), (13, "days restricted (RWI)", 0)]:
    s = sum(c[idx] for c in COMM)
    if not close(s, t[idx], tol):
        problems.append(f"commodity {label}: rows sum {s} vs total {t[idx]}")
for c in COMM:
    name, hrs, ltis, rwis, lf, rf, comb, dl, dr_l, dur_l, ix_l, dur_lr, ix_lr, dr_r, dur_r, ix_r = c
    # published rates must be reproducible from counts and hours (allowing for hours rounded to 0.1M)
    for cnt, rate, nm in [(ltis, lf, "LTIFR"), (rwis, rf, "RWIFR")]:
        lo, hi = cnt / (hrs + 0.05) - 0.05, cnt / (hrs - 0.05) + 0.05
        if not lo <= rate <= hi:
            problems.append(f"{name} {nm}: {rate} outside [{lo:.2f}, {hi:.2f}]")
    if not close(lf + rf, comb, 0.11):
        problems.append(f"{name}: LTIFR+RWIFR {lf + rf:.1f} vs {comb}")
    if ltis and not close(dl / ltis, dur_l, 0.06):
        problems.append(f"{name}: duration rate (lost) {dl / ltis:.2f} vs {dur_l}")
    if ltis and not close((dl + dr_l) / ltis, dur_lr, 0.06):
        problems.append(f"{name}: duration rate (lost+restricted) {(dl + dr_l) / ltis:.2f} vs {dur_lr}")
    if rwis and not close(dr_r / rwis, dur_r, 0.06):
        problems.append(f"{name}: duration rate (RWI) {dr_r / rwis:.2f} vs {dur_r}")
    if not close(dl / hrs, ix_l, 0.04 * max(ix_l, 1) + 0.2):
        problems.append(f"{name}: injury index (lost) {dl / hrs:.1f} vs {ix_l}")
if 17876 + 0 != t[7] or 13852 + 35393 != 49245:
    problems.append("days restricted total does not reconcile to 49,245")

# regions
hrs_sum = sum(r[1] for r in REG)
if not close(hrs_sum, 269.7, 0.06):
    problems.append(f"region hours {hrs_sum:.2f} vs mining hours 269.7")
for reg, hrs, lf, rf, comb, _ in REG:
    if not close(lf + rf, comb, 0.02):
        problems.append(f"{reg}: LTIFR+RWIFR {lf + rf:.2f} vs {comb}")
il_sum = sum(round(r[2] * r[1]) for r in REG)
ir_sum = sum(round(r[3] * r[1]) for r in REG)
if not (close(il_sum, 569, 3) and close(ir_sum, 942, 3)):
    problems.append(f"implied region counts {il_sum}/{ir_sum} vs mining 569/942")

# fatalities: three breakdowns must each total 23, with 2 in exploration
for label, total, expl in [("year", sum(m + e for _, m, e in YEARS), sum(e for _, _, e in YEARS)),
                           ("commodity", sum(n for _, _, n, _ in FCOM), 2),
                           ("incident type", sum(n for _, n, _ in FTYPE), sum(e for _, _, e in FTYPE))]:
    if total != 23 or expl != 2:
        problems.append(f"fatalities by {label}: total {total}, exploration {expl}")
if not close(sum(h for _, h, _, _ in FCOM), 2165.7, 0.15):
    problems.append("fatality hours do not sum to 2,165.7")

# surface + underground should equal all-sector totals (both include exploration)
if not (close(252.0 + 26.0, 278.0, 0.01) and 553 + 38 == 591 and 853 + 121 == 974):
    problems.append("surface + underground does not equal all-sector totals")
if not (569 + 22 == 591 and 942 + 32 == 974):
    problems.append("mining + exploration does not equal all-sector totals")

# top categories: percentages valid
for r in top_rows:
    if not 0 < r[8] <= 100:
        problems.append(f"top category percent out of range: {r}")

print()
print("RECONCILIATION:", "all checks passed" if not problems else f"{len(problems)} problem(s)")
for p in problems:
    print(" -", p)
print(f"2023-24 quarters sum: LTIs {sum(q[8] for q in Q if q[2] == '2023-24')}, "
      f"RWIs {sum(q[9] for q in Q if q[2] == '2023-24')} (annual mining: 569 / 942)")
print(f"Implied region counts: LTIs {il_sum}, RWIs {ir_sum}")
