#!/bin/bash

OUTDIR=$1
VARS="met_tst_nolep_et,mll,mt_mety,ptll,lepPt0,lepPt1,phPt,mllg,ptllg"
FieldSeparator=$IFS

IFS=,
for vars in $VARS; do
    python HInvPlot/macros/drawStack.py out.root --selkey=pass_crtt_all_eu_Nominal --vars=$vars --do-ratio --do-pdf --save
    python HInvPlot/macros/drawStack.py out.root --selkey=pass_crtt_all_eu_Nominal --vars=$vars --do-ratio --do-pdf --do-logy --save
done
IFS=$FieldSeparator

rm -rf $OUTDIR
mkdir $OUTDIR
mv *.png $OUTDIR
mv *.pdf $OUTDIR
