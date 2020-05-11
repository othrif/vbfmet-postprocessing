
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
				  hTruthTauPt(0), hTruthTauDR(0), hTruthTauEta(0),
				  hminDRLep(0),
				  hjj_mass_variableBin(0),
				  hjj_mass_variableBinGam(0),
				  htruth_jj_mass_variableBin(0),
				  hjj_mass_dphi_variableBin(0),
				  hmetsig_variableBin(0),
				  htmva_variableBin(0),
				  htmva_variableBin11(0),
				  htmva_wmj_variableBin(0),
				  htmva_wmj_variableBin11(0),
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
				  hmuDR(0),
				  hmuEta(0),
				  hptvarcone20(0),
				  hptvarcone30(0),
				  htopoetcone20(0),
				  hJetHT(0),hAllJetMETSig(0),
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
  if(fDetailLvl<5){
    hTruthMuPt    = GetTH1("truthMuPt",    50,  0.0,   100.0);
    hTruthMuEta   = GetTH1("truthMuEta",   45,  -4.5,   4.5);  
    hBaseMuPt     = GetTH1("baseMuPt",    50,  0.0,   100.0);
    hBaseMuEta    = GetTH1("baseMuEta",   45,  -4.5,   4.5);
    hTruthElPt    = GetTH1("truthElPt",    50,  0.0,   100.0);
    hTruthElEta   = GetTH1("truthElEta",   45,  -4.5,   4.5);  
    hBaseElPt     = GetTH1("baseElPt",    50,  0.0,   100.0);
    hBaseElEta    = GetTH1("baseElEta",   45,  -4.5,   4.5);
    hTruthTauPt   = GetTH1("truthTauPt",    50,  0.0,   100.0);
    hTruthTauDR   = GetTH1("truthTauDR",    100,  0.0,   10.0);
    hTruthTauEta  = GetTH1("truthTauEta",   45,  -4.5,   4.5);
    hminDRLep     = GetTH1("minDRLep",   60,  0.0,   6.0);
    hptvarcone20  = GetTH1("ptvarcone20",   12,  -0.2,   1.0);  
    hptvarcone30  = GetTH1("ptvarcone30",   12,  -0.2,   1.0);  
    htopoetcone20 = GetTH1("topoetcone20",  12,  -0.2,   1.0);
    hdRj1             = GetTH1("dRj1",             20,  0.0,   10.0);		  
    hdRj2             = GetTH1("dRj2",             20,  0.0,   10.0);
  }
  // extra vars
  hmj34             = GetTH1("mj34",             50,  0.0,   1000.0);
  hminDR            = GetTH1("minDR",            20,  0.0,  10.0);		  
  hmin_mj3          = GetTH1("min_mj3",          50,  0.0,   2000.0);
  hmin_mj3_over_mjj = GetTH1("min_mj3_over_mjj", 25,  0.0,   1.0);
  hcentrality       = GetTH1("centrality",       25,  0.0,   1.0);
  hj3Pt             = GetTH1("j3Pt",             20,  0.0,   200.0);
  hj3Eta            = GetTH1("j3Eta",            22,  -4.5,  4.5);
  hj3Jvt            = GetTH1("j3Jvt",            12,  -0.2,  1.0);
  hj3FJvt           = GetTH1("j3FJvt",           22,  -0.2,  2.0);

  hAllJetMETSig = GetTH1("alljet_metsig", 200, 0, 20);
  hJetHT = GetTH1("jetHT", 50, 0.0, 1000.0);

   if(fDetailLvl<5){
    hJetEtaPt25       = GetTH1("JetEtaPt25",       90,  -4.5,  4.5);		  
    hJetEtaPt35       = GetTH1("JetEtaPt35",       90,  -4.5,  4.5);		  
    hJetEtaPt55       = GetTH1("JetEtaPt55",       90,  -4.5,  4.5);
    hmax_j_eta        = GetTH1("max_j_eta",        45,  0.0,   4.5);  
    hjj_deta_signed   = GetTH1("jj_deta_signed",   50, -10.0, 10.0);
    hjj_deta_diff     = GetTH1("jj_deta_diff",   50, -10.0, 10.0);
    hjj_deta_abs      = GetTH1("jj_deta_abs",   50, -3.0, 3.0);    
    hmuDR           = GetTH1("muDR",           25,  0.0,  5.0);
    hmuEta          = GetTH1("muEta",          30,  0.0,  3.0);
    hJetEMECvsBCIDPosPt25 = GetTH2("JetEMECvsBCIDPosPt25",  5,  -0.5,  4.5, 35, 0.0, 70);
    hJetEMECvsBCIDPosPt35 = GetTH2("JetEMECvsBCIDPosPt35",  5,  -0.5,  4.5, 35, 0.0, 70);
    hJetEMECvsBCIDPosPt55 = GetTH2("JetEMECvsBCIDPosPt55",  5,  -0.5,  4.5, 35, 0.0, 70);  
    hMetvsMu = GetTH2("MetvsMu",  50, 0.0, 500.0, 10,  0.0,  100);
    hmj1              = GetTH1("mj1",              50,  0.0,   2000.0);
    hmj2              = GetTH1("mj2",              50,  0.0,   2000.0);
    hminDRmj2         = GetTH1("minDRmj2",         50,  0.0,   2000.0);
    hZMCIDQCD    = GetTH1("ZMCIDQCD",     100,  364099.5,364199.5);
    hZPTVMCIDQCD    = GetTH1("ZPTVMCIDQCD",     26,  366009.5,366035.5);  
    hWMCIDQCD    = GetTH1("WMCIDQCD",     100,  364155.5,364255.5);
    hZMadMCIDQCD = GetTH1("ZMadMCIDQCD",  10,  361509.5,361519.5);
    hZMad2MCIDQCD= GetTH1("ZMad2MCIDQCD", 100, 363122.5,363222.5);
    hZMadFMCIDQCD= GetTH1("ZMadFMCIDQCD", 25, 311428.5,311453.5);    
    hWMadMCIDQCD = GetTH1("WMadMCIDQCD",  74,  363599.5,363673.5);
    hZPowMCIDQCD = GetTH1("ZPowMCIDQCD",  19,  301019.5,301038.5);
    hZShMCIDQCD  = GetTH1("ZShMCIDQCD",   84,  312447.5,312531.5);   
    }

  // jj_mass limits
  float binsjjmass [9] = { 0.0, 200.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0, 3500.0, 5000.0 };
  float binsjjmassGam [6] = { 0.0, 250.0, 500.0, 1000.0, 1500.0, 3000.0};
  float binsdphi [4] = { 0.0, 1.0, 2.0, 3.2 };
  hjj_mass_variableBin = GetTH1("jj_mass_variableBin",  8,  binsjjmass);
  hjj_mass_variableBinGam = GetTH1("jj_mass_variableBinGam",  5,  binsjjmassGam);  
  htruth_jj_mass_variableBin = GetTH1("truth_jj_mass_variableBin",  8,  binsjjmass);
  hjj_mass_dphi_variableBin = GetTH2("jj_mass_dphi_variableBin",  8,  binsjjmass, 3, binsdphi);

  // Rebinned met significance.
  float binsmetsig [17] = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 20.0};
  hmetsig_variableBin = GetTH1("metsig_variableBin", 16, binsmetsig);

  // TMVA variable binned
  //float binstmva[8] = {0.0, 0.75300000, 0.81700000, 0.86100000, 0.89500000, 0.92200000, 0.94600000, 1.0};
  float binstmva[8] = {0.0,0.80690000, 0.85710000, 0.88910000, 0.91370000, 0.93310000, 0.9526, 1.0};
  htmva_variableBin =  GetTH1("tmva_variableBin",  7,  binstmva);
  //float binstmva12[12] = {0.0, 0.77280000, 0.82340000, 0.85320000, 0.87660000, 0.89370000, 0.90910000, 0.92290000, 0.93480000, 0.94700000, 0.9602, 1.0};
  float binstmva12[12] = {0.0,  0.83490000, 0.86300000, 0.87740000, 0.88990000, 0.90140000, 0.91320000, 0.92450000, 0.93410000, 0.94210000, 0.94960000, 1.0};
  htmva_variableBin11 =  GetTH1("tmva_variableBin11",  11,  binstmva12);
  float binstmvamj[8] = {0.0,0.80480000, 0.83740000, 0.87190000, 0.91070000, 0.93410000, 0.9508,1.0};
  htmva_wmj_variableBin =  GetTH1("tmva_wmj_variableBin",  7,  binstmvamj);
  //float binstmvamj12[12] = {0.0, 0.77910000, 0.81730000, 0.83540000, 0.85340000, 0.87840000, 0.90440000, 0.92230000, 0.93580000, 0.94670000, 0.956, 1.0};
  //float binstmvamj12[12] = {0.0, 0.75100000, 0.80770000, 0.83910000, 0.86250000, 0.88030000, 0.89640000, 0.90950000, 0.92100000, 0.93210000, 0.9448,1.0};
  float binstmvamj12[12] = {0.0,  0.68120000, 0.76320000, 0.80770000, 0.83480000, 0.85870000, 0.87730000, 0.89510000, 0.91060000, 0.92500000, 0.94130000, 1.0};
  htmva_wmj_variableBin11 =  GetTH1("tmva_wmj_variableBin11",  11,  binstmvamj12);  

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
  if(hZPTVMCIDQCD)  hZPTVMCIDQCD->Fill(event.RunNumber, weight);
  if(hZMCIDQCD)     hZMCIDQCD->Fill(event.RunNumber, weight);  
  if(hWMCIDQCD)     hWMCIDQCD->Fill(event.RunNumber, weight);
  if(hZMadMCIDQCD)  hZMadMCIDQCD->Fill(event.RunNumber, weight);
  if(hZMad2MCIDQCD) hZMad2MCIDQCD->Fill(event.RunNumber, weight);
  if(hZMadFMCIDQCD) hZMadFMCIDQCD->Fill(event.RunNumber, weight);  
  if(hWMadMCIDQCD)  hWMadMCIDQCD->Fill(event.RunNumber, weight);  
  if(hZPowMCIDQCD)  hZPowMCIDQCD->Fill(event.RunNumber, weight);
  if(hZShMCIDQCD)   hZShMCIDQCD->Fill(event.RunNumber, weight);  
  float jj_deta = event.GetVar(Mva::jj_deta);
  if(hjj_deta_signed) hjj_deta_signed->Fill(( fabs(event.GetVar(Mva::jetEta0)) > fabs(event.GetVar(Mva::jetEta1)) ? -1.0*jj_deta : jj_deta), weight);
  if(hjj_deta_diff) hjj_deta_diff->Fill(( fabs(event.GetVar(Mva::jetEta0)) - fabs(event.GetVar(Mva::jetEta1))), weight);
  if(hjj_deta_abs) hjj_deta_abs->Fill(( fabs(event.GetVar(Mva::jetEta0)) - fabs(event.GetVar(Mva::jetEta1)))/jj_deta, weight);
  FillHist(hjj_mass_variableBin,   Mva::jj_mass, event, weight);
  FillHist(hjj_mass_variableBinGam,   Mva::jj_mass, event, weight);
  FillHist(htruth_jj_mass_variableBin,   Mva::truth_jj_mass, event, weight);  
  FillHist(htmva_variableBin,      Mva::tmva,    event, weight);
  FillHist(htmva_variableBin11,    Mva::tmva,    event, weight);
  FillHist(htmva_wmj_variableBin,      Mva::tmva,    event, weight);
  FillHist(htmva_wmj_variableBin11,    Mva::tmva,    event, weight);

  FillHist(hmetsig_variableBin, Mva::met_significance, event, weight);

  if(hjj_mass_dphi_variableBin && event.jets.size()==2) hjj_mass_dphi_variableBin->Fill(event.GetVar(Mva::jj_mass), event.GetVar(Mva::jj_dphi), weight);
  if(hMetvsMu && event.HasVar(Mva::averageIntPerXing)) hMetvsMu->Fill(event.GetVar(Mva::met_tst_nolep_et), event.GetVar(Mva::averageIntPerXing), weight);
  if(event.truth_mu.size()>0){
    if(hTruthMuPt)  hTruthMuPt ->Fill(event.truth_mu.at(0).pt, weight);
    if(hTruthMuEta) hTruthMuEta->Fill(event.truth_mu.at(0).eta, weight);
  }
  if(event.truth_el.size()>0){
    if(hTruthElPt)  hTruthElPt ->Fill(event.truth_el.at(0).pt, weight);
    if(hTruthElEta) hTruthElEta->Fill(event.truth_el.at(0).eta, weight);
  }

  if(event.muons.size()>1){
    if(hmuDR)  hmuDR->Fill(event.muons.at(0).GetVec().DeltaR(event.muons.at(1).GetVec()), weight);
    if(hmuEta) hmuEta->Fill(event.muons.at(0).eta, weight);
    if(hmuEta) hmuEta->Fill(event.muons.at(1).eta, weight);        
  }
  if(event.electrons.size()>1){
    if(hmuDR)  hmuDR->Fill(event.electrons.at(0).GetVec().DeltaR(event.electrons.at(1).GetVec()), weight);
    if(hmuEta) hmuEta->Fill(event.electrons.at(0).eta, weight);
    if(hmuEta) hmuEta->Fill(event.electrons.at(1).eta, weight);        
  }

  if(event.basemu.size()>0){
    if(hBaseMuPt) hBaseMuPt ->Fill(event.basemu.at(0).pt, weight);
    if(hBaseMuEta) hBaseMuEta->Fill(event.basemu.at(0).eta, weight);
  }
  if(event.baseel.size()>0){
    if(hBaseElPt)  hBaseElPt ->Fill(event.baseel.at(0).pt, weight);
    if(hBaseElEta) hBaseElEta->Fill(event.baseel.at(0).eta, weight);
  }
  if(event.truth_taus.size()>0){
    if(hTruthTauPt) hTruthTauPt ->Fill(event.truth_taus.at(0).pt, weight);
    for(unsigned iJet=0; iJet<event.jets.size(); ++iJet){
      if(hTruthTauDR) hTruthTauDR ->Fill(event.truth_taus.at(0).GetVec().DeltaR(event.jets.at(iJet).GetVec()), weight);
    }
    if(hTruthTauEta) hTruthTauEta->Fill(event.truth_taus.at(0).eta, weight);
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
    if(hJetEtaPt25 && tmp.Pt()<35.0){ hJetEtaPt25->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet25EMEC; }
    else if(hJetEtaPt35 && tmp.Pt()<55.0){ hJetEtaPt35->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet35EMEC; }
    else if(hJetEtaPt55) {  hJetEtaPt55->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet55EMEC; }
  }
  if(event.jets.size()>2){
    const TLorentzVector j1v = event.jets.at(0).GetLVec();
    const TLorentzVector j2v = event.jets.at(1).GetLVec();

    for(unsigned iJet=2; iJet<event.jets.size(); ++iJet){
      tmp=event.jets.at(iJet).GetLVec();
      if(hcentrality) hcentrality->Fill(event.GetVar(Mva::maxCentrality), weight);
      
      float dRj1=tmp.DeltaR(j1v);
      float dRj2=tmp.DeltaR(j2v);
      if(hdRj1) hdRj1->Fill(dRj1, weight);
      if(hdRj2) hdRj2->Fill(dRj2, weight);
      if(hminDR) hminDR->Fill(std::min(dRj1,dRj2), weight);
      if(hJetEtaPt25 && tmp.Pt()<35.0){ hJetEtaPt25->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet25EMEC; }
      else if(hJetEtaPt35 && tmp.Pt()<55.0){ hJetEtaPt35->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet35EMEC; }
      else if(hJetEtaPt55){  hJetEtaPt55->Fill(tmp.Eta(),weight); if(fabs(tmp.Eta())>2.5 && fabs(tmp.Eta())<3.2)++njet55EMEC; }
            
      float mj1 =  (tmp+j1v).M();
      float mj2 =  (tmp+j2v).M();
      if(hmj1) hmj1->Fill(mj1, weight);
      if(hmj2) hmj2->Fill(mj2, weight);
      if(hminDRmj2) hminDRmj2->Fill((dRj1<dRj2 ? mj1 : mj2), weight);
      if(hmin_mj3) hmin_mj3->Fill(std::min(mj1,mj2), weight);
      if(hmin_mj3_over_mjj) hmin_mj3_over_mjj->Fill(event.GetVar(Mva::maxmj3_over_mjj), weight);
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
    if(hJetEMECvsBCIDPosPt25) hJetEMECvsBCIDPosPt25->Fill(njet25EMEC,event.GetVar(Mva::BCIDDistanceFromFront));
    if(hJetEMECvsBCIDPosPt35) hJetEMECvsBCIDPosPt35->Fill(njet35EMEC,event.GetVar(Mva::BCIDDistanceFromFront));
    if(hJetEMECvsBCIDPosPt55) hJetEMECvsBCIDPosPt55->Fill(njet55EMEC,event.GetVar(Mva::BCIDDistanceFromFront));
  }
  // end testing

  // Hmm.. why is this necessary?
  // It seems that if we don't explicitly ->Fill() here with weights,
  // the python gets the weights wrong, since nothing is capable of setting it.
  if (hJetHT && event.HasVar(Mva::jetHT)) hJetHT->Fill(event.GetVar(Mva::jetHT), weight);
  if (hAllJetMETSig && event.HasVar(Mva::alljet_metsig)) hAllJetMETSig->Fill(event.GetVar(Mva::alljet_metsig), weight);

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
  if(hminDRLep) hminDRLep->Fill(minDR, weight);
  
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
