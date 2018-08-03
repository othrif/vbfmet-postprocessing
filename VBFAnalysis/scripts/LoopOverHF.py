#!/usr/bin/env python 

import os
import sys
import argparse

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-s", "--syst", type = str, dest = "syst", default = "NONE", help = "which systematics to generate HF input for" )
args, unknown = parser.parse_known_args()

sampleDict = {"signalH125_new" : "/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/FinalNtuplesJuly18/VBFHiggsInv_signals.root", 
              "signalH125_new_ggF" : "/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/FinalNtuplesJuly18/VBFHiggsInv_signals.root"
              "W_strong" : "~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_Wtot_bkgcomplete_fixednom.root",
              "W_EWK" : "~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_Wtot_bkgcomplete_fixednom.root",
              "Z_strong" : "~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_Ztot_bkg_fixednom.root",
              "Z_EWK" : "~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_Ztot_bkg_fixednom.root",   
              "ttbar": "~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_topbkg.root",
              "physics_micro": "~/eosvbfinv/FinalNtuplesJuly18/merge_data.root"
              }
for sample in sampleDict:
    if "physics" in sample:
        if args.syst != "NONE":
            continue
        os.system("athena VBFAnalysis/HFInputJobOptions.py --filesInput "+sampleDict[sample]+" - --currentSamples "+sample+" --currentVariation "+args.syst+" --isData")
    else:
        os.system("athena VBFAnalysis/HFInputJobOptions.py --filesInput "+sampleDict[sample]+" - --currentSamples "+sample+" --currentVariation "+args.syst)

        

