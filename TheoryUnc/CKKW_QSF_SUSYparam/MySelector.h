//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Nov 20 14:11:35 2019 by ROOT version 5.34/38
// from TTree Z_strongNominal/Z_strongNominal
// found on file: Z_strong.root
//////////////////////////////////////////////////////////

#ifndef MySelector_h
#define MySelector_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TH1.h>

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TH1.h>
#include <iostream>
#include <fstream>

// Header file for the classes stored in the TTree if any.
#include <vector>
#include <map>

// Fixed size dimensions of array or collections stored in the TTree if any.

class MySelector : public TSelector {
public :
   TTreeReader     fReader;  //!the tree reader
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain

   Int_t nentries=0;
   Long64_t        fProcessed=0;//!
   std::vector<TString> vjSysts;
   std::vector <TString> regions;
   std::vector <TString> samples;
   std::map < TString, std::map < TString, std::map <TString, TH1F*> > > h_vjSyst;
   TProofOutputFile *m_prooffile; //!
   TFile *m_outfile; //!
   std::map < TString, Bool_t> isRegion;//!
   std::map < TString, Bool_t > b_samples; //!
   TString sample_name;
   TString suffix;

   // Declaration of leaf types
   Float_t         w;
   Double_t        vjWeight;
   Float_t         puSyst2018Weight;
   Float_t         xeSFTrigWeight;
   Float_t         xeSFTrigWeight_nomu;
   Float_t         puWeight;
   Float_t         xeSFTrigWeight__1up;
   Float_t         xeSFTrigWeight__1down;
   Float_t         xeSFTrigWeight_nomu__1up;
   Float_t         xeSFTrigWeight_nomu__1down;
   Float_t         eleANTISF;
   Int_t           runNumber;
   Int_t           randomRunNumber;
   ULong64_t       eventNumber;
   Int_t           trigger_met;
   Int_t           trigger_met_encodedv2;
   Int_t           l1_met_trig_encoded;
   Int_t           trigger_met_encoded;
   Bool_t          passBatman;
   Bool_t          passVjetsFilter;
   Bool_t          passVjetsFilterTauEl;
   Bool_t          passVjetsPTV;
   Float_t         MGVTruthPt;
   Bool_t          in_vy_overlap;
   Int_t           trigger_lep;
   Int_t           lep_trig_match;
   Int_t           passJetCleanTight;
   Float_t         averageIntPerXing;
   Int_t           n_vx;
   Int_t           n_jet;
   Int_t           n_el;
   Int_t           n_mu;
   Int_t           n_el_w;
   Int_t           n_mu_w;
   Int_t           n_ph;
   Int_t           n_tau;
   Double_t        jj_mass;
   Double_t        jj_deta;
   Double_t        jj_dphi;
   Double_t        met_tst_j1_dphi;
   Double_t        met_tst_j2_dphi;
   Double_t        met_tst_nolep_j1_dphi;
   Double_t        met_tst_nolep_j2_dphi;
   Float_t         met_tst_et;
   Float_t         met_tst_nolep_et;
   Float_t         met_tst_phi;
   Float_t         met_tst_nolep_phi;
   Double_t        met_cst_jet;
   Float_t         met_soft_tst_et;
   vector<float>   *mu_charge;
   vector<float>   *mu_pt;
   vector<float>   *el_charge;
   vector<float>   *el_pt;
   vector<float>   *jet_pt;
   vector<float>   *jet_timing;
   vector<float>   *mu_phi;
   vector<float>   *el_phi;
   vector<float>   *mu_eta;
   vector<float>   *el_eta;
   vector<float>   *jet_phi;
   vector<float>   *jet_eta;
   vector<float>   *jet_m;
   vector<float>   *jet_jvt;
   Float_t         met_significance;
   Float_t         max_mj_over_mjj;
   Float_t         maxCentrality;
   Int_t           n_baseel;
   Int_t           n_basemu;
   Int_t           n_el_baseline_noOR;
   Int_t           n_mu_baseline_noOR;
   Int_t           n_el_baseline_iso;
   Int_t           n_mu_baseline_iso;
   Int_t           n_bjet;
   vector<float>   *jet_btag_weight;
   vector<float>   *j3_centrality;
   vector<float>   *j3_min_mj_over_mjj;
   vector<float>   *j3_dRj1;
   vector<float>   *j3_dRj2;
   vector<float>   *j3_minDR;
   vector<float>   *j3_mjclosest;
   vector<float>   *j3_min_mj;
   Float_t         mj34;
   Float_t         max_j_eta;
   Int_t           lb;
   Int_t           bcid;
   Int_t           BCIDDistanceFromFront;
   vector<int>     *jet_PartonTruthLabelID;
   vector<int>     *jet_ConeTruthLabelID;
   vector<float>   *jet_fjvt;
   vector<float>   *basemu_pt;
   vector<float>   *basemu_eta;
   vector<float>   *basemu_phi;
   vector<int>     *basemu_charge;
   vector<float>   *basemu_ptvarcone30;
   vector<float>   *baseel_pt;
   vector<float>   *baseel_eta;
   vector<float>   *baseel_phi;
   vector<int>     *baseel_charge;
   vector<float>   *baseel_ptvarcone20;
   vector<float>   *basemu_ptvarcone20;
   vector<float>   *basemu_z0;
   vector<float>   *basemu_d0sig;
   vector<float>   *basemu_topoetcone20;
   vector<float>   *basemu_topoetcone30;
   vector<int>     *basemu_type;
   vector<int>     *basemu_truthOrigin;
   vector<int>     *basemu_truthType;
   vector<float>   *baseel_z0;
   vector<float>   *baseel_d0sig;
   vector<float>   *baseel_topoetcone20;
   vector<int>     *baseel_truthOrigin;
   vector<int>     *baseel_truthType;
   vector<float>   *ph_pt;
   vector<float>   *ph_phi;
   vector<float>   *ph_eta;
   vector<float>   *tau_pt;
   vector<float>   *tau_phi;
   vector<float>   *tau_eta;
   Float_t         met_soft_tst_phi;
   Float_t         met_soft_tst_sumet;
   Float_t         met_tenacious_tst_et;
   Float_t         met_tenacious_tst_phi;
   Float_t         met_tenacious_tst_nolep_et;
   Float_t         met_tenacious_tst_nolep_phi;
   Float_t         met_tenacious_tst_j1_dphi;
   Float_t         met_tenacious_tst_j2_dphi;
   Float_t         met_tenacious_tst_nolep_j1_dphi;
   Float_t         met_tenacious_tst_nolep_j2_dphi;
   Float_t         met_tight_tst_et;
   Float_t         met_tight_tst_phi;
   Float_t         met_tight_tst_nolep_et;
   Float_t         met_tight_tst_nolep_phi;
   Double_t        metsig_tst;
   vector<float>   *truth_tau_pt;
   vector<float>   *truth_tau_eta;
   vector<float>   *truth_tau_phi;
   vector<float>   *truth_el_pt;
   vector<float>   *truth_el_eta;
   vector<float>   *truth_el_phi;
   vector<float>   *truth_mu_pt;
   vector<float>   *truth_mu_eta;
   vector<float>   *truth_mu_phi;
   vector<float>   *truth_ph_pt;
   vector<float>   *truth_ph_eta;
   vector<float>   *truth_ph_phi;
   Float_t         GenMET_pt;
   Float_t         met_truth_et;
   Float_t         met_truth_phi;
   Float_t         met_truth_sumet;
   vector<float>   *truth_jet_pt;
   vector<float>   *truth_jet_eta;
   vector<float>   *truth_jet_phi;
   vector<float>   *truth_jet_m;
   Double_t        truth_jj_mass;
   Double_t        truth_jj_dphi;
   Double_t        truth_j2_pt;
   Int_t           n_jet_truth;
   Double_t        truthloMG_jj_mass;
   Double_t        truthloMG_jj_dphi;
   Double_t        truthloMG_j2_pt;
   Float_t         truth_V_dressed_pt;
   Float_t         weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down;
   Float_t         welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up;
   Float_t         wjvtSFWeightJET_JvtEfficiency__1down;
   Float_t         wjvtSFWeightJET_JvtEfficiency__1up;
   Float_t         wfjvtSFWeightJET_fJvtEfficiency__1down;
   Float_t         wfjvtSFTighterWeightJET_fJvtEfficiency__1down;
   Float_t         wfjvtSFWeightJET_fJvtEfficiency__1up;
   Float_t         wfjvtSFTighterWeightJET_fJvtEfficiency__1up;
   Float_t         wmuSFWeightMUON_EFF_BADMUON_STAT__1down;
   Float_t         wmuSFWeightMUON_EFF_BADMUON_STAT__1up;
   Float_t         wmuSFWeightMUON_EFF_BADMUON_SYS__1down;
   Float_t         wmuSFWeightMUON_EFF_BADMUON_SYS__1up;
   Float_t         wmuSFWeightMUON_EFF_ISO_STAT__1down;
   Float_t         wmuSFWeightMUON_EFF_ISO_STAT__1up;
   Float_t         wmuSFWeightMUON_EFF_ISO_SYS__1down;
   Float_t         wmuSFWeightMUON_EFF_ISO_SYS__1up;
   Float_t         wmuSFWeightMUON_EFF_RECO_STAT__1down;
   Float_t         wmuSFWeightMUON_EFF_RECO_STAT__1up;
   Float_t         wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1down;
   Float_t         wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1up;
   Float_t         wmuSFWeightMUON_EFF_RECO_SYS__1down;
   Float_t         wmuSFWeightMUON_EFF_RECO_SYS__1up;
   Float_t         wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1down;
   Float_t         wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1up;
   Float_t         wmuSFWeightMUON_EFF_TTVA_STAT__1down;
   Float_t         wmuSFWeightMUON_EFF_TTVA_STAT__1up;
   Float_t         wmuSFWeightMUON_EFF_TTVA_SYS__1down;
   Float_t         wmuSFWeightMUON_EFF_TTVA_SYS__1up;
   Float_t         wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1down;
   Float_t         wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1down;
   Float_t         wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1up;
   Float_t         wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1up;
   Float_t         wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1down;
   Float_t         wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1down;
   Float_t         wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1up;
   Float_t         wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1up;
   Float_t         wphSFWeightPH_EFF_ID_Uncertainty__1down;
   Float_t         wphSFWeightPH_EFF_ID_Uncertainty__1up;
   Float_t         wphSFWeightPH_EFF_ISO_Uncertainty__1down;
   Float_t         wphSFWeightPH_EFF_ISO_Uncertainty__1up;
   Float_t         wpuWeightPRW_DATASF__1down;
   Float_t         wpuWeightPRW_DATASF__1up;
   Float_t         wnloEWKWeight__1up;
   Float_t         wnloEWKWeight__1down;
   Float_t         wpuSyst2018Weight__1up;
   Float_t         wpuSyst2018Weight__1down;
   Float_t         wvjets_d1kappa_EW__1up;
   Float_t         wvjets_d1kappa_EW__1down;
   Float_t         wvjets_d2kappa_EW__1up;
   Float_t         wvjets_d2kappa_EW__1down;
   Float_t         wvjets_d3kappa_EW__1up;
   Float_t         wvjets_d3kappa_EW__1down;
   Float_t         wvjets_d1K_NNLO__1up;
   Float_t         wvjets_d1K_NNLO__1down;
   Float_t         wvjets_d2K_NNLO__1up;
   Float_t         wvjets_d2K_NNLO__1down;
   Float_t         wvjets_d3K_NNLO__1up;
   Float_t         wvjets_d3K_NNLO__1down;
   Float_t         wvjets_dK_NNLO_mix__1up;
   Float_t         wvjets_dK_NNLO_mix__1down;
   Float_t         wvjets_dK_PDF__1up;
   Float_t         wvjets_dK_PDF__1down;
   Float_t         wvjets_ckkw15;
   Float_t         wvjets_ckkw30;
   Float_t         wvjets_fac025;
   Float_t         wvjets_fac4;
   Float_t         wvjets_renorm025;
   Float_t         wvjets_renorm4;
   Float_t         wvjets_qsf025;
   Float_t         wvjets_qsf4;

