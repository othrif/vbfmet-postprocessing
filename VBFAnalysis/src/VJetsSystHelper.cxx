#include "VJetsSystHelper.h"

#include <TF1.h>
#include <TH1.h>
#include <TFile.h>
#include <TGraphAsymmErrors.h>
#include <TObjArray.h>
#include <TCanvas.h>
#include <iostream>

TH1 *getHisto(TDirectory *fIn, TString hname);
TH1 *rebinHisto(TH1 *h);

VJetsSystHelper::VJetsSystHelper()
{
   m_initialized = false;
   m_inputName = "input/theoretical_corrections.root";
   m_histoMap.clear();
   m_variations.clear();
   m_applyEWCorrection["eej"] = true;
   m_applyQCDCorrection["eej"] = true;
   m_applyEWCorrection["evj"] = true;
   m_applyQCDCorrection["evj"] = true;
   m_applyEWCorrection["vvj"] = true;
   m_applyQCDCorrection["vvj"] = true;
   m_smoothQCDCorrection = true;
   m_mergePDF = true;
}

VJetsSystHelper::~VJetsSystHelper()
{

   for (std::map<TString, TH1*>::iterator itr = m_histoMap.begin(); itr != m_histoMap.end(); itr++) {
      delete itr->second;
      itr->second = 0;
   }
   m_histoMap.clear();
   m_variations.clear();
}


void VJetsSystHelper::setInputFileName(TString fname)
{
   m_inputName = fname;
}

void VJetsSystHelper::applyEWCorrection(bool doApply, TString processes)
{

   TObjArray *tokens = processes.Tokenize(",");
   for (int iTok = 0; iTok < tokens->GetSize(); iTok++) {
      if (!tokens->At(iTok)) break;
      TString process = tokens->At(iTok)->GetName();
      m_applyEWCorrection[process] = doApply;
   }
}

void VJetsSystHelper::applyQCDCorrection(bool doApply, TString processes)
{

   TObjArray *tokens = processes.Tokenize(",");
   for (int iTok = 0; iTok < tokens->GetSize(); iTok++) {
      if (!tokens->At(iTok)) break;
      TString process = tokens->At(iTok)->GetName();
      m_applyQCDCorrection[process] = doApply;
   }
}

void VJetsSystHelper::smoothQCDCorrection(bool doSmooth)
{

   m_smoothQCDCorrection = doSmooth;
}

void VJetsSystHelper::mergePDF(bool do_merge_PDF)
{

   m_mergePDF = do_merge_PDF;
}

