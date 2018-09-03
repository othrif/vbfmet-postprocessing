// VBFAnalysis includes
#include "VBFAnalysisAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
//#include "xAODEventInfo/EventInfo.h"
#include <vector>



VBFAnalysisAlg::VBFAnalysisAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty( "currentSample", m_currentSample = "W_strong", "current sample");
  declareProperty( "runNumberInput", m_runNumberInput, "runNumber read from file name");
  declareProperty( "isMC", m_isMC = true, "true if sample is MC" );
  declareProperty( "currentVariation", m_currentVariation = "Nominal", "current sytematics of the tree" );
  declareProperty( "normFile", m_normFile = "current.root", "path to a file with the number of events processed" );
  declareProperty( "mcCampaign", m_mcCampaign = "mc16a", "mcCampaign of the mc sample. only read if isMC is true" );
}


VBFAnalysisAlg::~VBFAnalysisAlg() {}


StatusCode VBFAnalysisAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");
  //
  //This is called once, before the start of the event loop
  //Retrieves of tools you have configured in the joboptions go here
  //
  
  cout<<"NAME of input tree in intialize ======="<<m_currentVariation<<endl;
  cout << "isMC: " << m_isMC << endl;
  //  cout<<"NAME of output before ======="<<newtree->GetName()<<endl;
  cout<< "CURRENT  sample === "<< m_currentSample<<endl;

  //double crossSection;
  if(m_isMC){
    //SUSY::CrossSectionDB *my_XsecDB;
    std::string xSecFilePath = "dev/PMGTools/PMGxsecDB_mc15.txt";
    xSecFilePath = PathResolverFindCalibFile(xSecFilePath);
    my_XsecDB = new SUSY::CrossSectionDB(xSecFilePath);
    // if( (runNumber == 308567 || runNumber == 308276 ) ){
    //   if(truthHiggs_pt->size() > 0) w_VBFhiggs =  -0.000342 * truthHiggs_pt->at(0)/GeV - 0.0708;
    // }else {
    //   w_VBFhiggs =1.;
    // }
  }
  //    if(runNumber >= 276262 && runNumber <= 284484) is2015 =true;
  //    else if(runNumber >= 296939 && runNumber <= 311481) is2016 =true;
  //    else throw std::invalid_argument("runNumber could not be identified with a dataset :o");

  //Create new output TTree
  treeTitleOut = m_currentSample+m_currentVariation;
  treeNameOut = m_currentSample+m_currentVariation;
  m_tree_out = new TTree(treeNameOut.c_str(), treeTitleOut.c_str());
  m_tree_out->Branch("w",&w); 
  m_tree_out->Branch("runNumber",&runNumber);
  m_tree_out->Branch("eventNumber",&eventNumber);
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
  m_tree_out->Branch("met_tst_phi",&met_tst_phi);
  m_tree_out->Branch("met_tst_nolep_phi",&met_tst_nolep_phi);
  m_tree_out->Branch("mu_charge",&mu_charge);
  m_tree_out->Branch("mu_pt",&mu_pt);
  m_tree_out->Branch("el_charge",&el_charge);
  m_tree_out->Branch("el_pt",&el_pt);
  m_tree_out->Branch("jet_pt",&jet_pt);
  m_tree_out->Branch("jet_timing",&jet_timing);
  m_tree_out->Branch("mu_phi",&mu_phi);
  m_tree_out->Branch("el_phi",&el_phi);
  m_tree_out->Branch("mu_eta",&mu_eta);    
  m_tree_out->Branch("el_eta",&el_eta); 
  m_tree_out->Branch("jet_phi",&jet_phi);
  m_tree_out->Branch("jet_eta",&jet_eta);
  m_tree_out->Branch("met_significance",&met_significance);
  
  //Register the output TTree 
  CHECK(histSvc()->regTree("/MYSTREAM/"+treeTitleOut,m_tree_out));
  MapNgen(); //fill std::map with dsid->Ngen 
  ATH_MSG_DEBUG ("Done Initializing");
  
  std::ostringstream runNumberss;
  runNumberss << runNumber;
  outputName = m_currentSample+m_currentVariation+runNumberss.str();
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
  TFile *f = TFile::Open(m_normFile.c_str(),"READ");
  if(!f or f->IsZombie()) std::cout << "ERROR normFile. Could not open " << m_normFile << std::endl;
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

  if (runNumber != m_runNumberInput) ATH_MSG_ERROR("VBFAnaysisAlg::execute: runNumber " << runNumber << " != m_runNumberInput " << m_runNumberInput);

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

  if (m_isMC){
    crossSection = my_XsecDB->xsectTimesEff(runNumber);//xs in pb 
    if(Ngen[runNumber]>0)  weight = crossSection/Ngen[runNumber]; 
    else ATH_MSG_WARNING("Ngen " << Ngen[runNumber] << " dsid " << runNumber ); 
    ATH_MSG_DEBUG("VBFAnalysisAlg: xs: "<< crossSection << " nevent: " << Ngen[runNumber] );
  } else {
    weight = 1;
  }

  if (!((passGRL == 1) & (passPV == 1) & (passDetErr == 1) & (passJetCleanLoose == 1))) return StatusCode::SUCCESS;
  ATH_MSG_DEBUG ("Pass GRL, PV, DetErr, JetCleanLoose");
  if (!(n_jet == 2)) return StatusCode::SUCCESS;
  ATH_MSG_DEBUG ("n_jet = 2!");
  if (!(n_jet == jet_pt->size())) ATH_MSG_WARNING("n_jet != jet_pt->size()! n_jet: " <<n_jet << " jet_pt->size(): " << jet_pt->size());
  if (!(n_jet == jet_eta->size())) ATH_MSG_WARNING("n_jet != jet_eta->size()! n_jet: " <<n_jet << " jet_eta->size(): " << jet_eta->size());
  if (!((jet_pt->at(0) > 80e3) & (jet_pt->at(1) > 50e3) & (jj_dphi < 1.8) & (jj_deta > 4.8) & ((jet_eta->at(0) * jet_eta->at(1))<0) & (jj_mass > 1e6))) return StatusCode::SUCCESS;
  ATH_MSG_DEBUG ("Pass VBF cuts!");
  if (trigger_HLT_xe100_mht_L1XE50 == 1 || trigger_HLT_xe110_mht_L1XE50 == 1 || trigger_HLT_xe90_mht_L1XE50 == 1) trigger_met = 1; else trigger_met = 0;
  ATH_MSG_DEBUG ("Assign trigger_met value");
  if(n_el== 1) {
    met_significance = met_tst_et/1000/sqrt(sqrt(el_pt->at(0)*el_pt->at(0)*cos(el_phi->at(0))*cos(el_phi->at(0))+el_pt->at(0)*el_pt->at(0)*sin(el_phi->at(0))*sin(el_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*sin(jet_phi->at(0))*sin(jet_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*cos(jet_phi->at(0))*cos(jet_phi->at(0))+jet_pt->at(1)*jet_pt->at(1)*sin(jet_phi->at(1))*sin(jet_phi->at(1))+jet_pt->at(1)*jet_pt->at(1)*cos(jet_phi->at(1))*cos(jet_phi->at(1)))/1000);
  } else {
    met_significance = 0;
  }
  ATH_MSG_DEBUG ("met_significance calculated");
  
  if ((trigger_met == 1) & (met_tst_et > 180e3) & (met_tst_j1_dphi>1.0) & (met_tst_j2_dphi>1.0) & (n_el == 0) & (n_mu == 0)) SR = true;
  if (SR) ATH_MSG_DEBUG ("It's SR!"); else ATH_MSG_DEBUG ("It's NOT SR");
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance > 4.0)) CRWep = true;}
  if (CRWep) ATH_MSG_DEBUG ("It's CRWep!"); else ATH_MSG_DEBUG ("It's NOT CRWep");
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance > 4.0)) CRWen = true;}
  if (CRWen) ATH_MSG_DEBUG ("It's CRWen!"); else ATH_MSG_DEBUG ("It's NOT CRWen");
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance <= 4.0)) CRWepLowSig = true;}
  if (CRWepLowSig) ATH_MSG_DEBUG ("It's CRWepLowSig!"); else ATH_MSG_DEBUG ("It's NOT CRWepLowSig");
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance <= 4.0)) CRWenLowSig = true;}
  if (CRWenLowSig) ATH_MSG_DEBUG ("It's CRWenLowSig!"); else ATH_MSG_DEBUG ("It's NOT CRWenLowSig");
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) > 0)) CRWmp = true;}
  if (CRWmp) ATH_MSG_DEBUG ("It's CRWmp!"); else ATH_MSG_DEBUG ("It's NOT CRWmp");
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) < 0)) CRWmn = true;}
  if (CRWmn) ATH_MSG_DEBUG ("It's CRWmn!"); else ATH_MSG_DEBUG ("It's NOT CRWmn");
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 2) & (n_mu == 0)){ if ((el_charge->at(0)*el_charge->at(1) < 0)) CRZee = true;}
  if (CRZee) ATH_MSG_DEBUG ("It's CRZee!"); else ATH_MSG_DEBUG ("It's NOT CRZee");
  if ((trigger_lep == 1) & (met_tst_nolep_et > 180e3) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 2)){ if ((mu_charge->at(0)*mu_charge->at(1) < 0)) CRZmm = true;}
  if (CRZmm) ATH_MSG_DEBUG ("It's CRZmm!"); else ATH_MSG_DEBUG ("It's NOT CRZmm");

  w = weight*mcEventWeight*puWeight*jvtSFWeight*elSFWeight*muSFWeight*elSFTrigWeight*muSFTrigWeight;
  ATH_MSG_DEBUG("VBFAnalysisAlg: weight: " << weight << " mcEventWeight: " << mcEventWeight << " puWeight: " << puWeight << " jvtSFWeight: " << jvtSFWeight << " elSFWeight: " << elSFWeight << " muSFWeight: " << muSFWeight << " elSFTrigWeight: " << elSFTrigWeight << " muSFTrigWeight: " << muSFTrigWeight);
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
  m_tree->SetBranchStatus("met_tst_phi",1);
  m_tree->SetBranchStatus("met_tst_nolep_phi",1);
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
  m_tree->SetBranchStatus("jet_jvt",1);
  m_tree->SetBranchStatus("jet_timing",1);
  m_tree->SetBranchStatus("jet_passJvt",1);

  m_tree->SetBranchAddress("runNumber", &runNumber);
  m_tree->SetBranchAddress("eventNumber", &eventNumber);
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
  m_tree->SetBranchAddress("met_tst_phi",&met_tst_phi);
  m_tree->SetBranchAddress("met_tst_nolep_phi",&met_tst_nolep_phi);
  m_tree->SetBranchAddress("mu_charge",&mu_charge);//, &b_mu_charge);
  m_tree->SetBranchAddress("mu_pt",&mu_pt);//, &b_mu_pt);
  m_tree->SetBranchAddress("mu_phi",&mu_phi);//, &b_mu_phi);
  m_tree->SetBranchAddress("el_charge",&el_charge);
  m_tree->SetBranchAddress("el_pt",&el_pt);
  m_tree->SetBranchAddress("el_phi",&el_phi);
  m_tree->SetBranchAddress("mu_eta",&mu_eta);
  m_tree->SetBranchAddress("el_eta",&el_eta);
  m_tree->SetBranchAddress("jet_pt",&jet_pt);
  m_tree->SetBranchAddress("jet_phi",&jet_phi);
  m_tree->SetBranchAddress("jet_eta",&jet_eta);
  m_tree->SetBranchAddress("jet_jvt",&jet_jvt);
  m_tree->SetBranchAddress("jet_timing",&jet_timing);
  m_tree->SetBranchAddress("jet_passJvt",&jet_passJvt);

  return StatusCode::SUCCESS;
}

