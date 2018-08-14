#!/usr/bin/env python

import os
import sys
import argparse

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-l", "--listSample", type = str, dest = "listSample", default = "/eos/user/r/rzou/v04/list", help = "list of ntuples to run over" )
args, unknown = parser.parse_known_args()

if args.nominal:
    systlist = ["Nominal"]
else:
    systlist = ["Nominal", "EG_RESOLUTION_ALL__1down", "EG_RESOLUTION_ALL__1up", "EG_SCALE_ALL__1down", "EG_SCALE_ALL__1up", "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down",  "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up", "JET_EtaIntercalibration_NonClosure__1down", "JET_EtaIntercalibration_NonClosure__1up", "JET_BJES_Response__1up",   "JET_BJES_Response__1down",   "JET_EffectiveNP_Detector1__1up",   "JET_EffectiveNP_Detector1__1down",   "JET_EffectiveNP_Detector2__1up",   "JET_EffectiveNP_Detector2__1down",   "JET_EffectiveNP_Mixed1__1up",   "JET_EffectiveNP_Mixed1__1down",   "JET_EffectiveNP_Mixed2__1up",   "JET_EffectiveNP_Mixed2__1down",   "JET_EffectiveNP_Mixed3__1up",   "JET_EffectiveNP_Mixed3__1down",   "JET_EffectiveNP_Modelling1__1up",   "JET_EffectiveNP_Modelling1__1down",   "JET_EffectiveNP_Modelling2__1up",   "JET_EffectiveNP_Modelling2__1down",   "JET_EffectiveNP_Modelling3__1up",   "JET_EffectiveNP_Modelling3__1down",   "JET_EffectiveNP_Modelling4__1up",   "JET_EffectiveNP_Modelling4__1down",   "JET_EffectiveNP_Statistical1__1up",   "JET_EffectiveNP_Statistical1__1down",   "JET_EffectiveNP_Statistical2__1up",   "JET_EffectiveNP_Statistical2__1down",   "JET_EffectiveNP_Statistical3__1up",   "JET_EffectiveNP_Statistical3__1down",   "JET_EffectiveNP_Statistical4__1up",   "JET_EffectiveNP_Statistical4__1down",   "JET_EffectiveNP_Statistical5__1up",   "JET_EffectiveNP_Statistical5__1down",   "JET_EffectiveNP_Statistical6__1up",   "JET_EffectiveNP_Statistical6__1down",   "JET_EffectiveNP_Statistical7__1up",   "JET_EffectiveNP_Statistical7__1down",   "JET_EtaIntercalibration_Modelling__1up",   "JET_EtaIntercalibration_Modelling__1down", "JET_EtaIntercalibration_TotalStat__1up",   "JET_EtaIntercalibration_TotalStat__1down",   "JET_Flavor_Composition__1up",   "JET_Flavor_Composition__1down",   "JET_Flavor_Response__1up",   "JET_Flavor_Response__1down", "JET_Pileup_OffsetMu__1up",   "JET_Pileup_OffsetMu__1down",   "JET_Pileup_OffsetNPV__1up",   "JET_Pileup_OffsetNPV__1down",   "JET_Pileup_PtTerm__1up",   "JET_Pileup_PtTerm__1down",   "JET_Pileup_RhoTopology__1up",   "JET_Pileup_RhoTopology__1down",   "JET_PunchThrough_MC15__1up",   "JET_PunchThrough_MC15__1down",   "JET_SingleParticle_HighPt__1up",   "JET_SingleParticle_HighPt__1down", "JET_JER_SINGLE_NP__1up", "JET_JvtEfficiency__1down", "JET_JvtEfficiency__1up", "MUON_EFF_STAT__1down", "MUON_EFF_STAT__1up", "MUON_EFF_SYS__1down", "MUON_EFF_SYS__1up", "MUON_EFF_TrigStatUncertainty__1down", "MUON_EFF_TrigStatUncertainty__1up", "MUON_EFF_TrigSystUncertainty__1down", "MUON_EFF_TrigSystUncertainty__1up", "MUON_ID__1down", "MUON_ID__1up", "MUON_ISO_STAT__1down", "MUON_ISO_STAT__1up", "MUON_ISO_SYS__1down", "MUON_ISO_SYS__1up", "MUON_MS__1down", "MUON_MS__1up", "MUON_SAGITTA_RESBIAS__1down", "MUON_SAGITTA_RESBIAS__1up", "MUON_SAGITTA_RHO__1down", "MUON_SAGITTA_RHO__1up", "MUON_SCALE__1down", "MUON_SCALE__1up", "MUON_TTVA_STAT__1down", "MUON_TTVA_STAT__1up", "MUON_TTVA_SYS__1down", "MUON_TTVA_SYS__1up", "PRW_DATASF__1down", "PRW_DATASF__1up", "MET_SoftTrk_ResoPara", "MET_SoftTrk_ResoPerp", "MET_SoftTrk_ScaleDown", "MET_SoftTrk_ScaleUp"]
