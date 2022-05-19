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
from mpl_toolkits import mplot3d

import __main__ as main

from read_uav_data import read_imet_data, read_deltaquad_position_data

intaractive = not hasattr(main, '__file__')

parser = argparse.ArgumentParser()
parser.add_argument('date', type=str, help='date (=foldername) of imet')
parser.add_argument('flight_number_imet', type=str, help='filename of imet log (e.g. LOG06)')
parser.add_argument('flight_number_deltaquad', type=str,
                    help='optional. number of deltaquad log (without .ulg extension), placed in ./data/'
                         ' of deltaquad log (e.g. 11_31_28)',
                    default='none', nargs='?')

if intaractive:
    date = '20220503'
    flight_number_imet = "LOG06"
    flight_nnumber_deltaquad = '11_31_28'
else:
    args = parser.parse_args()
    date = args.date
    flight_number_imet = args.flight_number_imet
    flight_nnumber_deltaquad = args.flight_number_deltaquad

plotdir = f'plots/{date}/{flight_number_imet}'
os.makedirs(plotdir, exist_ok=True)

ifile = f'{date}/{flight_number_imet}.txt'
ifile_dq = f'data/{flight_nnumber_deltaquad}/{flight_nnumber_deltaquad}_vehicle_gps_position_0.csv'

df_imet_raw = read_imet_data(ifile)

# remove duplicates
duplicate_pos, = np.where(df_imet_raw['datetime'].duplicated())
df_imet_raw = df_imet_raw.groupby('datetime').head(1).reset_index()

assert (~df_imet_raw['datetime'].duplicated().any())

plt.figure()
plt.scatter(df_imet_raw['lon'], df_imet_raw['lat'], c=df_imet_raw['t'])
plt.colorbar()
plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-lat-lon-p.svg')

n_vars = df_imet_raw.shape[1]
plt.figure(figsize=(10, 20))
for i in range(n_vars):
    plt.subplot(n_vars, 1, i + 1)
    plt.plot(df_imet_raw[df_imet_raw.keys()[i]])
    plt.ylabel(df_imet_raw.keys()[i])
plt.xlabel('step')
plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-overviewplot.svg')
plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-overviewplot.png')

# remove all "weird" lat and lons
df = df_imet_raw.query('lon > 180')
plt.figure()
plt.scatter(df['lon'], df['lat'], c=df['alt'])
cb = plt.colorbar()
cb.set_label('alt')
plt.plot(df['lon'], df['lat'])
plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-lat-lon-alt_imetvalidcoords.svg')

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
plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-3D-lat-lon-alt-t_imetvalidcoords.svg')

n_vars = df.shape[1]
plt.figure(figsize=(10, 20))
for i in range(n_vars):
    plt.subplot(n_vars, 1, i + 1)
    plt.plot(df[df.keys()[i]])
    plt.ylabel(df.keys()[i])
plt.xlabel('step')
plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-overviewplot-imetvalidcoords.svg')
plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-overviewplot-imetvalidcoords.png')

# read in corresponding deltaquad file
if flight_nnumber_deltaquad != 'none':

    res = os.system(f'ulog2csv  -o data/{flight_nnumber_deltaquad} data/{flight_nnumber_deltaquad}.ulg')
    if res != 0:
        raise Exception('ulog conversion failed!')
    df_dq_raw = read_deltaquad_position_data(ifile_dq, round_time='1s')

    # find common datetimes
    common_dates = pd.Series(list(set(df_dq_raw['datetime']) & set(df_imet_raw['datetime'])))

    df_imet = df_imet_raw[df_imet_raw['datetime'].isin(common_dates)].reset_index()
    df_dq = df_dq_raw[df_dq_raw['datetime'].isin(common_dates)].reset_index()
    assert (len(df_imet) == len(df_dq))

    # merge dq position into imet data
    df_merged = df_imet.copy()
    df_merged['lat_uav'] = df_dq['lat'] / 1e7
    df_merged['lon_uav'] = df_dq['lon'] / 1e7
    df_merged['alt_uav'] = df_dq['alt'] / 1e3

    # combined plots

    df = df_merged
    n_vars = df.shape[1]
    plt.figure(figsize=(7, 20))
    for i in range(n_vars):
        plt.subplot(n_vars, 1, i + 1)
        plt.plot(df[df.keys()[i]])
        plt.ylabel(df.keys()[i])
    plt.xlabel('step')
    plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-overviewplot_uavcoords.svg')
    plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-overviewplot_uavcoords.png')

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
    plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-3D-lat-lon-alt-t_uavcoords.svg')

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
    plt.savefig(f'{plotdir}/{date}-{flight_number_imet}-imetcoord_vs_uavcoords.svg')
