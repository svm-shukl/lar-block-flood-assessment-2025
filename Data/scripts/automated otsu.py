import numpy as np 
from osgeo import gdal 
from qgis.core import QgsProject 
  
# Get loaded VV dB layer 
layer = QgsProject.instance().mapLayersByName('July_VV_dB')[0] 
path = layer.source() 
  
# Read raster 
ds = gdal.Open(path) 
band = ds.GetRasterBand(1) 
arr = band.ReadAsArray().astype(np.float32) 
  
# Remove NoData, NaN and infinite values 
nodata = band.GetNoDataValue() 
valid = np.isfinite(arr) 
if nodata is not None: 
    valid &= (arr != nodata) 
values = arr[valid] 
  
# Remove extreme outliers using 0.5-99.5 percentile 
low, high = np.percentile(values, [0.5, 99.5]) 
values = values[(values >= low) & (values <= high)] 
  
# Histogram 
hist, edges = np.histogram(values, bins=512) 
centers = (edges[:-1] + edges[1:]) / 2.0 
  
# Otsu calculation 
hist = hist.astype(np.float64) 
prob = hist / hist.sum() 
omega = np.cumsum(prob) 
mu = np.cumsum(prob * centers) 
mu_total = mu[-1] 
  
sigma_b = (mu_total * omega - mu) ** 2 / ( 
    omega * (1.0 - omega) + 1e-12 
) 
  
idx = np.argmax(sigma_b) 
threshold = centers[idx] 
  
print('--------------------------------') 
print('AUTOMATIC OTSU RESULT') 
print('--------------------------------') 
print(f'Valid pixels: {len(values):,}') 
print(f'Analysis range: {low:.2f} to {high:.2f} dB') 
print(f'Otsu threshold: {threshold:.2f} dB') 
print('--------------------------------')
