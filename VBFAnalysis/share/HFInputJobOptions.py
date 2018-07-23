#---- Import job config for customized command line inputs ----
from VBFAnalysis.job_configuration import JobConfigurationBase
from glob import glob
#---- Options you could specify on command line -----
jps.AthenaCommonFlags.EvtMax =vars().get("nEvents", -1)                          #set on command-line with: --evtMax=-1
#jps.AthenaCommonFlags.SkipEvents=0                       #set on command-line with: --skipEvents=0
jps.AthenaCommonFlags.FilesInput =[vars().get("input", "~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_Ztot_bkg_fixednom.root")]

config = JobConfigurationBase("JobOptions")
arg_group = config.parser.add_argument_group("JobOptions", "Extra arguments specific to HFInputJobOptions")
arg_group.add_argument("--currentVariation", dest='currentVariation',default="NONE", help="current systematics, default: NONE")
arg_group.add_argument("--currentSamples",dest='currentSample',default="Z_EWK", help="current sample, default: Z_strong")
# parse the commandline options
args = config.parse_args()

jps.AthenaCommonFlags.AccessMode = "TreeAccess"              #Choose from TreeAccess,BranchAccess,ClassAccess,AthenaAccess,POOLAccess
jps.AthenaCommonFlags.TreeName = args.currentSample+"_"+args.currentVariation   #form:"Z_strong_NONE"                    #when using TreeAccess, must specify the input tree name 
jps.AthenaCommonFlags.HistOutputs = ["MYSTREAM:"+args.currentSample+args.currentVariation+".root"]  #register output files like this. MYSTREAM is used in the code

athAlgSeq += CfgMgr.HFInputAlg("HFInputAlg",
                               currentVariation = args.currentVariation,#"NONE",                                
                               currentSample = args.currentSample);#"Z_strong");  


include("AthAnalysisBaseComps/SuppressLogging.py")              #Optional include to suppress as much athena output as possible. Keep at bottom of joboptions so that it doesn't suppress the logging of the things you have configured above

