theApp.EvtMax = -1

import AthenaPoolCnvSvc.ReadAthenaPool
svcMgr.EventSelector.InputCollections = [ 'Samples/MoreSamples/mc15_13TeV.312484.Sh_227_NN30NNLO_Znunu_PTV100_140_MJJ0_500_KtMerging.evgen.EVNT.e7728/EVNT.18992357._000007.pool.root.1']

from AthenaCommon.AlgSequence import AlgSequence
job = AlgSequence()

from Rivet_i.Rivet_iConf import Rivet_i
rivet = Rivet_i()
import os
rivet.AnalysisPath = os.environ['PWD']

rivet.Analyses += [ 'Re_Vjj_vbf_nn_asym' ]
rivet.RunName = ''
rivet.HistoFile = 'File312484v2.yoda.gz'
rivet.CrossSection = 105.869824
#rivet.IgnoreBeamCheck = True
#rivet.SkipWeights=True
job += rivet
