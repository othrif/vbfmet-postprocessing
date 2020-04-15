#!/bin/bash

# Run

#./run.sh "" "" 3

inputDir=${1:-run_140420_replace/theoryVariation}
name=${2:-140420_replace_noCorr}
corr=${3:-0.375749}

python plotVar.py -p ${inputDir} --var boson_pT_Incl_nominal,boson_pT_CRZll_nominal,boson_pT_CRZPhi_nominal -n ${name}_nocorr -c 1  #--wait
python plotVar.py -p ${inputDir} --var boson_mass_Incl_nominal,boson_mass_CRZll_nominal,boson_mass_CRZPhi_nominal -n ${name}_nocorr -c 1  #--wait

python plotVar.py -p ${inputDir} --var boson_pT_Incl_nominal,boson_pT_CRZll_nominal,boson_pT_CRZPhi_nominal -n ${name}_corr -c ${corr}  #--wait
python plotVar.py -p ${inputDir} --var boson_mass_Incl_nominal,boson_mass_CRZll_nominal,boson_mass_CRZPhi_nominal -n ${name}_corr -c ${corr}  #--wait