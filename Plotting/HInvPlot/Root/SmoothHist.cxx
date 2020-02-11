#include <HInvPlot/SmoothHist.h>
#include "HInvPlot/TRExTools.h"

#include <algorithm>
#include <cmath>
#include <forward_list>

#include <TAxis.h>
#include <TGraph.h>
#include <TGraphSmooth.h>
#include <TH1.h>
#include <TH2.h>

#include "TDirectoryFile.h"
#include "TFile.h"

// **********************************************************************
// Smoothing definitions used in WSMaker
// **********************************************************************

using namespace std;

float statError(TH1 *hnom, int beg, int end) { // end is excluded
  double err = 0;
  float nomInt = hnom->IntegralAndError(beg, end - 1, err);
  return fabs(err / nomInt);
}

float computeChi2(TH1 *hnom, TH1 *hsys, int beg, int end) {
  float ratio = hsys->Integral(beg, end) / hnom->Integral(beg, end);
  float chi2 = 0;
  for (int i = beg; i < end + 1; i++) {
    if (hnom->GetBinContent(i) != 0) {
      float iratio = hsys->GetBinContent(i) / hnom->GetBinContent(i);
      float err = hnom->GetBinError(i) / hnom->GetBinContent(i);
      chi2 += ((iratio - ratio) / err) * ((iratio - ratio) / err);
    }
  }
  return chi2;
}

int findSmallerChi2(TH1 *hnom, TH1 *hsys, const std::vector<int> &extrema) {
  int pos = 0;
  float minval = 99999;
  for (unsigned int i = 0; i < extrema.size() - 1; i++) {
    float chi2 = computeChi2(hnom, hsys, extrema[i], extrema[i + 1]);
    if (chi2 < minval) {
      pos = i;
      minval = chi2;
    }
  }
  return pos;
}

void getRatioHist(TH1 *hnom, TH1 *hsys, const std::vector<int> &bins,
                  TH1 *res) {
  for (unsigned int iRefBin = 0; iRefBin < bins.size() - 1; iRefBin++) {
    float nomInt = hnom->Integral(bins.at(iRefBin), bins.at(iRefBin + 1) - 1);
    float varInt = hsys->Integral(bins.at(iRefBin), bins.at(iRefBin + 1) - 1);
    for (int b = bins.at(iRefBin); b < bins.at(iRefBin + 1); b++) {
      if (nomInt != 0) {
        res->SetBinContent(b, varInt / nomInt);
      } else {
        res->SetBinContent(b, 0);
      }
    }
  }
}

TH1 *getRatioHist(TH1 *hnom, TH1 *hsys, const std::vector<int> &bins) {
  TH1 *res = (TH1 *)hsys->Clone();
  getRatioHist(hnom, hsys, bins, res);
  return res;
}

// inclusive in lo and hi
void mergeBins(int lo, int hi, std::vector<int> &bins) {
  std::vector<int>::iterator beg =
      std::upper_bound(bins.begin(), bins.end(), lo);
  // +1 because inclusive merge
  std::vector<int>::iterator last =
      std::lower_bound(bins.begin(), bins.end(), hi + 1);
  bins.erase(beg, last);
}

std::vector<int> findExtrema(TH1 *h) {
  std::vector<int> res;
  res.push_back(1);
  int status = 0; // 1: potential max, -1: potential min
  int k = 1;
  for (int i = 2; i < h->GetNbinsX() + 1; i++) {
    // special rule for bins with 0 stat. Keep going on, until one finds another
    // bin to compare to
    if (h->GetBinContent(i) < 1.e-6) {
      continue;
    }
    if (status == 1 && h->GetBinContent(i) < h->GetBinContent(k) - 1.e-6) {
      res.push_back(i - 1);
      status = -1;
    }
    if (status == -1 && h->GetBinContent(i) > h->GetBinContent(k) + 1.e-6) {
      res.push_back(i - 1);
      status = 1;
    }
    if (status == 0 && h->GetBinContent(i) < h->GetBinContent(k) - 1.e-6) {
      status = -1;
    }
    if (status == 0 && h->GetBinContent(i) > h->GetBinContent(k) + 1.e-6) {
      status = 1;
    }
    k = i;
  }
  res.push_back(h->GetNbinsX());

  return res;
}

