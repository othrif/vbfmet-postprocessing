jps.AthenaCommonFlags.TreeName = "MiniNtuple" 
jps.AthenaCommonFlags.FilesInput = ["/eos/atlas/user/b/bcarlson/TestRel21Setup/user.rzou.v02SRe.364174.Sherpa_221_NNPDF30NNLO_Wenu_MAXHTPTV70_140_CFilterBVeto.p3575_MiniNtuple.root/user.rzou.14633081._000001.MiniNtuple.root"]

jps.AthenaCommonFlags.HistOutputs = ["MYSTREAM:myfile.root"]  #optional, register output files like this. MYSTREAM is used in the code

athAlgSeq += CfgMgr.VBFAnalysisAlg()                               #adds an instance of your alg to the main alg sequence

include("AthAnalysisBaseComps/SuppressLogging.py") #optional line
