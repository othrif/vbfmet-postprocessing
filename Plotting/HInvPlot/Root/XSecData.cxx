// C/C++
#include <set>
#include <math.h>
#include <cstdlib>
#include <iomanip>

// ROOT
#include "TDirectory.h"
#include "TH1.h"
#include "TFile.h"
#include "TLeaf.h"
#include "TTree.h"
#include "TStopwatch.h"
#include "TLorentzVector.h"

// Local
#include "HInvPlot/XSecData.h"

using namespace std;


//-----------------------------------------------------------------------------
std::string Msl::Ntuple::AsStr(Type t)
{
  if(t == kNoType)       return "NoType,";
  if(t == kCommonData)   return "CommonData";
  if(t == kCommonMC)     return "CommonMC";

  return "notype";
}

//-----------------------------------------------------------------------------
Msl::XSecData::XSecData():
  run     (0),
  xsec    (0),
  kfactor (0),
  feff    (0),
  hmass   (0),
  weight  (1.0),
  escale  (0.0),
  inputw  (0.0),
  inlumi  (0.0),
  eventn  (0),
  evente  (0),
  eventw  (0.0),
  sample  (Mva::kNone)
{
}

//-----------------------------------------------------------------------------
Msl::XSecData::XSecData(const Registry &reg):
  run     (0),
  xsec    (0),
  kfactor (0),
  feff    (0),
  hmass   (0),
  weight  (1.0),
  escale  (0.0),
  inputw  (0.0),
  inlumi  (0.0),
  eventn  (0),
  evente  (0),
  eventw  (0.0),
  sample  (Mva::kNone)
{
  reg.Get("run",       run);
  reg.Get("xsec",      xsec);
  reg.Get("kfactor",   kfactor);
  reg.Get("feff",      feff);
  reg.Get("hmass",     hmass);
  reg.Get("process",   process);
  reg.Get("key",       key);

  sample = Mva::Convert2Sample(key);

  if(sample == Mva::kNone && false) {
    cout << "------------------------------------------------------------" << endl
	 << "XSecData - failed to find sample" << endl;
    Print();
  }
  
  weight = Weight();
}

//-----------------------------------------------------------------------------
void Msl::XSecData::Print() const
{
  cout << "   Process:       " << process << endl
       << "      sample:      " << Mva  ::Convert2Str(sample) << endl
       << "      key:         " << key         << endl
       << "      run:         " << run         << endl
       << "      xsec:        " << xsec        << endl
       << "      kfactor:     " << kfactor     << endl
       << "      feff:        " << feff        << endl
       << "      hmass:       " << hmass       << endl;
}

//-----------------------------------------------------------------------------
double Msl::XSecData::Weight() const
{
  //
  // Compute total sample weight
  //
  double w = 1.0;

  if(xsec    > 0.0) { w *= xsec   ; }
  if(kfactor > 0.0) { w *= kfactor; }
  if(feff    > 0.0) { w *= feff   ; }

  return w;
}

//-----------------------------------------------------------------------------
Msl::FileData::FileData():
  dir    (0),
  ntuple (Ntuple::kNoType),
  version(Ntuple::kNoVersion)
{
}

//-----------------------------------------------------------------------------
Msl::VarData::VarData():
  var (Mva::NONE),
  type(kNone),
  vald(0.0),
  valf(0.0),
  vali(0),
  valu(0),
  valb(false)
{
}


//-----------------------------------------------------------------------------
void Msl::VarData::Clear()
{
  vald = 0.0;
  valf = 0.0;
  vali = 0;
  valu = 0;
  valb = false;
}

//-----------------------------------------------------------------------------
void Msl::VarData::Print() const
{
  cout << "   key=" << key << " var=" << Mva::Convert2Str(var) << endl;
}

//-----------------------------------------------------------------------------
double Msl::VarData::GetVal() const
{
  if     (type == kDouble) return static_cast<double>(vald);
  else if(type == kFloat ) return static_cast<double>(valf);
  else if(type == kInt   ) return static_cast<double>(vali);
  else if(type == kUInt  ) return static_cast<double>(valu);
  else if(type == kBool  ) return static_cast<double>(valb);

  cout << "VarData::GetVal - using undefined type" << endl;
  return 0.0;
}

//-----------------------------------------------------------------------------
bool Msl::VarData::SetVarBranch(TTree *tree)
{
  //
  // Init branch 
  //
  TBranch *b = tree->GetBranch(key.c_str());
  if(!b) {
    return false;
  }
  if(b->GetNleaves() != 1) {
    std::cout << "VarData::SetVarBranch - branch has more than 1 leaf: " << key << endl;
    b->Print();
    return false;   
  }
  
  TLeaf *l = 0;

  if(b->GetListOfLeaves()) {
    l = dynamic_cast<TLeaf *>(b->GetListOfLeaves()->First());
  }

  if(!l) {
    std::cout << "VarData::SetVarBranch - missing leaf: " << key << endl;
    b->Print();
    return false;
  }

  //
  // Determine type and set branch address
  //
  type = GetType(l->GetTypeName());

  if(false) {
    cout << "VarData::SetVarBranch - " << setw(10) << std::left << l->GetTypeName() 
	 << "\"" << key << "\""  << endl;
  }

  if     (type == kDouble) return SetBranch(tree, key, vald);
  else if(type == kFloat ) return SetBranch(tree, key, valf);
  else if(type == kInt   ) return SetBranch(tree, key, vali);
  else if(type == kUInt  ) return SetBranch(tree, key, valu);
  else if(type == kBool  ) return SetBranch(tree, key, valb);

  cout << "VarData::SetVarBranch - using undefined type" << endl;
  return false;
}

//-----------------------------------------------------------------------------
Msl::VarData::Type Msl::VarData::GetType(const std::string &t) const
{
  //
  // Convert known type strings to enum
  //

  if     (t == "Double_t") return kDouble;
  else if(t == "Float_t" ) return kFloat;
  else if(t == "Int_t"   ) return kInt;
  else if(t == "UInt_t"  ) return kUInt;
  else if(t == "Bool_t"  ) return kBool;

  cout << "VarData::GetType - unknown type: " << type << endl;
  return kNone;

}
