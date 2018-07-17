#Skeleton joboption for a simple analysis job

#---- Minimal job options -----
from glob import glob
jps.AthenaCommonFlags.AccessMode = "TreeAccess"              #Choose from TreeAccess,BranchAccess,ClassAccess,AthenaAccess,POOLAccess
jps.AthenaCommonFlags.TreeName = "W_strong_NONE"                    #when using TreeAccess, must specify the input tree name

jps.AthenaCommonFlags.HistOutputs = ["MYSTREAM:myfile.root"]  #register output files like this. MYSTREAM is used in the code

athAlgSeq += CfgMgr.HFInputAlg()                               #adds an instance of your alg to the main alg sequence


#---- Options you could specify on command line -----
jps.AthenaCommonFlags.EvtMax =vars().get("nEvents", -1)                          #set on command-line with: --evtMax=-1
#jps.AthenaCommonFlags.SkipEvents=0                       #set on command-line with: --skipEvents=0
jps.AthenaCommonFlags.FilesInput =[vars().get("input", "~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_Wtot_bkgcomplete_fixednom.root")]







include("AthAnalysisBaseComps/SuppressLogging.py")              #Optional include to suppress as much athena output as possible. Keep at bottom of joboptions so that it doesn't suppress the logging of the things you have configured above