list_file = open(args.listSample, "r")
runNumber = 0

workDir = os.getcwd()+"/"+args.submitDir
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)                

def writeCondorSub(subDir, sys, runNumber,isMC, sample, insample):
    if isMC:
        isData = ""
        mc = "MC"
    else:
        isData = " --isData"
        mc = ""
    print 'athena VBFAnalysis/VBFAnalysisAlgJobOptions.py - --currentSample '+sample+' --currentVariation '+syst+' --runNumber '+str(runNumber)+isData+' --inputDir '+insample
    if isMC or sys == "Nominal":
        os.system('''echo "#!/bin/bash" > '''+subDir+'''/VBFAnalysisCondorSub'''+mc+sys+str(runNumber)+'''.sh''')
        os.system("echo 'export HOME=$(pwd)' >> "+subDir+"/VBFAnalysisCondorSub"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase' >> "+subDir+"/VBFAnalysisCondorSub"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet' >> "+subDir+"/VBFAnalysisCondorSub"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'asetup AthAnalysis,21.2.35,here' >> "+subDir+"/VBFAnalysisCondorSub"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'source "+workDir+"/../../build/${CMTCONFIG}/setup.sh' >> "+subDir+"/VBFAnalysisCondorSub"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'athena VBFAnalysis/VBFAnalysisAlgJobOptions.py - --currentSample "+sample+" --currentVariation "+syst+" --runNumber "+str(runNumber)+isData+" --inputDir "+insample+" ' >> "+subDir+"/VBFAnalysisCondorSub"+mc+sys+str(runNumber)+".sh")
        os.system("chmod 777 "+subDir+"/VBFAnalysisCondorSub"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'universe                = vanilla' > "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'executable              = "+workDir+"/VBFAnalysisCondorSub"+sys+str(runNumber)+".sh' >> "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'output                  = "+workDir+"/output"+mc+sys+str(runNumber)+"' >> "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'error                   = "+workDir+"/error"+mc+sys+str(runNumber)+"' >> "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh") 
        os.system("echo 'log                     = "+workDir+"/log"+mc+sys+str(runNumber)+"' >> "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh") 
        os.system('''echo "+JobFlavour = 'tomorrow'" >> '''+subDir+'''/submit_this_python'''+mc+sys+str(runNumber)+'''.sh''') 
        os.system("echo '' >> "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh")
        os.system("echo 'queue' >> "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh")
        os.system("chmod 777 "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh")
        os.system("condor_submit "+subDir+"/submit_this_python"+mc+sys+str(runNumber)+".sh")                                                              
    

for syst in systlist:
    for sample in list_file:
        samplesplit = sample.split(".")
        for p,s in enumerate(samplesplit):
            if s[0]=="v":
                runNumber = int(samplesplit[p+1]) 
            
        if "physics_Main" in samplesplit:
            isMC = False
        else:
            isMC = True
        if (isMC):
            if ((runNumber >= 308096 and runNumber <= 308098) or (runNumber == 363359) or (runNumber == 363360) or (runNumber == 363489)):
                currentSample = "W_EWK"
            elif (runNumber >= 364156 and runNumber <= 364197):
                currentSample = "W_strong"
            elif ((runNumber >= 308092 and runNumber <= 308095) or (runNumber >= 363355 and runNumber <= 363358)):
                currentSample = "Z_EWK"
            elif (runNumber >= 364100 and runNumber <= 364155):
                currentSample = "Z_strong"
            elif ((runNumber >= 410011 and runNumber <= 410014) or (runNumber == 410025) or (runNumber == 410026) or (runNumber == 410470) or (runNumber == 410471)):
                currentSample = "ttbar"
            elif ((runNumber == 308276) or (runNumber == 308567)):
                currentSample = "VBFH125"
            elif (runNumber == 308284):
                currentSample = "ggFH125"
            elif ((runNumber == 308071) or (runNumber == 308072)):
                currentSample = "VH125"
            else:
                print "runNumber "+str(runNumber)+" could not be identified as a valid MC :o"
                break
  #                                                                                                                                                                                                               
  # Signal:  VBF: 308276,308567, ggF: 308284, VH: 308071,308072                                                                                                                                                   
  # Diboson: W: 363359-363360, 363489, Z: 363355-363358                                                                                                                                                           
  # Wenu:    strong 364170-364183, EWK 308096                                                                                                                                                                     
  # Wmunu:   strong 364156-364169, EWK 308097                                                                                                                                                                     
  # Wtaunu:  strong 364184-364197, EWK 308098                                                                                                                                                                     
  # Zee:     strong 364114-364127, EWK 308092                                                                                                                                                                     
  # Zmumu:   strong 364100-364113, EWK 308093                                                                                                                                                                     
  # Ztautau: strong 364128-364141, EWK 308094                                                                                                                                                                     
  # Znunu:   strong 364142-364155, EWK 308095                                                                                                                                                                     
  # SingleTop: 410011-410014,410025,410026,ttbar:410470,410471                                                                                                                                                    
  # Other higgs: 308275-308283                                                                                                                                                                                    
  #                                                                                                                                                                                                               
        else:
            currentSample = "data"
        writeCondorSub(args.submitDir, syst, runNumber, isMC, currentSample, sample)
#        print "athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --filesInput "+sample+" - --currentSample "+currentSample+" --currentVariation "+syst+" --runNumber "+str(runNumber)

# workDir = os.getcwd()+"/"+args.submitDir
# os.system("rm -rf "+workDir)
# os.system("mkdir "+workDir)
# for sys in systlist:
#     isLow = ""
#     if "__1down" in sys or "Down" in sys:
#         isLow = " --isLow"
#     os.system('''echo "#!/bin/bash" > '''+args.submitDir+'''/VBFAnalysisCondorSub'''+sys+str(runNumber)+'''.sh''')
#     os.system("echo 'export HOME=$(pwd)' >> "+args.submitDir+"/VBFAnalysisCondorSub"+sys+str(runNumber)+".sh")
#     os.system("echo 'export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase' >> "+args.submitDir+"/VBFAnalysisCondorSub"+sys+str(runNumber)+".sh")
#     os.system("echo 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet' >> "+args.submitDir+"/VBFAnalysisCondorSub"+sys+str(runNumber)+".sh")
#     os.system("echo 'asetup AthAnalysis,21.2.35,here' >> "+args.submitDir+"/VBFAnalysisCondorSub"+sys+str(runNumber)+".sh")
#     os.system("echo 'source "+workDir+"/../../build/${CMTCONFIG}/setup.sh' >> "+args.submitDir+"/VBFAnalysisCondorSub"+sys+str(runNumber)+".sh")
#     os.system("echo 'python "+workDir+"/../../source/STPostProcessing/VBFAnalysis/scripts/LoopOverHF.py -s "+sys+isLow+"' >> "+args.submitDir+"/VBFAnalysisCondorSub"+sys+str(runNumber)+".sh")
#     os.system("chmod 777 "+args.submitDir+"/VBFAnalysisCondorSub"+sys+str(runNumber)+".sh")
#     os.system("echo 'universe                = vanilla' > "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")
#     os.system("echo 'executable              = "+workDir+"/VBFAnalysisCondorSub"+sys+".sh' >> "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")
#     os.system("echo 'output                  = "+workDir+"/output"+sys+"' >> "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")
#     os.system("echo 'error                   = "+workDir+"/error"+sys+"' >> "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")
#     os.system("echo 'log                     = "+workDir+"/log"+sys+"' >> "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")
#     os.system('''echo "+JobFlavour = 'tomorrow'" >> '''+args.submitDir+'''/submit_this_python'''+sys+str(runNumber)+'''.sh''')
#     os.system("echo '' >> "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")
#     os.system("echo 'queue' >> "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")
#     os.system("chmod 777 "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")

#     os.system("condor_submit "+args.submitDir+"/submit_this_python"+sys+str(runNumber)+".sh")
