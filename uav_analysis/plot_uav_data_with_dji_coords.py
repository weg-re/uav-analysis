"""
TODO NOT YET FINISHED!!!!
script for plotting imet data combined with dji position data

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
parser.add_argument('imet_file', type=str, help='filename of imet log (e.g. LOG06.txt)')
parser.add_argument('dji_file', type=str)

if intaractive:
    imet_file = "imet/20220503/LOG06.txt"
    ifile_dq = 'dji/11_31_28.ulg'
else:
    args = parser.parse_args()
    imet_file = args.flight_number_imet
    ifile_dq = args.flight_number_deltaquad

plotdir = f'plots/{os.path.splitext(imet_file)[0]}'
os.makedirs(plotdir, exist_ok=True)

df_imet_raw = read_imet_data(imet_file)

# remove duplicates
duplicate_pos, = np.where(df_imet_raw['datetime'].duplicated())
df_imet_raw = df_imet_raw.groupby('datetime').head(1).reset_index()
df_imet_raw = df_imet_raw.drop('index', axis=1)

assert (~df_imet_raw['datetime'].duplicated().any())


# FINISH!!!!1