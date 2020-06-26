// VBFAnalysis includes
#include "VBFTruthAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"

#include <vector>
#include "TLorentzVector.h"
#include <math.h>

#define LINE std::cerr << __FILE__ << "::" << __FUNCTION__ << "::" << __LINE__ << std::endl;

const std::string regions[] = {"Incl_ZCR", "Incl_ZSR", "Incl_WCR", "Incl_WSR","Incl", "SRPhi","CRWPhi","CRZPhi", "SRPhiHigh","CRWPhiHigh","CRZPhiHigh","SRPhiLow","CRWPhiLow","CRZPhiLow","SRNjet","CRWNjet","CRZNjet","SRMETlow","CRWMETlow","CRZMETlow", "SRVRPhiHigh","CRZVRPhiHigh","CRWVRPhiHigh"};
const std::string variations[] = {"fac_up","fac_down","renorm_up","renorm_down","both_up","both_down"};



VBFTruthAlg::VBFTruthAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty( "currentSample", m_currentSample = "W_strong", "current sample");
  declareProperty( "runNumberInput", m_runNumberInput, "runNumber read from file name");
  declareProperty( "currentVariation", m_currentVariation = "Nominal", "Just truth tree here!" );
  declareProperty( "theoVariation", m_theoVariation = true, "Do theory systematic variations");
  declareProperty( "normFile", m_normFile = "/nfs/dust/atlas/user/othrif/vbf/myPP/source/VBFAnalysis/data/fout_v49.root", "path to a file with the number of events processed" );
  declareProperty( "noSkim", noSkim = false, "No skim");
}

VBFTruthAlg::~VBFTruthAlg() {}

StatusCode VBFTruthAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");

  cout<<"NAME of input tree in intialize ======="<<m_currentVariation<<endl;
  cout<< "CURRENT  sample === "<< m_currentSample<<endl;
  std::string   xSecFilePath = "dev/PMGTools/PMGxsecDB_mc15.txt";
 //std::string xSecFilePath = "VBFAnalysis/PMGxsecDB_mc16.txt"; // run from local file
  //std::string  xSecFilePath = "VBFAnalysis/PMGxsecDB_mc16_replace.txt";
  xSecFilePath = PathResolverFindCalibFile(xSecFilePath);
  my_XsecDB = new SUSY::CrossSectionDB(xSecFilePath);

  // old variables
  EventWeightSys = new std::vector<float>(0);
  jet_E = new std::vector<float>(0);
  jet_pt = new std::vector<float>(0);
  jet_eta = new std::vector<float>(0);
  jet_phi = new std::vector<float>(0);
  jet_m = new std::vector<float>(0);
  jet_label = new std::vector<int>(0);
  el_m = new std::vector<float>(0);
  el_pt = new std::vector<float>(0);
  el_eta = new std::vector<float>(0);
  el_phi = new std::vector<float>(0);
  el_type = new std::vector<unsigned int>(0);
  el_origin = new std::vector<unsigned int>(0);
  el_ptcone30 = new std::vector<float>(0);
  el_etcone20 = new std::vector<float>(0);
  el_pdgid = new std::vector<int>(0);
  mu_m = new std::vector<float>(0);
  mu_pt = new std::vector<float>(0);
  mu_eta = new std::vector<float>(0);
  mu_phi = new std::vector<float>(0);
  mu_type = new std::vector<unsigned int>(0);
  mu_origin = new std::vector<unsigned int>(0);
  mu_ptcone30 = new std::vector<float>(0);
  mu_etcone20 = new std::vector<float>(0);
  mu_pdgid = new std::vector<int>(0);
  boson_m = new std::vector<float>(0);
  boson_pt = new std::vector<float>(0);
  boson_eta = new std::vector<float>(0);
  boson_phi = new std::vector<float>(0);
  boson_pdgid = new std::vector<int>(0);
  nu_e = new std::vector<float>(0);
  nu_m = new std::vector<float>(0);
  nu_pt = new std::vector<float>(0);
  nu_eta = new std::vector<float>(0);
  nu_phi = new std::vector<float>(0);
  nu_type = new std::vector<unsigned int>(0);
  nu_origin = new std::vector<unsigned int>(0);
  nu_pdgid = new std::vector<int>(0);
  parton_x1 = new std::vector<float>(0);
  parton_x2 = new std::vector<float>(0);
  parton_xf1 = new std::vector<float>(0);
  parton_xf2 = new std::vector<float>(0);
  parton_Q = new std::vector<float>(0);
  parton_pdgid1 = new std::vector<int>(0);
  parton_pdgid2 = new std::vector<int>(0);
  parton_pdfid1 = new std::vector<int>(0);
  parton_pdfid2 = new std::vector<int>(0);
  parton_pp = new std::vector<int>(0);

  // new variables
  new_jet_E = new std::vector<float>(0);
  new_jet_pt = new std::vector<float>(0);
  new_jet_eta = new std::vector<float>(0);
  new_jet_phi = new std::vector<float>(0);
  new_el_m = new std::vector<float>(0);
  new_el_pt = new std::vector<float>(0);
  new_el_eta = new std::vector<float>(0);
  new_el_phi = new std::vector<float>(0);
  new_el_pdgid = new std::vector<int>(0);
  new_el_charge = new std::vector<float>(0);
  new_mu_m = new std::vector<float>(0);
  new_mu_pt = new std::vector<float>(0);
  new_mu_eta = new std::vector<float>(0);
  new_mu_phi = new std::vector<float>(0);
  new_mu_pdgid = new std::vector<int>(0);
  new_mu_charge = new std::vector<float>(0);
  new_boson_m = new std::vector<float>(0);
  new_boson_pt = new std::vector<float>(0);
  new_boson_eta = new std::vector<float>(0);
  new_boson_phi = new std::vector<float>(0);
  new_boson_pdgid = new std::vector<int>(0);
  new_nu_e = new std::vector<float>(0);
  new_nu_pt = new std::vector<float>(0);
  new_nu_eta = new std::vector<float>(0);
  new_nu_phi = new std::vector<float>(0);
  new_nu_charge = new std::vector<float>(0);
  new_lep_jet_dR = new std::vector<float>(0);

  //Create new output TTree
  treeTitleOut = m_currentSample+m_currentVariation;
  treeNameOut = m_currentSample+m_currentVariation;
  m_tree_out = new TTree(treeNameOut.c_str(), treeTitleOut.c_str());
  m_tree_out = new TTree(treeNameOut.c_str(), treeTitleOut.c_str());
  m_tree_out->Branch("w",&new_w);
