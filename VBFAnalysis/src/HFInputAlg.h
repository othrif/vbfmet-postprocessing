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
  bool replace(std::string& str, const std::string& from, const std::string& to);
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
  Bool_t doLowNom = false; //put nominal yields for "Low" histogram for asymmetric systematics for HistFitter
  Bool_t isHigh = true;
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
  std::string currentVariation = "Nominal";
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

  Float_t met_significance;
  Int_t trigger_met;
  Float_t w;
  Int_t runNumber;
  Int_t passJetCleanLoose;
  Int_t passJetCleanTight;
  Int_t trigger_lep;
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
  std::vector<Int_t>* mu_charge;
  std::vector<Float_t>* mu_pt;
  std::vector<Float_t>* mu_phi;
  std::vector<Float_t>* mu_eta;
  std::vector<Int_t>* el_charge;
  std::vector<Float_t>* el_pt;
  std::vector<Float_t>* el_phi;
  std::vector<Float_t>* el_eta;
  std::vector<Float_t>* jet_pt;
  std::vector<Float_t>* jet_phi;
  std::vector<Float_t>* jet_eta;
  std::vector<Float_t>* jet_jvt;
  std::vector<Float_t>* jet_timing;
  std::vector<Int_t>* jet_passJvt;
}; 

#endif //> !VBFANALYSIS_HFINPUTALG_H
