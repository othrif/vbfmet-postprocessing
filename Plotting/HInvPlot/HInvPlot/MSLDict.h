#ifndef MSL_MVA_DICT_H
#define MSL_MVA_DICT_H

// Data
#include "HInvPlot/Event.h"
#include "HInvPlot/RecParticle.h"
#include "HInvPlot/Registry.h"
#include "HInvPlot/VarHolder.h"
#include "HInvPlot/VarEvent.h"
#include "HInvPlot/VarEntry.h"
#include "HInvPlot/VarStore.h"
#include "HInvPlot/TRExTools.h"
#include "HInvPlot/SmoothHist.h"

// Specialized algorithms
#include "HInvPlot/ReadEvent.h"

// Algorithms inheriting from IExecAlg
#include "HInvPlot/IExecAlg.h"
#include "HInvPlot/PassEvent.h"
#include "HInvPlot/PlotEvent.h"

#ifndef __CINT__

struct MSLDict
{
  std::vector<Msl::Event>       f01;
  std::vector<Msl::VarEntry>    f02;
  std::vector<Msl::VarHolder>   f03;
  std::vector<Msl::RecParticle> f04;
  
  std::vector<Msl::IExecAlg *>  f06;
  std::vector<Msl::VarStore>    f07;
};

namespace Msl
{
  template void Registry::Set<int>        (const std::string &, const int &);
  template void Registry::Set<double>     (const std::string &, const double &);
  template void Registry::Set<std::string>(const std::string &, const std::string &);
  template void Registry::Set<Registry>   (const std::string &, const Registry &);
}

#endif
#endif
