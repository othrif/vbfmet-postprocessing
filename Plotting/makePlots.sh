#!/bin/bash

SELKEY=$1
VARS="met_tight_tst_et,mll,mt_mety,ptll,lepPt0,lepPt1,phPt,mllg,ptllg,dphi_mety_ll,pTt"
FieldSeparator=$IFS

IFS=,
for vars in $VARS; do
    python HInvPlot/macros/drawStack.py outtree_v02.root --selkey=$SELKEY --vars=$vars --do-ratio --do-pdf --save
    python HInvPlot/macros/drawStack.py outtree_v02.root --selkey=$SELKEY --vars=$vars --do-ratio --do-pdf --do-logy --save
#    python HInvPlot/macros/drawStack.py outtree_v02.root --selkey=pass_crtt_all_eu_Nominal --vars=$vars --do-ratio --do-pdf --save
#    python HInvPlot/macros/drawStack.py outtree_v02.root --selkey=pass_crtt_all_eu_Nominal --vars=$vars --do-ratio --do-pdf --do-logy --save
done
IFS=$FieldSeparator

rm -rf $SELKEY
mkdir $SELKEY
mv *.png $SELKEY
mv *.pdf $SELKEY
