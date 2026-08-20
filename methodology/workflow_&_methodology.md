# Workflow and Methodology

This document details the step-by-step analytical workflow used for the Lar Block 2025 Flood Inundation and Susceptibility Assessment. The methodology integrates optical terrain data, microwave remote sensing, and spatial modeling.

---

## Phase 1: Hydrological Terrain Modeling
*Note: An initial trial using ALOS PALSAR was discarded due to transparent/NoData pixels that interrupted surface continuity. The workflow transitioned entirely to Copernicus DEM GLO-30.*

1. **Source Preparation:** Downloaded Copernicus DEM GLO-30 (30m).
2. **Geoprocessing:** Reprojected the DEM to the working CRS (EPSG:32644 - WGS 84/UTM Zone 44N) and clipped it to the Lar Block boundary.
3. **Hydrological Conditioning:** Applied **Depression Filling** to remove local sinks, creating a hydrologically connected surface for downslope routing.
4. **Terrain Derivatives (Generated using QGIS/GDAL):**
   * **Slope:** Derived continuous slope in degrees.
   * **Specific Catchment Area (SCA):** Routed flow across the filled surface to accumulate upstream contribution. 
   * **Topographic Wetness Index (TWI):** Calculated combining SCA and slope. Excluded zero/negative inputs to create a stable, corrected continuous TWI raster.

---

## Phase 2: SAR Data Preprocessing (ESA SNAP)
Flood mapping was performed using Sentinel-1A Level-1 IW GRDH dual-polarization (VV+VH) products for baseline (29 July 2025) and flood-period (31 August 2025). Both dates underwent identical preprocessing in ESA SNAP:

1. **Apply Orbit File:** Improved geometric state-vector information.
2. **Thermal Noise Removal:** Reduced additive sensor noise.
3. **Remove GRD Border Noise:** Cleaned low-intensity edge artifacts.
4. **Radiometric Calibration:** Generated Sigma0 VV and VH backscatter.
5. **Multi-temporal Speckle Filtering:** Reduced speckle noise across the paired dates.
6. **Range-Doppler Terrain Correction:** Orthorectified the imagery using the Copernicus GLO-30 DEM, outputting to a 10m grid.
7. **Linear to dB Conversion:** Converted Sigma0 to Decibels (dB) for classification.

---

## Phase 3: Automated Flood Classification (Python)
Instead of manual histogram thresholding, an automated approach was implemented using a custom Python script (utilizing GDAL and NumPy) run inside the QGIS Python Console.

1. **Outlier Control:** Retained the 0.5 to 99.5 percentile range of valid pixels to prevent extreme tails from skewing the data.
2. **Otsu Optimization:** Constructed a 512-bin histogram and maximized between-class variance to find the optimal water separation threshold.
3. **Calculated Thresholds (VV dB):**
   * **29 July 2025 (Baseline):** `-12.97 dB`
   * **31 August 2025 (Flood):** `-14.22 dB`
4. **Temporal Differencing:** Candidate new water was generated using a binary rule: `(August water = 1) AND (July water = 0)`.

---

## Phase 4: Spatial Filtering and Channel Masking
To ensure the final output represented true *overbank flooding on land* rather than normal river dynamics:

1. **Sieve Filtering:** Applied a **100-pixel connected-component sieve** to the candidate new water mask. This removed isolated patches smaller than ~1 hectare.
   * *Intermediate Result:* ~310 ha of water.
2. **Active Channel Exclusion:** A digitized polygon representing the pre-existing active river channel was masked out from the sieved result.
   * *Final Result:* **129.62 ha** of overbank inundation.

---

## Phase 5: Exposure and Susceptibility Modeling
1. **LULC Exposure:** The final 10m flood grid was overlaid with the ESRI 2025 Land Use/Land Cover dataset using categorical nearest-neighbor handling to calculate class-wise exposure (e.g., Agriculture/Crops).
2. **Zonal Statistics:** Extracted mean elevation, slope, TWI, and SCA values for flooded vs. non-flooded zones on their native grids.
3. **Weighted Susceptibility Model (WLC):** 
   * Created a Weighted Linear Combination (MCDA) surface with direct weights: **40% Elevation, 30% Slope, 20% SCA, and 10% TWI**.
   * Validation showed that 83.63% of observed flood pixels fell within the 'High' and 'Very High' susceptibility classes.
