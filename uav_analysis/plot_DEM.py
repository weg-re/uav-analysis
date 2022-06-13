import xarray as xr
import matplotlib

matplotlib.use('QT5Agg')
from pylab import plt
import numpy as np
import pyproj
from mpl_toolkits import mplot3d

dem_file = 'demdata/DEMsOfDiffFromBaseMapQaa_20192022julsept.tif'
# the dem file is in the EPSG:3413 projection, unit metres
dem = xr.open_dataset(dem_file, engine='rasterio')

print('projection:', dem.rio.crs)
print('unit:', dem.rio.crs.linear_units)

# convert the  DEM to lat lon coordinates
# note that this introduces some infinite values, so it is probably not very useful
# for us
latlon = dem.rio.reproject("EPSG:4326")

# converting latlons to the coordinate system of the height model

transformer = pyproj.Transformer.from_crs("epsg:4326", str(dem.rio.crs))
lat = 70
lon = -51

x, y = transformer.transform(lat, lon)

# 3d plot of surface


fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection='3d')
ax.grid()
x = dem['x']
y = dem['y']
X, Y = np.meshgrid(x, y)
ax.plot_surface(X, Y, dem['band_data'][0])
ax.set_box_aspect((1, 1, 0.2))
plt.savefig('plots/DEM_3dlot.svg')

# fig = plt.figure(figsize=(8, 8))
# ax = plt.axes(projection='3d')
# ax.grid()
# x = latlon['x']
# y = latlon['y']
# X, Y = np.meshgrid(x, y)
# ax.plot_surface(X, Y, latlon['band_data'][0])
