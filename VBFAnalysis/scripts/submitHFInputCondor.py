#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import VBFAnalysis.sample
import VBFAnalysis.systematics
import pickle
from VBFAnalysis.buildCondorScript import *
from VBFAnalysis.writeMultiJEleFake import *

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-i", "--inputDir",  type = str, dest = "inputDir", default = "/eos/user/r/rzou/v04/microtuples/", help = "dir for input file")
parser.add_argument( "--noSubmit", dest = "noSubmit", action="store_true", default = False, help = "Dont submit jobs" )
parser.add_argument("--extraVars", dest='extraVars', default="0", help="extraVars, 1=cut on the new variables for leptons veto, 2=loosen cuts, default: 0")
args, unknown = parser.parse_known_args()

writeMultiJet()
writeFakeEle()

### Load systematics list from VBFAnalysis/python/systematics.py ###
if args.nominal:
    sys = VBFAnalysis.systematics.systematics("Nominal")
    asys_systlist = []
    wsys_systlist = []
else:
    sys = VBFAnalysis.systematics.systematics("All")
    asys = VBFAnalysis.systematics.systematics("OneSided")
    wsys = VBFAnalysis.systematics.systematics("WeightSyst")
    asys_systlist = asys.getsystematicsList()
    wsys_systlist = wsys.getsystematicsList()

systlist = sys.getsystematicsList()
print systlist

### Remake submitDir ###
workDir = os.getcwd()+"/"+args.submitDir
buildDir = workDir[:workDir.find("/run/")]+"/build"
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)                

listoffiles = workDir+"/filelist"
listoffilesMC = workDir+"/filelistMC"
f = open(listoffiles, 'w')
fMC = open(listoffilesMC, 'w')
samplePatternGlobal = ""
p = subprocess.Popen("ls "+args.inputDir+"*root*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    filepath = line.strip()
    f.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] != "data"):
        fMC.write(filepath+"\n")
f.close()
fMC.close()

extraCommand=''
if args.extraVars:
    extraCommand=' --extraVars '

for syst in systlist:
    isLow = ""    
    if "__1down" in syst or "Down" in syst:
        isLow = " --isLow"
    if syst in wsys_systlist:
        isLow+=' --weightSyst'
    runCommand = '''athena VBFAnalysis/HFInputJobOptions.py --filesInput "$1" - --currentVariation '''+syst+isLow+extraCommand
    print runCommand
    writeCondorShell(workDir, buildDir, runCommand, syst, "HFInputCondorSub")
    writeCondorSub(workDir, syst, "HFInputCondorSub", listoffiles, listoffilesMC)

for syst in asys_systlist:
    runCommand = '''athena VBFAnalysis/HFInputJobOptions.py --filesInput "$1" - --currentVariation '''+syst+" --doLowNom"+extraCommand
    print runCommand
    writeCondorShell(workDir, buildDir, runCommand, syst, "HFInputCondorSub")
    writeCondorSub(workDir, syst, "HFInputCondorSub", listoffiles, listoffilesMC)

