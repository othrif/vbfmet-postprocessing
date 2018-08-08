// VBFAnalysis includes
#include "VBFAnalysisAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
//#include "xAODEventInfo/EventInfo.h"
#include <vector>



VBFAnalysisAlg::VBFAnalysisAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){

  //declareProperty( "Property", m_nProperty = 0, "My Example Integer Property" ); //example property declaration

}


VBFAnalysisAlg::~VBFAnalysisAlg() {}


StatusCode VBFAnalysisAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");
  //
  //This is called once, before the start of the event loop
  //Retrieves of tools you have configured in the joboptions go here
  //
  
  bool isMC = true;
  currentVariation = "Nominal";
  cout<<"NAME of input tree in intialize ======="<<currentVariation<<endl;
  //  cout<<"NAME of output before ======="<<newtree->GetName()<<endl;


  currentSample = "ttbar";
  cout<< "CURRENT  sample === "<< currentSample<<endl;

  TString histoName="";
  histoName = "_" + currentSample;
  cout<<"currentVariation.substr(currentVariation.find_first_of(_)+1); "<<currentVariation.substr(currentVariation.find_first_of("_")+1)<<endl;
  //double crossSection;
  if(isMC){
    //SUSY::CrossSectionDB *my_XsecDB;
      std::string xSecFilePath = "dev/PMGTools/PMGxsecDB_mc15.txt";
      xSecFilePath = PathResolverFindCalibFile(xSecFilePath);
      my_XsecDB = new SUSY::CrossSectionDB(xSecFilePath);
  }//iSMC
  else  {
      if(runNumber >= 276262 && runNumber <= 284484) is2015 =true;
      else if(runNumber >= 296939 && runNumber <= 311481) is2016 =true;
      else throw std::invalid_argument("runNumber could not be identified with a dataset :o");
  }//Not MC 
  //Create new output TTree
  m_tree_out = new TTree(treeNameOut, treeTitleOut);
  m_tree_out->Branch("w",&w); 
  m_tree_out->Branch("trigger_met", &trigger_met);
  m_tree_out->Branch("trigger_lep", &trigger_lep);
  m_tree_out->Branch("passJetCleanTight", &passJetCleanTight);
  m_tree_out->Branch("n_jet",&n_jet);
  m_tree_out->Branch("n_el",&n_el);
  m_tree_out->Branch("n_mu",&n_mu);
  m_tree_out->Branch("jj_mass",&jj_mass);
  m_tree_out->Branch("jj_deta",&jj_deta);
  m_tree_out->Branch("jj_dphi",&jj_dphi);
  m_tree_out->Branch("met_tst_j1_dphi",&met_tst_j1_dphi);
  m_tree_out->Branch("met_tst_j2_dphi",&met_tst_j2_dphi);
  m_tree_out->Branch("met_tst_nolep_j1_dphi",&met_tst_nolep_j1_dphi);
  m_tree_out->Branch("met_tst_nolep_j2_dphi",&met_tst_nolep_j2_dphi);
  m_tree_out->Branch("met_tst_et",&met_tst_et);
  m_tree_out->Branch("met_tst_nolep_et",&met_tst_nolep_et);
  m_tree_out->Branch("mu_charge",&mu_charge);
  m_tree_out->Branch("mu_pt",&mu_pt);
  m_tree_out->Branch("el_charge",&el_charge);
  m_tree_out->Branch("el_pt",&el_pt);
  m_tree_out->Branch("jet_pt",&jet_pt);
  m_tree_out->Branch("jet_timing",&jet_timing);
  m_tree_out->Branch("mu_phi",&mu_phi);
  m_tree_out->Branch("el_phi",&el_phi);
  m_tree_out->Branch("jet_phi",&jet_phi);
  m_tree_out->Branch("jet_eta",&jet_eta);

  //Register the output TTree 
  CHECK(histSvc()->regTree("/MYSTREAM/nominal",m_tree_out));
  MapNgen(); //fill std::map with dsid->Ngen 
  ATH_MSG_DEBUG ("Done Initializing");
  return StatusCode::SUCCESS;
}

StatusCode VBFAnalysisAlg::finalize() {
  ATH_MSG_INFO ("Finalizing " << name() << "...");
  //
  //Things that happen once at the end of the event loop go here
  //


  return StatusCode::SUCCESS;
}

