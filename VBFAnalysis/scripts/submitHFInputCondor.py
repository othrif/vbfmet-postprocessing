#!/usr/bin/env python

import os
import sys
import argparse

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", type = bool, dest = "nominal", default = False, help = "Do nominal only" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
args, unknown = parser.parse_known_args()

if args.nominal:
    syslist = ["NONE"]
else:
    systlist = ["NONE", "JET_EtaIntercalibration_NonClosure__1down","EG_RESOLUTION_ALL__1down", "EG_RESOLUTION_ALL__1up", "EG_SCALE_ALL__1down", "EG_SCALE_ALL__1up", "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down",  "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up", "JET_EtaIntercalibration_NonClosure__1down", "JET_EtaIntercalibration_NonClosure__1up", "JET_BJES_Response__1up",   "JET_BJES_Response__1down",   "JET_EffectiveNP_Detector1__1up",   "JET_EffectiveNP_Detector1__1down",   "JET_EffectiveNP_Detector2__1up",   "JET_EffectiveNP_Detector2__1down",   "JET_EffectiveNP_Mixed1__1up",   "JET_EffectiveNP_Mixed1__1down",   "JET_EffectiveNP_Mixed2__1up",   "JET_EffectiveNP_Mixed2__1down",   "JET_EffectiveNP_Mixed3__1up",   "JET_EffectiveNP_Mixed3__1down",   "JET_EffectiveNP_Modelling1__1up",   "JET_EffectiveNP_Modelling1__1down",   "JET_EffectiveNP_Modelling2__1up",   "JET_EffectiveNP_Modelling2__1down",   "JET_EffectiveNP_Modelling3__1up",   "JET_EffectiveNP_Modelling3__1down",   "JET_EffectiveNP_Modelling4__1up",   "JET_EffectiveNP_Modelling4__1down",   "JET_EffectiveNP_Statistical1__1up",   "JET_EffectiveNP_Statistical1__1down",   "JET_EffectiveNP_Statistical2__1up",   "JET_EffectiveNP_Statistical2__1down",   "JET_EffectiveNP_Statistical3__1up",   "JET_EffectiveNP_Statistical3__1down",   "JET_EffectiveNP_Statistical4__1up",   "JET_EffectiveNP_Statistical4__1down",   "JET_EffectiveNP_Statistical5__1up",   "JET_EffectiveNP_Statistical5__1down",   "JET_EffectiveNP_Statistical6__1up",   "JET_EffectiveNP_Statistical6__1down",   "JET_EffectiveNP_Statistical7__1up",   "JET_EffectiveNP_Statistical7__1down",   "JET_EtaIntercalibration_Modelling__1up",   "JET_EtaIntercalibration_Modelling__1down", "JET_EtaIntercalibration_TotalStat__1up",   "JET_EtaIntercalibration_TotalStat__1down",   "JET_Flavor_Composition__1up",   "JET_Flavor_Composition__1down",   "JET_Flavor_Response__1up",   "JET_Flavor_Response__1down", "JET_Pileup_OffsetMu__1up",   "JET_Pileup_OffsetMu__1down",   "JET_Pileup_OffsetNPV__1up",   "JET_Pileup_OffsetNPV__1down",   "JET_Pileup_PtTerm__1up",   "JET_Pileup_PtTerm__1down",   "JET_Pileup_RhoTopology__1up",   "JET_Pileup_RhoTopology__1down",   "JET_PunchThrough_MC15__1up",   "JET_PunchThrough_MC15__1down",   "JET_SingleParticle_HighPt__1up",   "JET_SingleParticle_HighPt__1down", "JET_JER_SINGLE_NP__1up", "JET_JvtEfficiency__1down", "JET_JvtEfficiency__1up", "MUON_EFF_STAT__1down", "MUON_EFF_STAT__1up", "MUON_EFF_SYS__1down", "MUON_EFF_SYS__1up", "MUON_EFF_TrigStatUncertainty__1down", "MUON_EFF_TrigStatUncertainty__1up", "MUON_EFF_TrigSystUncertainty__1down", "MUON_EFF_TrigSystUncertainty__1up", "MUON_ID__1down", "MUON_ID__1up", "MUON_ISO_STAT__1down", "MUON_ISO_STAT__1up", "MUON_ISO_SYS__1down", "MUON_ISO_SYS__1up", "MUON_MS__1down", "MUON_MS__1up", "MUON_SAGITTA_RESBIAS__1down", "MUON_SAGITTA_RESBIAS__1up", "MUON_SAGITTA_RHO__1down", "MUON_SAGITTA_RHO__1up", "MUON_SCALE__1down", "MUON_SCALE__1up", "MUON_TTVA_STAT__1down", "MUON_TTVA_STAT__1up", "MUON_TTVA_SYS__1down", "MUON_TTVA_SYS__1up", "PRW_DATASF__1down", "PRW_DATASF__1up", "MET_SoftTrk_ResoPara", "MET_SoftTrk_ResoPerp", "MET_SoftTrk_ScaleDown", "MET_SoftTrk_ScaleUp"]

workDir = os.getcwd()+"/"+args.submitDir
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)
for sys in systlist:
    os.system("echo 'cd " + str(workDir) + "/../../build/' > "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'asetup AthAnalysis,21.2.35,here' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'cd " + str(workDir) + "' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'source ../../build/${CMTCONFIG}/setup.sh' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
    os.system("echo 'python "+workDir+"/../../source/STPostProcessing/VBFAnalysis/scripts/LoopOverHF.py -s "+sys+"' >> "+args.submitDir+"/HFInputCondorSub"+sys+".sh")
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