int VJetsSystHelper::initialize()
{

   std::vector<TString> variations = { "Nominal",
                                       "vjets_d1kappa_EW_High", "vjets_d1kappa_EW_Low",
                                       "vjets_d2kappa_EW_High", "vjets_d2kappa_EW_Low",
                                       "vjets_d3kappa_EW_High", "vjets_d3kappa_EW_Low",
                                       "vjets_d1K_NNLO_High", "vjets_d1K_NNLO_Low",
                                       "vjets_d2K_NNLO_High", "vjets_d2K_NNLO_Low",
                                       "vjets_d3K_NNLO_High", "vjets_d3K_NNLO_Low",
                                       "vjets_dK_NNLO_mix_High", "vjets_dK_NNLO_mix_Low",
                                     };
   if (m_smoothQCDCorrection) {
     variations.push_back("vjets_QCDSmoothing_High");
     variations.push_back("vjets_QCDSmoothing_Low");
   }

   m_nPDF = 107;
   for (Int_t p = 0; p < m_nPDF; p++) {
     variations.push_back("vjets_" + TString::Format("dK_PDF_%d_High", p + 1));
     variations.push_back("vjets_" + TString::Format("dK_PDF_%d_Low", p + 1));
   }
   m_variations = variations;

   TFile *fIn = TFile::Open(m_inputName, "READ");

   std::vector<TString> processes = {"eej", "evj", "vvj"};

   for (unsigned int iP = 0; iP < processes.size(); iP++) {

      TString process = processes[iP];

      TString suffix = "";

      TH1 *hMC = getHisto(fIn, process + "_mc" + suffix);
      if (!hMC) return 1;

      TH1 *hMC_SmoothUp = (TH1*)hMC->Clone(process + "_mc_smoothUp");
      TH1 *hMC_SmoothDn = (TH1*)hMC->Clone(process + "_mc_smoothDn");
      TH1 *hSLO = getHisto(fIn, process + "_pTV_LO");
      TH1 *hNNLO = getHisto(fIn, process + "_pTV_NNLO");
      TH1 *hKNLO = getHisto(fIn, process + "_pTV_K_NLO");
      TH1 *hKNNLO = getHisto(fIn, process + "_pTV_K_NNLO");
      TH1 *hd1KNNLO = getHisto(fIn, process + "_pTV_d1K_NNLO");
      TH1 *hd2KNNLO = getHisto(fIn, process + "_pTV_d2K_NNLO");
      TH1 *hd3KNNLO = getHisto(fIn, process + "_pTV_d3K_NNLO");
      TH1 *hkEW = getHisto(fIn, process + "_pTV_kappa_EW");
      TH1 *hd1kEW = getHisto(fIn, process + "_pTV_d1kappa_EW");
      TH1 *hd2kEW = getHisto(fIn, process + "_pTV_d2kappa_EW");
      TH1 *hd3kEW = getHisto(fIn, process + "_pTV_d3kappa_EW");
      TH1 *hdKNNLOmix = getHisto(fIn, process + "_pTV_dK_NNLO_mix");

      std::map <TString, TH1*> hdPDF;
      for (Int_t p = 0; p < m_nPDF; p++) {
         hdPDF[TString::Format("PDF%d", p + 1)] = getHisto(fIn, process + TString::Format("_pTV_dK_PDF_%d", p + 1));
      }

      /**
       * This is smoothing using a linear fit
       */
      TH1 *hTH = (TH1*)hSLO->Clone();
      hTH->Multiply(hKNNLO);
      TH1 *hQCDCorr = rebinHisto(hTH); // (TH1*)hTH->Clone(); //
      hQCDCorr->Divide(rebinHisto(hMC)); // hMC); //
      TGraphAsymmErrors *gQCDCorr = new TGraphAsymmErrors();
      for (int bin = 1; bin <= hQCDCorr->FindBin(1999.99); bin++) {
         double content = hQCDCorr->GetBinContent(bin);
         double error = hQCDCorr->GetBinError(bin);
         double binxmin = hQCDCorr->GetXaxis()->GetBinLowEdge(bin) + 0.001;
         double binxmax = hQCDCorr->GetXaxis()->GetBinUpEdge(bin) - 0.001;
         int binmin = hTH->FindBin(binxmin);
         int binmax = hTH->FindBin(binxmax);
         double sumPt = 0;
         double sumW = 0;
         for (int obin = binmin; obin <= binmax; obin++) {
            sumPt += hTH->GetBinCenter(obin) * hTH->GetBinContent(obin) * hTH->GetBinWidth(obin);
            sumW += hTH->GetBinContent(obin) * hTH->GetBinWidth(obin);
         }
         double avgPt = hQCDCorr->GetBinCenter(bin);
         if (sumW != 0) {
            avgPt = sumPt / sumW;
         }
         gQCDCorr->SetPoint(bin - 1, avgPt, content);
         gQCDCorr->SetPointError(bin - 1, 0, 0, error, error);
      }

      if (m_smoothQCDCorrection) {
         TF1 *fLinear = new TF1(process + "_fLinear", "pol1", 0, 6500); //hMC->GetXaxis()->GetXmin(), hMC->GetXaxis()->GetXmax());
         gQCDCorr->Fit(fLinear, "NO", "", 200, 2000);
         TF1 *fTruncated = new TF1(process + "_fTruncated", "x<1200?([0]+[1]*x):[2]", 0, 6500);
         fTruncated->SetParameter(0, fLinear->GetParameter(0));
         fTruncated->SetParameter(1, fLinear->GetParameter(1));
         fTruncated->SetParameter(2, fLinear->Eval(1200));
         fTruncated->SetParError(0, fLinear->GetParError(0));
         fTruncated->SetParError(1, fLinear->GetParError(1));
         fLinear->SetParameter(1, fLinear->GetParameter(1) + fLinear->GetParError(1));
         fTruncated->SetParError(2, fLinear->Eval(1200) - fTruncated->Eval(1200));
         m_fit[process] = fTruncated;
         //      TF1 *fitup = new TF1(process+"_fUp", "(x<1000?[0]+[1]*x:[2]) + TMath::Sqrt( [3]*[3] + [4]*[4]*x*x )",
         TF1 *fitup = new TF1(process + "_fUp", "(x<1200?[0]+[1]*x:[2]) + (x<1200?TMath::Sqrt( [3]*[3] + [4]*[4]*x*x ):[2]*0.05)", 0, 2000);
         fitup->SetParameter(0, fTruncated->GetParameter(0));
         fitup->SetParameter(1, fTruncated->GetParameter(1));
         fitup->SetParameter(2, fTruncated->GetParameter(2));
         fitup->SetParameter(3, fTruncated->GetParError(0));
         fitup->SetParameter(4, fTruncated->GetParError(1));
         m_fit[process + "_up"] = fitup;
         //      TF1 *fitdn = new TF1(process+"_fDn", "(x<1000?[0]+[1]*x:[2]) - TMath::Sqrt( [3]*[3] + [4]*[4]*x*x )",
         TF1 *fitdn = new TF1(process + "_fDn", "(x<1200?[0]+[1]*x:[2]) - (x<1200?TMath::Sqrt( [3]*[3] + [4]*[4]*x*x ):[2]*0.05)", 0, 2000);
         fitdn->SetParameter(0, fTruncated->GetParameter(0));
         fitdn->SetParameter(1, fTruncated->GetParameter(1));
         fitdn->SetParameter(2, fTruncated->GetParameter(2));
         fitdn->SetParameter(3, fTruncated->GetParError(0));
         fitdn->SetParameter(4, fTruncated->GetParError(1));
         m_fit[process + "_dn"] = fitdn;
         hMC = (TH1*)hSLO->Clone();
         hMC->Multiply(hKNNLO);
         // hMC->Scale(0.9725);
         hMC->Divide(fTruncated);
         hMC_SmoothUp = (TH1*)hSLO->Clone();
         hMC_SmoothUp->Multiply(hKNNLO);
         // hMC_SmoothUp->Scale(0.9725);
         hMC_SmoothUp->Divide(fitup);
         hMC_SmoothDn = (TH1*)hSLO->Clone();
         hMC_SmoothDn->Multiply(hKNNLO);
         // hMC_SmoothDn->Scale(0.9725);
         hMC_SmoothDn->Divide(fitdn);
      }



      for (unsigned int iVar = 0; iVar < m_variations.size(); iVar++) {

         TString variation = m_variations[iVar];
         TH1 *hMC_used = hMC;

         if (variation == "vjets_QCDSmoothing_High") hMC_used = hMC_SmoothUp;
         if (variation == "vjets_QCDSmoothing_Low") hMC_used = hMC_SmoothDn;

         const Int_t n_var = m_nPDF + 8;
         double e[n_var];
	 for (Int_t p = 0; p < 8+m_nPDF; p++)  {
	   e[p] = 0;
	 }
         if (variation == "vjets_d1kappa_EW_High") e[0] = 1;
         if (variation == "vjets_d1kappa_EW_Low") e[0] = -1;
         if (variation == "vjets_d2kappa_EW_High") e[1] = 1;
         if (variation == "vjets_d2kappa_EW_Low") e[1] = -1;
         if (variation == "vjets_d3kappa_EW_High") e[2] = 1;
         if (variation == "vjets_d3kappa_EW_Low") e[2] = -1;
         if (variation == "vjets_d1K_NNLO_High") e[3] = 1;
         if (variation == "vjets_d1K_NNLO_Low") e[3] = -1;
         if (variation == "vjets_d2K_NNLO_High") e[4] = 1;
         if (variation == "vjets_d2K_NNLO_Low") e[4] = -1;
         if (variation == "vjets_d3K_NNLO_High") e[5] = 1;
         if (variation == "vjets_d3K_NNLO_Low") e[5] = -1;
         if (variation == "vjets_dK_NNLO_mix_High") e[6] = 1;
         if (variation == "vjets_dK_NNLO_mix_Low") e[6] = -1;
         for (Int_t p = 0; p < m_nPDF; p++) {
            if (variation == "vjets_" + TString::Format("dK_PDF_%d_High", p + 1)) e[p + 8] = 1;
            if (variation == "vjets_" + TString::Format("dK_PDF_%d_Low", p + 1)) e[p + 8] = -1;
         }

         TH1 *hVar = (TH1*)hMC_used->Clone(process + "_" + variation);
         hVar->SetDirectory(0);
         hVar->Reset();

         for (int bin = 1; bin <= hMC_used->GetNbinsX() + 1; bin++) {

            double kappa_EW = hkEW->GetBinContent(bin);
            double d1kappa_EW = hd1kEW->GetBinContent(bin);
            double d2kappa_EW = hd2kEW->GetBinContent(bin);
            double d3kappa_EW = hd3kEW->GetBinContent(bin);
            double K_NNLO = hKNNLO->GetBinContent(bin);
            double K_NLO = hKNLO->GetBinContent(bin);
            double d1K_NNLO = hd1KNNLO->GetBinContent(bin);
            double d2K_NNLO = hd2KNNLO->GetBinContent(bin);
            double d3K_NNLO = hd3KNNLO->GetBinContent(bin);
            double dK_NNLO_mix = hdKNNLOmix->GetBinContent(bin);

            double dK_PDF[m_nPDF];
            for (Int_t p = 0; p < m_nPDF; p++) {
               dK_PDF[p] = hdPDF[TString::Format("PDF%d", p + 1)]->GetBinContent(bin);
            }


            double sLO = hSLO->GetBinContent(bin);
            double thNNLO = hNNLO->GetBinContent(bin);

            double e_kappa_EW = kappa_EW + e[0] * d1kappa_EW + e[1] * d2kappa_EW + e[2] * d3kappa_EW;
            double e_K_NNLO = K_NNLO + e[3] * d1K_NNLO + e[4] * d2K_NNLO + e[5] * d3K_NNLO ;

	    for (Int_t p = 0; p < m_nPDF; p++)  {
	      e_K_NNLO += e[p + 8] * dK_PDF[p];
	    }
            double e_K = e_K_NNLO * (1 + e_kappa_EW) + e[6] * dK_NNLO_mix;

            double sNNLO = e_K * sLO;

            if (!m_applyEWCorrection[process]) {
               sNNLO /= (1 + kappa_EW);
            }

            if (!m_applyQCDCorrection[process]) {
               sNNLO *= hMC_used->GetBinContent(bin) / (K_NNLO * sLO) ;
            }

	    hVar->SetBinContent(bin, sNNLO);

	 }
         TH1 *hNum = rebinHisto(hVar); // (TH1*)hVar->Clone(); //
         TH1 *hDen = rebinHisto(hMC_used); // hMC_used; //

         hNum->Divide(hDen);
         m_histoMap[hVar->GetName()] = hNum;

      }
   }

   fIn->Clear();
   fIn->Close();
   delete fIn;
   m_initialized = true;
   std::cout << "INFO: Initialization completed" << std::endl;
   return 0;
}


