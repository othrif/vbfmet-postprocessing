#ifndef VBFANALYSIS_VBFTRUTHALG_H
#define VBFANALYSIS_VBFTRUTHALG_H 1

#include "AthAnalysisBaseComps/AthAnalysisAlgorithm.h"
#include "SUSYTools/SUSYCrossSection.h"

#include "TTree.h"
#include "TH1.h"
#include "TH2.h"
#include "TLorentzVector.h"
#include <vector>
#include <map>
#include <iostream>

#define muon_mass             105.6583715   // in MeV
#define electron_mass         0.510998928   // in MeV
#define nu_mass         0   // in MeV

const Int_t MAXJETS = 20;
const Int_t MAXLEPT = 10;

using namespace std;

class VBFTruthAlg: public ::AthAnalysisAlgorithm {
public:
    VBFTruthAlg( const std::string& name, ISvcLocator* pSvcLocator );
    virtual ~VBFTruthAlg();
    virtual StatusCode  initialize();     //once, before any input is loaded
    virtual StatusCode  beginInputFile(); //start of each input file, only metadata loaded
    virtual StatusCode  execute();
    virtual StatusCode  finalize();       //once, after all events processed
    virtual StatusCode  MapNgen();

private:
    bool m_theoVariation;
    bool noSkim;
    std::map< std::string, std::vector<TH1*> >  h_theoVariations;  //!
    TH1D* make1DHist (TString name, TString title, unsigned nbins, float low, float high);
    int npevents = 0;
    long int nFileEvt = 0;
    long int nFileEvtTot = 0;
    TTree *m_tree = 0;
    TTree *m_tree_out = 0;
    SUSY::CrossSectionDB *my_XsecDB;
    TString m_treeName = "MiniNtuple";
    TString outputFileName = "ntuple";

  TH1D *h_Gen;
  std::map<int,double> Ngen;

    //output tree
    std::string outputName;
    std::string m_currentVariation;
    std::string m_normFile;
    std::string m_currentSample;
    UInt_t m_runNumberInput;
    std::string treeNameOut="nominal";
    std::string treeTitleOut="nominal";

    Int_t runNumber;
    Float_t new_w;
    Float_t new_w_noxsec;
    Float_t new_xsec;
    Float_t new_sumw;

    //  TRUTH Ntuples
  // Declaration of leaf types
    ULong64_t       EventNumber;
    UInt_t          RunNumber;
    Double_t        crossSection;
    Double_t        new_crossSection;
    Float_t         EventWeight;
    UInt_t          ChannelNumber;
    vector<float>   *EventWeightSys;
    Int_t           njets;
    vector<float>   *jet_E;
    vector<float>   *jet_pt;
    vector<float>   *jet_eta;
    vector<float>   *jet_phi;
    vector<float>   *jet_m;
    vector<int>     *jet_label;
    Int_t           nels;
    vector<float>   *el_m;
    vector<float>   *el_pt;
    vector<float>   *el_eta;
    vector<float>   *el_phi;
    vector<unsigned int> *el_type;
    vector<unsigned int> *el_origin;
    vector<float>   *el_ptcone30;
    vector<float>   *el_etcone20;
    vector<int>     *el_pdgid;
    Int_t           nmus;
    vector<float>   *mu_m;
    vector<float>   *mu_pt;
    vector<float>   *mu_eta;
    vector<float>   *mu_phi;
    vector<unsigned int> *mu_type;
    vector<unsigned int> *mu_origin;
    vector<float>   *mu_ptcone30;
    vector<float>   *mu_etcone20;
    vector<int>     *mu_pdgid;
    Int_t           nbosons;
    vector<float>   *boson_m;
    vector<float>   *boson_pt;
    vector<float>   *boson_eta;
    vector<float>   *boson_phi;
    vector<int>     *boson_pdgid;
    Int_t           nnus;
    vector<float>   *nu_e;
    vector<float>   *nu_m;
    vector<float>   *nu_pt;
    vector<float>   *nu_eta;
    vector<float>   *nu_phi;
    vector<unsigned int> *nu_type;
    vector<unsigned int> *nu_origin;
    vector<int>     *nu_pdgid;
    Float_t         met_et;
    Float_t         met_phi;
    vector<float>   *parton_x1;
    vector<float>   *parton_x2;
    vector<float>   *parton_xf1;
    vector<float>   *parton_xf2;
    vector<float>   *parton_Q;
    vector<int>     *parton_pdgid1;
    vector<int>     *parton_pdgid2;
    vector<int>     *parton_pdfid1;
    vector<int>     *parton_pdfid2;
    vector<int>     *parton_pp;

