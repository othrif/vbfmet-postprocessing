
// ROOT
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"

// Local
#include "HInvPlot/PlotEvent.h"
#include "HInvPlot/UtilCore.h"

using namespace std;

//-----------------------------------------------------------------------------
Msl::PlotEvent::PlotEvent():      fPassAlg(0), 
				  hMu(0)
{
}

//-----------------------------------------------------------------------------
Msl::PlotEvent::~PlotEvent()
{
}

//-----------------------------------------------------------------------------
void Msl::PlotEvent::DoConf(const Registry &reg)
{
  //
  // Read self-configuration
  //
  IExecAlg::DoConf(reg);

  reg.Get("PlotEvent::NBin",      fNBin      = 50);
  reg.Get("PlotEvent::NBinLim",   fNBinLim   =  0);
  reg.Get("PlotEvent::DetailLvl", fDetailLvl =  0);

  reg.Get("PlotEvent::SelKey" , fSelKey);
  reg.Get("PlotEvent::Region" , fRegion);
  reg.Get("PlotEvent::VarPref", fVarPref);

  fVarVec =  Mva::ReadVars(reg, "PlotEvent::VarVec", GetAlgName());
  reg.Get("PlotEvent::NBinVec", fNBinVec);  
  reg.Get("PlotEvent::LoVec",   fLoVec);  
  reg.Get("PlotEvent::HiVec",   fHiVec);  

  //
  // Read configuration for selecting MC samples
  //
  fSample.FillSample(reg, "PlotEvent::Samples");

  //
  // Convert string keys to Mva::Key enum values
  //
  fVars = Mva::ReadVars(reg, "PlotEvent::Vars", fName);

  //
  // Created histograms
  //
  hMu          = GetTH1("mu",           50,  0.0,   100.0);

  // creating histograms
  for(unsigned a=0; a<fVarVec.size(); ++a){
    fHistVec[fVarVec[a]] =  GetTH1(Mva::Convert2Str(fVarVec[a]),unsigned(fNBinVec[a]), float(fLoVec[a]), float(fHiVec[a]));
  }
  
    if(fDebug) {
      fSample.Print(std::cout, "   ");
    }
}

//-----------------------------------------------------------------------------
bool Msl::PlotEvent::DoExec(Event &event)
{
  //
  // Select sample
  //
  if(fSample.GetSize() > 0 && !fSample.MatchSample(event.sample)) {
    return true;
  }

  double weight = event.GetWeight();
  if(fDebug) std::cout << "PlotEvent: " << weight << " " << GetAlgName() << std::endl;
  if(fPassAlg) {
    if(!(fPassAlg->GetPassStatus())) {
      return true;
    }
    weight = fPassAlg->GetPassWeight();
  }

  //
  // Fill and save new VarStore
  //
  //fEvents.push_back(VarStore(event, fVars));
  //fEvents.back().SetWeight(weight);
  
  //
  // Fill histograms
  //
  //FillHist(hjj_deta,   Mva::jj_deta, event, weight);
  for(unsigned a=0; a<fVarVec.size(); ++a){
    FillHist(fHistVec[fVarVec[a]], fVarVec[a], event, weight);
  }
  
  return true;
}

//-----------------------------------------------------------------------------
void Msl::PlotEvent::DoSave(TDirectory *idir)
{
  //
  // Plot stored variables
  //
  for(unsigned i = 0; i < fVars.size(); ++i) {
    PlotVar(fVars.at(i));
  }

  //
  // Save histograms
  //
  IExecAlg::DoSave(idir);
}

//-----------------------------------------------------------------------------
void Msl::PlotEvent::PlotVar(const Mva::Var var)
{
  //
  // Make and fill histogram for output variables
  //
  if(!HasVar(var)) {
    return;
  }

  const pair<double, double> res = GetMinMax(var); 
  if(!(res.first < res.second)) {
    return;
  }

  //
  // Book histogram
  //
  const double vpad = 0.01*(res.second-res.first);

  TH1 *h = GetTH1(fVarPref+Mva::Convert2Str(var), fNBin, res.first-vpad, res.second+vpad);

  h->GetXaxis()->CenterTitle();
  h->GetXaxis()->SetTitle(Mva::Convert2Str(var).c_str());

  //
  // Fill histogram
  //
  FillHist(h, var);
}

//-----------------------------------------------------------------------------
bool Msl::PlotEvent::HasVar(Mva::Var var) const
{
  return std::find(fVars.begin(), fVars.end(), var) != fVars.end();
}

//-----------------------------------------------------------------------------
std::pair<double, double> Msl::PlotEvent::GetMinMax(Mva::Var var) const
{
  //
  // Compute min/max value for stored variable
  //
  pair<double, double> res(0.0, 0.0);

  if(var == Mva::NONE) {
    return res;
  }

  for(unsigned i = 0; i < fEvents.size(); ++i) {
    const VarStore &event = fEvents.at(i);
    
    double val = 0.0;
    if(event.GetVar(var, val)) {
      res.first  = std::min<double>(res.first,  val);
      res.second = std::max<double>(res.second, val);
    }
  }

  return res;
}

//-----------------------------------------------------------------------------
void Msl::PlotEvent::FillHist(TH1 *h, Mva::Var var) const
{
  //
  // Fill histogram
  //
  if(var == Mva::NONE || !h) {
    return;
  }

  for(unsigned i = 0; i < fEvents.size(); ++i) {
    const VarStore &event = fEvents.at(i);

    double val = 0.0;
    if(event.GetVar(var, val)) {
      h->Fill(val, event.GetWeight());
    }
  }
}

//-----------------------------------------------------------------------------
double Msl::PlotEvent::FillHist(TH1 *h, Mva::Var var, const Event &event, double weight) const
{
  double val = 0.0;

  if(!h) {
    return val;
  }

  if(event.GetVar(var, val)) {
    h->Fill(val, weight);
  }

  return val;
}
