// VBFAnalysis includes
#include "VBFAnalysisAlg.h"
#include "SignalSystHelper.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
#include "TLorentzVector.h"
#include <math.h>       /* exp */


VBFAnalysisAlg::VBFAnalysisAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ), nParton(-1),
										      fjvtSFWeight(1.0), fjvtSFTighterWeight(1.0), phSFWeight(1.0){
  declareProperty( "currentSample", m_currentSample = "W_strong", "current sample");
  declareProperty( "runNumberInput", m_runNumberInput, "runNumber read from file name");
  declareProperty( "isMC", m_isMC = true, "true if sample is MC" );
  declareProperty( "LooseSkim", m_LooseSkim = true, "true if loose skimming is requested" );
  declareProperty( "ExtraVars", m_extraVars = true, "true if extra variables should be output" );
  declareProperty( "QGTagger", m_QGTagger = false, "true if extra variables should be output for QGTagger" );
  declareProperty( "METTrigPassThru", m_METTrigPassThru = false, "true if require no met triggers" );
  declareProperty( "ContLep", m_contLep = false, "true if container lepton variables should be output" );
  declareProperty( "currentVariation", m_currentVariation = "Nominal", "current sytematics of the tree" );
  declareProperty( "normFile", m_normFile = "current.root", "path to a file with the number of events processed" );
  declareProperty( "mcCampaign", m_mcCampaign = "mc16a", "mcCampaign of the mc sample. only read if isMC is true" );
  declareProperty( "UseExtMC", m_UseExtMC = false, "Use extended MC samples mc16a");
  declareProperty( "UseExtMGVjet", m_UseExtMGVjet = false, "Use extended LO MG extension");
  declareProperty( "theoVariation", m_theoVariation = false, "Do theory systematic variations");
  declareProperty( "oneTrigMuon", m_oneTrigMuon = false, "Trigger muon SF set to 1");
}


VBFAnalysisAlg::~VBFAnalysisAlg() {}

const std::string regions[] = {"Incl","SR","CRWe","CRWm","CRW","CRZee", "CRZmm","CRZ"};
const std::string variations[] = {"fac_up","fac_down","renorm_up","renorm_down","both_up","both_down"};

