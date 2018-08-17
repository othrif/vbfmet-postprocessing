#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import VBFAnalysis.sample
import VBFAnalysis.systematics
from VBFAnalysis.buildCondorScript import *

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-l", "--listSample", type = str, dest = "listSample", default = "/eos/user/r/rzou/v04/list", help = "list of ntuples to run over" )
args, unknown = parser.parse_known_args()

### Load systematics list from VBFAnalysis/python/systematics.py ###
if args.nominal:
    sys = VBFAnalysis.systematics.systematics("Nominal")
else:
    sys = VBFAnalysis.systematics.systematics("All")
systlist = sys.getsystematicsList()
print systlist
list_file = open(args.listSample, "r")

### Remake submitDir ###
workDir = os.getcwd()+"/"+args.submitDir
buildDir = workDir[:workDir.find("/run/")]+"/build"
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)                

listofrunN = workDir+"/filelist"
listofrunNMC = workDir+"/filelistMC"
f = open(listofrunN, 'w')
fMC = open(listofrunNMC, 'w')
samplePatternGlobal = ""
for sampledir in list_file:
    s=VBFAnalysis.sample.sample(sampledir)
    isMC = s.getisMC()
    runNumberS = s.getrunNumberS()
    p = subprocess.Popen("ls "+sampledir.strip()+"*/*root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        filepath = line.strip()
        f.write(filepath[filepath.find(runNumberS):]+"\n")
        if isMC:
            fMC.write(filepath[filepath.find(runNumberS):]+"\n")
    samplePattern = sampledir[:sampledir.find(".v")]
    foundV = False
    for p,s in enumerate(sampledir.split(".")):
        if s[0]=="v":
            samplePattern+="."+s
            foundV = True
    if not(foundV):
        print "ERROR: samples have different names than assumed!"
        break
    if (samplePatternGlobal != samplePattern) and (samplePatternGlobal != ""):
        print "ERROR: samples have different patterns!"
        break
    samplePatternGlobal = samplePattern
f.close()
fMC.close()

for syst in systlist:
    runCommand = '''athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --filesInput "'''+samplePatternGlobal+'''.$1" - --currentVariation '''+syst
    writeCondorShell(workDir, buildDir, runCommand, syst, "VBFAnalysisCondorSub") #writeCondorShell(subDir, buildDir, syst, runCommand, scriptName="VBFAnalysisCondorSub")
    print listofrunN
    writeCondorSub(workDir, syst, "VBFAnalysisCondorSub", listofrunN, listofrunNMC)
