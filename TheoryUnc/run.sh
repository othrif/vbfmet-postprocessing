#!/bin/bash

# Run

#./run.sh "" "" 3
# python STPostProcessing/TheoryUnc/plotVar.py -p input/theoryVariation --var boson_pT_Incl_nominal,boson_pT_CRZll_nominal,boson_pT_CRZPhi_nominal --wait -n 150420_noCorr  -c 1 -s /Applications/root_v6.10.08/RootUtils

inputDir=${1:-input/theoryVariation}
name=${2:-150420}
corr=${3:-0.375749}

python STPostProcessing/TheoryUnc/plotVar.py -p ${inputDir} --var boson_pT_Incl_nominal,boson_pT_CRZll_nominal,boson_pT_CRZPhi_nominal -n ${name}_noCorr -c 1  -s /Applications/root_v6.10.08/RootUtils #--wait
python STPostProcessing/TheoryUnc/plotVar.py -p ${inputDir} --var boson_mass_Incl_nominal,boson_mass_CRZll_nominal,boson_mass_CRZPhi_nominal -n ${name}_noCorr -c 1  -s /Applications/root_v6.10.08/RootUtils #--wait

python STPostProcessing/TheoryUnc/plotVar.py -p ${inputDir} --var boson_pT_Incl_nominal,boson_pT_CRZll_nominal,boson_pT_CRZPhi_nominal -n ${name}_Corr -c ${corr}  -s /Applications/root_v6.10.08/RootUtils #--wait
python STPostProcessing/TheoryUnc/plotVar.py -p ${inputDir} --var boson_mass_Incl_nominal,boson_mass_CRZll_nominal,boson_mass_CRZPhi_nominal -n ${name}_Corr -c ${corr}  -s /Applications/root_v6.10.08/RootUtils #--wait