#ifndef VBFANALYSIS_HFINPUTALG_H
#define VBFANALYSIS_HFINPUTALG_H 1

#include "AthAnalysisBaseComps/AthAnalysisAlgorithm.h"

//Example ROOT Includes
//#include "TTree.h"
//#include "TH1D.h"

#include "TTree.h"
#include "TH1D.h"
#include <vector>
#include <iostream>

using namespace std;

class HFInputAlg: public ::AthAnalysisAlgorithm { 
 public: 
  HFInputAlg( const std::string& name, ISvcLocator* pSvcLocator );
  virtual ~HFInputAlg(); 

  ///uncomment and implement methods as required

                                        //IS EXECUTED:
  virtual StatusCode  initialize();     //once, before any input is loaded
  virtual StatusCode  beginInputFile(); //start of each input file, only metadata loaded
  //virtual StatusCode  firstExecute();   //once, after first eventdata is loaded (not per file)
  std::string HistoNameMaker(std::string currentSample, std::string currentCR, std::string bin, std::string syst, Bool_t isMC);
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
  //  const TFile outputFile;
  TString m_treeName = "MiniNtuple";
  TString outputFileName = "ntuple";
   //Example algorithm property, see constructor for declaration:
   //int m_nProperty = 0;

   //Example histogram, see initialize method for registration to output histSvc
   //TH1D* m_myHist = 0;
   //TTree* m_myTree = 0;

  //output tree                                                                                                                                                                                                   
  std::string currentVariation = "NONE";
  std::string currentSample = "Z_strong";//"W_strong";

  vector <TH1F*> hSR;
  vector <TH1F*> hCRWep;
  vector <TH1F*> hCRWen;
  vector <TH1F*> hCRWepLowSig;
  vector <TH1F*> hCRWenLowSig;
  vector <TH1F*> hCRWmp;
  vector <TH1F*> hCRWmn;
  vector <TH1F*> hCRZee;
  vector <TH1F*> hCRZmm;
  
  Float_t w;
  Int_t pass_JetCleaning_tight;
  Int_t jet_n;
  Float_t j1_pt;
  Float_t j2_pt;
  Float_t deltaPhi_j1_met;
  Float_t deltaPhi_j2_met;
  Float_t jj_dphi;
  Float_t j1_eta;
  Float_t j2_eta;
  Float_t jj_deta;
  Float_t Inv_mass;
  Float_t metjet_CST;
  Bool_t MET_trig;
  Float_t met_et;
  Int_t el_n;
  Int_t mu_n;
  Float_t el1_pt;
  Float_t el2_pt;
  Float_t mu1_pt;
  Float_t mu2_pt;
  Float_t el1_charge;
  Float_t el2_charge;
  Float_t mu1_charge;
  Float_t mu2_charge;
  Int_t elTrig;
  Float_t lepmet_et;
  Float_t met_significance;
  Int_t muTrig;
  Float_t deltaPhi_j1_lepmet;
  Float_t deltaPhi_j2_lepmet;
  Float_t Zll_m;

  /* TBranch *b_w; */
  /* TBranch *b_pass_JetCleaning_tight; */
  /* TBranch *b_jet_n; */
  /* TBranch *b_j1_pt; */
  /* TBranch *b_j2_pt; */
  /* TBranch *b_deltaPhi_j1_met; */
  /* TBranch *b_deltaPhi_j2_met; */
  /* TBranch *b_jj_dphi; */
  /* TBranch *b_j1_eta; */
  /* TBranch *b_j2_eta; */
  /* TBranch *b_jj_deta; */
  /* TBranch *b_Inv_mass; */
  /* TBranch *b_metjet_CST; */
  /* TBranch *b_MET_trig; */
  /* TBranch *b_met_et; */
  /* TBranch *b_el_n; */
  /* TBranch *b_mu_n; */
  /* TBranch *b_el1_pt; */
  /* TBranch *b_el2_pt; */
  /* TBranch *b_mu1_pt; */
  /* TBranch *b_mu2_pt; */
  /* TBranch *b_el1_charge; */
  /* TBranch *b_el2_charge; */
  /* TBranch *b_mu1_charge; */
  /* TBranch *b_mu2_charge; */
  /* TBranch *b_elTrig; */
  /* TBranch *b_lepmet_et; */
  /* TBranch *b_met_significance; */
  /* TBranch *b_muTrig; */
  /* TBranch *b_deltaPhi_j1_lepmet; */
  /* TBranch *b_deltaPhi_j2_lepmet; */
  /* TBranch *b_Zll_m; */
}; 

#endif //> !VBFANALYSIS_HFINPUTALG_H
