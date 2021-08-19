# Codes to Extract MSBAS inputs from ISCE files

## Dependencies 
Codes are run in python command line and require the following modules to be installed: 
[`os`], [`sys`], [`glob`], [`shutil`], [`argparse`], [`gdal`], [`ogr`], [`pandas`], [`numpy`]

## Usage
[`updated_move_script.py`]
Designed to be used on summit on directory structure produced from running ISCE container.
Subdirectories in this example take the format 20XX_20XX instead of the whole pair name. If using complete pair name you will need to go in and change the wildcard for listing dirs.
Creates directory [`MSBAS_FILES`] that contains the files needed for MSBAS for each image pair.
This can then be downloaded via Globus.

[`updated_move_scirpt.py`] working_directory [--rm_flag] 

--rm_flag is optional, if used it will find large directories such as fine_offsets, master etc. and delete them to free up space.
 
[`PrepMsbasIfgs_jh.py`] 
Used on MSBAS_FILES directory after download to local computer.
Copy this script to MSBAS_FILES directory, create input file and run.
Creates input files needed for MSBAS algorithm. necessary file structure follows on from updated_move_script.py script.

[`PrepMsbasIfgs_jh.py`] input_file.txt

Example [`inputs.txt`] file included in repo. Here you assign the working directory path, and the extents you wish to run MSBAS on.
Extents variable can be the values of extent OR a shapefile in EPSG:4326 matching desired area.

