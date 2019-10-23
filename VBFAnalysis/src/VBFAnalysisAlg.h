#ifndef VBFANALYSIS_VBFANALYSISALG_H
#define VBFANALYSIS_VBFANALYSISALG_H 1

#include "AthAnalysisBaseComps/AthAnalysisAlgorithm.h"
#include <AsgTools/AnaToolHandle.h>
#include "SUSYTools/SUSYCrossSection.h"
#include "BoostedJetTaggers/IJetQGTagger.h"
#include "BoostedJetTaggers/JetQGTagger.h"
#include "xAODJet/Jet.h"
#include "xAODJet/JetContainer.h"
#include "xAODCore/AuxContainerBase.h"

//Example ROOT Includes
//#include "TTree.h"
//#include "TH1D.h"
// For making the systematics list and looping through it
#include "PATInterfaces/SystematicsUtil.h"
#include "PATInterfaces/SystematicRegistry.h"

#include "SignalSystHelper.h"
#include "VJetsSystHelper.h"
#include "TTree.h"
#include "TH1D.h"
#include <vector>
#include <map>
#include <iostream>

using namespace std;

class VBFAnalysisAlg: public ::AthAnalysisAlgorithm {
 public:
  VBFAnalysisAlg( const std::string& name, ISvcLocator* pSvcLocator );
  virtual ~VBFAnalysisAlg();

  ///uncomment and implement methods as required

                                        //IS EXECUTED:
  virtual StatusCode  initialize();     //once, before any input is loaded
  virtual StatusCode  beginInputFile(); //start of each input file, only metadata loaded
  virtual StatusCode  MapNgen();
  //virtual StatusCode  firstExecute();   //once, after first eventdata is loaded (not per file)
  virtual StatusCode  execute();        //per event
  //virtual StatusCode  endInputFile();   //end of each input file
  //virtual StatusCode  metaDataStop();   //when outputMetaStore is populated by MetaDataTools
  virtual StatusCode  finalize();       //once, after all events processed

  ///Other useful methods provided by base class are:
  ///evtStore()        : ServiceHandle to main event data storegate
  ///inputMetaStore()  : ServiceHandle to input metadata storegate
  ///outputMetaStore() : ServiceHandle to output metadata storegate
  ///histSvc()         : ServiceHandle to output ROOT service (writing TObjects)
  ///currentFile()     : TFile* to the currently open input file
  ///retrieveMetadata(...): See twiki.cern.ch/twiki/bin/view/AtlasProtected/AthAnalysisBase#ReadingMetaDataInCpp
  double weightXETrigSF(const float met_pt, unsigned metRunNumber, int syst);
  void computeMETj( Float_t met_phi,  std::vector<Float_t>* jet_phi, double &e_met_j1_dphi, double &e_met_j2_dphi);
  float GetDPhi(const float phi1, const float phi2);

 private:

  int npevents = 0;
  long int nFileEvt = 0;
  long int nFileEvtTot = 0;
  Bool_t m_isMC = true;
  Bool_t m_UseExtMC = false;
  Bool_t m_UseExtMGVjet = false;
  bool is2015;
  bool is2016;
  bool m_LooseSkim = true;
  bool m_extraVars = true;
  bool m_contLep   = false;
  bool m_QGTagger   = true;
  bool m_METTrigPassThru = false;
  TTree *m_tree = 0;
  TTree *m_tree_out = 0;
  SignalSystHelper     my_signalSystHelper;
  VJetsSystHelper      my_vjSystHelper;


  SUSY::CrossSectionDB *my_XsecDB;
  std::map<TString,asg::AnaToolHandle<CP::IJetQGTagger> >      m_jetQGTool;                     //!
  std::map<TString,CP::SystematicSet>        m_systSet;                     //!
  //  const TFile outputFile;
  TString m_treeName = "MiniNtuple";
  TString outputFileName = "ntuple";

  TH1D *h_Gen;
  std::map<int,double> Ngen;
  std::map<int,TH1D*>  Ngen_filter;

  //Maps for types of Tree things
  std::map<TString, int>   tMapInt;
  std::map<TString, Float_t> tMapFloat;
  std::map<TString, Float_t> tMapFloatW;
  vector<TString> m_qgVars;
  std::vector<TString> m_vjVariations;

