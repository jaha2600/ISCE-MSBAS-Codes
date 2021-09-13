#SBATCH --nodes=1
## select one core to do the job
#SBATCH --ntasks=1
## set shas partition
#SBATCH --partition=shas
## set condo for job? 
#SBATCH  --account ucb-summit-mjw
## set walltime
#SBATCH --time=2:00:00
## set email to send at end of job 
#SBATCH --mail-user=jaha2600@colorado.edu
#SBATCH --mail-type=END

module purge
source /curc/sw/anaconda3/latest
conda activate /curc/sw/anaconda3/2019.03/envs/idp

# your input file will be the first commandline variable submitted with the script 
# I would include the full path to input file to be safe. 

INPUT_FILE=$1

# $2 will be optional and will refer to the --r_vals flag in the python script 
# we need to first check if $2 is input at all, and then check that it is --rm_flag

# if there is a second input then do this:
if [ ! -z $2] ; then
   # check that the second string is equal to --r_vals
   if [ $2 = "--r_vals" ] ; then
      python /projects/jaha2600/MSBAS/make_msbas_inputs_r_vals.py $INPUT_FILE $2
   else
     echo 'Second command line input is optional. If inlcuded it must equal --rm_flag'
   fi
# if there is not a second input then just run script with input texfile:
else
  python /projects/jaha2600/MSBAS/make_msbas_inputs_r_vals.py $INPUT_FILE


fi

