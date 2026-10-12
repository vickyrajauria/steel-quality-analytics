# Dataset provenance

Source: Buscema, M., Terzi, S., & Tastle, W. (2010), Steel Plates Faults, UCI Machine Learning Repository, https://doi.org/10.24432/C5J88N.
Source page: https://archive.ics.uci.edu/dataset/198/steel+plates+faults
Download: https://archive.ics.uci.edu/static/public/198/steel+plates+faults.zip
Retrieved: 2026-10-12. License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/.

The original `Faults.NNA` and `Faults27x7_var` are bundled unchanged. Source data was donated in 2010; retrieval date does not imply recent observations. The records represent labeled faults, not the entire inspected population.

Processed data adapts the source: lower-case column names, one-hot flags combined into readable categories, display spelling `K_Scatch` mapped to `K Scratch`, analyst-defined thickness bands, log10 pixel area, and sequential source-row ID. No records are removed. `record_id` is generated and is not a source plate or machine identifier.

`source_manifest.json` records raw file hashes. `python -m src.download_data` optionally downloads and verifies source bytes. The bundled files make the normal pipeline reproducible offline after dependency installation. Data license is independent of the project code's MIT license.
