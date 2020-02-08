#ifndef MSL_LINKDEF_H
#define MSL_LINKDEF_H


// Include dictionary headers
#include "HInvPlot/MSLDict.h"
#include <vector>

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclass;

#pragma link C++ namespace Msl::Mva;

#pragma link C++ function Msl::Mva::GetAllVarNames;
#pragma link C++ function Msl::Mva::GetAllVarEnums;

#pragma link C++ class Msl::Event+;
#pragma link C++ class Msl::RecParticle+;

#pragma link C++ class Msl::Registry-;
#pragma link C++ class Msl::VarEntry+;
#pragma link C++ class Msl::VarStore+;
#pragma link C++ class Msl::VarHolder+;
#pragma link C++ class Msl::ReadEvent-;
#pragma link C++ class Msl::IExecAlg-;

#pragma link C++ class TRExTools-;
#pragma link C++ class SmoothHist-;

#pragma link C++ class Msl::PassEvent+;
#pragma link C++ class Msl::PlotEvent+;

#pragma link C++ class std::vector<std::vector<float> >+;
#pragma link C++ class std::vector<std::vector<int> >+;
#pragma link C++ class std::vector<Msl::IExecAlg *>;
#pragma link C++ class std::vector<Msl::Event>+;
#pragma link C++ class std::vector<Msl::VarEntry>+;
#pragma link C++ class std::vector<Msl::VarStore>+;
#pragma link C++ class std::vector<Msl::VarHolder>+;

#endif
#endif


