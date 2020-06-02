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


class SortByPt {
public:
   bool operator()(const TLorentzVector &a, const TLorentzVector &b) const { return (a.Perp() > b.Perp()); }
};


VBFVjetsAlg::VBFVjetsAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty( "currentSample", m_currentSample = "W_strong", "current sample");
  declareProperty( "runNumberInput", m_runNumberInput, "runNumber read from file name");
  declareProperty( "currentVariation", m_currentVariation = "Nominal", "Just truth tree here!" );
  declareProperty( "theoVariation", m_theoVariation = true, "Do theory systematic variations");
  declareProperty( "normFile", m_normFile = "/nfs/dust/atlas/user/othrif/vbf/myPP/source/VBFAnalysis/data/fout_v46.root", "path to a file with the number of events processed" );
  declareProperty( "skim", m_skim = 2, "Skim options: 0 No skimming applied, 1 Loose skimming, 2 tight skimming (default), 3 skimming matching ACE");
}

VBFVjetsAlg::~VBFVjetsAlg() {}

StatusCode VBFVjetsAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");

  cout<<"NAME of input tree in intialize ======="<<m_currentVariation<<endl;
  cout<< "CURRENT  sample === "<< m_currentSample<<endl;
  std::string   xSecFilePath = "dev/PMGTools/PMGxsecDB_mc15.txt";
  //std::string xSecFilePath = "VBFAnalysis/PMGxsecDB_mc16.txt"; // run from local file
  //std::string  xSecFilePath = "VBFAnalysis/PMGxsecDB_mc16_replace.txt";
  xSecFilePath = PathResolverFindCalibFile(xSecFilePath);
  my_XsecDB = new SUSY::CrossSectionDB(xSecFilePath);

  new_photon_MCTC = new std::vector<int>(0);
  new_photon_boson_dR = new std::vector<float>(0);
  new_photon_lepton_dressed_dR = new std::vector<float>(0);
  new_photon_lepton_undressed_dR = new std::vector<float>(0);

  jet_E_undress = new std::vector<float>(0);
  jet_pt_undress = new std::vector<float>(0);
  jet_eta_undress = new std::vector<float>(0);
  jet_phi_undress = new std::vector<float>(0);

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

  m_tree_out->Branch("jj_mass_undress",&jj_mass_undress);
  m_tree_out->Branch("jj_deta_undress",&jj_deta_undress);
  m_tree_out->Branch("jj_dphi_undress",&jj_dphi_undress);
  m_tree_out->Branch("jet_pt_undress",&jet_pt_undress);
  m_tree_out->Branch("jet_eta_undress",&jet_eta_undress);
  m_tree_out->Branch("jet_phi_undress",&jet_phi_undress);
  m_tree_out->Branch("jet_E_undress",&jet_E_undress);
  m_tree_out->Branch("n_jet25_undress", &n_jet25_undress);

  m_tree_out->Branch("met_et",&met_et);
  m_tree_out->Branch("met_phi",&met_phi);

  m_tree_out->Branch("w",&new_w);
  m_tree_out->Branch("EventWeight",&new_EventWeight);
  m_tree_out->Branch("crossSection",&new_crossSection);
  m_tree_out->Branch("nevents",&new_nevents);

