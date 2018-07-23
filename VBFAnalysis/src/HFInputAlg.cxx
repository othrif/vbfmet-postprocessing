// HFInput includes
#include "HFInputAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
//#include "xAODEventInfo/EventInfo.h"


HFInputAlg::HFInputAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty("currentVariation", currentVariation = "NONE", "current systematics, NONE means nominal");
  declareProperty("currentSample", currentSample = "W_strong", "current samples");
  //declareProperty( "Property", m_nProperty = 0, "My Example Integer Property" ); //example property declaration
}


HFInputAlg::~HFInputAlg() {}


StatusCode HFInputAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");
  //
  //This is called once, before the start of the event loop
  //Retrieves of tools you have configured in the joboptions go here
  //

  //HERE IS AN EXAMPLE
  //We will create a histogram and a ttree and register them to the histsvc
  //Remember to configure the histsvc stream in the joboptions
  //
  //m_myHist = new TH1D("myHist","myHist",100,0,100);
  //CHECK( histSvc()->regHist("/MYSTREAM/myHist", m_myHist) ); //registers histogram to output stream
  //m_myTree = new TTree("myTree","myTree");
  //CHECK( histSvc()->regTree("/MYSTREAM/SubDirectory/myTree", m_myTree) ); //registers tree to output stream inside a sub-directory
  
  bool isMC = true;
  //  currentVariation = "NONE";
  cout<<"NAME of input tree in intialize ======="<<currentVariation<<endl;
  //  cout<<"NAME of output before ======="<<newtree->GetName()<<endl;                                                                                                                                             
  //  currentSample = "physics_micro";//ttbar";
  if (currentSample == "physics_micro") isMC = false;
  cout<< "CURRENT  sample === "<< currentSample<<endl;
  
  std::string syst;
  if (isMC) {
  if (currentVariation == "NONE") syst="Nom"; else syst=currentVariation;
  for (int c=1;c<4;c++) {
    hSR.push_back( new TH1F(HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
    hCRWep.push_back(new TH1F(HistoNameMaker(currentSample,string("ONEelCR"+to_string(c)+"pos"),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
    hCRWen.push_back(new TH1F(HistoNameMaker(currentSample,string("ONEelCR"+to_string(c)+"neg"),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
    hCRWmp.push_back(new TH1F(HistoNameMaker(currentSample,string("ONEmuCR"+to_string(c)+"pos"),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
    hCRWmn.push_back(new TH1F(HistoNameMaker(currentSample,string("ONEmuCR"+to_string(c)+"neg"),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
    hCRZee.push_back(new TH1F(HistoNameMaker(currentSample,string("TWOelCR"+to_string(c)),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
    hCRZmm.push_back(new TH1F(HistoNameMaker(currentSample,string("TWOmuCR"+to_string(c)),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
    CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC), hSR[c-1]));  
    CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("ONEelCR"+to_string(c)+"pos"),to_string(c), syst, isMC), hCRWep[c-1]));
    CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("ONEelCR"+to_string(c)+"neg"),to_string(c), syst, isMC), hCRWen[c-1]));
    CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("ONEmuCR"+to_string(c)+"pos"),to_string(c), syst, isMC), hCRWmp[c-1]));
    CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("ONEmuCR"+to_string(c)+"neg"),to_string(c), syst, isMC), hCRWmn[c-1]));
    CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("TWOelCR"+to_string(c)),to_string(c), syst, isMC), hCRZee[c-1]));
    CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("TWOmuCR"+to_string(c)),to_string(c), syst, isMC), hCRZmm[c-1]));
  }} else {
    for (int c=1;c<4;c++) {
      hSR.push_back( new TH1F(HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
      hCRWep.push_back(new TH1F(HistoNameMaker(currentSample,string("ONEelCR"+to_string(c)+"pos"),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
      hCRWen.push_back(new TH1F(HistoNameMaker(currentSample,string("ONEelCR"+to_string(c)+"neg"),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
      hCRWmp.push_back(new TH1F(HistoNameMaker(currentSample,string("ONEmuCR"+to_string(c)+"pos"),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
      hCRWmn.push_back(new TH1F(HistoNameMaker(currentSample,string("ONEmuCR"+to_string(c)+"neg"),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
      hCRZee.push_back(new TH1F(HistoNameMaker(currentSample,string("TWOelCR"+to_string(c)),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
      hCRZmm.push_back(new TH1F(HistoNameMaker(currentSample,string("TWOmuCR"+to_string(c)),to_string(c), syst, isMC).c_str(), ";;", 1, 0.5, 1.5));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("SR"+to_string(c)),to_string(c), syst, isMC), hSR[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("ONEelCR"+to_string(c)+"pos"),to_string(c), syst, isMC), hCRWep[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("ONEelCR"+to_string(c)+"neg"),to_string(c), syst, isMC), hCRWen[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("ONEmuCR"+to_string(c)+"pos"),to_string(c), syst, isMC), hCRWmp[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("ONEmuCR"+to_string(c)+"neg"),to_string(c), syst, isMC), hCRWmn[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("TWOelCR"+to_string(c)),to_string(c), syst, isMC), hCRZee[c-1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+HistoNameMaker(currentSample,string("TWOmuCR"+to_string(c)),to_string(c), syst, isMC), hCRZmm[c-1]));
    }
  }
  return StatusCode::SUCCESS;
}
std::string HFInputAlg::HistoNameMaker(std::string currentSample, std::string currentCR, std::string bin, std::string syst, Bool_t isMC) {
  if (isMC) {
    if (bin == "") return "h"+currentSample+ "_"+syst+"_"+currentCR + "_obs_cuts";
    else return "h"+currentSample+ "_bin"+bin+syst+"_"+currentCR + "_obs_cuts";
  } else {
    return "h"+currentSample+ "_NONE_"+currentCR + "_obs_cuts";
  }
}

StatusCode HFInputAlg::finalize() {
  ATH_MSG_INFO ("Finalizing " << name() << "...");
  //
  ;
  //


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
  bool CRWmp = false;
  bool CRWmn = false;
  bool CRZee = false;
  bool CRZmm = false;
  
  m_tree->GetEntry(m_tree->GetReadEntry());
  if (!((jet_n ==2) & (j1_pt > 80e3) & (j2_pt > 50e3) & (jj_dphi < 1.8) & (jj_deta > 4.8) & ((j1_eta * j2_eta)<0) & (Inv_mass > 1e6) & (metjet_CST > 150e3))) return StatusCode::SUCCESS;

  if ((MET_trig == 1) & (met_et > 180e3) & ( deltaPhi_j1_met>1.0) & (deltaPhi_j2_met>1.0) & (el_n == 0) & (mu_n == 0)) SR = true;
  if ((elTrig == 1) & (lepmet_et > 180e3) & (deltaPhi_j1_lepmet>1.0) & (deltaPhi_j2_lepmet>1.0) & (el_n == 1) & (mu_n == 0) & (el1_charge > 0)) CRWep = true;
  if ((elTrig == 1) & (lepmet_et > 180e3) & (deltaPhi_j1_lepmet>1.0) & (deltaPhi_j2_lepmet>1.0) & (el_n == 1) & (mu_n == 0) & (el1_charge < 0)) CRWen = true;
  if ((muTrig == 1) & (lepmet_et > 180e3) & (deltaPhi_j1_lepmet>1.0) & (deltaPhi_j2_lepmet>1.0) & (el_n == 0) & (mu_n == 1) & (mu1_charge > 0)) CRWmp = true;
  if ((muTrig == 1) & (lepmet_et > 180e3) & (deltaPhi_j1_lepmet>1.0) & (deltaPhi_j2_lepmet>1.0) & (el_n == 0) & (mu_n == 1) & (mu1_charge < 0)) CRWmn = true;
  if ((elTrig == 1) & (lepmet_et > 180e3) & (deltaPhi_j1_lepmet>1.0) & (deltaPhi_j2_lepmet>1.0) & (el_n == 2) & (mu_n == 0) & (el1_charge*el2_charge < 0)) CRZee = true;
  if ((muTrig == 1) & (lepmet_et > 180e3) & (deltaPhi_j1_lepmet>1.0) & (deltaPhi_j2_lepmet>1.0) & (el_n == 0) & (mu_n == 2) & (mu1_charge*mu2_charge < 0)) CRZmm = true;

  if (SR){
    if (Inv_mass < 1.5e6) hSR[0]->Fill(1,w);
    else if (Inv_mass < 2e6) hSR[1]->Fill(1,w);
    else hSR[2]->Fill(1,w);
  }
  if (CRWep){
    if (Inv_mass < 1.5e6) hCRWep[0]->Fill(1,w);
    else if (Inv_mass < 2e6) hCRWep[1]->Fill(1,w);
    else hCRWep[2]->Fill(1,w);
  }
  if (CRWen){
    if (Inv_mass < 1.5e6) hCRWen[0]->Fill(1,w);
    else if (Inv_mass < 2e6) hCRWen[1]->Fill(1,w);
    else hCRWen[2]->Fill(1,w);
  }
  if (CRWmp){
    if (Inv_mass < 1.5e6) hCRWmp[0]->Fill(1,w);
    else if (Inv_mass < 2e6) hCRWmp[1]->Fill(1,w);
    else hCRWmp[2]->Fill(1,w);
  }
  if (CRWmn){
    if (Inv_mass < 1.5e6) hCRWmn[0]->Fill(1,w);
    else if (Inv_mass < 2e6) hCRWmn[1]->Fill(1,w);
    else hCRWmn[2]->Fill(1,w);
  }
  if (CRZee){
    if (Inv_mass < 1.5e6) hCRZee[0]->Fill(1,w);
    else if (Inv_mass < 2e6) hCRZee[1]->Fill(1,w);
    else hCRZee[2]->Fill(1,w);
  }
  if (CRZmm){
    if (Inv_mass < 1.5e6) hCRZmm[0]->Fill(1,w);
    else if (Inv_mass < 2e6) hCRZmm[1]->Fill(1,w);
    else hCRZmm[2]->Fill(1,w);
  }

  //HERE IS AN EXAMPLE
  //const xAOD::EventInfo* ei = 0;
  //CHECK( evtStore()->retrieve( ei , "EventInfo" ) );
  //ATH_MSG_INFO("eventNumber=" << ei->eventNumber() );
  //m_myHist->Fill( ei->averageInteractionsPerCrossing() ); //fill mu into histogram

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

  m_treeName = currentSample+"_"+currentVariation;
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  m_tree->SetBranchStatus("*",0);
  m_tree->SetBranchStatus("w", 1);
  m_tree->SetBranchStatus("pass_JetCleaning_tight", 1);
  m_tree->SetBranchStatus("jet_n", 1);
  m_tree->SetBranchStatus("j1_pt", 1);
  m_tree->SetBranchStatus("j2_pt", 1);
  m_tree->SetBranchStatus("deltaPhi_j1_met", 1);
  m_tree->SetBranchStatus("deltaPhi_j2_met", 1);
  m_tree->SetBranchStatus("jj_dphi", 1);
  m_tree->SetBranchStatus("j1_eta", 1);
  m_tree->SetBranchStatus("j2_eta", 1);
  m_tree->SetBranchStatus("jj_deta", 1);
  m_tree->SetBranchStatus("Inv_mass", 1);
  m_tree->SetBranchStatus("metjet_CST", 1);
  m_tree->SetBranchStatus("MET_trig", 1);
  m_tree->SetBranchStatus("met_et", 1);
  m_tree->SetBranchStatus("el_n", 1);
  m_tree->SetBranchStatus("mu_n", 1);
  m_tree->SetBranchStatus("el1_pt", 1);
  m_tree->SetBranchStatus("el2_pt", 1);
  m_tree->SetBranchStatus("mu1_pt", 1);
  m_tree->SetBranchStatus("mu2_pt", 1);
  m_tree->SetBranchStatus("el1_charge", 1);
  m_tree->SetBranchStatus("el2_charge", 1);
  m_tree->SetBranchStatus("mu1_charge", 1);
  m_tree->SetBranchStatus("mu2_charge", 1);
  m_tree->SetBranchStatus("elTrig", 1);
  m_tree->SetBranchStatus("lepmet_et", 1);
  m_tree->SetBranchStatus("met_significance", 1);
  m_tree->SetBranchStatus("muTrig", 1);
  m_tree->SetBranchStatus("deltaPhi_j1_lepmet", 1);
  m_tree->SetBranchStatus("deltaPhi_j2_lepmet", 1);
  m_tree->SetBranchStatus("Zll_m", 1);

  m_tree->SetBranchAddress("w", &w);
  m_tree->SetBranchAddress("pass_JetCleaning_tight", &pass_JetCleaning_tight);
  m_tree->SetBranchAddress("jet_n", &jet_n);
  m_tree->SetBranchAddress("j1_pt", &j1_pt);
  m_tree->SetBranchAddress("j2_pt", &j2_pt);
  m_tree->SetBranchAddress("deltaPhi_j1_met", &deltaPhi_j1_met);
  m_tree->SetBranchAddress("deltaPhi_j2_met", &deltaPhi_j2_met);
  m_tree->SetBranchAddress("jj_dphi", &jj_dphi);
  m_tree->SetBranchAddress("j1_eta", &j1_eta);
  m_tree->SetBranchAddress("j2_eta", &j2_eta);
  m_tree->SetBranchAddress("jj_deta", &jj_deta);
  m_tree->SetBranchAddress("Inv_mass", &Inv_mass);
  m_tree->SetBranchAddress("metjet_CST", &metjet_CST);
  m_tree->SetBranchAddress("MET_trig", &MET_trig);
  m_tree->SetBranchAddress("met_et", &met_et);
  m_tree->SetBranchAddress("el_n", &el_n);
  m_tree->SetBranchAddress("mu_n", &mu_n);
  m_tree->SetBranchAddress("el1_pt", &el1_pt);
  m_tree->SetBranchAddress("el2_pt", &el2_pt);
  m_tree->SetBranchAddress("mu1_pt", &mu1_pt);
  m_tree->SetBranchAddress("mu2_pt", &mu2_pt);
  m_tree->SetBranchAddress("el1_charge", &el1_charge);
  m_tree->SetBranchAddress("el2_charge", &el2_charge);
  m_tree->SetBranchAddress("mu1_charge", &mu1_charge);
  m_tree->SetBranchAddress("mu2_charge", &mu2_charge);
  m_tree->SetBranchAddress("elTrig", &elTrig);
  m_tree->SetBranchAddress("lepmet_et", &lepmet_et);
  m_tree->SetBranchAddress("met_significance", &met_significance);
  m_tree->SetBranchAddress("muTrig", &muTrig);
  m_tree->SetBranchAddress("deltaPhi_j1_lepmet", &deltaPhi_j1_lepmet);
  m_tree->SetBranchAddress("deltaPhi_j2_lepmet", &deltaPhi_j2_lepmet);
  m_tree->SetBranchAddress("Zll_m", &Zll_m);

  return StatusCode::SUCCESS;
}