   // List of branches
   TBranch        *b_w;   //!
   TBranch        *b_vjWeight;   //!
   TBranch        *b_puSyst2018Weight;   //!
   TBranch        *b_xeSFTrigWeight;   //!
   TBranch        *b_xeSFTrigWeight_nomu;   //!
   TBranch        *b_puWeight;   //!
   TBranch        *b_xeSFTrigWeight__1up;   //!
   TBranch        *b_xeSFTrigWeight__1down;   //!
   TBranch        *b_xeSFTrigWeight_nomu__1up;   //!
   TBranch        *b_xeSFTrigWeight_nomu__1down;   //!
   TBranch        *b_eleANTISF;   //!
   TBranch        *b_runNumber;   //!
   TBranch        *b_randomRunNumber;   //!
   TBranch        *b_eventNumber;   //!
   TBranch        *b_trigger_met;   //!
   TBranch        *b_trigger_met_encodedv2;   //!
   TBranch        *b_l1_met_trig_encoded;   //!
   TBranch        *b_trigger_met_encoded;   //!
   TBranch        *b_passBatman;   //!
   TBranch        *b_passVjetsFilter;   //!
   TBranch        *b_passVjetsFilterTauEl;   //!
   TBranch        *b_passVjetsPTV;   //!
   TBranch        *b_MGVTruthPt;   //!
   TBranch        *b_in_vy_overlap;   //!
   TBranch        *b_trigger_lep;   //!
   TBranch        *b_lep_trig_match;   //!
   TBranch        *b_passJetCleanTight;   //!
   TBranch        *b_averageIntPerXing;   //!
   TBranch        *b_n_vx;   //!
   TBranch        *b_n_jet;   //!
   TBranch        *b_n_el;   //!
   TBranch        *b_n_mu;   //!
   TBranch        *b_n_el_w;   //!
   TBranch        *b_n_mu_w;   //!
   TBranch        *b_n_ph;   //!
   TBranch        *b_n_tau;   //!
   TBranch        *b_jj_mass;   //!
   TBranch        *b_jj_deta;   //!
   TBranch        *b_jj_dphi;   //!
   TBranch        *b_met_tst_j1_dphi;   //!
   TBranch        *b_met_tst_j2_dphi;   //!
   TBranch        *b_met_tst_nolep_j1_dphi;   //!
   TBranch        *b_met_tst_nolep_j2_dphi;   //!
   TBranch        *b_met_tst_et;   //!
   TBranch        *b_met_tst_nolep_et;   //!
   TBranch        *b_met_tst_phi;   //!
   TBranch        *b_met_tst_nolep_phi;   //!
   TBranch        *b_met_cst_jet;   //!
   TBranch        *b_met_soft_tst_et;   //!
   TBranch        *b_mu_charge;   //!
   TBranch        *b_mu_pt;   //!
   TBranch        *b_el_charge;   //!
   TBranch        *b_el_pt;   //!
   TBranch        *b_jet_pt;   //!
   TBranch        *b_jet_timing;   //!
   TBranch        *b_mu_phi;   //!
   TBranch        *b_el_phi;   //!
   TBranch        *b_mu_eta;   //!
   TBranch        *b_el_eta;   //!
   TBranch        *b_jet_phi;   //!
   TBranch        *b_jet_eta;   //!
   TBranch        *b_jet_m;   //!
   TBranch        *b_jet_jvt;   //!
   TBranch        *b_met_significance;   //!
   TBranch        *b_max_mj_over_mjj;   //!
   TBranch        *b_maxCentrality;   //!
   TBranch        *b_n_baseel;   //!
   TBranch        *b_n_basemu;   //!
   TBranch        *b_n_el_baseline_noOR;   //!
   TBranch        *b_n_mu_baseline_noOR;   //!
   TBranch        *b_n_el_baseline_iso;   //!
   TBranch        *b_n_mu_baseline_iso;   //!
   TBranch        *b_n_bjet;   //!
   TBranch        *b_jet_btag_weight;   //!
   TBranch        *b_j3_centrality;   //!
   TBranch        *b_j3_min_mj_over_mjj;   //!
   TBranch        *b_j3_dRj1;   //!
   TBranch        *b_j3_dRj2;   //!
   TBranch        *b_j3_minDR;   //!
   TBranch        *b_j3_mjclosest;   //!
   TBranch        *b_j3_min_mj;   //!
   TBranch        *b_mj34;   //!
   TBranch        *b_max_j_eta;   //!
   TBranch        *b_lb;   //!
   TBranch        *b_bcid;   //!
   TBranch        *b_BCIDDistanceFromFront;   //!
   TBranch        *b_jet_PartonTruthLabelID;   //!
   TBranch        *b_jet_ConeTruthLabelID;   //!
   TBranch        *b_jet_fjvt;   //!
   TBranch        *b_basemu_pt;   //!
   TBranch        *b_basemu_eta;   //!
   TBranch        *b_basemu_phi;   //!
   TBranch        *b_basemu_charge;   //!
   TBranch        *b_basemu_ptvarcone30;   //!
   TBranch        *b_baseel_pt;   //!
   TBranch        *b_baseel_eta;   //!
   TBranch        *b_baseel_phi;   //!
   TBranch        *b_baseel_charge;   //!
   TBranch        *b_baseel_ptvarcone20;   //!
   TBranch        *b_basemu_ptvarcone20;   //!
   TBranch        *b_basemu_z0;   //!
   TBranch        *b_basemu_d0sig;   //!
   TBranch        *b_basemu_topoetcone20;   //!
   TBranch        *b_basemu_topoetcone30;   //!
   TBranch        *b_basemu_type;   //!
   TBranch        *b_basemu_truthOrigin;   //!
   TBranch        *b_basemu_truthType;   //!
   TBranch        *b_baseel_z0;   //!
   TBranch        *b_baseel_d0sig;   //!
   TBranch        *b_baseel_topoetcone20;   //!
   TBranch        *b_baseel_truthOrigin;   //!
   TBranch        *b_baseel_truthType;   //!
   TBranch        *b_ph_pt;   //!
   TBranch        *b_ph_phi;   //!
   TBranch        *b_ph_eta;   //!
   TBranch        *b_tau_pt;   //!
   TBranch        *b_tau_phi;   //!
   TBranch        *b_tau_eta;   //!
   TBranch        *b_met_soft_tst_phi;   //!
   TBranch        *b_met_soft_tst_sumet;   //!
   TBranch        *b_met_tenacious_tst_et;   //!
   TBranch        *b_met_tenacious_tst_phi;   //!
   TBranch        *b_met_tenacious_tst_nolep_et;   //!
   TBranch        *b_met_tenacious_tst_nolep_phi;   //!
   TBranch        *b_met_tenacious_tst_j1_dphi;   //!
   TBranch        *b_met_tenacious_tst_j2_dphi;   //!
   TBranch        *b_met_tenacious_tst_nolep_j1_dphi;   //!
   TBranch        *b_met_tenacious_tst_nolep_j2_dphi;   //!
   TBranch        *b_met_tight_tst_et;   //!
   TBranch        *b_met_tight_tst_phi;   //!
   TBranch        *b_met_tight_tst_nolep_et;   //!
   TBranch        *b_met_tight_tst_nolep_phi;   //!
   TBranch        *b_metsig_tst;   //!
   TBranch        *b_truth_tau_pt;   //!
   TBranch        *b_truth_tau_eta;   //!
   TBranch        *b_truth_tau_phi;   //!
   TBranch        *b_truth_el_pt;   //!
   TBranch        *b_truth_el_eta;   //!
   TBranch        *b_truth_el_phi;   //!
   TBranch        *b_truth_mu_pt;   //!
   TBranch        *b_truth_mu_eta;   //!
   TBranch        *b_truth_mu_phi;   //!
   TBranch        *b_truth_ph_pt;   //!
   TBranch        *b_truth_ph_eta;   //!
   TBranch        *b_truth_ph_phi;   //!
   TBranch        *b_GenMET_pt;   //!
   TBranch        *b_met_truth_et;   //!
   TBranch        *b_met_truth_phi;   //!
   TBranch        *b_met_truth_sumet;   //!
   TBranch        *b_truth_jet_pt;   //!
   TBranch        *b_truth_jet_eta;   //!
   TBranch        *b_truth_jet_phi;   //!
   TBranch        *b_truth_jet_m;   //!
   TBranch        *b_truth_jj_mass;   //!
   TBranch        *b_truth_jj_dphi;   //!
   TBranch        *b_truth_j2_pt;   //!
   TBranch        *b_n_jet_truth;   //!
   TBranch        *b_truthloMG_jj_mass;   //!
   TBranch        *b_truthloMG_jj_dphi;   //!
   TBranch        *b_truthloMG_j2_pt;   //!
   TBranch        *b_truth_V_dressed_pt;   //!
   TBranch        *b_weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down;   //!
   TBranch        *b_welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up;   //!
   TBranch        *b_wjvtSFWeightJET_JvtEfficiency__1down;   //!
   TBranch        *b_wjvtSFWeightJET_JvtEfficiency__1up;   //!
   TBranch        *b_wfjvtSFWeightJET_fJvtEfficiency__1down;   //!
   TBranch        *b_wfjvtSFTighterWeightJET_fJvtEfficiency__1down;   //!
   TBranch        *b_wfjvtSFWeightJET_fJvtEfficiency__1up;   //!
   TBranch        *b_wfjvtSFTighterWeightJET_fJvtEfficiency__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_BADMUON_STAT__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_BADMUON_STAT__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_BADMUON_SYS__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_BADMUON_SYS__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_ISO_STAT__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_ISO_STAT__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_ISO_SYS__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_ISO_SYS__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_RECO_STAT__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_RECO_STAT__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_RECO_SYS__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_RECO_SYS__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_TTVA_STAT__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_TTVA_STAT__1up;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_TTVA_SYS__1down;   //!
   TBranch        *b_wmuSFWeightMUON_EFF_TTVA_SYS__1up;   //!
   TBranch        *b_wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1down;   //!
   TBranch        *b_wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1down;   //!
   TBranch        *b_wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1up;   //!
   TBranch        *b_wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1up;   //!
   TBranch        *b_wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1down;   //!
   TBranch        *b_wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1down;   //!
   TBranch        *b_wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1up;   //!
   TBranch        *b_wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1up;   //!
   TBranch        *b_wphSFWeightPH_EFF_ID_Uncertainty__1down;   //!
   TBranch        *b_wphSFWeightPH_EFF_ID_Uncertainty__1up;   //!
   TBranch        *b_wphSFWeightPH_EFF_ISO_Uncertainty__1down;   //!
   TBranch        *b_wphSFWeightPH_EFF_ISO_Uncertainty__1up;   //!
   TBranch        *b_wpuWeightPRW_DATASF__1down;   //!
   TBranch        *b_wpuWeightPRW_DATASF__1up;   //!
   TBranch        *b_wnloEWKWeight__1up;   //!
   TBranch        *b_wnloEWKWeight__1down;   //!
   TBranch        *b_wpuSyst2018Weight__1up;   //!
   TBranch        *b_wpuSyst2018Weight__1down;   //!
   TBranch        *b_wvjets_d1kappa_EW__1up;   //!
   TBranch        *b_wvjets_d1kappa_EW__1down;   //!
   TBranch        *b_wvjets_d2kappa_EW__1up;   //!
   TBranch        *b_wvjets_d2kappa_EW__1down;   //!
   TBranch        *b_wvjets_d3kappa_EW__1up;   //!
   TBranch        *b_wvjets_d3kappa_EW__1down;   //!
   TBranch        *b_wvjets_d1K_NNLO__1up;   //!
   TBranch        *b_wvjets_d1K_NNLO__1down;   //!
   TBranch        *b_wvjets_d2K_NNLO__1up;   //!
   TBranch        *b_wvjets_d2K_NNLO__1down;   //!
   TBranch        *b_wvjets_d3K_NNLO__1up;   //!
   TBranch        *b_wvjets_d3K_NNLO__1down;   //!
   TBranch        *b_wvjets_dK_NNLO_mix__1up;   //!
   TBranch        *b_wvjets_dK_NNLO_mix__1down;   //!
   TBranch        *b_wvjets_dK_PDF__1up;   //!
   TBranch        *b_wvjets_dK_PDF__1down;   //!
   TBranch        *b_wvjets_ckkw15;   //!
   TBranch        *b_wvjets_ckkw30;   //!
   TBranch        *b_wvjets_fac025;   //!
   TBranch        *b_wvjets_fac4;   //!
   TBranch        *b_wvjets_renorm025;   //!
   TBranch        *b_wvjets_renorm4;   //!
   TBranch        *b_wvjets_qsf025;   //!
   TBranch        *b_wvjets_qsf4;   //!

