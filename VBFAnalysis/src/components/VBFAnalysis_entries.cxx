
#include "GaudiKernel/DeclareFactoryEntries.h"

#include "../VBFAnalysisAlg.h"
#include "../HFInputAlg.h"
#include "../VBFTruthAlg.h"
#include "../SignalSystHelper.h"

DECLARE_ALGORITHM_FACTORY( VBFAnalysisAlg )
DECLARE_ALGORITHM_FACTORY( HFInputAlg )
DECLARE_ALGORITHM_FACTORY( VBFTruthAlg )
//DECLARE_ALGORITHM_FACTORY( SignalSystHelper )

DECLARE_FACTORY_ENTRIES( VBFAnalysis ) 
{
  DECLARE_ALGORITHM( VBFAnalysisAlg );
  DECLARE_ALGORITHM( HFInputAlg );
  DECLARE_ALGORITHM( VBFTruthAlg );
  //DECLARE_ALGORITHM( SignalSystHelper );
}
