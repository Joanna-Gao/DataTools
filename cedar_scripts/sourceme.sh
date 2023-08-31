#!/bin/bash
module load StdEnv/2016
module load gcc/6.4.0
module load python/3.6.3
module load scipy-stack
source /project/rpp-blairt2k/machine_learning/production_software/root/install-2021-03-26/bin/thisroot.sh
export GEANT4_BASE_DIR=/project/rpp-blairt2k/machine_learning/production_software/Geant4/geant4.10.03.p03-install
source ${GEANT4_BASE_DIR}/share/Geant4-10.3.3/geant4make/geant4make.sh
# source /scratch/jgao/software/root/install/bin/thisroot.sh
# source /scratch/jgao/software/geant4.10.03.p03/install/share/Geant4-10.3.3/geant4make/geant4make.sh
export G4WORKDIR=/project/rpp-blairt2k/jgao/WCSim/exe
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+"$LD_LIBRARY_PATH:"}${G4LIB}/${G4SYSTEM}
export WCSIMDIR=/project/rpp-blairt2k/jgao/WCSim
export DATATOOLS="$(cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
export FITQUN_ROOT=/project/rpp-blairt2k/prouse/hk/fiTQun
export PYTHONPATH=$DATATOOLS:$PYTHONPATH