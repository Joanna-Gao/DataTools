#!/bin/bash
# Example script to set up and submit batch jobs

# exit when any command fails
#set -e

# name and output data directory for this run
name=HKHybrid
data_dir=/project/rpp-blairt2k/machine_learning/data

# initial environment setup
source ${data_dir}/${name}/sourceme.sh

# set directory where log files will be saved
export LOGDIR="/scratch/$USER/log/WCSim_data_jobs/$name/fiTQun"
mkdir -p "$LOGDIR"
# cd to this directory so SLURM puts its logs there too
cd "$LOGDIR"

params="${FITQUN_ROOT}/ParameterOverrideFiles/Official_HyperK_HybridmPMT.parameters.dat"

# submit jobs with desired options
for f in ${data_dir}/${name}/WCSim/mu-/*/*/*/*_0.root; do
  p=${f##*/WCSim/}
  p=${p%%/*}
  for i in "2700"; do 
    JOBTIME=`date` sbatch --time=1-12:00:00 --mem=10G --array=8,11,13,72,94,95,102,142,145,178,191,220,242,251,256,260,275,287,293,298,327,334,357,381,382\
     --job-name=fq${i}_${p} "/project/rpp-blairt2k/jgao/DataTools/cedar_scripts/runfiTQun.sh"\
     "$f" "fiTQun" ${params} $i 300 ${LOGDIR}
  done
done
