# Understand the project before putting it on your CV

## A 45-second explanation

“I analyzed 1,941 labeled steel fault observations using Python and SQLite. I validated the source, converted one-hot labels into categories, and used SQL window functions to calculate Pareto and within-steel shares. Three categories represented 75.5% of the recorded faults. K Scratch represented about 20.1% of records but 81.1% of summed pixel area, showing why frequency alone is insufficient. I built a Streamlit dashboard to explore steel and thickness groups. Because there are no defect-free observations or production totals, I report fault composition rather than factory rejection rates.”

## Questions you should answer without reading code

1. **What is one row?** A labeled fault observation; not necessarily a unique plate.
2. **Why SQL and Python?** SQL expresses grouped metrics and windows; Python handles validation, reproducible preparation, plots, and dashboard integration. SQL outputs are reconciled against pandas calculations.
3. **What did you clean?** Labels, column naming, types/categories and analytical structure. There were no missing values or exact duplicates; do not pretend to have removed thousands of dirty rows.
4. **Why not compare raw A300 and A400 counts?** Their sample sizes differ. Within-steel percentages normalize the denominator, though they cannot fix sampling bias.
5. **What does 81.1% mean?** K Scratch's share of summed recorded pixel areas. It is not 81.1% of defects, steel production, damage costs, or scrap mass.
6. **How did you handle outliers?** Retained them because there was no basis to classify them as errors; report median alongside aggregate pixel area.
7. **Why not claim savings?** No costs or implemented intervention exist. Recommendations are hypotheses for engineering validation.
8. **What would you request next?** Production and inspection totals, timestamps, plate/line/batch IDs, calibrated imaging, severity, and cost outcomes.
9. **Why is there no time chart?** No timestamp exists, and source row order is not a timeline.
10. **Where is the SQL window function useful?** It calculates cumulative category totals and group denominators without collapsing the grouped rows further.

## A focused practice sequence

- Run the pipeline and dashboard yourself; change filters and explain why each denominator changes.
- Recalculate 391/1,941 and 2,980,458/3,676,018 manually.
- Write the category-count SQL from memory, then add the cumulative window.
- Inspect 10 raw rows and trace them to the clean table using `record_id`.
- Add one analysis of your own, with a justified denominator and limitations.
- Explain one test failure by deliberately setting a pixel area to zero in a temporary DataFrame.

If asked about assistance, accurately explain that AI helped scaffold the code and that you reviewed, ran, and understood it only after you have actually done those steps. Do not present generated code as proof of skills you have not yet practiced.