//  m_tree_out->Branch("n_boson",&new_nbosons);
//  m_tree_out->Branch("boson_m",&new_boson_m);
//  m_tree_out->Branch("boson_pt",&new_boson_pt);
//  m_tree_out->Branch("boson_phi",&new_boson_phi);
//  m_tree_out->Branch("boson_eta",&new_boson_eta);

  //m_tree_out->Branch("n_V_dressed",&new_n_V_dressed);
  //m_tree_out->Branch("V_dressed_m",&new_V_dressed_m);
  m_tree_out->Branch("V_dressed_pt",&new_V_dressed_pt);
  //m_tree_out->Branch("V_dressed_phi",&new_V_dressed_phi);
  //m_tree_out->Branch("V_dressed_eta",&new_V_dressed_eta);

  //m_tree_out->Branch("n_V_undressed",&new_n_V_undressed);
  //m_tree_out->Branch("V_undressed_m",&new_V_undressed_m);
  m_tree_out->Branch("V_undressed_pt",&new_V_undressed_pt);
  //m_tree_out->Branch("V_undressed_phi",&new_V_undressed_phi);
  //m_tree_out->Branch("V_undressed_eta",&new_V_undressed_eta);

  m_tree_out->Branch("n_jet",   &new_n_jet);
  m_tree_out->Branch("n_jet25", &new_n_jet25);
  m_tree_out->Branch("n_jet30", &new_n_jet30);
  m_tree_out->Branch("n_jet35", &new_n_jet35);
  m_tree_out->Branch("n_jet40", &new_n_jet40);
  m_tree_out->Branch("n_jet50", &new_n_jet50);

 // m_tree_out->Branch("photon_MCTC", &new_photon_MCTC);
 // m_tree_out->Branch("photon_boson_dR", &new_photon_boson_dR);
 // m_tree_out->Branch("photon_lepton_dressed_dR", &new_photon_lepton_dressed_dR);
 // m_tree_out->Branch("photon_lepton_undressed_dR", &new_photon_lepton_undressed_dR);

  m_tree_out->Branch("met_nolep_et",&new_met_nolep_et);
  m_tree_out->Branch("met_nolep_phi",&new_met_nolep_phi);

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
 new_EventWeight = mconly_weight;
 new_crossSection = crossSection;
 new_nevents = NgenCorrected;



 TLorentzVector vV(0, 0, 0, 0);
 TLorentzVector vV_boson(0, 0, 0, 0);
 TLorentzVector vV_unDressed(0, 0, 0, 0);

 std::vector<TLorentzVector> bosons;
 std::vector<TLorentzVector> leptons;
 std::vector<TLorentzVector> leptons_unDressed;
 std::vector<TLorentzVector> neutrinos;
 std::vector<TLorentzVector> photons;
 std::vector<TLorentzVector> jets;

new_photon_MCTC->clear();
new_photon_boson_dR->clear();
new_photon_lepton_dressed_dR->clear();
new_photon_lepton_undressed_dR->clear();


 const Int_t n_mc = truth_mc_pdg->size();

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

// JETS
// Undress jets: remove muon or neutrino if within 0.4 of a jet
jets.clear();
for (size_t jeti = 0; jeti < jet_pt->size(); jeti++)
    {
      TLorentzVector jet_tmp; jet_tmp.SetPtEtaPhiE(jet_pt->at(jeti), jet_eta->at(jeti), jet_phi->at(jeti), jet_E->at(jeti));

      for (int mc = 0; mc < n_mc; mc++) {
        TLorentzVector p4(truth_mc_px->at(mc), truth_mc_py->at(mc), truth_mc_pz->at(mc), truth_mc_e->at(mc));
        if ( (truth_mc_status->at(mc) == 1) && (abs(truth_mc_pdg->at(mc)) == 13 || abs(truth_mc_pdg->at(mc)) == 12 || abs(truth_mc_pdg->at(mc)) == 14 || abs(truth_mc_pdg->at(mc)) == 16)){

          Float_t dR = p4.DeltaR(jet_tmp);
          if (dR<0.4){
            ATH_MSG_DEBUG(event << ": jet" << jeti << ": " << jet_tmp.Pt() << ", " << jet_tmp.Eta() << ", " << jet_tmp.Phi() << ", " << jet_tmp.E());
            ATH_MSG_DEBUG(event << ": mc" << mc << " " <<  truth_mc_pdg->at(mc)  << ": "<< p4.Pt() << ", " << p4.Eta() << ", " << p4.Phi() << ", " << p4.E());
            TLorentzVector new_jet_tmp = jet_tmp-p4;
            jet_tmp = new_jet_tmp;
            ATH_MSG_DEBUG(event << ": new jet: " << new_jet_tmp.Pt() << " " << new_jet_tmp.Eta() << " " << new_jet_tmp.Phi() << " " << new_jet_tmp.E());
          }
        }
      }
      jets.push_back(jet_tmp);
    }

std::sort(jets.begin(), jets.end(), SortByPt());

  jet_E_undress->clear();
  jet_pt_undress->clear();
  jet_eta_undress->clear();
  jet_phi_undress->clear();

int njet25un=0,njetun=0;
for (int ijet=0; ijet<jets.size(); ijet++){
  jet_E_undress->push_back(jets.at(ijet).E());
  jet_pt_undress->push_back(jets.at(ijet).Pt());
  jet_eta_undress->push_back(jets.at(ijet).Eta());
  jet_phi_undress->push_back(jets.at(ijet).Phi());
  if (jets.at(ijet).Pt() > 25.e3) njet25un++;
  njetun++;
}
n_jet25_undress = njet25un;

   if (new_n_jet < 2 && njetun>1)
     ATH_MSG_INFO(event << ": Got one event passing Njet" <<  new_n_jet << " " << n_jet25_undress);
   if (new_n_jet < 2 /*&& njetun<2*/) return StatusCode::SUCCESS;


