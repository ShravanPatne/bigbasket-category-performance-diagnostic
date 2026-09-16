# BigBasket Category Data Story

Part 1's clean SQL diagnostic shows three categories above target and three below target:

| Category | Revenue (INR) | Target (INR) | Variance (Target - Revenue) | % Variance | Status |
|---|---:|---:|---:|---:|---|
| Household Essentials | 21,715 | 17,000 | -4,715 | 27.74% | Above Target |
| Personal Care | 16,382 | 15,500 | -882 | 5.69% | Above Target |
| Bakery | 15,410 | 12,000 | -3,410 | 28.42% | Above Target |
| Dairy & Eggs | 14,090 | 16,500 | 2,410 | -14.61% | Below Target - Watch |
| Snacks & Beverages | 10,895 | 13,000 | 2,105 | -16.19% | Below Target - Critical |
| Fruits & Vegetables | 9,790 | 12,000 | 2,210 | -18.42% | Below Target - Critical |

## Recommendation 1
Prioritize **Fruits & Vegetables** for catalog and marketing review. It has the largest percentage shortfall among the categories at 18.42% below its INR 12,000 target, making it the clearest under-target category to investigate.

## Recommendation 2
Review **Dairy & Eggs** suppliers and category execution before the shortfall worsens. Revenue is INR 14,090 against a INR 16,500 target, a 14.61% shortfall that falls inside the project's Watch band.

The Part 4 Pandas analysis independently reaches the same top-category and top-supplier conclusion: Household Essentials is the top category and HomeEssentials Traders is the top supplier. Its exact rupee totals differ because the raw export is independently cleaned, missing revenue is excluded, and IQR outliers are capped.
