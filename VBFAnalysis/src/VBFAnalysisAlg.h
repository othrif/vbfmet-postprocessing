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

  bool is2015;
  bool is2016;
  TTree *m_tree = 0;
  TTree *m_tree_out = 0;
  SUSY::CrossSectionDB *my_XsecDB; 
  //  const TFile outputFile;
  TString m_treeName = "MiniNtuple";
  TString outputFileName = "ntuple";
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

  Int_t runNumber;
  Int_t averageIntPerXing;
  Float_t mcEventWeight;
  Float_t puWeight;
  Float_t jvtSFWeight;
  Float_t elSFWeight;
  Float_t muSFWeight;
  Float_t elSFTrigWeight;
  Float_t muSFTrigWeight;
  Int_t passJetClean;
  Int_t passJetCleanTight;
  Float_t met_tst_et;
}; 

#endif //> !VBFANALYSIS_VBFANALYSISALG_H