std::vector<int> SmoothHist::getLocalExtremaBinning(TH1 *hnom, TH1 *hsys,
                                                    unsigned int nmax) {
  // This implementation is iterative.
  // A faster (say analytic) implementation is possible if this one proves to be
  // too slow. This one is however easier to write and read
  std::vector<int> res;
  double err = 0;
  float sum = hnom->IntegralAndError(0, hnom->GetNbinsX()+1, err);
  //float sum = hnom->IntegralAndError(1, hnom->GetNbinsX(), err);
  // too large stat unc: no shape
  if (sum>0. && fabs(err / sum) > StatErr) {
    res.push_back(1);
    res.push_back(hnom->GetNbinsX() + 1);
    return res;
  }

  // normal case. Then, beginning with no rebinning
  for (int i = 1; i < hnom->GetNbinsX() + 2; i++) {
    res.push_back(i);
  }

  TH1 *ratio = getRatioHist(hnom, hsys, res);
  std::vector<int> extrema = findExtrema(ratio);

  while (extrema.size() > nmax + 2) {
    int pos = findSmallerChi2(hnom, hsys, extrema);
    mergeBins(extrema[pos], extrema[pos + 1], res);
    getRatioHist(hnom, hsys, res, ratio);
    extrema = findExtrema(ratio);
  }

  // second pass to avoid bins with too large stat uncertainty
  std::vector<int>::iterator fst = res.end();
  std::vector<int>::iterator lst = res.end();
  std::vector<int> to_remove;
  --lst;
  --fst;
  while (fst != res.begin()) {
    if (fst == lst) {
      --fst;
    } else {
      float statE = statError(hnom, *fst, *lst);
      if (statE > StatErr) {
        to_remove.push_back(fst - res.begin());
        --fst;
      } else {
        lst = fst;
      }
    }
  }
  for (int i : to_remove) {
    res.erase(res.begin() + i);
  }

  delete ratio;
  return res;
}


TH1 *SmoothHist::smoothHistogram(TH1 *hnom, TH1 *hsys, bool smooth) {
  
  if (rebinFactor > 0){
    hnom->Rebin(rebinFactor);
    hsys->Rebin(rebinFactor);
  }

  const std::vector<int> bins = getLocalExtremaBinning(hnom, hsys, Nmax);
  float norm_init = hsys->Integral();
  TH1 *ratio = getRatioHist(hnom, hsys, bins);

  if (smooth && ratio->GetNbinsX() > 2) {
    std::vector<float> vals(ratio->GetNbinsX() - 2);
    for (int i = 2; i < ratio->GetNbinsX(); i++) {
      vals[i - 2] =
          (2. * ratio->GetBinContent(i) + ratio->GetBinContent(i - 1) +
           ratio->GetBinContent(i + 1)) /
          4.;
    }
    for (int i = 2; i < ratio->GetNbinsX(); i++) {
      ratio->SetBinContent(i, vals[i - 2]);
    }
  }

  for (int i = 1; i < hsys->GetNbinsX() + 1; i++) {
    if (hnom->GetBinContent(i) != 0) {
      hsys->SetBinContent(i, ratio->GetBinContent(i) * hnom->GetBinContent(i));
    } else {
      hsys->SetBinContent(i, 0);
    }
  }
  hsys->Scale(norm_init / hsys->Integral());
  delete ratio;
  // set bin errors to 0 for systematics. Easier later when doing chi2 tests
  for (int i = 0; i < hsys->GetNbinsX() + 2; i++) {
    hsys->SetBinError(i, 0);
  }
  return hsys;
}