StatusCode VBFAnalysisAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");
  //
  //This is called once, before the start of the event loop
  //Retrieves of tools you have configured in the joboptions go here
  //

  cout<<"NAME of input tree in intialize ======="<<m_currentVariation<<endl;
  cout << "isMC: " << m_isMC << endl;
  cout<< "CURRENT  sample === "<< m_currentSample<<endl;

  // initialize jet container
  m_newJets = new xAOD::JetContainer();
  m_newJetsAux = new xAOD::AuxContainerBase();
  m_newJets->setStore( m_newJetsAux ); //< Connect the two  
  xAOD::Jet* new_jet = new xAOD::Jet();
  m_newJets->push_back(new_jet);
  
  if(m_isMC){
    std::string xSecFilePath = "dev/PMGTools/PMGxsecDB_mc15.txt";
    xSecFilePath = "VBFAnalysis/PMGxsecDB_mc16.txt"; // run from local file
    xSecFilePath = PathResolverFindCalibFile(xSecFilePath);
    std::cout << "Cross section using local file: " << xSecFilePath << std::endl;
    my_XsecDB = new SUSY::CrossSectionDB(xSecFilePath, false, false, true);

    // signal systematics
    my_signalSystHelper.initialize();

    // qg tagging
    m_qgVars.clear();
    m_systSet.clear();
    if(m_QGTagger){
      m_qgVars.push_back("JET_QG_Nominal");
      
      asg::AnaToolHandle<CP::IJetQGTagger> my_handleNom;
      my_handleNom.setTypeAndName("CP::JetQGTagger/JetQGTagger_VBF");
      ANA_CHECK(my_handleNom.setProperty("NTrackCut", 5));
      ANA_CHECK(my_handleNom.setProperty("UseJetVars", 1));
      ANA_CHECK(my_handleNom.setProperty("cuttype", "threshold"));
      ANA_CHECK(my_handleNom.retrieve());
      m_jetQGTool[m_qgVars.at(0)]=my_handleNom;
      m_systSet["JET_QG_Nominal"] = CP::SystematicSet("");
      if(m_currentVariation=="Nominal"){
	// loading the systematics
	const CP::SystematicRegistry& registry = CP::SystematicRegistry::getInstance();
	const CP::SystematicSet& recommendedSystematics = registry.recommendedSystematics();
	// add all recommended systematics
	for (const auto& systSet : CP::make_systematics_vector(recommendedSystematics)) {
	  TString nameRunThisSyst="";
	  for (const auto& sys : systSet) {
	    std::cout << "syst: " << sys.name() << " base: " << sys.basename() << std::endl;
	    // select only QG tagging
	    if(sys.basename().find("JET_QG_")!=std::string::npos){
	      std::cout << "QG syst Loaded: " << sys.name() << std::endl;
	      nameRunThisSyst=sys.name();
	    }
	  }
	  if(nameRunThisSyst!=""){
	    m_qgVars.push_back(nameRunThisSyst);
	    m_systSet[nameRunThisSyst] = CP::SystematicSet(std::string(nameRunThisSyst.Data()));
	  }
	}
      }// end qg systematics setup
    }// end qg setup
  }// end nominal check

  xeSFTrigWeight=1.0;
  xeSFTrigWeight__1up=1.0;
  xeSFTrigWeight__1down=1.0;
  xeSFTrigWeight_nomu=1.0;
  xeSFTrigWeight_nomu__1up=1.0;
  xeSFTrigWeight_nomu__1down=1.0;

  j3_centrality = new std::vector<float>(0);
  j3_dRj1 = new std::vector<float>(0);
  j3_dRj2 = new std::vector<float>(0);
  j3_minDR = new std::vector<float>(0);
  j3_mjclosest = new std::vector<float>(0);
  j3_min_mj = new std::vector<float>(0);
  j3_min_mj_over_mjj = new std::vector<float>(0);
  mj34=-9999.0;
  max_j_eta=-9999.0;
  // add container leptons
  contmu_pt= new std::vector<float>(0);
  contmu_eta= new std::vector<float>(0);
  contmu_phi= new std::vector<float>(0);
  contel_pt= new std::vector<float>(0);
  contel_eta= new std::vector<float>(0);
  contel_phi= new std::vector<float>(0);

  basemu_pt= new std::vector<float>(0);
  basemu_eta= new std::vector<float>(0);
  basemu_phi= new std::vector<float>(0);
  basemu_charge= new std::vector<int>(0);
  basemu_z0= new std::vector<float>(0);
  basemu_d0sig= new std::vector<float>(0);
  basemu_ptvarcone20= new std::vector<float>(0);
  basemu_ptvarcone30= new std::vector<float>(0);
  basemu_topoetcone20= new std::vector<float>(0);
  basemu_topoetcone30= new std::vector<float>(0);
  basemu_type= new std::vector<int>(0);
  basemu_truthType= new std::vector<int>(0);
  basemu_truthOrigin= new std::vector<int>(0);

  baseel_pt= new std::vector<float>(0);
  baseel_eta= new std::vector<float>(0);
  baseel_phi= new std::vector<float>(0);
  baseel_charge= new std::vector<int>(0);
  baseel_z0= new std::vector<float>(0);
  baseel_d0sig= new std::vector<float>(0);
  baseel_ptvarcone20= new std::vector<float>(0);
  baseel_ptvarcone30= new std::vector<float>(0);
  baseel_topoetcone20= new std::vector<float>(0);
  baseel_topoetcone30= new std::vector<float>(0);
  baseel_truthType= new std::vector<int>(0);
  baseel_truthOrigin= new std::vector<int>(0);

  mu_charge= new std::vector<float>(0);
  mu_pt= new std::vector<float>(0);
  mu_phi= new std::vector<float>(0);
  el_charge= new std::vector<float>(0);
  el_pt= new std::vector<float>(0);
  el_phi= new std::vector<float>(0);
  mu_eta= new std::vector<float>(0);
  el_eta= new std::vector<float>(0);
  jet_pt= new std::vector<float>(0);
  jet_phi= new std::vector<float>(0);
  jet_eta= new std::vector<float>(0);
  jet_m= new std::vector<float>(0);
  jet_jvt= new std::vector<float>(0);
  jet_fjvt= new std::vector<float>(0);
  jet_timing= new std::vector<float>(0);
  jet_passJvt= new std::vector<int>(0);
  jet_PartonTruthLabelID = new std::vector<int>(0);
  jet_ConeTruthLabelID = new std::vector<int>(0);
  jet_NTracks = new std::vector<std::vector<unsigned short> >(0);
  jet_NTracks_PV = new std::vector<unsigned short>(0);
  jet_SumPtTracks = new std::vector<std::vector<float> >(0);
  jet_SumPtTracks_PV = new std::vector<float>(0);
  jet_TrackWidth = new std::vector<float>(0);
  jet_TracksC1 = new std::vector<float>(0);
  jet_truthjet_pt = new std::vector<float>(0);
  jet_truthjet_eta = new std::vector<float>(0);
  jet_truthjet_nCharged = new std::vector<int>(0);
  jet_HECFrac = new std::vector<float>(0);
  jet_EMFrac = new std::vector<float>(0);
  jet_fch = new std::vector<float>(0);
  jet_btag_weight = new std::vector<float>(0);

  truth_jet_pt= new std::vector<float>(0);
  truth_jet_eta= new std::vector<float>(0);
  truth_jet_phi= new std::vector<float>(0);
  truth_jet_m= new std::vector<float>(0);

  truth_tau_pt= new std::vector<float>(0);
  truth_tau_eta= new std::vector<float>(0);
  truth_tau_phi= new std::vector<float>(0);
  truth_tau_status= new std::vector<int>(0);
  truth_mu_pt= new std::vector<float>(0);
  truth_mu_eta= new std::vector<float>(0);
  truth_mu_phi= new std::vector<float>(0);
  truth_ph_pt= new std::vector<float>(0);
  truth_ph_eta= new std::vector<float>(0);
  truth_ph_phi= new std::vector<float>(0);
  truth_el_pt= new std::vector<float>(0);
  truth_el_eta= new std::vector<float>(0);
  truth_el_phi= new std::vector<float>(0);
  truth_el_status= new std::vector<int>(0);

  outtau_pt = new std::vector<float>(0);
  outtau_phi = new std::vector<float>(0);
  outtau_eta = new std::vector<float>(0);

  ph_pt = new std::vector<float>(0);
  ph_phi = new std::vector<float>(0);
  ph_eta = new std::vector<float>(0);
  tau_pt = new std::vector<float>(0);
  tau_phi = new std::vector<float>(0);
  tau_eta = new std::vector<float>(0);

  mcEventWeights = new std::vector<float>(0);

  //Create new output TTree
  treeTitleOut = m_currentSample+m_currentVariation;
  treeNameOut = m_currentSample+m_currentVariation;
  m_tree_out = new TTree(treeNameOut.c_str(), treeTitleOut.c_str());
  m_tree_out->Branch("w",&w);
  //m_tree_out->Branch("nloEWKWeight",&nloEWKWeight);
  m_tree_out->Branch("puSyst2018Weight",&puSyst2018Weight);
  m_tree_out->Branch("xeSFTrigWeight",&xeSFTrigWeight);
  m_tree_out->Branch("xeSFTrigWeight_nomu",&xeSFTrigWeight_nomu);
  if(m_currentVariation=="Nominal"){ // only write for the nominal
    m_tree_out->Branch("xeSFTrigWeight__1up",&xeSFTrigWeight__1up);
    m_tree_out->Branch("xeSFTrigWeight__1down",&xeSFTrigWeight__1down);
    m_tree_out->Branch("xeSFTrigWeight_nomu__1up",&xeSFTrigWeight_nomu__1up);
    m_tree_out->Branch("xeSFTrigWeight_nomu__1down",&xeSFTrigWeight_nomu__1down);
    if(m_theoVariation) m_tree_out->Branch("mcEventWeights",&mcEventWeights);
  }
  if(m_currentVariation=="Nominal") m_tree_out->Branch("eleANTISF",&eleANTISF);
  m_tree_out->Branch("runNumber",&runNumber);
  m_tree_out->Branch("randomRunNumber",&randomRunNumber);
  m_tree_out->Branch("eventNumber",&eventNumber);
  m_tree_out->Branch("trigger_met", &trigger_met);
  m_tree_out->Branch("trigger_met_encodedv2", &trigger_met_encodedv2);
  m_tree_out->Branch("l1_met_trig_encoded", &l1_met_trig_encoded);
  if(m_extraVars) m_tree_out->Branch("trigger_met_encoded", &trigger_met_encoded);
  m_tree_out->Branch("passBatman", &passBatman );
  m_tree_out->Branch("passVjetsFilter", &passVjetsFilter );
  m_tree_out->Branch("passVjetsFilterTauEl", &passVjetsFilterTauEl );
  m_tree_out->Branch("passVjetsPTV", &passVjetsPTV );
  m_tree_out->Branch("MGVTruthPt", &MGVTruthPt);
  m_tree_out->Branch("in_vy_overlap", &in_vy_overlap);
  m_tree_out->Branch("trigger_lep", &trigger_lep);
  m_tree_out->Branch("lep_trig_match", &lep_trig_match);
  m_tree_out->Branch("passJetCleanTight", &passJetCleanTight);
  m_tree_out->Branch("averageIntPerXing", &averageIntPerXing);
  m_tree_out->Branch("n_vx", &n_vx);
  m_tree_out->Branch("n_jet",&n_jet);
  m_tree_out->Branch("n_el",&n_el);
  m_tree_out->Branch("n_mu",&n_mu);
  m_tree_out->Branch("n_el_w",&n_el_w);
  m_tree_out->Branch("n_mu_w",&n_mu_w);
  m_tree_out->Branch("n_ph",&n_ph);
  m_tree_out->Branch("n_tau",&n_tau);
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
  m_tree_out->Branch("met_cst_jet",&met_cst_jet);
  m_tree_out->Branch("met_soft_tst_et",        &met_soft_tst_et);
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
  m_tree_out->Branch("jet_m",&jet_m);
  m_tree_out->Branch("jet_jvt",&jet_jvt);
  m_tree_out->Branch("met_significance",&met_significance);
  m_tree_out->Branch("max_mj_over_mjj",&max_mj_over_mjj);
  m_tree_out->Branch("maxCentrality",&maxCentrality);
  m_tree_out->Branch("n_baseel",&n_baseel);
  m_tree_out->Branch("n_basemu",&n_basemu);
  m_tree_out->Branch("n_el_baseline_noOR",&n_baseel_noOR);
  m_tree_out->Branch("n_mu_baseline_noOR",&n_basemu_noOR);
  m_tree_out->Branch("n_el_baseline_iso",&n_baseel_iso);
  m_tree_out->Branch("n_mu_baseline_iso",&n_basemu_iso);

  m_tree_out->Branch("n_bjet",&n_bjet);

  if(m_contLep){
    m_tree_out->Branch("contmu_pt",           &contmu_pt);
    m_tree_out->Branch("contmu_eta",          &contmu_eta);
    m_tree_out->Branch("contmu_phi",          &contmu_phi);
    m_tree_out->Branch("contel_pt",           &contel_pt);
    m_tree_out->Branch("contel_eta",          &contel_eta);
    m_tree_out->Branch("contel_phi",          &contel_phi);
  }

  if(m_extraVars){

    if(m_currentVariation=="Nominal"){

      m_tree_out->Branch("jet_btag_weight",&jet_btag_weight);
      m_tree_out->Branch("j3_centrality",&j3_centrality);
      m_tree_out->Branch("j3_min_mj_over_mjj",&j3_min_mj_over_mjj);
      m_tree_out->Branch("j3_dRj1",&j3_dRj1);
      m_tree_out->Branch("j3_dRj2",&j3_dRj2);
      m_tree_out->Branch("j3_minDR",&j3_minDR);
      m_tree_out->Branch("j3_mjclosest",&j3_mjclosest);
      m_tree_out->Branch("j3_min_mj",&j3_min_mj);
      m_tree_out->Branch("mj34",&mj34);
      m_tree_out->Branch("max_j_eta",&max_j_eta);

      m_tree_out->Branch("lb",&lumiBlock);
      m_tree_out->Branch("bcid",&bcid);
      m_tree_out->Branch("BCIDDistanceFromFront",&BCIDDistanceFromFront);

      if(m_QGTagger){
	m_tree_out->Branch("jet_NTracks",&jet_NTracks_PV);
	m_tree_out->Branch("jet_SumPtTracks",&jet_SumPtTracks_PV);
	m_tree_out->Branch("jet_TrackWidth",&jet_TrackWidth);
	m_tree_out->Branch("jet_TracksC1",&jet_TracksC1);
	m_tree_out->Branch("jet_HECFrac",&jet_HECFrac);
	m_tree_out->Branch("jet_EMFrac",&jet_EMFrac);
	m_tree_out->Branch("jet_fch",&jet_fch);
      }
      if(m_isMC && m_currentVariation=="Nominal") m_tree_out->Branch("jet_PartonTruthLabelID",&jet_PartonTruthLabelID);
      if(m_isMC && m_currentVariation=="Nominal") m_tree_out->Branch("jet_ConeTruthLabelID",&jet_ConeTruthLabelID);
    }else{
      if(m_QGTagger){
      	m_tree_out->Branch("jet_NTracks",&jet_NTracks_PV);
      }
    }

    m_tree_out->Branch("jet_fjvt",&jet_fjvt);

    m_tree_out->Branch("basemu_pt",           &basemu_pt);
    m_tree_out->Branch("basemu_eta",          &basemu_eta);
    m_tree_out->Branch("basemu_phi",          &basemu_phi);
    m_tree_out->Branch("basemu_charge",          &basemu_charge);
    m_tree_out->Branch("basemu_ptvarcone30",  &basemu_ptvarcone30);
    m_tree_out->Branch("baseel_pt",           &baseel_pt);
    m_tree_out->Branch("baseel_eta",          &baseel_eta);
    m_tree_out->Branch("baseel_phi",          &baseel_phi);
    m_tree_out->Branch("baseel_charge",          &baseel_charge);
    m_tree_out->Branch("baseel_ptvarcone20",  &baseel_ptvarcone20);
    if(m_currentVariation=="Nominal"){
      m_tree_out->Branch("basemu_ptvarcone20",  &basemu_ptvarcone20);
      m_tree_out->Branch("basemu_z0",           &basemu_z0);
      m_tree_out->Branch("basemu_d0sig",           &basemu_d0sig);
      m_tree_out->Branch("basemu_topoetcone20",  &basemu_topoetcone20);
      m_tree_out->Branch("basemu_topoetcone30",  &basemu_topoetcone30);
      m_tree_out->Branch("basemu_type",         &basemu_type);
      if(m_isMC) m_tree_out->Branch("basemu_truthOrigin",  &basemu_truthOrigin);
      if(m_isMC) m_tree_out->Branch("basemu_truthType",    &basemu_truthType);
      m_tree_out->Branch("baseel_z0",           &baseel_z0);
      m_tree_out->Branch("baseel_d0sig",        &baseel_d0sig);
      m_tree_out->Branch("baseel_topoetcone20",  &baseel_topoetcone20);
      if(m_isMC) m_tree_out->Branch("baseel_truthOrigin",  &baseel_truthOrigin);
      if(m_isMC) m_tree_out->Branch("baseel_truthType",    &baseel_truthType);
    }
    m_tree_out->Branch("ph_pt", &ph_pt);
    m_tree_out->Branch("ph_phi",&ph_phi);
    m_tree_out->Branch("ph_eta",&ph_eta);
    if(m_currentVariation=="Nominal"){
      m_tree_out->Branch("tau_pt",&outtau_pt);
      m_tree_out->Branch("tau_phi",&outtau_phi);
      m_tree_out->Branch("tau_eta",&outtau_eta);
      m_tree_out->Branch("met_soft_tst_phi",       &met_soft_tst_phi);
      m_tree_out->Branch("met_soft_tst_sumet",     &met_soft_tst_sumet);
    }else{
      tau_pt=0; tau_phi=0; tau_eta=0; 
    }
    // Tenacious MET
    m_tree_out->Branch("met_tenacious_tst_et",   &met_tenacious_tst_et);
    m_tree_out->Branch("met_tenacious_tst_phi",  &met_tenacious_tst_phi);
    m_tree_out->Branch("met_tenacious_tst_nolep_et",&met_tenacious_tst_nolep_et);
    m_tree_out->Branch("met_tenacious_tst_nolep_phi",&met_tenacious_tst_nolep_phi);

    if(m_currentVariation=="Nominal"){
      m_tree_out->Branch("met_tenacious_tst_j1_dphi",&met_tenacious_tst_j1_dphi);
      m_tree_out->Branch("met_tenacious_tst_j2_dphi",&met_tenacious_tst_j2_dphi);
      m_tree_out->Branch("met_tenacious_tst_nolep_j1_dphi",&met_tenacious_tst_nolep_j1_dphi);
      m_tree_out->Branch("met_tenacious_tst_nolep_j2_dphi",&met_tenacious_tst_nolep_j2_dphi);
      m_tree_out->Branch("met_tight_tst_et",       &met_tight_tst_et);
      m_tree_out->Branch("met_tight_tst_phi",      &met_tight_tst_phi);
      m_tree_out->Branch("met_tight_tst_nolep_et",       &met_tight_tst_nolep_et);
      m_tree_out->Branch("met_tight_tst_nolep_phi",      &met_tight_tst_nolep_phi);
    }
    m_tree_out->Branch("metsig_tst",             &metsig_tst);

    if(m_currentVariation=="Nominal" && m_isMC){
      m_tree_out->Branch("truth_tau_pt", &truth_tau_pt);
      m_tree_out->Branch("truth_tau_eta",&truth_tau_eta);
      m_tree_out->Branch("truth_tau_phi",&truth_tau_phi);
      m_tree_out->Branch("truth_el_pt", &truth_el_pt);
      m_tree_out->Branch("truth_el_eta",&truth_el_eta);
      m_tree_out->Branch("truth_el_phi",&truth_el_phi);
      m_tree_out->Branch("truth_mu_pt", &truth_mu_pt);
      m_tree_out->Branch("truth_mu_eta",&truth_mu_eta);
      m_tree_out->Branch("truth_mu_phi",&truth_mu_phi);
      m_tree_out->Branch("truth_ph_pt", &truth_ph_pt);
      m_tree_out->Branch("truth_ph_eta",&truth_ph_eta);
      m_tree_out->Branch("truth_ph_phi",&truth_ph_phi);
    }else{
      truth_tau_pt=0; truth_tau_eta=0; truth_tau_phi=0;
      truth_el_pt=0;  truth_el_eta=0;  truth_el_phi=0;
      truth_mu_pt=0;  truth_mu_eta=0;  truth_mu_phi=0;
      truth_ph_pt=0;  truth_ph_eta=0;  truth_ph_phi=0;
    }
  }

  if(m_currentVariation=="Nominal" && m_isMC){
    m_tree_out->Branch("GenMET_pt", &GenMET_pt);
    m_tree_out->Branch("met_truth_et", &met_truth_et);
    m_tree_out->Branch("met_truth_phi", &met_truth_phi);
    m_tree_out->Branch("met_truth_sumet", &met_truth_sumet);
    m_tree_out->Branch("truth_jet_pt", &truth_jet_pt);
    m_tree_out->Branch("truth_jet_eta",&truth_jet_eta);
    m_tree_out->Branch("truth_jet_phi",&truth_jet_phi);
    m_tree_out->Branch("truth_jet_m",  &truth_jet_m);
    m_tree_out->Branch("truth_jj_mass",  &truth_jj_mass);
    m_tree_out->Branch("truth_jj_dphi",  &truth_jj_dphi);
    m_tree_out->Branch("truth_j2_pt",  &truth_j2_pt);
    m_tree_out->Branch("truthloMG_jj_mass",  &truthloMG_jj_mass);
    m_tree_out->Branch("truthloMG_jj_dphi",  &truthloMG_jj_dphi);
    m_tree_out->Branch("truthloMG_j2_pt",    &truthloMG_j2_pt);
  }else{
    truth_jet_pt=0; truth_jet_phi=0; truth_jet_eta=0; truth_jet_m=0;
  }
  //Register the output TTree
  CHECK(histSvc()->regTree("/MYSTREAM/"+treeTitleOut,m_tree_out));
  MapNgen(); //fill std::map with dsid->Ngen

  if(m_theoVariation){
    for (auto reg : regions){
      ANA_CHECK (book (TH1F (Form("jj_mass_%s_nominal",reg.c_str()), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    for(int i=0; i<115; i++)
      ANA_CHECK (book (TH1F (Form("all/jj_mass_%s_index_%d", reg.c_str(), i), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    for (auto var : variations)
      ANA_CHECK (book (TH1F (Form("scales/jj_mass_%s_%s",reg.c_str(),var.c_str()), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    for(int j=0; j<100; j++)
      ANA_CHECK (book (TH1F (Form("PDF/jj_mass_%s_pdf%d",reg.c_str(),j), ";m_{jj} [TeV];Entries", 50, 0, 5)));
   }
  }

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
  h_Gen = (TH1D*) f->Get("h_total");
  if(!h_Gen)ATH_MSG_WARNING("Number of events not found");

  for(int i=1; i<=h_Gen->GetNbinsX();i++){
    TString tmp = h_Gen->GetXaxis()->GetBinLabel(i);
    int dsid = tmp.Atoi();
    double N = h_Gen->GetBinContent(i);
    Ngen[dsid]=N;
    //std::cout << "input: " << dsid << " " << N << std::endl;
   }
  if(m_UseExtMGVjet){

    std::set<int> mg_w_filter = {311445,311446,311447,311448,311449,311450}; // W b-veto and c-veto
    std::set<int> mg_w_incl_lf = {363606, 363609, 363630, 363633, 363654, 363657}; // w samples to overlap remove in
    std::map<int,int> mg_w_LF_map = {{311445,363606},{311446,363630},{311447,363609},{311448,363633},{311449,363654},{311450,363657}};
    std::set<int> mg_w_filter_highHT = {311451, 311452, 311453}; // W ---> need to implement the year dependence
    std::set<int> mg_filter_lo_np01  =  {311429, 311433, 311437, 311441}; //entry 21 
    std::set<int> mg_filter_lo_np234 =  {311430, 311431, 311432, 311434, 311435, 311436, 311438, 311439, 311440, 311442, 311443, 311444}; //entry 22
    Ngen_filter.clear();
    TIter next(f->GetListOfKeys());
    TKey *key;
    while ((key = (TKey*)next())) {
      std::string the_dsid = std::string(key->GetName());
      if(the_dsid.find("skim_")==std::string::npos) continue;
      the_dsid.erase(0,5); // remove "skim_"
      int dsid = std::stoi(the_dsid);
      std::cout << "Skimming histograms for merging are being loaded for key: " << key->GetName() << std::endl;
      Ngen_filter[dsid]=static_cast<TH1D*>(f->Get(key->GetName()));
      // printing info
      if(mg_filter_lo_np01.find(dsid)!=mg_filter_lo_np01.end() || mg_filter_lo_np234.find(dsid)!=mg_filter_lo_np234.end()){
	std::cout << "Ngen: " << Ngen[dsid] << " filtered: " << Ngen_filter[dsid]->GetBinContent(21) << " " << Ngen_filter[dsid]->GetBinContent(22) << std::endl;
      }      
    }
  }

  return StatusCode::SUCCESS;

}

StatusCode VBFAnalysisAlg::execute() {
  ATH_MSG_DEBUG ("Executing " << name() << "...");

  // check that we don't have too many events
  if(nFileEvt>nFileEvtTot){
    if(m_currentVariation=="Nominal") ATH_MSG_ERROR("VBFAnaysisAlg::execute: Too  many events:  " << nFileEvt << " total evts: " << nFileEvtTot);
    return StatusCode::SUCCESS;
  }

  if(!m_tree) ATH_MSG_ERROR("VBFAnaysisAlg::execute: tree invalid: " <<m_tree );
  m_tree->GetEntry(nFileEvt);

  // iterate event count
  ++nFileEvt;
  if (runNumber != m_runNumberInput){ //HACK to hard set the run number except for the filtered samples
    if(!((m_runNumberInput>=309662 && m_runNumberInput<=309679) || m_runNumberInput==310502)) ATH_MSG_ERROR("VBFAnaysisAlg::execute: runNumber " << runNumber << " != m_runNumberInput " << m_runNumberInput << " " << jj_dphi << " avg: " << averageIntPerXing);
    runNumber=m_runNumberInput;
  }

  // initialize to 1
  for(std::map<TString,Float_t>::iterator it=tMapFloatW.begin(); it!=tMapFloatW.end(); ++it)
    it->second=1.0;

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
  bool CRZtt = false;

  // Fill
  truth_jj_mass =-1.0;
  truth_jj_dphi = -1.0;
  truth_j2_pt = -1.0;

  truthloMG_jj_mass =-1.0;
  truthloMG_jj_dphi = -1.0;
  truthloMG_j2_pt = -1.0;
  if(m_isMC && truth_jet_pt && truth_jet_pt->size()>1){
    TVector3 tvlep;
    vector<TLorentzVector> lomg_jets;
    TLorentzVector tmp, jjtruth;
    tmp.SetPtEtaPhiM(truth_jet_pt->at(0), truth_jet_eta->at(0),truth_jet_phi->at(0),truth_jet_m->at(0));
    jjtruth = tmp;
    tmp.SetPtEtaPhiM(truth_jet_pt->at(1), truth_jet_eta->at(1),truth_jet_phi->at(1),truth_jet_m->at(1));
    truth_jj_dphi = fabs(jjtruth.DeltaPhi(tmp));
    truth_j2_pt = truth_jet_pt->at(1);
    jjtruth += tmp;
    truth_jj_mass =jjtruth.M();
    // the LO MG filtering required overlap with electrons and taus. we need to implement this for the merging
    for(unsigned itjet=0; itjet<truth_jet_pt->size(); ++itjet){
      bool passOR_truthjet=true;
      tmp.SetPtEtaPhiM(truth_jet_pt->at(itjet), truth_jet_eta->at(itjet),truth_jet_phi->at(itjet),truth_jet_m->at(itjet));
      for(unsigned ittau=0; ittau<truth_tau_pt->size(); ++ittau){
	if(fabs(truth_tau_eta->at(ittau))>5 || truth_tau_pt->at(ittau)<20.0e3) continue;
	tvlep.SetPtEtaPhi(truth_tau_pt->at(ittau), truth_tau_eta->at(ittau),truth_tau_phi->at(ittau));
	if(tvlep.DeltaR(tmp.Vect())<0.3){ passOR_truthjet=false; break; }
      }
      if(passOR_truthjet){
	for(unsigned itele=0; itele<truth_el_pt->size(); ++itele){
	  if(fabs(truth_el_eta->at(itele))>5 || truth_el_pt->at(itele)<20.0e3) continue;
	  tvlep.SetPtEtaPhi(truth_el_pt->at(itele), truth_el_eta->at(itele),truth_el_phi->at(itele));
	  if(tvlep.DeltaR(tmp.Vect())<0.3){ passOR_truthjet=false; break; }
	}
      }// end electron overlap check
      if(passOR_truthjet) lomg_jets.push_back(tmp);
    }// end truth jet loop
    if(lomg_jets.size()>=2){
      truthloMG_jj_mass = (lomg_jets.at(0)+lomg_jets.at(1)).M();
      truthloMG_jj_dphi = fabs(lomg_jets.at(0).DeltaPhi(lomg_jets.at(1)));
      truthloMG_j2_pt = lomg_jets.at(1).Pt();
    }
    if(false && truthloMG_jj_mass<800.0e3){
      for(unsigned itjet=0; itjet<truth_jet_pt->size(); ++itjet){
	std::cout << "  jet " << itjet << " pt: " << truth_jet_pt->at(itjet) << " eta: " << truth_jet_eta->at(itjet) << " phi: " << truth_jet_phi->at(itjet) << std::endl;
	tmp.SetPtEtaPhiM(truth_jet_pt->at(itjet), truth_jet_eta->at(itjet),truth_jet_phi->at(itjet),truth_jet_m->at(itjet));
	for(unsigned ittau=0; ittau<truth_tau_pt->size(); ++ittau){
	  if(fabs(truth_tau_eta->at(ittau))>5 || truth_tau_pt->at(ittau)<20.0e3) continue;
	  tvlep.SetPtEtaPhi(truth_tau_pt->at(ittau), truth_tau_eta->at(ittau),truth_tau_phi->at(ittau));
	  std::cout << "     tau " << ittau << " pt: " << truth_tau_pt->at(ittau) <<" eta: " << truth_tau_eta->at(ittau) <<" phi: " << truth_tau_phi->at(ittau) 
		    << "status: " << truth_tau_status->at(ittau) << " dr: " << tvlep.DeltaR(tmp.Vect()) <<std::endl;
	}
	for(unsigned itele=0; itele<truth_el_pt->size(); ++itele){
          if(fabs(truth_el_eta->at(itele))>5 || truth_el_pt->at(itele)<20.0e3) continue;
          tvlep.SetPtEtaPhi(truth_el_pt->at(itele), truth_el_eta->at(itele),truth_el_phi->at(itele));
	  std::cout << "       ele " << itele << " pt: " << truth_el_pt->at(itele) <<" eta: " << truth_el_eta->at(itele) <<" phi: " << truth_el_phi->at(itele) 
		    << "status: " << truth_el_status->at(itele) << " dr: " << tvlep.DeltaR(tmp.Vect()) <<std::endl;
	}
      }
    } // end check
    
  }// end truth computation
  // MET trigger scale factor
  unsigned metRunNumber = randomRunNumber;
  if(!m_isMC) metRunNumber=runNumber;
  xeSFTrigWeight=1.0;
  xeSFTrigWeight__1up=1.0;
  xeSFTrigWeight__1down=1.0;
  xeSFTrigWeight_nomu=1.0;
  xeSFTrigWeight_nomu__1up=1.0;
  xeSFTrigWeight_nomu__1down=1.0;
  if(m_isMC && jet_pt && jet_pt->size()>1){
    TLorentzVector tmp, jj;
    tmp.SetPtEtaPhiM(jet_pt->at(0), jet_eta->at(0),jet_phi->at(0),jet_m->at(0));
    jj=tmp;
    tmp.SetPtEtaPhiM(jet_pt->at(1), jet_eta->at(1),jet_phi->at(1),jet_m->at(1));
    jj+=tmp;
    xeSFTrigWeight        = weightXETrigSF(met_tst_et, metRunNumber, 0); // met was used in the end instead of jj.Pt()
    xeSFTrigWeight__1up   = weightXETrigSF(met_tst_et, metRunNumber, 1);
    xeSFTrigWeight__1down = weightXETrigSF(met_tst_et, metRunNumber, 2);
    xeSFTrigWeight_nomu        = weightXETrigSF(met_tst_nolep_et, metRunNumber, 0); // met was used in the end instead of jj.Pt()
    xeSFTrigWeight_nomu__1up   = weightXETrigSF(met_tst_nolep_et, metRunNumber, 1);
    xeSFTrigWeight_nomu__1down = weightXETrigSF(met_tst_nolep_et, metRunNumber, 2);
  }
  // signal electroweak SF -NOTE: these numbers need to be updated for new cuts, mjj bins, and different mediator mass!!!
  nloEWKWeight=1.0;
  if(m_isMC && met_truth_et>-0.5 && (runNumber==346600 || runNumber==308567)){ // || (runNumber>=308275 && runNumber<=308283))){ // only applying to H125
    //nloEWKWeight=1.0 - 0.000342*(met_truth_et/1.0e3) - 0.0708;// tighter mjj>1TeV
    nloEWKWeight=1.0 - 0.000350*(met_truth_et/1.0e3) - 0.0430;    
    nloEWKWeight/=0.947; // the inclusive NLO EWK correction is already applied. Removing this here.

    // add systematics here - these are from the tighter mjj>1 TeV cuts
    // UP -0.000320 x Pt(Higgs) - 0.0729
    // DOWN -0.000355 x Pt(Higgs) - 0.0692
    // use (UP - DOWN) / 2
    float up = -0.000333*(met_truth_et/1.0e3) - 0.0450;
    float down = -0.000366 *(met_truth_et/1.0e3) - 0.0410;
    float syst = fabs(up-down)/2.0;
    if(m_currentVariation=="Nominal"){
      tMapFloat["nloEWKWeight__1down"]=nloEWKWeight - syst;
      tMapFloat["nloEWKWeight__1up"]=nloEWKWeight + syst;
    }
  }
  if(m_isMC && m_currentVariation=="Nominal"){// initialize
    // set the VBF variables systematics
    if(runNumber==346600) my_signalSystHelper.setVBFVars(tMapFloat,HTXS_Stage1_1_Fine_Category_pTjet25,mcEventWeights);
    if(runNumber==346588) my_signalSystHelper.setggFVars(tMapFloat,mcEventWeights, 111);
    if(runNumber>=312448 && runNumber<=312531) my_signalSystHelper.setggFVars(tMapFloat,mcEventWeights, 115); // filtered sherpa uses nnpdf

    // This is a bug fix in the MC production. The wrong PDF weight was used for the default. 
    // This changes to the => systematics will be fixed when the new signal samples are processed. This is tranparent with the fix
    if((!mcEventWeights || mcEventWeights->size()<120) && (runNumber==346600 || runNumber==346588)) std::cout << "ERROR the mcEvent Weights are missing!!!" << std::endl;
    if(runNumber==346588) mcEventWeight = mcEventWeights->at(111); // ggF
    if(runNumber==346600) mcEventWeight = mcEventWeights->at(109); // VBF
  }
  
  // applying a pileup weight for 2018 data
  puSyst2018Weight=1.0;
  if(m_currentVariation=="Nominal"){// initialize
    tMapFloat["puSyst2018Weight__1down"]=1.0;
    tMapFloat["puSyst2018Weight__1up"]=1.0;
  }
  if(m_isMC && metRunNumber>=348197){ // select for 2018
    if(averageIntPerXing>39.0 && averageIntPerXing<52.1){
      if(n_jet>2) puSyst2018Weight*=1.2;
      if(n_jet>2 && fabs(jet_eta->at(2))>3.0) puSyst2018Weight*=1.4;
      if(n_jet==2) puSyst2018Weight*=1.07;
      if(m_currentVariation=="Nominal"){
	tMapFloat["puSyst2018Weight__1down"]=1.0+(puSyst2018Weight-1.0)/2.0;
	tMapFloat["puSyst2018Weight__1up"]  =puSyst2018Weight+(puSyst2018Weight-1.0)/2.0;
	//std::cout << "puSyst2018Wei: " << puSyst2018Weight << " up: " << tMapFloat["puSyst2018Weight__1up"]  << " down: " << tMapFloat["puSyst2018Weight__1down"] << std::endl; 
      }
    }
    //puSyst2018Weight=1.0;
  } // end pileup weight systematic

  if (m_isMC){
    // hack for when the cross-section code messed up
    if(runNumber==309668) crossSection =  592.36*0.9728*0.001043;
    else  crossSection = my_XsecDB->xsectTimesEff(runNumber);//xs in pb
    //std::cout << "crossSection: " << crossSection << " " << runNumber << std::endl;
    // corrections for the filtered samples
    if(runNumber==309662) crossSection *= 0.9331*0.9702;
    else if(runNumber==309663) crossSection *= 0.9527*0.9702;
    else if(runNumber==309664) crossSection *= 0.9307*0.9702;
    else if(runNumber==309665) crossSection *= 0.6516*0.9751;
    else if(runNumber==309666) crossSection *= 0.1804*0.9751;
    else if(runNumber==309667) crossSection *= 0.6516*0.9728;
    else if(runNumber==309669) crossSection *= 0.5681*0.9728;
    else if(runNumber==309670) crossSection *= 0.2215*0.9728;
    else if(runNumber==309671) crossSection *= 0.5891*0.9728;
    else if(runNumber==309672) crossSection *= 0.6045*0.9728;
    else if(runNumber==309673) crossSection *= 0.5928*0.9728;
    else if(runNumber==309674) crossSection *= 0.5684*0.9702;
    else if(runNumber==309675) crossSection *= 0.2782*0.9702;
    else if(runNumber==309676) crossSection *= 0.5430*0.9702;
    else if(runNumber==309677) crossSection *= 0.2749*0.9702;
    else if(runNumber==309678) crossSection *= 0.5632*0.9702;
    else if(runNumber==309679) crossSection *= 0.2691*0.9702;
    else if(runNumber==310502) crossSection *= 0.95325;

    double NgenCorrected = 0.;
    if (m_UseExtMC) {
      vector<int> samplesfilter = {309665,309666,309667,309668,309669,309670,309671,309672,309673,309674,309675,309676,309677,309678,309679};
      vector<float> filtereffs = {6.28e-03,4.08e-03,6.08e-03,5.48e-03,1.56e-02,1.22e-02,1.02e-02,1.13e-02,1.58e-02,1.43e-02,1.03e-02,1.06e-02,8.75e-03,1.23e-02,9.03e-03};
      vector<int> samplesinclusive = {364103,364132,364145,364146,364106,364107,364120,364134,364148,364162,364163,364176,364177,364190,364191};
      unsigned index_f = std::find(samplesfilter.begin(), samplesfilter.end(), runNumber)-samplesfilter.begin();
      unsigned index_i = std::find(samplesinclusive.begin(), samplesinclusive.end(), runNumber)-samplesinclusive.begin();
      if (index_f < samplesfilter.size()){
	if(Ngen[runNumber]>0 && Ngen[samplesinclusive.at(index_f)] > 0){
	  NgenCorrected = (Ngen[runNumber]/filtereffs.at(index_f)+Ngen[samplesinclusive.at(index_f)])*filtereffs.at(index_f);
	}
      } else if (index_i < samplesinclusive.size()){
	if (passVjetsFilter) {
	  if(Ngen[runNumber]>0 && Ngen[samplesfilter.at(index_i)] > 0){
	    NgenCorrected = (Ngen[samplesfilter.at(index_i)]/filtereffs.at(index_i)+Ngen[runNumber]);
	  }
	} else {
	  NgenCorrected = Ngen[runNumber];
	}
      } else {
	NgenCorrected = Ngen[runNumber];
      }
    } else if(m_UseExtMGVjet){
      std::set<int> mg_w_filter = {311445,311446,311447,311448,311449,311450}; // W b-veto and c-veto
      std::set<int> mg_w_incl_lf = {363606, 363609, 363630, 363633, 363654, 363657}; // w samples to overlap remove in
      std::set<int> mg_w_filter_highHT = {311451, 311452, 311453}; // W ---> need to implement the year dependence
      //std::set<int> mg_w_incl_highHT = {363615,363616,};
      std::map<int,int> mg_w_LF_map = {{311445,363606},{311446,363630},{311447,363609},{311448,363633},{311449,363654},{311450,363657}};
      std::map<int,int> mg_w_LF_map_rev;
      for(std::map<int,int>::iterator it = mg_w_LF_map.begin(); it!=mg_w_LF_map.end(); ++it) { mg_w_LF_map_rev[it->second] = it->first; }

      // Look up weights in order to match
      if(mg_w_LF_map.find(runNumber)!=mg_w_LF_map.end()){  int aRun = runNumber; int bRun = mg_w_LF_map[runNumber];
	MGMergeWeightFilt=Ngen_filter[aRun]->GetBinContent(24)/(Ngen_filter[aRun]->GetBinContent(24)+Ngen_filter[bRun]->GetBinContent(24)); 
      }
      if(mg_w_LF_map_rev.find(runNumber)!=mg_w_LF_map_rev.end()){  int aRun = runNumber; int bRun = mg_w_LF_map_rev[runNumber];
	MGMergeWeightIncl=Ngen_filter[aRun]->GetBinContent(24)/(Ngen_filter[aRun]->GetBinContent(24)+Ngen_filter[bRun]->GetBinContent(24)); 
      }

      std::set<int> mg_filter_lo_np01  =  {311429, 311433, 311437, 311441}; //entry 21 
      std::set<int> mg_filter_lo_np234 =  {311430, 311431, 311432, 311434, 311435, 311436, 311438, 311439, 311440, 311442, 311443, 311444}; //entry 22
      NgenCorrected = Ngen[runNumber];
      if((truthloMG_j2_pt>35.0e3 && truthloMG_jj_dphi<2.5 && truthloMG_jj_mass>800.0e3) && !passVjetsFilterTauEl) std::cout << "local truth, but passVjetsFilterTauEl is false" << std::endl;
      //if(runNumber>=363123 && runNumber<=363170 && (MGVTruthPt>100.0e3 && (truthloMG_j2_pt>35.0e3 && truthloMG_jj_dphi<2.5 && truthloMG_jj_mass>800.0e3)) ) {  weight=-1;  return StatusCode::SUCCESS; } // remove events as these are replaced by filtered samples
      //if(runNumber>=361510 && runNumber<=361519 && (MGVTruthPt>100.0e3 && (truthloMG_j2_pt>35.0e3 && truthloMG_jj_dphi<2.5 && truthloMG_jj_mass>800.0e3)) ) {  weight=-1;  return StatusCode::SUCCESS; } // remove events as these are replaced by filtered samples
      if(runNumber>=363123 && runNumber<=363170 && (MGVTruthPt>100.0e3 && (passVjetsFilterTauEl)) ) {  weight=-1;  return StatusCode::SUCCESS; } // remove events as these are replaced by filtered samples
      if(runNumber>=361510 && runNumber<=361519 && (MGVTruthPt>100.0e3 && (passVjetsFilterTauEl)) ) {  weight=-1;  return StatusCode::SUCCESS; } // remove events as these are replaced by filtered samples
      if(mg_w_incl_lf.find(runNumber)!=mg_w_incl_lf.end() && (MGVTruthPt>100.0e3) && passVjetsFilter) {  NgenCorrected/=MGMergeWeightIncl;  } // apply the filter efficiency.
      if(mg_w_filter.find(runNumber)!=mg_w_filter.end()) {  NgenCorrected/=MGMergeWeightFilt;  } // apply the filter efficiency also to the filtered sample to merge
      //if(mg_w_filter_highHT.find(runNumber)!=mg_w_filter_highHT.end() ) { weight=-1; return StatusCode::SUCCESS; } // remove events. implemented to replace
      if(((runNumber>=363615 && runNumber<=363623) || (runNumber>=363639 && runNumber<=363647) || (runNumber>=363660 && runNumber<=363671)) && MGVTruthPt>100.0e3 && passVjetsFilter && nParton!=4) { weight=-1; return StatusCode::SUCCESS; } // remove events as these are replaced by filtered samples. only up to 3 partons are included in the filtered samples
      if(mg_filter_lo_np01.find(runNumber)!=mg_filter_lo_np01.end() && (MGVTruthPt<99.0e3) ) { weight=-1; return StatusCode::SUCCESS; } // remove events.
    } else {
      NgenCorrected = Ngen[runNumber];
    }
    if(NgenCorrected>0)  weight = crossSection/NgenCorrected;
    else ATH_MSG_WARNING("Ngen " << Ngen[runNumber] << " dsid " << runNumber );
    ATH_MSG_DEBUG("VBFAnalysisAlg: xs: "<< crossSection << " nevent: " << Ngen[runNumber] );
  } else {
    weight = 1;
  }

  // base lepton selection
  n_tau=0;
  outtau_pt->clear();
  outtau_eta->clear();
  outtau_phi->clear();
  if(m_extraVars || true){

    // overlap remove with the photons
    if(tau_pt){
      TVector3 tauvec,tmp;
      for(unsigned iTau=0; iTau<tau_pt->size(); ++iTau){
    	bool passOR=true;
    	tauvec.SetPtEtaPhi(tau_pt->at(iTau),tau_eta->at(iTau),tau_phi->at(iTau));
    	if(baseel_pt){
    	  for(unsigned iEle=0; iEle<baseel_pt->size(); ++iEle){
    	    if(baseel_pt->at(iEle)>4.5e3){
    	      tmp.SetPtEtaPhi(baseel_pt->at(iEle),baseel_eta->at(iEle),baseel_phi->at(iEle));
    	      if(tauvec.DeltaR(tmp)<0.2) passOR=false;
    	    }
    	  }
    	}
    	if(basemu_pt){
    	  for(unsigned iMuo=0; iMuo<basemu_pt->size(); ++iMuo){
    	    if(basemu_pt->at(iMuo)>4.0e3){
    	      tmp.SetPtEtaPhi(basemu_pt->at(iMuo),basemu_eta->at(iMuo),basemu_phi->at(iMuo));
    	      if(tauvec.DeltaR(tmp)<0.2) passOR=false;
    	    }
    	  }
    	}// end base muon overlap
    	if(passOR){
    	  outtau_pt->push_back(tau_pt->at(iTau));
    	  outtau_eta->push_back(tau_eta->at(iTau));
    	  outtau_phi->push_back(tau_phi->at(iTau));
    	  ++n_tau;
    	}
      }// end tau loop
    }// end tau overlap removal
  }// end extra variables
  // fill extra jet variables for 3rd jets
  if(m_extraVars && jet_pt){
    maxCentrality=0;
    max_mj_over_mjj=0.0;
    mj34=-9999.0;
    max_j_eta= fabs(jet_eta->at(0));
    if(jet_eta->size()>1 && fabs(jet_eta->at(1))>max_j_eta) max_j_eta= fabs(jet_eta->at(1));
    j3_centrality->clear();
    j3_dRj1->clear();
    j3_dRj2->clear();
    j3_minDR->clear();
    j3_mjclosest->clear();
    j3_min_mj->clear();
    j3_min_mj_over_mjj->clear();
    if(jet_pt->size()>2){
      TLorentzVector tmp, j1v, j2v, j3v, j4v;
      j1v.SetPtEtaPhiM(jet_pt->at(0), jet_eta->at(0), jet_phi->at(0), jet_m->at(0));
      j2v.SetPtEtaPhiM(jet_pt->at(1), jet_eta->at(1), jet_phi->at(1), jet_m->at(1));
      for(unsigned iJet=2; iJet<jet_pt->size(); ++iJet){
	tmp.SetPtEtaPhiM(jet_pt->at(iJet), jet_eta->at(iJet), jet_phi->at(iJet), jet_m->at(iJet));
	float dRj1=tmp.DeltaR(j1v);
	float dRj2=tmp.DeltaR(j2v);
	j3_dRj1->push_back(dRj1);
	j3_dRj2->push_back(dRj2);
	j3_minDR->push_back(std::min(dRj1,dRj2));
	float mj1 =  (tmp+j1v).M();
	float mj2 =  (tmp+j2v).M();
	j3_mjclosest->push_back(dRj1<dRj2 ? mj1 : mj2);
	j3_min_mj->push_back(std::min(mj1,mj2));
	j3_min_mj_over_mjj->push_back(std::min(mj1,mj2)/jj_mass);
	float centrality = exp(-4.0/std::pow(jj_deta,2) * std::pow(jet_eta->at(iJet) - (jet_eta->at(0)+jet_eta->at(1))/2.0,2));
	j3_centrality->push_back(centrality);
	if(maxCentrality<centrality) maxCentrality=centrality;
	if(max_mj_over_mjj<j3_min_mj_over_mjj->at(iJet-2)) max_mj_over_mjj=j3_min_mj_over_mjj->at(iJet-2);
      }
      if(jet_pt->size()>3){
	j3v.SetPtEtaPhiM(jet_pt->at(2), jet_eta->at(2), jet_phi->at(2), jet_m->at(2));
	j4v.SetPtEtaPhiM(jet_pt->at(3), jet_eta->at(3), jet_phi->at(3), jet_m->at(3));
	mj34 = (j3v+j4v).M();
      }
    }
  }

  // Load the PV parameters for jets
  if(m_QGTagger && jet_NTracks){
    jet_NTracks_PV->clear();
    jet_SumPtTracks_PV->clear();

    static SG::AuxElement::Accessor<int> acc_NumTrkPt500PV("NumTrkPt500PV");
    static SG::AuxElement::ConstAccessor<float> acc_qgTaggerDec("qgTagger");
    static SG::AuxElement::ConstAccessor<float> acc_qgTaggerWeight("qgTaggerWeight");

    if(m_currentVariation=="Nominal"){
      for(unsigned iQG=0; iQG<m_qgVars.size(); ++iQG){
	tMapFloat [m_qgVars.at(iQG)]=1.0;
      }
    }

    for(unsigned iJet=0; iJet<jet_NTracks->size(); ++iJet){
      if(jet_NTracks->at(iJet).size()>0)     jet_NTracks_PV    ->push_back(jet_NTracks->at(iJet)[0]);
      if(jet_SumPtTracks->at(iJet).size()>0) jet_SumPtTracks_PV->push_back(jet_SumPtTracks->at(iJet)[0]);

      // loading the qg tagger for systematics
      xAOD::Jet* new_jet = m_newJets->at(0);
      const xAOD::JetFourMom_t newp4(jet_pt->at(iJet), jet_eta->at(iJet), jet_phi->at(iJet), jet_m->at(iJet));
      new_jet->setJetP4(newp4); 

      acc_NumTrkPt500PV(*new_jet) = jet_NTracks->at(iJet)[0];
      if(jet_truthjet_pt && jet_truthjet_pt->size()>iJet){ // check that the variables exist to give backward compatibility
	new_jet->auxdata<int>("DFCommonJets_QGTagger_truthjet_nCharged") = jet_truthjet_nCharged->at(iJet);//jet->getAttribute<int>("truthjet_nCharged");
	new_jet->auxdata<int>("PartonTruthLabelID") = jet_PartonTruthLabelID->at(iJet); //jet->getAttribute<int>("PartonTruthLabelID");
	new_jet->auxdata<float>("DFCommonJets_QGTagger_truthjet_eta") = jet_truthjet_eta->at(iJet); //jet->getAttribute<float>("truthjet_eta");
	new_jet->auxdata<float>("DFCommonJets_QGTagger_truthjet_pt") = jet_truthjet_pt->at(iJet); //jet->getAttribute<float>("truthjet_pt");
      }else{ // dummy values for backward compatibility
	new_jet->auxdata<int>("DFCommonJets_QGTagger_truthjet_nCharged") = 10;//jet->getAttribute<int>("truthjet_nCharged");
	new_jet->auxdata<int>("PartonTruthLabelID") = jet_PartonTruthLabelID->at(iJet); //jet->getAttribute<int>("PartonTruthLabelID");
	new_jet->auxdata<float>("DFCommonJets_QGTagger_truthjet_eta") = 0.0; //jet->getAttribute<float>("truthjet_eta");
	new_jet->auxdata<float>("DFCommonJets_QGTagger_truthjet_pt") = 50000.0; //jet->getAttribute<float>("truthjet_pt");
      }
      // Loop over QG systematics
      if (m_isMC && m_currentVariation=="Nominal"){
	for(unsigned iQG=0; iQG<m_qgVars.size(); ++iQG){
	  ANA_CHECK(m_jetQGTool["JET_QG_Nominal"]->sysApplySystematicVariation(m_systSet[m_qgVars.at(iQG)]));
	  m_jetQGTool["JET_QG_Nominal"]->tag(*new_jet, nullptr); // add qg taging
	  if(acc_qgTaggerWeight.isAvailable(*new_jet))
	    tMapFloat[m_qgVars.at(iQG)] *= acc_qgTaggerWeight(*new_jet);
	}
      }
    }
  }
  // refill the base leptons
  if(n_baseel>int(baseel_pt->size())){
    for(unsigned a=0; a<el_pt->size(); ++a){
      unsigned fillIndx=0;
      for(unsigned b=0; b<baseel_pt->size(); ++b){
	if(el_pt->at(a)>baseel_pt->at(b)){
	  fillIndx=b; break;
	}
      }
      baseel_pt->insert(baseel_pt->begin()+fillIndx,el_pt->at(a));
      baseel_eta->insert(baseel_eta->begin()+fillIndx,el_eta->at(a));
      baseel_phi->insert(baseel_phi->begin()+fillIndx,el_phi->at(a));
      baseel_charge->insert(baseel_charge->begin()+fillIndx,el_charge->at(a));
    }
  }
  if(n_basemu>int(basemu_pt->size())){
    for(unsigned a=0; a<mu_pt->size(); ++a){
      unsigned fillIndx=0;
      for(unsigned b=0; b<basemu_pt->size(); ++b){
	if(mu_pt->at(a)>basemu_pt->at(b)){
	  fillIndx=b; break;
	}
      }
      basemu_pt->insert(basemu_pt->begin()+fillIndx,mu_pt->at(a));
      basemu_eta->insert(basemu_eta->begin()+fillIndx,mu_eta->at(a));
      basemu_phi->insert(basemu_phi->begin()+fillIndx,mu_phi->at(a));
      basemu_charge->insert(basemu_charge->begin()+fillIndx,mu_charge->at(a));
    }
  }
  // set the merging for the existing samples
  //364173-364175,364159-364161,364187-364189,364162-364163,364176-364177,364193-364194
  //364103,364132,364145-364146,364151,364134,364120,364106-364107
  if (m_UseExtMC){
    if((runNumber>=309662 && runNumber<=309664)) {
      passVjetsFilter=false;
    }else passVjetsFilter=true;
  } else {
    if((runNumber>=309662 && runNumber<=309679)){ // QCD NLO sherpa extension samples with Mjj filter
      // use the filter as calculated
    }else if((runNumber>=364173 && runNumber<=364175) || // Wenu 70-140 all three
	     (runNumber>=364159 && runNumber<=364161) || // Wmunu 70-140 all three
	     (runNumber>=364187 && runNumber<=364189) || // Wtaunu 70-140 all three
	     (runNumber>=364162 && runNumber<=364163) || // Wmunu 140-280 CVBV+cFilter
	     (runNumber>=364176 && runNumber<=364177) || // Wenu 140-280 CVBV+cFilter
	     (runNumber>=364190 && runNumber<=364191) || // Wtaunu 140-280 CVBV+cFilter
	     (runNumber>=364103 && runNumber<=364103) || // Zmm 70-140 CVBV
	     (runNumber>=364132 && runNumber<=364132) || // Ztautau_MAXHTPTV70_140_CFBV
	     (runNumber>=364145 && runNumber<=364146) || // Znn 70-140 CVBV, c Filter
	     (runNumber>=364148 && runNumber<=364148) || // znn 140-280 CVBV
	     (runNumber>=364134 && runNumber<=364134) || // Ztt 140-280 CVBV
	     (runNumber>=364120 && runNumber<=364120) || // Zee 140-280 CVBV
	     (runNumber>=364106 && runNumber<=364107)){  // Zmm 140-280 CVBV+cfilter
      passVjetsFilter=(!passVjetsFilter);
    }else passVjetsFilter=true;
  }
  //364112-364113,364126-364127,364140-364141,364154-364155
  //364168-364169,364182-364183,364196-364197
  // This section merges events with pTV>500 GeV. The MAXHTPTV samples have to be added together
  if((runNumber>=364216 && runNumber<=364229)){ // QCD NLO sherpa extension samples for pTV
  }else if((runNumber>=364112 && runNumber<=364113) || // Zmm 500, 1000 MAXPTHT
	   (runNumber>=364126 && runNumber<=364127) || // Zee 500, 1000 MAXPTHT
	   (runNumber>=364140 && runNumber<=364141) || // Ztt 500, 1000 MAXPTHT
	   (runNumber>=364154 && runNumber<=364155) || // Znn 500, 1000 MAXPTHT
	   (runNumber>=364168 && runNumber<=364169) || // Wmunu 500, 1000 MAXPTHT
	   (runNumber>=364182 && runNumber<=364183) || // Wenu 500, 1000 MAXPTHT
	   (runNumber>=364196 && runNumber<=364197)){  // Wtaunu 500, 1000 MAXPTHT
    passVjetsPTV=(!passVjetsPTV); // flip these
  }else passVjetsPTV=true;// others must pass
  // Now we have the KT merged 100-500 GeV in PTV samples. We want to merge these as well.
  if((runNumber>=312448 && runNumber<=312531)) passVjetsPTV=true; // these are the KT merged samples 100-500 GeV
  if((runNumber>=364100 && runNumber<=364113) || // Zmm MAXPTHT
     (runNumber>=364114 && runNumber<=364127) || // Zee MAXPTHT
     (runNumber>=364128 && runNumber<=364141) || // Ztt MAXPTHT
     (runNumber>=364142 && runNumber<=364155) || // Znn MAXPTHT
     (runNumber>=366010 && runNumber<=366035) || // Znn ptvmjj
     (runNumber>=364156 && runNumber<=364169) || // Wmunu MAXPTHT
     (runNumber>=364170 && runNumber<=364183) || // Wenu MAXPTHT
     (runNumber>=364184 && runNumber<=364197)){  // Wtaunu MAXPTHT  
    if(SherpaVTruthPt<100.0e3) passVjetsPTV=false; // remove if pTV>100
    if(SherpaVTruthPt>500.0e3) passVjetsPTV=false; // remove if pTV>100
  }

  // Fixing a bug in the variables
  if(jet_phi->size()>1){
    met_tst_nolep_j1_dphi = fabs(GetDPhi(met_tst_nolep_phi, jet_phi->at(0)));
    met_tst_nolep_j2_dphi = fabs(GetDPhi(met_tst_nolep_phi, jet_phi->at(1)));
  }

  // Definiing a loose skimming
  float METCut = 150.0e3;
  float LeadJetPtCut = 80.0e3;
  float subLeadJetPtCut = 50.0e3;
  float MjjCut =8e5;
  float DEtajjCut =3.5;

  if(m_LooseSkim && m_currentVariation=="Nominal"){
    METCut = 100.0e3;
    LeadJetPtCut = 60.0e3; // 60.0e3
    subLeadJetPtCut = 50.0e3; // 40.0e3
    MjjCut =2e5; // 2e5
    DEtajjCut =3.5; // 3.5
  }

  if (!((passGRL == 1) & (passPV == 1) & (passDetErr == 1) & (passJetCleanLoose == 1))) return StatusCode::SUCCESS;

  bool GammaMETSR = (n_ph>0) && (jj_deta>2.5) && (jj_mass>250.0e3);
  ATH_MSG_DEBUG ("Pass GRL, PV, DetErr, JetCleanLoose");
  if (n_jet < 2) return StatusCode::SUCCESS;
  if (!(n_jet < 5) && !m_LooseSkim) return StatusCode::SUCCESS;
  ATH_MSG_DEBUG ("n_jet = 2!");
  if (!(unsigned(n_jet) == jet_pt->size())) ATH_MSG_WARNING("n_jet != jet_pt->size()! n_jet: " <<n_jet << " jet_pt->size(): " << jet_pt->size());
  if (!(unsigned(n_jet) == jet_eta->size())) ATH_MSG_WARNING("n_jet != jet_eta->size()! n_jet: " <<n_jet << " jet_eta->size(): " << jet_eta->size());
  if (!(((jet_pt->at(0) > LeadJetPtCut) & (jet_pt->at(1) > subLeadJetPtCut) & (jj_dphi < 2.0) & (jj_deta > DEtajjCut) & ((jet_eta->at(0) * jet_eta->at(1))<0) & (jj_mass > MjjCut)) || GammaMETSR)) return StatusCode::SUCCESS; // was 1e6 for mjj
  ATH_MSG_DEBUG ("Pass VBF cuts!");
  // encoding met triggers
  trigger_met_encoded=0;
  if (trigger_HLT_xe100_mht_L1XE50 == 1) trigger_met_encoded+=0x1;
  if (trigger_HLT_xe110_mht_L1XE50 == 1) trigger_met_encoded+=0x2;
  if (trigger_HLT_xe90_mht_L1XE50 == 1)  trigger_met_encoded+=0x4;
  if (trigger_HLT_xe70_mht == 1)         trigger_met_encoded+=0x8;
  if (trigger_HLT_noalg_L1J400 == 1)     trigger_met_encoded+=0x10;

  // implement the trigger used in the analysis
  if((metRunNumber<=284484 && trigger_HLT_xe70_mht==1) ||                                // 2015
     (metRunNumber>284484 && metRunNumber<=302872 && trigger_HLT_xe90_mht_L1XE50==1) ||  // 2016
     (metRunNumber>302872 && trigger_HLT_xe110_mht_L1XE50==1) ||           // 2016
     trigger_HLT_noalg_L1J400 ==1 ) trigger_met = 1; else trigger_met = 0; // 2015+2016

  //
  // run selected for 2017 => value 4 for 2017
  //
  if     (325713<=metRunNumber) trigger_met=0; // zero it out for 2017
  if     (325713<=metRunNumber && metRunNumber<=328393 && ((trigger_met_encodedv2 & 0x4)==0x4))   trigger_met=1; //HLT_xe90_pufit_L1XE50;    // period B
  else if(329385<=metRunNumber && metRunNumber<=330470 && ((trigger_met_encodedv2 & 0x40)==0x40)) trigger_met=1; //HLT_xe100_pufit_L1XE55;   // period C
  else if(330857<=metRunNumber && metRunNumber<=331975 && ((trigger_met_encodedv2 & 0x2)==0x2))   trigger_met=1; //HLT_xe110_pufit_L1XE55;   // period D1-D5
  else if(341649>=metRunNumber && metRunNumber>331975 && ((trigger_met_encodedv2 & 0x80)==0x80))  trigger_met=1; //HLT_xe110_pufit_L1XE50;   // period D6-K  
  // 2018 update trigger for later periods => value 5 for
  if(metRunNumber>=348197) trigger_met=0; // zero it out for 2018
  if     (350067 >metRunNumber && metRunNumber>=348197  && ((trigger_met_encodedv2 & 0x8)==0x8))    trigger_met=1; // HLT_xe110_pufit_xe70_L1XE50
  else if(350067<=metRunNumber && metRunNumber<=364292 && ((trigger_met_encodedv2 & 0x800)==0x800)) trigger_met=1; // HLT_xe110_pufit_xe65_L1XE50
  //
  // end trigger implmentation for run periods
  //

  bool passMETTrig = trigger_met_encodedv2>0 || trigger_met>0 || trigger_met_encoded>0;
  if(m_METTrigPassThru) passMETTrig=true;
  ATH_MSG_DEBUG ("Assign trigger_met value");
  if(n_el== 1) {
    met_significance = met_tst_et/1000/sqrt((el_pt->at(0) + jet_pt->at(0) + jet_pt->at(1))/1000.);
  }else if(baseel_pt && n_baseel == 1 && baseel_pt->size()==1){
    met_significance = met_tst_et/1000/sqrt((baseel_pt->at(0) + jet_pt->at(0) + jet_pt->at(1))/1000.);
  }else if(n_mu == 1){
    met_significance = met_tst_et/1000/sqrt((mu_pt->at(0) + jet_pt->at(0) + jet_pt->at(1))/1000.);
  }else if(basemu_pt && n_basemu == 1 && basemu_pt->size()>0){
    met_significance = met_tst_et/1000/sqrt((basemu_pt->at(0) + jet_pt->at(0) + jet_pt->at(1))/1000.);
  }else {
    met_significance = 0;
  }
  ATH_MSG_DEBUG ("met_significance calculated");

  bool OneElec = (n_el == 1); // n_el should be a subset of baseel
  bool OneMuon = (n_mu == 1);// n_mu should be a subset of basemu
  bool passMETCut = (met_tst_et > METCut && (met_tst_j1_dphi>1.0) && (met_tst_j2_dphi>1.0));
  bool passMETNoLepCut = (met_tst_nolep_et > METCut && (met_tst_nolep_j1_dphi>1.0) && (met_tst_nolep_j2_dphi>1.0));
  if(!m_LooseSkim){
    if ((passMETTrig) && (passMETCut) && (n_el == 0) && (n_mu == 0)) SR = true;
  }else{
    passMETCut = (met_tst_et > METCut || met_tenacious_tst_et > METCut || met_tight_tst_et > METCut); // || met_tighter_tst_et > METCut);
    passMETNoLepCut = (met_tst_nolep_et > METCut || met_tenacious_tst_nolep_et > METCut || met_tight_tst_nolep_et > METCut);// || met_tighter_tst_nolep_et > METCut);
    //if ((passMETTrig) && (passMETCut) && (n_el == 0) && (n_mu == 0)) SR = true;
    if ((passMETCut) && (n_el == 0) && (n_mu == 0)) SR = true;
    // saving the base leptons for the fake lepton estimate. This is done in the loose skimming
    OneElec = (n_el == 1 || n_baseel==1); // n_el should be a subset of baseel ... will need to modify for the systematics in v27Loose
    OneMuon = (n_mu == 1 || n_basemu==1);// n_mu should be a subset of basemu
  }
  // protect the systematic variations from crashing
  if(n_baseel==1 && n_el==0 && baseel_charge->size()==0) baseel_charge->push_back(-999);
  if(n_basemu==1 && n_mu==0 && basemu_charge->size()==0) basemu_charge->push_back(-999);

  //std::cout << "charge: " << baseel_charge->size() << " n_baseel: " << n_baseel << " mu: " << basemu_charge->size() << " n_basemu: " << n_basemu << " n_mu: " << n_mu << " n_el: " << n_el << " n_jet: " << n_jet << std::endl;
  if (SR) ATH_MSG_DEBUG ("It's SR!"); else ATH_MSG_DEBUG ("It's NOT SR");
  if ((trigger_lep > 0) && (passMETNoLepCut) && (OneElec) & (n_mu == 0)){ if ((baseel_charge->at(0) > 0) & (met_significance > 4.0)) CRWep = true;}
  if (CRWep) ATH_MSG_DEBUG ("It's CRWep!"); else ATH_MSG_DEBUG ("It's NOT CRWep");
  if ((trigger_lep > 0) && (passMETNoLepCut) && (OneElec) && (n_mu == 0)){ if ((baseel_charge->at(0) < 0) & (met_significance > 4.0)) CRWen = true;}
  if (CRWen) ATH_MSG_DEBUG ("It's CRWen!"); else ATH_MSG_DEBUG ("It's NOT CRWen");
  if ((trigger_lep > 0) && (passMETNoLepCut) && (OneElec) && (n_mu == 0)){ if ((baseel_charge->at(0) > 0) & (met_significance <= 4.0)) CRWepLowSig = true;}
  if (CRWepLowSig) ATH_MSG_DEBUG ("It's CRWepLowSig!"); else ATH_MSG_DEBUG ("It's NOT CRWepLowSig");
  if ((trigger_lep > 0) && (passMETNoLepCut) && (OneElec) && (n_mu == 0)){ if ((baseel_charge->at(0) < 0) & (met_significance <= 4.0)) CRWenLowSig = true;}
  if (CRWenLowSig) ATH_MSG_DEBUG ("It's CRWenLowSig!"); else ATH_MSG_DEBUG ("It's NOT CRWenLowSig");
  if ((trigger_lep > 0 || passMETTrig) && (passMETNoLepCut) && (n_el == 0) && (OneMuon)){ if ((basemu_charge->at(0) > 0)) CRWmp = true;}
  if (CRWmp) ATH_MSG_DEBUG ("It's CRWmp!"); else ATH_MSG_DEBUG ("It's NOT CRWmp");
  if ((trigger_lep > 0 || passMETTrig) && (passMETNoLepCut) && (n_el == 0) && (OneMuon)){ if ((basemu_charge->at(0) < 0)) CRWmn = true;}
  if (CRWmn) ATH_MSG_DEBUG ("It's CRWmn!"); else ATH_MSG_DEBUG ("It's NOT CRWmn");
  if ((trigger_lep > 0) && (passMETNoLepCut) && (n_el == 2) && (n_mu == 0)){ if ((el_charge->at(0)*el_charge->at(1) < 0)) CRZee = true;}
  if (CRZee) ATH_MSG_DEBUG ("It's CRZee!"); else ATH_MSG_DEBUG ("It's NOT CRZee");
  if ((trigger_lep > 0 || passMETTrig) && (passMETNoLepCut) && (n_el == 0) && (n_mu == 2)){ if ((mu_charge->at(0)*mu_charge->at(1) < 0)) CRZmm = true;}
  if (CRZmm) ATH_MSG_DEBUG ("It's CRZmm!"); else ATH_MSG_DEBUG ("It's NOT CRZmm");
  if ((trigger_lep > 0 || passMETTrig) && (passMETNoLepCut) && (n_baseel+n_basemu>=2)){ CRZtt = true;}
  if (CRZtt) ATH_MSG_DEBUG ("It's CRZtt!"); else ATH_MSG_DEBUG ("It's NOT CRZtt"); // this allows the baseline>=2 to pass

  // reset the electron anti-ID SF to only affect W events. To be fixed. kind of a hack
  bool isWenu = ((runNumber>=364170 && runNumber<=364183) || (runNumber>=363600 && runNumber<=363623) || (runNumber==363359 || runNumber==363360 || runNumber==363489));
  eleANTISF=std::min<float>(eleANTISF,1.5);
  eleANTISF=std::max<float>(eleANTISF,0.6);
  if(isWenu){
    if(!(n_baseel==0 && n_basemu==0)) eleANTISF=1.0;
  }else{ eleANTISF=1.0; }

  float tmpD_muSFTrigWeight = muSFTrigWeight;
  if(m_oneTrigMuon && passMETTrig) tmpD_muSFTrigWeight=1.0;
  w = weight*mcEventWeight*puWeight*(met_tenacious_tst_nolep_et>180.0e3 ? fjvtSFWeight : fjvtSFTighterWeight)*jvtSFWeight*elSFWeight*muSFWeight*elSFTrigWeight*tmpD_muSFTrigWeight*eleANTISF*nloEWKWeight*phSFWeight*puSyst2018Weight;

  if(m_theoVariation){
    std::map<TString,bool> regDecision;
    regDecision["Incl"]=true;
    regDecision["SR"]=SR;
    regDecision["CRWe"]=(CRWep || CRWen);
    regDecision["CRWm"]=(CRWmp || CRWmn);
    regDecision["CRW"]= (CRWep || CRWen || CRWmp || CRWmn);
    regDecision["CRZee"]=CRZee;
    regDecision["CRZmm"]=CRZmm;
    regDecision["CRZ"]=(CRZee || CRZmm);

    for(auto reg : regions){
      for(int i=0; i<115; i++){
        if(regDecision[reg])
          hist("jj_mass_"+reg+"_index_"+to_string(i))->Fill(jj_mass/1e6, w*mcEventWeights->at(i));
      }
      if(regDecision[reg]){
	hist( "jj_mass_"+reg+"_nominal" )->Fill(jj_mass/1e6, w);
	hist( "scales/jj_mass_"+reg+"_fac_up" )->Fill(jj_mass/1e6, w*mcEventWeights->at(8));
	hist( "scales/jj_mass_"+reg+"_fac_down" )->Fill(jj_mass/1e6, w*mcEventWeights->at(6));
	hist( "scales/jj_mass_"+reg+"_renorm_up" )->Fill(jj_mass/1e6, w*mcEventWeights->at(9));
	hist( "scales/jj_mass_"+reg+"_renorm_down" )->Fill(jj_mass/1e6, w*mcEventWeights->at(5));
	hist( "scales/jj_mass_"+reg+"_both_up" )->Fill(jj_mass/1e6, w*mcEventWeights->at(10));
	hist( "scales/jj_mass_"+reg+"_both_down" )->Fill(jj_mass/1e6, w*mcEventWeights->at(4));
	for(unsigned int j = 11; j <= 110; j++)
	  hist( "PDF/jj_mass_"+reg+"_pdf"+to_string(j-11) )->Fill(jj_mass/1e6, w*mcEventWeights->at(j));
      }
    }
  }

  //
  /// compute the systematics weights
  //
  float tmp_puWeight = puWeight;
  float tmp_jvtSFWeight = jvtSFWeight;
  float tmp_fjvtSFWeight = (met_tenacious_tst_nolep_et>180.0e3 ? fjvtSFWeight : fjvtSFTighterWeight);
  float tmp_elSFWeight = elSFWeight;
  float tmp_muSFWeight = muSFWeight;
  float tmp_elSFTrigWeight = elSFTrigWeight;
  float tmp_muSFTrigWeight = muSFTrigWeight;
  float tmp_phSFWeight = phSFWeight;
  float tmp_eleANTISF = eleANTISF;
  float tmp_nloEWKWeight = nloEWKWeight;
  float tmp_puSyst2018Weight = puSyst2018Weight;
  float tmp_qgTagWeight = 1.0; // assuming the default weight is 1.0 for qg tagging
  float tmp_signalTruthSyst=1.0; // signal truth systematics

  for(std::map<TString,Float_t>::iterator it=tMapFloat.begin(); it!=tMapFloat.end(); ++it){
    //std::cout << "syst: " << it->first <<std::endl;
    // initialize
    tmp_puWeight = puWeight;
    tmp_jvtSFWeight = jvtSFWeight;
    tmp_fjvtSFWeight = (met_tenacious_tst_nolep_et>180.0e3 ? fjvtSFWeight : fjvtSFTighterWeight);
    tmp_elSFWeight = elSFWeight;
    tmp_muSFWeight = muSFWeight;
    tmp_elSFTrigWeight = elSFTrigWeight;
    tmp_muSFTrigWeight = muSFTrigWeight;
    tmp_phSFWeight = phSFWeight;
    tmp_eleANTISF = eleANTISF;
    tmp_nloEWKWeight = nloEWKWeight;
    tmp_puSyst2018Weight = puSyst2018Weight;
    tmp_qgTagWeight = 1.0; // default value is 1
    tmp_signalTruthSyst=1.0; // default value is 1
    if(it->first.Contains("fjvtSFWeight")        && (met_tenacious_tst_nolep_et >180.0e3))   tmp_fjvtSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("fjvtSFTighterWeight") && (met_tenacious_tst_nolep_et<=180.0e3))   tmp_fjvtSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("jvtSFWeight"))         tmp_jvtSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("puWeight"))       tmp_puWeight=tMapFloat[it->first];
    else if(it->first.Contains("elSFWeight"))     tmp_elSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("muSFWeight"))     tmp_muSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("elSFTrigWeight")) tmp_elSFTrigWeight=tMapFloat[it->first];
    else if(it->first.Contains("muSFTrigWeight")) tmp_muSFTrigWeight=tMapFloat[it->first];
    else if(it->first.Contains("phSFWeight")) tmp_phSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("nloEWKWeight"))   tmp_nloEWKWeight=tMapFloat[it->first];
    else if(it->first.Contains("puSyst2018Weight"))   tmp_puSyst2018Weight=tMapFloat[it->first];
    else if(it->first.Contains("VBF_qqH_"))   tmp_signalTruthSyst=tMapFloat[it->first]; // scale + S-T VBF + PS modelling
    else if(it->first.Contains("ggF_gg2H_"))   tmp_signalTruthSyst=tMapFloat[it->first]; // PS modelling
    else if(it->first.Contains("ATLAS_PDF4LHC_NLO_30_"))   tmp_signalTruthSyst=tMapFloat[it->first]; //PDF
    else if(it->first.Contains("JET_QG_"))        tmp_qgTagWeight=tMapFloat[it->first];
    else if(it->first.Contains("eleANTISF")){
      tmp_eleANTISF=tMapFloat[it->first];
      tmp_eleANTISF=std::min<float>(tmp_eleANTISF,1.5);
      tmp_eleANTISF=std::max<float>(tmp_eleANTISF,0.6);
      if(isWenu){
	if(!(n_baseel==0 && n_basemu==0)) tmp_eleANTISF=1.0;
      }else{ tmp_eleANTISF=1.0; }
    }

    if(m_oneTrigMuon && passMETTrig) tmp_muSFTrigWeight=1.0;
    ATH_MSG_DEBUG("VBFAnalysisAlg Syst: " << it->first << " weight: " << weight << " mcEventWeight: " << mcEventWeight << " puWeight: " << tmp_puWeight << " jvtSFWeight: " << tmp_jvtSFWeight << " elSFWeight: " << tmp_elSFWeight << " muSFWeight: " << tmp_muSFWeight << " elSFTrigWeight: " << tmp_elSFTrigWeight << " muSFTrigWeight: " << tmp_muSFTrigWeight << " phSFWeight: " << tmp_phSFWeight << " eleANTISF: " << tmp_eleANTISF << " nloEWKWeight: " << tmp_nloEWKWeight << " qg: " << tmp_qgTagWeight << " PU2018: " << tmp_puSyst2018Weight << " truth syst: " << tmp_signalTruthSyst);


    tMapFloatW[it->first]=weight*mcEventWeight*tmp_puWeight*tmp_jvtSFWeight*tmp_fjvtSFWeight*tmp_elSFWeight*tmp_muSFWeight*tmp_elSFTrigWeight*tmp_muSFTrigWeight*tmp_eleANTISF*tmp_nloEWKWeight*tmp_qgTagWeight*tmp_phSFWeight*tmp_puSyst2018Weight*tmp_signalTruthSyst;
    //std::cout << "sys: " << it->first << " pu: " << tmp_puSyst2018Weight << " " << tMapFloatW[it->first] << std::endl; 
  }//end systematic weight loop

  ATH_MSG_DEBUG("VBFAnalysisAlg: weight: " << weight << " mcEventWeight: " << mcEventWeight << " puWeight: " << puWeight << " jvtSFWeight: " << jvtSFWeight << " elSFWeight: " << elSFWeight << " muSFWeight: " << muSFWeight << " elSFTrigWeight: " << elSFTrigWeight << " muSFTrigWeight: " << muSFTrigWeight << " phSFWeight: " << phSFWeight << " eleANTISF: " << eleANTISF << " nloEWKWeight: " << nloEWKWeight << " qg: " << tmp_qgTagWeight << " PU2018: " << tmp_puSyst2018Weight);

  // only save events that pass any of the regions
  if (!(SR || CRWep || CRWen || CRWepLowSig || CRWenLowSig || CRWmp || CRWmn || CRZee || CRZmm || CRZtt || GammaMETSR)) return StatusCode::SUCCESS;
  double m_met_tenacious_tst_j1_dphi, m_met_tenacious_tst_j2_dphi;
  computeMETj(met_tenacious_tst_phi, jet_phi, m_met_tenacious_tst_j1_dphi,m_met_tenacious_tst_j2_dphi);
  met_tenacious_tst_j1_dphi = m_met_tenacious_tst_j1_dphi;
  met_tenacious_tst_j2_dphi = m_met_tenacious_tst_j2_dphi;

  double m_met_tenacious_tst_nolep_j1_dphi, m_met_tenacious_tst_nolep_j2_dphi;
  computeMETj(met_tenacious_tst_nolep_phi, jet_phi, m_met_tenacious_tst_nolep_j1_dphi,m_met_tenacious_tst_nolep_j2_dphi);
  met_tenacious_tst_nolep_j1_dphi = m_met_tenacious_tst_nolep_j1_dphi;
  met_tenacious_tst_nolep_j2_dphi = m_met_tenacious_tst_nolep_j2_dphi;

  m_tree_out->Fill();

  //setFilterPassed(true); //if got here, assume that means algorithm passed
  return StatusCode::SUCCESS;
}

void VBFAnalysisAlg::computeMETj( Float_t met_phi,  std::vector<Float_t>* jet_phi, double &e_met_j1_dphi, double &e_met_j2_dphi)
{
  e_met_j1_dphi = abs(TVector2::Phi_mpi_pi(met_phi-jet_phi->at(0)));
  e_met_j2_dphi = abs(TVector2::Phi_mpi_pi(met_phi-jet_phi->at(1)));
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
  nFileEvt=0;
  m_treeName = "MiniNtuple";
  if(m_currentVariation!="Nominal")
    m_treeName = "MiniNtuple_"+m_currentVariation;
  std::cout << "Tree: " << m_treeName << std::endl;
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  if(!m_tree) ATH_MSG_ERROR("VBFAnaysisAlg::beginInputFile - tree is invalid " << m_tree);

  nFileEvtTot=m_tree->GetEntries();
  m_tree->SetBranchStatus("*",0);
  // add the systematics weights to the nominal
  TObjArray *var_list = m_tree->GetListOfBranches();

  if(m_currentVariation=="Nominal"){
    for(unsigned a=0; a<unsigned(var_list->GetEntries()); ++a) {
      TString var_name = var_list->At(a)->GetName();
      if(var_name.Contains("__1up") || var_name.Contains("__1down")){
	m_tree->SetBranchStatus(var_name, 1);
	if(tMapFloat.find(var_name)==tMapFloat.end()){
	  tMapFloat[var_name]=-999.0;
	  tMapFloatW[var_name]=-999.0;
	  m_tree_out->Branch("w"+var_name,&(tMapFloatW[var_name]));
	}
	m_tree->SetBranchStatus(var_name, 1);
	m_tree->SetBranchAddress(var_name, &(tMapFloat[var_name]));
      }
    }
  }
  // add nloEWK
  if(m_isMC){
    if(m_currentVariation=="Nominal"){
      
      // initialize the VBF & ggF variables
      if(m_runNumberInput==346600) my_signalSystHelper.initVBFVars(tMapFloat,tMapFloatW, m_tree_out);
      if(m_runNumberInput==346588) my_signalSystHelper.initggFVars(tMapFloat,tMapFloatW, m_tree_out);
      if(m_runNumberInput>=312448 && m_runNumberInput<=312531) my_signalSystHelper.initggFVars(tMapFloat,tMapFloatW, m_tree_out);// filtered Sherpa samples use nnPDF

      if(tMapFloat.find("nloEWKWeight__1up")==tMapFloat.end()){
	tMapFloat["nloEWKWeight__1up"]=1.0;
	tMapFloatW["nloEWKWeight__1up"]=1.0;
	m_tree_out->Branch("wnloEWKWeight__1up",&(tMapFloatW["nloEWKWeight__1up"]));
      }
      if(tMapFloat.find("nloEWKWeight__1down")==tMapFloat.end()){
	tMapFloat["nloEWKWeight__1down"]=1.0;
	tMapFloatW["nloEWKWeight__1down"]=1.0;
	m_tree_out->Branch("wnloEWKWeight__1down",&(tMapFloatW["nloEWKWeight__1down"]));
      }
      if(tMapFloat.find("puSyst2018Weight__1up")==tMapFloat.end()){
	tMapFloat ["puSyst2018Weight__1up"]=1.0;
	tMapFloatW["puSyst2018Weight__1up"]=1.0;
	m_tree_out->Branch("wpuSyst2018Weight__1up",&(tMapFloatW["puSyst2018Weight__1up"]));
      }
      if(tMapFloat.find("puSyst2018Weight__1down")==tMapFloat.end()){
	tMapFloat ["puSyst2018Weight__1down"]=1.0;
	tMapFloatW["puSyst2018Weight__1down"]=1.0;
	m_tree_out->Branch("wpuSyst2018Weight__1down",&(tMapFloatW["puSyst2018Weight__1down"]));
      }

      for(unsigned iQG=0; iQG<m_qgVars.size(); ++iQG){
	if(tMapFloat.find(m_qgVars.at(iQG))==tMapFloat.end()){ 
	  tMapFloat[m_qgVars.at(iQG)]=1.0; 
	  tMapFloatW[m_qgVars.at(iQG)]=1.0;
	  m_tree_out->Branch("w"+m_qgVars.at(iQG),&(tMapFloatW[m_qgVars.at(iQG)])); 
	}
      }// end qg variables
    }
  }

  m_tree->SetBranchStatus("runNumber", 1);
  m_tree->SetBranchStatus("randomRunNumber", 1);
  m_tree->SetBranchStatus("eventNumber", 1);
  m_tree->SetBranchStatus("nParton", 1);
  m_tree->SetBranchStatus("averageIntPerXing", 1);
  m_tree->SetBranchStatus("mcEventWeight", 1);
  m_tree->SetBranchStatus("mcEventWeights", 1);
  if(m_currentVariation=="Nominal" && m_isMC){
    m_tree->SetBranchStatus("HTXS_prodMode", 1);
    m_tree->SetBranchStatus("HTXS_errorCode", 1);
    m_tree->SetBranchStatus("HTXS_Stage1_1_Fine_Category_pTjet25", 1);
  }
  m_tree->SetBranchStatus("puWeight", 1);
  m_tree->SetBranchStatus("jvtSFWeight", 1);
  m_tree->SetBranchStatus("fjvtSFWeight", 1);
  m_tree->SetBranchStatus("fjvtSFTighterWeight", 1);
  m_tree->SetBranchStatus("eleANTISF", 1);
  m_tree->SetBranchStatus("elSFWeight", 1);
  m_tree->SetBranchStatus("muSFWeight", 1);
  m_tree->SetBranchStatus("elSFTrigWeight", 1);
  m_tree->SetBranchStatus("muSFTrigWeight", 1);
  m_tree->SetBranchStatus("phSFWeight", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe100_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe110_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe90_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe70_mht", 1);
  m_tree->SetBranchStatus("trigger_HLT_noalg_L1J400", 1);
  m_tree->SetBranchStatus("trigger_lep", 1);
  m_tree->SetBranchStatus("lep_trig_match", 1);
  m_tree->SetBranchStatus("trigger_met", 1);
  m_tree->SetBranchStatus("l1_met_trig_encoded", 1);
  m_tree->SetBranchStatus("passBatman", 1);
  m_tree->SetBranchStatus("passVjetsFilter", 1);
  m_tree->SetBranchStatus("passVjetsFilterTauEl", 1);
  m_tree->SetBranchStatus("passVjetsPTV", 1);
  m_tree->SetBranchStatus("MGVTruthPt", 1);
  m_tree->SetBranchStatus("SherpaVTruthPt", 1);
  m_tree->SetBranchStatus("in_vy_overlap", 1);// prefer this one. the iso shouldnt be required
  m_tree->SetBranchStatus("in_vy_overlap_iso", 1);
  m_tree->SetBranchStatus("FlavourFilter", 1);
  m_tree->SetBranchStatus("passGRL", 1);
  m_tree->SetBranchStatus("passPV", 1);
  m_tree->SetBranchStatus("passDetErr", 1);
  m_tree->SetBranchStatus("n_vx", 1);
  m_tree->SetBranchStatus("passJetCleanLoose", 1);
  m_tree->SetBranchStatus("passJetCleanTight", 1);
  m_tree->SetBranchStatus("n_jet",1);
  m_tree->SetBranchStatus("n_el",1);
  m_tree->SetBranchStatus("n_mu",1);
  m_tree->SetBranchStatus("n_el_w",1);
  m_tree->SetBranchStatus("n_mu_w",1);
  m_tree->SetBranchStatus("n_ph",1);
  m_tree->SetBranchStatus("n_bjet",1);
  m_tree->SetBranchStatus("n_el_baseline",1);
  m_tree->SetBranchStatus("n_mu_baseline",1);
  m_tree->SetBranchStatus("n_el_baseline_noOR",1);
  m_tree->SetBranchStatus("n_mu_baseline_noOR",1);
  m_tree->SetBranchStatus("n_el_baseline_iso",1);
  m_tree->SetBranchStatus("n_mu_baseline_iso",1);
  m_tree->SetBranchStatus("jj_mass",1);
  m_tree->SetBranchStatus("jj_deta",1);
  m_tree->SetBranchStatus("jj_dphi",1);
  m_tree->SetBranchStatus("met_tst_j1_dphi",1);
  m_tree->SetBranchStatus("met_tst_j2_dphi",1);
  m_tree->SetBranchStatus("met_tst_nolep_j1_dphi",1);
  m_tree->SetBranchStatus("met_tst_nolep_j2_dphi",1);
  m_tree->SetBranchStatus("met_cst_jet",1);
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
  m_tree->SetBranchStatus("jet_m",1);
  m_tree->SetBranchStatus("jet_jvt",1);
  m_tree->SetBranchStatus("jet_timing",1);
  m_tree->SetBranchStatus("jet_btag_weight",1);
  m_tree->SetBranchStatus("jet_PartonTruthLabelID",1);
  m_tree->SetBranchStatus("jet_ConeTruthLabelID",1);
  if(m_QGTagger){
    m_tree->SetBranchStatus("jet_NTracks",1);
    m_tree->SetBranchStatus("jet_SumPtTracks",1);
    m_tree->SetBranchStatus("jet_TrackWidth",1);
    m_tree->SetBranchStatus("jet_TracksC1",1);
    m_tree->SetBranchStatus("jet_truthjet_pt",1);
    m_tree->SetBranchStatus("jet_truthjet_eta",1);
    m_tree->SetBranchStatus("jet_truthjet_nCharged",1);
    m_tree->SetBranchStatus("jet_HECFrac",1);
    m_tree->SetBranchStatus("jet_EMFrac",1);
    m_tree->SetBranchStatus("jet_fch",1);
  }

  if(m_extraVars){

    m_tree->SetBranchStatus("lumiBlock",1);
    m_tree->SetBranchStatus("bcid",1);
    m_tree->SetBranchStatus("BCIDDistanceFromFront",1);

    m_tree->SetBranchStatus("ph_pt",1);
    m_tree->SetBranchStatus("ph_phi",1);
    m_tree->SetBranchStatus("ph_eta",1);
    m_tree->SetBranchStatus("tau_pt",1);
    m_tree->SetBranchStatus("tau_phi",1);
    m_tree->SetBranchStatus("tau_eta",1);

    m_tree->SetBranchStatus("jet_fjvt",1);
    m_tree->SetBranchStatus("basemu_pt",1);
    m_tree->SetBranchStatus("basemu_eta",1);
    m_tree->SetBranchStatus("basemu_phi",1);
    m_tree->SetBranchStatus("basemu_charge",1);
    m_tree->SetBranchStatus("basemu_z0",1);
    m_tree->SetBranchStatus("basemu_d0sig",1);
    m_tree->SetBranchStatus("basemu_ptvarcone20",1);
    m_tree->SetBranchStatus("basemu_ptvarcone30",1);
    m_tree->SetBranchStatus("basemu_topoetcone20",1);
    m_tree->SetBranchStatus("basemu_topoetcone30",1);
    m_tree->SetBranchStatus("basemu_type",1);
    if(m_isMC) m_tree->SetBranchStatus("basemu_truthOrigin",1);
    if(m_isMC) m_tree->SetBranchStatus("basemu_truthType",1);
    m_tree->SetBranchStatus("baseel_pt",1);
    m_tree->SetBranchStatus("baseel_eta",1);
    m_tree->SetBranchStatus("baseel_phi",1);
    m_tree->SetBranchStatus("baseel_charge",1);
    m_tree->SetBranchStatus("baseel_z0",1);
    m_tree->SetBranchStatus("baseel_d0sig",1);
    m_tree->SetBranchStatus("baseel_ptvarcone20",1);
    m_tree->SetBranchStatus("baseel_topoetcone20",1);
    if(m_isMC) m_tree->SetBranchStatus("baseel_truthOrigin",1);
    if(m_isMC) m_tree->SetBranchStatus("baseel_truthType",1);
    m_tree->SetBranchStatus("met_soft_tst_phi",1);
    m_tree->SetBranchStatus("met_soft_tst_sumet",1);
    m_tree->SetBranchStatus("met_soft_tst_et",1);
    m_tree->SetBranchStatus("met_tenacious_tst_et",1);
    m_tree->SetBranchStatus("met_tenacious_tst_phi",1);
    m_tree->SetBranchStatus("met_tight_tst_et",1);
    m_tree->SetBranchStatus("met_tight_tst_phi",1);
    m_tree->SetBranchStatus("met_tenacious_tst_nolep_et",1);
    m_tree->SetBranchStatus("met_tenacious_tst_nolep_phi",1);
    m_tree->SetBranchStatus("met_tight_tst_nolep_et",1);
    m_tree->SetBranchStatus("met_tight_tst_nolep_phi",1);
    m_tree->SetBranchStatus("metsig_tst",1);

    if(m_currentVariation=="Nominal" && m_contLep){
      m_tree->SetBranchStatus("contel_pt",1);
      m_tree->SetBranchStatus("contel_eta",1);
      m_tree->SetBranchStatus("contel_phi",1);
      m_tree->SetBranchStatus("contmu_pt",1);
      m_tree->SetBranchStatus("contmu_eta",1);
      m_tree->SetBranchStatus("contmu_phi",1);
    }

    if(m_currentVariation=="Nominal" && m_isMC){
      m_tree->SetBranchStatus("truth_tau_pt", 1);
      m_tree->SetBranchStatus("truth_tau_eta",1);
      m_tree->SetBranchStatus("truth_tau_phi",1);
      m_tree->SetBranchStatus("truth_tau_status",1);
      m_tree->SetBranchStatus("truth_el_pt",  1);
      m_tree->SetBranchStatus("truth_el_eta", 1);
      m_tree->SetBranchStatus("truth_el_phi", 1);
      m_tree->SetBranchStatus("truth_el_status", 1);
      m_tree->SetBranchStatus("truth_mu_pt",  1);
      m_tree->SetBranchStatus("truth_mu_eta", 1);
      m_tree->SetBranchStatus("truth_mu_phi", 1);
      m_tree->SetBranchStatus("truth_ph_pt",  1);
      m_tree->SetBranchStatus("truth_ph_eta", 1);
      m_tree->SetBranchStatus("truth_ph_phi", 1);
    }
  }

  UInt_t foundGenMET = 0;
  if(m_isMC){
    m_tree->SetBranchStatus("met_truth_et",1);
    m_tree->SetBranchStatus("met_truth_phi",1);
    m_tree->SetBranchStatus("met_truth_sumet",1);
  }
  if(m_currentVariation=="Nominal" && m_isMC){
    m_tree->SetBranchStatus("truth_jet_pt",1);
    m_tree->SetBranchStatus("truth_jet_phi",1);
    m_tree->SetBranchStatus("truth_jet_eta",1);
    m_tree->SetBranchStatus("truth_jet_m",1);
    m_tree->SetBranchStatus("GenMET_pt",1, &foundGenMET);
  }
  m_tree->SetBranchAddress("runNumber", &runNumber);
  m_tree->SetBranchAddress("randomRunNumber", &randomRunNumber);
  m_tree->SetBranchAddress("eventNumber", &eventNumber);
  m_tree->SetBranchAddress("nParton", &nParton);
  m_tree->SetBranchAddress("averageIntPerXing", &averageIntPerXing);
  m_tree->SetBranchAddress("mcEventWeight", &mcEventWeight);
  m_tree->SetBranchAddress("mcEventWeights", &mcEventWeights);
  if(m_currentVariation=="Nominal" && m_isMC){
    m_tree->SetBranchAddress("HTXS_prodMode", &HTXS_prodMode);
    m_tree->SetBranchAddress("HTXS_errorCode", &HTXS_errorCode);
    m_tree->SetBranchAddress("HTXS_Stage1_1_Fine_Category_pTjet25", &HTXS_Stage1_1_Fine_Category_pTjet25);
  }
  m_tree->SetBranchAddress("puWeight", &puWeight);
  m_tree->SetBranchAddress("jvtSFWeight", &jvtSFWeight);
  m_tree->SetBranchAddress("fjvtSFWeight", &fjvtSFWeight);
  m_tree->SetBranchAddress("fjvtSFTighterWeight", &fjvtSFTighterWeight);
  m_tree->SetBranchAddress("eleANTISF", &eleANTISF);
  m_tree->SetBranchAddress("elSFWeight", &elSFWeight);
  m_tree->SetBranchAddress("muSFWeight", &muSFWeight);
  m_tree->SetBranchAddress("elSFTrigWeight", &elSFTrigWeight);
  m_tree->SetBranchAddress("muSFTrigWeight", &muSFTrigWeight);
  m_tree->SetBranchAddress("phSFWeight", &phSFWeight);
  m_tree->SetBranchAddress("trigger_HLT_xe100_mht_L1XE50", &trigger_HLT_xe100_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_HLT_xe110_mht_L1XE50", &trigger_HLT_xe110_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_HLT_xe90_mht_L1XE50", &trigger_HLT_xe90_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_HLT_xe70_mht", &trigger_HLT_xe70_mht);
  m_tree->SetBranchAddress("trigger_HLT_noalg_L1J400", &trigger_HLT_noalg_L1J400);
  m_tree->SetBranchAddress("trigger_lep", &trigger_lep);
  m_tree->SetBranchAddress("lep_trig_match", &lep_trig_match);
  //m_tree->SetBranchAddress("trigger_met", &trigger_met); // just testing being copying directly
  m_tree->SetBranchAddress("trigger_met", &trigger_met_encodedv2);
  m_tree->SetBranchAddress("l1_met_trig_encoded", &l1_met_trig_encoded);
  m_tree->SetBranchAddress("passBatman", &passBatman);
  m_tree->SetBranchAddress("passVjetsFilter", &passVjetsFilter);
  m_tree->SetBranchAddress("passVjetsFilterTauEl", &passVjetsFilterTauEl);
  m_tree->SetBranchAddress("passVjetsPTV", &passVjetsPTV);
  m_tree->SetBranchAddress("MGVTruthPt", &MGVTruthPt);
  m_tree->SetBranchAddress("SherpaVTruthPt", &SherpaVTruthPt);
  m_tree->SetBranchAddress("in_vy_overlap", &in_vy_overlap);
  m_tree->SetBranchAddress("in_vy_overlap_iso", &in_vy_overlap_iso);
  m_tree->SetBranchAddress("FlavourFilter", &FlavourFilter);
  m_tree->SetBranchAddress("passGRL", &passGRL);
  m_tree->SetBranchAddress("passPV", &passPV);
  m_tree->SetBranchAddress("passDetErr", &passDetErr);
  m_tree->SetBranchAddress("n_vx", &n_vx);
  m_tree->SetBranchAddress("passJetCleanLoose", &passJetCleanLoose);
  m_tree->SetBranchAddress("passJetCleanTight", &passJetCleanTight);
  m_tree->SetBranchAddress("n_jet",&n_jet);
  m_tree->SetBranchAddress("n_el",&n_el);
  m_tree->SetBranchAddress("n_mu",&n_mu);
  m_tree->SetBranchAddress("n_el_w",&n_el_w);
  m_tree->SetBranchAddress("n_mu_w",&n_mu_w);

  // variables that are now filled
  m_tree->SetBranchAddress("n_el_baseline",&n_baseel);
  m_tree->SetBranchAddress("n_mu_baseline",&n_basemu);
  m_tree->SetBranchAddress("n_el_baseline_noOR",&n_baseel_noOR);
  m_tree->SetBranchAddress("n_mu_baseline_noOR",&n_basemu_noOR);
  m_tree->SetBranchAddress("n_el_baseline_iso",&n_baseel_iso);
  m_tree->SetBranchAddress("n_mu_baseline_iso",&n_basemu_iso);
  m_tree->SetBranchAddress("n_ph",&n_ph);
  m_tree->SetBranchAddress("n_bjet",            &n_bjet);
  m_tree->SetBranchAddress("lumiBlock",&lumiBlock);
  m_tree->SetBranchAddress("bcid",&bcid);
  m_tree->SetBranchAddress("BCIDDistanceFromFront",&BCIDDistanceFromFront);

  m_tree->SetBranchAddress("jj_mass",&jj_mass);
  m_tree->SetBranchAddress("jj_deta",&jj_deta);
  m_tree->SetBranchAddress("jj_dphi",&jj_dphi);
  m_tree->SetBranchAddress("met_tst_j1_dphi",&met_tst_j1_dphi);
  m_tree->SetBranchAddress("met_tst_j2_dphi",&met_tst_j2_dphi);
  m_tree->SetBranchAddress("met_tst_nolep_j1_dphi",&met_tst_nolep_j1_dphi);
  m_tree->SetBranchAddress("met_tst_nolep_j2_dphi",&met_tst_nolep_j2_dphi);
  m_tree->SetBranchAddress("met_cst_jet",&met_cst_jet);
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
  m_tree->SetBranchAddress("jet_m",&jet_m);
  m_tree->SetBranchAddress("jet_jvt",&jet_jvt);
  m_tree->SetBranchAddress("jet_timing",&jet_timing);
  m_tree->SetBranchAddress("jet_PartonTruthLabelID",&jet_PartonTruthLabelID);
  m_tree->SetBranchAddress("jet_ConeTruthLabelID",&jet_ConeTruthLabelID);
  if(m_currentVariation=="Nominal"){
    m_tree->SetBranchAddress("jet_btag_weight",&jet_btag_weight);
  }
  //if(foundGenMET) m_tree->SetBranchAddress("jet_passJvt",&jet_passJvt);
  if(m_QGTagger){
    m_tree->SetBranchAddress("jet_NTracks",&jet_NTracks);
    m_tree->SetBranchAddress("jet_SumPtTracks",&jet_SumPtTracks);
    m_tree->SetBranchAddress("jet_TrackWidth",&jet_TrackWidth);
    m_tree->SetBranchAddress("jet_TracksC1",&jet_TracksC1);
    m_tree->SetBranchAddress("jet_truthjet_pt",&jet_truthjet_pt);
    m_tree->SetBranchAddress("jet_truthjet_eta",&jet_truthjet_eta);
    m_tree->SetBranchAddress("jet_truthjet_nCharged",&jet_truthjet_nCharged);
    m_tree->SetBranchAddress("jet_HECFrac",&jet_HECFrac);
    m_tree->SetBranchAddress("jet_EMFrac",&jet_EMFrac);
    m_tree->SetBranchAddress("jet_fch",&jet_fch);
  }
  if(m_isMC){
    m_tree->SetBranchAddress("met_truth_et",  &met_truth_et);
    m_tree->SetBranchAddress("met_truth_phi",  &met_truth_phi);
    m_tree->SetBranchAddress("met_truth_sumet",  &met_truth_sumet);
  }
  if(m_isMC && m_currentVariation=="Nominal"){
    m_tree->SetBranchAddress("truth_jet_pt", &truth_jet_pt);
    m_tree->SetBranchAddress("truth_jet_phi",&truth_jet_phi);
    m_tree->SetBranchAddress("truth_jet_eta",&truth_jet_eta);
    m_tree->SetBranchAddress("truth_jet_m",  &truth_jet_m);
    if(foundGenMET) m_tree->SetBranchAddress("GenMET_pt",  &GenMET_pt);
  }

    if(m_currentVariation=="Nominal" && m_contLep){
      m_tree->SetBranchAddress("contel_pt",           &contel_pt);
      m_tree->SetBranchAddress("contel_eta",          &contel_eta);
      m_tree->SetBranchAddress("contel_phi",          &contel_phi);
      m_tree->SetBranchAddress("contmu_pt",           &contmu_pt);
      m_tree->SetBranchAddress("contmu_eta",          &contmu_eta);
      m_tree->SetBranchAddress("contmu_phi",          &contmu_phi);
    }

  if(m_extraVars){
    m_tree->SetBranchAddress("jet_fjvt",            &jet_fjvt);
    m_tree->SetBranchAddress("basemu_pt",           &basemu_pt);
    m_tree->SetBranchAddress("basemu_eta",          &basemu_eta);
    m_tree->SetBranchAddress("basemu_phi",          &basemu_phi);
    m_tree->SetBranchAddress("basemu_charge",          &basemu_charge);
    m_tree->SetBranchAddress("basemu_z0",           &basemu_z0);
    m_tree->SetBranchAddress("basemu_d0sig",        &basemu_d0sig);
    m_tree->SetBranchAddress("basemu_ptvarcone20",  &basemu_ptvarcone20);
    m_tree->SetBranchAddress("basemu_ptvarcone30",  &basemu_ptvarcone30);
    m_tree->SetBranchAddress("basemu_topoetcone20",  &basemu_topoetcone20);
    m_tree->SetBranchAddress("basemu_topoetcone30",  &basemu_topoetcone30);
    m_tree->SetBranchAddress("basemu_type",         &basemu_type);
    if(m_isMC) m_tree->SetBranchAddress("basemu_truthOrigin",  &basemu_truthOrigin);
    if(m_isMC) m_tree->SetBranchAddress("basemu_truthType",    &basemu_truthType);
    m_tree->SetBranchAddress("baseel_pt",           &baseel_pt);
    m_tree->SetBranchAddress("baseel_eta",          &baseel_eta);
    m_tree->SetBranchAddress("baseel_phi",          &baseel_phi);
    m_tree->SetBranchAddress("baseel_charge",          &baseel_charge);
    m_tree->SetBranchAddress("baseel_z0",           &baseel_z0);
    m_tree->SetBranchAddress("baseel_d0sig",           &baseel_d0sig);
    m_tree->SetBranchAddress("baseel_ptvarcone20",  &baseel_ptvarcone20);
    m_tree->SetBranchAddress("baseel_topoetcone20",  &baseel_topoetcone20);
    if(m_isMC) m_tree->SetBranchAddress("baseel_truthOrigin",  &baseel_truthOrigin);
    if(m_isMC) m_tree->SetBranchAddress("baseel_truthType",    &baseel_truthType);

    m_tree->SetBranchAddress("ph_pt",           &ph_pt);
    m_tree->SetBranchAddress("ph_phi",          &ph_phi);
    m_tree->SetBranchAddress("ph_eta",          &ph_eta);
    if(m_currentVariation=="Nominal" && m_isMC){
      m_tree->SetBranchAddress("tau_pt",           &tau_pt);
      m_tree->SetBranchAddress("tau_phi",          &tau_phi);
      m_tree->SetBranchAddress("tau_eta",          &tau_eta);
    }else{ tau_pt=0; tau_phi=0; tau_eta=0; }

    m_tree->SetBranchAddress("met_soft_tst_et",        &met_soft_tst_et);
    m_tree->SetBranchAddress("met_soft_tst_phi",       &met_soft_tst_phi);
    m_tree->SetBranchAddress("met_soft_tst_sumet",     &met_soft_tst_sumet);
    m_tree->SetBranchAddress("met_tenacious_tst_et",   &met_tenacious_tst_et);
    m_tree->SetBranchAddress("met_tenacious_tst_phi",  &met_tenacious_tst_phi);
    m_tree->SetBranchAddress("met_tight_tst_et",       &met_tight_tst_et);
    m_tree->SetBranchAddress("met_tight_tst_phi",      &met_tight_tst_phi);
    m_tree->SetBranchAddress("met_tenacious_tst_nolep_et",   &met_tenacious_tst_nolep_et);
    m_tree->SetBranchAddress("met_tenacious_tst_nolep_phi",  &met_tenacious_tst_nolep_phi);
    m_tree->SetBranchAddress("met_tight_tst_nolep_et",       &met_tight_tst_nolep_et);
    m_tree->SetBranchAddress("met_tight_tst_nolep_phi",      &met_tight_tst_nolep_phi);
    m_tree->SetBranchAddress("metsig_tst",             &metsig_tst);

    if(m_currentVariation=="Nominal" && m_isMC){
      m_tree->SetBranchAddress("truth_tau_pt", &truth_tau_pt);
      m_tree->SetBranchAddress("truth_tau_eta",&truth_tau_eta);
      m_tree->SetBranchAddress("truth_tau_phi",&truth_tau_phi);
      m_tree->SetBranchAddress("truth_tau_status",&truth_tau_status);
      m_tree->SetBranchAddress("truth_el_pt", &truth_el_pt);
      m_tree->SetBranchAddress("truth_el_eta",&truth_el_eta);
      m_tree->SetBranchAddress("truth_el_phi",&truth_el_phi);
      m_tree->SetBranchAddress("truth_el_status",&truth_el_status);
      m_tree->SetBranchAddress("truth_mu_pt", &truth_mu_pt);
      m_tree->SetBranchAddress("truth_mu_eta",&truth_mu_eta);
      m_tree->SetBranchAddress("truth_mu_phi",&truth_mu_phi);
      m_tree->SetBranchAddress("truth_ph_pt", &truth_ph_pt);
      m_tree->SetBranchAddress("truth_ph_eta",&truth_ph_eta);
      m_tree->SetBranchAddress("truth_ph_phi",&truth_ph_phi);
    }
  }

  return StatusCode::SUCCESS;
}

double VBFAnalysisAlg::weightXETrigSF(const float met_pt, unsigned metRunNumber, int syst=0) {
  // 20.7 values
  //static const double p0 = 59.3407;
  //static const double p1 = 54.9134;
  // For MET tight
  //double p0 = 99.4255;
  //double p1 = 38.6145;
  // For MET Tenacious
  double p0 = 99.4255;
  double p1 = 38.6145;
  double e0 = 0.000784094;
  double e1 = 0.05;
  if(metRunNumber<=284484)                        { p0 = 110.396; p1 = 19.4147; e1 = 0.06; }  // 2015 xe70
  if(metRunNumber>284484 && metRunNumber<=302872) { p0 = 111.684; p1 = 19.147;  e1 = 0.08; }  // 2016 xe90
  if(metRunNumber>302872)                         { p0 = 68.8679; p1 = 54.0594; e1 = 0.06; }  // 2016 xe110 //p0 = 101.759; p1 = 36.5069;
  //if(325713<=metRunNumber && metRunNumber<=328393) { p0 = 86.6614; p1 = 49.8935; e1 = 0.05; } // 2017 xe90_pufit_L1XE50
  //if(329385<=metRunNumber && metRunNumber<=330470) { p0 = 103.780; p1 = 57.2547; e1 = 0.05; } // 2017 xe100_pufit_L1XE55
  //if(330857<=metRunNumber && metRunNumber<=331975) { p0 = 118.959; p1 = 32.2808; e1 = 0.05; } // 2017 xe110_pufit_L1XE55
  //if(331975< metRunNumber && metRunNumber<=341649) { p0 = 103.152; p1 = 38.6121; e1 = 0.05; } // 2017 xe110_pufit_L1XE50
  if(325713<=metRunNumber && metRunNumber<=341649) { p0 = 118.959; p1 = 32.2808; e1 = 0.05; } // 2017 xe110_pufit_L1XE55
  //if(350067> metRunNumber && metRunNumber>=348197) { p0 = 104.830; p1 = 38.5267; e1 = 0.05; } // 2018 xe110_xe70_L1XE50
  //if(350067<=metRunNumber && metRunNumber<=364292) { p0 = 107.509; p1 = 32.0065; e1 = 0.05; } // 2018 xe110_xe65_L1XE50
  if(364292>= metRunNumber && metRunNumber>=348197) { p0 = 104.830; p1 = 38.5267; e1 = 0.05; } // 2018 xe110_xe70_L1XE50

  double x = met_pt / 1.0e3;
  if (x < 100) { return 0; }
  if (x > 240) { x = 240; }
  double sf = 0.5*(1+TMath::Erf((x-p0)/(TMath::Sqrt(2)*p1)));
  if(sf<0) sf=0.0;
  if(sf > 1.5) sf=1.5;

  // linear parameterization of the systematics
  if(syst==1){ // up variation
    if(x<210.0) sf+=((e0)*(150-x)+e1)*0.6;
    else sf=1.0;
  }else if(syst==2){ // down
    if(x<210.0)sf-=((e0)*(150-x)+e1)*0.6;
    else sf=1.0;
  }
  return sf;
}

float VBFAnalysisAlg::GetDPhi(const float phi1, const float phi2){
  float dphi = phi1-phi2;
  if ( dphi > M_PI ) {
    dphi -= 2.0*M_PI;
  } else if ( dphi <= -M_PI ) {
    dphi += 2.0*M_PI;
  }
  return dphi;
}
