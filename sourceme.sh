#!/bin/bash
module load StdEnv/2016
module load gcc/6.4.0
module load python/3.6.3
module load scipy-stack
source /scratch/jgao/root/install/bin/thisroot.sh
export GEANT4_BASE_DIR=/scratch/jgao/geant4.10.03.p03/install
source ${GEANT4_BASE_DIR}/share/Geant4-10.3.3/geant4make/geant4make.sh
# source /project/rpp-blairt2k/prouse/hk/cry_v1.7/setup.sh /project/rpp-blairt2k/prouse/hk/cry_v1.7
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+"$LD_LIBRARY_PATH:"}${G4LIB}/${G4SYSTEM}
export WCSIMDIR=/project/rpp-blairt2k/jgao/WCSim
export G4WORKDIR=${WCSIMDIR}/exe
export FITQUN_ROOT=/project/rpp-blairt2k/prouse/hk/fiTQun