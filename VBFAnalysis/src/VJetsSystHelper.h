#ifndef VBFANALYSIS_VJETSSYSTHELPER_H
#define VBFANALYSIS_VJETSSYSTHELPER_H 1

#include <TString.h>
#include <map>
#include <vector>

class TH1;
class TF1;

class VJetsSystHelper {

public:

  VJetsSystHelper();
  ~VJetsSystHelper();

  void setInputFileName(TString fname);
  void applyEWCorrection(bool doApply, TString processes = "eej,evj,vvj");
  void applyQCDCorrection(bool doApply, TString processes = "eej,evj,vvj");
  void smoothQCDCorrection(bool doSmooth);
  void setNominalOnly(bool setNominalOnly);
  void mergePDF(bool do_merge_PDF);
  TF1 *getFitFunction(TString process) {return m_fit[process];}

  int initialize();

  const std::vector<TString> &getAllVariationNames();

  double getCorrection(int mcChannelNumber, double pTV, double mjj, TString variation="Nominal");

private:

  Int_t m_nPDF;
  bool m_initialized;
  TString m_inputName;
  std::map<TString, TH1*> m_histoMap;
  std::vector<TString> m_variations;
  std::map<TString, bool> m_applyEWCorrection;
  std::map<TString, bool> m_applyQCDCorrection;
  bool m_smoothQCDCorrection;
  bool m_mergePDF;
  bool m_nominalOnly;
  std::map<TString, TF1 *>m_fit;
};

#endif
