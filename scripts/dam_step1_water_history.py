import ee

ee.Initialize(project="floodmapping-506505")

DAMS = {
    "NagarjunaSagar": ee.Geometry.Rectangle([79.05, 16.45, 79.45, 16.75]),
    "Srisailam": ee.Geometry.Rectangle([78.20, 15.70, 78.95, 16.30]),
}

gsw_monthly = ee.ImageCollection("JRC/GSW1_4/MonthlyHistory")
count = gsw_monthly.size().getInfo()
first_date = ee.Image(gsw_monthly.first()).date().format("YYYY-MM").getInfo()
last_date = ee.Image(gsw_monthly.sort("system:time_start", False).first()).date().format("YYYY-MM").getInfo()
print(f"JRC Monthly History: {count} images, {first_date} to {last_date}")

pixel_area_ha = ee.Image.pixelArea().divide(10000)

for name, aoi in DAMS.items():
    def compute_water_area(img):
        water_mask = img.select("water").eq(2)
        area = pixel_area_ha.updateMask(water_mask).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=30,
            maxPixels=1e10,
        ).get("area")
        return ee.Feature(None, {
            "date": img.date().format("YYYY-MM"),
            "water_area_ha": area,
        })

    fc = ee.FeatureCollection(gsw_monthly.map(compute_water_area))

    task = ee.batch.Export.table.toDrive(
        collection=fc,
        description=f"WaterArea_{name}",
        folder="DamMonitoringExports",
        fileNamePrefix=f"water_area_{name}",
        fileFormat="CSV",
    )
    task.start()
    print(f"Started export: WaterArea_{name}")

print("\nDone. Check https://code.earthengine.google.com/tasks")
print("Note: this export processes ~40 years of monthly data per dam, so it may take longer than previous exports.")
