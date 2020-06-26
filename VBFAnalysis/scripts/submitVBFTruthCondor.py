#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import VBFAnalysis.sampleTruth
import VBFAnalysis.systematics
import pickle
from VBFAnalysis.buildCondorScript import *

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-l", "--listSample", type = str, dest = "listSample", default = "/eos/user/r/rzou/v04/list", help = "list of ntuples to run over" )
parser.add_argument( "-p", "--proxyName", type = str, dest = "proxyName", default = "/tmp/x509up_u29949", help = "proxy file for grid")
parser.add_argument( "--noSubmit", dest = "noSubmit", action="store_true", default = False, help = "Dont submit jobs" )
parser.add_argument( "-f", "--normFile", type = str, dest = "normFile", default = "/nfs/dust/atlas/user/othrif/vbf/myPP/source/VBFAnalysis/data/fout_v48.root", help = "file with the total number of event processed" )
parser.add_argument( "--noSkim", dest='noSkim', action="store_true", default=False, help="No skim, default: False")
parser.add_argument( "--theoVariation", dest = "theoVariation", action="store_true", default = False, help = "Run Theory uncertainties ")
args, unknown = parser.parse_known_args()

### Load Nominal from VBFAnalysis/python/systematics.py ###
sys = VBFAnalysis.systematics.systematics("Nominal")
systlist = sys.getsystematicsList()
print systlist
list_file=None
isFileMap=False
if args.listSample.count('.p'):
    list_file = pickle.load( open( args.listSample, "rb" ) ) #open(args.listSample, "r")
    isFileMap=True
else:
    list_file = open(args.listSample, "r")

### Remake submitDir ###
workDir = os.getcwd()+"/"+args.submitDir
CMTCONFIG = os.getenv('CMTCONFIG')
buildPaths = os.getenv('CMAKE_PREFIX_PATH')
buildPathsVec = buildPaths.split(':')
buildDir =  buildPathsVec[0][:buildPathsVec[0].find(CMTCONFIG)].rstrip('/')
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)

listofrunN = workDir+"/filelist"
f = open(listofrunN, 'w')
samplePatternGlobal = ""
if isFileMap:
    nb=0
    for container,contFileList in list_file.iteritems():
        #if not container.count('276181'):#'364184'):
        #    continue
        s=VBFAnalysis.sampleTruth.sample(container)
        isMC = s.getisMC()
        runNumberS = s.getrunNumberS()
        comma_sep_files=''
        for filepath in contFileList:
            comma_sep_files+=filepath+','
            nb+=1
        f.write(comma_sep_files.rstrip(',')+' '+container+"\n")
        samplePatternGlobal=''
else:
    for sampledir in list_file:
        s=VBFAnalysis.sampleTruth.sample(sampledir)
        isMC = s.getisMC()
        runNumberS = s.getrunNumberS()
        p = subprocess.Popen("ls "+sampledir.strip()+"/*root*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            filepath = line.strip()
            f.write(filepath[filepath.find("user."):]+"\n")
        samplePattern = sampledir[:sampledir.find("user.")]
        foundV = False
        for p,s in enumerate(sampledir.split(".")):
            if s[0]=="v":
                #samplePattern+="."+s
                #print " > ", samplePattern #
                foundV = True
        if not(foundV):
            print "ERROR: samples have different names than assumed!"
            break
        if (samplePatternGlobal != samplePattern) and (samplePatternGlobal != ""):
            print "ERROR: samples have different patterns!"
            break
        samplePatternGlobal = samplePattern#+'.'
f.close()

addArgs =""
if args.theoVariation:
    addArgs += " --theoVariation"
if args.noSkim:
    addArgs += " --noSkim"

for syst in systlist:
    print listofrunN
    if args.noSubmit:
        break
    runCommand = '''athena VBFAnalysis/VBFTruthAlgJobOptions.py --filesInput "'''+samplePatternGlobal+'''$1" - --currentVariation '''+syst+''' --normFile '''+args.normFile + addArgs
    if isFileMap:
        runCommand+=''' --containerName $2'''
    writeCondorShell(workDir, buildDir, runCommand, syst, "VBFAnalysisCondorSub", proxyName=args.proxyName) #writeCondorShell(subDir, buildDir, syst, runCommand, scriptName="VBFAnalysisCondorSub")
    print listofrunN
    writeCondorSub(workDir, syst, "VBFAnalysisCondorSub", listofrunN, listofrunN)

