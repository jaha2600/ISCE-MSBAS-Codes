#!/bin/bash

# Written by: jaha2600@colorado.edu
# Date: 20210909
# Purpose: This script submits a job on RMACC Summit. Can be used with other HPC systems if SBATCH/scheduling commands are changed.   
#SBATCH -A      # Summit allocation
#SBATCH --partition=     # Summit partition
#SBATCH --qos=                # Summit qos
#SBATCH --time=           # Max wall time
#SBATCH --nodes=          # Number of Nodes
#SBATCH --ntasks=          # Number of tasks per job

#SBATCH --job-name=       # Job submission name
#SBATCH --mail-type=END            # Email user when job finishes
#SBATCH --mail-user= # Email address of user

module purge
source /curc/sw/anaconda3/latest
conda activate /curc/sw/anaconda3/2019.03/envs/idp

# directory containing all the r-val subdirectories
WORKING_DIR=$PWD/$CASENAME

# create an input list with the paths to all the log files
ls $WORKING_DIR/*/MSBAS_LOG.txt > $WORKING_DIR/log_list.txt

#this textfile will be your input variable
input_file=$WORKING_DIR/log_list.txt

# run python script, outputs appear in the location of $WORKING_DIR
python make_x_ax-y_graphs.py $input_file $WORKING_DIR




