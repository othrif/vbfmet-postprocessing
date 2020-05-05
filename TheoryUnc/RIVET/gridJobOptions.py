theApp.EvtMax = -1

import AthenaPoolCnvSvc.ReadAthenaPool

from AthenaCommon.AlgSequence import AlgSequence
job = AlgSequence()

from Rivet_i.Rivet_iConf import Rivet_i
rivet = Rivet_i()
import os
rivet.AnalysisPath = os.environ['PWD']

rivet.Analyses += [ 'Re_Vjj_vbf_nn_asym' ]
rivet.RunName = ''
rivet.HistoFile = '364222.yoda.gz'
rivet.CrossSection = 0.29612032
#rivet.IgnoreBeamCheck = True
#rivet.SkipWeights = True
job += rivet
