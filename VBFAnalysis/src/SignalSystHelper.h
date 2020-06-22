#ifndef VBFANALYSIS_SIGNALSYSTHELPER_H
#define VBFANALYSIS_SIGNALSYSTHELPER_H 1

#include <iostream>
#include <vector>
#include <map>
#include "TTree.h"
#include "TString.h"

using namespace std;

class SignalSystHelper{
 public:
  SignalSystHelper( );
  virtual ~SignalSystHelper();

  void initialize();

  double vbf_uncert_stage_1_1(int source, int event_STXS, double Nsigma=1.0);
  std::string getVBFVarName(int selection);
  void initVBFVars(std::map<TString, Float_t> &tMapFloat, std::map<TString, Float_t> &tMapFloatW, TTree *tree);
  void initVBFGamVars(std::map<TString, Float_t> &tMapFloat, std::map<TString, Float_t> &tMapFloatW, TTree *tree);  
  void initggFVars(std::map<TString, Float_t> &tMapFloat, std::map<TString, Float_t> &tMapFloatW, TTree *tree, bool isggF);  
  void setVBFVars(std::map<TString, Float_t> &tMapFloat, int category, std::vector<Float_t>* mcEventWeights, Int_t n_jet_truth, Double_t truth_jj_mass,  Double_t truth_jj_dphi);
  void setVBFGamVars(std::map<TString, Float_t> &tMapFloat, int category, std::vector<Float_t>* mcEventWeights, Int_t n_jet_truth, Double_t truth_jj_mass,  Double_t truth_jj_dphi);  
  void setggFVars(std::map<TString, Float_t> &tMapFloat, std::vector<Float_t>* mcEventWeights, unsigned defaultPDFVal);  
  
 private:
  std::vector<double> m_uncert_deltas;
  std::map<int, double> m_powheg_xsec;
  std::map<int, std::vector<double> > m_stxs_acc;
  std::vector<std::string> m_selection; // 10 systematics names
};

#endif //> !VBFANALYSIS_SIGNALSYSTHELPER_H   