//  m_tree_out->Branch("w_noxsec",&new_w_noxsec);
//  m_tree_out->Branch("xsec",&new_xsec);
//  m_tree_out->Branch("sumw", &new_sumw);
  m_tree_out->Branch("runNumber",&RunNumber);
//  m_tree_out->Branch("eventNumber",&EventNumber);
  m_tree_out->Branch("jj_mass",&new_jj_mass);
  m_tree_out->Branch("jj_deta",&new_jj_deta);
  m_tree_out->Branch("jj_dphi",&new_jj_dphi);
  m_tree_out->Branch("met_et",&new_met_et);
  m_tree_out->Branch("met_nolep_et",&new_met_nolep_et);
//  m_tree_out->Branch("met_phi",&new_met_phi);
//  m_tree_out->Branch("met_nolep_phi",&new_met_nolep_phi);
//  m_tree_out->Branch("mu_charge",&new_mu_charge);
//  m_tree_out->Branch("mu_pt",&new_mu_pt);
//  m_tree_out->Branch("el_charge",&new_el_charge);
//  m_tree_out->Branch("el_pt",&new_el_pt);
//  m_tree_out->Branch("mu_phi",&new_mu_phi);
//  m_tree_out->Branch("el_phi",&new_el_phi);
//  m_tree_out->Branch("mu_eta",&new_mu_eta);
//  m_tree_out->Branch("el_eta",&new_el_eta);
  m_tree_out->Branch("jet_pt",&new_jet_pt);
//  m_tree_out->Branch("jet_eta",&new_jet_eta);
//  m_tree_out->Branch("jet_phi",&new_jet_phi);
//  m_tree_out->Branch("jet_E",&new_jet_E);
//  m_tree_out->Branch("met_significance",&new_met_significance);
//  m_tree_out->Branch("lep_jet_dR",&new_lep_jet_dR);
//  m_tree_out->Branch("boson_m",&new_boson_m);
//  m_tree_out->Branch("boson_pt",&new_boson_pt);
//  m_tree_out->Branch("boson_phi",&new_boson_phi);
//  m_tree_out->Branch("boson_eta",&new_boson_eta);
//  m_tree_out->Branch("boson_pdgid",&new_boson_pdgid);
//  m_tree_out->Branch("nu_pt",&new_nu_pt);
//  m_tree_out->Branch("nu_phi",&new_nu_phi);
//  m_tree_out->Branch("nu_eta",&new_nu_eta);
//  m_tree_out->Branch("nu_charge",&new_nu_charge);
  m_tree_out->Branch("MV",&new_MV);
  m_tree_out->Branch("PTV",&new_PTV);
  m_tree_out->Branch("hasZ",&new_hasZ);


  m_tree_out->Branch("n_jet",   &new_njets);
//  m_tree_out->Branch("n_jet25", &new_n_jet25);
//  m_tree_out->Branch("n_jet30", &new_n_jet30);
//  m_tree_out->Branch("n_jet35", &new_n_jet35);
//  m_tree_out->Branch("n_jet40", &new_n_jet40);
//  m_tree_out->Branch("n_jet50", &new_n_jet50);

  m_tree_out->Branch("n_el",&new_nels);
//  m_tree_out->Branch("n_mu",&new_nmus);
 // m_tree_out->Branch("n_nu",&new_nnus);
 // m_tree_out->Branch("n_boson",&new_nbosons);

 // m_tree_out->Branch("ee_pt",   &new_ee_pt);
//  m_tree_out->Branch("ee_eta",  &new_ee_eta);
//  m_tree_out->Branch("ee_phi",  &new_ee_phi);
 // m_tree_out->Branch("ee_m",    &new_ee_m);
//  m_tree_out->Branch("mumu_pt", &new_mumu_pt);
//  m_tree_out->Branch("mumu_eta",&new_mumu_eta);
//  m_tree_out->Branch("mumu_phi",&new_mumu_phi);
//  m_tree_out->Branch("mumu_m",  &new_mumu_m);
//  m_tree_out->Branch("nunu_pt", &new_nunu_pt);
//  m_tree_out->Branch("nunu_eta",&new_nunu_eta);
//  m_tree_out->Branch("nunu_phi",&new_nunu_phi);
//  m_tree_out->Branch("nunu_m",  &new_nunu_m);

