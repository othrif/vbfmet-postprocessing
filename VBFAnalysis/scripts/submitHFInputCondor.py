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
parser.add_argument( "--slc7", dest = "slc7", action="store_true", default = False, help = "Do slc7 for chicago tier3" )
parser.add_argument( "--metOptSyst", dest = "metOptSyst", action="store_true", default = False, help = "Do only the met optimization systematics" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-i", "--inputDir",  type = str, dest = "inputDir", default = "/eos/user/r/rzou/v04/microtuples/", help = "dir for input file")
parser.add_argument( "--noSubmit", dest = "noSubmit", action="store_true", default = False, help = "Dont submit jobs" )
parser.add_argument("--extraVars", dest='extraVars', default="7", help="extraVars, 1=cut on the new variables for leptons veto, 2=loosen cuts, 3=no soft met cut default: 7, 5=met OR lep trig CR, 6=met trig CR, 7=corrected SF for v31")
parser.add_argument("--Binning", dest='Binning', default="11", help="Binning, 11=default, 0=Mjj binning, 1=low MET bin, 2=njet>2 binning, 3=met binning, 4=3bins for nj>2, 5=3dphibin, 6= dphi by mjj+nj>2, 7=800mjj withdphi, 8=mjj 8bins")
parser.add_argument( "--isMadgraph", dest = "isMadgraph", action="store_true", default = False, help = "Use the madgraph samples" )
parser.add_argument( "--mergeKTPTV", dest = "mergeKTPTV", action="store_true", default = False, help = "Use the kt filtered sherpa samples" )
parser.add_argument( "--doTMVA", dest = "doTMVA", action="store_true", default = False, help = "Use the variable filled as tmva for the fitting" )
parser.add_argument( "--doDoubleRatio", dest = "doDoubleRatio", action="store_true", default = False, help = "Use this variable to run the double ratio inputs")
parser.add_argument( "--doPlot", dest = "doPlot", action="store_true", default = False, help = "Generate additional histograms for postfit plots")
parser.add_argument( "--v26Ntuples", dest = "v26Ntuples", action="store_true", default = False, help = "Run version 26 style ntuples. important for lepton selection")
parser.add_argument( "--doVBFMETGam", dest = "doVBFMETGam", action="store_true", default = False, help = "VBF + MET + photon analysis")
parser.add_argument( "--singleHist", dest = "singleHist", action="store_true", default = False, help = "Runs VBF + MET in one histogram when true")
parser.add_argument("--year", type=int, dest='year', default=2016, help="year, default: 2016 - 2017 or 2018 for those years")
parser.add_argument("--METCut", type=int, dest='METCut', default=160e3, help="METCut, default: 160 MeV")
parser.add_argument("--METDef", dest='METDef', default='0', help="met definition, default: 0=loose, 1=tenacious")
args, unknown = parser.parse_known_args()

if not args.doVBFMETGam:
    writeMultiJet(int(args.Binning), args.year, doDoubleRatio=args.doDoubleRatio, METCut=int(args.METCut/1e3), singleHist=args.singleHist)
    writeFakeEle(int(args.Binning), args.year, doDoubleRatio=args.doDoubleRatio, singleHist=args.singleHist,METCut=int(args.METCut/1e3))

### Load systematics list from VBFAnalysis/python/systematics.py ###
if args.nominal:
    sys = VBFAnalysis.systematics.systematics("Nominal")
    asys_systlist = []
    wsys_systlist = []
elif args.metOptSyst:
    sys = VBFAnalysis.systematics.systematics("METSystOpt")
    asys = VBFAnalysis.systematics.systematics("OneSided")
    wsys = VBFAnalysis.systematics.systematics("WeightSyst")
    asys_systlist = asys.getsystematicsList()
    wsys_systlist = wsys.getsystematicsList()
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
#buildDir = workDir[:workDir.find("/run/")]+"/build"
CMTCONFIG = os.getenv('CMTCONFIG')
buildPaths = os.getenv('CMAKE_PREFIX_PATH')
buildPathsVec = buildPaths.split(':')
buildDir =  buildPathsVec[0][:buildPathsVec[0].find(CMTCONFIG)].rstrip('/')
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)

