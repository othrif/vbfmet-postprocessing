python pyAnalysis/extractNtuples.py processed/W_strong.root processed/Z_strong.root

python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_checks.json --treename nominal --eventWeight "w" --newOutputs --name checks_
python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_NjetTJV.json --treename nominal --eventWeight "w" --newOutputs --name tjv_

python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v /all/Incl/boson_pt,/all/Incl/boson_pt -l --wait
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Zll_QCD -v /all/Incl/boson_pt,/all/Incl/boson_pt -l --wait
python pyAnalysis/drawHists.py -f hists_checks_extract_Wev_QCD,hists_checks_extract_Wmv_QCD     -v /all/Incl/boson_pt,/all/Incl/boson_pt -l --wait

python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v /all/Incl/jj_mass,/all/Incl/jj_mass --wait
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Zll_QCD -v /all/Incl/jj_mass,/all/Incl/jj_mass --wait
python pyAnalysis/drawHists.py -f hists_checks_extract_Wev_QCD,hists_checks_extract_Wmv_QCD -v /all/Incl/jj_mass,/all/Incl/jj_mass --wait

python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v /all/Incl/n_jet25,/all/Incl/n_jet25 --wait
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Zll_QCD -v /all/Incl/n_jet25,/all/Incl/n_jet25 --wait

python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v /all/Incl/jet3_pt,/all/Incl/jet3_pt --wait
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Zll_QCD -v /all/Incl/jet3_pt,/all/Incl/jet3_pt --wait

python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v /all/Incl/jet1_pt,all/Incl/jet1_pt --wait
python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v /all/Incl/jet2_pt,all/Incl/jet2_pt --wait

python pyAnalysis/ratioHists.py -f hists_tjv_extract_Zvv_QCD,hists_tjv_extract_Wlv_QCD -v /all/SR25/jj_mass,/all/SRmTJV/jj_mass --wait