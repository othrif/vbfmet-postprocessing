from AthenaCommon.AppMgr import ServiceMgr
ServiceMgr.MessageSvc.defaultLimit = 9999999  # all messages
ServiceMgr.MessageSvc.OutputLevel = INFO #DEBUG

#---- Import job config for customized command line inputs ----                                                                                                                                                    
from VBFAnalysis.job_configuration import JobConfigurationBase
import VBFAnalysis.sample
#---- Options you could specify on command line -----
jps.AthenaCommonFlags.EvtMax =vars().get("nEvents", -1)                          #set on command-line with: --evtMax=-1 
#jps.AthenaCommonFlags.SkipEvents=0                       #set on command-line with: --skipEvents=0

config = JobConfigurationBase("JobOptions")
arg_group = config.parser.add_argument_group("JobOptions", "Extra arguments specific to VBFAnalysisAlgJobOptions")
arg_group.add_argument("--currentVariation", dest='currentVariation', default="Nominal", help="current systematics, default: Nominal")
# parse the commandline options

args = config.parse_args()


jps.AthenaCommonFlags.TreeName = "MiniNtuple" 

from glob import glob
jps.AthenaCommonFlags.FilesInput = glob(vars().get("input", "/eos/user/r/rzou/v04/user.othrif.v04.364106.Sherpa_221_NNPDF30NNLO_Zmumu_MAXHTPTV140_280_CVetoBVeto.e5271_s3126_r9364_r9315_p3575_MiniNtuple.root/*"))

### Build sample from FilesInput and read its properties ###
inputDir = str(jps.AthenaCommonFlags.FilesInput)
s=VBFAnalysis.sample.sample(inputDir)
currentSample = s.getsampleType()
isMC = s.getisMC()
runNumber = s.getrunNumber()

jps.AthenaCommonFlags.HistOutputs = ["MYSTREAM:"+currentSample+args.currentVariation+str(runNumber)+".root"]  #optional, register output files like this. MYSTREAM is used in the code

athAlgSeq += CfgMgr.VBFAnalysisAlg("VBFAnalysisAlg",
                               currentVariation = args.currentVariation,
                               currentSample = currentSample,
                               isMC = isMC,
                               runNumberInput = runNumber);

include("AthAnalysisBaseComps/SuppressLogging.py") #optional line
