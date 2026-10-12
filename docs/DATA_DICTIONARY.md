# Data dictionary

The clean table has 30 columns. Numeric source features are retained without unit conversion. UCI provides names but limited feature definitions; unspecified index formulas are not reverse-engineered or assumed.

| Clean field | Type | Meaning / treatment |
|---|---|---|
| `record_id` | int64 | Generated 1-based source row number; not a plate or machine ID. |
| `x_minimum` | int64 | Source X minimum coordinate. |
| `x_maximum` | int64 | Source X maximum coordinate. |
| `y_minimum` | int64 | Source Y minimum coordinate. |
| `y_maximum` | int64 | Source Y maximum coordinate. |
| `pixels_areas` | int64 | Source defect area in image pixels; not calibrated physical area. |
| `x_perimeter` | int64 | Source X perimeter measurement; retained without conversion. |
| `y_perimeter` | int64 | Source Y perimeter measurement; retained without conversion. |
| `sum_of_luminosity` | int64 | Source summed luminosity feature. |
| `minimum_of_luminosity` | int64 | Source minimum luminosity feature. |
| `maximum_of_luminosity` | int64 | Source maximum luminosity feature. |
| `length_of_conveyer` | int64 | Source conveyer-length feature; units not asserted. |
| `steel_plate_thickness` | int64 | Source thickness measurement; units unspecified, no mm conversion. |
| `edges_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `empty_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `square_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `outside_x_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `edges_x_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `edges_y_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `outside_global_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `logofareas` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `log_x_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `log_y_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `orientation_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `luminosity_index` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `sigmoidofareas` | float64 | Source engineered numerical feature; exact formula/units not documented on the cited source page. Retained unchanged. |
| `fault_type` | object | Single readable category from the seven source binary labels. |
| `steel_type` | object | A300 or A400, decoded from source binary steel flags. |
| `thickness_band` | object | Analyst bins: <=50, >50 to <=100, >100, in source units. |
| `log10_pixel_area` | float64 | Computed log10(pixels_areas); retained alongside source LogOfAreas. |

## Raw-label handling

Raw labels are `Pastry`, `Z_Scratch`, `K_Scatch`, `Stains`, `Dirtiness`, `Bumps`, and `Other_Faults`. Exactly one must equal 1 per row. Raw steel flags must also be binary and sum to 1. Their clean categorical replacements remove redundant flags. Original names and values remain available in `data/raw/`.

Zero missing cells and zero exact duplicate rows were observed. A future duplicate is reported, not automatically deleted, because no source observation identifier proves that identical measurements are duplicate events.
