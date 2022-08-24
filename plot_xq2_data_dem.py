import os
from pathlib import Path
import __main__ as main
import argparse
import pandas as pd
import numpy as np
from pylab import plt
import xarray as xr
import pyproj

from read_uav_data import read_xq2_data

intaractive = not hasattr(main, '__file__')


parser = argparse.ArgumentParser()
parser.add_argument('ifile', type=str, help='filename of xq2 log (csv file)')

if intaractive:
    ifile = 'data/XQ2/by_flight/20220706/20220706-1.csv'
else:
    args = parser.parse_args()
    ifile = args.ifile

# plotdir = f'plots/{os.path.splitext(ifile)[0]}'
plotdir = f'plots/xq2/'
plot_base_name = Path(ifile).stem
os.makedirs(plotdir, exist_ok=True)

# read DEM data
dem_file = 'demdata/DEMsOfDiffFromBaseMapQaa_20192022julsept.tif'
# the dem file is in the EPSG:3413 projection, unit metres
dem = xr.open_dataset(dem_file, engine='rasterio')

df = read_xq2_data(ifile)

df.rename(columns={'Longitude': 'lon', 'Latitude': 'lat', 'Altitude': 'alt',
                   'Air Temperature': 'T'}, inplace=True)


# compute height above ground (with DEM model)
transformer = pyproj.Transformer.from_crs("epsg:4326", str(dem.rio.crs))
reverse_transformer = pyproj.Transformer.from_crs(str(dem.rio.crs), "epsg:4326")
# convert lat and lon to coordinates of DEM
x, y = transformer.transform(df['lat'], df['lon'])
df['x'] = x
df['y'] = y
# get the corresponding height (linearly interpolated)
df['z_dem'] = dem['band_data'][0].interp(x=('z', x), y=('z', y)).values
df['alt_over_ground'] = df['alt']


n_vars = df.shape[1]

plt.figure(figsize=(10, 20))
for i in range(n_vars):
    plt.subplot(n_vars, 1, i + 1)
    plt.plot(df[df.keys()[i]])
    plt.ylabel(df.keys()[i])
plt.savefig(f'{plotdir}/time_vs_vars_{plot_base_name}.svg')
plt.savefig(f'{plotdir}/time_vs_vars_{plot_base_name}.png')

plt.figure(figsize=(30, 10))
for i in range(n_vars):
    plt.subplot(1, n_vars, i + 1)
    plt.plot(df[df.keys()[i]].values, df['alt'], marker='x')
    plt.xlabel(df.keys()[i])
    plt.ylabel('alt')
plt.savefig(f'{plotdir}/alt_vs_vars_{plot_base_name}.svg')
plt.savefig(f'{plotdir}/alt_vs_vars_{plot_base_name}.png')

varname = "T"
fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection='3d')
ax.grid()
ax.plot3D(df['lon'], df['lat'], df['alt'])
cf = ax.scatter(df['lon'], df['lat'], df['alt'], c=df[varname], cmap=plt.cm.Reds)
ax.set_xlabel('lon')
ax.set_ylabel('lat')
ax.set_zlabel('alt')
ax.set_box_aspect((1, 1, 0.5))
cb = plt.colorbar(cf)
cb.set_label(varname)
plt.savefig(f'{plotdir}/imet-3D-lat-lon-alt-{varname}_{plot_base_name}.svg')
# with vixed x and y extend
dlat = 0.008
dlon = 0.008
lon_center = 1/2*(df['lon'].min()+df['lon'].max())
lat_center = 1/2*(df['lat'].min()+df['lat'].max())
plt.xlim(lon_center-dlon, lon_center+dlon)
plt.ylim(lat_center-dlat, lat_center+dlat)
plt.savefig(f'{plotdir}/imet-3D-lat-lon-alt-{varname}_fixedscale_{plot_base_name}.svg')

# 3d plot with x,y and height countours from DEM
# create grid for plotting DEM
X_dem, Y_dem = np.meshgrid(dem['x'], dem['y'])
fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection='3d')
ax.grid()
# the DEM is (y,x)
ax.plot_surface(Y_dem[::20,::20], X_dem[::20,::20], dem['band_data'][0][::20,::20], alpha=0.6)
ax.plot3D(df['y'], df['x'], df['alt'])
if varname != 'position':
    cf = ax.scatter(df['y'], df['x'], df['alt'], c=df[varname], cmap=plt.cm.Reds)
ax.set_xlabel('y')
ax.set_ylabel('x')
ax.set_zlabel('alt')
# set initial 3d view
# ax.view_init(azim=-165, elev=11)
# make scale of height smaller
ax.set_box_aspect((1, 1, 0.5))
cb = plt.colorbar(cf)
cb.set_label(varname)
plt.savefig(f'{plotdir}/imet-3D-x-y-alt-DEM-{varname}_{plot_base_name}.svg')
