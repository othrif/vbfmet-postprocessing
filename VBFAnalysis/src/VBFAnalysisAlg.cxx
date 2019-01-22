// VBFAnalysis includes
#include "VBFAnalysisAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
//#include "xAODEventInfo/EventInfo.h"
#include <vector>
#include "TLorentzVector.h"
#include <math.h>       /* exp */


VBFAnalysisAlg::VBFAnalysisAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ),
										      fjvtSFWeight(1.0){
  declareProperty( "currentSample", m_currentSample = "W_strong", "current sample");
  declareProperty( "runNumberInput", m_runNumberInput, "runNumber read from file name");
  declareProperty( "isMC", m_isMC = true, "true if sample is MC" );
  declareProperty( "LooseSkim", m_LooseSkim = true, "true if loose skimming is requested" );
  declareProperty( "ExtraVars", m_extraVars = true, "true if extra variables should be output" );
  declareProperty( "ContLep", m_contLep = false, "true if container lepton variables should be output" );
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
  cout<< "CURRENT  sample === "<< m_currentSample<<endl;

  if(m_isMC){
    std::string xSecFilePath = "dev/PMGTools/PMGxsecDB_mc15.txt";
    //xSecFilePath = "/home/schae/testarea/HInv/source/VBFAnalysis/data/PMGxsecDB_mc16.txt";
    xSecFilePath = PathResolverFindCalibFile(xSecFilePath);
    std::cout << "Cross section: " << xSecFilePath << std::endl;
    my_XsecDB = new SUSY::CrossSectionDB(xSecFilePath);
    // if( (runNumber == 308567 || runNumber == 308276 ) ){
    //   if(truthHiggs_pt->size() > 0) w_VBFhiggs =  -0.000342 * truthHiggs_pt->at(0)/GeV - 0.0708;
    // }else {
    //   w_VBFhiggs =1.;
    // }
  }
  xeSFTrigWeight=1.0;

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
  jet_SumPtTracks = new std::vector<std::vector<float> >(0);
  jet_TrackWidth = new std::vector<float>(0);
  jet_HECFrac = new std::vector<float>(0);
  jet_EMFrac = new std::vector<float>(0);
  jet_fch = new std::vector<float>(0);

  truth_jet_pt= new std::vector<float>(0);
  truth_jet_eta= new std::vector<float>(0);
  truth_jet_phi= new std::vector<float>(0);
  truth_jet_m= new std::vector<float>(0);

  truth_tau_pt= new std::vector<float>(0);
  truth_tau_eta= new std::vector<float>(0);
  truth_tau_phi= new std::vector<float>(0);
  truth_mu_pt= new std::vector<float>(0);
  truth_mu_eta= new std::vector<float>(0);
  truth_mu_phi= new std::vector<float>(0);
  truth_el_pt= new std::vector<float>(0);
  truth_el_eta= new std::vector<float>(0);
  truth_el_phi= new std::vector<float>(0);

  outtau_pt = new std::vector<float>(0);
  outtau_phi = new std::vector<float>(0);
  outtau_eta = new std::vector<float>(0);

  ph_pt = new std::vector<float>(0);
  ph_phi = new std::vector<float>(0);
  ph_eta = new std::vector<float>(0);
  tau_pt = new std::vector<float>(0);
  tau_phi = new std::vector<float>(0);
  tau_eta = new std::vector<float>(0);

  //    if(runNumber >= 276262 && runNumber <= 284484) is2015 =true;
  //    else if(runNumber >= 296939 && runNumber <= 311481) is2016 =true;
  //    else throw std::invalid_argument("runNumber could not be identified with a dataset :o");

  //Create new output TTree
  treeTitleOut = m_currentSample+m_currentVariation;
  treeNameOut = m_currentSample+m_currentVariation;
  m_tree_out = new TTree(treeNameOut.c_str(), treeTitleOut.c_str());
  m_tree_out->Branch("w",&w); 
  m_tree_out->Branch("xeSFTrigWeight",&xeSFTrigWeight); 
  m_tree_out->Branch("eleANTISF",&eleANTISF); 
  m_tree_out->Branch("runNumber",&runNumber);
  m_tree_out->Branch("eventNumber",&eventNumber);
  m_tree_out->Branch("trigger_met", &trigger_met);
  if(m_extraVars) m_tree_out->Branch("trigger_met_encoded", &trigger_met_encoded);
  m_tree_out->Branch("trigger_lep", &trigger_lep);
  m_tree_out->Branch("passJetCleanTight", &passJetCleanTight);
  m_tree_out->Branch("n_jet",&n_jet);
  m_tree_out->Branch("n_el",&n_el);
  m_tree_out->Branch("n_mu",&n_mu);
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

  if(m_contLep){
    m_tree_out->Branch("contmu_pt",           &contmu_pt);
    m_tree_out->Branch("contmu_eta",          &contmu_eta);
    m_tree_out->Branch("contmu_phi",          &contmu_phi);
    m_tree_out->Branch("contel_pt",           &contel_pt);
    m_tree_out->Branch("contel_eta",          &contel_eta);
    m_tree_out->Branch("contel_phi",          &contel_phi);
  }

  if(m_extraVars){

    m_tree_out->Branch("n_bjet",&n_bjet);

    m_tree_out->Branch("j3_centrality",&j3_centrality);
    m_tree_out->Branch("j3_dRj1",&j3_dRj1);
    m_tree_out->Branch("j3_dRj2",&j3_dRj2);
    m_tree_out->Branch("j3_minDR",&j3_minDR);
    m_tree_out->Branch("j3_mjclosest",&j3_mjclosest);
    m_tree_out->Branch("j3_min_mj",&j3_min_mj);
    m_tree_out->Branch("j3_min_mj_over_mjj",&j3_min_mj_over_mjj);
    m_tree_out->Branch("mj34",&mj34);
    m_tree_out->Branch("max_j_eta",&max_j_eta);
    if(m_QGTagger){
      m_tree_out->Branch("jet_NTracks",&jet_NTracks);
      m_tree_out->Branch("jet_SumPtTracks",&jet_SumPtTracks);
      m_tree_out->Branch("jet_TrackWidth",&jet_TrackWidth);
      m_tree_out->Branch("jet_HECFrac",&jet_HECFrac);
      m_tree_out->Branch("jet_EMFrac",&jet_EMFrac);
      m_tree_out->Branch("jet_fch",&jet_fch);
    }
    if(m_isMC) m_tree_out->Branch("jet_PartonTruthLabelID",&jet_PartonTruthLabelID);
    if(m_isMC) m_tree_out->Branch("jet_ConeTruthLabelID",&jet_ConeTruthLabelID);

    m_tree_out->Branch("jet_fjvt",&jet_fjvt);    
    m_tree_out->Branch("basemu_pt",           &basemu_pt);
    m_tree_out->Branch("basemu_eta",          &basemu_eta);
    m_tree_out->Branch("basemu_phi",          &basemu_phi);
    m_tree_out->Branch("basemu_charge",          &basemu_charge);
    m_tree_out->Branch("basemu_z0",           &basemu_z0);
    m_tree_out->Branch("basemu_d0sig",           &basemu_d0sig);
    m_tree_out->Branch("basemu_ptvarcone20",  &basemu_ptvarcone20);
    m_tree_out->Branch("basemu_ptvarcone30",  &basemu_ptvarcone30);
    m_tree_out->Branch("basemu_topoetcone20",  &basemu_topoetcone20);
    m_tree_out->Branch("basemu_topoetcone30",  &basemu_topoetcone30);
    m_tree_out->Branch("basemu_type",         &basemu_type);
    if(m_isMC) m_tree_out->Branch("basemu_truthOrigin",  &basemu_truthOrigin);
    if(m_isMC) m_tree_out->Branch("basemu_truthType",    &basemu_truthType);
    m_tree_out->Branch("baseel_pt",           &baseel_pt);
    m_tree_out->Branch("baseel_eta",          &baseel_eta);
    m_tree_out->Branch("baseel_phi",          &baseel_phi);
    m_tree_out->Branch("baseel_charge",          &baseel_charge);
    m_tree_out->Branch("baseel_z0",           &baseel_z0);
    m_tree_out->Branch("baseel_d0sig",        &baseel_d0sig);
    m_tree_out->Branch("baseel_ptvarcone20",  &baseel_ptvarcone20);
    m_tree_out->Branch("baseel_ptvarcone30",  &baseel_ptvarcone30);
    m_tree_out->Branch("baseel_topoetcone20",  &baseel_topoetcone20);
    m_tree_out->Branch("baseel_topoetcone30",  &baseel_topoetcone30);
    if(m_isMC) m_tree_out->Branch("baseel_truthOrigin",  &baseel_truthOrigin);
    if(m_isMC) m_tree_out->Branch("baseel_truthType",    &baseel_truthType);

    m_tree_out->Branch("ph_pt", &ph_pt);
    m_tree_out->Branch("ph_phi",&ph_phi);
    m_tree_out->Branch("ph_eta",&ph_eta);
    m_tree_out->Branch("tau_pt",&outtau_pt);
    m_tree_out->Branch("tau_phi",&outtau_phi);
    m_tree_out->Branch("tau_eta",&outtau_eta);

    m_tree_out->Branch("met_soft_tst_phi",       &met_soft_tst_phi);
    m_tree_out->Branch("met_soft_tst_sumet",     &met_soft_tst_sumet);
    m_tree_out->Branch("met_tenacious_tst_et",   &met_tenacious_tst_et);
    m_tree_out->Branch("met_tenacious_tst_phi",  &met_tenacious_tst_phi);

    m_tree_out->Branch("met_tenacious_tst_j1_dphi",&met_tenacious_tst_j1_dphi);
    m_tree_out->Branch("met_tenacious_tst_j2_dphi",&met_tenacious_tst_j2_dphi);
    m_tree_out->Branch("met_tenacious_tst_nolep_j1_dphi",&met_tenacious_tst_nolep_j1_dphi);
    m_tree_out->Branch("met_tenacious_tst_nolep_j2_dphi",&met_tenacious_tst_nolep_j2_dphi);
    m_tree_out->Branch("met_tenacious_tst_nolep_et",&met_tenacious_tst_nolep_et);
    m_tree_out->Branch("met_tenacious_tst_nolep_phi",&met_tenacious_tst_nolep_phi);

    m_tree_out->Branch("met_tight_tst_et",       &met_tight_tst_et);
    m_tree_out->Branch("met_tight_tst_phi",      &met_tight_tst_phi);
    m_tree_out->Branch("met_tighter_tst_et",     &met_tighter_tst_et);
    m_tree_out->Branch("met_tighter_tst_phi",    &met_tighter_tst_phi);
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
  }else{
    truth_jet_pt=0; truth_jet_phi=0; truth_jet_eta=0; truth_jet_m=0;
  }
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
  h_Gen = (TH1D*) f->Get("h_total");
  if(!h_Gen)ATH_MSG_WARNING("Number of events not found");

  for(int i=1; i<=h_Gen->GetNbinsX();i++){
    TString tmp = h_Gen->GetXaxis()->GetBinLabel(i);
    int dsid = tmp.Atoi(); 
    double N = h_Gen->GetBinContent(i); 
    Ngen[dsid]=N; 
    //std::cout << "input: " << dsid << " " << N << std::endl;
   }
  
  return StatusCode::SUCCESS; 

}

