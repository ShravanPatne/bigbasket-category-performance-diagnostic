# BigBasket Category Performance Diagnostic

This capstone creates one deterministic BigBasket-style SQLite dataset, produces a fixed monthly category revenue CSV, reconciles that exact CSV in a spreadsheet, visualizes the same numbers in Tableau Public, and independently cleans the deliberately messy raw export in Pandas. The clean SQL diagnostic and the independent Pandas pipeline agree on the key business findings while preserving a clear audit trail from source data to final recommendation.

## Tableau Public

**Live dashboard:** https://public.tableau.com/app/profile/shravan.patne6614/viz/BigBasketCategoryPerformanceDashboard\_17894915053080/Dashboard1

Publish the dashboard from Tableau Public, set it to public, then replace the placeholder above with the exact live view URL.

## Data story

See [`DATA\_STORY.md`](DATA_STORY.md). The clean SQL totals identify Household Essentials, Personal Care, and Bakery as Above Target; Dairy \& Eggs as Below Target - Watch; and Snacks \& Beverages plus Fruits \& Vegetables as Below Target - Critical. The two recommendations focus on Fruits \& Vegetables and Dairy \& Eggs using only the dashboard numbers.

## Repository structure

```text
.
├── generate\_data.py
├── bigbasket\_capstone.db
├── orders\_raw.csv
├── products.csv
├── verify.sql
├── 01\_foundations.sql
├── 02\_aggregation\_joins.sql
├── 03\_reporting.sql
├── monthly\_category\_revenue.csv
├── bigbasket\_category\_analysis.xlsx
├── analysis.ipynb
├── ai\_log.md
├── DATA\_STORY.md
└── README.md
```

## Part 1 — SQL

* `generate\_data.py` creates the deterministic SQLite database and both raw CSV exports using the required `random.seed(42)`.
* `verify.sql` records the required verification results: 31 products, 50 customers, 500 orders, 6 category targets; status counts are Delivered 434, Cancelled 42, Pending 24.
* `01\_foundations.sql` contains the required WHERE, DISTINCT, ORDER BY + LIMIT, AS, IN, BETWEEN, NOT BETWEEN, and IS NULL examples.
* `02\_aggregation\_joins.sql` contains the Delivered category aggregation with HAVING and the product-level LEFT JOIN using `COUNT(o.order\_id)`.
* `03\_reporting.sql` contains CASE WHEN product tiers, the monthly-by-category report, and target variance/percentage-variance reporting.
* `monthly\_category\_revenue.csv` is the direct export of the Part 1 monthly report: 36 rows and INR 88,282 total revenue.

### Regenerate the deterministic source data

From the repository root:

```bash
python3 generate\_data.py
```

Do not change the seed or fixed lists/weights. Regenerating with the supplied script recreates the same database and raw exports.

## Part 2 — Spreadsheet

`bigbasket\_category\_analysis.xlsx` contains:

* `Monthly Data` — the unmodified 36-row CSV import.
* `Category Targets` — the six fixed category targets.
* `Pivot Table` — the category-level SUM of revenue and SUM of order count from Monthly Data.
* `Category Summary` — pivot-referenced revenue, XLOOKUP target, variance, percentage variance, nested-IF status, and reconciliation to Part 1 totals.

## Part 3 — Tableau dashboard build

Use `monthly\_category\_revenue.csv` as the only Tableau data source. The dashboard should contain:

1. A Jan–Jun 2026 monthly total revenue line chart.
2. A descending category revenue bar chart.
3. Three-tier category colors: Above Target, Below Target - Watch, Below Target - Critical.
4. Four KPI cards: Total Revenue, Total Delivered Orders, Average Order Value, Categories Meeting Target.
5. A visible category or month filter applied across the dashboard.
6. One combined dashboard with a clean floating layout.

Because Tableau Public publishing requires the user's own Tableau Public account, the final live URL must be pasted into the Tableau Public section above after publication.

## Part 4 — Python/Pandas

`analysis.ipynb` independently:

* loads and inspects both raw CSVs;
* removes eight duplicate order IDs to return to 500 rows;
* cleans city/category casing and whitespace;
* excludes 10 missing revenue values from revenue calculations;
* leaves Cancelled/Pending rating nulls untouched;
* computes IQR using Delivered non-null revenue: Q1 = 90.0, Q3 = 275.0, upper fence = 552.5;
* caps 16 Delivered rows above the upper fence;
* creates date and derived fields;
* calculates category and supplier revenue after cleaning;
* confirms Household Essentials is the top category and HomeEssentials Traders is the top supplier;
* includes three matplotlib charts; and
* contains exactly three What / Why it matters / Next step observations.

## AI-assisted prompting log

See [`ai\_log.md`](ai_log.md) for both RCTCF prompts and the concrete verification performed for each retained solution.

## Key clean SQL numbers

|Category|Delivered revenue (INR)|Target (INR)|Status|
|-|-:|-:|-|
|Household Essentials|21,715|17,000|Above Target|
|Personal Care|16,382|15,500|Above Target|
|Bakery|15,410|12,000|Above Target|
|Dairy \& Eggs|14,090|16,500|Below Target - Watch|
|Snacks \& Beverages|10,895|13,000|Below Target - Critical|
|Fruits \& Vegetables|9,790|12,000|Below Target - Critical|

**Clean monthly CSV grand total:** INR 88,282.

## Free tools

SQLite via Python's built-in `sqlite3`, Google Sheets or Excel, Tableau Public, and Python/Pandas/Matplotlib are sufficient. No paid database, Tableau Desktop, or API account is required for the project.

