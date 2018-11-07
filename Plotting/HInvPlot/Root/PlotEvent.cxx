
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
				  hTruthMuPt(0), hTruthMuEta(0),
				  hBaseMuPt(0), hBaseMuEta(0),
				  hTruthElPt(0), hTruthElEta(0),
				  hBaseElPt(0), hBaseElEta(0),
				  hTruthTauPt(0), hTruthTauEta(0),
				  hZMCIDQCD(0), hWMCIDQCD(0),
				  hZMadMCIDQCD(0), hZMad2MCIDQCD(0),
				  hWMadMCIDQCD(0),
				  hZPowMCIDQCD(0)
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
  hTruthMuPt   = GetTH1("truthMuPt",    50,  0.0,   100.0);
  hTruthMuEta  = GetTH1("truthMuEta",   45,  -4.5,   4.5);  
  hBaseMuPt    = GetTH1("baseMuPt",    50,  0.0,   100.0);
  hBaseMuEta   = GetTH1("baseMuEta",   45,  -4.5,   4.5);
  hTruthElPt   = GetTH1("truthElPt",    50,  0.0,   100.0);
  hTruthElEta  = GetTH1("truthElEta",   45,  -4.5,   4.5);  
  hBaseElPt    = GetTH1("baseElPt",    50,  0.0,   100.0);
  hBaseElEta   = GetTH1("baseElEta",   45,  -4.5,   4.5);
  hTruthTauPt  = GetTH1("truthTauPt",    50,  0.0,   100.0);
  hTruthTauDR  = GetTH1("truthTauDR",    100,  0.0,   10.0);
  hTruthTauEta = GetTH1("truthTauEta",   45,  -4.5,   4.5);    
  hZMCIDQCD    = GetTH1("ZMCIDQCD",     100,  364099.5,364199.5);
  hWMCIDQCD    = GetTH1("WMCIDQCD",     100,  364155.5,364255.5);
  hZMadMCIDQCD = GetTH1("ZMadMCIDQCD",  10,  361509.5,361519.5);
  hZMad2MCIDQCD= GetTH1("ZMad2MCIDQCD", 10,  363122.5,363222.5);  
  hWMadMCIDQCD = GetTH1("WMadMCIDQCD",  74,  363599.5,363673.5);
  hZPowMCIDQCD = GetTH1("ZPowMCIDQCD",  19,  301019.5,301038.5);  

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
  //FillHist(hZMCIDQCD,   Mva::jj_deta, event, weight);
  hZMCIDQCD->Fill(event.RunNumber, weight);
  hWMCIDQCD->Fill(event.RunNumber, weight);
  hZMadMCIDQCD->Fill(event.RunNumber, weight);
  hZMad2MCIDQCD->Fill(event.RunNumber, weight);  
  hWMadMCIDQCD->Fill(event.RunNumber, weight);  
  hZPowMCIDQCD->Fill(event.RunNumber, weight);
  
  if(event.truth_mu.size()>0){
    hTruthMuPt ->Fill(event.truth_mu.at(0).pt, weight);
    hTruthMuEta->Fill(event.truth_mu.at(0).eta, weight);
  }
  if(event.truth_el.size()>0){
    hTruthElPt ->Fill(event.truth_el.at(0).pt, weight);
    hTruthElEta->Fill(event.truth_el.at(0).eta, weight);
  }

  if(event.basemu.size()>0){
    hBaseMuPt ->Fill(event.basemu.at(0).pt, weight);
    hBaseMuEta->Fill(event.basemu.at(0).eta, weight);
  }
  if(event.baseel.size()>0){
    hBaseElPt ->Fill(event.baseel.at(0).pt, weight);
    hBaseElEta->Fill(event.baseel.at(0).eta, weight);
  }
  if(event.truth_taus.size()>0){
    hTruthTauPt ->Fill(event.truth_taus.at(0).pt, weight);
    for(unsigned iJet=0; iJet<event.jets.size(); ++iJet)
      hTruthTauDR ->Fill(event.truth_taus.at(0).GetVec().DeltaR(event.jets.at(iJet).GetVec()), weight);
    hTruthTauEta->Fill(event.truth_taus.at(0).eta, weight);
  }  
  
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
