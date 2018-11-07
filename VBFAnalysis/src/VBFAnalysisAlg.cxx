// VBFAnalysis includes
#include "VBFAnalysisAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
//#include "xAODEventInfo/EventInfo.h"
#include <vector>
#include "TLorentzVector.h"


VBFAnalysisAlg::VBFAnalysisAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty( "currentSample", m_currentSample = "W_strong", "current sample");
  declareProperty( "runNumberInput", m_runNumberInput, "runNumber read from file name");
  declareProperty( "isMC", m_isMC = true, "true if sample is MC" );
  declareProperty( "LooseSkim", m_LooseSkim = true, "true if loose skimming is requested" );
  declareProperty( "ExtraVars", m_extraVars = true, "true if extra variables should be output" );
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

  basemu_pt= new std::vector<float>(0);
  basemu_eta= new std::vector<float>(0);
  basemu_phi= new std::vector<float>(0);
  basemu_z0= new std::vector<float>(0);
  basemu_ptvarcone20= new std::vector<float>(0);
  basemu_type= new std::vector<int>(0);
  basemu_truthType= new std::vector<int>(0);
  basemu_truthOrigin= new std::vector<int>(0);

  baseel_pt= new std::vector<float>(0);
  baseel_eta= new std::vector<float>(0);
  baseel_phi= new std::vector<float>(0);
  baseel_z0= new std::vector<float>(0);
  baseel_ptvarcone20= new std::vector<float>(0);
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

  outph_pt = new std::vector<float>(0);
  outph_phi = new std::vector<float>(0);
  outph_eta = new std::vector<float>(0);
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
  m_tree_out->Branch("runNumber",&runNumber);
  m_tree_out->Branch("eventNumber",&eventNumber);
  m_tree_out->Branch("trigger_met", &trigger_met);
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
  m_tree_out->Branch("met_cst_jet",&met_cst_jet);
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
  m_tree_out->Branch("jet_m",&jet_m);
  m_tree_out->Branch("jet_jvt",&jet_jvt);
  m_tree_out->Branch("met_significance",&met_significance);

  if(m_extraVars){
    m_tree_out->Branch("jet_fjvt",&jet_fjvt);    
    m_tree_out->Branch("basemu_pt",           &basemu_pt);
    m_tree_out->Branch("basemu_eta",          &basemu_eta);
    m_tree_out->Branch("basemu_phi",          &basemu_phi);
    m_tree_out->Branch("basemu_z0",           &basemu_z0);
    m_tree_out->Branch("basemu_ptvarcone20",  &basemu_ptvarcone20);
    m_tree_out->Branch("basemu_type",         &basemu_type);
    if(m_isMC) m_tree_out->Branch("basemu_truthOrigin",  &basemu_truthOrigin);
    if(m_isMC) m_tree_out->Branch("basemu_truthType",    &basemu_truthType);
    m_tree_out->Branch("baseel_pt",           &baseel_pt);
    m_tree_out->Branch("baseel_eta",          &baseel_eta);
    m_tree_out->Branch("baseel_phi",          &baseel_phi);
    m_tree_out->Branch("baseel_z0",           &baseel_z0);
    m_tree_out->Branch("baseel_ptvarcone20",  &baseel_ptvarcone20);
    if(m_isMC) m_tree_out->Branch("baseel_truthOrigin",  &baseel_truthOrigin);
    if(m_isMC) m_tree_out->Branch("baseel_truthType",    &baseel_truthType);

    m_tree_out->Branch("ph_pt", &outph_pt);
    m_tree_out->Branch("ph_phi",&outph_phi);
    m_tree_out->Branch("ph_eta",&outph_eta);
    m_tree_out->Branch("tau_pt",&outtau_pt);
    m_tree_out->Branch("tau_phi",&outtau_phi);
    m_tree_out->Branch("tau_eta",&outtau_eta);

    m_tree_out->Branch("met_soft_tst_et",        &met_soft_tst_et);
    m_tree_out->Branch("met_soft_tst_phi",       &met_soft_tst_phi);
    m_tree_out->Branch("met_soft_tst_sumet",     &met_soft_tst_sumet);
    m_tree_out->Branch("met_tenacious_tst_et",   &met_tenacious_tst_et);
    m_tree_out->Branch("met_tenacious_tst_phi",  &met_tenacious_tst_phi);
    m_tree_out->Branch("met_tight_tst_et",       &met_tight_tst_et);
    m_tree_out->Branch("met_tight_tst_phi",      &met_tight_tst_phi);
    m_tree_out->Branch("met_tighter_tst_et",     &met_tighter_tst_et);
    m_tree_out->Branch("met_tighter_tst_phi",    &met_tighter_tst_phi);
    m_tree_out->Branch("metsig_tst",             &metsig_tst);

    m_tree_out->Branch("n_baseel",&n_baseel);
    m_tree_out->Branch("n_basemu",&n_basemu);

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
  h_Gen = (TH1F*) f->Get("h_total");
  if(!h_Gen)ATH_MSG_WARNING("Number of events not found");

  for(int i=1; i<=h_Gen->GetNbinsX();i++){
    TString tmp = h_Gen->GetXaxis()->GetBinLabel(i);
    int dsid = tmp.Atoi(); 
    float N = h_Gen->GetBinContent(i); 
    Ngen[dsid]=N; 
    //std::cout << "input: " << dsid << " " << N << std::endl;
   }
  
  return StatusCode::SUCCESS; 

}

