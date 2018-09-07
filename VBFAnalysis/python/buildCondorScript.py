#!/usr/bin/env python 
import os

def writeCondorShell(subDir, buildDir, runCommand, syst, scriptName="VBFAnalysisCondorSub", proxyName='/home/schae/testarea/HInv/run/x509up_u20186'):
    os.system('''echo "#!/bin/bash" > '''+subDir+'''/'''+scriptName+syst+'''.sh''')
    os.system("echo 'export HOME=$(pwd)' >> "+subDir+"/"+scriptName+syst+".sh")
    os.system("echo 'export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase' >> "+subDir+"/"+scriptName+syst+".sh")
    os.system("echo 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet' >> "+subDir+"/"+scriptName+syst+".sh")
    os.system("echo 'asetup AthAnalysis,21.2.35,here' >> "+subDir+"/"+scriptName+syst+".sh")
    os.system("echo 'source "+buildDir+"/${CMTCONFIG}/setup.sh' >> "+subDir+"/"+scriptName+syst+".sh")
    os.system("echo 'export X509_USER_PROXY="+proxyName+"' >> "+subDir+"/"+scriptName+syst+".sh")
    os.system('''echo ' echo INPUT:$1 $2' >> '''+subDir+'''/'''+scriptName+syst+'''.sh''')
    os.system('''echo ' echo '''+runCommand+'''' >> '''+subDir+'''/'''+scriptName+syst+'''.sh''')
    os.system('''echo ' '''+runCommand+'''' >> '''+subDir+'''/'''+scriptName+syst+'''.sh''')
    os.system("chmod 777 "+subDir+"/"+scriptName+syst+".sh")

def writeCondorSub(workDir, syst="Nominal", scriptName="VBFAnalysisCondorSub", fileForArguments="filelist",fileForArgumentsSys=""):
    os.system("echo 'universe                = vanilla' > "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'executable              = "+workDir+"/"+scriptName+syst+".sh' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'output                  = "+workDir+"/output$(ClusterId).$(ProcId)' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'error                   = "+workDir+"/error$(ClusterId).$(ProcId)' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'log                     = "+workDir+"/log$(ClusterId)' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("echo 'max_retries = 5' >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system('''echo "+JobFlavour = 'tomorrow'" >> '''+workDir+'''/submit_this_python'''+syst+'''.sh''')
    os.system("echo '' >> "+workDir+"/submit_this_python"+syst+".sh")
    if syst == "Nominal":
        os.system("echo 'queue arguments from '"+fileForArguments+" >> "+workDir+"/submit_this_python"+syst+".sh")
    else:
        if fileForArgumentsSys == "":
            fileForArgumentsSys = fileForArguments
        os.system("echo 'queue arguments from '"+fileForArgumentsSys+" >> "+workDir+"/submit_this_python"+syst+".sh")
    os.system("chmod 777 "+workDir+"/submit_this_python"+syst+".sh")
    os.system("condor_submit "+workDir+"/submit_this_python"+syst+".sh")
