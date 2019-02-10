#---- Import job config for customized command line inputs ----
from VBFAnalysis.job_configuration import JobConfigurationBase
from glob import glob
import VBFAnalysis.sample
#---- Options you could specify on command line -----
jps.AthenaCommonFlags.EvtMax =vars().get("nEvents", -1)                          #set on command-line with: --evtMax=-1
#jps.AthenaCommonFlags.SkipEvents=0                       #set on command-line with: --skipEvents=0
jps.AthenaCommonFlags.FilesInput =[vars().get("input", "/eos/user/r/rzou/v04/merged/Z_EWKNominal308092_000001.root")]
jps.AthenaCommonFlags.TreeName = "MiniNtuple"

config = JobConfigurationBase("JobOptions")
arg_group = config.parser.add_argument_group("JobOptions", "Extra arguments specific to HFInputJobOptions")
arg_group.add_argument("--currentVariation", dest='currentVariation', default="Nominal", help="current systematics, default: NONE")
arg_group.add_argument("--containerName", dest='containerName', default="", help="container name used to look up the sample ID if not in the file path")
arg_group.add_argument("--currentSample", dest='currentSample', default="", help="sample name to process")
arg_group.add_argument("--doLowNom", action="store_true", dest='doLowNom', default=False, help="doLowNom, to symmetrize asymmetric syst, default: False")
arg_group.add_argument("--extraVars", dest='extraVars', default='0', help="extraVars, cut on the new variables for leptons veto etc, default: 0, 1=lepton vars, 2= includes kinematics")
arg_group.add_argument("--isMadgraph", action="store_true", dest='isMadgraph', default=False, help="isMadgraph, default: False")
arg_group.add_argument("--isLow", action="store_true", dest='isLow', default=False, help="isLow, default: False")
arg_group.add_argument("--weightSyst", action="store_true", dest='weightSyst', default=False, help="is a weight systematic, default: False")
arg_group.add_argument("--oldInput", action="store_true", dest='oldInput', default=False, help="if oldInput, switch to HFInputOldInput")
# parse the commandline options
args = config.parse_args()

doLowNom_str = ""
if (args.doLowNom):
    doLowNom_str = "Low"
inputDir = str(jps.AthenaCommonFlags.FilesInput)
s = VBFAnalysis.sample.sample("", args.currentVariation)
currentSampleKey=''
currentSampleList=[]
currentSample=''
if args.currentSample!="":
    currentSampleList+=[args.currentSample]
subfileN=''
if len(currentSampleList)==0:
    #for sampl,slist in s.sampleMap.iteritems():
    for sampl in s.sampleTypeList:
        if inputDir.count(sampl):
            currentSampleKey=sampl
            currentSampleList=[sampl]
            currentSample=sampl
            break;
#s = VBFAnalysis.sample.sample(inputDir, args.currentVariation)
#currentSample = s.getsampleType()
#print inputDir
#runNumberS = s.getrunNumberS().rstrip('.root')
#subfileN = s.getsubfileN()
runNumberS=''
containerName = args.containerName
if containerName!="":
    s=VBFAnalysis.sample.sample(containerName)
    currentSample = s.getsampleType()
    isMC = s.getisMC()
    runNumber = s.getrunNumber()
    subfileN = s.getsubfileN()

#for currentSample in currentSampleList:
if True:
    print 'currentSample: ',currentSample
    jps.AthenaCommonFlags.AccessMode = "TreeAccess"              #Choose from TreeAccess,BranchAccess,ClassAccess,AthenaAccess,POOLAccess
    jps.AthenaCommonFlags.TreeName = currentSample+args.currentVariation   #form:"Z_strongNominal"                    #when using TreeAccess, must specify the input tree name 
    if args.weightSyst:
        jps.AthenaCommonFlags.TreeName = currentSample+"Nominal"   #form:"Z_strongNominal"                    #when using TreeAccess, must specify the input tree name 
    print currentSample+args.currentVariation
    jps.AthenaCommonFlags.HistOutputs = ["MYSTREAM:HF"+currentSample+args.currentVariation+doLowNom_str+runNumberS+"_"+str(subfileN)+".root"]  #register output files like this. MYSTREAM is used in the code
    
    if currentSample == "data":
        isMC = False
    else:
        isMC = True
    
    if not(args.oldInput):
        athAlgSeq += CfgMgr.HFInputAlg("HFInputAlg",
                                       currentVariation = args.currentVariation,
                                       currentSample = currentSample,
                                       isMC = isMC,
                                       ExtraVars=int(args.extraVars),
                                       doLowNom = args.doLowNom,
                                       isHigh = not args.isLow,
                                       isMadgraph = args.isMadgraph,
                                       weightSyst = args.weightSyst);
    else:
        if args.currentSample == "physics_micro":
            isMC = False
        athAlgSeq += CfgMgr.HFInputOldInputAlg("HFInputOldInputAlg",
                                               currentVariation = args.currentVariation,
                                               currentSample = currentSample,
                                               isMC = isMC,
                                               ExtraVars=int(args.extraVars),
                                               doLowNom = args.doLowNom,
                                               isHigh = not args.isLow,
                                               isMadgraph = args.isMadgraph,
                                               weightSyst=weightSyst);
    
    
    include("AthAnalysisBaseComps/SuppressLogging.py")              #Optional include to suppress as much athena output as possible. Keep at bottom of joboptions so that it doesn't suppress the logging of the things you have configured above

