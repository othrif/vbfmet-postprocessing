#include "TFile.h"
#include "TH1.h"
#include "THStack.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "atlasstyle-00-03-05/AtlasStyle.C"

void drawStack(){

  SetAtlasStyle();
  TString name = "vbfTrig.root";
  TString var = "jj_mass";
  TFile* in = TFile::Open(name);
  std::cout<<"Reading file "<<name<<std::endl;
  std::cout<<"Plotting variable "<<var<<std::endl;
  TH1F* h_hvbf = (TH1F*)in->Get("pass_sr_vbfTrig_nn_Nominal/plotEvent_higgs/jj_mass");
  h_hvbf->SetFillStyle(0);
  h_hvbf->SetLineColor(kRed+1);
  h_hvbf->SetLineWidth(2);
  h_hvbf->SetLineStyle(kDashed);
  h_hvbf->Rebin(5);
  TH1F* h_wewk = (TH1F*)in->Get("pass_sr_vbfTrig_nn_Nominal/plotEvent_wewk/jj_mass");
  //h_wewk->SetFillStyle(1001);
  h_wewk->SetFillColor(kOrange+1);
  h_wewk->SetLineWidth(0);
  h_wewk->Rebin(5);
  TH1F* h_wqcd = (TH1F*)in->Get("pass_sr_vbfTrig_nn_Nominal/plotEvent_wqcd/jj_mass");
  //h_wqcd->SetFillStyle(1001);
  h_wqcd->SetFillColor(kOrange+2);
  h_wqcd->SetLineWidth(0);
  h_wqcd->Rebin(5);
  TH1F* h_zewk = (TH1F*)in->Get("pass_sr_vbfTrig_nn_Nominal/plotEvent_zewk/jj_mass");
  //h_zewk->SetFillStyle(1001);
  h_zewk->SetFillColor(kGreen-2);
  h_zewk->SetLineWidth(0);
  h_zewk->Rebin(5);
  TH1F* h_zqcd = (TH1F*)in->Get("pass_sr_vbfTrig_nn_Nominal/plotEvent_zqcd/jj_mass");
  //h_zqcd->SetFillStyle(1001);
  h_zqcd->SetFillColor(kSpring+8);
  h_zqcd->SetLineWidth(0);
  h_zqcd->Rebin(5);
  TH1F* h_dqcd = (TH1F*)in->Get("pass_sr_vbfTrig_nn_Nominal/plotEvent_dqcd/jj_mass");
  //h_dqcd->SetFillStyle(1001);
  h_dqcd->SetFillColor(kMagenta-10);
  h_dqcd->SetLineWidth(0);
  h_dqcd->Rebin(5);
  TH1F* h_tall = (TH1F*)in->Get("pass_sr_vbfTrig_nn_Nominal/plotEvent_tall/jj_mass");
  //h_tall->SetFillStyle(1001);
  h_tall->SetFillColor(kBlue-6);
  h_tall->SetLineWidth(0);
  h_tall->Rebin(5);
  
  THStack* hs = new THStack("hs", "");
  hs->Add(h_wqcd);
  hs->Add(h_wewk);
  hs->Add(h_zqcd);
  hs->Add(h_zewk);
  hs->Add(h_dqcd);
  hs->Add(h_tall);

  h_hvbf->GetXaxis()->SetTitle("jj_mass");
  h_hvbf->GetYaxis()->SetTitle("Events / 500 GeV");  

  TCanvas* c = new TCanvas("c", "c", 500, 500);
  c->SetLogy();
  hs->Draw("hist");
  hs->SetMaximum(1.75*hs->GetMaximum());
  hs->GetXaxis()->SetRangeUser(0, 2.0);
  h_hvbf->Draw("hist same");

  TLegend* leg = new TLegend(0.55, 0.60, 0.85, 0.9);
  leg->SetNColumns(2);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.04);


  TLatex* l = new TLatex(0.19, 0.85, "ATLAS");
  l->SetNDC();
  l->SetTextFont(72);
  l->SetTextSize(0.07);
  l->SetTextAlign(11);
  l->SetTextColor(kBlack);
  l->Draw("same");

  TLatex* p = new TLatex(0.19+0.17, 0.85, "Internal");
  p->SetNDC();
  p->SetTextFont(42);
  p->SetTextSize(0.065);
  p->SetTextAlign(11);
  p->SetTextColor(kBlack);
  p->Draw("same");

  TLatex* a = new TLatex(0.19, 0.85-0.04, "#sqrt{#it{s}} = 13 TeV, 40 fb^{-1}");
  a->SetNDC();
  a->SetTextFont(42);
  a->SetTextSize(0.05);
  a->SetTextAlign(12);
  a->SetTextColor(kBlack);
  a->Draw("same");

  TLatex* r = new TLatex(0.19, 0.85-0.08, "VBF h#rightarrowInvis SR");
  r->SetNDC();
  r->SetTextFont(42);
  r->SetTextSize(0.05);
  r->SetTextAlign(12);
  r->SetTextColor(kBlack);
  r->Draw("same");

  leg->AddEntry(h_wqcd, "#it{W} strong", "f");
  leg->AddEntry(h_wewk, "#it{W} EWK", "f");
  leg->AddEntry(h_zqcd, "#it{Z} strong", "f");
  leg->AddEntry(h_zewk, "#it{Z} EWK", "f");
  leg->AddEntry(h_dqcd, "Multijet", "f");
  leg->AddEntry(h_tall, "Other", "f");
  leg->AddEntry(h_hvbf, "H (#it{B}_{inv} = 1.00)", "l");



  leg->Draw("same");
}
