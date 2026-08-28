# Reservoir Water Storage & Drought Trends: Nagarjuna Sagar and Srisailam (Krishna River, India)

A 38-year satellite time series analysis of water surface area for two major reservoirs on the Krishna River in Telangana and Andhra Pradesh, using the JRC Global Surface Water dataset, with a terrain and drainage context map covering the corridor between them.

## Key Finding

An initial pass at this analysis produced a striking but misleading result: a statistically significant increasing trend in water area (p < 0.0001) and "drought years" clustered entirely in 1984-1990, near the start of the satellite record. Investigation showed this was a data-completeness artifact, not a hydrological signal, early Landsat coverage of these reservoirs was sparser and noisier than later years, so a larger share of each reservoir's pixels were "no data" rather than genuinely dry land, manufacturing an apparent decline at the start of the record and a spurious increasing trend over time as coverage quality improved.

This was corrected by computing the percentage of valid (non-"no data") pixels observed each month and restricting the analysis to months with at least 70% reliable coverage. The corrected analysis shows no statistically significant long-term trend in either reservoir (p = 0.26 for Nagarjuna Sagar, p = 0.68 for Srisailam) and identifies drought years spread realistically across the record: 2002-2004 and 2015 for Nagarjuna Sagar, and 2004, 2012, and 2015 for Srisailam. These years were checked against documented South Indian drought history rather than accepted at face value, both periods match well-recorded droughts, and one contemporaneous report states Nagarjuna Sagar had no water in live storage during 2015-16, directly corroborating the satellite-derived finding for the same reservoir and year.

## Methodology

**Data source.** JRC Global Surface Water Monthly History (v1.4), accessed via Google Earth Engine. Classifies each 30m Landsat pixel every month as no data, not water, or water, based on the full Landsat archive (1984-2021, 454 monthly images).

**Study areas.** Bounding boxes around each reservoir's full extent: Nagarjuna Sagar (79.05-79.45°E, 16.45-16.75°N) and Srisailam (78.20-78.95°E, 15.70-16.30°N).

**Water area metric.** Monthly water surface area computed as the sum of pixel area (hectares) classified as water, reduced over each reservoir's bounding box at 30m scale.

**Coverage filtering.** Percentage of the bounding box classified as observed (not "no data") computed alongside water area for every month. Months below 70% valid coverage excluded from all trend and drought calculations; years with fewer than 6 reliable months also excluded.

**Trend analysis.** Annual mean water area (reliable months only) regressed against year via ordinary least squares (scipy.stats.linregress).

**Drought year definition.** A year is flagged as a drought year if its annual mean water area falls more than one standard deviation below the long-term coverage-filtered average.

**Terrain and drainage context.** A 30m SRTM DEM and the JRC water occurrence layer were combined in QGIS to map the Krishna River corridor connecting both reservoirs, with both dam locations marked. Rendered as a 2D map rather than a 3D scene — a 3D rendering was attempted but proved unreliable for this dataset within scope, and a correctly working 2D map was judged the more honest deliverable.

## Data Sources

| Data | Source | Resolution | Purpose |
|---|---|---|---|
| JRC Global Surface Water Monthly History v1.4 | European Commission Joint Research Centre, via Google Earth Engine | 30m | Monthly water classification, 1984-2021 |
| SRTM Global DEM | NASA, via Google Earth Engine | 30m | Terrain elevation for the Krishna River corridor |

## Repository Structure

```
scripts/
  dam_step1_water_history.py                  Initial JRC water area export (no coverage tracking) - superseded
  dam_step1b_water_history_with_coverage.py    JRC water area + coverage % export - final version
  dam_step2_trend_analysis.py                  Initial trend analysis, no coverage filtering - superseded
  dam_step2_trend_analysis_v2.py               Coverage-filtered trend analysis - final version
  dam_step3_terrain_data.py                    SRTM DEM + JRC water occurrence export for the terrain map
output/
  trend_NagarjunaSagar_v2.png
  trend_Srisailam_v2.png
  dam_comparison_v2.png
  annual_water_area_NagarjunaSagar_v2.csv
  annual_water_area_Srisailam_v2.csv
  dam_comparison_annual_v2.csv
maps/
  dam_terrain_map.png                          QGIS terrain/drainage context map, Krishna River corridor
reports/
  Dam_Monitoring_Technical_Report.docx
```

Raw monthly water area/coverage exports (`data/*.csv`) and the SRTM/water occurrence rasters (`data/*.tif`) are excluded from version control due to file size — fully reproducible by running the scripts in order against fresh Earth Engine exports.

## Tech Stack

Python (pandas, numpy, scipy, matplotlib), Google Earth Engine, QGIS, Git/GitHub.

## Author

**Manu Chauhan Mudavath**
MSc Computer Science — University of Waikato, New Zealand
MSc Information Systems — University of West London, UK
BTech — MGIT Hyderabad, India

[LinkedIn](https://linkedin.com/in/manu-chauhan-mudavath) · manuchauhanm76@gmail.com
