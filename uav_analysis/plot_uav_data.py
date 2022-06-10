"""
script for plotting imet data, and optionally combining it with deltaquad position data.

@author: Sebastian Scher
May 2022
"""
import os
import argparse

import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('agg')
from pylab import plt
import xarray as xr
import pyproj
from mpl_toolkits import mplot3d

import __main__ as main

from read_uav_data import read_imet_data, read_deltaquad_position_data

intaractive = not hasattr(main, '__file__')

parser = argparse.ArgumentParser()
parser.add_argument('imet_file', type=str, help='filename of imet log (e.g. LOG06.txt)')
parser.add_argument('deltaquad_file', type=str,
                    help='optional. number of deltaquad log (e.g. 11_31_28.ulg)',
                    default='none', nargs='?')

hack_shift_coordinats_to_quaamarujuk = False

if intaractive:
    imet_file = "imet/20220503/LOG06.txt"
    ifile_dq = 'deltaquad/11_31_28.ulg'
else:
    args = parser.parse_args()
    imet_file = args.imet_file
    ifile_dq = args.deltaquad_file

plotdir = f'plots/{os.path.splitext(imet_file)[0]}'
os.makedirs(plotdir, exist_ok=True)

# read DEM data
dem_file = 'demdata/DEMsOfDiffFromBaseMapQaa_20192022julsept.tif'
# the dem file is in the EPSG:3413 projection, unit metres
dem = xr.open_dataset(dem_file, engine='rasterio')

df_imet_raw = read_imet_data(imet_file)

# remove duplicates
duplicate_pos, = np.where(df_imet_raw['datetime'].duplicated())
df_imet_raw = df_imet_raw.groupby('datetime').head(1).reset_index()
df_imet_raw = df_imet_raw.drop('index', axis=1)

assert (~df_imet_raw['datetime'].duplicated().any())

plt.figure()
plt.scatter(df_imet_raw['lon'], df_imet_raw['lat'], c=df_imet_raw['t'])
plt.colorbar()
plt.savefig(f'{plotdir}/imet-lat-lon-p.svg')

n_vars = df_imet_raw.shape[1]
plt.figure(figsize=(10, 20))
for i in range(n_vars):
    plt.subplot(n_vars, 1, i + 1)
    plt.plot(df_imet_raw[df_imet_raw.keys()[i]])
    plt.ylabel(df_imet_raw.keys()[i])
plt.xlabel('step')
plt.savefig(f'{plotdir}/imet-overviewplot.svg')
plt.savefig(f'{plotdir}/imet-overviewplot.png')

# remove all "weird" lat and lons
df = df_imet_raw.query('lon > 180')
plt.figure()
plt.scatter(df['lon'], df['lat'], c=df['alt'])
cb = plt.colorbar()
cb.set_label('alt')
plt.plot(df['lon'], df['lat'])
plt.savefig(f'{plotdir}/imet-lat-lon-alt_imetvalidcoords.svg')

fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection='3d')
ax.grid()
ax.plot3D(df['lon'], df['lat'], df['alt'])
cf = ax.scatter(df['lon'], df['lat'], df['alt'], c=df['t'], cmap=plt.cm.Reds)
ax.set_xlabel('lon')
ax.set_ylabel('lat')
ax.set_zlabel('alt')
cb = plt.colorbar(cf)
cb.set_label('t')
plt.savefig(f'{plotdir}/imet-3D-lat-lon-alt-t_imetvalidcoords.svg')

n_vars = df.shape[1]
plt.figure(figsize=(10, 20))
for i in range(n_vars):
    plt.subplot(n_vars, 1, i + 1)
    plt.plot(df[df.keys()[i]])
    plt.ylabel(df.keys()[i])
plt.xlabel('step')
plt.savefig(f'{plotdir}/imet-overviewplot-imetvalidcoords.svg')
plt.savefig(f'{plotdir}/imet-overviewplot-imetvalidcoords.png')

# height vs variables

plt.figure(figsize=(30, 10))
for i in range(n_vars):
    plt.subplot(1, n_vars, i + 1)
    plt.plot(df[df.keys()[i]].values, df['alt'], marker='x')
    plt.xlabel(df.keys()[i])
    plt.ylabel('alt')
plt.savefig(f'{plotdir}/alt_vs_vars_imetvalidcoords.svg')
plt.savefig(f'{plotdir}/alt_vs_vars_imetvalidcoords.png')

