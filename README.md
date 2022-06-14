

## uav analysis requirements
to install the requirements, you need miniconda (https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)
. after you install miniconda, run the following commands
(on linux/macos in the terminal, on windows in the miniconda prompt)
```commandline
conda create -n uav-analysis-env
conda activate uav-analysis-env
conda install ipython numpy pandas seaborn matplotlib xarray rasterio
pip install pyulog rioxarray
```

## converting uav data
We have two different measurements:
* Deltaquad drone with Imet sensor. the imet sensor has problems with the positions, therefore we also use the drone
  position data
* DJI Drone with XQ2 sensor
Deltaquad data needs to be provided in the original .ulg file as input

XQ2 data needs to be in .csv format (exported from the data transfer program)


## How-to
### XQ2 data
#### get data from sensor
* connect XQ2 to PC with USB cable
* make sure your system language is English (otherwise the iMet application does not work properly)
* start the application "iMet-X User Controller"
* click Settings > Com Port > ComX   (e.g. Com3). if you see multiple ComX, try both. if after selecting you see
  "iMet-XQ" in the menu bar, you have the correct one.
* click iMet-XQ > Save memory Data, and choose a location and filename (.csv)
#### analyze and plot
* open anaconda shell
* conda activate uav-analysis-env
* navigate to folder where the .py scripts are stored
* ```python plot_xq2_data.py path/to/xq2file.txt```, where xq2file.txt is the file from the step above

### Imet + Deltaquad
* windows: open anaconda shell, linux: open terminal
* conda activate uav-analysis-env
* navigate to folder where the .py scripts are stored
* ```python plot_uav_data.py imetfile deltaquadfile.ulg```

### interactive 3D plots
if you want to view the 3dplots interactively, type
```ipython -i plot_xq2_data.py path/to/xq2file.txt```
or
```ipython -i plot_xq2_data.py path/to/xq2file.txt```






### 3d visualizations
I tried mayavi http://docs.enthought.com/mayavi/mayavi/mlab.html#simple-scripting-with-mlab, but I didnt
get it running together with the other dependencies, and I gave up.

Now simply matplotlib 3d is used.




## deltaquad drone data conversion

