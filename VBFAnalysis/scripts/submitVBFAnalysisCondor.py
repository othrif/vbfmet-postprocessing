#!/usr/bin/env python

import os
import sys
import argparse
import VBFAnalysis.sample
import VBFAnalysis.systematics

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

def writeCondorShell(subDir, syst, sampledir):
    print "athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --filesInput '"+sampledir+"' - --currentVariation "+syst
    os.system('''echo "#!/bin/bash" > '''+subDir+'''/VBFAnalysisCondorSub'''+syst+'''.sh''')
    os.system("echo 'export HOME=$(pwd)' >> "+subDir+"/VBFAnalysisCondorSub"+syst+".sh")
    os.system("echo 'export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase' >> "+subDir+"/VBFAnalysisCondorSub"+syst+".sh")
    os.system("echo 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet' >> "+subDir+"/VBFAnalysisCondorSub"+syst+".sh")
    os.system("echo 'asetup AthAnalysis,21.2.35,here' >> "+subDir+"/VBFAnalysisCondorSub"+syst+".sh")
    os.system("echo 'source "+buildDir+"/${CMTCONFIG}/setup.sh' >> "+subDir+"/VBFAnalysisCondorSub"+syst+".sh")
    os.system('''echo 'athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --filesInput "'''+sampledir+'''" - --currentVariation '''+syst+'''' >> '''+subDir+'''/VBFAnalysisCondorSub'''+syst+'''.sh''')
    os.system("chmod 777 "+subDir+"/VBFAnalysisCondorSub"+syst+".sh")

def writeCondorSub(workDir, syst):
    os.system("echo 'universe                = vanilla' > "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'executable              = "+workDir+"/VBFAnalysisCondorSub"+syst+".sh' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'output                  = "+workDir+"/output$(ClusterId).$(ProcId)' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'error                   = "+workDir+"/error$(ClusterId).$(ProcId)' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'log                     = "+workDir+"/log$(ClusterId)' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system('''echo "+JobFlavour = 'tomorrow'" >> '''+workDir+'''/submit_this_python'''+syst+'''.sh''')
    os.system("echo '' >> "+workDir+"/submit_this_python"+syst+".sh")
    if syst == "Nominal":
        os.system("echo 'queue arguments from '"+listofrunN+" >> "+workDir+"/submit_this_python"+syst+".sh")
    else:
        os.system("echo 'queue arguments from '"+listofrunNMC+" >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("chmod 777 "+workDir+"/submit_this_python"+syst+".sh")
    os.system("condor_submit "+workDir+"/submit_this_python"+syst+".sh")

listofrunN = workDir+"/filelist"
listofrunNMC = workDir+"/filelistMC"
f = open(listofrunN, 'w')
fMC = open(listofrunNMC, 'w')
samplePatternGlobal = ""
for sampledir in list_file:
    s=VBFAnalysis.sample.sample(sampledir)
    isMC = s.getisMC()
    runNumberS = s.getrunNumberS()
    f.write(runNumberS+"\n")
    if isMC:
        fMC.write(runNumberS+"\n")
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
    writeCondorShell(workDir, syst, samplePatternGlobal+".$1.*/*")
    writeCondorSub(workDir, syst)