# read in corresponding deltaquad file
if ifile_dq != 'none':

    dq_converted_folder = os.path.splitext(ifile_dq)[0]
    res = os.system(f'ulog2csv  -o {dq_converted_folder} {ifile_dq}')
    if res != 0:
        raise Exception('ulog conversion failed!')

    # the converted files start with the original filename (without parent folders)
    base_filename_dq_no_ext = os.path.splitext(os.path.basename(ifile_dq))[0]
    dw_converted_file = f'{dq_converted_folder}/{base_filename_dq_no_ext}_vehicle_gps_position_0.csv'
    df_dq_raw = read_deltaquad_position_data(dw_converted_file, round_time='1s')
    df_dq_raw = df_dq_raw.drop('index', axis=1)
    # find common datetimes
    common_dates = pd.Series(list(set(df_dq_raw['datetime']) & set(df_imet_raw['datetime'])))

    df_imet = df_imet_raw[df_imet_raw['datetime'].isin(common_dates)].reset_index()
    df_dq = df_dq_raw[df_dq_raw['datetime'].isin(common_dates)].reset_index()
    assert (len(df_imet) == len(df_dq))

    # merge dq position into imet data
    df_merged = df_imet.copy().drop('index', axis=1)
    df_merged['lat_uav'] = df_dq['lat'] / 1e7
    df_merged['lon_uav'] = df_dq['lon'] / 1e7
    df_merged['alt_uav'] = df_dq['alt'] / 1e3

    # TODO START HACK
    if hack_shift_coordinats_to_quaamarujuk:
        print("WARNING!!! HACK!!! COORDINATES CHANGED!!! ONLY FOR TESTING!!!!")
        target_lat = 71.172
        target_lon = -51.1
        # TODO: there is a problem her with precision, the small variations in lon and lat just vanish...
        df_merged['lat_uav'] = df_merged['lat_uav'][0] - (df_merged['lat_uav'] - target_lat)
        df_merged['lon_uav'] = df_merged['lon_uav'][0] - (df_merged['lon_uav'] - target_lon)

    # END START HACK
    # compute height above ground
    transformer = pyproj.Transformer.from_crs("epsg:4326", str(dem.rio.crs))
    reverse_transformer = pyproj.Transformer.from_crs(str(dem.rio.crs), "epsg:4326")
    # convert lat and lon to coordinates of DEM
    x, y = transformer.transform(df_merged['lat_uav'], df_merged['lon_uav'])
    # get the corresponding height (linearly interpolated)
    df_merged['z_dem'] =  dem['band_data'][0].interp(x=('z',x),y=('z',y)).values
    df_merged['alt_over_ground'] = df_merged['alt_uav'] - df_merged['z_dem']


# combined plots

df = df_merged
n_vars = df.shape[1]
plt.figure(figsize=(7, 20))
for i in range(n_vars):
    plt.subplot(n_vars, 1, i + 1)
    plt.plot(df[df.keys()[i]])
    plt.ylabel(df.keys()[i])
plt.xlabel('step')
plt.savefig(f'{plotdir}/imet-overviewplot_uavcoords.svg')
plt.savefig(f'{plotdir}/imet-overviewplot_uavcoords.png')

fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection='3d')
ax.grid()
ax.plot3D(df['lon_uav'], df['lat_uav'], df['alt_uav'])
cf = ax.scatter(df['lon_uav'], df['lat_uav'], df['alt_uav'], c=df['t'], cmap=plt.cm.Reds)
ax.set_xlabel('lon_uav')
ax.set_ylabel('lat_uav')
ax.set_zlabel('alt_uav')
cb = plt.colorbar(cf)
cb.set_label('t')
plt.savefig(f'{plotdir}/imet-3D-lat-lon-alt-t_uavcoords.svg')

plt.figure()
plt.subplot(221)
plt.scatter(df['lat'], df['lat_uav'])
plt.xlabel('lat imet')
plt.ylabel('lat uav')
plt.subplot(222)
plt.scatter(df['lon'], df['lon_uav'])
plt.xlabel('lon imet')
plt.ylabel('lon uav')
plt.subplot(223)
plt.scatter(df['alt'], df['alt_uav'])
plt.xlabel('alt imet')
plt.ylabel('alt uav')
plt.savefig(f'{plotdir}/imet-imetcoord_vs_uavcoords.svg')

# height vs variables

plt.figure(figsize=(30, 10))
for i in range(n_vars):
    plt.subplot(1, n_vars, i + 1)
    plt.plot(df[df.keys()[i]].values, df['alt_uav'])
    plt.xlabel(df.keys()[i])
    plt.ylabel('alt uav')
plt.savefig(f'{plotdir}/alt_vs_vars_uavcoords.svg')
plt.savefig(f'{plotdir}/alt_vs_vars_uavcoords.png')
