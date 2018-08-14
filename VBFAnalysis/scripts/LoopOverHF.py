#!/usr/bin/env python 

import os
import sys
import argparse

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')
parser.add_argument( "-s", "--syst", type = str, dest = "syst", default = "NONE", help = "which systematics to generate HF input for" )
parser.add_argument( "-n", "--doLowNom", action = "store_true", dest = "doLowNom", default = False, help = "symmetrize asymmetric systematics for HF")
parser.add_argument( "-l", "--isLow", action = "store_true", dest = "isLow", default = False, help = "is downward systematics");
parser.add_argument( "-t", "--test", action = "store_true", dest = "test", default = False, help = "test with one sample");
parser.add_argument( "-i", "--inputDir", type = str, dest = "inputDir", default = "/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/FinalNtuplesJuly18", help = "dir where input files are stored" )
args, unknown = parser.parse_known_args()

if args.test:
    sampleDict = {"signalH125_new" : inputDir+"/"+"VBFHiggsInv_signals.root"}
else:
    sampleDict = {"signalH125_new" : inputDir+"/"+"VBFHiggsInv_signals.root", 
                  "signalH125_new_ggF" : inputDir+"/"+"VBFHiggsInv_signals.root",
                  "W_strong" : inputDir+"/"+"VBFHiggsInv_Wtot_bkgcomplete_fixednom.root",
                  "W_EWK" : inputDir+"/"+"VBFHiggsInv_Wtot_bkgcomplete_fixednom.root",
                  "Z_strong" : inputDir+"/"+"VBFHiggsInv_Ztot_bkg_fixednom.root",
                  "Z_EWK" : inputDir+"/"+"VBFHiggsInv_Ztot_bkg_fixednom.root",   
                  "ttbar": inputDir+"/"+"VBFHiggsInv_topbkg.root",
                  "physics_micro": inputDir+"/"+"merge_data.root"
                  }

doLowNom_str = ""
isLow_str = ""
if args.doLowNom:
    doLowNom_str = " --doLowNom"
if args.isLow:
    isLow_str = " --isLow"
    
for sample in sampleDict:
    if "physics" in sample:
        if args.syst != "NONE":
            continue
        os.system("athena VBFAnalysis/HFInputJobOptions.py --filesInput "+sampleDict[sample]+" - --currentSamples "+sample+" --currentVariation "+args.syst+" --isData")
    else:
        os.system("athena VBFAnalysis/HFInputJobOptions.py --filesInput "+sampleDict[sample]+" - --currentSamples "+sample+" --currentVariation "+args.syst+doLowNom_str+isLow_str)


        

