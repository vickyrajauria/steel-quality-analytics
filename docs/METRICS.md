# Metric definitions

| Metric | Calculation | Meaning / boundary |
|---|---|---|
| Fault observations | Count rows in the selection | Not total production or unique plates |
| Category share | Category records / selected records × 100 | Fault composition, not defect probability |
| Cumulative share | Running sum of category counts, descending count / selected count × 100 | Pareto coverage; ties ordered by category |
| Within-steel share | Category records for a steel / all selected fault records for that steel × 100 | Corrects unequal sample denominators, not selection bias |
| Pixel-area share | Sum of category pixel areas / sum of selected pixel areas × 100 | Image measurement concentration, not physical area, severity or cost |
| Median pixel area | 50th percentile of selected pixel areas | Less sensitive to large extremes than mean |
| Thickness band | <=50, >50 to <=100, >100 in source units | Descriptive analyst bins; no engineering thresholds implied |

A300 and A400 sample counts are 777 and 1,164 before filtering. Every dashboard card and chart uses the current steel and thickness selection. Empty selections display a message rather than invalid divisions. No dates are fabricated.

## Why no model?

The project answers descriptive questions needed by an analyst. Adding a classifier would introduce a different objective, evaluation design, and leakage risks without providing the missing production or cost information. A classification extension should be scoped and tested separately.
