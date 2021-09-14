# Codes to Create Inputs and run MSBAS from ISCE Outputs.

## Usage
### `msbas_move_script.py`

Designed to be used on summit on directory structure produced from running ISCE container.

Subdirectories in this example take the format 20XX_20XX instead of the whole pair name. If using complete pair name you will need to go in and change the wildcard for listing dirs.

Creates directory `MSBAS_FILES` that contains the files needed for MSBAS for each image pair.

This can then be downloaded via Globus.


`msbas_move_script.py` working_directory [--rm_flag] 

--rm_flag is optional, if used it will find large directories such as fine_offsets, master etc. and delete them to free up space.

 
### `make_msbas_inputs.py` 

Used on MSBAS_FILES directory after download to local computer.

Copy this script to MSBAS_FILES directory, create input file and run.

Creates input files needed for MSBAS algorithm. necessary file structure follows on from updated_move_script.py script.


`make_msbas_inputs.py` input_file.txt


Example `inputs.txt` file included in repo. Here you assign the working directory path, and the extents you wish to run MSBAS on.

Extents variable can be the values of extent OR a shapefile in EPSG:4326 matching desired area.

### misc directory scripts
Other useful things that are still in development:

`get_insar_pairs_all_combo.py`

This is a prelim script that reads in a list of insar files from ASF, and calculates all possible pairs within a certain amount of dates (that you set as a variable in cmd line).

Output format is not yet compatible with the jobscript used to run isce, as you would want your ref and sec to be lines 1 & 2, then lines 3 & 4 etc.

Usage: `get_insar_pairs_all_combo.py` asf_filelist.txt 10

`filt_topo_stats.py`

Get average coherance and coverage of filt topo image. 

