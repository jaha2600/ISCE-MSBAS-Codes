#SBATCH --nodes=
## select one core to do the job
#SBATCH --ntasks=
## set shas partition
#SBATCH --partition=
## set condo for job? 
#SBATCH  --account 
## set walltime
#SBATCH --time=
## set email to send at end of job 
#SBATCH --mail-user=
#SBATCH --mail-type=END

module purge
source /curc/sw/anaconda3/latest
conda activate /curc/sw/anaconda3/2019.03/envs/idp

# your input file will be the first commandline variable submitted with the script 
# I would include the full path to input file to be safe. 

if [[! -z $1]] ; then

   INPUT_FILE=$1
else
  echo 'Script requies an input texfile as command line variable'
  exit

# $2 will be optional and will refer to the --r_vals flag in the python script 
# we need to first check if $2 is input at all, and then check that it is --rm_flag

# if there is a second input then do this:
if [[ ! -z $2]] ; then
   # check that the second string is equal to --r_vals
   if [[ $2 = "--r_vals" ]] ; then
      python /projects/$USER/MSBAS/make_msbas_inputs_r_vals.py $INPUT_FILE $2
   else
     echo 'Second command line input is optional. If inlcuded it must equal --rm_flag'
     exit
   fi
# if there is not a second input then just run script with input texfile:
else
  python /projects/$USER/MSBAS/make_msbas_inputs_r_vals.py $INPUT_FILE


fi