    Bool_t passVjetsFilter;
    Float_t truthF_jj_mass=-9999;
    Float_t truthF_jj_deta=-9999;
    Float_t truthF_jj_dphi=-9999;

   // List of branches
   TBranch        *b_EventNumber;   //!
   TBranch        *b_RunNumber;   //!
   TBranch        *b_crossSection;   //!
   TBranch        *b_EventWeight;   //!
   TBranch        *b_ChannelNumber;   //!
   TBranch        *b_EventWeightSys;   //!
   TBranch        *b_njets;   //!
   TBranch        *b_jet_E;   //!
   TBranch        *b_jet_pt;   //!
   TBranch        *b_jet_eta;   //!
   TBranch        *b_jet_phi;   //!
   TBranch        *b_jet_m;   //!
   TBranch        *b_jet_label;   //!
   TBranch        *b_nels;   //!
   TBranch        *b_el_m;   //!
   TBranch        *b_el_pt;   //!
   TBranch        *b_el_eta;   //!
   TBranch        *b_el_phi;   //!
   TBranch        *b_el_type;   //!
   TBranch        *b_el_origin;   //!
   TBranch        *b_el_ptcone30;   //!
   TBranch        *b_el_etcone20;   //!
   TBranch        *b_el_pdgid;   //!
   TBranch        *b_nmus;   //!
   TBranch        *b_mu_m;   //!
   TBranch        *b_mu_pt;   //!
   TBranch        *b_mu_eta;   //!
   TBranch        *b_mu_phi;   //!
   TBranch        *b_mu_type;   //!
   TBranch        *b_mu_origin;   //!
   TBranch        *b_mu_ptcone30;   //!
   TBranch        *b_mu_etcone20;   //!
   TBranch        *b_mu_pdgid;   //!
   TBranch        *b_nbosons;   //!
   TBranch        *b_boson_m;   //!
   TBranch        *b_boson_pt;   //!
   TBranch        *b_boson_eta;   //!
   TBranch        *b_boson_phi;   //!
   TBranch        *b_boson_pdgid;   //!
   TBranch        *b_nnus;   //!
   TBranch        *b_nu_e;   //!
   TBranch        *b_nu_m;   //!
   TBranch        *b_nu_pt;   //!
   TBranch        *b_nu_eta;   //!
   TBranch        *b_nu_phi;   //!
   TBranch        *b_nu_type;   //!
   TBranch        *b_nu_origin;   //!
   TBranch        *b_nu_pdgid;   //!
   TBranch        *b_met_et;   //!
   TBranch        *b_met_phi;   //!
   TBranch        *b_parton_x1;   //!
   TBranch        *b_parton_x2;   //!
   TBranch        *b_parton_xf1;   //!
   TBranch        *b_parton_xf2;   //!
   TBranch        *b_parton_Q;   //!
   TBranch        *b_parton_pdgid1;   //!
   TBranch        *b_parton_pdgid2;   //!
   TBranch        *b_parton_pdfid1;   //!
   TBranch        *b_parton_pdfid2;   //!
   TBranch        *b_parton_pp;   //!

   // New ntuple
   ULong64_t       new_EventNumber;
   UInt_t          new_RunNumber;
   UInt_t          new_ChannelNumber;
   Int_t           new_njets;
   vector<float>   *new_jet_E;
   vector<float>   *new_jet_pt;
   vector<float>   *new_jet_eta;
   vector<float>   *new_jet_phi;
   Int_t           new_nels;
   vector<float>   *new_el_m;
   vector<float>   *new_el_pt;
   vector<float>   *new_el_eta;
   vector<float>   *new_el_phi;
   vector<int>     *new_el_pdgid;
   vector<float>   *new_el_charge;
   Int_t           new_nmus;
   vector<float>   *new_mu_m;
   vector<float>   *new_mu_pt;
   vector<float>   *new_mu_eta;
   vector<float>   *new_mu_phi;
   vector<int>     *new_mu_pdgid;
   vector<float>   *new_mu_charge;
   Int_t           new_nbosons;
   vector<float>   *new_boson_m;
   vector<float>   *new_boson_pt;
   vector<float>   *new_boson_eta;
   vector<float>   *new_boson_phi;
   vector<int>     *new_boson_pdgid;
   Int_t           new_nnus;
   vector<float>   *new_nu_e;
   vector<float>   *new_nu_m;
   vector<float>   *new_nu_pt;
   vector<float>   *new_nu_eta;
   vector<float>   *new_nu_phi;
   vector<int>     *new_nu_pdgid;
   vector<float>   *new_nu_charge;
   Float_t         new_met_et;
   Float_t         new_met_phi;
   Float_t         new_met_nolep_et;
   Float_t         new_met_nolep_phi;
   Float_t         new_jj_mass;
   Float_t         new_jj_deta;
   Float_t         new_jj_dphi;
   Float_t         new_met_significance;
   vector<float>         *new_lep_jet_dR;
   Float_t         new_MV;
   Float_t         new_PTV;
   Bool_t          new_hasZ;

