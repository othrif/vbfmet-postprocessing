
// C/C++
#include <iomanip>

// Local
#include "HInvPlot/VarHolder.h"

using namespace std;

//--------------------------------------------------------------------------------------      
bool Msl::VarComp::operator()(const VarHolder &lhs, const VarHolder &rhs) const
{
  double lvar = 0.0;
  double rvar = 0.0;

  if(lhs.GetVar(fVar, lvar) && rhs.GetVar(fVar, rvar)) {
    if(fRev) {
      return lvar > rvar;
    }
    
    return lvar < rvar;
  }

  cout << "VarComp::operator() - undefine result for missing var: " << Mva::AsStr(fVar) << endl;
  lhs.Print();
  rhs.Print();
  
  return (&lhs) < (&rhs);
}

//--------------------------------------------------------------------------------------      
std::vector<double> Msl::VarHolder::GetVars(const std::vector<Mva::Var> &vars) const
{
  //
  // Fill vector with requested variables
  //
  vector<double> vals;

  for(unsigned i = 0; i < vars.size(); ++i) {
    Mva::Var var = vars.at(i);
    double val   = 0.0;
    
    if(GetVar(var, val)) {
      vals.push_back(val);
    }
  }

  return vals;
}

//--------------------------------------------------------------------------------------      
void Msl::VarHolder::Print(std::ostream &os) const
{
  os << "VarEntry::Print - " << fVars.size() << " variable(s)" << endl;
  
  for(unsigned i = 0; i < fVars.size(); ++i) {
    os << "   key=" << setw(10) << right << fVars.at(i).GetKey() 
       << ": data=" << fVars.at(i).GetData() << endl;
  }
}
