# MSBAS Container on RMACC Summit

This directory contains a bash script to install MSBASv3 on summit, and an example of a standard Jobscript.

## Installation

To install msbasv3 on summit:

Step 1: Log into summit 'scompile' node

Step 2: Run installation script:

```
bash ./MSBAS_Container_Install.sh 
```

The continer will be installed in `/projects/$USER/containers` and you should see the file msbasv3_latest.sif in that directory.

## Usage

To run a simple usage case of MSBAS see the Jobscript_MSBASv3.sh script above.

Copy this script into the directory that you want to run msbas in, as all the outputs are placed in the dir it runs from.

```
sbatch Jobscript_MSBASv3.sh 

```
You need to change the path to your header.txt file and change the sbatch commands at the top to your own allocation, email etc.

The number of nodes / ntasks varies depending on your input data size, along with what the suitable wall time is. 



