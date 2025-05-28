# Flood-Risk-Modeling

# 🌊 Flood Risk Mapping Using AHP and ArcPy

This guide explains how to perform flood risk mapping using the Analytical Hierarchy Process (AHP) and ArcPy in ArcGIS. It is written in a simple, step-by-step format to help other researcher to replicate the process.

---

## 🧰 Step 1: Prepare Your Input Files

You need the following raster and vector datasets:

- **DEM (Digital Elevation Model)** – Terrain elevation data.
- **River shapefile** – River locations.
- **Land use map** – Types of land cover.
- **Soil map** – Soil types.
- **Rainfall map** – Rain distribution.

All should be projected and aligned properly.

---

## 🧗 Step 2: Extract Maps from DEM

From the DEM, generate:

- **Slope map** – Indicates steepness.
- **Elevation map** – Already present in the DEM.
- **Distance to river map** – Calculated using `Euclidean Distance` tool.

---

## 📊 Step 3: Reclassify Each Map

Convert values in each map to a 1–5 scale:

| Value Range      | Risk Score |
|------------------|------------|
| Flat or Low Area | 5          |
| Steep or High    | 1          |

Reclassify for:
- Slope
- Elevation
- Distance to river
- Land use
- Soil type
- Rainfall

---

## ⚖️ Step 4: Assign Weights (AHP)

Assign importance to each factor. Example:

| Factor            | Weight (%) |
|-------------------|------------|
| Slope             | 20%        |
| Elevation         | 20%        |
| Distance to river | 20%        |
| Land use          | 15%        |
| Rainfall          | 15%        |
| Soil type         | 10%        |

---

## 🧮 Step 5: Create a Suitability Map

Multiply each layer by its weight and sum them:

```python
suitability = (
    slope_reclass * 0.2 +
    elevation_reclass * 0.2 +
    distance_reclass * 0.2 +
    landuse_reclass * 0.15 +
    soil_reclass * 0.1 +
    rainfall_reclass * 0.15
)
```

---

## 🚦 Step 6: Classify Final Risk Zones

Reclassify the suitability score into zones:

| Score Range | Flood Risk   |
|-------------|--------------|
| 1.0 – 2.0   | Very Low     |
| 2.0 – 3.0   | Low          |
| 3.0 – 4.0   | Moderate     |
| 4.0 – 5.0   | High         |
| 5.0 – 6.0   | Very High    |

---

## ✅ Output

- `Flood_Suitability.tif` – Continuous flood risk score.
- `Flood_Risk_Zones.tif` – Classified flood risk zones.

---

## 📦 Suggested Folder Structure

```
C:\FloodModel\Workspace\
    ├── DEM.tif
    ├── river.shp
    ├── landuse.tif
    ├── soil.tif
    ├── rainfall.tif
```

Make sure to update paths in your script:

```python
arcpy.env.workspace = r"C:\FloodModel\Workspace"
```

---

## 🧠 Summary

Flood risk mapping with AHP is about:
1. Preparing and deriving input data
2. Standardizing layers
3. Applying weights
4. Combining and classifying results

Use this guide to build a practical, GIS-based flood risk model.