// **********************************************************************
// Function for caclulating chi2 from TH1F
// **********************************************************************

double chi2(TH1 *const hnom, TH1 *const hsmooth) {

  double chi2 = 0.0;
  for (int i = 1; i < hnom->GetNbinsX() + 1; ++i) {
    chi2 += std::pow(hsmooth->GetBinContent(i) - hnom->GetBinContent(i), 2);
    // if ( h_nom->GetBinError(i) != 0.0 ) chi2 /=
    // std::pow(h_nom->GetBinError(i),2);
  }

  // chi2 += std::pow(maxDelta(h_smooth),2);

  return fabs(chi2);
}

double SmoothHist::getBestSpan(TH1 *const hnom, TH1 *const hsys) {
  // Loop over all points to be removed
  double bestSpan(0.);
  int npoints = hnom->GetNbinsX();
  if (npoints < 2)
    return bestSpan; // don't do anything if bins <2.
  for (int i = 0; i < npoints; ++i) {

    double bestChi2Point(-1.);
    double bestSpanPoint(-1.);

    // loop over spans
    for (auto span : spans) {

      double chi2_up;
      // Smooth
      smoothRemovePoint(hnom, hsys, span, chi2_up, i);

      // Store best chi2 and span
      if (bestSpanPoint < 0. || chi2_up < bestChi2Point) {
        bestChi2Point = chi2_up;
        bestSpanPoint = span;
      }
      // std::cout << "span = " << span << " , chi2_up = " << chi2_up <<
      // std::endl;

    } // span loop

    // printf("---> Point %2d : Best span up = %4.3f\n", i, bestSpanPoint);
    bestSpan += bestSpanPoint;

  } // point loop

  // Calculate best span
  bestSpan /= npoints;
  // printf("===> %-60s :   Best span = %4.3f\n", sysName.Data(), bestSpan_up);
  return bestSpan;
}

