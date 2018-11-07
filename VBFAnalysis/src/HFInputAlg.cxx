// HFInput includes
#include "HFInputAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
//#include "xAODEventInfo/EventInfo.h"


HFInputAlg::HFInputAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty("currentVariation", currentVariation = "Nominal", "current systematics, NONE means nominal");
  declareProperty("currentSample", currentSample = "W_strong", "current samples");
  declareProperty("isMC", isMC = true, "isMC flag, true means the sample is MC");
  declareProperty("isHigh", isHigh = true, "isHigh flag, true for upward systematics");
  declareProperty("doLowNom", doLowNom = false, "isMC flag, true means the sample is MC");
  //  declareProperty("plots", doPlot = true, "doPlot flag, true means the output contains variable distributions");
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

  cout<<"NAME of input tree in intialize ======="<<currentVariation<<endl;
  if (currentSample == "data") isMC = false;
  cout<< "CURRENT  sample === "<< currentSample<<endl;
  
  std::string syst = "";
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
  }
  for (int c=1;c<4;c++) {
    hSR.push_back(HistoAppend(HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC), string("SR"+to_string(c))));
    hCRWep.push_back(HistoAppend(HistoNameMaker(currentSample,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC), string("oneElePosCR"+to_string(c))));
    hCRWen.push_back(HistoAppend(HistoNameMaker(currentSample,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC), string("oneEleNegCR"+to_string(c))));
    hCRWepLowSig.push_back(HistoAppend(HistoNameMaker(currentSample,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC), string("oneElePosLowSigCR"+to_string(c))));
    hCRWenLowSig.push_back(HistoAppend(HistoNameMaker(currentSample,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC), string("oneEleNegLowSigCR"+to_string(c))));
    hCRWmp.push_back(HistoAppend(HistoNameMaker(currentSample,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC), string("oneMuPosCR"+to_string(c))));
    hCRWmn.push_back(HistoAppend(HistoNameMaker(currentSample,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC), string("oneMuNegCR"+to_string(c))));
    hCRZee.push_back(HistoAppend(HistoNameMaker(currentSample,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC), string("twoEleCR"+to_string(c))));
    hCRZmm.push_back(HistoAppend(HistoNameMaker(currentSample,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC), string("twoMuCR"+to_string(c))));
    //    CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC)+"_cuts", hSR[c-1]));
    vector <std::pair<vector <TH1F*>, std::string>> hnames;
    hnames.push_back(std::make_pair(hSR.back(),HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC)));
    hnames.push_back(std::make_pair(hCRWep.back(), HistoNameMaker(currentSample,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC)));
    hnames.push_back(std::make_pair(hCRWen.back(), HistoNameMaker(currentSample,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC)));
    hnames.push_back(std::make_pair(hCRWepLowSig.back(), HistoNameMaker(currentSample,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC)));
    hnames.push_back(std::make_pair(hCRWenLowSig.back(), HistoNameMaker(currentSample,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC)));
    hnames.push_back(std::make_pair(hCRWmp.back(), HistoNameMaker(currentSample,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC)));
    hnames.push_back(std::make_pair(hCRWmn.back(), HistoNameMaker(currentSample,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC)));
    hnames.push_back(std::make_pair(hCRZee.back(), HistoNameMaker(currentSample,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC)));
    hnames.push_back(std::make_pair(hCRZmm.back(), HistoNameMaker(currentSample,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC)));
    CheckHists(hnames);
  }
  return StatusCode::SUCCESS;
}
std::string HFInputAlg::HistoNameMaker(std::string currentSample, std::string currentCR, std::string bin, std::string syst, Bool_t isMC) {
  if (isMC) {
    if (bin == "") return "h"+currentSample+ "_"+syst+"_"+currentCR + "_obs";
    else if (currentSample.find("signal") != std::string::npos) return "h"+currentSample+syst+"_"+currentCR + "_obs";
    //    else return "h"+currentSample+ "_VBFjetSel_bin"+bin+syst+"_"+currentCR + "_obs_cuts";
    else return "h"+currentSample+ "_VBFjetSel_"+bin+syst+"_"+currentCR + "_obs";
  } else {
    //    return "h"+currentSample+ "_NONE_"+currentCR + "_obs_cuts";
    return "h"+currentSample+ "_NONE_"+currentCR + "_obs";  
  }
}

vector <TH1F*> HFInputAlg::HistoAppend(std::string name, std::string currentCR) {
  vector <TH1F*> h;
  h.push_back(new TH1F((name+"_cuts").c_str(), (name+"_cuts;;").c_str(), 1, 0.5, 1.5));
  h.push_back(new TH1F((name+"_jj_mass").c_str(), (name+"_jj_mass;;").c_str(), 10, 0, 5000));
  h.push_back(new TH1F((name+"_met_et").c_str(), (name+"_met_et;;").c_str(), 10, 0, 800));
  h.push_back(new TH1F((name+"_lepmet_et").c_str(), (name+"_lepmet_et;;").c_str(), 10, 0, 800));
  // h.back()->GetXaxis()->SetBinLabel(1,(currentCR).c_str());
  //  h.push_back(new TH1F((name+"_").c_str(), (name+"_cuts;;").c_str(), 1, 0.5, 1.5));
  //  CHECK(histSvc()->regHist("/MYSTREAM/"+name, h.back()));
  return h;
}