  // jet container
  xAOD::JetContainer* m_newJets;
  xAOD::AuxContainerBase* m_newJetsAux;

   //Example algorithm property, see constructor for declaration:
   //int m_nProperty = 0;

   //Example histogram, see initialize method for registration to output histSvc
   //TH1D* m_myHist = 0;
   //TTree* m_myTree = 0;

  //output tree
  std::string outputName;
  std::string m_currentVariation;
  std::string m_normFile;
  std::string m_currentSample;
  Int_t m_runNumberInput;
  std::string treeNameOut="nominal";
  std::string treeTitleOut="nominal";
  std::string m_mcCampaign;
  bool m_theoVariation;
  bool m_oneTrigMuon;

  Float_t crossSection;
  Double_t weight;
  Float_t w;
  Double_t vjWeight;
  Float_t met_significance;
  Int_t trigger_met;
  Int_t trigger_met_encoded;
  Int_t trigger_met_encodedv2;
  Int_t l1_met_trig_encoded;
  Int_t lumiBlock;
  Int_t bcid;
  Int_t BCIDDistanceFromFront;
  Bool_t passBatman;
  Bool_t passVjetsFilter;
  Bool_t passVjetsFilterTauEl;
  Bool_t passVjetsPTV;
  Float_t MGVTruthPt;
  Float_t SherpaVTruthPt;
  Float_t MGMergeWeightIncl;
  Float_t MGMergeWeightFilt;
  Bool_t in_vy_overlap;
  Bool_t in_vy_overlap_iso;
  Int_t FlavourFilter;

  Int_t nParton;
  Int_t runNumber;
  Int_t randomRunNumber;
  ULong64_t eventNumber;
  Float_t averageIntPerXing;
  Float_t mcEventWeight;
  Int_t HTXS_prodMode;
  Int_t HTXS_errorCode;
  Int_t HTXS_Stage1_1_Fine_Category_pTjet25;
  Float_t nloEWKWeight;
  Float_t puSyst2018Weight;
  Float_t puWeight;
  Float_t jvtSFWeight;
  Float_t fjvtSFWeight;
  Float_t fjvtSFTighterWeight;
  Float_t eleANTISF;
  Float_t elSFWeight;
  Float_t muSFWeight;
  Float_t elSFTrigWeight;
  Float_t muSFTrigWeight;
  Float_t phSFWeight;
  Float_t xeSFTrigWeight;
  Float_t xeSFTrigWeight__1up;
  Float_t xeSFTrigWeight__1down;
  Float_t xeSFTrigWeight_nomu;
  Float_t xeSFTrigWeight_nomu__1up;
  Float_t xeSFTrigWeight_nomu__1down;
  Int_t n_vx;
  Int_t passJetCleanLoose;
  Int_t passJetCleanTight;
  Int_t trigger_HLT_xe100_mht_L1XE50;
  Int_t trigger_HLT_xe110_mht_L1XE50;
  Int_t trigger_HLT_xe90_mht_L1XE50;
  Int_t trigger_HLT_xe70_mht;
  Int_t trigger_HLT_noalg_L1J400;
  Int_t trigger_lep;
  Int_t lep_trig_match;
  Int_t passGRL;
  Int_t passPV;
  Int_t passDetErr;
  Int_t n_jet;
  Int_t n_bjet;
  Int_t n_el;
  Int_t n_mu;
  Int_t n_el_w;
  Int_t n_mu_w;
  Int_t n_ph;
  Int_t n_tau;
  Double_t jj_mass;
  Double_t jj_deta;
  Double_t jj_dphi;
  Double_t met_tst_j1_dphi;
  Double_t met_tst_j2_dphi;
  Double_t met_tst_nolep_j1_dphi;
  Double_t met_tst_nolep_j2_dphi;
  Double_t met_cst_jet;
  Float_t met_tst_et;
  Float_t met_tst_nolep_et;
  Float_t met_tst_phi;
  Float_t met_tst_nolep_phi;
  Float_t max_mj_over_mjj;
  Float_t maxCentrality;
  // to fill min_mj_over_mjj,minCentrality,met_tenacious_tst_j1_dphi,met_tenacious_tst_j2_dphi
  //met_tenacious_tst_nolep_j1_dphi,met_tenacious_tst_nolep_j2_dphi,met_tenacious_tst_nolep_et,
  //met_tenacious_tst_nolep_phi
  // extra vars
  Int_t   n_baseel=0;
  Int_t   n_basemu=0;
  Int_t   n_baseel_noOR=0;
  Int_t   n_basemu_noOR=0;
  Int_t   n_baseel_iso=0;
  Int_t   n_basemu_iso=0;
  Float_t met_soft_tst_et=-9999;
  Float_t met_soft_tst_phi=-9999;
  Float_t met_soft_tst_sumet=-9999;
  Float_t met_tenacious_tst_et=-9999;
  Float_t met_tenacious_tst_phi=-9999;
  Float_t met_tenacious_tst_j1_dphi=-9999;
  Float_t met_tenacious_tst_j2_dphi=-9999;
  Float_t met_tenacious_tst_nolep_j1_dphi=-9999;
  Float_t met_tenacious_tst_nolep_j2_dphi=-9999;
  Float_t met_tenacious_tst_nolep_et=-9999;
  Float_t met_tenacious_tst_nolep_phi=-9999;
  Float_t met_tighter_tst_et=-9999;
  Float_t met_tighter_tst_phi=-9999;
  Float_t met_tight_tst_et=-9999;
  Float_t met_tight_tst_phi=-9999;
  Float_t met_tighter_tst_nolep_et=-9999;
  Float_t met_tighter_tst_nolep_phi=-9999;
  Float_t met_tight_tst_nolep_et=-9999;
  Float_t met_tight_tst_nolep_phi=-9999;
  Double_t metsig_tst=-9999;

