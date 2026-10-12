# Quality investigation brief

## Decision to support

Select a small set of fault categories for engineering review. This analysis describes 1,941 labeled fault observations from the UCI Steel Plates Faults dataset; it is not a production performance audit.

## Evidence and interpretation

1. **Concentration:** Other Faults (673), Bumps (402), and K Scratch (391) together represent 1,466 observations, or 75.53%. Adding Z Scratch reaches 85.32%. The three-category result is not an “80/20 rule”; use the actual cumulative share.
2. **Measurement choice changes priorities:** Other Faults is most frequent, but K Scratch contributes 2,980,458 of 3,676,018 summed pixel-area units (81.08%). K Scratch's median area is 6,281 pixels, compared with 146 for Other Faults. The pattern is not based solely on one maximum value. Image calibration and defect severity still need validation.
3. **Composition varies by steel type:** Bumps represents 279/777 (35.91%) of A300 observations and 123/1,164 (10.57%) of A400 observations. K Scratch is 1/777 (0.13%) for A300 and 390/1,164 (33.51%) for A400. These are composition differences among observed faults, not evidence that A400 has a greater production failure risk.
4. **Labeling may limit diagnosis:** 34.67% of records are Other Faults. That bucket is too broad to provide a specific corrective action by itself.

## Recommended investigation sequence

| Priority | Proposed action | Evidence needed before implementation |
|---|---|---|
| 1 | Review representative Other Faults records and refine label definitions | Images, labeling rules, engineer review |
| 2 | Investigate K Scratch cases for shared process conditions | Calibrated images, line/batch IDs, handling records, severity assessment |
| 3 | Investigate the Bumps mix within steel types | Comparable sampling, production volumes, process settings, repeated observations |
| 4 | Collect denominators and operational outcomes | Total inspected plates, good plates, rework/scrap, downtime and costs |

These are proposed next steps; no operational change or improvement has been measured.

## Data quality

The delivered source has 1,941 rows and 34 columns, no missing values, and no exact duplicate rows. Each observation has one fault label and one steel-type flag. All recorded pixel areas and thickness values are positive and coordinate maxima are not below minima. Source values are retained; data quality checks cannot independently verify measurement accuracy.

## Decision boundaries

Do not calculate plant defect rate from a fault-only dataset. Do not equate defect record count to distinct plate count. Do not infer root causes from category associations. Do not convert pixel areas into square millimeters or money without calibration and cost data. Do not present this 2010 research dataset as a current factory audit.