   Float_t         weight;


   Float_t new_ee_pt ;
   Float_t new_ee_eta;
   Float_t new_ee_phi;
   Float_t new_ee_m  ;
   Float_t new_mumu_pt ;
   Float_t new_mumu_eta;
   Float_t new_mumu_phi;
   Float_t new_mumu_m  ;
   Float_t new_nunu_pt ;
   Float_t new_nunu_eta;
   Float_t new_nunu_phi;
   Float_t new_nunu_m  ;
   Int_t   new_n_jet;
   Int_t   new_n_jet25;
   Int_t   new_n_jet30;
   Int_t   new_n_jet35;
   Int_t   new_n_jet40;
   Int_t   new_n_jet50;

   Int_t  useMerged=-1;


};

// defines the jet collection in the event
struct jet_info{
  int num_jets;
  int index[MAXJETS];
  Double_t pT[MAXJETS];
  Double_t phi[MAXJETS];
  Double_t eta[MAXJETS];
  Double_t E[MAXJETS];
};
typedef struct jet_info my_jets;

struct short_jet {
  double pt;
  int ind;
};
typedef struct short_jet srtJt;

// defines the lepton collection in the event
struct lepton_info {
  int num_leptons;
  int index[2 * MAXLEPT];
  Double_t pT[2 * MAXLEPT];
  Double_t phi[2 * MAXLEPT];
  Double_t eta[2 * MAXLEPT];
  bool is_electron[2 * MAXLEPT];
  float charge[2 * MAXLEPT];
  bool has_Z_OS;
  double Mll;
  double PTV;
};
typedef struct lepton_info my_leptons;

struct short_lep {
  bool is_electron;
  double pT;
  int ind;
};


int jet_pt_comparator(const void * a, const void * b) {
  Float_t pt1 = ((srtJt*) a)->pt;
  Float_t pt2 = ((srtJt*) b)->pt;
  if (pt1 < pt2)
    return 1;
else if (pt1 == pt2)
    return 0;
else
    return -1;
}

void sortJets(my_jets *jet) {
  srtJt jet_srt[2 * MAXLEPT];
  my_jets temp_jet;
  for (int i = 0; i < jet->num_jets; i++) {
    jet_srt[i].ind = i;
    jet_srt[i].pt = jet->pT[i];
}
qsort(jet_srt, jet->num_jets, sizeof(srtJt), jet_pt_comparator);
for (int i = 0; i < jet->num_jets; i++) {
    temp_jet.index[i] = jet->index[jet_srt[i].ind];
    temp_jet.pT[i] = jet->pT[jet_srt[i].ind];
    temp_jet.phi[i] = jet->phi[jet_srt[i].ind];
    temp_jet.eta[i] = jet->eta[jet_srt[i].ind];
    temp_jet.E[i] = jet->E[jet_srt[i].ind];
}
for (int i = 0; i < jet->num_jets; i++) {
    jet->index[i] = temp_jet.index[i];
    jet->pT[i] = temp_jet.pT[i];
    jet->phi[i] = temp_jet.phi[i];
    jet->eta[i] = temp_jet.eta[i];
    jet->E[i] = temp_jet.E[i];
}
return;
}