// **********************************************************************
// Function for smoothing deltas
// **********************************************************************
TH1 *SmoothHist::smoothRemovePoint(TH1 *const hnom, TH1 *const hsys,
                                   float span_up, double &chi2_up,
                                   const int pointRemoved) {
  // if nbins < 2, do nothing.
  if (hsys->GetNbinsX() < 2)
    return hsys;
  // otherwise perfome smoothing.
  //
  TH1F *h_cl = nullptr;
  TH1F *h_up_cl = nullptr;

  h_cl = (TH1F *)hnom->Clone(TString::Format("%d", pointRemoved));
  h_up_cl = (TH1F *)hsys->Clone(TString::Format("%d", pointRemoved));
  //No rebinning here. Already done.
  /*if (rebinFactor > -1) {
    h_cl->Rebin(rebinFactor);
    h_up_cl->Rebin(rebinFactor);
  } else if (rebinFactor == -2) {
    std::vector<Double_t> binning = {
        -1.000, -0.867, -0.733, -0.600, -0.467, -0.333, -0.200, -0.067,
        0.067,  0.200,  0.333,  0.467,  0.600,  0.733,  0.867,  1.000};
    Double_t *binarray = binning.data();

    h_cl = (TH1F *)hnom->Rebin(15, "_rebinned", binarray);
    h_up_cl = (TH1F *)hsys->Rebin(15, "_rebinned", binarray);
  } else {
  }*/ 

  if (relative) {
    span_up = span_up * h_cl->GetBinWidth(1);
  }

  const int npoints = h_cl->GetNbinsX();

  // Get Delta or ratio
  TH1F *h_delta_up = (TH1F *)h_up_cl->Clone();
  if (DeltaOrRatio == SmoothType::SmoothDelta) {
    h_delta_up->Add(h_cl, -1.); // h_delta_up = h_up - h_nom
  } else {
    const int nbins = h_delta_up->GetNbinsX();
    for (int i = 1; i < nbins + 1; ++i) {
      if (h_cl->GetBinContent(i) != 0.0)
        h_delta_up->SetBinContent(i, h_delta_up->GetBinContent(i) /
                                         h_cl->GetBinContent(i));
      else
        h_delta_up->SetBinContent(i, 1.0);
    }
  }

  // Convert TH1 to TGraph
  TGraph *g_delta_up = new TGraph(h_delta_up);

  // Get x values of graph
  Double_t *xpoints = new Double_t(npoints);
  for (int i = 0; i < npoints; ++i)
    xpoints[i] = h_delta_up->GetBinCenter(i + 1);

  if (pointRemoved != -1) { // Remove point i
    g_delta_up->RemovePoint(pointRemoved);
  }

  // Smooth without removing points
  TGraph *g_delta_up_fin = new TGraph(h_delta_up);
  TGraphSmooth gs_smooth_up_fin;
  TGraph *g_delta_up_smooth = nullptr;
  if (pointRemoved != -1) {
    g_delta_up_smooth = gs_smooth_up_fin.SmoothKern(g_delta_up, kernel.c_str(),
                                                    span_up, npoints, xpoints);
  } else {
    g_delta_up_smooth = gs_smooth_up_fin.SmoothKern(
        g_delta_up_fin, kernel.c_str(), span_up, npoints, xpoints);
  }

  // Get the y values of the smoothed histogram
  double *yval_up = new double(npoints);
  int filled = 0;
  bool extrap = false;
  for (int i = 0; i < g_delta_up_smooth->GetN(); ++i) {
    if (i == pointRemoved && !extrap) {
      double y_up_inter =
          g_delta_up_smooth->Eval(xpoints[pointRemoved], nullptr, "S");
      yval_up[pointRemoved] = y_up_inter;
      ++filled;
      --i;
      extrap = true;
    } else {
      double x(0.0), y_up(0.0);
      g_delta_up_smooth->GetPoint(i, x, y_up);
      if (fabs(x - xpoints[filled]) < 1.E-10) {
        yval_up[filled] = y_up;
        ++filled;
      }
    }
  }
  // ... and convert the graph to a histogram
  TH1F *h_delta_up_smooth = (TH1F *)h_delta_up->Clone();
  for (int i = 1; i < h_delta_up_smooth->GetNbinsX() + 1; ++i) {
    h_delta_up_smooth->SetBinContent(i, yval_up[i - 1]);
  }

  TH1F *h_delta_up_reb = nullptr;
  TH1F *h_delta_up_reb_sm = nullptr;

  // The following is to be used for custom rebinning
  // why apply rebinning agian???
  /*if (rebinFactor == -2) {
    std::vector<Double_t> binning = {
        -1.000, -0.867, -0.733, -0.600, -0.467, -0.333, -0.200, -0.067,
        0.067,  0.200,  0.333,  0.467,  0.600,  0.733,  0.867,  1.000};
    Double_t *binarray = binning.data();

    h_delta_up_reb = (TH1F *)h_delta_up->Rebin(15, "_rebinned", binarray);
    h_delta_up_reb_sm =
        (TH1F *)h_delta_up_smooth->Rebin(15, "_rebinned", binarray);
  }*/

  // The following is to be used for constant rebinning
    h_delta_up_reb = (TH1F *)h_delta_up->Clone();
    h_delta_up_reb_sm = (TH1F *)h_delta_up_smooth->Clone();


  // Calculate chi2
  chi2_up = chi2(h_delta_up_reb, h_delta_up_reb_sm);

  // Get absolute histograms from deltas
  // sysHistoFromDelta(h_cl, h_delta_up_reb_sm, smoothType);
  if (DeltaOrRatio == SmoothType::SmoothDelta)
    h_delta_up_reb_sm->Add(h_cl);
  else
    h_delta_up_reb_sm->Multiply(h_cl);
  // Set bin errors to 0.
  for (int i = 1; i < h_delta_up->GetNbinsX() + 1; ++i)
    h_delta_up_reb_sm->SetBinError(i, 0.0);

  delete [] xpoints;
  delete [] yval_up;
  return h_delta_up_reb_sm;
}
///

