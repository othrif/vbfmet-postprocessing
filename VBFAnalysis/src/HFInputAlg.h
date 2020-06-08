#ifndef VBFANALYSIS_HFINPUTALG_H
#define VBFANALYSIS_HFINPUTALG_H 1

#include "AthAnalysisBaseComps/AthAnalysisAlgorithm.h"

//Example ROOT Includes
//#include "TTree.h"
//#include "TH1D.h"

#include "TTree.h"
#include "TH1D.h"
#include <vector>
#include <map>
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
  vector <TH1F*> HistoAppend(std::string name, std::string currentCR, int bins=1);
  virtual StatusCode CheckHists(vector <std::pair<vector <TH1F*>, std::string>> hnames);
  void HistoFill(vector<TH1F*> hs, double w);
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
  double weightXETrigSF(const float met_pt,  unsigned metRunNumber, int syst);
  float  GetDPhi(const float phi1, const float phi2);

 private: 
  int npevents = 0;
  int year     = 2016;
  int totalBins = 11;
  Bool_t isMC = true;
  Bool_t isMadgraph = false;
  Bool_t mergeKTPTV = false;
  Bool_t doTMVA = false;
  Bool_t doLowNom = false; //put nominal yields for "Low" histogram for asymmetric systematics for HistFitter
  Bool_t isHigh = true;
  Bool_t weightSyst=false;
  Bool_t doPlot = false;
  Bool_t singleHist = false;
  Bool_t doVBFMETGam = false;
  Bool_t doMTFit = false;  
  Bool_t doDuplicateCheck = false;
  Bool_t doDoubleRatio = false;
  Bool_t doHighDphijj = false;  
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
  Bool_t m_doSigOverlapTree = false;
  std::map<unsigned, TFile *> m_signalOverlapFileMap;
  std::map<unsigned, TTree *> m_signalOverlapTreeMap;
  unsigned long long m_sigOverlapEvent;
  vector<int> m_sigOverlapCategory;
  //output tree
  std::string currentVariation = "Nominal";
  std::string currentSample = "Z_strong";//"W_strong";

  vector <vector <TH1F*>> hSR;
  vector <vector <TH1F*>> hCRWe;
  vector <vector <TH1F*>> hCRWep;
  vector <vector <TH1F*>> hCRWen;
  vector <vector <TH1F*>> hCRWeLowSig;
  vector <vector <TH1F*>> hCRWepLowSig;
  vector <vector <TH1F*>> hCRWenLowSig;
  vector <vector <TH1F*>> hCRWm;
  vector <vector <TH1F*>> hCRWmMT;
  vector <vector <TH1F*>> hCRWmp;
  vector <vector <TH1F*>> hCRWmn;
  vector <vector <TH1F*>> hCRFJVT;
  vector <vector <TH1F*>> hCRZll;
  vector <vector <TH1F*>> hCRZee;
  vector <vector <TH1F*>> hCRZmm;

  Int_t m_extraVars = 0;
  Int_t m_binning = 0;
  Int_t m_metdef = 0;
  Float_t m_METCut=-1.0;
  Bool_t v26Ntuples=false;

  Double_t xeSFTrigWeight;
  Double_t xeSFTrigWeight_nomu;
  Float_t met_significance;
  Float_t averageIntPerXing;
  Int_t trigger_met;
  Int_t trigger_met_encodedv2;
  Float_t w;
  Int_t runNumber;
  Int_t randomRunNumber;
  ULong64_t eventNumber;
  Bool_t in_vy_overlap;
  Bool_t passVjetsFilter;
  Bool_t passVjetsFilterTauEl;
  Int_t passJetCleanLoose;
  Int_t passJetCleanTight;
  Int_t trigger_lep;
  Int_t lep_trig_match;
  Int_t n_jet;
  Int_t n_bjet;
  Int_t n_ph;
  Int_t n_el;
  Int_t n_mu;
  Int_t n_el_w;
  Int_t n_mu_w;
  Int_t n_baseel;
  Int_t n_basemu;
  Int_t n_baseel_noOR;
  Int_t n_basemu_noOR;
  Int_t n_baseel_iso;
  Int_t n_basemu_iso;
  Float_t tmva;
  Double_t jj_mass;
  Double_t jj_deta;
  Double_t jj_dphi;
  Double_t met_tst_j1_dphi;
  Double_t met_tst_j2_dphi;
  Double_t met_tst_nolep_j1_dphi;
  Double_t met_tst_nolep_j2_dphi;
  Float_t met_tst_et;
  Float_t met_tst_nolep_et;
  Float_t met_tst_phi;
  Float_t met_tst_nolep_phi;
  Double_t met_cst_jet;
  Float_t ph_pointing_z;  
  std::vector<Int_t>* mu_charge;
  std::vector<Int_t>* basemu_charge;
  std::vector<Float_t>* mu_pt;
  std::vector<Float_t>* mu_phi;
  std::vector<Float_t>* mu_eta;
  std::vector<Int_t>* el_charge;
  std::vector<Int_t>* baseel_charge;
  std::vector<Float_t>* el_pt;
  std::vector<Float_t>* el_phi;
  std::vector<Float_t>* el_eta;
  std::vector<Float_t>* ph_pt;
  std::vector<Float_t>* ph_phi;
  std::vector<Float_t>* ph_eta;
  std::vector<Float_t>* jet_pt;
  std::vector<Float_t>* jet_phi;
  std::vector<Float_t>* jet_eta;
  std::vector<Float_t>* jet_m;
  std::vector<Float_t>* jet_jvt;
  std::vector<Float_t>* jet_timing;
  std::vector<Int_t>* jet_passJvt;
  std::vector<Float_t>* jet_fjvt;
  std::vector<unsigned short> *jet_NTracks;
  
  Float_t met_soft_tst_et=-9999; 
  Float_t met_tight_tst_et=-9999;
  Float_t met_tighter_tst_et=-9999;
  Float_t met_tenacious_tst_et=-9999;
  Float_t met_tenacious_tst_phi=-9999;
  Float_t met_tenacious_tst_nolep_et=-9999;
  Float_t met_tenacious_tst_nolep_phi=-9999;

  std::vector<Float_t>* basemu_pt;
  std::vector<Float_t>* basemu_eta;
  std::vector<Float_t>* basemu_phi;
  std::vector<Float_t>* baseel_pt;
  std::vector<Float_t>* baseel_eta;
  std::vector<Float_t>* baseel_phi;
  
}; 

#endif //> !VBFANALYSIS_HFINPUTALG_H
