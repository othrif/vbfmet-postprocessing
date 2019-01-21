#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import VBFAnalysis.sample
import VBFAnalysis.systematics
import pickle
from VBFAnalysis.buildCondorScript import *

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "--slc7", dest = "slc7", action="store_true", default = False, help = "Do slc7" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-l", "--listSample", type = str, dest = "listSample", default = "/eos/user/r/rzou/v04/list", help = "list of ntuples to run over" )
#parser.add_argument( "-f", "--normFile", type = str, dest = "normFile", default = "/home/rzou/STPostProcessing/run/f_out_total_v05.root", help = "file with the total number of event processed" )
parser.add_argument( "-f", "--normFile", type = str, dest = "normFile", default = "/home/schae/testarea/HInv/source/VBFAnalysis/data/f_out_total_v05.root", help = "file with the total number of event processed" )
parser.add_argument( "-p", "--proxyName", type = str, dest = "proxyName", default = "/home/schae/testarea/HInv/run/x509up_u20186", help = "proxy file for grid")
parser.add_argument( "--noSubmit", dest = "noSubmit", action="store_true", default = False, help = "Dont submit jobs" )
args, unknown = parser.parse_known_args()


systlist  = []
### Load systematics list from VBFAnalysis/python/systematics.py ###
if args.nominal:
    sys = VBFAnalysis.systematics.systematics("Nominal")
    systlist = sys.getsystematicsList()
else:
    sys = VBFAnalysis.systematics.systematics("All")
    sysweight = VBFAnalysis.systematics.systematics("WeightSyst")
    systalllist = sys.getsystematicsList()
    systweightlist = sysweight.getsystematicsList()
    for sys in systalllist:
        if sys not in systweightlist:
            systlist.append(sys)

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
buildDir =  buildPathsVec[0][:buildPathsVec[0].find(CMTCONFIG)-len(CMTCONFIG)].rstrip('/')
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)                

listofrunN = workDir+"/filelist"
listofrunNMC = workDir+"/filelistMC"
f = open(listofrunN, 'w')
fMC = open(listofrunNMC, 'w')
samplePatternGlobal = ""
if isFileMap:
    nb=0
    for container,contFileList in list_file.iteritems():
        #if not container.count('276181'):#'364184'):
        #    continue
        s=VBFAnalysis.sample.sample(container)
        isMC = s.getisMC()
        runNumberS = s.getrunNumberS()
        comma_sep_files=''
        for filepath in contFileList:
            comma_sep_files+=filepath+','
            nb+=1
        f.write(comma_sep_files.rstrip(',')+' '+container+"\n")
        if isMC:
            fMC.write(comma_sep_files.rstrip(',')+' '+container+"\n")
        #if nb>10:
        #    break;
        samplePatternGlobal=''
else:
    for sampledir in list_file:
        s=VBFAnalysis.sample.sample(sampledir)
        isMC = s.getisMC()
        runNumberS = s.getrunNumberS()
        print 'RunNumber:',runNumberS
        p = subprocess.Popen("ls "+sampledir.strip()+"*/*root*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        samplePatternGlobal = samplePattern+'.'
f.close()
fMC.close()

for syst in systlist:
    print listofrunN
    if args.noSubmit:
        break
    runCommand = '''athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --filesInput "'''+samplePatternGlobal+'''$1" - --currentVariation '''+syst+''' --normFile '''+args.normFile
    if isFileMap:
        runCommand+=''' --containerName $2'''
    writeCondorShell(workDir, buildDir, runCommand, syst, "VBFAnalysisCondorSub", proxyName=args.proxyName, slc7=args.slc7) #writeCondorShell(subDir, buildDir, syst, runCommand, scriptName="VBFAnalysisCondorSub")
    print listofrunN
    writeCondorSub(workDir, syst, "VBFAnalysisCondorSub", listofrunN, listofrunNMC)
