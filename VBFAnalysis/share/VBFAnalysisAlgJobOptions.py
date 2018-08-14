from AthenaCommon.AppMgr import ServiceMgr
ServiceMgr.MessageSvc.defaultLimit = 9999999  # all messages
ServiceMgr.MessageSvc.OutputLevel = INFO#DEBUG#INFO

#---- Import job config for customized command line inputs ----                                                                                                                                                    
from VBFAnalysis.job_configuration import JobConfigurationBase
#---- Options you could specify on command line -----
jps.AthenaCommonFlags.EvtMax =vars().get("nEvents", -1)                          #set on command-line with: --evtMax=-1 
#jps.AthenaCommonFlags.SkipEvents=0                       #set on command-line with: --skipEvents=0

config = JobConfigurationBase("JobOptions")
arg_group = config.parser.add_argument_group("JobOptions", "Extra arguments specific to VBFAnalysisAlgJobOptions")
arg_group.add_argument("--currentVariation", dest='currentVariation', default="Nominal", help="current systematics, default: Nominal")
arg_group.add_argument("--currentSample", dest='currentSample', default="W_strong", help="current sample, default: Z_strong")
arg_group.add_argument("--runNumberInput", dest='runNumberInput', default= "364162", help="dsid, mcChannelNumber for mc, runNumber for data")
arg_group.add_argument("--isData", action="store_true", dest='isData', default=False, help="isData, default: False")
arg_group.add_argument("--inputDir", dest='inputDir', default="/eos/user/r/rzou/v04/user.othrif.v04.364106.Sherpa_221_NNPDF30NNLO_Zmumu_MAXHTPTV140_280_CVetoBVeto.e5271_s3126_r9364_r9315_p3575_MiniNtuple.root", help="inputDir")
# parse the commandline options

args = config.parse_args()


jps.AthenaCommonFlags.TreeName = "MiniNtuple" 

print str(args.runNumberInput)
from glob import glob
print glob(inputDir+'/*.root*')
INPUT = glob(inputDir+'/*.root*')
jps.AthenaCommonFlags.FilesInput = INPUT 
#["/eos/user/r/rzou/v04/user.othrif.v04.364162.Sherpa_221_NNPDF30NNLO_Wmunu_MAXHTPTV140_280_CVetoBVeto.e5340_s3126_r9364_r9315_p3575_MiniNtuple.root/user.othrif.14790250._000001.MiniNtuple.root"]

jps.AthenaCommonFlags.HistOutputs = ["MYSTREAM:"+args.currentSample+args.currentVariation+str(args.runNumberInput)+".root"]  #optional, register output files like this. MYSTREAM is used in the code

athAlgSeq += CfgMgr.VBFAnalysisAlg("VBFAnalysisAlg",
                               currentVariation = args.currentVariation,
                               currentSample = args.currentSample,
                               isMC = not args.isData,
                               runNumberInput = int(args.runNumberInput));


athAlgSeq += CfgMgr.VBFAnalysisAlg()                               #adds an instance of your alg to the main alg sequence
include("AthAnalysisBaseComps/SuppressLogging.py") #optional line