  Float_t met_truth_et=-9999;
  Float_t met_truth_phi=-9999;
  Float_t met_truth_sumet=-9999;
  Float_t GenMET_pt=-9999;
  Double_t truth_jj_mass=-9999;
  Double_t truth_jj_dphi=-9999;
  Double_t truth_j2_pt=-9999;
  Double_t truthloMG_jj_mass=-9999;
  Double_t truthloMG_jj_dphi=-9999;
  Double_t truthloMG_j2_pt=-9999;

  // optimization variables
  std::vector<Float_t>* j3_centrality;
  std::vector<Float_t>* j3_dRj1;
  std::vector<Float_t>* j3_dRj2;
  std::vector<Float_t>* j3_minDR;
  std::vector<Float_t>* j3_mjclosest;
  std::vector<Float_t>* j3_min_mj;
  std::vector<Float_t>* j3_min_mj_over_mjj;
  Float_t mj34;
  Float_t max_j_eta;

  // container vars
  std::vector<Float_t>* contmu_pt;
  std::vector<Float_t>* contmu_eta;
  std::vector<Float_t>* contmu_phi;
  std::vector<Float_t>* contel_pt;
  std::vector<Float_t>* contel_eta;
  std::vector<Float_t>* contel_phi;

  // extra vars
  std::vector<Float_t>* basemu_pt;
  std::vector<Float_t>* basemu_eta;
  std::vector<Float_t>* basemu_phi;
  std::vector<Int_t>* basemu_charge;
  std::vector<Float_t>* basemu_z0;
  std::vector<Float_t>* basemu_d0sig;
  std::vector<Float_t>* basemu_ptvarcone20;
  std::vector<Float_t>* basemu_ptvarcone30;
  std::vector<Float_t>* basemu_topoetcone20;
  std::vector<Float_t>* basemu_topoetcone30;
  std::vector<Int_t>* basemu_type;
  std::vector<Int_t>* basemu_truthType;
  std::vector<Int_t>* basemu_truthOrigin;

  std::vector<Float_t>* baseel_pt;
  std::vector<Float_t>* baseel_eta;
  std::vector<Float_t>* baseel_phi;
  std::vector<Int_t>* baseel_charge;
  std::vector<Float_t>* baseel_z0;
  std::vector<Float_t>* baseel_d0sig;
  std::vector<Float_t>* baseel_ptvarcone20;
  std::vector<Float_t>* baseel_ptvarcone30;
  std::vector<Float_t>* baseel_topoetcone20;
  std::vector<Float_t>* baseel_topoetcone30;
  std::vector<Int_t>* baseel_truthType;
  std::vector<Int_t>* baseel_truthOrigin;

