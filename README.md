# Retail Sales Analytics — SQL Pivot & Quality-Impact Analysis

A compact analytics project demonstrating two common operations-analytics tasks:

1. **SQL pivot reporting** — turning a long transactional table into a monthly
   sales summary per SKU, with month/quarter shares and ranking.
2. **Quality-impact visualization** — quantifying how the defect rate affects
   profit margin and communicating the finding as a clear, actionable insight.

The dataset here is **synthetic** (randomly generated) and mirrors the *structure*
of a typical retail operations dataset — no proprietary or client data is included.

---

## What this shows

- Conditional aggregation (`CASE WHEN`) to pivot months into columns
- Window functions (`SUM() OVER ()`, `ROW_NUMBER()`) for shares and ranking
- Correct handling of the integer-division trap (`1.0 *` / `CAST AS FLOAT`)
- Both **SQLite** and **SQL Server (T-SQL)** dialects, side by side
- A correlation-focused scatter plot with a fitted trend line

---

## Repository structure

```
retail-sales-analytics/
├── data/
│   ├── sales_sample.csv        # synthetic transactional data (OrderDate, SKU, UnitsSold)
│   └── quality_sample.csv      # synthetic quality data (Date, Orders, Defects, Revenue, Profit)
├── sql/
│   ├── 01_monthly_pivot.sql    # pivot + shares + rank (SQLite + SQL Server)
│   └── 02_defect_margin.sql    # defect-rate vs margin extract
├── python/
│   ├── load_data.py            # loads CSVs into analytics.db (SQLite)
│   └── visualize.py            # builds the scatter plot
├── output/
│   └── defect_margin_impact.png
└── README.md
```

---

## How to run

```bash
# 1. Install dependencies
pip install pandas matplotlib numpy

# 2. Load the data into a local SQLite database
cd python
python load_data.py            # creates analytics.db (tables: sales, quality)

# 3. Run the SQL (in DBeaver, SSMS, or the sqlite3 CLI)
#    open sql/01_monthly_pivot.sql and sql/02_defect_margin.sql

# 4. Build the visualization
python visualize.py            # writes output/defect_margin_impact.png
```

---

## Task 1 — Monthly SKU pivot

From a long table of daily `(OrderDate, SKU, UnitsSold)` rows, produce one row per
SKU with January / February / March unit sales, the Q1 total, each period's share
of that period's grand total, and a rank by Q1 volume.

Key technique — conditional aggregation feeding window functions:

```sql
SUM(CASE WHEN MONTH(OrderDate) = 1 THEN UnitsSold ELSE 0 END) AS Jan
...
CAST(Jan AS FLOAT) / SUM(Jan) OVER () AS JanShare      -- share of column total
ROW_NUMBER() OVER (ORDER BY Q1 DESC) AS Rank
```

**Note on the integer-division trap:** dividing two integers in SQL truncates to
zero. Casting to float (`1.0 *` in SQLite, `CAST(... AS FLOAT)` in SQL Server)
is required for correct share percentages.

---

## Task 2 — Defect rate vs profit margin

Two derived metrics:

- `DefectRate  = Defects / Orders`
- `ProfitMargin = Profit / Revenue`

Plotting margin against defect rate reveals a strong **inverse relationship**:
as the defect rate rises, profit margin falls in a near-linear fashion. The
scatter plot (with trend line) makes this the headline finding rather than
burying it in a time-series chart.

![Defect vs Margin](output/defect_impact.png)

**Business takeaway:** defects are a direct, predictable drag on profitability —
each increase in defect rate erodes margin linearly, so quality control has a
measurable, quantifiable payback.

---

## Tech stack

Python (pandas, matplotlib, numpy) · SQLite · SQL Server (T-SQL) · DBeaver
