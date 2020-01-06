
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
				  hminDRLep(0),
				  hjj_mass_variableBin(0),
				  htruth_jj_mass_variableBin(0),
				  htmva_variableBin(0),
				  hmj34(0),
				  hmax_j_eta(0),
				  hdRj1(0),
				  hdRj2(0),
				  hminDR(0),
				  hJetEtaPt25(0),
				  hJetEtaPt35(0),
				  hJetEtaPt55(0),
				  hJetEMECvsBCIDPosPt25(0),
				  hJetEMECvsBCIDPosPt35(0),
				  hJetEMECvsBCIDPosPt55(0),
				  hMetvsMu(0),
				  hmj1(0),
				  hmj2(0),
				  hminDRmj2(0),
				  hmin_mj3(0),
				  hmin_mj3_over_mjj(0),
				  hcentrality(0),
				  hjj_deta_signed(0),
				  hjj_deta_diff(0),
				  hjj_deta_abs(0),
				  hZMCIDQCD(0), hWMCIDQCD(0),hZPTVMCIDQCD(0),
				  hZMadMCIDQCD(0), hZMad2MCIDQCD(0),hZMadFMCIDQCD(0),
				  hWMadMCIDQCD(0),
				  hZPowMCIDQCD(0),hZShMCIDQCD(0)
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
  hTruthMuPt    = GetTH1("truthMuPt",    50,  0.0,   100.0);
  hTruthMuEta   = GetTH1("truthMuEta",   45,  -4.5,   4.5);
  hBaseMuPt     = GetTH1("baseMuPt",    50,  0.0,   100.0);
  hBaseMuEta    = GetTH1("baseMuEta",   45,  -4.5,   4.5);
  hTruthElPt    = GetTH1("truthElPt",    50,  0.0,   100.0);
  hTruthElEta   = GetTH1("truthElEta",   45,  -4.5,   4.5);
  hBaseElPt     = GetTH1("baseElPt",    120,  0.0,   600.0);
  hBaseElEta    = GetTH1("baseElEta",   45,  -4.5,   4.5);
  hTruthTauPt   = GetTH1("truthTauPt",    50,  0.0,   100.0);
  hTruthTauDR   = GetTH1("truthTauDR",    100,  0.0,   10.0);
  hTruthTauEta  = GetTH1("truthTauEta",   45,  -4.5,   4.5);
  hminDRLep     = GetTH1("minDRLep",   60,  0.0,   6.0);
  hptvarcone20  = GetTH1("ptvarcone20",   12,  -0.2,   1.0);
  hptvarcone30  = GetTH1("ptvarcone30",   12,  -0.2,   1.0);
  htopoetcone20 = GetTH1("topoetcone20",  12,  -0.2,   1.0);

  // extra vars
  hmj34             = GetTH1("mj34",             50,  0.0,   1000.0);
  hmax_j_eta        = GetTH1("max_j_eta",        45,  0.0,   4.5);
  hdRj1             = GetTH1("dRj1",             20,  0.0,   10.0);
  hdRj2             = GetTH1("dRj2",             20,  0.0,   10.0);
  hminDR            = GetTH1("minDR",            20,  0.0,  10.0);
  hJetEtaPt25       = GetTH1("JetEtaPt25",       90,  -4.5,  4.5);
  hJetEtaPt35       = GetTH1("JetEtaPt35",       90,  -4.5,  4.5);
  hJetEtaPt55       = GetTH1("JetEtaPt55",       90,  -4.5,  4.5);
  hJetEMECvsBCIDPosPt25 = GetTH2("JetEMECvsBCIDPosPt25",  5,  -0.5,  4.5, 35, 0.0, 70);
  hJetEMECvsBCIDPosPt35 = GetTH2("JetEMECvsBCIDPosPt35",  5,  -0.5,  4.5, 35, 0.0, 70);
  hJetEMECvsBCIDPosPt55 = GetTH2("JetEMECvsBCIDPosPt55",  5,  -0.5,  4.5, 35, 0.0, 70);
  hMetvsMu = GetTH2("MetvsMu",  50, 0.0, 500.0, 10,  0.0,  100);
  hmj1              = GetTH1("mj1",              50,  0.0,   2000.0);
  hmj2              = GetTH1("mj2",              50,  0.0,   2000.0);
  hminDRmj2         = GetTH1("minDRmj2",         50,  0.0,   2000.0);
  hmin_mj3          = GetTH1("min_mj3",          50,  0.0,   2000.0);
  hmin_mj3_over_mjj = GetTH1("min_mj3_over_mjj", 25,  0.0,   1.0);
  hcentrality       = GetTH1("centrality",       25,  0.0,   1.0);
  hj3Pt             = GetTH1("j3Pt",             20,  0.0,   200.0);
  hj3Eta            = GetTH1("j3Eta",            22,  -4.5,  4.5);
  hj3Jvt            = GetTH1("j3Jvt",            12,  -0.2,  1.0);
  hj3FJvt           = GetTH1("j3FJvt",           22,  -0.2,  2.0);

  hJetHT            = GetTH1("jetHT",            50,  0.0,   1000.0);
  hAllJetMETSig     = GetTH1("alljet_metsig",    200,  0.0,   20.0);

  hjj_deta_signed   = GetTH1("jj_deta_signed",   50, -10.0, 10.0);
  hjj_deta_diff     = GetTH1("jj_deta_diff",   50, -10.0, 10.0);
  hjj_deta_abs      = GetTH1("jj_deta_abs",   50, -3.0, 3.0);

  hmuDR           = GetTH1("muDR",           25,  0.0,  5.0);
  hmuEta          = GetTH1("muEta",          30,  0.0,  3.0);

  hZMCIDQCD    = GetTH1("ZMCIDQCD",     100,  364099.5,364199.5);
  hZPTVMCIDQCD    = GetTH1("ZPTVMCIDQCD",     26,  366009.5,366035.5);  
  hWMCIDQCD    = GetTH1("WMCIDQCD",     100,  364155.5,364255.5);
  hZMadMCIDQCD = GetTH1("ZMadMCIDQCD",  10,  361509.5,361519.5);
  hZMad2MCIDQCD= GetTH1("ZMad2MCIDQCD", 100, 363122.5,363222.5);
  hZMadFMCIDQCD= GetTH1("ZMadFMCIDQCD", 25, 311428.5,311453.5);
  hWMadMCIDQCD = GetTH1("WMadMCIDQCD",  74,  363599.5,363673.5);
  hZPowMCIDQCD = GetTH1("ZPowMCIDQCD",  19,  301019.5,301038.5);
  hZShMCIDQCD  = GetTH1("ZShMCIDQCD",   84,  312447.5,312531.5);

  // jj_mass limits
  float binsjjmass [9] = { 0.0, 200.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0, 3500.0, 5000.0 };
  hjj_mass_variableBin = GetTH1("jj_mass_variableBin",  8,  binsjjmass);
  htruth_jj_mass_variableBin = GetTH1("truth_jj_mass_variableBin",  8,  binsjjmass);

  // TMVA variable binned
  float binstmva[8] = {0.0, 0.75300000, 0.81700000, 0.86100000, 0.89500000, 0.92200000, 0.94600000, 1.0};
  htmva_variableBin =  GetTH1("tmva_variableBin",  7,  binstmva);

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
  //std::cout << "Run:" << " " << event.RunNumber << " event: " << event.EventNumber << std::endl;
  //FillHist(hZMCIDQCD,   Mva::jj_deta, event, weight);
  hZPTVMCIDQCD->Fill(event.RunNumber, weight);
  hZMCIDQCD->Fill(event.RunNumber, weight);  
  hWMCIDQCD->Fill(event.RunNumber, weight);
  hZMadMCIDQCD->Fill(event.RunNumber, weight);
  hZMad2MCIDQCD->Fill(event.RunNumber, weight);
  hZMadFMCIDQCD->Fill(event.RunNumber, weight);
  hWMadMCIDQCD->Fill(event.RunNumber, weight);
  hZPowMCIDQCD->Fill(event.RunNumber, weight);
  hZShMCIDQCD->Fill(event.RunNumber, weight);  
  float jj_deta = event.GetVar(Mva::jj_deta);
  if(hjj_deta_signed) hjj_deta_signed->Fill(( fabs(event.GetVar(Mva::jetEta0)) > fabs(event.GetVar(Mva::jetEta1)) ? -1.0*jj_deta : jj_deta), weight);
  if(hjj_deta_diff) hjj_deta_diff->Fill(( fabs(event.GetVar(Mva::jetEta0)) - fabs(event.GetVar(Mva::jetEta1))), weight);
  if(hjj_deta_abs) hjj_deta_abs->Fill(( fabs(event.GetVar(Mva::jetEta0)) - fabs(event.GetVar(Mva::jetEta1)))/jj_deta, weight);
  FillHist(hjj_mass_variableBin,   Mva::jj_mass, event, weight);
  FillHist(htruth_jj_mass_variableBin,   Mva::truth_jj_mass, event, weight);  
  FillHist(htmva_variableBin,      Mva::tmva,    event, weight);
  if(hMetvsMu && event.HasVar(Mva::averageIntPerXing)) hMetvsMu->Fill(event.GetVar(Mva::met_tst_nolep_et), event.GetVar(Mva::averageIntPerXing), weight);
  if(event.truth_mu.size()>0){
    hTruthMuPt ->Fill(event.truth_mu.at(0).pt, weight);
    hTruthMuEta->Fill(event.truth_mu.at(0).eta, weight);
  }
  if(event.truth_el.size()>0){
    hTruthElPt ->Fill(event.truth_el.at(0).pt, weight);
    hTruthElEta->Fill(event.truth_el.at(0).eta, weight);
  }

  if(event.muons.size()>1){
    hmuDR->Fill(event.muons.at(0).GetVec().DeltaR(event.muons.at(1).GetVec()), weight);
    hmuEta->Fill(event.muons.at(0).eta, weight);
    hmuEta->Fill(event.muons.at(1).eta, weight);
  }
  if(event.electrons.size()>1){
    hmuDR->Fill(event.electrons.at(0).GetVec().DeltaR(event.electrons.at(1).GetVec()), weight);
    hmuEta->Fill(event.electrons.at(0).eta, weight);
    hmuEta->Fill(event.electrons.at(1).eta, weight);
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
  //if(event.GetVar(Mva::n_el)==2)
  //std::cout << "eventNum: " << event.EventNumber << " weight: " << weight << std::endl;
  // testing
  float max_j_eta=fabs(event.jets.at(0).eta);
  if(event.jets.size()>1)
    if(fabs(event.jets.at(1).eta)>max_j_eta) max_j_eta= fabs(event.jets.at(1).eta);
  if(hmax_j_eta)  hmax_j_eta->Fill(max_j_eta, weight);
  unsigned njet25EMEC=0, njet35EMEC=0, njet55EMEC=0;
  TLorentzVector tmp;
  for(unsigned iJet=1; iJet<std::min<unsigned>(2,event.jets.size()); ++iJet){ // start with sub-leading jet
    tmp=event.jets.at(iJet).GetLVec();
    if(tmp.Pt()<35.0){ hJetEtaPt25->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet25EMEC; }
    else if(tmp.Pt()<55.0){ hJetEtaPt35->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet35EMEC; }
    else{  hJetEtaPt55->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet55EMEC; }
  }
  if(event.jets.size()>2){
    const TLorentzVector j1v = event.jets.at(0).GetLVec();
    const TLorentzVector j2v = event.jets.at(1).GetLVec();

    for(unsigned iJet=2; iJet<event.jets.size(); ++iJet){
      tmp=event.jets.at(iJet).GetLVec();
      hcentrality->Fill(event.GetVar(Mva::maxCentrality), weight);

      float dRj1=tmp.DeltaR(j1v);
      float dRj2=tmp.DeltaR(j2v);
      hdRj1->Fill(dRj1, weight);
      hdRj2->Fill(dRj2, weight);
      hminDR->Fill(std::min(dRj1,dRj2), weight);
      if(tmp.Pt()<35.0){ hJetEtaPt25->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet25EMEC; }
      else if(tmp.Pt()<55.0){ hJetEtaPt35->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet35EMEC; }
      else{  hJetEtaPt55->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet55EMEC; }

      float mj1 =  (tmp+j1v).M();
      float mj2 =  (tmp+j2v).M();
      hmj1->Fill(mj1, weight);
      hmj2->Fill(mj2, weight);
      hminDRmj2->Fill((dRj1<dRj2 ? mj1 : mj2), weight);
      hmin_mj3->Fill(std::min(mj1,mj2), weight);
      hmin_mj3_over_mjj->Fill(event.GetVar(Mva::maxmj3_over_mjj), weight);
    }
    if(event.jets.size()>3){
      float mj34 = (event.jets.at(2).GetLVec()+event.jets.at(3).GetLVec()).M();
      if(hmj34) hmj34->Fill(mj34, weight);
    }
    if(hj3Pt) hj3Pt->Fill(event.jets.at(2).pt, weight);
    if(hj3Eta) hj3Eta->Fill(event.jets.at(2).eta, weight);
    if(hj3Jvt) hj3Jvt->Fill(event.jets.at(2).GetVar(Mva::jvt), weight);
    if(hj3FJvt) hj3FJvt->Fill(event.jets.at(2).GetVar(Mva::fjvt), weight);
  }
  if(event.HasVar(Mva::BCIDDistanceFromFront)){
    hJetEMECvsBCIDPosPt25->Fill(njet25EMEC,event.GetVar(Mva::BCIDDistanceFromFront));
    hJetEMECvsBCIDPosPt35->Fill(njet35EMEC,event.GetVar(Mva::BCIDDistanceFromFront));
    hJetEMECvsBCIDPosPt55->Fill(njet55EMEC,event.GetVar(Mva::BCIDDistanceFromFront));
  }
  // end testing

  // Hmm.. why is this necessary?
  // It seems that if we don't explicitly ->Fill() here with weights,
  // the python gets the weights wrong, since nothing is capable of setting it.
  if (event.HasVar(Mva::jetHT)) hJetHT->Fill(event.GetVar(Mva::jetHT), weight);
  if (event.HasVar(Mva::alljet_metsig)) hAllJetMETSig->Fill(event.GetVar(Mva::alljet_metsig), weight);

  // jet DR
  float minDR=999.0;
  for(unsigned il=0; il<event.muons.size(); ++il){
    if(hptvarcone20 && event.muons.at(il).HasVar(Mva::ptvarcone20)) hptvarcone20->Fill(event.muons.at(il).GetVar(Mva::ptvarcone20), weight);
    if(hptvarcone30 && event.muons.at(il).HasVar(Mva::ptvarcone30)) hptvarcone30->Fill(event.muons.at(il).GetVar(Mva::ptvarcone30), weight);
    if(htopoetcone20 && event.muons.at(il).HasVar(Mva::topoetcone20)) htopoetcone20->Fill(event.muons.at(il).GetVar(Mva::topoetcone20), weight);
    for(unsigned ij=0; ij<event.jets.size(); ++ij){
      float qDR = event.jets.at(ij).GetVec().DeltaR(event.muons.at(il).GetVec());
      if(minDR>qDR) minDR = qDR;
    }
  }
  for(unsigned il=0; il<event.electrons.size(); ++il){
    if(hptvarcone20 && event.electrons.at(il).HasVar(Mva::ptvarcone20)) hptvarcone20->Fill(event.electrons.at(il).GetVar(Mva::ptvarcone20), weight);
    if(hptvarcone30 && event.electrons.at(il).HasVar(Mva::ptvarcone30)) hptvarcone30->Fill(event.electrons.at(il).GetVar(Mva::ptvarcone30), weight);
    if(htopoetcone20 && event.electrons.at(il).HasVar(Mva::topoetcone20)) htopoetcone20->Fill(event.electrons.at(il).GetVar(Mva::topoetcone20), weight);
    for(unsigned ij=0; ij<event.jets.size(); ++ij){
      float qDR = event.jets.at(ij).GetVec().DeltaR(event.electrons.at(il).GetVec());
      if(minDR>qDR) minDR = qDR;
    }
  }
  hminDRLep->Fill(minDR, weight);

  // fill stored variables
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