StatusCode VBFAnalysisAlg::MapNgen(){
  TFile *f = new TFile("f_out_total.root","READ");
  h_Gen = (TH1F*) f->Get("h_total");
  if(!h_Gen)ATH_MSG_WARNING("Number of events not found");

  for(int i=1; i<=h_Gen->GetNbinsX();i++){
    TString tmp = h_Gen->GetXaxis()->GetBinLabel(i);
    int dsid = tmp.Atoi(); 
    float N = h_Gen->GetBinContent(i); 
    Ngen[dsid]=N; 
   }
  
  return StatusCode::SUCCESS; 

}

StatusCode VBFAnalysisAlg::execute() {  
  ATH_MSG_DEBUG ("Executing " << name() << "...");
  //setFilterPassed(false); //optional: start with algorithm not passed
  m_tree->GetEntry(m_tree->GetReadEntry());

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

  crossSection = my_XsecDB->xsectTimesEff(runNumber);//xs in pb 
  if(Ngen[runNumber]>0)  weight = crossSection/Ngen[runNumber]; 
  else ATH_MSG_WARNING("Ngen " << Ngen[runNumber] << " dsid " << runNumber ); 

  if ((passGRL == 1) & (passPV == 1) & (passDetErr == 1) & (passJetCleanLoose == 1)) return StatusCode::SUCCESS;
  if (!(n_jet == 2)) return StatusCode::SUCCESS;
  if (!(n_jet == jet_pt->size())) ATH_MSG_WARNING("n_jet != jet_pt->size()! n_jet=" <<n_jet << " jet_pt->size(): " << jet_pt->size());
  if (!(n_jet == jet_eta->size())) ATH_MSG_WARNING("n_jet != jet_eta->size()! n_jet=" <<n_jet << " jet_eta->size(): " << jet_eta->size());
  if (!((jet_pt->at(0) > 80e3) & (jet_pt->at(1) > 50e3) & (jj_dphi < 1.8) & (jj_deta > 4.8) & ((jet_eta->at(0) * jet_eta->at(1))<0) & (jj_mass > 1e6))) return StatusCode::SUCCESS;
  if (trigger_HLT_xe100_mht_L1XE50 == 1 || trigger_HLT_xe110_mht_L1XE50 == 1 || trigger_HLT_xe90_mht_L1XE50 == 1) trigger_met = 1; else trigger_met = 0;
  if(n_el== 1) {
    met_significance = met_tst_et/1000/sqrt(sqrt(el_pt->at(0)*el_pt->at(0)*cos(el_phi->at(0))*cos(el_phi->at(0))+el_pt->at(0)*el_pt->at(0)*sin(el_phi->at(0))*sin(el_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*sin(jet_phi->at(0))*sin(jet_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*cos(jet_phi->at(0))*cos(jet_phi->at(0))+jet_pt->at(1)*jet_pt->at(1)*sin(jet_phi->at(1))*sin(jet_phi->at(1))+jet_pt->at(1)*jet_pt->at(1)*cos(jet_phi->at(1))*cos(jet_phi->at(1)))/1000);
  } else {
    met_significance = 0;
  }

  if ((trigger_met == 1) & (met_tst_et > 180e3) & (met_tst_j1_dphi>1.0) & (met_tst_j2_dphi>1.0) & (n_el == 0) & (n_mu == 0)) SR = true;
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0) & (el_charge->at(0) > 0) & (met_significance > 4.0)) CRWep = true;
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0) & (el_charge->at(0) < 0) & (met_significance > 4.0)) CRWen = true;
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0) & (el_charge->at(0) > 0) & (met_significance <= 4.0)) CRWepLowSig = true;
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0) & (el_charge->at(0) < 0) & (met_significance <= 4.0)) CRWenLowSig = true;
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1) & (mu_charge->at(0) > 0)) CRWmp = true;
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1) & (mu_charge->at(0) < 0)) CRWmn = true;
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 2) & (n_mu == 0) & (el_charge->at(0)*el_charge->at(1) < 0)) CRZee = true;
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 2) & (mu_charge->at(0)*mu_charge->at(1) < 0)) CRZmm = true;

  w = weight*mcEventWeight*puWeight*jvtSFWeight*elSFWeight*muSFWeight*elSFTrigWeight*muSFTrigWeight;

  // only save events that pass any of the regions
  if (!(SR || CRWep || CRWen || CRWepLowSig || CRWenLowSig || CRWmp || CRWmn || CRZee || CRZmm)) return StatusCode::SUCCESS;

  m_tree_out->Fill();

  //setFilterPassed(true); //if got here, assume that means algorithm passed
  return StatusCode::SUCCESS;
}

