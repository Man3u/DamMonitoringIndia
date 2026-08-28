import ee

ee.Initialize(project="floodmapping-506505")

DAMS = {
    "NagarjunaSagar": ee.Geometry.Rectangle([79.05, 16.45, 79.45, 16.75]),
    "Srisailam": ee.Geometry.Rectangle([78.20, 15.70, 78.95, 16.30]),
}

gsw_monthly = ee.ImageCollection("JRC/GSW1_4/MonthlyHistory")
pixel_area_ha = ee.Image.pixelArea().divide(10000)

for name, aoi in DAMS.items():
    aoi_total_ha = aoi.area().divide(10000)

    def compute_water_area(img):
        water_band = img.select("water")
        water_mask = water_band.eq(2)
        valid_mask = water_band.gt(0)

        water_area = pixel_area_ha.updateMask(water_mask).reduceRegion(
            reducer=ee.Reducer.sum(), geometry=aoi, scale=30, maxPixels=1e10,
        ).get("area")

        valid_area = pixel_area_ha.updateMask(valid_mask).reduceRegion(
            reducer=ee.Reducer.sum(), geometry=aoi, scale=30, maxPixels=1e10,
        ).get("area")

        pct_valid = ee.Number(valid_area).divide(aoi_total_ha).multiply(100)

        return ee.Feature(None, {
            "date": img.date().format("YYYY-MM"),
            "water_area_ha": water_area,
            "pct_valid_coverage": pct_valid,
        })

    fc = ee.FeatureCollection(gsw_monthly.map(compute_water_area))

    task = ee.batch.Export.table.toDrive(
        collection=fc,
        description=f"WaterAreaWithCoverage_{name}",
        folder="DamMonitoringExports",
        fileNamePrefix=f"water_area_coverage_{name}",
        fileFormat="CSV",
    )
    task.start()
    print(f"Started export: WaterAreaWithCoverage_{name}")

print("\nDone. Check https://code.earthengine.google.com/tasks")
