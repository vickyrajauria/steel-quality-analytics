-- SQLite dialect. Each named statement is exported by python -m src.pipeline.
-- Grain: one labeled fault observation, NOT all produced/inspected plates.

-- query: overall_kpis
SELECT COUNT(*) AS fault_records, COUNT(DISTINCT fault_type) AS fault_categories,
       COUNT(DISTINCT steel_type) AS steel_types,
       ROUND(AVG(pixels_areas), 2) AS mean_pixel_area,
       SUM(pixels_areas) AS summed_pixel_area
FROM faults;

-- query: fault_pareto
WITH counts AS (
 SELECT fault_type, COUNT(*) AS records FROM faults GROUP BY fault_type
)
SELECT fault_type, records,
 ROUND(100.0 * records / SUM(records) OVER (), 2) AS record_share_pct,
 ROUND(100.0 * SUM(records) OVER (
   ORDER BY records DESC, fault_type ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
 ) / SUM(records) OVER (), 2) AS cumulative_share_pct
FROM counts ORDER BY records DESC, fault_type;

-- query: steel_fault_mix
WITH grouped AS (
 SELECT steel_type, fault_type, COUNT(*) AS records FROM faults GROUP BY steel_type, fault_type
)
SELECT steel_type, fault_type, records,
 SUM(records) OVER (PARTITION BY steel_type) AS steel_sample_size,
 ROUND(100.0*records / SUM(records) OVER (PARTITION BY steel_type), 2) AS within_steel_share_pct
FROM grouped ORDER BY steel_type, records DESC, fault_type;

-- query: thickness_fault_mix
WITH grouped AS (
 SELECT thickness_band, fault_type, COUNT(*) AS records FROM faults GROUP BY thickness_band, fault_type
)
SELECT thickness_band, fault_type, records,
 SUM(records) OVER (PARTITION BY thickness_band) AS band_sample_size,
 ROUND(100.0*records/SUM(records) OVER (PARTITION BY thickness_band), 2) AS within_band_share_pct
FROM grouped ORDER BY thickness_band, records DESC, fault_type;

-- query: area_priority
WITH grouped AS (
 SELECT fault_type, COUNT(*) AS records, SUM(pixels_areas) AS total_pixels,
        AVG(pixels_areas) AS mean_pixels FROM faults GROUP BY fault_type
)
SELECT fault_type, records, total_pixels, ROUND(mean_pixels,2) AS mean_pixels,
 ROUND(100.0*total_pixels/SUM(total_pixels) OVER (),2) AS pixel_share_pct,
 DENSE_RANK() OVER (ORDER BY total_pixels DESC) AS pixel_area_rank
FROM grouped ORDER BY pixel_area_rank;
