// VBFAnalysis includes
#include "VBFVjetsAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"

#include <vector>
#include "TLorentzVector.h"
#include <math.h>

#define LINE std::cerr << __FILE__ << "::" << __FUNCTION__ << "::" << __LINE__ << std::endl;

const std::string regions[] = {"Incl","SRPhi", "CRWPhi", "CRZPhi", "SRPhiHigh","CRWPhiHigh","CRZPhiHigh","SRPhiLow","CRWPhiLow","CRZPhiLow","SRNjet","CRWNjet","CRZNjet","CRZll"};
const std::string variations[] = {"fac_up","fac_down","renorm_up","renorm_down","both_up","both_down"};



VBFVjetsAlg::VBFVjetsAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty( "currentSample", m_currentSample = "W_strong", "current sample");
  declareProperty( "runNumberInput", m_runNumberInput, "runNumber read from file name");
  declareProperty( "currentVariation", m_currentVariation = "Nominal", "Just truth tree here!" );
  declareProperty( "theoVariation", m_theoVariation = true, "Do theory systematic variations");
  declareProperty( "normFile", m_normFile = "/nfs/dust/atlas/user/othrif/vbf/myPP/source/VBFAnalysis/data/fout_v42.root", "path to a file with the number of events processed" );
  declareProperty( "noSkim", noSkim = false, "No skim");
}

VBFVjetsAlg::~VBFVjetsAlg() {}

StatusCode VBFVjetsAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");

  cout<<"NAME of input tree in intialize ======="<<m_currentVariation<<endl;
  cout<< "CURRENT  sample === "<< m_currentSample<<endl;
  std::string   xSecFilePath = "dev/PMGTools/PMGxsecDB_mc15.txt";
 // std::string xSecFilePath = "VBFAnalysis/PMGxsecDB_mc16.txt"; // run from local file
  //std::string  xSecFilePath = "VBFAnalysis/PMGxsecDB_mc16_replace.txt";
  xSecFilePath = PathResolverFindCalibFile(xSecFilePath);
  my_XsecDB = new SUSY::CrossSectionDB(xSecFilePath);

  new_photon_MCTC = new std::vector<int>(0);
  new_photon_boson_dR = new std::vector<float>(0);
  new_photon_lepton_dressed_dR = new std::vector<float>(0);
  new_photon_lepton_undressed_dR = new std::vector<float>(0);

  //Create new output TTree
  treeTitleOut = m_currentSample+m_currentVariation;
  treeNameOut = m_currentSample+m_currentVariation;
  m_tree_out = new TTree(treeNameOut.c_str(), treeTitleOut.c_str());
  m_tree_out = new TTree(treeNameOut.c_str(), treeTitleOut.c_str());

  m_tree_out->Branch("runNumber",&run);
  m_tree_out->Branch("eventNumber",&event);
  m_tree_out->Branch("jj_mass",&jj_mass);
  m_tree_out->Branch("jj_deta",&jj_deta);
  m_tree_out->Branch("jj_dphi",&jj_dphi);
  m_tree_out->Branch("jet_pt",&jet_pt);
  m_tree_out->Branch("jet_eta",&jet_eta);
  m_tree_out->Branch("jet_phi",&jet_phi);
  m_tree_out->Branch("jet_E",&jet_E);

  m_tree_out->Branch("w",&new_w);

  m_tree_out->Branch("n_boson",&new_nbosons);
  m_tree_out->Branch("boson_m",&new_boson_m);
  m_tree_out->Branch("boson_pt",&new_boson_pt);
  m_tree_out->Branch("boson_phi",&new_boson_phi);
  m_tree_out->Branch("boson_eta",&new_boson_eta);

  m_tree_out->Branch("n_V_dressed",&new_n_V_dressed);
  m_tree_out->Branch("V_dressed_m",&new_V_dressed_m);
  m_tree_out->Branch("V_dressed_pt",&new_V_dressed_pt);
  m_tree_out->Branch("V_dressed_phi",&new_V_dressed_phi);
  m_tree_out->Branch("V_dressed_eta",&new_V_dressed_eta);

  m_tree_out->Branch("n_V_undressed",&new_n_V_undressed);
  m_tree_out->Branch("V_undressed_m",&new_V_undressed_m);
  m_tree_out->Branch("V_undressed_pt",&new_V_undressed_pt);
  m_tree_out->Branch("V_undressed_phi",&new_V_undressed_phi);
  m_tree_out->Branch("V_undressed_eta",&new_V_undressed_eta);

  m_tree_out->Branch("n_jet",   &new_n_jet);
  m_tree_out->Branch("n_jet25", &new_n_jet25);
  m_tree_out->Branch("n_jet30", &new_n_jet30);
  m_tree_out->Branch("n_jet35", &new_n_jet35);
  m_tree_out->Branch("n_jet40", &new_n_jet40);
  m_tree_out->Branch("n_jet50", &new_n_jet50);

  m_tree_out->Branch("photon_MCTC", &new_photon_MCTC);
  m_tree_out->Branch("photon_boson_dR", &new_photon_boson_dR);
  m_tree_out->Branch("photon_lepton_dressed_dR", &new_photon_lepton_dressed_dR);
  m_tree_out->Branch("photon_lepton_undressed_dR", &new_photon_lepton_undressed_dR);

  //Register the output TTree
  CHECK(histSvc()->regTree("/MYSTREAM/"+treeTitleOut,m_tree_out));

  MapNgen(); //fill std::map with dsid->Ngen
  ATH_MSG_DEBUG ("Done Initializing");

  std::ostringstream runNumberss;
  runNumberss << run;
  outputName = m_currentSample+m_currentVariation+runNumberss.str();