  std::vector<Float_t>* mu_charge;
  std::vector<Float_t>* mu_pt;
  std::vector<Float_t>* mu_phi;
  std::vector<Float_t>* el_charge;
  std::vector<Float_t>* el_pt;
  std::vector<Float_t>* el_phi;
  std::vector<Float_t>* mu_eta;
  std::vector<Float_t>* el_eta;
  std::vector<Float_t>* jet_pt;
  std::vector<Float_t>* jet_phi;
  std::vector<Float_t>* jet_eta;
  std::vector<Float_t>* jet_m;
  std::vector<Float_t>* jet_jvt;
  std::vector<Float_t>* jet_fjvt;
  std::vector<Float_t>* jet_timing;
  std::vector<Int_t>* jet_passJvt;
  std::vector<Int_t>* jet_PartonTruthLabelID;
  std::vector<Int_t>* jet_ConeTruthLabelID;
  std::vector<std::vector<unsigned short> >* jet_NTracks;
  std::vector<unsigned short>* jet_NTracks_PV;
  std::vector<std::vector<Float_t> >* jet_SumPtTracks;
  std::vector<Float_t>* jet_SumPtTracks_PV;
  std::vector<Float_t>* jet_TrackWidth;
  std::vector<Float_t>* jet_HECFrac;
  std::vector<Float_t>* jet_EMFrac;
  std::vector<Float_t>* jet_fch;
  std::vector<Float_t>* jet_btag_weight;
  std::vector<Float_t>* jet_TracksC1;
  std::vector<Float_t>* jet_truthjet_pt;
  std::vector<Float_t>* jet_truthjet_eta;
  std::vector<Int_t>*   jet_truthjet_nCharged;

  std::vector<Float_t>* truth_jet_pt;
  std::vector<Float_t>* truth_jet_eta;
  std::vector<Float_t>* truth_jet_phi;
  std::vector<Float_t>* truth_jet_m;

  std::vector<Float_t>* truth_tau_pt;
  std::vector<Float_t>* truth_tau_eta;
  std::vector<Float_t>* truth_tau_phi;
  std::vector<Int_t>* truth_tau_status;
  std::vector<Float_t>* truth_mu_pt;
  std::vector<Float_t>* truth_mu_eta;
  std::vector<Float_t>* truth_mu_phi;
  std::vector<Float_t>* truth_ph_pt;
  std::vector<Float_t>* truth_ph_eta;
  std::vector<Float_t>* truth_ph_phi;
  std::vector<Float_t>* truth_el_pt;
  std::vector<Float_t>* truth_el_eta;
  std::vector<Float_t>* truth_el_phi;
  std::vector<Int_t>* truth_el_status;

  std::vector<Float_t>* outtau_pt;
  std::vector<Float_t>* outtau_phi;
  std::vector<Float_t>* outtau_eta;
  std::vector<Float_t>* ph_pt;
  std::vector<Float_t>* ph_phi;
  std::vector<Float_t>* ph_eta;
  std::vector<Float_t>* tau_pt;
  std::vector<Float_t>* tau_phi;
  std::vector<Float_t>* tau_eta;

  std::vector<Float_t>* mcEventWeights;

  TBranch    *b_mu_charge;
  TBranch    *b_mu_pt;
  TBranch    *b_mu_phi;
  TBranch    *b_el_charge;
  TBranch    *b_el_pt;
  TBranch    *b_el_phi;
  TBranch    *b_jet_pt;
  TBranch    *b_jet_phi;
  TBranch    *b_jet_eta;
  TBranch    *b_jet_jvt;
  TBranch    *b_jet_fjvt;
  TBranch    *b_jet_timing;
  TBranch    *b_jet_passJvt;

  TBranch    *b_truth_jet_pt;
  TBranch    *b_truth_jet_eta;
  TBranch    *b_truth_jet_phi;
  TBranch    *b_truth_jet_m;

  TBranch    *b_ph_pt;
  TBranch    *b_ph_eta;
  TBranch    *b_ph_phi;

  TBranch    *b_tau_pt;
  TBranch    *b_tau_eta;
  TBranch    *b_tau_phi;

  TBranch    *b_mcEventWeights;

  Float_t         truth_V_dressed_pt=-9999;
  TBranch        *b_truth_V_dressed_pt;   //!


};

#endif //> !VBFANALYSIS_VBFANALYSISALG_H
