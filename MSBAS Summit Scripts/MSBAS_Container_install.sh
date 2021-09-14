#!/bin/bash

mkdir -p /projects/$USER/containers

cd /projects/$USER/containers

module load singularity

export SINGULARITY_TMPDIR=/scratch/summit/$USER
export SINGULARITY_CACHEDIR=/scratch/summit/$USER

singularity pull msbasv3.sif library://monaghaa/default/msbasv3:latest

#singularity pull --name msbasv3.sif

#singularity pull library://monaghaa/default/msbasv3:latest

echo 'Done creating msbas container in /projects/$USER/containers'