StatusCode HFInputAlg::CheckHists(vector <std::pair<vector <TH1F*>, std::string>> hnames){
  for (auto hname : hnames) {
    CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_cuts", std::get<0>(hname)[0]));
    CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_jj_mass", std::get<0>(hname)[1]));
    CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_met_et", std::get<0>(hname)[2]));
    CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_lepmet_et", std::get<0>(hname)[3]));
  }
  return StatusCode::SUCCESS;
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

  //  TLorentzVector lep1,lep2,Z;
  m_tree->GetEntry(m_tree->GetReadEntry());
  if (!((passJetCleanTight == 1) & (n_jet ==2) & (jet_pt->at(0) > 80e3) & (jet_pt->at(1) > 50e3) & (jj_dphi < 1.8) & (jj_deta > 4.8) & ((jet_eta->at(0) * jet_eta->at(1))<0) & (jj_mass > 1e6))) return StatusCode::SUCCESS; //metjet_CST>150e3

  if(n_el== 1) {
    met_significance = met_tst_et/1000/sqrt(sqrt(el_pt->at(0)*el_pt->at(0)*cos(el_phi->at(0))*cos(el_phi->at(0))+el_pt->at(0)*el_pt->at(0)*sin(el_phi->at(0))*sin(el_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*sin(jet_phi->at(0))*sin(jet_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*cos(jet_phi->at(0))*cos(jet_phi->at(0))+jet_pt->at(1)*jet_pt->at(1)*sin(jet_phi->at(1))*sin(jet_phi->at(1))+jet_pt->at(1)*jet_pt->at(1)*cos(jet_phi->at(1))*cos(jet_phi->at(1)))/1000);
  } else {
    met_significance = 0;
  }

  if ((trigger_met == 1) & (met_tst_et > 180e3) & (met_tst_j1_dphi>1.0) & (met_tst_j2_dphi>1.0) & (n_el == 0) & (n_mu == 0)) SR = true;
    // lep1->SetPtEtaPhiM(el_pt->at(0),el_eta->at(0),el_phi->at(0),el_m->at(0));
    // lep2->SetPtEtaPhiM(el_pt->at(0),el_eta->at(0),el_phi->at(0),el_m->at(0));
    // Z = lep1+lep2;
    // Z_mass = Z.M()
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance > 4.0)) CRWep = true;}
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance > 4.0)) CRWen = true;}
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance <= 4.0)) CRWepLowSig = true;}
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance <= 4.0)) CRWenLowSig = true;}
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) > 0)) CRWmp = true;}
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) < 0)) CRWmn = true;}
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 2) & (n_mu == 0)){ if ((el_charge->at(0)*el_charge->at(1) < 0)) CRZee = true;}
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 2)){ if ((mu_charge->at(0)*mu_charge->at(1) < 0)) CRZmm = true;}

  Float_t w_final = 1;
  Float_t lumi = 36.1;
  if (isMC) w_final = w*1000*lumi;
  int bin = 0;
  if (jj_mass < 1.5e6) bin = 0;
  else if (jj_mass < 2e6) bin = 1;
  else bin = 2;
			 
  if (SR){
    hSR[bin][0]->Fill(1,w_final);
    hSR[bin][1]->Fill(jj_mass/(1e3),w_final);
    hSR[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hSR[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
  }
  if (CRWep){
    hCRWep[bin][0]->Fill(1,w_final);
    hCRWep[bin][1]->Fill(jj_mass/(1e3),w_final);
    hCRWep[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hCRWep[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
  }
  if (CRWen){
    hCRWen[bin][0]->Fill(1,w_final);
    hCRWen[bin][1]->Fill(jj_mass/(1e3),w_final);
    hCRWen[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hCRWen[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
  }
  if (CRWepLowSig){
    hCRWepLowSig[bin][0]->Fill(1,w_final);
    hCRWepLowSig[bin][1]->Fill(jj_mass/(1e3),w_final);
    hCRWepLowSig[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hCRWepLowSig[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
  }
  if (CRWenLowSig){
    hCRWenLowSig[bin][0]->Fill(1,w_final);
    hCRWenLowSig[bin][1]->Fill(jj_mass/(1e3),w_final);
    hCRWenLowSig[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hCRWenLowSig[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
  }
  if (CRWmp){
    hCRWmp[bin][0]->Fill(1,w_final);
    hCRWmp[bin][1]->Fill(jj_mass/(1e3),w_final);
    hCRWmp[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hCRWmp[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
  }
  if (CRWmn){
    hCRWmn[bin][0]->Fill(1,w_final);
    hCRWmn[bin][1]->Fill(jj_mass/(1e3),w_final);
    hCRWmn[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hCRWmn[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
  }
  if (CRZee){
    hCRZee[bin][0]->Fill(1,w_final);
    hCRZee[bin][1]->Fill(jj_mass/(1e3),w_final);
    hCRZee[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hCRZee[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
  }
  if (CRZmm){
    hCRZmm[bin][0]->Fill(1,w_final);
    hCRZmm[bin][1]->Fill(jj_mass/(1e3),w_final);
    hCRZmm[bin][2]->Fill(met_tst_et/(1e3),w_final);
    hCRZmm[bin][3]->Fill(met_tst_nolep_et/(1e3),w_final);
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
  if (doLowNom) {
    m_treeName = currentSample+"Nominal";
  } else{
    m_treeName = currentSample+currentVariation;
  }
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  m_tree->SetBranchStatus("*",0);
  m_tree->SetBranchStatus("runNumber", 1);
  m_tree->SetBranchStatus("w", 1);
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
  m_tree->SetBranchStatus("jet_timing",1);

  m_tree->SetBranchAddress("w", &w);
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
  return StatusCode::SUCCESS;
}