   MySelector(TTree * /*tree*/ =0) : fChain(0) { }
   virtual ~MySelector() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();
   virtual void    WriteTable(TString suffix = "");
   virtual void    AssignRunToSamples();

   ClassDef(MySelector,0);
};

#endif

#ifdef MySelector_cxx
void MySelector::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   mu_charge = 0;
   mu_pt = 0;
   el_charge = 0;
   el_pt = 0;
   jet_pt = 0;
   jet_timing = 0;
   mu_phi = 0;
   el_phi = 0;
   mu_eta = 0;
   el_eta = 0;
   jet_phi = 0;
   jet_eta = 0;
   jet_m = 0;
   jet_jvt = 0;
   jet_btag_weight = 0;
   j3_centrality = 0;
   j3_min_mj_over_mjj = 0;
   j3_dRj1 = 0;
   j3_dRj2 = 0;
   j3_minDR = 0;
   j3_mjclosest = 0;
   j3_min_mj = 0;
   jet_PartonTruthLabelID = 0;
   jet_ConeTruthLabelID = 0;
   jet_fjvt = 0;
   basemu_pt = 0;
   basemu_eta = 0;
   basemu_phi = 0;
   basemu_charge = 0;
   basemu_ptvarcone30 = 0;
   baseel_pt = 0;
   baseel_eta = 0;
   baseel_phi = 0;
   baseel_charge = 0;
   baseel_ptvarcone20 = 0;
   basemu_ptvarcone20 = 0;
   basemu_z0 = 0;
   basemu_d0sig = 0;
   basemu_topoetcone20 = 0;
   basemu_topoetcone30 = 0;
   basemu_type = 0;
   basemu_truthOrigin = 0;
   basemu_truthType = 0;
   baseel_z0 = 0;
   baseel_d0sig = 0;
   baseel_topoetcone20 = 0;
   baseel_truthOrigin = 0;
   baseel_truthType = 0;
   ph_pt = 0;
   ph_phi = 0;
   ph_eta = 0;
   tau_pt = 0;
   tau_phi = 0;
   tau_eta = 0;
   truth_tau_pt = 0;
   truth_tau_eta = 0;
   truth_tau_phi = 0;
   truth_el_pt = 0;
   truth_el_eta = 0;
   truth_el_phi = 0;
   truth_mu_pt = 0;
   truth_mu_eta = 0;
   truth_mu_phi = 0;
   truth_ph_pt = 0;
   truth_ph_eta = 0;
   truth_ph_phi = 0;
   truth_jet_pt = 0;
   truth_jet_eta = 0;
   truth_jet_phi = 0;
   truth_jet_m = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("w", &w, &b_w);
   fChain->SetBranchAddress("vjWeight", &vjWeight, &b_vjWeight);
   fChain->SetBranchAddress("puSyst2018Weight", &puSyst2018Weight, &b_puSyst2018Weight);
   fChain->SetBranchAddress("xeSFTrigWeight", &xeSFTrigWeight, &b_xeSFTrigWeight);
   fChain->SetBranchAddress("xeSFTrigWeight_nomu", &xeSFTrigWeight_nomu, &b_xeSFTrigWeight_nomu);
   fChain->SetBranchAddress("puWeight", &puWeight, &b_puWeight);
   fChain->SetBranchAddress("xeSFTrigWeight__1up", &xeSFTrigWeight__1up, &b_xeSFTrigWeight__1up);
   fChain->SetBranchAddress("xeSFTrigWeight__1down", &xeSFTrigWeight__1down, &b_xeSFTrigWeight__1down);
   fChain->SetBranchAddress("xeSFTrigWeight_nomu__1up", &xeSFTrigWeight_nomu__1up, &b_xeSFTrigWeight_nomu__1up);
   fChain->SetBranchAddress("xeSFTrigWeight_nomu__1down", &xeSFTrigWeight_nomu__1down, &b_xeSFTrigWeight_nomu__1down);
   fChain->SetBranchAddress("eleANTISF", &eleANTISF, &b_eleANTISF);
   fChain->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
   fChain->SetBranchAddress("randomRunNumber", &randomRunNumber, &b_randomRunNumber);
   fChain->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
   fChain->SetBranchAddress("trigger_met", &trigger_met, &b_trigger_met);
   fChain->SetBranchAddress("trigger_met_encodedv2", &trigger_met_encodedv2, &b_trigger_met_encodedv2);
   fChain->SetBranchAddress("l1_met_trig_encoded", &l1_met_trig_encoded, &b_l1_met_trig_encoded);
   fChain->SetBranchAddress("trigger_met_encoded", &trigger_met_encoded, &b_trigger_met_encoded);
   fChain->SetBranchAddress("passBatman", &passBatman, &b_passBatman);
   fChain->SetBranchAddress("passVjetsFilter", &passVjetsFilter, &b_passVjetsFilter);
   fChain->SetBranchAddress("passVjetsFilterTauEl", &passVjetsFilterTauEl, &b_passVjetsFilterTauEl);
   fChain->SetBranchAddress("passVjetsPTV", &passVjetsPTV, &b_passVjetsPTV);
   fChain->SetBranchAddress("MGVTruthPt", &MGVTruthPt, &b_MGVTruthPt);
   fChain->SetBranchAddress("in_vy_overlap", &in_vy_overlap, &b_in_vy_overlap);
   fChain->SetBranchAddress("trigger_lep", &trigger_lep, &b_trigger_lep);
   fChain->SetBranchAddress("lep_trig_match", &lep_trig_match, &b_lep_trig_match);
   fChain->SetBranchAddress("passJetCleanTight", &passJetCleanTight, &b_passJetCleanTight);
   fChain->SetBranchAddress("averageIntPerXing", &averageIntPerXing, &b_averageIntPerXing);
   fChain->SetBranchAddress("n_vx", &n_vx, &b_n_vx);
   fChain->SetBranchAddress("n_jet", &n_jet, &b_n_jet);
   fChain->SetBranchAddress("n_el", &n_el, &b_n_el);
   fChain->SetBranchAddress("n_mu", &n_mu, &b_n_mu);
   fChain->SetBranchAddress("n_el_w", &n_el_w, &b_n_el_w);
   fChain->SetBranchAddress("n_mu_w", &n_mu_w, &b_n_mu_w);
   fChain->SetBranchAddress("n_ph", &n_ph, &b_n_ph);
   fChain->SetBranchAddress("n_tau", &n_tau, &b_n_tau);
   fChain->SetBranchAddress("jj_mass", &jj_mass, &b_jj_mass);
   fChain->SetBranchAddress("jj_deta", &jj_deta, &b_jj_deta);
   fChain->SetBranchAddress("jj_dphi", &jj_dphi, &b_jj_dphi);
   fChain->SetBranchAddress("met_tst_j1_dphi", &met_tst_j1_dphi, &b_met_tst_j1_dphi);
   fChain->SetBranchAddress("met_tst_j2_dphi", &met_tst_j2_dphi, &b_met_tst_j2_dphi);
   fChain->SetBranchAddress("met_tst_nolep_j1_dphi", &met_tst_nolep_j1_dphi, &b_met_tst_nolep_j1_dphi);
   fChain->SetBranchAddress("met_tst_nolep_j2_dphi", &met_tst_nolep_j2_dphi, &b_met_tst_nolep_j2_dphi);
   fChain->SetBranchAddress("met_tst_et", &met_tst_et, &b_met_tst_et);
   fChain->SetBranchAddress("met_tst_nolep_et", &met_tst_nolep_et, &b_met_tst_nolep_et);
   fChain->SetBranchAddress("met_tst_phi", &met_tst_phi, &b_met_tst_phi);
   fChain->SetBranchAddress("met_tst_nolep_phi", &met_tst_nolep_phi, &b_met_tst_nolep_phi);
   fChain->SetBranchAddress("met_cst_jet", &met_cst_jet, &b_met_cst_jet);
   fChain->SetBranchAddress("met_soft_tst_et", &met_soft_tst_et, &b_met_soft_tst_et);
   fChain->SetBranchAddress("mu_charge", &mu_charge, &b_mu_charge);
   fChain->SetBranchAddress("mu_pt", &mu_pt, &b_mu_pt);
   fChain->SetBranchAddress("el_charge", &el_charge, &b_el_charge);
   fChain->SetBranchAddress("el_pt", &el_pt, &b_el_pt);
   fChain->SetBranchAddress("jet_pt", &jet_pt, &b_jet_pt);
   fChain->SetBranchAddress("jet_timing", &jet_timing, &b_jet_timing);
   fChain->SetBranchAddress("mu_phi", &mu_phi, &b_mu_phi);
   fChain->SetBranchAddress("el_phi", &el_phi, &b_el_phi);
   fChain->SetBranchAddress("mu_eta", &mu_eta, &b_mu_eta);
   fChain->SetBranchAddress("el_eta", &el_eta, &b_el_eta);
   fChain->SetBranchAddress("jet_phi", &jet_phi, &b_jet_phi);
   fChain->SetBranchAddress("jet_eta", &jet_eta, &b_jet_eta);
   fChain->SetBranchAddress("jet_m", &jet_m, &b_jet_m);
   fChain->SetBranchAddress("jet_jvt", &jet_jvt, &b_jet_jvt);
   fChain->SetBranchAddress("met_significance", &met_significance, &b_met_significance);
   fChain->SetBranchAddress("max_mj_over_mjj", &max_mj_over_mjj, &b_max_mj_over_mjj);
   fChain->SetBranchAddress("maxCentrality", &maxCentrality, &b_maxCentrality);
   fChain->SetBranchAddress("n_baseel", &n_baseel, &b_n_baseel);
   fChain->SetBranchAddress("n_basemu", &n_basemu, &b_n_basemu);
   fChain->SetBranchAddress("n_el_baseline_noOR", &n_el_baseline_noOR, &b_n_el_baseline_noOR);
   fChain->SetBranchAddress("n_mu_baseline_noOR", &n_mu_baseline_noOR, &b_n_mu_baseline_noOR);
   fChain->SetBranchAddress("n_el_baseline_iso", &n_el_baseline_iso, &b_n_el_baseline_iso);
   fChain->SetBranchAddress("n_mu_baseline_iso", &n_mu_baseline_iso, &b_n_mu_baseline_iso);
   fChain->SetBranchAddress("n_bjet", &n_bjet, &b_n_bjet);
   fChain->SetBranchAddress("jet_btag_weight", &jet_btag_weight, &b_jet_btag_weight);
   fChain->SetBranchAddress("j3_centrality", &j3_centrality, &b_j3_centrality);
   fChain->SetBranchAddress("j3_min_mj_over_mjj", &j3_min_mj_over_mjj, &b_j3_min_mj_over_mjj);
   fChain->SetBranchAddress("j3_dRj1", &j3_dRj1, &b_j3_dRj1);
   fChain->SetBranchAddress("j3_dRj2", &j3_dRj2, &b_j3_dRj2);
   fChain->SetBranchAddress("j3_minDR", &j3_minDR, &b_j3_minDR);
   fChain->SetBranchAddress("j3_mjclosest", &j3_mjclosest, &b_j3_mjclosest);
   fChain->SetBranchAddress("j3_min_mj", &j3_min_mj, &b_j3_min_mj);
   fChain->SetBranchAddress("mj34", &mj34, &b_mj34);
   fChain->SetBranchAddress("max_j_eta", &max_j_eta, &b_max_j_eta);
   fChain->SetBranchAddress("lb", &lb, &b_lb);
   fChain->SetBranchAddress("bcid", &bcid, &b_bcid);
   fChain->SetBranchAddress("BCIDDistanceFromFront", &BCIDDistanceFromFront, &b_BCIDDistanceFromFront);
   fChain->SetBranchAddress("jet_PartonTruthLabelID", &jet_PartonTruthLabelID, &b_jet_PartonTruthLabelID);
   fChain->SetBranchAddress("jet_ConeTruthLabelID", &jet_ConeTruthLabelID, &b_jet_ConeTruthLabelID);
   fChain->SetBranchAddress("jet_fjvt", &jet_fjvt, &b_jet_fjvt);
   fChain->SetBranchAddress("basemu_pt", &basemu_pt, &b_basemu_pt);
   fChain->SetBranchAddress("basemu_eta", &basemu_eta, &b_basemu_eta);
   fChain->SetBranchAddress("basemu_phi", &basemu_phi, &b_basemu_phi);
   fChain->SetBranchAddress("basemu_charge", &basemu_charge, &b_basemu_charge);
   fChain->SetBranchAddress("basemu_ptvarcone30", &basemu_ptvarcone30, &b_basemu_ptvarcone30);
   fChain->SetBranchAddress("baseel_pt", &baseel_pt, &b_baseel_pt);
   fChain->SetBranchAddress("baseel_eta", &baseel_eta, &b_baseel_eta);
   fChain->SetBranchAddress("baseel_phi", &baseel_phi, &b_baseel_phi);
   fChain->SetBranchAddress("baseel_charge", &baseel_charge, &b_baseel_charge);
   fChain->SetBranchAddress("baseel_ptvarcone20", &baseel_ptvarcone20, &b_baseel_ptvarcone20);
   fChain->SetBranchAddress("basemu_ptvarcone20", &basemu_ptvarcone20, &b_basemu_ptvarcone20);
   fChain->SetBranchAddress("basemu_z0", &basemu_z0, &b_basemu_z0);
   fChain->SetBranchAddress("basemu_d0sig", &basemu_d0sig, &b_basemu_d0sig);
   fChain->SetBranchAddress("basemu_topoetcone20", &basemu_topoetcone20, &b_basemu_topoetcone20);
   fChain->SetBranchAddress("basemu_topoetcone30", &basemu_topoetcone30, &b_basemu_topoetcone30);
   fChain->SetBranchAddress("basemu_type", &basemu_type, &b_basemu_type);
   fChain->SetBranchAddress("basemu_truthOrigin", &basemu_truthOrigin, &b_basemu_truthOrigin);
   fChain->SetBranchAddress("basemu_truthType", &basemu_truthType, &b_basemu_truthType);
   fChain->SetBranchAddress("baseel_z0", &baseel_z0, &b_baseel_z0);
   fChain->SetBranchAddress("baseel_d0sig", &baseel_d0sig, &b_baseel_d0sig);
   fChain->SetBranchAddress("baseel_topoetcone20", &baseel_topoetcone20, &b_baseel_topoetcone20);
   fChain->SetBranchAddress("baseel_truthOrigin", &baseel_truthOrigin, &b_baseel_truthOrigin);
   fChain->SetBranchAddress("baseel_truthType", &baseel_truthType, &b_baseel_truthType);
   fChain->SetBranchAddress("ph_pt", &ph_pt, &b_ph_pt);
   fChain->SetBranchAddress("ph_phi", &ph_phi, &b_ph_phi);
   fChain->SetBranchAddress("ph_eta", &ph_eta, &b_ph_eta);
   fChain->SetBranchAddress("tau_pt", &tau_pt, &b_tau_pt);
   fChain->SetBranchAddress("tau_phi", &tau_phi, &b_tau_phi);
   fChain->SetBranchAddress("tau_eta", &tau_eta, &b_tau_eta);
   fChain->SetBranchAddress("met_soft_tst_phi", &met_soft_tst_phi, &b_met_soft_tst_phi);
   fChain->SetBranchAddress("met_soft_tst_sumet", &met_soft_tst_sumet, &b_met_soft_tst_sumet);
   fChain->SetBranchAddress("met_tenacious_tst_et", &met_tenacious_tst_et, &b_met_tenacious_tst_et);
   fChain->SetBranchAddress("met_tenacious_tst_phi", &met_tenacious_tst_phi, &b_met_tenacious_tst_phi);
   fChain->SetBranchAddress("met_tenacious_tst_nolep_et", &met_tenacious_tst_nolep_et, &b_met_tenacious_tst_nolep_et);
   fChain->SetBranchAddress("met_tenacious_tst_nolep_phi", &met_tenacious_tst_nolep_phi, &b_met_tenacious_tst_nolep_phi);
   fChain->SetBranchAddress("met_tenacious_tst_j1_dphi", &met_tenacious_tst_j1_dphi, &b_met_tenacious_tst_j1_dphi);
   fChain->SetBranchAddress("met_tenacious_tst_j2_dphi", &met_tenacious_tst_j2_dphi, &b_met_tenacious_tst_j2_dphi);
   fChain->SetBranchAddress("met_tenacious_tst_nolep_j1_dphi", &met_tenacious_tst_nolep_j1_dphi, &b_met_tenacious_tst_nolep_j1_dphi);
   fChain->SetBranchAddress("met_tenacious_tst_nolep_j2_dphi", &met_tenacious_tst_nolep_j2_dphi, &b_met_tenacious_tst_nolep_j2_dphi);
   fChain->SetBranchAddress("met_tight_tst_et", &met_tight_tst_et, &b_met_tight_tst_et);
   fChain->SetBranchAddress("met_tight_tst_phi", &met_tight_tst_phi, &b_met_tight_tst_phi);
   fChain->SetBranchAddress("met_tight_tst_nolep_et", &met_tight_tst_nolep_et, &b_met_tight_tst_nolep_et);
   fChain->SetBranchAddress("met_tight_tst_nolep_phi", &met_tight_tst_nolep_phi, &b_met_tight_tst_nolep_phi);
   fChain->SetBranchAddress("metsig_tst", &metsig_tst, &b_metsig_tst);
   fChain->SetBranchAddress("truth_tau_pt", &truth_tau_pt, &b_truth_tau_pt);
   fChain->SetBranchAddress("truth_tau_eta", &truth_tau_eta, &b_truth_tau_eta);
   fChain->SetBranchAddress("truth_tau_phi", &truth_tau_phi, &b_truth_tau_phi);
   fChain->SetBranchAddress("truth_el_pt", &truth_el_pt, &b_truth_el_pt);
   fChain->SetBranchAddress("truth_el_eta", &truth_el_eta, &b_truth_el_eta);
   fChain->SetBranchAddress("truth_el_phi", &truth_el_phi, &b_truth_el_phi);
   fChain->SetBranchAddress("truth_mu_pt", &truth_mu_pt, &b_truth_mu_pt);
   fChain->SetBranchAddress("truth_mu_eta", &truth_mu_eta, &b_truth_mu_eta);
   fChain->SetBranchAddress("truth_mu_phi", &truth_mu_phi, &b_truth_mu_phi);
   fChain->SetBranchAddress("truth_ph_pt", &truth_ph_pt, &b_truth_ph_pt);
   fChain->SetBranchAddress("truth_ph_eta", &truth_ph_eta, &b_truth_ph_eta);
   fChain->SetBranchAddress("truth_ph_phi", &truth_ph_phi, &b_truth_ph_phi);
   fChain->SetBranchAddress("GenMET_pt", &GenMET_pt, &b_GenMET_pt);
   fChain->SetBranchAddress("met_truth_et", &met_truth_et, &b_met_truth_et);
   fChain->SetBranchAddress("met_truth_phi", &met_truth_phi, &b_met_truth_phi);
   fChain->SetBranchAddress("met_truth_sumet", &met_truth_sumet, &b_met_truth_sumet);
   fChain->SetBranchAddress("truth_jet_pt", &truth_jet_pt, &b_truth_jet_pt);
   fChain->SetBranchAddress("truth_jet_eta", &truth_jet_eta, &b_truth_jet_eta);
   fChain->SetBranchAddress("truth_jet_phi", &truth_jet_phi, &b_truth_jet_phi);
   fChain->SetBranchAddress("truth_jet_m", &truth_jet_m, &b_truth_jet_m);
   fChain->SetBranchAddress("truth_jj_mass", &truth_jj_mass, &b_truth_jj_mass);
   fChain->SetBranchAddress("truth_jj_dphi", &truth_jj_dphi, &b_truth_jj_dphi);
   fChain->SetBranchAddress("truth_j2_pt", &truth_j2_pt, &b_truth_j2_pt);
   fChain->SetBranchAddress("n_jet_truth", &n_jet_truth, &b_n_jet_truth);
   fChain->SetBranchAddress("truthloMG_jj_mass", &truthloMG_jj_mass, &b_truthloMG_jj_mass);
   fChain->SetBranchAddress("truthloMG_jj_dphi", &truthloMG_jj_dphi, &b_truthloMG_jj_dphi);
   fChain->SetBranchAddress("truthloMG_j2_pt", &truthloMG_j2_pt, &b_truthloMG_j2_pt);
   fChain->SetBranchAddress("truth_V_dressed_pt", &truth_V_dressed_pt, &b_truth_V_dressed_pt);
   fChain->SetBranchAddress("weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down", &weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up", &weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_weleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down", &weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up", &weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_weleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down", &welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up", &welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_welSFWeightEL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down", &welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up", &welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_welSFWeightEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down", &welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up", &welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_welSFWeightEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down", &welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up", &welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_welSFWeightEL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down", &welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down", &wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up", &welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_welSFTrigWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up", &wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_wdilepTrigSFWeightEL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down", &welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down", &wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down, &b_wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down);
   fChain->SetBranchAddress("welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up", &welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_welSFTrigWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up", &wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up, &b_wdilepTrigSFWeightEL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up);
   fChain->SetBranchAddress("wjvtSFWeightJET_JvtEfficiency__1down", &wjvtSFWeightJET_JvtEfficiency__1down, &b_wjvtSFWeightJET_JvtEfficiency__1down);
   fChain->SetBranchAddress("wjvtSFWeightJET_JvtEfficiency__1up", &wjvtSFWeightJET_JvtEfficiency__1up, &b_wjvtSFWeightJET_JvtEfficiency__1up);
   fChain->SetBranchAddress("wfjvtSFWeightJET_fJvtEfficiency__1down", &wfjvtSFWeightJET_fJvtEfficiency__1down, &b_wfjvtSFWeightJET_fJvtEfficiency__1down);
   fChain->SetBranchAddress("wfjvtSFTighterWeightJET_fJvtEfficiency__1down", &wfjvtSFTighterWeightJET_fJvtEfficiency__1down, &b_wfjvtSFTighterWeightJET_fJvtEfficiency__1down);
   fChain->SetBranchAddress("wfjvtSFWeightJET_fJvtEfficiency__1up", &wfjvtSFWeightJET_fJvtEfficiency__1up, &b_wfjvtSFWeightJET_fJvtEfficiency__1up);
   fChain->SetBranchAddress("wfjvtSFTighterWeightJET_fJvtEfficiency__1up", &wfjvtSFTighterWeightJET_fJvtEfficiency__1up, &b_wfjvtSFTighterWeightJET_fJvtEfficiency__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_BADMUON_STAT__1down", &wmuSFWeightMUON_EFF_BADMUON_STAT__1down, &b_wmuSFWeightMUON_EFF_BADMUON_STAT__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_BADMUON_STAT__1up", &wmuSFWeightMUON_EFF_BADMUON_STAT__1up, &b_wmuSFWeightMUON_EFF_BADMUON_STAT__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_BADMUON_SYS__1down", &wmuSFWeightMUON_EFF_BADMUON_SYS__1down, &b_wmuSFWeightMUON_EFF_BADMUON_SYS__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_BADMUON_SYS__1up", &wmuSFWeightMUON_EFF_BADMUON_SYS__1up, &b_wmuSFWeightMUON_EFF_BADMUON_SYS__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_ISO_STAT__1down", &wmuSFWeightMUON_EFF_ISO_STAT__1down, &b_wmuSFWeightMUON_EFF_ISO_STAT__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_ISO_STAT__1up", &wmuSFWeightMUON_EFF_ISO_STAT__1up, &b_wmuSFWeightMUON_EFF_ISO_STAT__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_ISO_SYS__1down", &wmuSFWeightMUON_EFF_ISO_SYS__1down, &b_wmuSFWeightMUON_EFF_ISO_SYS__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_ISO_SYS__1up", &wmuSFWeightMUON_EFF_ISO_SYS__1up, &b_wmuSFWeightMUON_EFF_ISO_SYS__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_RECO_STAT__1down", &wmuSFWeightMUON_EFF_RECO_STAT__1down, &b_wmuSFWeightMUON_EFF_RECO_STAT__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_RECO_STAT__1up", &wmuSFWeightMUON_EFF_RECO_STAT__1up, &b_wmuSFWeightMUON_EFF_RECO_STAT__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1down", &wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1down, &b_wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1up", &wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1up, &b_wmuSFWeightMUON_EFF_RECO_STAT_LOWPT__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_RECO_SYS__1down", &wmuSFWeightMUON_EFF_RECO_SYS__1down, &b_wmuSFWeightMUON_EFF_RECO_SYS__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_RECO_SYS__1up", &wmuSFWeightMUON_EFF_RECO_SYS__1up, &b_wmuSFWeightMUON_EFF_RECO_SYS__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1down", &wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1down, &b_wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1up", &wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1up, &b_wmuSFWeightMUON_EFF_RECO_SYS_LOWPT__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_TTVA_STAT__1down", &wmuSFWeightMUON_EFF_TTVA_STAT__1down, &b_wmuSFWeightMUON_EFF_TTVA_STAT__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_TTVA_STAT__1up", &wmuSFWeightMUON_EFF_TTVA_STAT__1up, &b_wmuSFWeightMUON_EFF_TTVA_STAT__1up);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_TTVA_SYS__1down", &wmuSFWeightMUON_EFF_TTVA_SYS__1down, &b_wmuSFWeightMUON_EFF_TTVA_SYS__1down);
   fChain->SetBranchAddress("wmuSFWeightMUON_EFF_TTVA_SYS__1up", &wmuSFWeightMUON_EFF_TTVA_SYS__1up, &b_wmuSFWeightMUON_EFF_TTVA_SYS__1up);
   fChain->SetBranchAddress("wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1down", &wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1down, &b_wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1down);
   fChain->SetBranchAddress("wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1down", &wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1down, &b_wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1down);
   fChain->SetBranchAddress("wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1up", &wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1up, &b_wmuSFTrigWeightMUON_EFF_TrigStatUncertainty__1up);
   fChain->SetBranchAddress("wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1up", &wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1up, &b_wdilepTrigSFWeightMUON_EFF_TrigStatUncertainty__1up);
   fChain->SetBranchAddress("wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1down", &wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1down, &b_wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1down);
   fChain->SetBranchAddress("wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1down", &wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1down, &b_wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1down);
   fChain->SetBranchAddress("wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1up", &wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1up, &b_wmuSFTrigWeightMUON_EFF_TrigSystUncertainty__1up);
   fChain->SetBranchAddress("wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1up", &wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1up, &b_wdilepTrigSFWeightMUON_EFF_TrigSystUncertainty__1up);
   fChain->SetBranchAddress("wphSFWeightPH_EFF_ID_Uncertainty__1down", &wphSFWeightPH_EFF_ID_Uncertainty__1down, &b_wphSFWeightPH_EFF_ID_Uncertainty__1down);
   fChain->SetBranchAddress("wphSFWeightPH_EFF_ID_Uncertainty__1up", &wphSFWeightPH_EFF_ID_Uncertainty__1up, &b_wphSFWeightPH_EFF_ID_Uncertainty__1up);
   fChain->SetBranchAddress("wphSFWeightPH_EFF_ISO_Uncertainty__1down", &wphSFWeightPH_EFF_ISO_Uncertainty__1down, &b_wphSFWeightPH_EFF_ISO_Uncertainty__1down);
   fChain->SetBranchAddress("wphSFWeightPH_EFF_ISO_Uncertainty__1up", &wphSFWeightPH_EFF_ISO_Uncertainty__1up, &b_wphSFWeightPH_EFF_ISO_Uncertainty__1up);
   fChain->SetBranchAddress("wpuWeightPRW_DATASF__1down", &wpuWeightPRW_DATASF__1down, &b_wpuWeightPRW_DATASF__1down);
   fChain->SetBranchAddress("wpuWeightPRW_DATASF__1up", &wpuWeightPRW_DATASF__1up, &b_wpuWeightPRW_DATASF__1up);
   fChain->SetBranchAddress("wnloEWKWeight__1up", &wnloEWKWeight__1up, &b_wnloEWKWeight__1up);
   fChain->SetBranchAddress("wnloEWKWeight__1down", &wnloEWKWeight__1down, &b_wnloEWKWeight__1down);
   fChain->SetBranchAddress("wpuSyst2018Weight__1up", &wpuSyst2018Weight__1up, &b_wpuSyst2018Weight__1up);
   fChain->SetBranchAddress("wpuSyst2018Weight__1down", &wpuSyst2018Weight__1down, &b_wpuSyst2018Weight__1down);
   fChain->SetBranchAddress("wvjets_d1kappa_EW__1up", &wvjets_d1kappa_EW__1up, &b_wvjets_d1kappa_EW__1up);
   fChain->SetBranchAddress("wvjets_d1kappa_EW__1down", &wvjets_d1kappa_EW__1down, &b_wvjets_d1kappa_EW__1down);
   fChain->SetBranchAddress("wvjets_d2kappa_EW__1up", &wvjets_d2kappa_EW__1up, &b_wvjets_d2kappa_EW__1up);
   fChain->SetBranchAddress("wvjets_d2kappa_EW__1down", &wvjets_d2kappa_EW__1down, &b_wvjets_d2kappa_EW__1down);
   fChain->SetBranchAddress("wvjets_d3kappa_EW__1up", &wvjets_d3kappa_EW__1up, &b_wvjets_d3kappa_EW__1up);
   fChain->SetBranchAddress("wvjets_d3kappa_EW__1down", &wvjets_d3kappa_EW__1down, &b_wvjets_d3kappa_EW__1down);
   fChain->SetBranchAddress("wvjets_d1K_NNLO__1up", &wvjets_d1K_NNLO__1up, &b_wvjets_d1K_NNLO__1up);
   fChain->SetBranchAddress("wvjets_d1K_NNLO__1down", &wvjets_d1K_NNLO__1down, &b_wvjets_d1K_NNLO__1down);
   fChain->SetBranchAddress("wvjets_d2K_NNLO__1up", &wvjets_d2K_NNLO__1up, &b_wvjets_d2K_NNLO__1up);
   fChain->SetBranchAddress("wvjets_d2K_NNLO__1down", &wvjets_d2K_NNLO__1down, &b_wvjets_d2K_NNLO__1down);
   fChain->SetBranchAddress("wvjets_d3K_NNLO__1up", &wvjets_d3K_NNLO__1up, &b_wvjets_d3K_NNLO__1up);
   fChain->SetBranchAddress("wvjets_d3K_NNLO__1down", &wvjets_d3K_NNLO__1down, &b_wvjets_d3K_NNLO__1down);
   fChain->SetBranchAddress("wvjets_dK_NNLO_mix__1up", &wvjets_dK_NNLO_mix__1up, &b_wvjets_dK_NNLO_mix__1up);
   fChain->SetBranchAddress("wvjets_dK_NNLO_mix__1down", &wvjets_dK_NNLO_mix__1down, &b_wvjets_dK_NNLO_mix__1down);
   fChain->SetBranchAddress("wvjets_dK_PDF__1up", &wvjets_dK_PDF__1up, &b_wvjets_dK_PDF__1up);
   fChain->SetBranchAddress("wvjets_dK_PDF__1down", &wvjets_dK_PDF__1down, &b_wvjets_dK_PDF__1down);
   fChain->SetBranchAddress("wvjets_ckkw15", &wvjets_ckkw15, &b_wvjets_ckkw15);
   fChain->SetBranchAddress("wvjets_ckkw30", &wvjets_ckkw30, &b_wvjets_ckkw30);
   fChain->SetBranchAddress("wvjets_fac025", &wvjets_fac025, &b_wvjets_fac025);
   fChain->SetBranchAddress("wvjets_fac4", &wvjets_fac4, &b_wvjets_fac4);
   fChain->SetBranchAddress("wvjets_renorm025", &wvjets_renorm025, &b_wvjets_renorm025);
   fChain->SetBranchAddress("wvjets_renorm4", &wvjets_renorm4, &b_wvjets_renorm4);
   fChain->SetBranchAddress("wvjets_qsf025", &wvjets_qsf025, &b_wvjets_qsf025);
   fChain->SetBranchAddress("wvjets_qsf4", &wvjets_qsf4, &b_wvjets_qsf4);
}

Bool_t MySelector::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

#endif // #ifdef MySelector_cxx