StatusCode VBFAnalysisAlg::execute() {
  ATH_MSG_DEBUG ("Executing " << name() << "...");

  // check that we don't have too many events
  if(nFileEvt>=nFileEvtTot){
    ATH_MSG_ERROR("VBFAnaysisAlg::execute: Too  many events:  " << nFileEvt << " total evts: " << nFileEvtTot);
    return StatusCode::SUCCESS;
  }

  if(!m_tree) ATH_MSG_ERROR("VBFAnaysisAlg::execute: tree invalid: " <<m_tree );
  m_tree->GetEntry(nFileEvt);

  // iterate event count
  ++nFileEvt;
  if (runNumber != m_runNumberInput){ //HACK to hard set the run number
    ATH_MSG_ERROR("VBFAnaysisAlg::execute: runNumber " << runNumber << " != m_runNumberInput " << m_runNumberInput << " " << jj_dphi << " avg: " << averageIntPerXing);
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
  if(m_isMC && truth_jet_pt && truth_jet_pt->size()>1){
    TLorentzVector tmp, jjtruth;
    tmp.SetPtEtaPhiM(truth_jet_pt->at(0), truth_jet_eta->at(0),truth_jet_phi->at(0),truth_jet_m->at(0));
    jjtruth = tmp;
    tmp.SetPtEtaPhiM(truth_jet_pt->at(1), truth_jet_eta->at(1),truth_jet_phi->at(1),truth_jet_m->at(1));
    jjtruth += tmp;
    truth_jj_mass =jjtruth.M();
  }

  xeSFTrigWeight=1.0;
  if(m_isMC && jet_pt && jet_pt->size()>1){
    TLorentzVector tmp, jj; 
    tmp.SetPtEtaPhiM(jet_pt->at(0), jet_eta->at(0),jet_phi->at(0),jet_m->at(0));    
    jj=tmp;
    tmp.SetPtEtaPhiM(jet_pt->at(1), jet_eta->at(1),jet_phi->at(1),jet_m->at(1));    
    jj+=tmp;
    xeSFTrigWeight = weightXETrigSF(met_tst_et); // met was used in the end instead of jj.Pt()
  }

  if (m_isMC){
    // hack for when the cross-section code messed up
    //if(runNumber==410011) crossSection =  43.739*1.00944237408;
    //else if (runNumber==410012)  crossSection =  25.778*1.01931879898;
    //else if (runNumber==410013)  crossSection =  34.009*1.054;
    //else if (runNumber==410014)  crossSection =  33.989*1.054;
    //else if (runNumber==410025)  crossSection =  2.0514*1.00478210003;
    //else if (runNumber==410026)  crossSection =  1.2615*1.02153151011;
    //else if (runNumber==410470)  crossSection =  729.77*0.54384*1.13975636159;
    //else if (runNumber==410471)  crossSection =  729.78*0.45627*1.13974074379;
    //else if (runNumber==410472)  crossSection =  729.77*0.10546*1.13975636159;
    //else 
    crossSection = my_XsecDB->xsectTimesEff(runNumber);//xs in pb 
    //std::cout << "crossSection: " << crossSection << std::endl;
    if(Ngen[runNumber]>0)  weight = crossSection/Ngen[runNumber]; 
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

  // Definiing a loose skimming
  float METCut = 180.0e3;
  float LeadJetPtCut = 80.0e3;
  float subLeadJetPtCut = 50.0e3;
  float MjjCut =2e5;
  float DEtajjCut =4.8;

  if(m_LooseSkim){
    METCut = 140.0e3;
    LeadJetPtCut = 60.0e3; // 60.0e3
    subLeadJetPtCut = 40.0e3; // 40.0e3
    MjjCut =2e5; // 2e5
    DEtajjCut =3.5; // 3.5
  }

  if (!((passGRL == 1) & (passPV == 1) & (passDetErr == 1) & (passJetCleanLoose == 1))) return StatusCode::SUCCESS;
  //if (!((passGRL == 1) & (passPV == 1) & (passDetErr == 1) )) return StatusCode::SUCCESS;
  ATH_MSG_DEBUG ("Pass GRL, PV, DetErr, JetCleanLoose");
  if (n_jet < 2) return StatusCode::SUCCESS;
  if (!(n_jet == 2) && !m_LooseSkim) return StatusCode::SUCCESS;
  ATH_MSG_DEBUG ("n_jet = 2!");
  if (!(n_jet == jet_pt->size())) ATH_MSG_WARNING("n_jet != jet_pt->size()! n_jet: " <<n_jet << " jet_pt->size(): " << jet_pt->size());
  if (!(n_jet == jet_eta->size())) ATH_MSG_WARNING("n_jet != jet_eta->size()! n_jet: " <<n_jet << " jet_eta->size(): " << jet_eta->size());
  if (!((jet_pt->at(0) > LeadJetPtCut) & (jet_pt->at(1) > subLeadJetPtCut) & (jj_dphi < 1.8) & (jj_deta > DEtajjCut) & ((jet_eta->at(0) * jet_eta->at(1))<0) & (jj_mass > MjjCut))) return StatusCode::SUCCESS; // was 1e6 for mjj
  ATH_MSG_DEBUG ("Pass VBF cuts!");
  // encoding met triggers
  trigger_met_encoded=0;
  if (trigger_HLT_xe100_mht_L1XE50 == 1) trigger_met_encoded+=0x1;
  if (trigger_HLT_xe110_mht_L1XE50 == 1) trigger_met_encoded+=0x2;
  if (trigger_HLT_xe90_mht_L1XE50 == 1)  trigger_met_encoded+=0x4;
  if (trigger_HLT_xe70_mht == 1)         trigger_met_encoded+=0x8;
  if (trigger_HLT_noalg_L1J400 == 1)     trigger_met_encoded+=0x10;

  if (trigger_HLT_xe100_mht_L1XE50 == 1 || trigger_HLT_xe110_mht_L1XE50 == 1 || trigger_HLT_xe90_mht_L1XE50 == 1) trigger_met = 1; else trigger_met = 0;
  ATH_MSG_DEBUG ("Assign trigger_met value");
  if(n_el== 1) {
    //met_significance = met_tst_et/1000/sqrt(sqrt(el_pt->at(0)*el_pt->at(0)*cos(el_phi->at(0))*cos(el_phi->at(0))+el_pt->at(0)*el_pt->at(0)*sin(el_phi->at(0))*sin(el_phi->at(0)))+sqrt(jet_pt->at(0)*jet_pt->at(0)*sin(jet_phi->at(0))*sin(jet_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*cos(jet_phi->at(0))*cos(jet_phi->at(0)))+sqrt(jet_pt->at(1)*jet_pt->at(1)*sin(jet_phi->at(1))*sin(jet_phi->at(1))+jet_pt->at(1)*jet_pt->at(1)*cos(jet_phi->at(1))*cos(jet_phi->at(1)))/1000);
    met_significance = met_tst_et/1000/sqrt((el_pt->at(0) + jet_pt->at(0) + jet_pt->at(1))/1000.);
  } else {
    met_significance = 0;
  }
  ATH_MSG_DEBUG ("met_significance calculated");
  
  if(!m_LooseSkim){
    if ((trigger_met == 1) & (met_tst_et > METCut) & (met_tst_j1_dphi>1.0) & (met_tst_j2_dphi>1.0) & (n_el == 0) & (n_mu == 0)) SR = true;
  }else{
    if ((trigger_met == 1) & (met_tst_et > METCut || met_tenacious_tst_et > METCut || met_tight_tst_et > METCut || met_tighter_tst_et > METCut) & (n_el == 0) & (n_mu == 0)) SR = true;
  }
  if (SR) ATH_MSG_DEBUG ("It's SR!"); else ATH_MSG_DEBUG ("It's NOT SR");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance > 4.0)) CRWep = true;}
  if (CRWep) ATH_MSG_DEBUG ("It's CRWep!"); else ATH_MSG_DEBUG ("It's NOT CRWep");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance > 4.0)) CRWen = true;}
  if (CRWen) ATH_MSG_DEBUG ("It's CRWen!"); else ATH_MSG_DEBUG ("It's NOT CRWen");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance <= 4.0)) CRWepLowSig = true;}
  if (CRWepLowSig) ATH_MSG_DEBUG ("It's CRWepLowSig!"); else ATH_MSG_DEBUG ("It's NOT CRWepLowSig");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance <= 4.0)) CRWenLowSig = true;}
  if (CRWenLowSig) ATH_MSG_DEBUG ("It's CRWenLowSig!"); else ATH_MSG_DEBUG ("It's NOT CRWenLowSig");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) > 0)) CRWmp = true;}
  if (CRWmp) ATH_MSG_DEBUG ("It's CRWmp!"); else ATH_MSG_DEBUG ("It's NOT CRWmp");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) < 0)) CRWmn = true;}
  if (CRWmn) ATH_MSG_DEBUG ("It's CRWmn!"); else ATH_MSG_DEBUG ("It's NOT CRWmn");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 2) & (n_mu == 0)){ if ((el_charge->at(0)*el_charge->at(1) < 0)) CRZee = true;}
  if (CRZee) ATH_MSG_DEBUG ("It's CRZee!"); else ATH_MSG_DEBUG ("It's NOT CRZee");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 2)){ if ((mu_charge->at(0)*mu_charge->at(1) < 0)) CRZmm = true;}
  if (CRZmm) ATH_MSG_DEBUG ("It's CRZmm!"); else ATH_MSG_DEBUG ("It's NOT CRZmm");
  if ((trigger_lep > 0) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_baseel+n_basemu>=2)){ CRZtt = true;}
  if (CRZtt) ATH_MSG_DEBUG ("It's CRZtt!"); else ATH_MSG_DEBUG ("It's NOT CRZtt");

  w = weight*mcEventWeight*puWeight*fjvtSFWeight*jvtSFWeight*elSFWeight*muSFWeight*elSFTrigWeight*muSFTrigWeight*eleANTISF;
  //
  /// compute the systematics weights
  //
  float tmp_puWeight = puWeight;
  float tmp_jvtSFWeight = jvtSFWeight;
  float tmp_fjvtSFWeight = fjvtSFWeight;
  float tmp_elSFWeight = elSFWeight;
  float tmp_muSFWeight = muSFWeight;
  float tmp_elSFTrigWeight = elSFTrigWeight;
  float tmp_muSFTrigWeight = muSFTrigWeight;
  float tmp_eleANTISF = eleANTISF;

  for(std::map<TString,Float_t>::iterator it=tMapFloat.begin(); it!=tMapFloat.end(); ++it){
    // initialize
    tmp_puWeight = puWeight;	    
    tmp_jvtSFWeight = jvtSFWeight;	    
    tmp_fjvtSFWeight = fjvtSFWeight;    
    tmp_elSFWeight = elSFWeight;	    
    tmp_muSFWeight = muSFWeight;	    
    tmp_elSFTrigWeight = elSFTrigWeight;
    tmp_muSFTrigWeight = muSFTrigWeight;
    tmp_eleANTISF = eleANTISF;

    if(it->first.Contains("jvtSFWeight"))         tmp_jvtSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("fjvtSFWeight"))   tmp_fjvtSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("puWeight"))       tmp_puWeight=tMapFloat[it->first];
    else if(it->first.Contains("elSFWeight"))     tmp_elSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("muSFWeight"))     tmp_muSFWeight=tMapFloat[it->first];
    else if(it->first.Contains("elSFTrigWeight")) tmp_elSFTrigWeight=tMapFloat[it->first];
    else if(it->first.Contains("muSFTrigWeight")) tmp_muSFTrigWeight=tMapFloat[it->first];
    else if(it->first.Contains("eleANTISF"))      tmp_eleANTISF=tMapFloat[it->first];

    ATH_MSG_DEBUG("VBFAnalysisAlg: " << it->first << " weight: " << weight << " mcEventWeight: " << mcEventWeight << " puWeight: " << tmp_puWeight << " jvtSFWeight: " << tmp_jvtSFWeight << " elSFWeight: " << tmp_elSFWeight << " muSFWeight: " << tmp_muSFWeight << " elSFTrigWeight: " << tmp_elSFTrigWeight << " muSFTrigWeight: " << tmp_muSFTrigWeight << " eleANTISF: " << tmp_eleANTISF);

    tMapFloatW[it->first]=weight*mcEventWeight*tmp_puWeight*tmp_jvtSFWeight*tmp_fjvtSFWeight*tmp_elSFWeight*tmp_muSFWeight*tmp_elSFTrigWeight*tmp_muSFTrigWeight*tmp_eleANTISF;
  }//end systematic weight loop

  ATH_MSG_DEBUG("VBFAnalysisAlg: weight: " << weight << " mcEventWeight: " << mcEventWeight << " puWeight: " << puWeight << " jvtSFWeight: " << jvtSFWeight << " elSFWeight: " << elSFWeight << " muSFWeight: " << muSFWeight << " elSFTrigWeight: " << elSFTrigWeight << " muSFTrigWeight: " << muSFTrigWeight << " eleANTISF: " << eleANTISF);
  // only save events that pass any of the regions
  if (!(SR || CRWep || CRWen || CRWepLowSig || CRWenLowSig || CRWmp || CRWmn || CRZee || CRZmm || CRZtt)) return StatusCode::SUCCESS;
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
  e_met_j1_dphi          = TVector2::Phi_mpi_pi(met_phi-jet_phi->at(0));
  e_met_j2_dphi          = TVector2::Phi_mpi_pi(met_phi-jet_phi->at(1));
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

  m_tree->SetBranchStatus("runNumber", 1);
  m_tree->SetBranchStatus("eventNumber", 1);
  m_tree->SetBranchStatus("averageIntPerXing", 1);
  m_tree->SetBranchStatus("mcEventWeight", 1);
  m_tree->SetBranchStatus("puWeight", 1);
  m_tree->SetBranchStatus("jvtSFWeight", 1);
  m_tree->SetBranchStatus("fjvtSFWeight", 1);
  m_tree->SetBranchStatus("eleANTISF", 1);
  m_tree->SetBranchStatus("elSFWeight", 1);
  m_tree->SetBranchStatus("muSFWeight", 1);
  m_tree->SetBranchStatus("elSFTrigWeight", 1);
  m_tree->SetBranchStatus("muSFTrigWeight", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe100_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe110_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe90_mht_L1XE50", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe70_mht", 1);
  m_tree->SetBranchStatus("trigger_HLT_noalg_L1J400", 1);
  m_tree->SetBranchStatus("trigger_lep", 1);
  m_tree->SetBranchStatus("passGRL", 1);
  m_tree->SetBranchStatus("passPV", 1);
  m_tree->SetBranchStatus("passDetErr", 1);
  m_tree->SetBranchStatus("passJetCleanLoose", 1);
  m_tree->SetBranchStatus("passJetCleanTight", 1);
  m_tree->SetBranchStatus("n_jet",1);
  m_tree->SetBranchStatus("n_el",1);
  m_tree->SetBranchStatus("n_mu",1);
  m_tree->SetBranchStatus("n_ph",1);
  m_tree->SetBranchStatus("n_el_baseline",1);
  m_tree->SetBranchStatus("n_mu_baseline",1);
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
  m_tree->SetBranchStatus("jet_PartonTruthLabelID",1);
  m_tree->SetBranchStatus("jet_ConeTruthLabelID",1);
  if(m_QGTagger){
    m_tree->SetBranchStatus("jet_NTracks",1);
    m_tree->SetBranchStatus("jet_SumPtTracks",1);
    m_tree->SetBranchStatus("jet_TrackWidth",1);
    m_tree->SetBranchStatus("jet_HECFrac",1);
    m_tree->SetBranchStatus("jet_EMFrac",1);
    m_tree->SetBranchStatus("jet_fch",1);
  }

  if(m_extraVars){
    m_tree->SetBranchStatus("n_bjet",1);

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
    m_tree->SetBranchStatus("baseel_ptvarcone30",1);
    m_tree->SetBranchStatus("baseel_topoetcone20",1);
    m_tree->SetBranchStatus("baseel_topoetcone30",1);
    if(m_isMC) m_tree->SetBranchStatus("baseel_truthOrigin",1);
    if(m_isMC) m_tree->SetBranchStatus("baseel_truthType",1);
    m_tree->SetBranchStatus("met_soft_tst_et",1);
    m_tree->SetBranchStatus("met_soft_tst_phi",1);
    m_tree->SetBranchStatus("met_soft_tst_sumet",1);
    m_tree->SetBranchStatus("met_tenacious_tst_et",1);
    m_tree->SetBranchStatus("met_tenacious_tst_phi",1);
    m_tree->SetBranchStatus("met_tight_tst_et",1);
    m_tree->SetBranchStatus("met_tight_tst_phi",1);
    m_tree->SetBranchStatus("met_tighter_tst_et",1);
    m_tree->SetBranchStatus("met_tighter_tst_phi",1);
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
      m_tree->SetBranchStatus("truth_el_pt",  1);
      m_tree->SetBranchStatus("truth_el_eta", 1);
      m_tree->SetBranchStatus("truth_el_phi", 1);
      m_tree->SetBranchStatus("truth_mu_pt",  1);
      m_tree->SetBranchStatus("truth_mu_eta", 1);
      m_tree->SetBranchStatus("truth_mu_phi", 1);
    }
  }

  UInt_t foundGenMET = 0;
  if(m_currentVariation=="Nominal" && m_isMC){
    m_tree->SetBranchStatus("truth_jet_pt",1);
    m_tree->SetBranchStatus("truth_jet_phi",1);
    m_tree->SetBranchStatus("truth_jet_eta",1);
    m_tree->SetBranchStatus("truth_jet_m",1);
    m_tree->SetBranchStatus("met_truth_et",1);
    m_tree->SetBranchStatus("met_truth_phi",1);
    m_tree->SetBranchStatus("met_truth_sumet",1);
    m_tree->SetBranchStatus("GenMET_pt",1, &foundGenMET);
    //m_tree->SetBranchStatus("GenMET_pt",1);
  }
  //if(foundGenMET) m_tree->SetBranchStatus("jet_passJvt",1);

  m_tree->SetBranchAddress("runNumber", &runNumber);
  m_tree->SetBranchAddress("eventNumber", &eventNumber);
  m_tree->SetBranchAddress("averageIntPerXing", &averageIntPerXing);
  m_tree->SetBranchAddress("mcEventWeight", &mcEventWeight);
  m_tree->SetBranchAddress("puWeight", &puWeight);
  m_tree->SetBranchAddress("jvtSFWeight", &jvtSFWeight);
  m_tree->SetBranchAddress("fjvtSFWeight", &fjvtSFWeight);
  m_tree->SetBranchAddress("eleANTISF", &eleANTISF);
  m_tree->SetBranchAddress("elSFWeight", &elSFWeight);
  m_tree->SetBranchAddress("muSFWeight", &muSFWeight);
  m_tree->SetBranchAddress("elSFTrigWeight", &elSFTrigWeight);
  m_tree->SetBranchAddress("muSFTrigWeight", &muSFTrigWeight);
  m_tree->SetBranchAddress("trigger_HLT_xe100_mht_L1XE50", &trigger_HLT_xe100_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_HLT_xe110_mht_L1XE50", &trigger_HLT_xe110_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_HLT_xe90_mht_L1XE50", &trigger_HLT_xe90_mht_L1XE50);
  m_tree->SetBranchAddress("trigger_HLT_xe70_mht", &trigger_HLT_xe70_mht);
  m_tree->SetBranchAddress("trigger_HLT_noalg_L1J400", &trigger_HLT_noalg_L1J400);
  m_tree->SetBranchAddress("trigger_lep", &trigger_lep);
  m_tree->SetBranchAddress("passGRL", &passGRL);
  m_tree->SetBranchAddress("passPV", &passPV);
  m_tree->SetBranchAddress("passDetErr", &passDetErr);
  m_tree->SetBranchAddress("passJetCleanLoose", &passJetCleanLoose);
  m_tree->SetBranchAddress("passJetCleanTight", &passJetCleanTight);
  m_tree->SetBranchAddress("n_jet",&n_jet);
  m_tree->SetBranchAddress("n_el",&n_el);
  m_tree->SetBranchAddress("n_mu",&n_mu);

  // variables that are now filled
  m_tree->SetBranchAddress("n_el_baseline",&n_baseel);
  m_tree->SetBranchAddress("n_mu_baseline",&n_basemu);
  m_tree->SetBranchAddress("n_ph",&n_ph);

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
  //if(foundGenMET) m_tree->SetBranchAddress("jet_passJvt",&jet_passJvt);
  if(m_QGTagger){
    m_tree->SetBranchAddress("jet_NTracks",&jet_NTracks);
    m_tree->SetBranchAddress("jet_SumPtTracks",&jet_SumPtTracks);
    m_tree->SetBranchAddress("jet_TrackWidth",&jet_TrackWidth);
    m_tree->SetBranchAddress("jet_HECFrac",&jet_HECFrac);
    m_tree->SetBranchAddress("jet_EMFrac",&jet_EMFrac);
    m_tree->SetBranchAddress("jet_fch",&jet_fch);
  }
  if(m_currentVariation=="Nominal" && m_isMC){
    m_tree->SetBranchAddress("truth_jet_pt", &truth_jet_pt);
    m_tree->SetBranchAddress("truth_jet_phi",&truth_jet_phi);
    m_tree->SetBranchAddress("truth_jet_eta",&truth_jet_eta);
    m_tree->SetBranchAddress("truth_jet_m",  &truth_jet_m);
    m_tree->SetBranchAddress("met_truth_et",  &met_truth_et);
    m_tree->SetBranchAddress("met_truth_phi",  &met_truth_phi);
    m_tree->SetBranchAddress("met_truth_sumet",  &met_truth_sumet);
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
  
    m_tree->SetBranchAddress("n_bjet",            &n_bjet);

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
    m_tree->SetBranchAddress("baseel_ptvarcone30",  &baseel_ptvarcone30);
    m_tree->SetBranchAddress("baseel_topoetcone20",  &baseel_topoetcone20);
    m_tree->SetBranchAddress("baseel_topoetcone30",  &baseel_topoetcone30);
    if(m_isMC) m_tree->SetBranchAddress("baseel_truthOrigin",  &baseel_truthOrigin);
    if(m_isMC) m_tree->SetBranchAddress("baseel_truthType",    &baseel_truthType);
    
    m_tree->SetBranchAddress("ph_pt",           &ph_pt);
    m_tree->SetBranchAddress("ph_phi",          &ph_phi);
    m_tree->SetBranchAddress("ph_eta",          &ph_eta);
    m_tree->SetBranchAddress("tau_pt",           &tau_pt);
    m_tree->SetBranchAddress("tau_phi",          &tau_phi);
    m_tree->SetBranchAddress("tau_eta",          &tau_eta);
    
    m_tree->SetBranchAddress("met_soft_tst_et",        &met_soft_tst_et);
    m_tree->SetBranchAddress("met_soft_tst_phi",       &met_soft_tst_phi);
    m_tree->SetBranchAddress("met_soft_tst_sumet",     &met_soft_tst_sumet);
    m_tree->SetBranchAddress("met_tenacious_tst_et",   &met_tenacious_tst_et);
    m_tree->SetBranchAddress("met_tenacious_tst_phi",  &met_tenacious_tst_phi);
    m_tree->SetBranchAddress("met_tight_tst_et",       &met_tight_tst_et);
    m_tree->SetBranchAddress("met_tight_tst_phi",      &met_tight_tst_phi);
    m_tree->SetBranchAddress("met_tighter_tst_et",     &met_tighter_tst_et);
    m_tree->SetBranchAddress("met_tighter_tst_phi",    &met_tighter_tst_phi);
    m_tree->SetBranchAddress("metsig_tst",             &metsig_tst);
  
    if(m_currentVariation=="Nominal" && m_isMC){
      m_tree->SetBranchAddress("truth_tau_pt", &truth_tau_pt);
      m_tree->SetBranchAddress("truth_tau_eta",&truth_tau_eta);
      m_tree->SetBranchAddress("truth_tau_phi",&truth_tau_phi);
      m_tree->SetBranchAddress("truth_el_pt", &truth_el_pt);
      m_tree->SetBranchAddress("truth_el_eta",&truth_el_eta);
      m_tree->SetBranchAddress("truth_el_phi",&truth_el_phi);
      m_tree->SetBranchAddress("truth_mu_pt", &truth_mu_pt);
      m_tree->SetBranchAddress("truth_mu_eta",&truth_mu_eta);
      m_tree->SetBranchAddress("truth_mu_phi",&truth_mu_phi);
    }
  }

  return StatusCode::SUCCESS;
}

double VBFAnalysisAlg::weightXETrigSF(const float jj_pt) {
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
