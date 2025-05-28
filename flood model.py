#-------------------------------------------------------------------------------
# Name:        Flood risk Modeling
# Purpose:
#
# Author:      OPEJINA22
#
# Created:     28/05/2025
# Copyright:   (c) OPEJINA22 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy.sa import *

# Enable Spatial Analyst
arcpy.CheckOutExtension("Spatial")

# Set environment
arcpy.env.workspace = r"C:\FloodModel\Workspace"
arcpy.env.overwriteOutput = True

# ------------------------------
# Step 1: Load base input files
# ------------------------------
dem = Raster("DEM.tif")
river = "river.shp"
landuse = Raster("landuse.tif")
soil = Raster("soil.tif")
rainfall = Raster("rainfall.tif")

# ------------------------------
# Step 2: Derive layers from DEM
# ------------------------------
# Derive slope (in degrees)
slope = Slope(dem, output_measurement="DEGREE")
slope.save("slope.tif")

# Distance to river
river_distance = EucDistance(river)
river_distance.save("distance_to_river.tif")

# Elevation
# Already available in DEM
elevation = dem

# ------------------------------
# Step 3: Reclassify layers (1–5)
# Customize ranges to your study area
# ------------------------------
slope_reclass = Reclassify(slope, "Value", RemapRange([[0, 5, 5], [5, 15, 4], [15, 25, 3], [25, 35, 2], [35, 90, 1]]))
elevation_reclass = Reclassify(elevation, "Value", RemapRange([[0, 10, 5], [10, 50, 4], [50, 100, 3], [100, 200, 2], [200, 10000, 1]]))
distance_reclass = Reclassify(river_distance, "Value", RemapRange([[0, 100, 5], [100, 300, 4], [300, 600, 3], [600, 1000, 2], [1000, 5000, 1]]))

landuse_reclass = Reclassify(landuse, "Value", RemapValue({1: 5, 2: 4, 3: 3, 4: 2, 5: 1}))  # Adjust class codes as needed
soil_reclass = Reclassify(soil, "Value", RemapValue({1: 5, 2: 3, 3: 1}))
rainfall_reclass = Reclassify(rainfall, "Value", RemapRange([[0, 50, 1], [50, 100, 2], [100, 150, 3], [150, 200, 4], [200, 300, 5]]))

# ------------------------------
# Step 4: AHP Weights (example)
# ------------------------------
weights = {
    "slope": 0.2,
    "elevation": 0.2,
    "distance": 0.2,
    "landuse": 0.15,
    "soil": 0.1,
    "rainfall": 0.15
}

# ------------------------------
# Step 5: Weighted overlay
# ------------------------------
suitability = (
    slope_reclass * weights["slope"] +
    elevation_reclass * weights["elevation"] +
    distance_reclass * weights["distance"] +
    landuse_reclass * weights["landuse"] +
    soil_reclass * weights["soil"] +
    rainfall_reclass * weights["rainfall"]
)

suitability.save("Flood_Suitability.tif")

# ------------------------------
# Step 6: Reclassify final map into flood risk zones
# ------------------------------
risk_map = Reclassify(suitability, "Value", RemapRange([[1, 2, 1], [2, 3, 2], [3, 4, 3], [4, 5, 4], [5, 6, 5]]))  # 1=Very Low, 5=Very High
risk_map.save("Flood_Risk_Zones.tif")

print("Flood risk map and zones generated successfully.")
