

## uav analysis requirements
```commandline
conda create -n uav-analysis-env
conda activate uav-analysis-env
conda install ipython numpy pandas seaborn matplotlib xarray rasterio
pip install pyulog rioxarray
```



### 3d visualizations
I tried mayavi http://docs.enthought.com/mayavi/mayavi/mlab.html#simple-scripting-with-mlab, but I didnt
get it running together with the other dependencies, and I gave up.

Now simply matplotlib 3d is used.