//  m_tree_out->Branch("useMerged",  &useMerged);

  //Register the output TTree
  CHECK(histSvc()->regTree("/MYSTREAM/"+treeTitleOut,m_tree_out));

  MapNgen(); //fill std::map with dsid->Ngen
  ATH_MSG_DEBUG ("Done Initializing");

  std::ostringstream runNumberss;
  runNumberss << RunNumber;
  outputName = m_currentSample+m_currentVariation+runNumberss.str();

  for (auto reg : regions){
    ANA_CHECK (book (TH1F (Form("jj_mass_%s_nominal",reg.c_str()), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    //ANA_CHECK (book (TH1F (Form("MV_%s_nominal",reg.c_str()), ";M_{V} [GeV];Entries", 50, 0, 500)));
    //ANA_CHECK (book (TH1F (Form("PTV_%s_nominal",reg.c_str()), ";p_{T}^{V} [GeV];Entries", 50, 0, 500)));
    //ANA_CHECK (book (TH1F (Form("boson_pT_%s_nominal",reg.c_str()), ";Boson p_{T} [GeV];Entries", 50, 0, 500)));
    //ANA_CHECK (book (TH1F (Form("boson_mass_%s_nominal",reg.c_str()), ";Boson Mass [GeV];Entries", 50, 0, 500)));
   if (m_theoVariation){
      for(int i=0; i<115; i++)
        ANA_CHECK (book (TH1F (Form("all/jj_mass_%s_index_%d", reg.c_str(), i), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    for (auto var : variations)
        ANA_CHECK (book (TH1F (Form("scales/jj_mass_%s_%s",reg.c_str(),var.c_str()), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    for(int j=0; j<100; j++)
        ANA_CHECK (book (TH1F (Form("PDF/jj_mass_%s_pdf%d",reg.c_str(),j), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    }
}

return StatusCode::SUCCESS;
}

StatusCode VBFTruthAlg::finalize() {
  ATH_MSG_INFO ("Finalizing " << name() << "...");

  return StatusCode::SUCCESS;}

StatusCode VBFTruthAlg::MapNgen(){
  TFile *f = TFile::Open(m_normFile.c_str(),"READ");
  if(!f or f->IsZombie()) std::cout << "\n\n\nERROR normFile. Could not open " << m_normFile << std::endl;
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

  StatusCode VBFTruthAlg::execute() {
      ATH_MSG_DEBUG ("\n\nExecuting " << name() << "...");

  // check that we don't have too many events
      if(nFileEvt>=nFileEvtTot){
        ATH_MSG_ERROR("VBFAnaysisAlg::execute: Too  many events:  " << nFileEvt << " total evts: " << nFileEvtTot);
        return StatusCode::SUCCESS;
    }

    if(!m_tree) ATH_MSG_ERROR("VBFAnaysisAlg::execute: tree invalid: " <<m_tree );
    m_tree->GetEntry(nFileEvt);

  // iterate event count
    ++nFileEvt;
  if (RunNumber != m_runNumberInput){ //HACK to hard set the run number
    ATH_MSG_ERROR("VBFAnaysisAlg::execute: runNumber " << RunNumber << " != m_runNumberInput " << m_runNumberInput );
    RunNumber=m_runNumberInput;
}

npevents++;
bool passExp = false;
for (int i = 0; i < 9; i++) {
  int exponent = pow(10, i);
  passExp |= (npevents <= exponent && (npevents % exponent) == 0);
}
if (passExp) std::cout <<" Processed "<< npevents << " Events"<<std::endl;


 // Number of generated events
 double NgenCorrected = 0.;
 NgenCorrected = Ngen[RunNumber];

  // Apply proper xsec
  crossSection = my_XsecDB->xsectTimesEff(RunNumber);//xs in pb
  // Multiply electron cross section by 3 to get all leptonic decay modes covered - ONLY for varied samples
  // 362192-362575 for zee and wenu
  if(362192 <= RunNumber && RunNumber <= 362575) crossSection *= 1; // this should be *3, but keep just the e-channel for now
  // Apply proper nomalization
  if(NgenCorrected>0)  weight = crossSection/NgenCorrected;
  else ATH_MSG_WARNING("Ngen " << nFileEvtTot << " dsid " << RunNumber );
  ATH_MSG_DEBUG("VBFAnalysisAlg: xs: "<< crossSection << " nevent: " << NgenCorrected);
  new_xsec = crossSection;
  new_sumw = NgenCorrected;

  // Decide which samples to use:

  // if Nominal Sherpa_221 MAXHTPTV, do not merge or change anything in the workflow
  // if Sherpa_227 PTV_MJJ kt merged OR Sherpa_221 PTV, merge the two based on PTV
  /*
  if (364100 <= RunNumber && RunNumber <= 364197)
    {useMerged = 0;
      if (fabs(EventWeight) > 100 ) {EventWeight=1.; std::cout << "RunNumber=" << RunNumber<< "Event " << EventNumber << " with |weight|>100 " << EventWeight << ", set to 1." << std::endl; }
    }
  else if (120.e3 < boson_pt->at(0) && boson_pt->at(0) < 500.e3 && 312448 <= RunNumber && RunNumber <= 312531)
    {useMerged = 1;}
  else if (boson_pt->at(0) > 500.e3 && 364216 <= RunNumber && RunNumber <= 364229)
  {useMerged = 1;}
else
   {useMerged = 2;}
  */

// Nominal: useMerged = 0
// kt-merged + PTV: useMerged = 1
// ckkw/qsf: useMerged = 2

if (364100 <= RunNumber && RunNumber <= 364197) // Sherpa_221 MAXHTPTV
{useMerged = 0;
      if (fabs(EventWeight) > 100 ) {EventWeight=1.; std::cout << "RunNumber=" << RunNumber<< ", EventNumber=" << EventNumber << " with |weight|>100 " << EventWeight << ", set to 1." << std::endl; }
}
else if (312448 <= RunNumber && RunNumber <= 312531){ // Sherpa_227 PTV_MJJ kt merged
  useMerged = 1;
}
else if (364216 <= RunNumber && RunNumber <= 364229){ // Sherpa_221 PTV
  useMerged = 1;
  if (fabs(EventWeight) > 100 ) {EventWeight=1.; std::cout << "RunNumber=" << RunNumber<< ", EventNumber=" << EventNumber << " with |weight|>100 " << EventWeight << ", set to 1." << std::endl; }
}
else if (362000 <= RunNumber && RunNumber <= 362575) // Sherpa_211 CT10 ckkw15,ckkw30,qsf025, qsf4
  {useMerged = 2;}
else
  {useMerged = 3;}

// Prepare variables

  // jets
  my_jets jet_signal;
  jet_signal.num_jets = 0;
  int njet25=0, njet30=0, njet35=0, njet40=0, njet50=0;
  for (size_t jeti = 0; jeti < jet_pt->size(); jeti++)
    //if(jet_pt->at(jeti)>25e3 && fabs(jet_eta->at(jeti)) < 4.5)
    {
      jet_signal.index[jet_signal.num_jets] = jeti;
      jet_signal.E[jet_signal.num_jets] =  jet_E->at(jeti);
      jet_signal.pT[jet_signal.num_jets] =  jet_pt->at(jeti);
      jet_signal.eta[jet_signal.num_jets] =  jet_eta->at(jeti);
      jet_signal.phi[jet_signal.num_jets] =  jet_phi->at(jeti);
      jet_signal.num_jets++;

      if(jet_pt->at(jeti) > 25e3) njet25++;
      if(jet_pt->at(jeti) > 30e3) njet30++;
      if(jet_pt->at(jeti) > 35e3) njet35++;
      if(jet_pt->at(jeti) > 40e3) njet40++;
      if(jet_pt->at(jeti) > 50e3) njet50++;
  }
  new_njets=jet_signal.num_jets;
  if (new_njets < 2) return StatusCode::SUCCESS;
  sortJets(&jet_signal);

  new_n_jet25 = njet25;
  new_n_jet30 = njet30;
  new_n_jet35 = njet35;
  new_n_jet40 = njet40;
  new_n_jet50 = njet50;

  // electrons
  my_leptons el_signal;
  el_signal.num_leptons = 0;
  for (size_t lepi = 0; lepi < el_pt->size(); lepi++)
    if(el_pt->at(lepi)>30e3 && fabs(el_eta->at(lepi)) < 2.5)
    {
      el_signal.index[el_signal.num_leptons] = lepi;
      el_signal.pT[el_signal.num_leptons] = el_pt->at(lepi);
      el_signal.phi[el_signal.num_leptons] = el_phi->at(lepi);
      el_signal.eta[el_signal.num_leptons] = el_eta->at(lepi);
      el_signal.is_electron[el_signal.num_leptons] = true;
      el_signal.charge[el_signal.num_leptons] = -1*el_pdgid->at(lepi)/TMath::Abs(el_pdgid->at(lepi));
      el_signal.num_leptons++;
  }
  new_nels = el_signal.num_leptons;
  sortLeptons(&el_signal);
  containsZ(&el_signal);

  // muons
  my_leptons mu_signal;
  mu_signal.num_leptons = 0;
  for (size_t lepi = 0; lepi < mu_pt->size(); lepi++)
    //if(mu_pt->at(lepi)>10e3 && fabs(mu_eta->at(lepi)) < 2.5)
    {
      mu_signal.index[mu_signal.num_leptons] = lepi;
      mu_signal.pT[mu_signal.num_leptons] = mu_pt->at(lepi);
      mu_signal.phi[mu_signal.num_leptons] = mu_phi->at(lepi);
      mu_signal.eta[mu_signal.num_leptons] = mu_eta->at(lepi);
      mu_signal.is_electron[mu_signal.num_leptons] = false;
      mu_signal.charge[mu_signal.num_leptons] = -1*mu_pdgid->at(lepi)/TMath::Abs(mu_pdgid->at(lepi));
      mu_signal.num_leptons++;
  }
  new_nmus = mu_signal.num_leptons;
  sortLeptons(&mu_signal);
  containsZ(&mu_signal);

// neutrinos
  my_leptons nu_signal;
  nu_signal.num_leptons = 0;
  for (size_t lepi = 0; lepi < nu_pt->size(); lepi++)
    //if(nu_pt->at(lepi)>10e3 && fabs(nu_eta->at(lepi)) < 2.5)
    {
      nu_signal.index[nu_signal.num_leptons] = lepi;
      nu_signal.pT[nu_signal.num_leptons] = nu_pt->at(lepi);
      nu_signal.phi[nu_signal.num_leptons] = nu_phi->at(lepi);
      nu_signal.eta[nu_signal.num_leptons] = nu_eta->at(lepi);
      nu_signal.is_electron[nu_signal.num_leptons] = false;
      nu_signal.charge[nu_signal.num_leptons] = -1*nu_pdgid->at(lepi)/TMath::Abs(nu_pdgid->at(lepi));
      nu_signal.num_leptons++;
  }
  new_nnus = nu_signal.num_leptons;
  sortLeptons(&nu_signal);
  containsZ(&nu_signal);

// Fill new variables of tree
  new_jet_E->clear();
  new_jet_pt->clear();
  new_jet_eta->clear();
  new_jet_phi->clear();
  new_mu_pt->clear();
  new_mu_eta->clear();
  new_mu_phi->clear();
  new_mu_charge->clear();
  new_el_pt->clear();
  new_el_eta->clear();
  new_el_phi->clear();
  new_el_charge->clear();
  new_nu_pt->clear();
  new_nu_eta->clear();
  new_nu_phi->clear();
  new_nu_charge->clear();
  new_boson_m->clear();
  new_boson_pt->clear();
  new_boson_eta->clear();
  new_boson_phi->clear();
  new_boson_pdgid->clear();

  for (size_t i_jet=0; i_jet<unsigned(new_njets); i_jet++){
      new_jet_E->push_back(jet_signal.E[i_jet]);
      new_jet_pt->push_back(jet_signal.pT[i_jet]);
      new_jet_eta->push_back(jet_signal.eta[i_jet]);
      new_jet_phi->push_back(jet_signal.phi[i_jet]);
  }
  for (size_t i_el=0; i_el<unsigned(new_nels); i_el++){
      new_el_pt->push_back(el_signal.pT[i_el]);
      new_el_eta->push_back(el_signal.eta[i_el]);
      new_el_phi->push_back(el_signal.phi[i_el]);
      new_el_charge->push_back(el_signal.charge[i_el]);
  }
  for (size_t i_mu=0; i_mu<unsigned(new_nmus); i_mu++){
      new_mu_pt->push_back(mu_signal.pT[i_mu]);
      new_mu_eta->push_back(mu_signal.eta[i_mu]);
      new_mu_phi->push_back(mu_signal.phi[i_mu]);
      new_mu_charge->push_back(mu_signal.charge[i_mu]);
  }
    for (size_t i_nu=0; i_nu<unsigned(new_nnus); i_nu++){
      new_nu_pt->push_back(nu_signal.pT[i_nu]);
      new_nu_eta->push_back(nu_signal.eta[i_nu]);
      new_nu_phi->push_back(nu_signal.phi[i_nu]);
      new_nu_charge->push_back(nu_signal.charge[i_nu]);
  }
  new_nbosons = boson_m->size();
  for (size_t i_v=0; i_v<unsigned(new_nbosons); i_v++){
    new_boson_m->push_back(boson_m->at(i_v));
    new_boson_pt->push_back(boson_pt->at(i_v));
    new_boson_phi->push_back(boson_phi->at(i_v));
    new_boson_eta->push_back(boson_eta->at(i_v));
    new_boson_pdgid->push_back(boson_pdgid->at(i_v));
  }


  // compute boson variables
  Double_t ee_m(-9999), ee_pt(-9999), ee_eta(-9999), ee_phi(-9999);
  Double_t mumu_m(-9999), mumu_pt(-9999), mumu_eta(-9999), mumu_phi(-9999);
  Double_t nunu_m(-9999), nunu_pt(-9999), nunu_eta(-9999), nunu_phi(-9999);

  TLorentzVector lep_tlv[3];
  if(new_nels==2) {
    //new_MV = el_signal.Mll; new_hasZ = el_signal.has_Z_OS;
    for(int i=0; i<2; i++) lep_tlv[i].SetPtEtaPhiM(el_signal.pT[i], el_signal.eta[i], el_signal.phi[i], electron_mass);
    lep_tlv[2] = lep_tlv[0] + lep_tlv[1];
    ee_pt  = (lep_tlv[2]).Pt();
    ee_eta = (lep_tlv[2]).Eta();
    ee_phi = (lep_tlv[2]).Phi();
    ee_m   = (lep_tlv[2]).M();
  }

  if(new_nmus==2) {
    //new_MV = mu_signal.Mll; new_hasZ = mu_signal.has_Z_OS;
    for(int i=0; i<2; i++) lep_tlv[i].SetPtEtaPhiM(mu_signal.pT[i], mu_signal.eta[i], mu_signal.phi[i], muon_mass);
    lep_tlv[2] = lep_tlv[0] + lep_tlv[1];
    mumu_pt  = (lep_tlv[2]).Pt();
    mumu_eta = (lep_tlv[2]).Eta();
    mumu_phi = (lep_tlv[2]).Phi();
    mumu_m   = (lep_tlv[2]).M();
  }

  if(new_nnus==2) {
    //new_MV = nu_signal.Mll; new_hasZ = nu_signal.has_Z_OS;
    for(int i=0; i<2; i++) lep_tlv[i].SetPtEtaPhiM(nu_signal.pT[i], nu_signal.eta[i], nu_signal.phi[i], nu_mass);
    lep_tlv[2] = lep_tlv[0] + lep_tlv[1];
    nunu_pt  = (lep_tlv[2]).Pt();
    nunu_eta = (lep_tlv[2]).Eta();
    nunu_phi = (lep_tlv[2]).Phi();
    nunu_m   = (lep_tlv[2]).M();
  }

  new_ee_pt  = ee_pt ;
  new_ee_eta = ee_eta;
  new_ee_phi = ee_phi;
  new_ee_m   = ee_m  ;
  new_mumu_pt  = mumu_pt ;
  new_mumu_eta = mumu_eta;
  new_mumu_phi = mumu_phi;
  new_mumu_m   = mumu_m  ;
  new_nunu_pt  = nunu_pt ;
  new_nunu_eta = nunu_eta;
  new_nunu_phi = nunu_phi;
  new_nunu_m   = nunu_m  ;

/*
if(new_nbosons==0){
  ATH_MSG_DEBUG("NO boson found! build one");
  if ( 364142 <= RunNumber && RunNumber <= 364155 ){ //Zvv
    new_boson_m->push_back(new_nunu_m);
    new_boson_pt->push_back(new_nunu_pt);
  }
  else if ( 364100 <= RunNumber && RunNumber <= 364113 ){ //Zmm
    new_boson_m->push_back(new_mumu_m);
    new_boson_pt->push_back(new_mumu_pt);
  }  else if ( 364114 <= RunNumber && RunNumber <= 364127 || 361372 <= RunNumber && RunNumber <= 361374 ||  364114 <= RunNumber && RunNumber <= 364127){ //Zee
    new_boson_m->push_back(new_ee_m);
    new_boson_pt->push_back(new_ee_pt);
  }
  new_nbosons++;
}*/

 if ( (364142 <= RunNumber && RunNumber <= 364155) || (362000 <= RunNumber && RunNumber <= 362191) || ( 312484<= RunNumber && RunNumber <= 312495) ){ //Zvv
  new_MV = nu_signal.Mll; new_hasZ = nu_signal.has_Z_OS; new_PTV = nu_signal.PTV;
 }
 else if ( (364114 <= RunNumber && RunNumber <= 364127) || (361372 <= RunNumber && RunNumber <= 361374) ||  (362192 <= RunNumber && RunNumber <= 362383) || (312448 <= RunNumber && RunNumber <= 312459)){ //Zee
new_MV = el_signal.Mll; new_hasZ = el_signal.has_Z_OS; new_PTV = el_signal.PTV;

}
 else if ( ((364170 <= RunNumber && RunNumber <= 364183) ||  (362384 <= RunNumber && RunNumber <= 362575) ||  (312496 <= RunNumber && RunNumber <= 312507)) && new_nbosons!=0){ //Wenu
new_MV = boson_m->at(0); new_hasZ = false; new_PTV = boson_pt->at(0); // hack for now, need to compute the W boson mass and ptv from e and nu
}

  computejj(&jet_signal, new_jj_mass, new_jj_deta, new_jj_dphi);
  new_met_et = met_et;
  new_met_phi = met_phi;
  new_met_nolep_et = -9999.;
  new_met_nolep_phi = -9999.;
  Float_t px = 0;
  Float_t py = 0;
  new_lep_jet_dR->clear();
  for (size_t i_el=0; i_el<new_el_pt->size(); i_el++){
   px += new_el_pt->at(i_el) * TMath::Cos(new_el_phi->at(i_el));
   py += new_el_pt->at(i_el) * TMath::Sin(new_el_phi->at(i_el));
   // calculate min dR with jet
   TLorentzVector tmp_lep, tmp_jet;
   float dR_lep_jet = 9999.;
   tmp_lep.SetPtEtaPhiM(new_el_pt->at(i_el), new_el_eta->at(i_el), new_el_phi->at(i_el), electron_mass);
   for (size_t i_jet=0; i_jet<new_jet_pt->size(); i_jet++){
      tmp_jet.SetPtEtaPhiE(new_jet_pt->at(i_jet), new_jet_eta->at(i_jet), new_jet_phi->at(i_jet), new_jet_E->at(i_jet));
      float tmp_dR=tmp_jet.DeltaR(tmp_lep);
      if(tmp_dR < dR_lep_jet) dR_lep_jet = tmp_dR;
  }
  new_lep_jet_dR->push_back(dR_lep_jet);
}
for (size_t i_mu=0; i_mu<new_mu_pt->size(); i_mu++){
 px += new_mu_pt->at(i_mu) * TMath::Cos(new_mu_phi->at(i_mu));
 py += new_mu_pt->at(i_mu) * TMath::Sin(new_mu_phi->at(i_mu));
   // calculate min dR with jet
 TLorentzVector tmp_lep, tmp_jet;
 float dR_lep_jet = 9999.;
 tmp_lep.SetPtEtaPhiM(new_mu_pt->at(i_mu), new_mu_eta->at(i_mu), new_mu_phi->at(i_mu), muon_mass);
 for (size_t i_jet=0; i_jet<new_jet_pt->size(); i_jet++){
    tmp_jet.SetPtEtaPhiE(new_jet_pt->at(i_jet), new_jet_eta->at(i_jet), new_jet_phi->at(i_jet), new_jet_E->at(i_jet));
    float tmp_dR=tmp_jet.DeltaR(tmp_lep);
    if(tmp_dR < dR_lep_jet) dR_lep_jet = tmp_dR;
}
new_lep_jet_dR->push_back(dR_lep_jet);
}
Float_t mpx = met_et*TMath::Cos(met_phi) + px;
Float_t mpy = met_et*TMath::Sin(met_phi) + py;
new_met_nolep_et = TMath::Sqrt(mpx*mpx+mpy*mpy);
new_met_nolep_phi = TMath::ATan2(mpy,mpx);

if(new_nels==1 && new_nmus==0) {
    new_met_significance = new_met_et/1000/sqrt((new_el_pt->at(0) + new_jet_pt->at(0) + new_jet_pt->at(1))/1000.);
} else {
    new_met_significance = 0;
}

// Define regions
bool CRZll = false;
bool SRPhiHigh = false;
bool CRWPhiHigh = false;
bool CRZPhiHigh = false;
bool SRPhiLow = false;
bool CRWPhiLow = false;
bool CRZPhiLow = false;
bool SRNjet = false;
bool CRWNjet = false;
bool CRZNjet = false;
bool SRMETlow = false;
bool CRWMETlow = false;
bool CRZMETlow = false;
bool VRPhiHigh = false;

bool SRVRPhiHigh = false;
bool CRZVRPhiHigh = false;
bool CRWVRPhiHigh = false;

// Definiing a loose skimming
float METCut = 200.0e3;
float LeadJetPtCut = 80.0e3;
float subLeadJetPtCut = 50.0e3;
float MjjCut =2e5;
float DEtajjCut =3.8;
float MV = -999;
float PTV = -999;

/*if(boson_pt->size() == 0 && new_boson_pt->size() !=0 ){
  PTV = new_boson_pt->at(0);
  MV = new_boson_m->at(0);
}
else if (boson_pt->size() != 0){
  PTV = boson_pt->at(0);
  MV = boson_m->at(0);
}
else
  ATH_MSG_ERROR("THERE IS A PROBLEM with Number of bosons!!");*/

bool vbfSkim = (new_jet_pt->at(0) > LeadJetPtCut) & (new_jet_pt->at(1) > subLeadJetPtCut) & (new_jj_deta > DEtajjCut) & ((new_jet_eta->at(0) * new_jet_eta->at(1))<0) & (new_jj_mass > MjjCut);
bool vbfSkimloose = (new_jet_pt->at(0) > 50.0e3) & (new_jet_pt->at(1) > 50.0e3)  & (new_jj_mass > 500e3) & (new_jj_deta > 2.5) & (new_PTV > 100e3); //  & (new_jj_dphi<2.5)  & ( PTV > 100e3)

if (vbfSkim & (new_njets == 2) & (1 <= new_jj_dphi && new_jj_dphi < 2.0) & (new_met_et > METCut) & (new_nels == 0) & (new_nmus == 0))                                                     SRPhiHigh = true;
if (vbfSkim & (new_njets == 2) & (1 <= new_jj_dphi && new_jj_dphi < 2.0) & (new_met_nolep_et > METCut) & ((new_nels == 2 & new_nmus == 0) || (new_nels == 0 & new_nmus == 2)) & new_hasZ) CRZPhiHigh = true;
if (vbfSkim & (new_njets == 2) & (1 <= new_jj_dphi && new_jj_dphi < 2.0) & (new_met_nolep_et > METCut) & ((new_nels == 1 & new_nmus == 0) || (new_nels == 0 & new_nmus == 1)))            CRWPhiHigh = true;

if (vbfSkim & (new_njets == 2) & (new_jj_dphi < 1.) & (new_met_et > METCut) & (new_nels == 0) & (new_nmus == 0))                                                      SRPhiLow= true;
if (vbfSkim & (new_njets == 2) & (new_jj_dphi < 1.) & (new_met_nolep_et > METCut) &  ((new_nels == 2 & new_nmus == 0) || (new_nels == 0 & new_nmus == 2)) & new_hasZ) CRZPhiLow = true;
if (vbfSkim & (new_njets == 2) & (new_jj_dphi < 1.) & (new_met_nolep_et > METCut) &  ((new_nels == 1 & new_nmus == 0) || (new_nels == 0 & new_nmus == 1)))            CRWPhiLow = true;

if (vbfSkim & (2 < new_njets && new_njets < 5) & (new_jj_dphi < 2.0) & (new_met_et > METCut) & (new_nels == 0) & (new_nmus == 0))                                                     SRNjet    = true;
if (vbfSkim & (2 < new_njets && new_njets < 5) & (new_jj_dphi < 2.0) & (new_met_nolep_et > METCut) & ((new_nels == 2 & new_nmus == 0) || (new_nels == 0 & new_nmus == 2)) & new_hasZ) CRZNjet = true;
if (vbfSkim & (2 < new_njets && new_njets < 5) & (new_jj_dphi < 2.0) & (new_met_nolep_et > METCut) & ((new_nels == 1 & new_nmus == 0) || (new_nels == 0 & new_nmus == 1)))            CRWNjet = true;

if (vbfSkim & (new_njets == 2) & (new_jj_dphi < 2.0) & (160e3 < new_met_et & new_met_et < METCut) & (new_nels == 0) & (new_nmus == 0))                                                           SRMETlow = true;
if (vbfSkim & (new_njets == 2) & (new_jj_dphi < 2.0) & (160e3 < new_met_nolep_et & new_met_nolep_et < METCut) & ((new_nels == 2 & new_nmus == 0) || (new_nels == 0 & new_nmus == 2)) & new_hasZ) CRZMETlow = true;
if (vbfSkim & (new_njets == 2) & (new_jj_dphi < 2.0) & (160e3 < new_met_nolep_et & new_met_nolep_et < METCut) & ((new_nels == 1 & new_nmus == 0) || (new_nels == 0 & new_nmus == 1)))            CRWMETlow = true;

if (vbfSkim & (2 <= new_jj_dphi && new_jj_dphi < 2.5) & (new_met_et > METCut) & (new_nels == 0) & (new_nmus == 0)) SRVRPhiHigh = true;
if (vbfSkim & (2 <= new_jj_dphi && new_jj_dphi < 2.5) & (new_met_et > METCut) & ((new_nels == 1 & new_nmus == 0) || (new_nels == 0 & new_nmus == 1))) CRWVRPhiHigh = true;
if (vbfSkim & (2 <= new_jj_dphi && new_jj_dphi < 2.5) & (new_met_et > METCut) & ((new_nels == 2 & new_nmus == 0) || (new_nels == 0 & new_nmus == 2)) & new_hasZ) CRZVRPhiHigh = true;

if(vbfSkimloose /*&& ( (362192 <= RunNumber && RunNumber <= 362383) || (364114 <= RunNumber && RunNumber <= 364127) )*/ ){
if (new_hasZ) CRZll = true; // (new_nels == 2) & (new_nmus == 0) &
//if (new_hasZ) CRZll = true; // (new_nels == 0) & (new_nmus == 2) &
}

std::map<TString,bool> regDecision;

bool Zvv = (362000 <= RunNumber && RunNumber <= 362191) || (364142 <= RunNumber && RunNumber <= 364155);
bool Zee = (362192 <= RunNumber && RunNumber <= 362383) || (364114 <= RunNumber && RunNumber <= 364127);
bool Wev = (362384 <= RunNumber && RunNumber <= 362575) || (364170 <= RunNumber && RunNumber <= 364183);

regDecision["Incl_ZSR"]=(vbfSkimloose && Zvv);
regDecision["Incl_ZCR"]=(vbfSkimloose && Zee);
regDecision["Incl_WSR"]=(vbfSkimloose && Wev && (new_nels == 0));
regDecision["Incl_WCR"]=(vbfSkimloose && Wev && (new_nels > 0));

regDecision["Incl"]=true;
//regDecision["SRPhi"]=(SRPhiHigh || SRPhiLow);
//regDecision["CRZPhi"]=(CRZPhiHigh || CRZPhiLow);
//regDecision["CRWPhi"]=(CRWPhiHigh || CRWPhiLow);
//regDecision["CRZll"]=((new_PTV > 100e3) && new_hasZ); //CRZll

regDecision["SRPhiHigh"]=SRPhiHigh;
regDecision["CRZPhiHigh"]=CRZPhiHigh;
regDecision["CRWPhiHigh"]=CRWPhiHigh;
regDecision["SRPhiLow"]=SRPhiLow;
regDecision["CRZPhiLow"]=CRZPhiLow;
regDecision["CRWPhiLow"]=CRWPhiLow;
regDecision["SRNjet"]=SRNjet;
regDecision["CRZNjet"]=CRZNjet;
regDecision["CRWNjet"]=CRWNjet;
regDecision["SRMETlow"] =SRMETlow;
regDecision["CRZMETlow"]=CRZMETlow;
regDecision["CRWMETlow"]=CRWMETlow;
regDecision["SRPhi"]=(SRPhiHigh || SRPhiLow);
regDecision["CRZPhi"]=(CRZPhiHigh || CRZPhiLow);
regDecision["CRWPhi"]=(CRWPhiHigh || CRWPhiLow);

regDecision["SRVRPhiHigh"]=SRVRPhiHigh;
regDecision["CRZVRPhiHigh"]=CRZVRPhiHigh;
regDecision["CRWVRPhiHigh"]=CRWVRPhiHigh;


new_w = weight*EventWeight;
new_w_noxsec = EventWeight;

for(auto reg : regions){
    if(regDecision[reg]){
      hist( "jj_mass_"+reg+"_nominal" )->Fill(new_jj_mass/1e6, new_w);
      //hist( "MV_"+reg+"_nominal" )->Fill(new_MV/1e3, new_w);
      //hist( "PTV_"+reg+"_nominal" )->Fill(new_PTV/1e3, new_w);
      //if( new_boson_pt->size() != 0 ){
      //hist( "boson_pT_"+reg+"_nominal" )->Fill(new_boson_pt->at(0)/1e3, new_w);
      //hist( "boson_mass_"+reg+"_nominal" )->Fill(new_boson_m->at(0)/1e3, new_w);
    //}
    //else
      //  ATH_MSG_DEBUG("Missing TruthBoson record!!");
  }

    if (m_theoVariation /*&& ( (362192 <= RunNumber && RunNumber <= 362383) || (364114 <= RunNumber && RunNumber <= 364127) ) */){
      for(int i=0; i<115; i++){
        if(regDecision[reg])
          hist("jj_mass_"+reg+"_index_"+to_string(i))->Fill(new_jj_mass/1e6, weight*EventWeightSys->at(i));
      }

      if(regDecision[reg])
  {
          hist( "scales/jj_mass_"+reg+"_fac_up" )->Fill(new_jj_mass/1e6, weight*EventWeightSys->at(8));
          hist( "scales/jj_mass_"+reg+"_fac_down" )->Fill(new_jj_mass/1e6, weight*EventWeightSys->at(6));
          hist( "scales/jj_mass_"+reg+"_renorm_up" )->Fill(new_jj_mass/1e6, weight*EventWeightSys->at(9));
          hist( "scales/jj_mass_"+reg+"_renorm_down" )->Fill(new_jj_mass/1e6, weight*EventWeightSys->at(5));
          hist( "scales/jj_mass_"+reg+"_both_up" )->Fill(new_jj_mass/1e6, weight*EventWeightSys->at(10));
          hist( "scales/jj_mass_"+reg+"_both_down" )->Fill(new_jj_mass/1e6, weight*EventWeightSys->at(4));
          for(unsigned int j = 11; j <= 110; j++)
            hist( "PDF/jj_mass_"+reg+"_pdf"+to_string(j-11) )->Fill(new_jj_mass/1e6, weight*EventWeightSys->at(j));
        }
      }
    }

if (vbfSkimloose || noSkim){ // && (useMerged == 0 || useMerged == 1 || useMerged == 2  || useMerged == 3)
  m_tree_out->Fill();
}

return StatusCode::SUCCESS;
}

StatusCode VBFTruthAlg::beginInputFile() {

    ATH_MSG_INFO("VBFTruthAlg::beginInputFile()");
    nFileEvt=0;
    m_treeName = "MiniNtuple";
    if(m_currentVariation!="Nominal")
      m_treeName = "MiniNtuple_"+m_currentVariation;
  std::cout << "Tree: " << m_treeName << std::endl;
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  if(!m_tree) ATH_MSG_ERROR("VBFAnaysisAlg::beginInputFile - tree is invalid " << m_tree);

  nFileEvtTot=m_tree->GetEntries();
  ATH_MSG_INFO(">>> Processing " << nFileEvtTot << " events!");
  m_tree->SetBranchStatus("*",0);

  m_tree->SetBranchStatus("EventNumber", 1);
  m_tree->SetBranchStatus("RunNumber", 1);
  m_tree->SetBranchStatus("crossSection", 1);
  m_tree->SetBranchStatus("EventWeight", 1);
  m_tree->SetBranchStatus("ChannelNumber", 1);
  m_tree->SetBranchStatus("EventWeightSys", 1);
  m_tree->SetBranchStatus("njets", 1);
  m_tree->SetBranchStatus("jet_E", 1);
  m_tree->SetBranchStatus("jet_pt", 1);
  m_tree->SetBranchStatus("jet_eta", 1);
  m_tree->SetBranchStatus("jet_phi", 1);
  m_tree->SetBranchStatus("jet_m", 1);
  m_tree->SetBranchStatus("jet_label", 1);
  m_tree->SetBranchStatus("nels", 1);
  m_tree->SetBranchStatus("el_m", 1);
  m_tree->SetBranchStatus("el_pt", 1);
  m_tree->SetBranchStatus("el_eta", 1);
  m_tree->SetBranchStatus("el_phi", 1);
  m_tree->SetBranchStatus("el_type", 1);
  m_tree->SetBranchStatus("el_origin", 1);
  m_tree->SetBranchStatus("el_ptcone30", 1);
  m_tree->SetBranchStatus("el_etcone20", 1);
  m_tree->SetBranchStatus("el_pdgid", 1);
  m_tree->SetBranchStatus("nmus", 1);
  m_tree->SetBranchStatus("mu_m", 1);
  m_tree->SetBranchStatus("mu_pt", 1);
  m_tree->SetBranchStatus("mu_eta", 1);
  m_tree->SetBranchStatus("mu_phi", 1);
  m_tree->SetBranchStatus("mu_type", 1);
  m_tree->SetBranchStatus("mu_origin", 1);
  m_tree->SetBranchStatus("mu_ptcone30", 1);
  m_tree->SetBranchStatus("mu_etcone20", 1);
  m_tree->SetBranchStatus("mu_pdgid", 1);
  m_tree->SetBranchStatus("nbosons", 1);
  m_tree->SetBranchStatus("boson_m", 1);
  m_tree->SetBranchStatus("boson_pt", 1);
  m_tree->SetBranchStatus("boson_eta", 1);
  m_tree->SetBranchStatus("boson_phi", 1);
  m_tree->SetBranchStatus("boson_pdgid", 1);
  m_tree->SetBranchStatus("nnus", 1);
  m_tree->SetBranchStatus("nu_e", 1);
  m_tree->SetBranchStatus("nu_m", 1);
  m_tree->SetBranchStatus("nu_pt", 1);
  m_tree->SetBranchStatus("nu_eta", 1);
  m_tree->SetBranchStatus("nu_phi", 1);
  m_tree->SetBranchStatus("nu_type", 1);
  m_tree->SetBranchStatus("nu_origin", 1);
  m_tree->SetBranchStatus("nu_pdgid", 1);
  m_tree->SetBranchStatus("met_et", 1);
  m_tree->SetBranchStatus("met_phi", 1);
  m_tree->SetBranchStatus("parton_x1", 1);
  m_tree->SetBranchStatus("parton_x2", 1);
  m_tree->SetBranchStatus("parton_xf1", 1);
  m_tree->SetBranchStatus("parton_xf2", 1);
  m_tree->SetBranchStatus("parton_Q", 1);
  m_tree->SetBranchStatus("parton_pdgid1", 1);
  m_tree->SetBranchStatus("parton_pdgid2", 1);
  m_tree->SetBranchStatus("parton_pdfid1", 1);
  m_tree->SetBranchStatus("parton_pdfid2", 1);
  m_tree->SetBranchStatus("parton_pp", 1);

  m_tree->SetBranchAddress("EventNumber", &EventNumber);
  m_tree->SetBranchAddress("RunNumber", &RunNumber);
  m_tree->SetBranchAddress("crossSection", &crossSection);
  m_tree->SetBranchAddress("EventWeight", &EventWeight);
  m_tree->SetBranchAddress("ChannelNumber", &ChannelNumber);
  m_tree->SetBranchAddress("EventWeightSys", &EventWeightSys);
  m_tree->SetBranchAddress("njets", &njets);
  m_tree->SetBranchAddress("jet_E", &jet_E);
  m_tree->SetBranchAddress("jet_pt", &jet_pt);
  m_tree->SetBranchAddress("jet_eta", &jet_eta);
  m_tree->SetBranchAddress("jet_phi", &jet_phi);
  m_tree->SetBranchAddress("jet_m", &jet_m);
  m_tree->SetBranchAddress("jet_label", &jet_label);
  m_tree->SetBranchAddress("nels", &nels);
  m_tree->SetBranchAddress("el_m", &el_m);
  m_tree->SetBranchAddress("el_pt", &el_pt);
  m_tree->SetBranchAddress("el_eta", &el_eta);
  m_tree->SetBranchAddress("el_phi", &el_phi);
  m_tree->SetBranchAddress("el_type", &el_type);
  m_tree->SetBranchAddress("el_origin", &el_origin);
  m_tree->SetBranchAddress("el_ptcone30", &el_ptcone30);
  m_tree->SetBranchAddress("el_etcone20", &el_etcone20);
  m_tree->SetBranchAddress("el_pdgid", &el_pdgid);
  m_tree->SetBranchAddress("nmus", &nmus);
  m_tree->SetBranchAddress("mu_m", &mu_m);
  m_tree->SetBranchAddress("mu_pt", &mu_pt);
  m_tree->SetBranchAddress("mu_eta", &mu_eta);
  m_tree->SetBranchAddress("mu_phi", &mu_phi);
  m_tree->SetBranchAddress("mu_type", &mu_type);
  m_tree->SetBranchAddress("mu_origin", &mu_origin);
  m_tree->SetBranchAddress("mu_ptcone30", &mu_ptcone30);
  m_tree->SetBranchAddress("mu_etcone20", &mu_etcone20);
  m_tree->SetBranchAddress("mu_pdgid", &mu_pdgid);
  m_tree->SetBranchAddress("nbosons", &nbosons);
  m_tree->SetBranchAddress("boson_m", &boson_m);
  m_tree->SetBranchAddress("boson_pt", &boson_pt);
  m_tree->SetBranchAddress("boson_eta", &boson_eta);
  m_tree->SetBranchAddress("boson_phi", &boson_phi);
  m_tree->SetBranchAddress("boson_pdgid", &boson_pdgid);
  m_tree->SetBranchAddress("nnus", &nnus);
  m_tree->SetBranchAddress("nu_e", &nu_e);
  m_tree->SetBranchAddress("nu_m", &nu_m);
  m_tree->SetBranchAddress("nu_pt", &nu_pt);
  m_tree->SetBranchAddress("nu_eta", &nu_eta);
  m_tree->SetBranchAddress("nu_phi", &nu_phi);
  m_tree->SetBranchAddress("nu_type", &nu_type);
  m_tree->SetBranchAddress("nu_origin", &nu_origin);
  m_tree->SetBranchAddress("nu_pdgid", &nu_pdgid);
  m_tree->SetBranchAddress("met_et", &met_et);
  m_tree->SetBranchAddress("met_phi", &met_phi);
  m_tree->SetBranchAddress("parton_x1", &parton_x1);
  m_tree->SetBranchAddress("parton_x2", &parton_x2);
  m_tree->SetBranchAddress("parton_xf1", &parton_xf1);
  m_tree->SetBranchAddress("parton_xf2", &parton_xf2);
  m_tree->SetBranchAddress("parton_Q", &parton_Q);
  m_tree->SetBranchAddress("parton_pdgid1", &parton_pdgid1);
  m_tree->SetBranchAddress("parton_pdgid2", &parton_pdgid2);
  m_tree->SetBranchAddress("parton_pdfid1", &parton_pdfid1);
  m_tree->SetBranchAddress("parton_pdfid2", &parton_pdfid2);
  m_tree->SetBranchAddress("parton_pp", &parton_pp);

  m_tree->SetBranchAddress("truthF_jj_mass", &truthF_jj_mass);
  m_tree->SetBranchAddress("truthF_jj_deta", &truthF_jj_deta);
  //m_tree->SetBranchAddress("truthF_jj_dphi", &truthF_jj_dphi); // Missing in v42
  m_tree->SetBranchAddress("passVjetsFilter", &passVjetsFilter);

  return StatusCode::SUCCESS;
}
