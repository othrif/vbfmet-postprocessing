python pyAnalysis/extract_CRSR.py processed/*
python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_NjetTJV.json --treename nominal --eventWeight "w" --newOutputs
root pyAnalysis/plotTJVRatio.C
