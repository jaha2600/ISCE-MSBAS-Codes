# MSBAS Container on RMACC Summit

This directory contains a bash script to install MSBASv3 on summit, and two example jobscripts, one for a single job submission and one for an array.

## Installation

To install msbasv3 on summit:

Step 1: Log into summit 'scompile' node

Step 2: Run installation script:

```
bash ./MSBAS_Container_Install.sh 
```

The continer will be installed in `/projects/$USER/containers` and you should see the file msbasv3_latest.sif in that directory.

## Usage

To run a simple usage case of MSBAS see the MSBASjob_single.sh script above.

Copy this script into the directory that you want to run msbas in, as all the outputs are placed in the dir it runs from.

```
sbatch MSBASjob_single.sh 
```
You need to change the path to your header.txt file and change the sbatch commands at the top to your own allocation, email etc.


To submit an array of MSBAS jobs with varying r_val parameter use the MSBASjob_array.sh script

```
sbatch MSBASjob_array.sh
```

You need to change the following parts to suit your needs
1. SLURM commands at the top of the script
2. CASENAME - this is the root for submitted jobs 
3. location of intf pairs file, par.txt
4. Location of your header_template.txt (see example file above) that contains all parameters you with to use EXLCUDING r_val 


The number of nodes / ntasks varies depending on your input data size. MSBAS is a high memory program, as such we reccomend running on a high memory node. For the RMACC Summit supercomputer this would be an 'smem' partition


## Assessing the Validity of MSBAS Outputs - r_val

To find the optimum r_val to be used in the MSBAS run we first suggest running the MSBASjob_array.sh script above

