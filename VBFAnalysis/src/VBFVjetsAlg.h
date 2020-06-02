#ifndef VBFANALYSIS_VBFVJETSALG_H
#define VBFANALYSIS_VBFVJETSALG_H 1

#include "AthAnalysisBaseComps/AthAnalysisAlgorithm.h"
#include "SUSYTools/SUSYCrossSection.h"

#include "TTree.h"
#include "TH1.h"
#include "TH2.h"
#include "TLorentzVector.h"
#include <vector>
#include <map>
#include <iostream>


using namespace std;

class VBFVjetsAlg: public ::AthAnalysisAlgorithm {
public:
    VBFVjetsAlg( const std::string& name, ISvcLocator* pSvcLocator );
    virtual ~VBFVjetsAlg();
    virtual StatusCode  initialize();     //once, before any input is loaded
    virtual StatusCode  beginInputFile(); //start of each input file, only metadata loaded
    virtual StatusCode  execute();
    virtual StatusCode  finalize();       //once, after all events processed
    virtual StatusCode  MapNgen();

private:
    bool m_theoVariation;
    int m_skim;
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

    // Input tree
   Int_t           run;
   Int_t           event;
   Float_t         mconly_weight;
   vector<float>   *truth_mc_px;
   vector<float>   *truth_mc_py;
   vector<float>   *truth_mc_pz;
   vector<float>   *truth_mc_e;
   vector<float>   *truth_mc_px_dressed;
   vector<float>   *truth_mc_py_dressed;
   vector<float>   *truth_mc_pz_dressed;
   vector<float>   *truth_mc_e_dressed;
   vector<int>     *truth_mc_type;
   vector<int>     *truth_mc_origin;
   vector<int>     *truth_mc_dyn_iso;
   vector<int>     *truth_mc_fix_iso;
   vector<int>     *truth_mc_pdg;
   vector<int>     *truth_mc_status;
   vector<int>     *truth_mc_barcode;
   Float_t         truth_V_simple_pt;
   Float_t         jj_mass;
   Float_t         jj_dphi;
   Float_t         jj_deta;
   Int_t           njets;
   Int_t           njets25;
   vector<float>   *jet_E;
   vector<float>   *jet_pt;
   vector<float>   *jet_eta;
   vector<float>   *jet_phi;
   vector<float>   *jet_m;
   vector<int>     *jet_label;
   Float_t         met_et;
   Float_t         met_phi;


    Double_t        crossSection;

    Float_t new_w;
    Float_t new_EventWeight;
    Float_t new_crossSection;
    Float_t new_nevents;

    Int_t   new_n_jet;
   Int_t   new_n_jet25;
   Int_t   new_n_jet30;
   Int_t   new_n_jet35;
   Int_t   new_n_jet40;
   Int_t   new_n_jet50;

   Int_t    new_nbosons;
   Double_t new_boson_m;
   Double_t new_boson_pt;
   Double_t new_boson_eta;
   Double_t new_boson_phi;

  Int_t new_n_V_dressed;
  Double_t new_V_dressed_m;
  Double_t new_V_dressed_pt;
  Double_t new_V_dressed_phi;
  Double_t new_V_dressed_eta;

  Int_t new_n_V_undressed;
  Double_t new_V_undressed_m;
  Double_t new_V_undressed_pt;
  Double_t new_V_undressed_phi;
  Double_t new_V_undressed_eta;

  vector<int>   *new_photon_MCTC;
  vector<float> *new_photon_boson_dR;
  vector<float> *new_photon_lepton_dressed_dR;
  vector<float> *new_photon_lepton_undressed_dR;

   Float_t         new_met_nolep_et;
   Float_t         new_met_nolep_phi;

   Float_t        jj_mass_undress;
   Float_t        jj_dphi_undress;
   Float_t        jj_deta_undress;
   vector<float>        *jet_pt_undress ;
   vector<float>        *jet_eta_undress;
   vector<float>        *jet_phi_undress;
   vector<float>        *jet_E_undress  ;
   Int_t n_jet25_undress;
};




#endif
