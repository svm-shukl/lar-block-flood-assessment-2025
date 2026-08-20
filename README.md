# Integrated Flood Inundation & Susceptibility Assessment - Lar Block (2025)

## 📌 Project Overview
This repository contains the complete GIS and remote-sensing workflow for assessing flood inundation in the Lar Block of Deoria District, Uttar Pradesh[cite: 1]. The project utilizes a continuous hydrological terrain framework built from the Copernicus DEM GLO-30 and maps baseline and flood-period water using dual-date Sentinel-1 SAR imagery[cite: 1]. 

The primary aim is to map overbank inundation during the 2025 monsoon period, quantify exposed land cover, and evaluate a weighted topographic susceptibility surface[cite: 1].

---

## 🚀 Core Results
* **Overbank Inundation:** Successfully mapped **129.62 ha** of landward overbank inundation after excluding the pre-existing active river channel[cite: 1].
* **Agricultural Exposure:** Agriculture/Crops form the dominant exposed land cover, accounting for **80.74 ha (62.29%)** of the flooded area[cite: 1].
* **Hydrological Consistency:** Analysis confirms flooding is concentrated on lower elevations, with higher Topographic Wetness Index (TWI) and Specific Catchment Area (SCA)[cite: 1].
* **Validation:** The resulting inundated area closely aligns in magnitude with the 125.76 ha reported by the Flood Management Information System Centre (FMISC) for 19 August 2025[cite: 1].

---

## 🛠️ Data & Tech Stack
* **Terrain Source:** Copernicus DEM GLO-30 (30 m), reprojected, clipped, and depression-filled[cite: 1].
* **SAR Observations:** Sentinel-1A IW GRDH (dual VV+VH) observations dated 29 July and 31 August 2025[cite: 1].
* **Land Cover:** ESRI 2025 LULC (10 m categorical raster)[cite: 1].
* **Software/Tools:** 
  * **ESA SNAP:** SAR preprocessing including orbit correction, thermal noise removal, calibration, speckle filtering, and terrain correction[cite: 1].
  * **QGIS + GDAL + NumPy:** Raster modeling, zonal statistics, sieving, overlays, and executing Python scripts[cite: 1].

---

## 🧠 Methodology Highlights
1. **Hydrological Modeling:** Developed elevation, slope, TWI, and SCA surfaces directly from the hydrologically conditioned Copernicus DEM to avoid spatial discontinuities[cite: 1].
2. **Automated Otsu Thresholding:** Implemented a custom Python script using GDAL to compute automated VV dB thresholds (-12.97 dB for July and -14.22 dB for August) without manual histogram picking[cite: 1].
3. **Temporal Differencing & Filtering:** Candidate new water was isolated by differencing the August and July masks, followed by a 100-pixel connected-component sieve filter to remove isolated patches[cite: 1].
4. **Channel Exclusion:** A digitized polygon representing the pre-existing active river channel was masked out to ensure the analysis strictly targeted overbank flooding on land[cite: 1].

---

## 📁 Repository Structure
* `docs/` - Contains the primary final analytical and cartographic documentation (e.g., `Lar_Block_2025.pdf`)[cite: 1].
* `scripts/` - Python scripts for automated Otsu thresholding implemented via the QGIS Python console[cite: 1].
* `maps/` - Exported high-resolution maps from the project's cartographic portfolio (e.g., Copernicus-Derived Slope, Final Overbank Flood, Susceptibility Maps)[cite: 1].
* `workflows/` - ESA SNAP graph builder sequences for repeatable SAR preprocessing steps[cite: 1].

---

## ⚙️ How to Use
The automated Otsu thresholding code provided in the `scripts/` directory is designed to be executed within the **QGIS Python Console**[cite: 1]. It utilizes the `qgis.core` and `osgeo.gdal` libraries to read loaded VV dB layers, handles NoData/outliers using the 0.5-99.5 percentile range, and dynamically calculates threshold values[cite: 1].