/*
  for (auto reg : regions){
    ANA_CHECK (book (TH1F (Form("jj_mass_%s_nominal",reg.c_str()), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    ANA_CHECK (book (TH1F (Form("Z_mass_%s_nominal",reg.c_str()), ";M_{Z} [GeV];Entries", 50, 0, 500)));
    ANA_CHECK (book (TH1F (Form("boson_pT_%s_nominal",reg.c_str()), ";Boson p_{T} [GeV];Entries", 50, 0, 500)));
    ANA_CHECK (book (TH1F (Form("boson_mass_%s_nominal",reg.c_str()), ";Boson Mass [GeV];Entries", 50, 0, 500)));
    if (m_theoVariation){
      for(int i=0; i<115; i++)
        ANA_CHECK (book (TH1F (Form("all/jj_mass_%s_index_%d", reg.c_str(), i), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    for (auto var : variations)
        ANA_CHECK (book (TH1F (Form("scales/jj_mass_%s_%s",reg.c_str(),var.c_str()), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    for(int j=0; j<100; j++)
        ANA_CHECK (book (TH1F (Form("PDF/jj_mass_%s_pdf%d",reg.c_str(),j), ";m_{jj} [TeV];Entries", 50, 0, 5)));
    }
}*/

return StatusCode::SUCCESS;
}

StatusCode VBFVjetsAlg::finalize() {
  ATH_MSG_INFO ("Finalizing " << name() << "...");

  return StatusCode::SUCCESS;}

