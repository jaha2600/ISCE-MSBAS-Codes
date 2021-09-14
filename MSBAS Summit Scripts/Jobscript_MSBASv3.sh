#!/bin/bash

# Written by: jaha2600@colorado.edu
# Date: 20210909
# Purpose: This script submits a job on Summit. Has been edited to accept a 5m local DEM instead of downloading one. 
# It is possible that the python script still downloads one, but doesn't use it.  
#SBATCH -A ucb-summit-mjw     # Summit allocation
#SBATCH --partition=shas     # Summit partition
#SBATCH --qos=normal                 # Summit qos
#SBATCH --time=024:00:00           # Max wall time
#SBATCH --nodes=1            # Number of Nodes
#SBATCH --ntasks=2           # Number of tasks per job

#SBATCH --job-name=msbasv3        # Job submission name
#SBATCH --mail-type=END            # Email user when job finishes
#SBATCH --mail-user=jaha2600@colorado.edu # Email address of user


#purge all existing modules
module purge
# load modules needed to run program 
module load singularity/3.6.4

#make path to header file the first commandline argument 
HEADER_FILE=/path/to/header.txt

#run msbas program with header file as argument 
singularity exec --bind /scratch/summit /projects/$USER/containers/msbasv3.sif msbasv3 $HEADER_FILE

