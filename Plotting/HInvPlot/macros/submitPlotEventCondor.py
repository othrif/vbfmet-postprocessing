#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import HInvPlot.systematics
import pickle
from HInvPlot.buildCondorScript import *

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-i", "--inputFile",  type = str, dest = "inputFile", default = "v26.txt", help = "path for input files")
parser.add_argument( "--noSubmit", dest = "noSubmit", action="store_true", default = False, help = "Dont submit jobs" )
parser.add_argument("--extraVars", dest='extraVars', default="0", help="extraVars, 1=cut on the new variables for leptons veto, 2=loosen cuts, default: 0")
args, unknown = parser.parse_known_args()

### Load systematics list from HInvPlot/python/systematics.py ###
if args.nominal:
    sys = VBFAnalysis.systematics.systematics("Nominal")
    asys_systlist = []
    wsys_systlist = []
else:
    sys =  HInvPlot.systematics.systematics("All")
    asys = HInvPlot.systematics.systematics("OneSided")
    wsys = HInvPlot.systematics.systematics("WeightSyst")
    asys_systlist = asys.getsystematicsList()
    wsys_systlist = wsys.getsystematicsList()

systlist = sys.getsystematicsList()
print systlist

### Remake submitDir ###
workDir = os.getcwd()+"/"+args.submitDir
bDir= os.getenv('ROOTCOREDIR')
buildDir = workDir[:bDir.find("/Plotting")]
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)                

listofsysts = workDir+"/systlist"
f = open(listofsysts, 'w')
for line in systlist:
    f.write(line+"\n")
f.close()

extraCommand=''
#if args.extraVars:
#    extraCommand=' --extraVars '
TESTAREA=buildDir+'/Plotting'
runCommand = '''python '''+TESTAREA+'''/HInvPlot/macros/plotEvent.py --syst "$1"  -r /tmp/out_"$1".root -i '''+args.inputFile+extraCommand
print runCommand
writeCondorShell(workDir, buildDir, '', runCommand, "PlotEventCondorSub")
writeCondorSub(workDir, '', "PlotEventCondorSub", listofsysts)