StatusCode VBFVjetsAlg::MapNgen(){
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

  StatusCode VBFVjetsAlg::execute() {
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
  if (run != m_runNumberInput){ //HACK to hard set the run number
    ATH_MSG_ERROR("VBFAnaysisAlg::execute: runNumber " << run << " != m_runNumberInput " << m_runNumberInput );
    run=m_runNumberInput;
}

npevents++;
bool passExp = false;
for (int i = 0; i < 9; i++) {
  int exponent = pow(10, i);
  passExp |= (npevents <= exponent && (npevents % exponent) == 0);
}
if (passExp) std::cout <<" Processed "<< npevents << " Events"<<std::endl;

if (364216 <= run && run <= 364229 && fabs(mconly_weight) > 100) mconly_weight = 1;

 // Number of generated events
 double NgenCorrected = 0.;
 double  weight = 1.;
 NgenCorrected = Ngen[run];
 crossSection = my_XsecDB->xsectTimesEff(run);//xs in pb
 if(NgenCorrected>0)  weight = crossSection/NgenCorrected;

 new_w = weight*mconly_weight;


  // JETS
  int njet=0, njet25=0, njet30=0, njet35=0, njet40=0, njet50=0;
  for (size_t jeti = 0; jeti < jet_pt->size(); jeti++)
    {
      njet++;
      if(jet_pt->at(jeti) > 25e3) njet25++;
      if(jet_pt->at(jeti) > 30e3) njet30++;
      if(jet_pt->at(jeti) > 35e3) njet35++;
      if(jet_pt->at(jeti) > 40e3) njet40++;
      if(jet_pt->at(jeti) > 50e3) njet50++;
  }
  new_n_jet=njet;
  new_n_jet25 = njet25;
  new_n_jet30 = njet30;
  new_n_jet35 = njet35;
  new_n_jet40 = njet40;
  new_n_jet50 = njet50;

  if (new_n_jet < 2) return StatusCode::SUCCESS;

 TLorentzVector vV(0, 0, 0, 0);
 TLorentzVector vV_boson(0, 0, 0, 0);
 TLorentzVector vV_unDressed(0, 0, 0, 0);

 std::vector<TLorentzVector> bosons;
 std::vector<TLorentzVector> leptons;
 std::vector<TLorentzVector> leptons_unDressed;
 std::vector<TLorentzVector> neutrinos;
 std::vector<TLorentzVector> photons;

new_photon_MCTC->clear();
new_photon_boson_dR->clear();
new_photon_lepton_dressed_dR->clear();
new_photon_lepton_undressed_dR->clear();


 const Int_t n_mc = truth_mc_pdg->size();
 Bool_t decayFound = false;

 for (int mc = 0; mc < n_mc; mc++) {

  // undressed leptons
  TLorentzVector p4(truth_mc_px->at(mc), truth_mc_py->at(mc), truth_mc_pz->at(mc), truth_mc_e->at(mc));

  //LEPTONS
  if ( (truth_mc_status->at(mc) == 1) && (abs(truth_mc_pdg->at(mc)) == 11 || abs(truth_mc_pdg->at(mc)) == 13) &&
    (truth_mc_origin->at(mc) == 12 || truth_mc_origin->at(mc) == 13) ){
    decayFound = true;
    leptons_unDressed.push_back(p4);
    // dressed leptons
    TLorentzVector p4_dressed(truth_mc_px_dressed->at(mc), truth_mc_py_dressed->at(mc), truth_mc_pz_dressed->at(mc), truth_mc_e_dressed->at(mc));
    leptons.push_back(p4_dressed);
    ATH_MSG_DEBUG( event << ": Found lepton with status 1");
  }

//NEUTRINOS
if ( (truth_mc_status->at(mc) == 1) && (abs(truth_mc_pdg->at(mc)) == 12 || abs(truth_mc_pdg->at(mc)) == 14 || abs(truth_mc_pdg->at(mc)) == 16) &&
    (truth_mc_origin->at(mc) == 12 || truth_mc_origin->at(mc) == 13) ){
    decayFound = true;
    neutrinos.push_back(p4);
    ATH_MSG_DEBUG(event << ": Found neutrino with status 1");
  }

//PHOTONS
// Dressing was handled already, here check what type of photons i have
if (  (truth_mc_status->at(mc) == 1) &&  (abs(truth_mc_pdg->at(mc) ) == 22) /*&&  (truth_mc_barcode->at(mc) < 10100)*/ ) {

  new_photon_MCTC->push_back(truth_mc_origin->at(mc));
  for (int i=0; i < leptons.size(); i++){

    Float_t dR = p4.DeltaR(leptons.at(i));
    Float_t dR_undressed = p4.DeltaR(leptons_unDressed.at(i));

    new_photon_lepton_undressed_dR->push_back(dR_undressed);
    if(truth_mc_barcode->at(mc) > 10100){
        photons.push_back(p4);
      new_photon_lepton_dressed_dR->push_back(dR);
    }

    if(dR<0.1 || dR_undressed<0.1){
    ATH_MSG_DEBUG(event << ": Dressed lep " << leptons.at(i).Px() << " " << leptons.at(i).Py() << " " << leptons.at(i).Pz());
    ATH_MSG_DEBUG(event << ": Undressed lep " << leptons_unDressed.at(i).Px() << " " << leptons_unDressed.at(i).Py() << " " << leptons_unDressed.at(i).Pz());
    ATH_MSG_DEBUG(event << ": Found photon with status " << truth_mc_status->at(mc) << " origin " << truth_mc_origin->at(mc)
      << " and dR(ph,Dressed lep"<< i << ")=" << dR);
    ATH_MSG_DEBUG(event << ": Found photon with status " << truth_mc_status->at(mc) << " origin " << truth_mc_origin->at(mc)
      << " and dR(ph,Undressed lep"<< i << ")=" << dR_undressed);
    TLorentzVector p4_new = p4 + leptons_unDressed.at(i);
    ATH_MSG_DEBUG(event << ": CHECK New dressed > " << p4_new.Px() << " " << p4_new.Py() << " " << p4_new.Pz());
    ATH_MSG_DEBUG(event << ": CHECK Old dressed > " << leptons.at(i).Px() << " " << leptons.at(i).Py() << " " << leptons.at(i).Pz());
  }
}
}

//VECTOR BOSONS
if (abs(truth_mc_pdg->at(mc)) >= 23 && abs(truth_mc_pdg->at(mc)) <= 24 && truth_mc_status->at(mc) == 3) {
  ATH_MSG_DEBUG(event << ": Found boson " << truth_mc_pdg->at(mc) << " with status " << truth_mc_status->at(mc) << " origin " << truth_mc_origin->at(mc));
  decayFound = true;
  bosons.push_back(p4);
}

} // end of mc loop

if (!decayFound) {
  throw std::runtime_error((string)TString::Format("no decay type found in the event = %d, mcid = %d", event, run));
}

int nDecay = 0;
int nDecay_boson = 0;

for (unsigned int iLep = 0; iLep < leptons.size(); iLep++) {
  nDecay++;
  vV += leptons[iLep];
  vV_unDressed += leptons_unDressed[iLep];
}
for (unsigned int iNu = 0; iNu < neutrinos.size(); iNu++) {
  nDecay++;
  vV += neutrinos[iNu];
  vV_unDressed += neutrinos[iNu];
}

if (bosons.size() > 0) {
  nDecay_boson++;
  vV_boson += bosons[0];
}


for (unsigned int iPh = 0; iPh < photons.size(); iPh++) {
  Float_t dR_boson = vV_boson.DeltaR(photons.at(iPh));
  new_photon_boson_dR->push_back(dR_boson);
}

// Fill Tree

  new_nbosons = nDecay_boson;
  new_boson_m = vV_boson.M();
  new_boson_pt = vV_boson.Pt();
  new_boson_phi = vV_boson.Phi();
  new_boson_eta = vV_boson.Eta();

  new_n_V_dressed = nDecay;
  new_V_dressed_m = vV.M();
  new_V_dressed_pt = vV.Pt();
  new_V_dressed_phi = vV.Phi();
  new_V_dressed_eta = vV.Eta();

  new_n_V_undressed = nDecay;
  new_V_undressed_m = vV_unDressed.M();
  new_V_undressed_pt = vV_unDressed.Pt();
  new_V_undressed_phi = vV_unDressed.Phi();
  new_V_undressed_eta = vV_unDressed.Eta();

bool PTV = (new_V_undressed_pt>100e3 || new_V_dressed_pt > 100e3 || new_boson_pt > 100e3);
if ( PTV && (jet_pt->at(0) > 80.0e3) && (jet_pt->at(1) > 50.0e3) && (jj_mass > 500e3) && (jj_deta > 3.8) )
  m_tree_out->Fill();


return StatusCode::SUCCESS;
}

StatusCode VBFVjetsAlg::beginInputFile() {

    ATH_MSG_INFO("VBFVjetsAlg::beginInputFile()");
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
  m_tree->SetBranchStatus("run",1 );
  m_tree->SetBranchStatus("event",1 );
  m_tree->SetBranchStatus("mconly_weight",1 );
  m_tree->SetBranchStatus("truth_mc_px",1 );
  m_tree->SetBranchStatus("truth_mc_py", 1 );
  m_tree->SetBranchStatus("truth_mc_pz",1 );
  m_tree->SetBranchStatus("truth_mc_e", 1 );
  m_tree->SetBranchStatus("truth_mc_px_dressed",1 );
  m_tree->SetBranchStatus("truth_mc_py_dressed",1 );
  m_tree->SetBranchStatus("truth_mc_pz_dressed",1 );
  m_tree->SetBranchStatus("truth_mc_e_dressed",1 );
  m_tree->SetBranchStatus("truth_mc_type", 1 );
  m_tree->SetBranchStatus("truth_mc_origin",1 );
  m_tree->SetBranchStatus("truth_mc_dyn_iso",1 );
  m_tree->SetBranchStatus("truth_mc_fix_iso",1 );
  m_tree->SetBranchStatus("truth_mc_pdg", 1 );
  m_tree->SetBranchStatus("truth_mc_status", 1 );
  m_tree->SetBranchStatus("truth_mc_barcode",1 );
  m_tree->SetBranchStatus("truth_V_simple_pt", 1 );
  m_tree->SetBranchStatus("jj_mass", 1);
  m_tree->SetBranchStatus("jj_dphi", 1);
  m_tree->SetBranchStatus("jj_deta", 1);
  m_tree->SetBranchStatus("njets",  1);
  m_tree->SetBranchStatus("njets25", 1);
  m_tree->SetBranchStatus("jet_E" , 1);
  m_tree->SetBranchStatus("jet_pt", 1);
  m_tree->SetBranchStatus("jet_eta", 1);
  m_tree->SetBranchStatus("jet_phi", 1);
  m_tree->SetBranchStatus("jet_m" , 1);
  m_tree->SetBranchStatus("jet_label", 1);

  m_tree->SetBranchAddress("run",&run );
  m_tree->SetBranchAddress("event",&event );
  m_tree->SetBranchAddress("mconly_weight",&mconly_weight );
  m_tree->SetBranchAddress("truth_mc_px", &truth_mc_px );
  m_tree->SetBranchAddress("truth_mc_py", &truth_mc_py);
  m_tree->SetBranchAddress("truth_mc_pz", &truth_mc_pz );
  m_tree->SetBranchAddress("truth_mc_e", &truth_mc_e );
  m_tree->SetBranchAddress("truth_mc_px_dressed", &truth_mc_px_dressed );
  m_tree->SetBranchAddress("truth_mc_py_dressed", &truth_mc_py_dressed );
  m_tree->SetBranchAddress("truth_mc_pz_dressed", &truth_mc_pz_dressed );
  m_tree->SetBranchAddress("truth_mc_e_dressed", &truth_mc_e_dressed );
  m_tree->SetBranchAddress("truth_mc_type", &truth_mc_type );
  m_tree->SetBranchAddress("truth_mc_origin",&truth_mc_origin );
  m_tree->SetBranchAddress("truth_mc_dyn_iso", &truth_mc_dyn_iso);
  m_tree->SetBranchAddress("truth_mc_fix_iso", &truth_mc_fix_iso);
  m_tree->SetBranchAddress("truth_mc_pdg", &truth_mc_pdg );
  m_tree->SetBranchAddress("truth_mc_status", &truth_mc_status);
  m_tree->SetBranchAddress("truth_mc_barcode", &truth_mc_barcode );
  m_tree->SetBranchAddress("truth_V_simple_pt", &truth_V_simple_pt );
  m_tree->SetBranchAddress("jj_mass", &jj_mass);
  m_tree->SetBranchAddress("jj_dphi", &jj_dphi);
  m_tree->SetBranchAddress("jj_deta", &jj_deta);
  m_tree->SetBranchAddress("njets",  &njets);
  m_tree->SetBranchAddress("njets25", &njets25);
  m_tree->SetBranchAddress("jet_E" , &jet_E);
  m_tree->SetBranchAddress("jet_pt", &jet_pt);
  m_tree->SetBranchAddress("jet_eta", &jet_eta);
  m_tree->SetBranchAddress("jet_phi", &jet_phi);
  m_tree->SetBranchAddress("jet_m" , &jet_m);
  m_tree->SetBranchAddress("jet_label", &jet_label);

  return StatusCode::SUCCESS;
}
