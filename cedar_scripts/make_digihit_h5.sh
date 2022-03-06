#!/bin/bash
#SBATCH --account=rpp-blairt2k
#SBATCH --time=3:0:0
#SBATCH --mem-per-cpu=16G
#SBATCH --output=%x-%a.out
#SBATCH --error=%x-%a.err
#SBATCH --cpus-per-task=1

# sets up environment and runs np_to_hit_array_hdf5.py, see that file for info
# on arguments, that all get passed through from this script

# need to write another script for the batch mode, if you're just running this
# script it counts as running in the login node

ulimit -c 0

name=HKHybrid
data_dir=/project/rpp-blairt2k/machine_learning/data
source "${data_dir}/${name}/sourceme.sh"

virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index h5py

#cd /project/rpp-blairt2k/machine_learning/production_software/DataTools/\
# root_utils/
cd /project/rpp-blairt2k/jgao/DataTools/root_utils/

# need to pass in output path + output name with option "-o", and the name of
# the npz files
echo "python np_to_digihit_array_hdf5.py -o $1 `echo ${@:2}`"
python np_to_digihit_array_hdf5.py -o "$1" `echo ${@:2}`

