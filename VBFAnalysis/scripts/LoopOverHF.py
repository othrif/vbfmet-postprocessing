#!/usr/bin/env python 

import os
import sys
import argparse

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')
parser.add_argument( "-s", "--syst", type = str, dest = "syst", default = "NONE", help = "which systematics to generate HF input for" )
parser.add_argument( "-n", "--doLowNom", action = "store_true", dest = "doLowNom", default = False, help = "symmetrize asymmetric systematics for HF")
parser.add_argument( "-l", "--isLow", action = "store_true", dest = "isLow", default = False, help = "is downward systematics");
parser.add_argument( "-t", "--test", action = "store_true", dest = "test", default = False, help = "test with one sample");
parser.add_argument( "-i", "--inputDir", type = str, dest = "inputDir", default = "/eos/user/r/rzou/v04/merged/", help = "dir where input files are stored" )
args, unknown = parser.parse_known_args()

s = sample.sample()
sampleList = s.getsampleTypeList()

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


        

