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


#purge all existing modules
module purge
# load modules needed to run program 
module load singularity/3.6.4

#make path to header file the first commandline argument 
HEADER_FILE=/path/to/header.txt

#run msbas program with header file as argument 
singularity exec --bind /scratch/summit /projects/$USER/containers/msbasv3.sif msbasv3 $HEADER_FILE

