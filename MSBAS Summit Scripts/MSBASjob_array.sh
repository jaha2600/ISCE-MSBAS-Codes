#!/bin/bash

# Written by: jaha2600, jojo8550 with A Monaghan's help
# Date: 20210928
# Purpose: This script submits an MSBAS array job on Summit using sed to input R vals from an input txt file 

#SBATCH --account=ucb62_summit3     # Summit allocation
#SBATCH --partition=shas            # Summit partition
#SBATCH --time=30:00                # Max wall time
#SBATCH --nodes=1                   # Number of Nodes
#SBATCH --ntasks=24                 # Number of tasks per job. Will vary depending on size and num of Ifgs.
#SBATCH --job-name=MSarr
#SBATCH --array=1-5
#SBATCH --mail-type=END            # Email user when job finishes
#SBATCH --mail-user=jojo8550@colorado.edu # Email address of user


#purge all existing modules
module purge
# load modules needed to run program 
module load singularity/3.6.4

CASENAME=jrun5arr
RVAL=$(sed -n "${SLURM_ARRAY_TASK_ID}p" rvals.txt)

WORKDIR=$PWD/$CASENAME/rval_$RVAL
mkdir -p $WORKDIR

# Need both an asc list and a par txt. I want to try adding in the PAR values to the header instead
cp /scratch/summit/jojo8550/MSBASstuff/coherence03/desc30pairs.txt $WORKDIR
cp /scratch/summit/jojo8550/MSBASstuff/coherence03/par.txt $WORKDIR

cd  $WORKDIR
#make path to header file the first commandline argument 
HEADER_TEMPLATE=/scratch/summit/jojo8550/MSBASstuff/coherence03/header_template.txt
HEADER_FILE=header_$RVAL.txt

sed 's/RVAL/'$RVAL'/g' $HEADER_TEMPLATE > ${HEADER_FILE}

#run msbas program with header file as argument 
singularity exec --bind /scratch/summit /projects/$USER/containers/msbasv3.sif msbasv3 ${HEAD
ER_FILE}