const std::vector<TString> &VJetsSystHelper::getAllVariationNames()
{

  static std::vector<TString> all_variation_names;

  for (auto variation: m_variations) {
    if (m_mergePDF and variation.Contains("dK_PDF")) continue;
    all_variation_names.push_back(variation);
  }
  if (m_mergePDF) {
    all_variation_names.push_back("vjets_dK_PDF_High");
    all_variation_names.push_back("vjets_dK_PDF_Low");
  }

  if (!m_initialized) {
    std::cout << "ERROR: VJetsSystHelper not initialized (called getAllVariationNames)" << std::endl;
    return all_variation_names;
  }

  return all_variation_names;

}

double VJetsSystHelper::getCorrection(int mcChannelNumber, double pTV, TString variation)
{

   if (!m_initialized) {
      std::cout << "ERROR: VJetsSystHelper not initialized" << std::endl;
      return 1;
   }

   TString process = "";
   // Sherpa 2.2.1
   if ((364142 <= mcChannelNumber && mcChannelNumber <= 364155)||mcChannelNumber==364222||mcChannelNumber==364223 ||
	    (366010 <= mcChannelNumber && mcChannelNumber <= 366017)||
	    (366019 <= mcChannelNumber && mcChannelNumber <= 366026)||
	    (366028 <= mcChannelNumber && mcChannelNumber <= 366035)) process = "vvj"; // Zvv
   //   else if ((364142 <= mcChannelNumber && mcChannelNumber <= 364155)||mcChannelNumber==364222||mcChannelNumber==364223) process = "vvj"; // Zvv
   else if ((364184 <= mcChannelNumber && mcChannelNumber <= 364197)||mcChannelNumber==364228||mcChannelNumber==364229) process = "evj"; // Wtv
   else if ((364156 <= mcChannelNumber && mcChannelNumber <= 364169)||mcChannelNumber==364224||mcChannelNumber==364225) process = "evj"; // Wuv
   else if ((364170 <= mcChannelNumber && mcChannelNumber <= 364183)||mcChannelNumber==364226||mcChannelNumber==364227) process = "evj"; // Wev
   else if ((364100 <= mcChannelNumber && mcChannelNumber <= 364113)||mcChannelNumber==364216||mcChannelNumber==364217) process = "eej"; // Zuu
   else if ((364114 <= mcChannelNumber && mcChannelNumber <= 364127)||mcChannelNumber==364218||mcChannelNumber==364219) process = "eej"; // Zee
   else if ((364128 <= mcChannelNumber && mcChannelNumber <= 364141)||mcChannelNumber==364220||mcChannelNumber==364221) process = "eej"; // Ztt

   if (process == "") return 1.;

   std::cout << "Process: " << process << std::endl;

   TH1 *hCorr;

   Double_t correction = 0;

   // Temporary Patch for assigning Zee PDF systs to Zvv
   TString sel_process = process;
   if (variation.Contains("dK_PDF") && process == "vvj") {
     process = "eej";
   }

   // sum in quadrature PDF uncertainties
   if (variation.Contains("dK_PDF") &&  m_mergePDF) {

     Bool_t High = variation.Contains("High");

     std::map<TString, TH1*>::iterator itr_nom = m_histoMap.find(process + "_Nominal");
     TH1* hNom = itr_nom->second;
     if (pTV < hNom->GetXaxis()->GetXmin()) return 1;
     if (pTV >= hNom->GetXaxis()->GetXmax()) return 1;
     int bin = hNom->FindBin(pTV);

     Float_t nominal = hNom->GetBinContent(bin);

     for (auto tmp_var: m_variations) {

       if (!tmp_var.Contains("dK_PDF")) continue;

       Bool_t tmp_High = tmp_var.Contains("High");
       if (High != tmp_High) continue;

       std::map<TString, TH1*>::iterator itr = m_histoMap.find(process + "_" + tmp_var);

       if (itr == m_histoMap.end()) {
	 std::cout << "Error: unknown variation: " << tmp_var << std::endl;
	 return 1;
       }

       hCorr = itr->second;
       correction += TMath::Power(hCorr->GetBinContent(bin) - nominal, 2);
       //       std::cout << process << "  " << pTV << "  " << variation << "  " << tmp_var << "  " << hCorr->GetBinContent(bin) << "  " << nominal << "  " << correction << std::endl;
     }

     if (High) correction = nominal + TMath::Sqrt(correction);
     else correction = nominal - TMath::Sqrt(correction);
     //     std:: cout << process << "  " << pTV << "  " << variation << "  " << correction << endl;

   } else {

     std::map<TString, TH1*>::iterator itr = m_histoMap.find(process + "_" + variation);
     if (itr == m_histoMap.end()) {
       std::cout << "Error: unknown variation: " << variation << std::endl;
       return 1;
     }

     hCorr = itr->second;
     if (pTV < hCorr->GetXaxis()->GetXmin()) return 1;
     if (pTV >= hCorr->GetXaxis()->GetXmax()) return 1;
     int bin = hCorr->FindBin(pTV);

     correction = hCorr->GetBinContent(bin);

   }

   // Temporary Patch for assigning Zee PDF systs to Zvv
   if (variation.Contains("dK_PDF") && sel_process == "vvj") {
     std::map<TString, TH1*>::iterator itr_eej_nom = m_histoMap.find("eej_Nominal");
     TH1* h_eej_nom = itr_eej_nom->second;
     std::map<TString, TH1*>::iterator itr_vvj_nom = m_histoMap.find("vvj_Nominal");
     TH1* h_vvj_nom = itr_vvj_nom->second;
     int bin = h_eej_nom->FindBin(pTV);
     correction = correction - h_eej_nom->GetBinContent(bin) + h_vvj_nom->GetBinContent(bin);
   }

  return correction;
}

