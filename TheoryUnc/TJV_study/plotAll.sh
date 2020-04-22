python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_checks.json --treename nominal --eventWeight "w" --newOutputs --name checks_

# Zvv vs Wlv
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v all/Incl/boson_pt,all/Incl/boson_pt -l
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v all/Incl/jj_mass,all/Incl/jj_mass
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v all/Incl/n_jet25,all/Incl/n_jet25
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v all/Incl/jet1_pt,all/Incl/jet1_pt
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v all/Incl/jet2_pt,all/Incl/jet2_pt
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v all/Incl/jet3_pt,all/Incl/jet3_pt
