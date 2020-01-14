#!/bin/bash

# Given:
# * a ROOT file produced by plotEvent.py with met_significance histograms
# * the year of that tree (2016, 2017, or 2018)
# the script runs the fake lepton estimate for all 11 bins and makes plots
# in EPS format for all these bins of the anti-ID region and template shape.

if [ "$#" -ne 2 ]; then
    echo "run_template_fake_leptons.sh [input] [year]"
    exit 1
fi

SAMPLE=$1
YEAR=$2

# It'd be nice if we could make these for all selkeys automatically with no hardcoding.
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_allmjj_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_allmjj_em_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_allmjj_ep_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj800dphijj1nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj1000dphijj1nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj1500dphijj1nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj2000dphijj1nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj3500dphijj1nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj800dphijj2nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj1000dphijj2nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj1500dphijj2nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj2000dphijj2nj2_e_Nominal
python HInvPlot/macros/drawStack.py ${SAMPLE} --year ${YEAR} --vars met_significance --do-eps --save --atlas-style ~/root/atlasstyle/ --selkey pass_wcranti_mjj3500dphijj2nj2_e_Nominal

# Run the fake lepton estimate.
HInvPlot/macros/make_template_fake_leptons.py -a ${SAMPLE} -y ${YEAR} -n ${YEAR}

# remove *.png files.
rm -f *.png
