#!/bin/bash
# Example script to set up and submit batch jobs

# exit when any command fails
set -e

# initial environment setup
export DATATOOLS=/project/rpp-blairt2k/jgao/DataTools
cd $DATATOOLS/cedar_scripts
# source /home/jgao/sourceme.sh

# name and output data directory for this run
export name=HKHybrid
export data_dir=/project/rpp-blairt2k/machine_learning/data
source "${data_dir}/${name}/sourceme.sh"

log_dir="/scratch/jgao/log/${name}"
mkdir -p $log_dir
cd $log_dir

# 0-999 root files for mu-, 0-999 root files for e- 
for i in "4" "5" "8" "9" "591"; do
  # f="${data_dir}/${name}/WCSim/*/*/*/*/*_${i}[0-9].root"
  f="${data_dir}/${name}/WCSim/gamma/*/*/*/*_${i}.root"
  sbatch --time=3:0:0 --job-name=rc${f##*_} "${DATATOOLS}/cedar_scripts/make_hybrid_npz.sh" "$f"
done