TH1 *SmoothHist::smoothWithKernel(TH1 *const hnom, TH1* hsys) {
  //gErrorIgnoreLevel = kFatal;
  // Check if nbins < 2. If yes, do nothing.
  if (hsys->GetNbinsX() < 2)
    return hsys;
  // Otherwise perform smoothing.
  //
  if (rebinFactor > 0){
    hnom->Rebin(rebinFactor);
    hsys->Rebin(rebinFactor);
  }
  // Get best span
  float bestSpan = getBestSpan(hnom, hsys);
  //if (rebinFactor > 0){
  //  bestSpan *= hnom->GetBinWidth(1)*rebinFactor;
  //}
  double chi2Sys;
  TH1 *hsys_smooth = smoothRemovePoint(hnom, hsys, bestSpan, chi2Sys, -1);
  // hsys is cloned with name include Smooth.
  hsys_smooth->SetName(hsys->GetName());

  TH1* tmpHist = hsys;
  hsys = (TH1*)hsys_smooth->Clone();
  delete hsys_smooth;
  delete tmpHist;
  return hsys;
}

//-------------------
//For TRExFitter
//-------------------
TH1* SmoothHist::Smooth_Ttres(TH1 *hnom, TH1 *hsys){
  return TREx::Smooth_Ttres(hnom, hsys, independentVar); 
}

TH1* SmoothHist::Smooth_maxVariations(TH1* hnom, TH1* hsys){
  return TREx::Smooth_maxVariations(hnom, hsys, TRExNbins, TREx_tolerance);
}

//-------------------
//This is a common interface to all methods
//------------------
TH1* SmoothHist::Smooth(TH1* hnom, TH1* hsys, string SmoothingMethod){

  if (!hnom ){
    std::cerr<<"ERROR: passing null pointer to nominal hists."<<std::endl;
  }
  if (!hsys ){
    std::cerr<<"ERROR: passing null pointer to systematic hists."<<std::endl;
  }
  
  if (SmoothingMethod=="smoothRebinMonotonic"){
    setNmax(0);
    return smoothHistogram(hnom, hsys, true); 
  }else if(SmoothingMethod=="smoothRebinParabolic"){
    setNmax(1);
    return smoothHistogram(hnom, hsys, true);
  }else if (SmoothingMethod=="smoothDeltaUniformKernel"){
    setKernelOption("box");
    setSmoothType("delta");
    return smoothWithKernel(hnom, hsys);
  }else if(SmoothingMethod=="smoothRatioUniformKernel"){
    setKernelOption("box");
    setSmoothType("ratio");
    return smoothWithKernel(hnom, hsys);
  }else if (SmoothingMethod=="smoothDeltaGaussKernel"){
    setKernelOption("normal");
    setSmoothType("delta");
    return smoothWithKernel(hnom, hsys);
  }else if(SmoothingMethod=="smoothRatioGaussKernel"){
    setKernelOption("normal");
    setSmoothType("ratio");
    return smoothWithKernel(hnom, hsys);
  }else if (SmoothingMethod=="smoothTtresDependent"){
    setIndependentVar(false);
    return Smooth_Ttres(hnom, hsys); 
  }else if (SmoothingMethod=="smoothTtresIndependent"){
    setIndependentVar(true);
    return Smooth_Ttres(hnom, hsys); 
  }else if (SmoothingMethod=="smoothTRExDefault"){
    return Smooth_maxVariations(hnom, hsys);
  }else{
    std::cerr<<"ERROR: Choose one method from smoothRebinMonotonic, smoothRebinParabolic,smoothDeltaUniformKernel,smoothRatioUniformKernel,smoothDeltaGaussKernel,smoothRatioGaussKernel, smoothTtresDependent, smoothTtresIndependent, smoothTRExDefault"<<std::endl;
    return nullptr;
  }


}

