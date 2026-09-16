# AI-Assisted Prompting Log

## Prompt #1 — SQL (RCTCF)

**Role:** Act as a SQL tutor and debugging partner who is careful about SQLite syntax and aggregate calculations.

**Context:** I am building the BigBasket Category Performance Diagnostic project in SQLite. The database contains `orders`, `products`, `customers`, and `category_targets`. Delivered orders should be used for revenue reporting. SQLite uses `strftime('%Y-%m', order_date)` for month extraction, and integer division must be avoided when calculating percentage variance.

**Task:** Draft/debug the SQL query that joins category-level Delivered revenue to `category_targets` and returns `category`, `total_revenue`, `target_revenue_inr`, `variance`, `percentage_variance`, and a three-way `target_status` using Above Target, Below Target - Watch, and Below Target - Critical.

**Constraints:** Use SQLite-compatible SQL; calculate `variance` as target minus revenue; calculate percentage variance with floating-point-safe arithmetic; use the 15% shortfall threshold; do not change table names or business rules.

**Format:** Return one runnable SQL query followed by a short explanation of each calculated field.

**Verification actually performed:** I ran the retained query against `bigbasket_capstone.db` and checked the six category results against the known SQL totals; the totals were 21715, 16382, 15410, 14090, 10895, and 9790, confirming the join and floating-point percentage calculation were behaving as intended.

## Prompt #2 — Pandas (RCTCF)

**Role:** Act as a Pandas data-cleaning tutor and code reviewer.

**Context:** I have a deliberately messy BigBasket `orders_raw.csv` containing duplicate order IDs, inconsistent city/category casing, missing `amount_inr` values, and extreme revenue outliers. Revenue analysis must use Delivered orders, missing revenue must be excluded rather than filled, and outliers must be capped rather than dropped.

**Task:** Explain/debug the Pandas IQR approach for Delivered, non-null `amount_inr` values: calculate Q1 and Q3 with `.quantile()`, calculate `IQR`, calculate the upper fence `Q3 + 1.5*IQR`, and cap values above the fence with `.clip(upper=...)`.

**Constraints:** Do not drop outliers; do not replace missing revenue with zero or a mean; compute the fence only from Delivered non-null revenue; keep the original row count after duplicate removal.

**Format:** Provide concise Pandas code plus a short explanation of why `.clip()` is appropriate.

**Verification actually performed:** I re-ran the suggested IQR logic on the generated raw export and manually checked the resulting counts and capped values: Q1 was 90.0, Q3 was 275.0, the upper fence was 552.5, and 16 Delivered rows were above the fence and therefore capped at 552.5.
