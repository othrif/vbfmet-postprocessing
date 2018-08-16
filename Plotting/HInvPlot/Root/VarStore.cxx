
// C/C++
#include <iomanip>

// Local
#include "HInvPlot/VarStore.h"

using namespace std;

//--------------------------------------------------------------------------------------      
Msl::VarStore::VarStore():
  RunNumber  (0),
  EventNumber(0),
  fWeight    (0.0),
  fBits      (0),
  fSample    (Mva::kNone)
{
}

//--------------------------------------------------------------------------------------      
Msl::VarStore::VarStore(const Event &event, const std::vector<Mva::Var> &vars):
  RunNumber  (event.RunNumber),
  EventNumber(event.EventNumber),
  fWeight    (0.0),
  fBits      (0),
  fSample    (Mva::kNone)
{
  FillStore(event, vars);
}

//--------------------------------------------------------------------------------------      
void Msl::VarStore::Clear()
{
  VarHolder::ClearVars();

  RunNumber   = 0;
  EventNumber = 0;
  fWeight     = 0.0;
  fBits       = 0;
  fSample     = Mva::kNone;
}

//--------------------------------------------------------------------------------------      
void Msl::VarStore::FillStore(const Event &event, const std::vector<Mva::Var> &vars)
{
  //
  // Fill self from event
  //
  RunNumber   = event.RunNumber;
  EventNumber = event.EventNumber;
  fWeight     = event.GetWeight();
  fSample     = event.sample;

  for(unsigned i = 0; i < vars.size(); ++i) {
    Mva::Var var = vars.at(i);
    double   val = 0.0;

    if(!event.GetVar(var, val)) {
      continue;
    }
    else {
      AddVar(var, val);
    }
  }
}
