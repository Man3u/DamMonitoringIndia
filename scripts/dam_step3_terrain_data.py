import ee

ee.Initialize(project="floodmapping-506505")

# One AOI covering the full Krishna River corridor between the two reservoirs,
# not just each dam's footprint - this is what lets the 3D scene show the
# terrain relationship between them rather than two disconnected boxes.
corridor = ee.Geometry.Rectangle([78.15, 15.65, 79.50, 16.80])

# SRTM 30m elevation - this becomes the 3D scene's elevation surface, and also
# the input for deriving a drainage network inside ArcGIS Pro's Hydrology tools
dem = ee.Image("USGS/SRTMGL1_003").select("elevation").clip(corridor)

# JRC water occurrence: percent of time (1984-2021) each pixel was classified
# as water. This traces the permanent river channel and both reservoirs in a
# single layer, which drapes cleanly onto the terrain in ArcGIS
occurrence = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence").clip(corridor)

export_dem = ee.batch.Export.image.toDrive(
    image=dem,
    description="DEM_KrishnaCorridor",
    folder="DamMonitoringExports",
    fileNamePrefix="dem_krishna_corridor",
    region=corridor,
    scale=30,
    maxPixels=1e10,
)
export_dem.start()
print("Started export: DEM_KrishnaCorridor")

export_water = ee.batch.Export.image.toDrive(
    image=occurrence,
    description="WaterOccurrence_KrishnaCorridor",
    folder="DamMonitoringExports",
    fileNamePrefix="water_occurrence_krishna_corridor",
    region=corridor,
    scale=30,
    maxPixels=1e10,
)
export_water.start()
print("Started export: WaterOccurrence_KrishnaCorridor")

print("\nDone. Check https://code.earthengine.google.com/tasks")
print("Both exports cover the same 78.15-79.50E, 15.65-16.80N corridor, so they'll align in ArcGIS Pro.")
