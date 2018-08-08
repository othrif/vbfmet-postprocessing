#ifndef VBFANALYSIS_VBFANALYSISALG_H
#define VBFANALYSIS_VBFANALYSISALG_H 1

#include "AthAnalysisBaseComps/AthAnalysisAlgorithm.h"
#include "SUSYTools/SUSYCrossSection.h"

//Example ROOT Includes
//#include "TTree.h"
//#include "TH1D.h"

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


 private: 

  int npevents = 0;
  Bool_t isMC = true;
  bool is2015;
  bool is2016;
  TTree *m_tree = 0;
  TTree *m_tree_out = 0;
  SUSY::CrossSectionDB *my_XsecDB; 
  //  const TFile outputFile;
  TString m_treeName = "MiniNtuple";
  TString outputFileName = "ntuple";

  TH1F *h_Gen; 
  std::map<int,float> Ngen; 

  //Maps for types of Tree things 
  std::map<TString, int>   tMapInt; 
  std::map<TString, float> tMapFloat;


   //Example algorithm property, see constructor for declaration:
   //int m_nProperty = 0;

   //Example histogram, see initialize method for registration to output histSvc
   //TH1D* m_myHist = 0;
   //TTree* m_myTree = 0;

  //output tree                                                                                                                                                                                                   
  std::string outputName;
  std::string currentVariation;
  TString currentSample;
  TString treeNameOut="nominal";
  TString treeTitleOut="nominal";

  Float_t crossSection;
  Float_t weight;
  Float_t w;
  Float_t met_significance;
  Int_t trigger_met;

  Int_t runNumber;
  Float_t averageIntPerXing;
  Float_t mcEventWeight;
  Float_t puWeight;
  Float_t jvtSFWeight;
  Float_t elSFWeight;
  Float_t muSFWeight;
  Float_t elSFTrigWeight;
  Float_t muSFTrigWeight;
  Int_t passJetCleanLoose;
  Int_t passJetCleanTight;
  Int_t trigger_HLT_xe100_mht_L1XE50;
  Int_t trigger_HLT_xe110_mht_L1XE50;
  Int_t trigger_HLT_xe90_mht_L1XE50;
  Int_t trigger_lep;
  Int_t passGRL;
  Int_t passPV;
  Int_t passDetErr;
  Int_t n_jet;
  Int_t n_el;
  Int_t n_mu;
  Double_t jj_mass;
  Double_t jj_deta;
  Double_t jj_dphi;
  Double_t met_tst_j1_dphi;
  Double_t met_tst_j2_dphi;
  Double_t met_tst_nolep_j1_dphi;
  Double_t met_tst_nolep_j2_dphi;
  Float_t met_tst_et;
  Float_t met_tst_nolep_et;
  std::vector<Float_t>* mu_charge;
  std::vector<Float_t>* mu_pt;
  std::vector<Float_t>* mu_phi;
  std::vector<Float_t>* el_charge;
  std::vector<Float_t>* el_pt;
  std::vector<Float_t>* el_phi;
  std::vector<Float_t>* jet_pt;
  std::vector<Float_t>* jet_phi;
  std::vector<Float_t>* jet_eta;
  std::vector<Float_t>* jet_jvt;
  std::vector<Float_t>* jet_timing;
  std::vector<Int_t>* jet_passJvt;

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
  TBranch    *b_jet_timing;
  TBranch    *b_jet_passJvt;
}; 

#endif //> !VBFANALYSIS_VBFANALYSISALG_H
