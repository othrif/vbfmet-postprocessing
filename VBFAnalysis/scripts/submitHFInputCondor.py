#!/usr/bin/env python

import os
import sys
import argparse
import VBFAnalysis.systematics

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-i", "--inputDir",  type = str, dest = "inputDir", default = "/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/FinalNtuplesJuly18", help = "dir for input file")
args, unknown = parser.parse_known_args()


### Load systematics list from VBFAnalysis/python/systematics.py ###
if args.nominal:
    sys = VBFAnalysis.systematics.systematics("Nominal")
else:
    sys = VBFAnalysis.systematics.systematics("All")
systlist = sys.getsystematicsList()
print systlist

asys = VBFAnalysis.systematics.systematics("Asym")
asy_systlist = asys.getsystematicsList()

workDir = os.getcwd()+"/"+args.submitDir
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)
for sys in systlist:
    isLow = ""
    if "__1down" in sys or "Down" in sys:
        isLow = " --isLow"
    os.system('''echo "#!/bin/bash" > '''+args.submitDir+'''/HFInputCondorSub'''+sys+'''.sh''')
    os.system("echo 'export HOME=$(pwd)' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'asetup AthAnalysis,21.2.35,here' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'source "+workDir+"/../../build/${CMTCONFIG}/setup.sh' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'python "+workDir+"/../../source/STPostProcessing/VBFAnalysis/scripts/LoopOverHF.py -s "+sys+isLow+" -i "+inputDir+"' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("chmod 777 "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'universe                = vanilla' > "+args.submitDir+"/submit_this_python"+sys+".sh")
    os.system("echo 'executable              = "+workDir+"/HFInputCondorSub"+sys+".sh' >> "+args.submitDir+"/submit_this_python"+sys+".sh")
    os.system("echo 'output                  = "+workDir+"/output"+sys+"' >> "+args.submitDir+"/submit_this_python"+sys+".sh")
    os.system("echo 'error                   = "+workDir+"/error"+sys+"' >> "+args.submitDir+"/submit_this_python"+sys+".sh")
    os.system("echo 'log                     = "+workDir+"/log"+sys+"' >> "+args.submitDir+"/submit_this_python"+sys+".sh")
    os.system('''echo "+JobFlavour = 'tomorrow'" >> '''+args.submitDir+'''/submit_this_python'''+sys+'''.sh''')
    os.system("echo '' >> "+args.submitDir+"/submit_this_python"+sys+".sh")
    os.system("echo 'queue' >> "+args.submitDir+"/submit_this_python"+sys+".sh")
    os.system("chmod 777 "+args.submitDir+"/submit_this_python"+sys+".sh")

    os.system("condor_submit "+args.submitDir+"/submit_this_python"+sys+".sh")

for sys in asy_systlist:
    syslow = sys+"low"
    os.system('''echo "#!/bin/bash" > '''+args.submitDir+'''/HFInputCondorSub'''+syslow+'''.sh''')
    os.system("echo 'export HOME=$(pwd)' >> "+args.submitDir+"/HFInputCondorSub"+syslow+".sh")
    os.system("echo 'export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase' >> "+args.submitDir+"/HFInputCondorSub"+syslow+".sh")
    os.system("echo 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet' >> "+args.submitDir+"/HFInputCondorSub"+syslow+".sh")
    os.system("echo 'asetup AthAnalysis,21.2.35,here' >> "+args.submitDir+"/HFInputCondorSub"+syslow+".sh")
    os.system("echo 'source "+workDir+"/../../build/${CMTCONFIG}/setup.sh' >> "+args.submitDir+"/HFInputCondorSub"+syslow+".sh")
    os.system("echo 'python "+workDir+"/../../source/STPostProcessing/VBFAnalysis/scripts/LoopOverHF.py -s "+sys+" --doLowNom"+" -i "+inputDir+"' >> "+args.submitDir+"/HFInputCondorSub"+syslow+".sh")
    os.system("chmod 777 "+args.submitDir+"/HFInputCondorSub"+syslow+".sh")
    os.system("echo 'universe                = vanilla' > "+args.submitDir+"/submit_this_python"+syslow+".sh")
    os.system("echo 'executable              = "+workDir+"/HFInputCondorSub"+syslow+".sh' >> "+args.submitDir+"/submit_this_python"+syslow+".sh")
    os.system("echo 'output                  = "+workDir+"/output"+syslow+"' >> "+args.submitDir+"/submit_this_python"+syslow+".sh")
    os.system("echo 'error                   = "+workDir+"/error"+syslow+"' >> "+args.submitDir+"/submit_this_python"+syslow+".sh")
    os.system("echo 'log                     = "+workDir+"/log"+syslow+"' >> "+args.submitDir+"/submit_this_python"+syslow+".sh")
    os.system('''echo "+JobFlavour = 'tomorrow'" >> '''+args.submitDir+'''/submit_this_python'''+syslow+'''.sh''')
    os.system("echo '' >> "+args.submitDir+"/submit_this_python"+syslow+".sh")
    os.system("echo 'queue' >> "+args.submitDir+"/submit_this_python"+syslow+".sh")
    os.system("chmod 777 "+args.submitDir+"/submit_this_python"+syslow+".sh")

    os.system("condor_submit "+args.submitDir+"/submit_this_python"+syslow+".sh")
