// HFInput includes
#include "HFInputAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
//#include "xAODEventInfo/EventInfo.h"
#include "TLorentzVector.h"

HFInputAlg::HFInputAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty("currentVariation", currentVariation = "Nominal", "current systematics, NONE means nominal");
  declareProperty("currentSample", currentSample = "W_strong", "current samples");
  declareProperty("isMC", isMC = true, "isMC flag, true means the sample is MC");
  declareProperty("ExtraVars", m_extraVars = 0, "true if extra variables should be cut on" );
  declareProperty("isHigh", isHigh = true, "isHigh flag, true for upward systematics");
  declareProperty("doLowNom", doLowNom = false, "isMC flag, true means the sample is MC");
  declareProperty("weightSyst", weightSyst = false, "weightSyst flag, true for weight systematics");
  //declareProperty( "Property", m_nProperty = 0, "My Example Integer Property" ); //example property declaration
}


HFInputAlg::~HFInputAlg() {}

bool HFInputAlg::replace(std::string& str, const std::string& from, const std::string& to) {
  size_t start_pos = str.find(from);
  if(start_pos == std::string::npos)
    return false;
  str.replace(start_pos, from.length(), to);
  return true;
}

StatusCode HFInputAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");
  //
  //This is called once, before the start of the event loop
  //Retrieves of tools you have configured in the joboptions go here
  //
  mu_charge= new std::vector<int>(0);
  mu_pt= new std::vector<float>(0);
  mu_phi= new std::vector<float>(0);
  mu_eta= new std::vector<float>(0);
  el_charge= new std::vector<int>(0);
  el_pt= new std::vector<float>(0);
  el_phi= new std::vector<float>(0);
  el_eta= new std::vector<float>(0);
  jet_pt= new std::vector<float>(0);
  jet_phi= new std::vector<float>(0);
  jet_eta= new std::vector<float>(0);
  jet_m= new std::vector<float>(0);
  jet_timing= new std::vector<float>(0); 
  jet_passJvt= new std::vector<int>(0); 
  jet_fjvt= new std::vector<float>(0);
  baseel_pt= new std::vector<float>(0);
  baseel_ptvarcone20= new std::vector<float>(0);
  basemu_pt= new std::vector<float>(0);
  basemu_ptvarcone20= new std::vector<float>(0); 
  
  cout<<"NAME of input tree in intialize ======="<<currentVariation<<endl;
  if (currentSample == "data") isMC = false;
  cout<< "CURRENT  sample === "<< currentSample<<endl;
  std::cout << "Running Extra Veto? " << m_extraVars << std::endl;
  std::cout << "is a weightSyst? " << weightSyst << std::endl;

  std::string syst;
  bool replacedHigh = false;
  bool replacedLow = false;
  if (isMC) {
    syst=currentVariation;
    cout << "CURRENT syst === " << syst << endl;
    if (syst != "Nominal") {
      replacedHigh = replace(syst, "__1up", "High");
      replacedLow = replace(syst, "__1down", "Low");
      if (doLowNom){
	if (replacedHigh) replace(syst, "High", "Low"); else syst.append("Low");
      } else{
	if (isHigh && !replacedHigh) replacedHigh = replace(syst, "Up", "High");
	if (isHigh && !replacedHigh) syst.append("High");
	if (!isHigh && !replacedLow) replacedLow = replace(syst, "Down", "Low");
	if (!isHigh && !replacedLow) syst.append("Low");
      }
    } else {
      syst = "Nom";
    }
    for (int c=1;c<4;c++) {
      hSR.push_back( new TH1F(HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWep.push_back(new TH1F(HistoNameMaker(currentSample,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWen.push_back(new TH1F(HistoNameMaker(currentSample,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWepLowSig.push_back(new TH1F(HistoNameMaker(currentSample,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWenLowSig.push_back(new TH1F(HistoNameMaker(currentSample,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWmp.push_back(new TH1F(HistoNameMaker(currentSample,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWmn.push_back(new TH1F(HistoNameMaker(currentSample,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRZee.push_back(new TH1F(HistoNameMaker(currentSample,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRZmm.push_back(new TH1F(HistoNameMaker(currentSample,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC), hSR[c-1]));  
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC), hCRWep[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC), hCRWen[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC), hCRWepLowSig[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC), hCRWenLowSig[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC), hCRWmp[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC), hCRWmn[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC), hCRZee[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC), hCRZmm[c-1]));
      hSR[c-1]->GetXaxis()->SetBinLabel(1,("SR"+to_string(c)).c_str());
      hCRWep[c-1]->GetXaxis()->SetBinLabel(1,("oneElePosCR"+to_string(c)).c_str());
      hCRWen[c-1]->GetXaxis()->SetBinLabel(1,("oneEleNegCR"+to_string(c)).c_str());
      hCRWepLowSig[c-1]->GetXaxis()->SetBinLabel(1,("oneElePosLowSigCR"+to_string(c)).c_str());
      hCRWenLowSig[c-1]->GetXaxis()->SetBinLabel(1,("oneEleNegLowSIgCR"+to_string(c)).c_str());
      hCRWmp[c-1]->GetXaxis()->SetBinLabel(1,("oneMuPosCR"+to_string(c)).c_str());
      hCRWmn[c-1]->GetXaxis()->SetBinLabel(1,("oneMuNegCR"+to_string(c)).c_str());
      hCRZee[c-1]->GetXaxis()->SetBinLabel(1,("twoEleCR"+to_string(c)).c_str());
      hCRZmm[c-1]->GetXaxis()->SetBinLabel(1,("twoMuCR"+to_string(c)).c_str());
    }} else {
    for (int c=1;c<4;c++) {
      hSR.push_back( new TH1F(HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWep.push_back(new TH1F(HistoNameMaker(currentSample,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWen.push_back(new TH1F(HistoNameMaker(currentSample,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWepLowSig.push_back(new TH1F(HistoNameMaker(currentSample,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWenLowSig.push_back(new TH1F(HistoNameMaker(currentSample,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWmp.push_back(new TH1F(HistoNameMaker(currentSample,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRWmn.push_back(new TH1F(HistoNameMaker(currentSample,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRZee.push_back(new TH1F(HistoNameMaker(currentSample,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      hCRZmm.push_back(new TH1F(HistoNameMaker(currentSample,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC).c_str(), (""+HistoNameMaker(currentSample,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC)+";;").c_str(), 1, 0.5, 1.5));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC), hSR[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC), hCRWep[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC), hCRWen[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC), hCRWepLowSig[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC), hCRWenLowSig[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC), hCRWmp[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC), hCRWmn[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC), hCRZee[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC), hCRZmm[c-1]));
      hSR[c-1]->GetXaxis()->SetBinLabel(1,("SR"+to_string(c)).c_str());
      hCRWep[c-1]->GetXaxis()->SetBinLabel(1,("oneElePosCR"+to_string(c)).c_str());
      hCRWen[c-1]->GetXaxis()->SetBinLabel(1,("oneEleNegCR"+to_string(c)).c_str());
      hCRWepLowSig[c-1]->GetXaxis()->SetBinLabel(1,("oneElePosLowSigCR"+to_string(c)).c_str());
      hCRWenLowSig[c-1]->GetXaxis()->SetBinLabel(1,("oneEleNegLowSigCR"+to_string(c)).c_str());
      hCRWmp[c-1]->GetXaxis()->SetBinLabel(1,("oneMuPosCR"+to_string(c)).c_str());
      hCRWmn[c-1]->GetXaxis()->SetBinLabel(1,("oneMuNegCR"+to_string(c)).c_str());
      hCRZee[c-1]->GetXaxis()->SetBinLabel(1,("twoEleCR"+to_string(c)).c_str());
      hCRZmm[c-1]->GetXaxis()->SetBinLabel(1,("twoMuCR"+to_string(c)).c_str());
    }
  }
  return StatusCode::SUCCESS;
}
std::string HFInputAlg::HistoNameMaker(std::string currentSample, std::string currentCR, std::string bin, std::string syst, Bool_t isMC) {
  if (isMC) {
    if (bin == "") return "h"+currentSample+ "_"+syst+"_"+currentCR + "_obs_cuts";
    else if (currentSample.find("signal") != std::string::npos) return "h"+currentSample+syst+"_"+currentCR + "_obs_cuts";
    //    else return "h"+currentSample+ "_VBFjetSel_bin"+bin+syst+"_"+currentCR + "_obs_cuts";
    else return "h"+currentSample+ "_VBFjetSel_"+bin+syst+"_"+currentCR + "_obs_cuts";
  } else {
    //    return "h"+currentSample+ "_NONE_"+currentCR + "_obs_cuts";
    return "h"+currentSample+ "_NONE_"+currentCR + "_obs_cuts";  
  }
}

StatusCode HFInputAlg::finalize() {
  ATH_MSG_INFO ("Finalizing " << name() << "...");

  return StatusCode::SUCCESS;
}

StatusCode HFInputAlg::execute() {  
  ATH_MSG_DEBUG ("Executing " << name() << "...");
  setFilterPassed(false); //optional: start with algorithm not passed

  npevents++;
  if( (npevents%10000) ==0) std::cout <<" Processed "<< npevents << " Events"<<std::endl;

  bool SR = false;
  bool CRWep = false;
  bool CRWen = false;
  bool CRWepLowSig = false;
  bool CRWenLowSig = false;
  bool CRWmp = false;
  bool CRWmn = false;
  bool CRZee = false;
  bool CRZmm = false;

  m_tree->GetEntry(m_tree->GetReadEntry());

  // Compute jet centrality
  float max_centrality=0.0, maxmj3_over_mjj=0.0;
  TLorentzVector j1v,j2v, tmp;
  if(jet_eta->size()>1){
    j1v.SetPtEtaPhiM(jet_pt->at(0), jet_eta->at(0), jet_phi->at(0), jet_m->at(0));
    j2v.SetPtEtaPhiM(jet_pt->at(1), jet_eta->at(1), jet_phi->at(1), jet_m->at(1));
  }
  for(unsigned iJet=2; iJet<jet_eta->size(); ++iJet){
    tmp.SetPtEtaPhiM(jet_pt->at(iJet), jet_eta->at(iJet), jet_phi->at(iJet), jet_m->at(iJet));
    float centrality = exp(-4.0/std::pow(jj_deta,2) * std::pow(jet_eta->at(iJet) - (jet_eta->at(0)+jet_eta->at(1))/2.0,2));
    if(max_centrality<centrality) max_centrality=centrality;
    float mj1 = (tmp+j1v).M();
    float mj2 = (tmp+j2v).M();
    float j3_over_mjj =std::min(mj1,mj2)/jj_mass;
    if(j3_over_mjj>maxmj3_over_mjj) maxmj3_over_mjj = j3_over_mjj;
  }

  // Cuts
  float METCut=180.0e3; // 150.0e3
  float METCSTJetCut = 150.0e3; // 120.0e3
  float jj_detaCut = 4.8; // 4.0
  float jj_massCut = 1000.0e3;
  bool jetCut = (n_jet ==2); //  (n_jet>1 && n_jet<5 && max_centrality<0.6 && maxmj3_over_mjj<0.05)

  // extra vetos  
  bool leptonVeto = false;
  bool metSoftVeto = false;
  bool fJVTVeto = false;
  bool JetTimingVeto = false;
  unsigned n_baseel=0;
  unsigned n_basemu=0;
  if(m_extraVars>0){
    for(unsigned iEle=0; iEle<baseel_pt->size(); ++iEle){
      if(baseel_pt->at(iEle)>4.5e3) ++n_baseel;
    }
    for(unsigned iMuo=0; iMuo<basemu_pt->size(); ++iMuo){
      if(basemu_pt->at(iMuo)>4.0e3) ++n_basemu;
    }

    leptonVeto = (n_baseel>0 || n_basemu>0) && !((n_el+n_mu==1 && n_baseel+n_basemu==1) || (n_el+n_mu==2 && n_baseel+n_basemu==2));
    metSoftVeto = met_soft_tst_et>20.0e3;
    if(jet_fjvt->size()>1)
      fJVTVeto = fabs(jet_fjvt->at(0))>0.5 || fabs(jet_fjvt->at(1))>0.5;
    else fJVTVeto=true;
    if(jet_timing->size()>1)
      JetTimingVeto = fabs(jet_timing->at(0))>11.0 || fabs(jet_timing->at(1))>11.0;
    else JetTimingVeto = true;

    // veto events with tighter selections
    if(metSoftVeto || fJVTVeto || JetTimingVeto || leptonVeto) return StatusCode::SUCCESS;

    if(m_extraVars>1){
      METCut=150.0e3;
      METCSTJetCut=120.0e3;
      jj_detaCut=4.0;
      jetCut = (n_jet>1 && n_jet<5 && max_centrality<0.6 && maxmj3_over_mjj<0.05);
    }
  }
  xeSFTrigWeight=1.0;
  if(isMC && jet_pt && jet_pt->size()>1 && currentVariation!="xeSFTrigWeight__1up"){ // the MET trigger SF is turned off in the up variation. so it will be =1.
    TLorentzVector tmp, jj; 
    tmp.SetPtEtaPhiM(jet_pt->at(0), jet_eta->at(0),jet_phi->at(0),jet_m->at(0));    
    jj=tmp;
    tmp.SetPtEtaPhiM(jet_pt->at(1), jet_eta->at(1),jet_phi->at(1),jet_m->at(1));    
    jj+=tmp;
    xeSFTrigWeight = weightXETrigSF(met_tst_et); // met was used in the end instead of jj.Pt() 
  }

  // MET choice to be implemented...
  if (!((passJetCleanTight == 1) & jetCut & (jet_pt->at(0) > 80e3) & (jet_pt->at(1) > 50e3) & (jj_dphi < 1.8) & (jj_deta > jj_detaCut) & ((jet_eta->at(0) * jet_eta->at(1))<0) & (jj_mass > jj_massCut))) return StatusCode::SUCCESS; 

  if(n_el== 1) {
    met_significance = met_tst_et/1000/sqrt((el_pt->at(0)+jet_pt->at(0)+jet_pt->at(1))/1000.0);
  } else {
    met_significance = 0;
  }

  bool trigger_lep_bool = (trigger_lep & 0x1)==0x1;
  if(m_extraVars) trigger_lep_bool = (trigger_lep>0);

  if ((trigger_met == 1) & (met_tst_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_j1_dphi>1.0) & (met_tst_j2_dphi>1.0) & (n_el == 0) & (n_mu == 0)) SR = true;
  if ((trigger_lep_bool) & (met_tst_nolep_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance > 4.0)) CRWep = true;}
  if ((trigger_lep_bool) & (met_tst_nolep_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance > 4.0)) CRWen = true;}
  if ((trigger_lep_bool) & (met_tst_nolep_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance <= 4.0)) CRWepLowSig = true;}
  if ((trigger_lep_bool) & (met_tst_nolep_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance <= 4.0)) CRWenLowSig = true;}
  if ((trigger_lep_bool) & (met_tst_nolep_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) > 0)) CRWmp = true;}
  if ((trigger_lep_bool) & (met_tst_nolep_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) < 0)) CRWmn = true;}
  if ((trigger_lep_bool) & (met_tst_nolep_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 2) & (n_mu == 0)){ if ((el_charge->at(0)*el_charge->at(1) < 0)) CRZee = true;}
  if ((trigger_lep_bool) & (met_tst_nolep_et > METCut) & (met_cst_jet > METCSTJetCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 2)){ if ((mu_charge->at(0)*mu_charge->at(1) < 0)) CRZmm = true;}

  Float_t w_final = 1;
  Float_t lumi = 36.1;
  if (isMC) w_final = w*1000*lumi;
  if (SR){
    if (jj_mass < 1.5e6) hSR[0]->Fill(1,w_final*xeSFTrigWeight);
    else if (jj_mass < 2e6) hSR[1]->Fill(1,w_final*xeSFTrigWeight);
    else hSR[2]->Fill(1,w_final*xeSFTrigWeight);
  }
  if (CRWep){
    if (jj_mass < 1.5e6) hCRWep[0]->Fill(1,w_final);
    else if (jj_mass < 2e6) hCRWep[1]->Fill(1,w_final);
    else hCRWep[2]->Fill(1,w_final);
  }
  if (CRWen){
    if (jj_mass < 1.5e6) hCRWen[0]->Fill(1,w_final);
    else if (jj_mass < 2e6) hCRWen[1]->Fill(1,w_final);
    else hCRWen[2]->Fill(1,w_final);
  }
  if (CRWepLowSig){
    if (jj_mass < 1.5e6) hCRWepLowSig[0]->Fill(1,w_final);
    else if (jj_mass < 2e6) hCRWepLowSig[1]->Fill(1,w_final);
    else hCRWepLowSig[2]->Fill(1,w_final);
  }
  if (CRWenLowSig){
    if (jj_mass < 1.5e6) hCRWenLowSig[0]->Fill(1,w_final);
    else if (jj_mass < 2e6) hCRWenLowSig[1]->Fill(1,w_final);
    else hCRWenLowSig[2]->Fill(1,w_final);
  }
  if (CRWmp){
    if (jj_mass < 1.5e6) hCRWmp[0]->Fill(1,w_final);
    else if (jj_mass < 2e6) hCRWmp[1]->Fill(1,w_final);
    else hCRWmp[2]->Fill(1,w_final);
  }
  if (CRWmn){
    if (jj_mass < 1.5e6) hCRWmn[0]->Fill(1,w_final);
    else if (jj_mass < 2e6) hCRWmn[1]->Fill(1,w_final);
    else hCRWmn[2]->Fill(1,w_final);
  }
  if (CRZee){
    if (jj_mass < 1.5e6) hCRZee[0]->Fill(1,w_final);
    else if (jj_mass < 2e6) hCRZee[1]->Fill(1,w_final);
    else hCRZee[2]->Fill(1,w_final);
  }
  if (CRZmm){
    if (jj_mass < 1.5e6) hCRZmm[0]->Fill(1,w_final);
    else if (jj_mass < 2e6) hCRZmm[1]->Fill(1,w_final);
    else hCRZmm[2]->Fill(1,w_final);
  }


  setFilterPassed(true); //if got here, assume that means algorithm passed
  return StatusCode::SUCCESS;
}

StatusCode HFInputAlg::beginInputFile() { 
  //
  //This method is called at the start of each input file, even if
  //the input file contains no events. Accumulate metadata information here
  //

  //example of retrieval of CutBookkeepers: (remember you will need to include the necessary header files and use statements in requirements file)
  // const xAOD::CutBookkeeperContainer* bks = 0;
  // CHECK( inputMetaStore()->retrieve(bks, "CutBookkeepers") );

  //example of IOVMetaData retrieval (see https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/AthAnalysisBase#How_to_access_file_metadata_in_C)
  //float beamEnergy(0); CHECK( retrieveMetadata("/TagInfo","beam_energy",beamEnergy) );
  //std::vector<float> bunchPattern; CHECK( retrieveMetadata("/Digitiation/Parameters","BeamIntensityPattern",bunchPattern) );
  if (doLowNom || weightSyst) {
    m_treeName = currentSample+"Nominal";
  } else{
    m_treeName = currentSample+currentVariation;
  }
  std::cout << "Tree Name: " <<m_treeName <<std::endl;
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  std::cout << "Tree Entries: " <<m_tree->GetEntries() <<std::endl;
  m_tree->SetBranchStatus("*",0);
  if(weightSyst && currentVariation!="xeSFTrigWeight__1up"){// MET trigger SF systematic is computed differently. The variable is saved. So here we just pickup the nominal weights
    bool found=false;
    TObjArray *var_list = m_tree->GetListOfBranches();
    for(unsigned a=0; a<unsigned(var_list->GetEntries()); ++a) { 
      TString var_name = var_list->At(a)->GetName();
      if(var_name.Contains(currentVariation)){
	if(var_name.Contains("ANTISF") && currentVariation.find("ANTISF")==std::string::npos) continue; // checking that the antiID SF are treated separately. skipping if they dont match to avoid picking the ID SF
	m_tree->SetBranchStatus(var_name, 1);
	m_tree->SetBranchAddress(var_name, &w);
	found=true;
	break;
      }
    }  
    if(!found){
      std::cout << "ERROR - did not find the correct weight systematic for " << currentVariation <<std::endl;
      m_tree->SetBranchStatus("w", 1);
      m_tree->SetBranchAddress("w", &w);
    }
  }else{
    m_tree->SetBranchStatus("w", 1);
    m_tree->SetBranchAddress("w", &w);
  }
  m_tree->SetBranchStatus("runNumber", 1);
  m_tree->SetBranchStatus("passJetCleanTight", 1);
  m_tree->SetBranchStatus("trigger_met", 1);
  m_tree->SetBranchStatus("trigger_lep", 1);
  m_tree->SetBranchStatus("n_jet",1);
  m_tree->SetBranchStatus("n_el",1);
  m_tree->SetBranchStatus("n_mu",1);
  m_tree->SetBranchStatus("jj_mass",1);
  m_tree->SetBranchStatus("jj_deta",1);
  m_tree->SetBranchStatus("jj_dphi",1);
  m_tree->SetBranchStatus("met_tst_j1_dphi",1);
  m_tree->SetBranchStatus("met_tst_j2_dphi",1);
  m_tree->SetBranchStatus("met_tst_nolep_j1_dphi",1);
  m_tree->SetBranchStatus("met_tst_nolep_j2_dphi",1);
  m_tree->SetBranchStatus("met_tst_et",1);
  m_tree->SetBranchStatus("met_tst_nolep_et",1);
  m_tree->SetBranchStatus("met_cst_jet",1);
  m_tree->SetBranchStatus("mu_charge",1);
  m_tree->SetBranchStatus("mu_pt",1);
  m_tree->SetBranchStatus("mu_phi",1);
  m_tree->SetBranchStatus("mu_eta",1);
  m_tree->SetBranchStatus("el_charge",1);
  m_tree->SetBranchStatus("el_pt",1);
  m_tree->SetBranchStatus("el_phi",1);
  m_tree->SetBranchStatus("el_eta",1);
  m_tree->SetBranchStatus("jet_pt",1);
  m_tree->SetBranchStatus("jet_phi",1);
  m_tree->SetBranchStatus("jet_eta",1);
  m_tree->SetBranchStatus("jet_m",1);
  m_tree->SetBranchStatus("jet_timing",1);

  m_tree->SetBranchAddress("runNumber",&runNumber);
  m_tree->SetBranchAddress("trigger_met", &trigger_met);
  m_tree->SetBranchAddress("trigger_lep", &trigger_lep);
  m_tree->SetBranchAddress("passJetCleanTight", &passJetCleanTight);
  m_tree->SetBranchAddress("n_jet",&n_jet);
  m_tree->SetBranchAddress("n_el",&n_el);
  m_tree->SetBranchAddress("n_mu",&n_mu);
  m_tree->SetBranchAddress("jj_mass",&jj_mass);
  m_tree->SetBranchAddress("jj_deta",&jj_deta);
  m_tree->SetBranchAddress("jj_dphi",&jj_dphi);
  m_tree->SetBranchAddress("met_tst_j1_dphi",&met_tst_j1_dphi);
  m_tree->SetBranchAddress("met_tst_j2_dphi",&met_tst_j2_dphi);
  m_tree->SetBranchAddress("met_tst_nolep_j1_dphi",&met_tst_nolep_j1_dphi);
  m_tree->SetBranchAddress("met_tst_nolep_j2_dphi",&met_tst_nolep_j2_dphi);
  m_tree->SetBranchAddress("met_tst_et",&met_tst_et);
  m_tree->SetBranchAddress("met_tst_nolep_et",&met_tst_nolep_et);
  m_tree->SetBranchAddress("met_cst_jet",&met_cst_jet);
  m_tree->SetBranchAddress("mu_charge",&mu_charge);
  m_tree->SetBranchAddress("mu_pt",&mu_pt);
  m_tree->SetBranchAddress("el_charge",&el_charge);
  m_tree->SetBranchAddress("el_pt",&el_pt);
  m_tree->SetBranchAddress("jet_pt",&jet_pt);
  m_tree->SetBranchAddress("jet_timing",&jet_timing);
  m_tree->SetBranchAddress("mu_phi",&mu_phi);
  m_tree->SetBranchAddress("el_phi",&el_phi);
  m_tree->SetBranchAddress("mu_eta",&mu_eta);
  m_tree->SetBranchAddress("el_eta",&el_eta);
  m_tree->SetBranchAddress("jet_phi",&jet_phi);
  m_tree->SetBranchAddress("jet_eta",&jet_eta);
  m_tree->SetBranchAddress("jet_m",&jet_m);

  if(m_extraVars>0){  
    m_tree->SetBranchStatus("met_soft_tst_et",1);
    m_tree->SetBranchStatus("met_tenacious_tst_et",1);
    m_tree->SetBranchStatus("met_tighter_tst_et",1);
    m_tree->SetBranchStatus("met_tight_tst_et",1);
    m_tree->SetBranchStatus("jet_fjvt",1);
    m_tree->SetBranchStatus("baseel_pt",1);
    m_tree->SetBranchStatus("baseel_ptvarcone20",1);
    m_tree->SetBranchStatus("basemu_pt",1);
    m_tree->SetBranchStatus("basemu_ptvarcone20",1);

    m_tree->SetBranchAddress("met_soft_tst_et",        &met_soft_tst_et);
    m_tree->SetBranchAddress("met_tenacious_tst_et",   &met_tenacious_tst_et);
    m_tree->SetBranchAddress("met_tight_tst_et",       &met_tight_tst_et);
    m_tree->SetBranchAddress("met_tighter_tst_et",     &met_tighter_tst_et);    
    m_tree->SetBranchAddress("jet_fjvt",            &jet_fjvt);
    m_tree->SetBranchAddress("baseel_ptvarcone20",  &baseel_ptvarcone20);
    m_tree->SetBranchAddress("baseel_pt",           &baseel_pt);
    m_tree->SetBranchAddress("basemu_pt",           &basemu_pt);
    m_tree->SetBranchAddress("basemu_ptvarcone20",  &basemu_ptvarcone20);
  }
  return StatusCode::SUCCESS;
}

double HFInputAlg::weightXETrigSF(const float jj_pt) {
  static const double p0 = 59.3407;
  static const double p1 = 54.9134;
  double x = jj_pt / 1.0e3;
  if (x < 100) { return 0; }
  if (x > 240) { x = 240; }
  double sf = 0.5*(1+TMath::Erf((x-p0)/(TMath::Sqrt(2)*p1)));
  if(sf<0) sf=0.0;
  if(sf > 1.5) sf=1.5;
  return sf;
}