StatusCode VBFAnalysisAlg::execute() {
  ATH_MSG_DEBUG ("Executing " << name() << "...");
  //setFilterPassed(false); //optional: start with algorithm not passed
  //m_tree->GetEntry(m_tree->GetReadEntry());

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

  if (m_isMC){
    crossSection = my_XsecDB->xsectTimesEff(runNumber);//xs in pb 
    if(Ngen[runNumber]>0)  weight = crossSection/Ngen[runNumber]; 
    else ATH_MSG_WARNING("Ngen " << Ngen[runNumber] << " dsid " << runNumber ); 
    ATH_MSG_DEBUG("VBFAnalysisAlg: xs: "<< crossSection << " nevent: " << Ngen[runNumber] );
  } else {
    weight = 1;
  }

  // base lepton selection
  n_baseel=0;
  n_basemu=0;
  n_ph=0;
  n_tau=0;
  outph_pt->clear();
  outph_eta->clear();
  outph_phi->clear();
  outtau_pt->clear();
  outtau_eta->clear();
  outtau_phi->clear();
  if(m_extraVars){
    if(baseel_pt){
      for(unsigned iEle=0; iEle<baseel_pt->size(); ++iEle){
	if(baseel_pt->at(iEle)>4.5e3 && baseel_ptvarcone20->at(iEle)/baseel_pt->at(iEle)<0.25) ++n_baseel;
      }
    }
    if(basemu_pt){
      for(unsigned iMuo=0; iMuo<basemu_pt->size(); ++iMuo){
	if(basemu_pt->at(iMuo)>4.0e3 && basemu_ptvarcone20->at(iMuo)/basemu_pt->at(iMuo)<0.25) ++n_basemu;
      }
    }
    // overlap remove with the photons
    if(ph_pt){
      TVector3 phvec,tmp;
      for(unsigned iPh=0; iPh<ph_pt->size(); ++iPh){
	bool passOR=true;
	phvec.SetPtEtaPhi(ph_pt->at(iPh),ph_eta->at(iPh),ph_phi->at(iPh));
	if(baseel_pt){
	  for(unsigned iEle=0; iEle<baseel_pt->size(); ++iEle){
	    if(baseel_pt->at(iEle)>4.5e3 && baseel_ptvarcone20->at(iEle)/baseel_pt->at(iEle)<0.25){
	      tmp.SetPtEtaPhi(baseel_pt->at(iEle),baseel_eta->at(iEle),baseel_phi->at(iEle));
	      if(phvec.DeltaR(tmp)<0.2) passOR=false;
	    }
	  }
	}
	if(basemu_pt){
	  for(unsigned iMuo=0; iMuo<basemu_pt->size(); ++iMuo){
	    if(basemu_pt->at(iMuo)>4.0e3 && basemu_ptvarcone20->at(iMuo)/basemu_pt->at(iMuo)<0.25){
	      tmp.SetPtEtaPhi(basemu_pt->at(iMuo),basemu_eta->at(iMuo),basemu_phi->at(iMuo));
	      if(phvec.DeltaR(tmp)<0.2) passOR=false;  
	    }
	  }
	}// end base muon overlap
	if(passOR){
	  ++n_ph;
	  outph_pt->push_back(ph_pt->at(iPh));
	  outph_eta->push_back(ph_eta->at(iPh));
	  outph_phi->push_back(ph_phi->at(iPh));
	}
      }// end photon loop
    }// end photon overlap removal

    // overlap remove with the photons
    if(tau_pt){
      TVector3 tauvec,tmp;
      for(unsigned iTau=0; iTau<tau_pt->size(); ++iTau){
	bool passOR=true;
	tauvec.SetPtEtaPhi(tau_pt->at(iTau),tau_eta->at(iTau),tau_phi->at(iTau));
	if(baseel_pt){
	  for(unsigned iEle=0; iEle<baseel_pt->size(); ++iEle){
	    if(baseel_pt->at(iEle)>4.5e3 && baseel_ptvarcone20->at(iEle)/baseel_pt->at(iEle)<0.25){
	      tmp.SetPtEtaPhi(baseel_pt->at(iEle),baseel_eta->at(iEle),baseel_phi->at(iEle));
	      if(tauvec.DeltaR(tmp)<0.2) passOR=false;
	    }
	  }
	}
	if(basemu_pt){
	  for(unsigned iMuo=0; iMuo<basemu_pt->size(); ++iMuo){
	    if(basemu_pt->at(iMuo)>4.0e3 && basemu_ptvarcone20->at(iMuo)/basemu_pt->at(iMuo)<0.25){
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

  // Definiing a loose skimming
  float METCut = 180.0e3;
  float LeadJetPtCut = 80.0e3;
  float subLeadJetPtCut = 50.0e3;
  float MjjCut =2e5;
  float DEtajjCut =4.8;

  if(m_LooseSkim){
    METCut = 140.0e3;
    LeadJetPtCut = 60.0e3;
    subLeadJetPtCut = 40.0e3;
    MjjCut =2e5;
    DEtajjCut =3.5;
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
  if (trigger_HLT_xe100_mht_L1XE50 == 1 || trigger_HLT_xe110_mht_L1XE50 == 1 || trigger_HLT_xe90_mht_L1XE50 == 1) trigger_met = 1; else trigger_met = 0;
  ATH_MSG_DEBUG ("Assign trigger_met value");
  if(n_el== 1) {
    met_significance = met_tst_et/1000/sqrt(sqrt(el_pt->at(0)*el_pt->at(0)*cos(el_phi->at(0))*cos(el_phi->at(0))+el_pt->at(0)*el_pt->at(0)*sin(el_phi->at(0))*sin(el_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*sin(jet_phi->at(0))*sin(jet_phi->at(0))+jet_pt->at(0)*jet_pt->at(0)*cos(jet_phi->at(0))*cos(jet_phi->at(0))+jet_pt->at(1)*jet_pt->at(1)*sin(jet_phi->at(1))*sin(jet_phi->at(1))+jet_pt->at(1)*jet_pt->at(1)*cos(jet_phi->at(1))*cos(jet_phi->at(1)))/1000);
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
  if ((trigger_lep == 1) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance > 4.0)) CRWep = true;}
  if (CRWep) ATH_MSG_DEBUG ("It's CRWep!"); else ATH_MSG_DEBUG ("It's NOT CRWep");
  if ((trigger_lep == 1) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance > 4.0)) CRWen = true;}
  if (CRWen) ATH_MSG_DEBUG ("It's CRWen!"); else ATH_MSG_DEBUG ("It's NOT CRWen");
  if ((trigger_lep == 1) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) > 0) & (met_significance <= 4.0)) CRWepLowSig = true;}
  if (CRWepLowSig) ATH_MSG_DEBUG ("It's CRWepLowSig!"); else ATH_MSG_DEBUG ("It's NOT CRWepLowSig");
  if ((trigger_lep == 1) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 1) & (n_mu == 0)){ if ((el_charge->at(0) < 0) & (met_significance <= 4.0)) CRWenLowSig = true;}
  if (CRWenLowSig) ATH_MSG_DEBUG ("It's CRWenLowSig!"); else ATH_MSG_DEBUG ("It's NOT CRWenLowSig");
  if ((trigger_lep == 1) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) > 0)) CRWmp = true;}
  if (CRWmp) ATH_MSG_DEBUG ("It's CRWmp!"); else ATH_MSG_DEBUG ("It's NOT CRWmp");
  if ((trigger_lep == 1) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 1)){ if ((mu_charge->at(0) < 0)) CRWmn = true;}
  if (CRWmn) ATH_MSG_DEBUG ("It's CRWmn!"); else ATH_MSG_DEBUG ("It's NOT CRWmn");
  if ((trigger_lep == 1) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 2) & (n_mu == 0)){ if ((el_charge->at(0)*el_charge->at(1) < 0)) CRZee = true;}
  if (CRZee) ATH_MSG_DEBUG ("It's CRZee!"); else ATH_MSG_DEBUG ("It's NOT CRZee");
  if ((trigger_lep == 1) & (met_tst_nolep_et > METCut) & (met_tst_nolep_j1_dphi>1.0) & (met_tst_nolep_j2_dphi>1.0) & (n_el == 0) & (n_mu == 2)){ if ((mu_charge->at(0)*mu_charge->at(1) < 0)) CRZmm = true;}
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
  nFileEvt=0;
  m_treeName = "MiniNtuple";
  if(m_currentVariation!="Nominal")
    m_treeName = "MiniNtuple_"+m_currentVariation;
  std::cout << "Tree: " << m_treeName << std::endl;  
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  if(!m_tree) ATH_MSG_ERROR("VBFAnaysisAlg::beginInputFile - tree is invalid " << m_tree);
  
  nFileEvtTot=m_tree->GetEntries();
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

  if(m_extraVars){

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
    m_tree->SetBranchStatus("basemu_z0",1);
    m_tree->SetBranchStatus("basemu_ptvarcone20",1);
    m_tree->SetBranchStatus("basemu_type",1);
    if(m_isMC) m_tree->SetBranchStatus("basemu_truthOrigin",1);
    if(m_isMC) m_tree->SetBranchStatus("basemu_truthType",1);
    m_tree->SetBranchStatus("baseel_pt",1);
    m_tree->SetBranchStatus("baseel_eta",1);
    m_tree->SetBranchStatus("baseel_phi",1);
    m_tree->SetBranchStatus("baseel_z0",1);
    m_tree->SetBranchStatus("baseel_ptvarcone20",1);
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
  //if(foundGenMET) m_tree->SetBranchAddress("jet_passJvt",&jet_passJvt);
  
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
  
  if(m_extraVars){
  
    m_tree->SetBranchAddress("jet_fjvt",            &jet_fjvt);
    m_tree->SetBranchAddress("basemu_pt",           &basemu_pt);
    m_tree->SetBranchAddress("basemu_eta",          &basemu_eta);
    m_tree->SetBranchAddress("basemu_phi",          &basemu_phi);
    m_tree->SetBranchAddress("basemu_z0",           &basemu_z0);
    m_tree->SetBranchAddress("basemu_ptvarcone20",  &basemu_ptvarcone20);
    m_tree->SetBranchAddress("basemu_type",         &basemu_type);
    if(m_isMC) m_tree->SetBranchAddress("basemu_truthOrigin",  &basemu_truthOrigin);
    if(m_isMC) m_tree->SetBranchAddress("basemu_truthType",    &basemu_truthType);
    m_tree->SetBranchAddress("baseel_pt",           &baseel_pt);
    m_tree->SetBranchAddress("baseel_eta",          &baseel_eta);
    m_tree->SetBranchAddress("baseel_phi",          &baseel_phi);
    m_tree->SetBranchAddress("baseel_z0",           &baseel_z0);
    m_tree->SetBranchAddress("baseel_ptvarcone20",  &baseel_ptvarcone20);
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