TH1 *getHisto(TDirectory *fIn, TString hname)
{

   TH1 *h = 0;

   if (!fIn || fIn->IsZombie()) {
      return h;
   }

   TObject *obj = fIn->Get(hname);
   if (!obj) {
      std::cout << "Error: object of name " << hname << " was not found in file " << fIn->GetName() << std::endl;
      return h;
   }

   h = (TH1*)obj->Clone();

   return h;
}

TH1 *rebinHisto(TH1 *h)
{

   h = (TH1*)h->Clone();

   for (int bin = 1; bin <= h->GetNbinsX(); bin++) {
      double content = h->GetBinContent(bin);
      double error = h->GetBinError(bin);
      double width = h->GetBinWidth(bin);
      h->SetBinContent(bin, content * width);
      h->SetBinError(bin, error * width);
   }

   const int nbins = 16;
   double limits[nbins + 1] = {30, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 2000, 6500};

   TH1 *hr = h->Rebin(nbins, h->GetName() + TString("_rebin"), limits);

   hr->SetBinContent(nbins - 1, hr->GetBinContent(nbins - 1) + hr->GetBinContent(nbins));
   hr->SetBinContent(nbins, 0);

   for (int bin = 1; bin <= hr->GetNbinsX(); bin++) {
      double content = hr->GetBinContent(bin);
      double error = hr->GetBinError(bin);
      double width = hr->GetBinWidth(bin);
      hr->SetBinContent(bin, content / width);
      hr->SetBinError(bin, error / width);
   }

   return hr;
}