The raw log data from the deltaquad UAV comes in ehe .ulg format (https://dev.px4.io/v1.9.0_noredirect/en/log/ulog_file_format.html)

Deltaquad recommended FlightPlot https://github.com/PX4/FlightPlot/releases/download/0.3.2/flightplot.jar.zip to
to convert to .kml format, but this does not work. Also displaying does not seem to work


pyFlightAnalysis (https://github.com/Marxlp/pyFlightAnalysis) works for displaying.
### installing pyFlightAnalysis
at least on ubuntu,the steps in the repo are not sufficient (dependency problems)
```
conda create -n deltaquad-env
conda activate deltaquad-env
conda install -y ipython
pip install pyqtgraph==0.10.0
pip install  pyOpenGL pyulog matplotlib numpy
pip install PyQt5
pip install simplekml
git clone https://github.com/Marxlp/pyFlightAnalysis.git
python setup.py install
```
then start the tool with typing
```commandline
analysis
```



## pyulog
https://github.com/PX4/pyulog/blob/master/README.md
pyulog is a command line tool for inspecting and converting .ulg files.
Installation: follow installation of pyFlightAnalysis, then it is automatically installed.


### most important commands
```bash
ulog2csv ifile -o outdir
```
converts to (multiple) .csv files

```bash
ulog2kml ifile -o ofile
```
converts to kml file

### Command Line Scripts
below info from the README of pyulog.

All scripts are installed as system-wide applications (i.e. they be called on the command line without specifying Python or a system path), and support the `-h` flag for getting usage instructions.

The sections below show the usage syntax and sample output (from [test/sample.ulg](test/sample.ulg)): 

###  Display information from an ULog file (ulog_info)

Usage:
```bash
usage: ulog_info [-h] [-v] file.ulg

Display information from an ULog file

positional arguments:
  file.ulg       ULog input file

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Verbose output
```

Example output:
```bash
$ ulog_info sample.ulg
Logging start time: 0:01:52, duration: 0:01:08
Dropouts: count: 4, total duration: 0.1 s, max: 62 ms, mean: 29 ms
Info Messages:
 sys_name: PX4
 time_ref_utc: 0
 ver_hw: AUAV_X21
 ver_sw: fd483321a5cf50ead91164356d15aa474643aa73

Name (multi id, message size in bytes)    number of data points, total bytes
 actuator_controls_0 (0, 48)                 3269     156912
 actuator_outputs (0, 76)                    1311      99636
 commander_state (0, 9)                       678       6102
 control_state (0, 122)                      3268     398696
 cpuload (0, 16)                               69       1104
 ekf2_innovations (0, 140)                   3271     457940
 estimator_status (0, 309)                   1311     405099
 sensor_combined (0, 72)                    17070    1229040
 sensor_preflight (0, 16)                   17072     273152
 telemetry_status (0, 36)                      70       2520
 vehicle_attitude (0, 36)                    6461     232596
 vehicle_attitude_setpoint (0, 55)           3272     179960
 vehicle_local_position (0, 123)              678      83394
 vehicle_rates_setpoint (0, 24)              6448     154752
 vehicle_status (0, 45)                       294      13230
```

### Display logged messages from an ULog file (ulog_messages)

Usage:
```
usage: ulog_messages [-h] file.ulg

Display logged messages from an ULog file

positional arguments:
  file.ulg    ULog input file

optional arguments:
  -h, --help  show this help message and exit
```

Example output:
```
ubuntu@ubuntu:~/github/pyulog/test$ ulog_messages sample.ulg
0:02:38 ERROR: [sensors] no barometer found on /dev/baro0 (2)
0:02:42 ERROR: [sensors] no barometer found on /dev/baro0 (2)
0:02:51 ERROR: [sensors] no barometer found on /dev/baro0 (2)
0:02:56 ERROR: [sensors] no barometer found on /dev/baro0 (2)
```

### Extract parameters from an ULog file (ulog_params)

Usage:
```
usage: ulog_params [-h] [-d DELIMITER] [-i] [-o] file.ulg [params.txt]

Extract parameters from an ULog file

positional arguments:
  file.ulg              ULog input file
  params.txt            Output filename (default=stdout)

optional arguments:
  -h, --help            show this help message and exit
  -d DELIMITER, --delimiter DELIMITER
                        Use delimiter in CSV (default is ',')
  -i, --initial         Only extract initial parameters
  -o, --octave          Use Octave format
```

Example output (to console):
```
ubuntu@ubuntu:~/github/pyulog/test$ ulog_params sample.ulg
ATT_ACC_COMP,1
ATT_BIAS_MAX,0.0500000007451
ATT_EXT_HDG_M,0
...
VT_OPT_RECOV_EN,0
VT_TYPE,0
VT_WV_LND_EN,0
VT_WV_LTR_EN,0
VT_WV_YAWR_SCL,0.15000000596
```

### Convert ULog to CSV files (ulog2csv)

Usage:
```
usage: ulog2csv [-h] [-m MESSAGES] [-d DELIMITER] [-o DIR] file.ulg

Convert ULog to CSV

positional arguments:
  file.ulg              ULog input file

optional arguments:
  -h, --help            show this help message and exit
  -m MESSAGES, --messages MESSAGES
                        Only consider given messages. Must be a comma-
                        separated list of names, like
                        'sensor_combined,vehicle_gps_position'
  -d DELIMITER, --delimiter DELIMITER
                        Use delimiter in CSV (default is ',')
  -o DIR, --output DIR  Output directory (default is same as input file)
```


### Convert ULog to KML files (ulog2kml)

> **Note** The `simplekml` module must be installed on your computer. If not already present, you can install it with:
  ```
  pip install simplekml
  ```

Usage:
```
usage: ulog2kml [-h] [-o OUTPUT_FILENAME] [--topic TOPIC_NAME]
                [--camera-trigger CAMERA_TRIGGER]
                file.ulg

Convert ULog to KML

positional arguments:
  file.ulg              ULog input file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILENAME, --output OUTPUT_FILENAME
                        output filename
  --topic TOPIC_NAME    topic name with position data
                        (default=vehicle_gps_position)
  --camera-trigger CAMERA_TRIGGER
                        Camera trigger topic name (e.g. camera_capture)
```

### Convert ULog to rosbag files (ulog2rosbag)

> **Note** You need a ROS environment with `px4_msgs` built and sourced.

Usage:
```
usage: ulog2rosbag [-h] [-m MESSAGES] file.ulg result.bag

Convert ULog to rosbag

positional arguments:
  file.ulg              ULog input file
  result.ulg            rosbag output file

optional arguments:
  -h, --help            show this help message and exit
  -m MESSAGES, --messages MESSAGES
                        Only consider given messages. Must be a comma-
                        separated list of names, like
                        'sensor_combined,vehicle_gps_position'
```



## mavic drone flight data conversion

more info here: https://mavicpilots.com/threads/mavic-flight-log-retrieval-and-analysis-guide.78627/

(part of) the mavic drone data (internal sensors etc) are logged on the phone that was used as a controller.
It is stored as .dat files, and can be converted and displayed with this tool:
https://datfile.net/CsvView/downloads.html
runs as java application on linux and mac, and as binary on windows.
when the DJI pilot app is used, the data is on the phone under
/Phone/DJI/com.dji.industry.pilot/MCDatFlightRecords/

there are also .txt files under /Phone/Android/data/com.dji.industry.pilot/files/DJI/com.dji.industry.pilot/FlightRecord$ 
, but they seem to be encrypted


## mavic drone android apps
the app that is probably best for is is the DJI Pilot app. It is, however, buggy.
on my private phone it did not work from the playstore, and I had to install it manually from the dji website.
on my KC-phone I could install it, but the map would not display at first. However, after entering manual flight mode
once, the map also showed in Mission Flight mode.
With this app one can plan flights ahead, but it seems relatively limited.
another potential alternative would be Litchi https://flylitchi.com/