jj_mass_undress = (jets.at(0)+jets.at(1)).M();
jj_deta_undress = fabs(jets.at(0).Eta() - jets.at(1).Eta());
jj_dphi_undress = fabs(jets.at(0).DeltaPhi(jets.at(1)));

ATH_MSG_DEBUG(event << ": old dijet " <<  jj_mass << " " << jj_deta << " " << jj_dphi);
ATH_MSG_DEBUG(event << ": new dijet " <<  jj_mass_undress << " " << jj_deta_undress << " " << jj_dphi_undress);



if (jets.at(1).Pt() > jets.at(0).Pt())
  ATH_MSG_ERROR(event << ": PROBLEM, jets not sorted properly!");


// Check bosons

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
   // if((1113151 == event || 1128230 == event || 201444 == event) )
//    ATH_MSG_INFO( event << ": Found lepton with status 1");
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
//if((1113151 == event || 1128230 == event || 201444 == event) ){
//  ATH_MSG_INFO(event << " Photon " << mc << " with (px,py,pz,E) = (" << truth_mc_px->at(mc) << "," << truth_mc_py->at(mc) << "," << truth_mc_pz->at(mc) << "," << truth_mc_e->at(mc) << ") and lepton " << i << " with (px,py,pz,E) = (" << leptons_unDressed.at(i).Px() << "," << leptons_unDressed.at(i).Py() << "," << leptons_unDressed.at(i).Pz() << "," << leptons_unDressed.at(i).E() <<  ") has DR=" << dR_undressed);
//}

    if(dR<0.1 || dR_undressed<0.1){
       /* if((1113151 == event || 1128230 == event || 201444 == event) ){
    ATH_MSG_INFO(event << ": Dressed lep " << leptons.at(i).Px() << " " << leptons.at(i).Py() << " " << leptons.at(i).Pz());
    ATH_MSG_INFO(event << ": Undressed lep " << leptons_unDressed.at(i).Px() << " " << leptons_unDressed.at(i).Py() << " " << leptons_unDressed.at(i).Pz());
    ATH_MSG_INFO(event << ": Found photon with status " << truth_mc_status->at(mc) << " origin " << truth_mc_origin->at(mc)
      << " and dR(ph,Dressed lep"<< i << ")=" << dR);
    ATH_MSG_INFO(event << ": Found photon with status " << truth_mc_status->at(mc) << " origin " << truth_mc_origin->at(mc)
      << " and dR(ph,Undressed lep"<< i << ")=" << dR_undressed);
  }*/
    TLorentzVector p4_new = p4 + leptons_unDressed.at(i);
          /*  if((1113151 == event || 1128230 == event || 201444 == event) ){
    ATH_MSG_INFO(event << ": CHECK New dressed > " << p4_new.Px() << " " << p4_new.Py() << " " << p4_new.Pz());
    ATH_MSG_INFO(event << ": CHECK Old dressed > " << leptons.at(i).Px() << " " << leptons.at(i).Py() << " " << leptons.at(i).Pz());
  }*/
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

new_met_nolep_et = -9999.;
new_met_nolep_phi = -9999.;
Float_t px = 0;
Float_t py = 0;

for (unsigned int iLep = 0; iLep < leptons.size(); iLep++) {
  nDecay++;
  vV += leptons[iLep];
  vV_unDressed += leptons_unDressed[iLep];

  px += leptons[iLep].Pt() * TMath::Cos(leptons[iLep].Phi());
  py += leptons[iLep].Pt() * TMath::Sin(leptons[iLep].Phi());
}

Float_t mpx = met_et*TMath::Cos(met_phi) + px;
Float_t mpy = met_et*TMath::Sin(met_phi) + py;
new_met_nolep_et = TMath::Sqrt(mpx*mpx+mpy*mpy);
new_met_nolep_phi = TMath::ATan2(mpy,mpx);

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

  // Variables to skim on:
  float PTV    = new_V_dressed_pt;
  float JetPt0 = jet_pt->at(0); //std::max(jet_pt->at(0),jets.at(0).Pt());
  float JetPt1 = jet_pt->at(1); //std::max(jet_pt->at(1),jets.at(1).Pt());
  float MJJ    = jj_mass; //std::max(jj_mass_undress, jj_mass);
  float ETAJJ  = jj_deta; //std::max(jj_deta_undress, jj_deta);
  float PHIJJ  = jj_dphi; //std::max(jj_dphi_undress, jj_dphi);


  //bool PTV = ((new_V_dressed_pt>150e3) || new_V_dressed_pt > 150e3 || new_boson_pt > 150e3);
  bool tightSkim = ( (PTV> 200e3) && (JetPt0> 80.0e3)    && (JetPt1> 50.0e3)  && (MJJ> 800e3)   && (ETAJJ> 3.8)  && (PHIJJ<2));
  bool looseSkim = ( (PTV> 200e3) && (JetPt0> 80.0e3)    && (JetPt1> 50.0e3)  && (MJJ> 800e3)   && (ETAJJ> 2.5)  && (PHIJJ<2.5));
  bool ace =       ( (PTV> 150e3) && (JetPt0> 100.0e3)   && (JetPt1> 50.0e3)  && (MJJ> 500e3)   && (ETAJJ> 2.5));
  bool passSkim = true;

  if(m_skim == 0){
    passSkim =  (MJJ> 3500e3);//true;
    //std::cout << "Got here! passSkim = true" << std::endl;
  }
  if(m_skim == 1){
    passSkim = looseSkim;
      //  std::cout << "Got here! passSkim = looseSkim" << std::endl;
  }
  if(m_skim == 2)
    passSkim = tightSkim;
  if(m_skim == 3)
    passSkim = ace;

  if ( passSkim ){
    m_tree_out->Fill();
  }

/*if (event == 1013191 || event == 1013369 || event == 1018864) // || event == 1021688 || event == 1028037 || event == 1036430 || event == 1040676 || event == 1040790 || event == 1048612 || event == 1051420 || event == 1053203 || event == 1058369 || event == 1067499 || event == 1069777 || event == 1073575 || event == 1074182 || event == 1086560 || event == 1090537 || event == 1091793 || event == 1092553 || event == 1093251 || event == 1095526 || event == 1096625 || event == 1108058 || event == 1112330 || event == 1118256 || event == 1123150 || event == 1127248 || event == 1131208 || event == 1132446 || event == 1134023 || event == 1136903 || event == 1139088 || event == 1139460 || event == 114664 || event == 1152632 || event == 1154077 || event == 1158359 || event == 1159855 || event == 1164014 || event == 1166433 || event == 1169503 || event == 1180737 || event == 1182870 || event == 1183312 || event == 1185824 || event == 11859 || event == 1193667 || event == 1208051 || event == 1209442 || event == 1217393 || event == 1218480 || event == 1219221 || event == 1229717 || event == 1229795 || event == 1231006 || event == 1232332 || event == 1244509 || event == 124612 || event == 1246269 || event == 1252432 || event == 125615 || event == 1258926 || event == 1269575 || event == 127259 || event == 1277346 || event == 1279475 || event == 1282725 || event == 1286677 || event == 1293346 || event == 1297965 || event == 1300467 || event == 1300801 || event == 1303113 || event == 1305170 || event == 1308861 || event == 1312834 || event == 1315563 || event == 1324883 || event == 1326641 || event == 1337867 || event == 1345608 || event == 134755 || event == 1356954 || event == 1359297 || event == 1360292 || event == 1361479 || event == 1363689 || event == 1365056 || event == 1367539 || event == 137713 || event == 1377993 || event == 1381397 || event == 1382938 || event == 1388681 || event == 1389224 || event == 1390444 || event == 139095 || event == 1391663 || event == 139537 || event == 1398943 || event == 140921 || event == 14281 || event == 151216 || event == 161996 || event == 162879 || event == 163722 || event == 177715 || event == 180509 || event == 184043 || event == 185115 || event == 185992 || event == 186892 || event == 191126 || event == 205445 || event == 221510 || event == 222090 || event == 223535 || event == 22496 || event == 228090 || event == 238888 || event == 25742 || event == 258419 || event == 259188 || event == 261641 || event == 262961 || event == 265910 || event == 267606 || event == 273710 || event == 282378 || event == 283562 || event == 284881 || event == 284982 || event == 288652 || event == 290315 || event == 291053 || event == 296312 || event == 302547 || event == 307668 || event == 310811 || event == 319444 || event == 324207 || event == 328218 || event == 333778 || event == 342705 || event == 343682 || event == 346567 || event == 346769 || event == 353000 || event == 356424 || event == 363747 || event == 369656 || event == 375903 || event == 375946 || event == 376389 || event == 378509 || event == 382040 || event == 384446 || event == 388462 || event == 389349 || event == 39 || event == 390662 || event == 393111 || event == 399133 || event == 402446 || event == 404607 || event == 404749 || event == 413017 || event == 417869 || event == 424769 || event == 42789 || event == 429660 || event == 43049 || event == 430524 || event == 431011 || event == 43749 || event == 443231 || event == 445187 || event == 447968 || event == 449750 || event == 449838 || event == 457199 || event == 459516 || event == 461563 || event == 464631 || event == 468708 || event == 472610 || event == 476392 || event == 47838 || event == 482837 || event == 489876 || event == 495608 || event == 501975 || event == 503436 || event == 508843 || event == 514236 || event == 518054 || event == 518108 || event == 519169 || event == 52037 || event == 528681 || event == 530478 || event == 533700 || event == 534009 || event == 534027 || event == 535441 || event == 539860 || event == 543992 || event == 544692 || event == 55149 || event == 563953 || event == 577082 || event == 577959 || event == 579681 || event == 582055 || event == 58335 || event == 586935 || event == 592997 || event == 606051 || event == 609675 || event == 610510 || event == 611380 || event == 611431 || event == 611732 || event == 612101 || event == 619702 || event == 621699 || event == 624584 || event == 625259 || event == 625533 || event == 631379 || event == 632007 || event == 632973 || event == 633806 || event == 65132 || event == 655765 || event == 658537 || event == 661033 || event == 665683 || event == 668403 || event == 670669 || event == 670840 || event == 672885 || event == 679152 || event == 680877 || event == 687540 || event == 690785 || event == 694749 || event == 695569 || event == 703372 || event == 706518 || event == 706561 || event == 707475 || event == 708551 || event == 709992 || event == 711989 || event == 712987 || event == 715028 || event == 72429 || event == 724515 || event == 725480 || event == 728012 || event == 728197 || event == 730304 || event == 730665 || event == 731494 || event == 734536 || event == 735968 || event == 745596 || event == 748070 || event == 750989 || event == 754785 || event == 759356 || event == 765065 || event == 76725 || event == 771313 || event == 778403 || event == 7789 || event == 782251 || event == 782531 || event == 783329 || event == 78627 || event == 787282 || event == 78976 || event == 79238 || event == 798327 || event == 79923 || event == 801339 || event == 805755 || event == 806832 || event == 807108 || event == 811649 || event == 813117 || event == 814947 || event == 817916 || event == 819403 || event == 820998 || event == 821052 || event == 829223 || event == 82974 || event == 834794 || event == 836446 || event == 838904 || event == 8401 || event == 840529 || event == 848924 || event == 859003 || event == 860388 || event == 860913 || event == 862085 || event == 862991 || event == 866328 || event == 868527 || event == 872016 || event == 872560 || event == 879158 || event == 881498 || event == 882783 || event == 886097 || event == 887315 || event == 898120 || event == 90074 || event == 90724 || event == 909059 || event == 913352 || event == 91869 || event == 930183 || event == 934186 || event == 937271 || event == 94423 || event == 946416 || event == 949869 || event == 951771 || event == 953377 || event == 957091 || event == 957297 || event == 958862 || event == 989088 || event == 989852 || event == 312489)

if (run == 312507)
  if((1113151 == event || 1128230 == event || 201444 == event) )
  //if ( (PTV> 200e3) && (JetPt0> 80.0e3)    && (JetPt1> 50.0e3)  && (MJJ>= 3500e3)   && (ETAJJ> 3.8)  && (PHIJJ<2))
{
std::cout << run << " " << event  << " " << new_crossSection  << " " <<  new_nevents << " " <<  new_EventWeight  << " " << jj_mass  << " " << jj_deta  << " " << jj_dphi  << " " << new_V_dressed_pt   << " " << new_V_dressed_pt  << " " << new_V_undressed_pt << std::endl;
}*/

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
  m_tree->SetBranchStatus("met_et", 1);
  m_tree->SetBranchStatus("met_phi", 1);

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
  m_tree->SetBranchAddress("met_et", &met_et);
  m_tree->SetBranchAddress("met_phi", &met_phi);

  return StatusCode::SUCCESS;
}
