"""
IMPORTANT!!!!
THIS SCRIPT NEEDS A DIFFERENT CONDA ENVIRONMENT THAN THE OTHER SCRIPTS!!!1

conda create -n mayavi-env
conda install -c conda-forge xarray  mayavi ipython netcdf4 pandas


"""
import xarray as xr
import pandas as pd
from mayavi import mlab
import __main__ as main

ifile = 'projected_tracks/imet/20220503/LOG06/track_converted.csv'

dem_file_nc = 'demdata/DEMsOfDiffFromBaseMapQaa_20192022julsept.nc'
# the dem file is in the EPSG:3413 projection, unit metres
dem = xr.open_dataset(dem_file_nc)

df = pd.read_csv(ifile)

dem_resolution = 10  # set to higher number if you run out of memory

# the DEM is in (y,x)
mlab.surf(dem['y'][::dem_resolution], dem['x'][::dem_resolution], dem['Band1'][::dem_resolution, ::dem_resolution])
mlab.plot3d(df['y'].values, df['x'].values, df['alt'].values, tube_radius=1, color=(0, 0, 0))
mlab.show()