StatusCode VBFAnalysisAlg::beginInputFile() { 
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
  ATH_MSG_INFO("VBFAnalysisAlg::beginInputFile()");

  m_treeName = "MiniNtuple";
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  m_tree->SetBranchStatus("*",0);
  m_tree->SetBranchStatus("runNumber", 1);
  m_tree->SetBranchStatus("eventNumber", 1);
  m_tree->SetBranchStatus("averageIntPerXing", 1);
  m_tree->SetBranchStatus("mcEventWeight", 1);
  m_tree->SetBranchStatus("puWeight", 1);
  m_tree->SetBranchStatus("jvtSFWeight", 1);
  m_tree->SetBranchStatus("elSFWeight", 1);
  m_tree->SetBranchStatus("muSFWeight", 1);
  m_tree->SetBranchStatus("elSFTrigWeight", 1);
  m_tree->SetBranchStatus("muSFTrigWeight", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe100_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe110_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe90_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_lep", 1);
  m_tree->SetBranchStatus("passGRL", 1);
  m_tree->SetBranchStatus("passPV", 1);
  m_tree->SetBranchStatus("passDetErr", 1);
  m_tree->SetBranchStatus("passJetCleanLoose", 1);
  m_tree->SetBranchStatus("passJetCleanTight", 1);
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
  m_tree->SetBranchStatus("el_charge",1);
  m_tree->SetBranchStatus("el_pt",1);
  m_tree->SetBranchStatus("el_phi",1);
  m_tree->SetBranchStatus("jet_pt",1);
  m_tree->SetBranchStatus("jet_phi",1);
  m_tree->SetBranchStatus("jet_jvt",1);
  m_tree->SetBranchStatus("jet_timing",1);
  m_tree->SetBranchStatus("jet_passJvt",1);

  m_tree->SetBranchAddress("runNumber", &runNumber);
  m_tree->SetBranchAddress("mcEventWeight", &mcEventWeight);
  m_tree->SetBranchAddress("puWeight", &puWeight);
  m_tree->SetBranchAddress("jvtSFWeight", &jvtSFWeight);
  m_tree->SetBranchAddress("elSFWeight", &elSFWeight);
  m_tree->SetBranchAddress("muSFWeight", &muSFWeight);
  m_tree->SetBranchAddress("elSFTrigWeight", &elSFTrigWeight);
  m_tree->SetBranchAddress("muSFTrigWeight", &muSFTrigWeight);
  m_tree->SetBranchAddress("trigger_HLT_xe100_mht_L1XE50", &trigger_HLT_xe100_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_HLT_xe110_mht_L1XE50", &trigger_HLT_xe110_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_HLT_xe90_mht_L1XE50", &trigger_HLT_xe90_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_lep", &trigger_lep);
  m_tree->SetBranchAddress("passGRL", &passGRL);
  m_tree->SetBranchAddress("passPV", &passPV);
  m_tree->SetBranchAddress("passDetErr", &passDetErr);
  m_tree->SetBranchAddress("passJetCleanLoose", &passJetCleanLoose);
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

  m_tree->SetBranchAddress("mu_charge",&mu_charge);//, &b_mu_charge);
  m_tree->SetBranchAddress("mu_pt",&mu_pt);//, &b_mu_pt);
  m_tree->SetBranchAddress("mu_phi",&mu_phi);//, &b_mu_phi);
  m_tree->SetBranchAddress("el_charge",&el_charge);
  m_tree->SetBranchAddress("el_pt",&el_pt);
  m_tree->SetBranchAddress("el_phi",&el_phi);
  m_tree->SetBranchAddress("jet_pt",&jet_pt);
  m_tree->SetBranchAddress("jet_phi",&jet_phi);
  m_tree->SetBranchAddress("jet_eta",&jet_eta);
  m_tree->SetBranchAddress("jet_jvt",&jet_jvt);
  m_tree->SetBranchAddress("jet_timing",&jet_timing);
  m_tree->SetBranchAddress("jet_passJvt",&jet_passJvt);

  return StatusCode::SUCCESS;
}

