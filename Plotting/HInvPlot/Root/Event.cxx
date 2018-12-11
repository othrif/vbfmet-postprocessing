
// C/C++
#include <cmath>
#include <sstream>
#include <iomanip>

// Local
#include "HInvPlot/UtilCore.h"
#include "HInvPlot/Event.h"

using namespace std;

//-----------------------------------------------------------------------------
std::string Msl::Mva::AsStr(Chan c)
{
  if(c == aa) return "aa";
  if(c == ee) return "ee";
  if(c == eu) return "eu";
  if(c == uu) return "uu";
  if(c == ll) return "ll";

  return "aa";
}

//-----------------------------------------------------------------------------
Msl::Mva::Chan Msl::Mva::Convert2Chan(const std::string &c)
{
  if(c == "aa") return aa;
  if(c == "ee") return ee;
  if(c == "eu") return eu;
  if(c == "uu") return uu;
  if(c == "ll") return ll;
  
  cout << "Convert2Chan - ERROR: unknown channel string: " << c << endl;
  exit(1);

  return aa;
}

//-----------------------------------------------------------------------------
std::string Msl::Mva::AsStr(Flavor f)
{
  if(f == e) return "e";
  if(f == u) return "u";

  return "FlavorUnknown";
}

//-----------------------------------------------------------------------------
Msl::Mva::Flavor Msl::Mva::Convert2Flavor(const std::string &f)
{
  if(f == "e") return e;
  if(f == "u") return u;
  
  cout << "Convert2Flavor - ERROR: unknown flavor string: " << f << endl;
  exit(1);

  return FlavorUnknown;
}


//-----------------------------------------------------------------------------
// Event class code
//-----------------------------------------------------------------------------
Msl::Event::Event():
  bits              (0)
{
}

//-----------------------------------------------------------------------------
void Msl::Event::Clear()
{
  //
  // Clear vector of variables
  //
  VarHolder::ClearVars();
  muons.clear();
  electrons.clear();
  taus.clear();  
  jets.clear();
  truth_jets.clear();
  truth_taus.clear();
  truth_el.clear();
  truth_mu.clear();
  baseel.clear();
  basemu.clear();
  photons.clear();
  
  //
  // Clear local vectors
  //
  totalWeight       = 1.0;
  isMC              = false;

}

//-----------------------------------------------------------------------------
void Msl::Event::SetVars()
{
  //
  // Sort leptons: lep0 is a leading lepton
  //
  
}

//-----------------------------------------------------------------------------
void Msl::Event::Print() const
{
  //
  // Printing variables
  //
  //Print();
}

//-----------------------------------------------------------------------------
void Msl::Event::Convert2GeV(const std::vector<Mva::Var> &vars)
{
  for(unsigned i = 0; i < vars.size(); ++i) {
    const Mva::Var var = vars.at(i);
    double         val = 0.0;

    if(GetVar(var, val)) {
      DelVar(var);
      AddVar(var, val/1000.0);
    }
  }
}

//--------------------------------------------------------------------------------------                                       
void Msl::Event::GetX1X2(const TLorentzVector &lep1,
			 const TLorentzVector &lep2,
			 const std::pair<float,float> &tmet,
			 double& output_x1,
			 double& output_x2)
{
  // 
  // Find the x1 and x2 vars used in the collinear approximation   
  //
  float x1=0.0, x2=0.0;
  float den1 = lep1.Px()*lep2.Py()+tmet.first*lep2.Py()-lep1.Py()*lep2.Px()-tmet.second*lep2.Px();
  float den2 = lep1.Px()*lep2.Py()-tmet.first*lep1.Py()-lep1.Py()*lep2.Px()+tmet.second*lep1.Px();

  if(den1!=0.0) x1 = (lep1.Px()*lep2.Py()-lep1.Py()*lep2.Px())/den1;
  if(den2!=0.0) x2 = (lep1.Px()*lep2.Py()-lep1.Py()*lep2.Px())/den2;

  output_x1 = x1;
  output_x2 = x2;

  return;
}
