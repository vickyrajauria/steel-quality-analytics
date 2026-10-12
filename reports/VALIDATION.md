# Validation record

Validated on 2026-10-12 using the package versions in `environment.json`.

- Pipeline completed from the bundled raw data and produced SQLite, clean CSV, five SQL result CSVs, three PNG charts, audit and metrics.
- Eight automated tests passed: seven cover source validation, failure paths, lineage, SQL/pandas reconciliation and filtered denominators; one dashboard test covers default, steel-filtered, thickness-filtered and empty-selection states.
- All eight notebook code cells executed successfully using the in-process IPython runner; real tables and image outputs are saved in the notebook. Socket-based Jupyter kernel startup was unavailable in the build environment.
- Pareto and steel-composition figures were visually inspected.

Dashboard behavior was tested through Streamlit AppTest. No externally hosted dashboard or remote GitHub deployment was tested or created. CI is included for execution after upload.