void sortLeptons(my_leptons *lep) {
  srtJt jet_srt[2 * MAXLEPT];
  my_leptons temp_lep;

  for (int i = 0; i < lep->num_leptons; i++) {
    jet_srt[i].ind = i;
    jet_srt[i].pt = lep->pT[i];
}

qsort(jet_srt, lep->num_leptons, sizeof(srtJt), jet_pt_comparator);


for (int i = 0; i < lep->num_leptons; i++) {
    temp_lep.index[i] = lep->index[jet_srt[i].ind];
    temp_lep.pT[i] = lep->pT[jet_srt[i].ind];
    temp_lep.phi[i] = lep->phi[jet_srt[i].ind];
    temp_lep.eta[i] = lep->eta[jet_srt[i].ind];
    temp_lep.is_electron[i] = lep->is_electron[jet_srt[i].ind];
    temp_lep.charge[i] = lep->charge[jet_srt[i].ind];
}

for (int i = 0; i < lep->num_leptons; i++) {
    lep->index[i] = temp_lep.index[i];
    lep->pT[i] = temp_lep.pT[i];
    lep->phi[i] = temp_lep.phi[i];
    lep->eta[i] = temp_lep.eta[i];
    lep->is_electron[i] = temp_lep.is_electron[i];
    lep->charge[i] = temp_lep.charge[i];
}
return;
}

void containsZ(my_leptons *lep) {

  TLorentzVector P_lep0;
  TLorentzVector P_lep1;
  TLorentzVector P_lep2;

  lep->has_Z_OS = false;
  lep->Mll = -9999;
  lep->PTV = -9999;

  if (lep->num_leptons < 2)
    return;

double best_M = -1;
double M;
double PTV;

int lept_count = 0;
for (int i = 0; i < lep->num_leptons && lept_count < 5; i++)
    lept_count++;


  for (int i = 0; i < lept_count ; i++) //Only the first five leptons are taken into account
    for (int j = i + 1; j < lept_count ; j++) //Only the first five leptons are taken into account
    {

        if (lep->is_electron[i] == lep->is_electron[j] && lep->charge[i] * lep->charge[j] < 0 ){
          if (!lep->is_electron[i]) { //muons -----------------------------------------------------------
            P_lep1.SetPtEtaPhiM(lep->pT[i],lep->eta[i],lep->phi[i],muon_mass);
            P_lep2.SetPtEtaPhiM(lep->pT[j],lep->eta[j],lep->phi[j],muon_mass);
          } else { //electrons -------------------------------------------------------------------------
            P_lep1.SetPtEtaPhiM(lep->pT[i],lep->eta[i],lep->phi[i],electron_mass);
            P_lep2.SetPtEtaPhiM(lep->pT[j],lep->eta[j],lep->phi[j],electron_mass);
        }
        TLorentzVector lep_sum = P_lep1 + P_lep2;
        M = (lep_sum).M();
        PTV = (lep_sum).Pt();

/*        if (best_M < 0) {
            best_M = M;
            lep->Mll = M;
        }*/

          // pick the pair closest to the Z mass if more than one Z
        if (fabs(M - 91000.) < fabs(best_M - 91000.)) {
            best_M = M;
            lep->Mll = M;
            lep->PTV = PTV;
        }
        if (M  < 116.2*1.e3 && M > 66.2*1.e3 &&  lep->charge[i] * lep->charge[j] < 0){
            lep->has_Z_OS = true;
        }
    }
}

}

void computejj(my_jets *jet, Float_t &e_DiJetMass, Float_t &e_JetsDEta, Float_t &e_JetsDPhi)
{

 std::vector<TLorentzVector> jet_tlv;
 TLorentzVector              jet_tmp;

 if (jet->num_jets >= 2 ) {
  jet_tmp.SetPtEtaPhiE(jet->pT[0],jet->eta[0],jet->phi[0],jet->E[0]);
  jet_tlv.push_back(jet_tmp);
  jet_tmp.SetPtEtaPhiE(jet->pT[1],jet->eta[1],jet->phi[1],jet->E[1]);
  jet_tlv.push_back(jet_tmp);

  TLorentzVector jet_sum = jet_tlv.at(0) + jet_tlv.at(1);
  e_JetsDEta             = fabs(jet_tlv.at(0).Eta() - jet_tlv.at(1).Eta());
  e_DiJetMass            = (jet_sum).M();
  e_JetsDPhi             = fabs(jet_tlv.at(0).DeltaPhi(jet_tlv.at(1)));
}
else{
    e_DiJetMass = -9999.;
    e_JetsDEta = -9999.;
    e_JetsDPhi = -9999.;
}

}





#endif
