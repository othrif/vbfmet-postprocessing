#---- Import job config for customized command line inputs ----
from VBFAnalysis.job_configuration import JobConfigurationBase
from glob import glob
#---- Options you could specify on command line -----
jps.AthenaCommonFlags.EvtMax =vars().get("nEvents", -1)                          #set on command-line with: --evtMax=-1
#jps.AthenaCommonFlags.SkipEvents=0                       #set on command-line with: --skipEvents=0
jps.AthenaCommonFlags.FilesInput =[vars().get("input", "~/eosvbfinv/FinalNtuplesJuly18/VBFHiggsInv_Ztot_bkg_fixednom.root")]

config = JobConfigurationBase("JobOptions")
arg_group = config.parser.add_argument_group("JobOptions", "Extra arguments specific to HFInputJobOptions")
arg_group.add_argument("--currentVariation", dest='currentVariation', default="NONE", help="current systematics, default: NONE")
arg_group.add_argument("--currentSamples", dest='currentSample', default="Z_EWK", help="current sample, default: Z_strong")
arg_group.add_argument("--isData", action="store_true", dest='isData', default=False, help="isData, default: False")
arg_group.add_argument("--doLowNom", action="store_true", dest='doLowNom', default=False, help="doLowNom, to symmetrize asymmetric syst, default: False")
arg_group.add_argument("--isLow", action="store_true", dest='isLow', default=False, help="isLow, default: False")
# parse the commandline options
args = config.parse_args()

doLowNom_str = ""
if (args.doLowNom):
    doLowNom_str = "Low"

jps.AthenaCommonFlags.AccessMode = "TreeAccess"              #Choose from TreeAccess,BranchAccess,ClassAccess,AthenaAccess,POOLAccess
jps.AthenaCommonFlags.TreeName = args.currentSample+"_"+args.currentVariation   #form:"Z_strong_NONE"                    #when using TreeAccess, must specify the input tree name 
jps.AthenaCommonFlags.HistOutputs = ["MYSTREAM:"+args.currentSample+args.currentVariation+doLowNom_str+".root"]  #register output files like this. MYSTREAM is used in the code

athAlgSeq += CfgMgr.HFInputAlg("HFInputAlg",
                               currentVariation = args.currentVariation,#"NONE",                                
                               currentSample = args.currentSample,
                               isMC = not args.isData,
                               doLowNom = args.doLowNom,
                               isHigh = not args.isLow);#"Z_strong");  


include("AthAnalysisBaseComps/SuppressLogging.py")              #Optional include to suppress as much athena output as possible. Keep at bottom of joboptions so that it doesn't suppress the logging of the things you have configured above