listoffiles = workDir+"/filelist"
listoffilesMC = workDir+"/filelistMC"
listoffilesVBFMC = workDir+"/filelistVBFMC"
listoffilesGGFMC = workDir+"/filelistGGFMC"
listoffilesGGFVBFMC = workDir+"/filelistGGFVBFMC"
listoffilesZstrongMC = workDir+"/filelistZstrongMC"
listoffilesWstrongMC = workDir+"/filelistWstrongMC"
listoffilesWewkMC = workDir+"/filelistWewkMC"
listoffilesZewkMC = workDir+"/filelistZewkMC"
f = open(listoffiles, 'w')
fMC = open(listoffilesMC, 'w')
fVBFMC = open(listoffilesVBFMC, 'w')
fGGFMC = open(listoffilesGGFMC, 'w')
fGGFVBFMC = open(listoffilesGGFVBFMC, 'w')
fZstrongMC = open(listoffilesZstrongMC, 'w')
fWstrongMC = open(listoffilesWstrongMC, 'w')
fWewkMC = open(listoffilesWewkMC, 'w')
fZewkMC = open(listoffilesZewkMC, 'w')
samplePatternGlobal = ""
p = subprocess.Popen("ls "+args.inputDir+"*root*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    filepath = line.strip()
    f.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] != "data"):
        fMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "VBFH"):
        fVBFMC.write(filepath+"\n")
        fGGFVBFMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "ggFH"):
        fGGFMC.write(filepath+"\n")
        fGGFVBFMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "Z_st"):
        fZstrongMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "Z_EW"):
        fZewkMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "W_st"):
        fWstrongMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "W_EW"):
        fWewkMC.write(filepath+"\n")
f.close()
fMC.close()
fVBFMC.close()
fGGFMC.close()
fGGFVBFMC.close()
fZstrongMC.close()
fWstrongMC.close()
fZewkMC.close()
fWewkMC.close()

extraCommand=''
if args.extraVars:
    extraCommand=' --extraVars '+args.extraVars
if args.isMadgraph:
    extraCommand+=' --isMadgraph '
if args.mergeKTPTV:
    extraCommand+=' --mergeKTPTV '
if args.METDef!="0":
    extraCommand+=' --METDef '+args.METDef+' '
if args.year!=2016:
    extraCommand+=' --year %s ' %(args.year)
if args.METCut!=160e3:
    extraCommand+=' --METCut %s ' %(args.METCut)
if args.doTMVA:
    extraCommand+=' --doTMVA '
if args.doDoubleRatio:
    extraCommand+=' --doDoubleRatio '
if args.v26Ntuples:
    extraCommand+=' --v26Ntuples '
if args.singleHist:
    extraCommand+=' --singleHist '
if args.doVBFMETGam:
    extraCommand+=' --doVBFMETGam '
if args.doPlot:
    extraCommand+=' --doPlot '
extraCommand+=' --Binning '+args.Binning


for syst in systlist:
    MCFileListToUse = listoffilesMC
    isLow = ""    
    if "__1down" in syst or "Down" in syst:
        isLow = " --isLow"
    if syst in wsys_systlist:
        isLow+=' --weightSyst'
    if syst in sys.getsystematicsOneSidedMap().keys():
        print 'Skipping one sided systematic: ',syst
        continue
    if syst in sys.systematicsVBFSignal:
        MCFileListToUse=listoffilesVBFMC
    if syst in sys.systematicsGGFSignal:
        MCFileListToUse=listoffilesGGFMC
    if syst in sys.systematicsSignalPDF:
        MCFileListToUse=listoffilesGGFVBFMC
    if syst in sys.systematicsZewkTheory:
        MCFileListToUse=listoffilesZewkMC
    if syst in sys.systematicsZstrongTheory:
        MCFileListToUse=listoffilesZstrongMC
    if syst in sys.systematicsWstrongTheory:
        MCFileListToUse=listoffilesWstrongMC
    if syst in sys.systematicsWewkTheory:
        MCFileListToUse=listoffilesWewkMC
    runCommand = '''athena VBFAnalysis/HFInputJobOptions.py --filesInput "$1" - --currentVariation '''+syst+isLow+extraCommand
    print runCommand
    if not args.noSubmit:
        writeCondorShell(workDir, buildDir, runCommand, syst, "HFInputCondorSub", slc7=args.slc7)
        writeCondorSub(workDir, syst, "HFInputCondorSub", listoffiles, MCFileListToUse)


# The low one sided systematics can be handled in the fitting. just call symmeterize in hist fitter
#for syst in asys_systlist:
#    runCommand = '''athena VBFAnalysis/HFInputJobOptions.py --filesInput "$1" - --currentVariation '''+syst+" --doLowNom"+extraCommand
#    print runCommand
#    writeCondorShell(workDir, buildDir, runCommand, syst, "HFInputCondorSub")
#    writeCondorSub(workDir, syst, "HFInputCondorSub", listoffiles, listoffilesMC)

