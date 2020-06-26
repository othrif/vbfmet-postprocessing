// Plot the transfer factor theory uncertainty and compare two sets of uncertainties:
// 1 > Rel21
// 2 > Rel20

#include "/afs/desy.de/user/o/othrif/atlasrootstyle/AtlasLabels.h"
#include "/afs/desy.de/user/o/othrif/atlasrootstyle/AtlasLabels.C"

void plot_TF_unc(TString folder= "allregions_final", TString region = "Njet"){

  using namespace TMath;

  //  SetAtlasStyle();
  gStyle->SetMarkerSize(0.9);
  gStyle->SetLegendBorderSize(0);
  gStyle->SetTextSize(0.04);
  gROOT->ForceStyle();
  TH1::AddDirectory(kFALSE);

  gSystem->Exec("mkdir -p output/"+folder+"/plots/unc/");

TString procV = "strong";
  const int numbins = 5;
  const int numfiles = 4;
  TString Ax_SR[numbins] = {"0.8 TeV < m_{jj} < 1 TeV","1 TeV < m_{jj} < 1.5 TeV","1.5 TeV < m_{jj} < 2 TeV", "2 < m_{jj} < 3.5 TeV", "m_{jj} > 3.5 TeV"};

  double max_def = 30;
  double min_def = -1;

  TString files[] = {"Z_"+procV+"_SR"+region,"Z_"+procV+"_CRZ"+region,"W_"+procV+"_SR"+region,"W_"+procV+"_CRW"+region};
  TString legend_files[] = {"Z "+procV+" SR","Z "+procV+" CRZ","W "+procV+" SR","W "+procV+" CRW"};


  TString var[] = {"envelope"};
  int numvars =1;

  double uncStatOld[numfiles][numbins], uncStatOld_up[numfiles][numbins], uncStatOld_dn[numfiles][numbins], uncSysOld_up[numfiles][numbins], uncSysOld_dn[numfiles][numbins];

  TH1F *h[numfiles][2]; // [ZSR, ZCR, WSR, WCR][up, down]
  for (int ifile =0; ifile< numfiles; ifile++)
    for (int jvar =0; jvar< numvars; jvar++){

      TString file_in = "output/"+folder+"/reweight_"+files[ifile]+".root";
      TFile *fIn = new TFile( file_in );

      h[ifile][0] = (TH1F*)fIn->Get( var[jvar]+"_up" );
      h[ifile][1] = (TH1F*)fIn->Get( var[jvar]+"_down" );

    }


// i=0 Znunu SR
// i=1 Zll CR
// i=2 Wlnu SR
// i=3 Wlnu CR

  TFile* fOut = new TFile("output/"+folder+"/plots/unc/env_tf_old_new.root", "RECREATE");
  TList* hList = new TList();

// Z process
  TCanvas *c1 = new TCanvas( "Envelope Z" , "Envelope Z" );
  TPad* p1 = new TPad("p1","p1",0.0,0.25,1.0,1.0,-22);
  p1->SetBottomMargin(0.02);
  p1->Draw();

// Up
  TH1F* h_Z_up = (TH1F*) h[0][0]->Clone();
  h_Z_up->Divide(h[1][0]);
  for (int i=0; i<h_Z_up->GetNbinsX(); i++) {
    h_Z_up->SetBinContent(i+1, fabs(100*(h_Z_up->GetBinContent(i+1)-1)));
    h_Z_up->SetBinError(i+1, fabs(100*h_Z_up->GetBinError(i+1)));
  }
  h_Z_up->GetXaxis()->SetLabelOffset(0.01);
  h_Z_up->SetTitle("");
  h_Z_up->GetYaxis()->SetTitle("Transfer Factor Uncertainty (%)");
  h_Z_up->SetMinimum(min_def);
  h_Z_up->SetMaximum(max_def);
  h_Z_up->SetLineColor(kRed+1);
  h_Z_up->SetMarkerColor(kRed+1);
  h_Z_up->Draw("HIST");

// Down
  TH1F* h_Z_dn = (TH1F*) h[0][1]->Clone();
  h_Z_dn->Divide(h[1][1]);
  for (int i=0; i<h_Z_dn->GetNbinsX(); i++) {
    h_Z_dn->SetBinContent(i+1, fabs(100*(h_Z_dn->GetBinContent(i+1)-1)));
    h_Z_dn->SetBinError(i+1, fabs(100*h_Z_dn->GetBinError(i+1)));
  }
  h_Z_dn->GetXaxis()->SetLabelOffset(0.01);
  h_Z_dn->SetTitle("");
  h_Z_dn->GetYaxis()->SetTitle("Transfer Factor Uncertainty (%)");
  h_Z_dn->SetMinimum(min_def);
  h_Z_dn->SetMaximum(max_def);
  h_Z_dn->SetLineColor(kRed+1);
  h_Z_dn->SetMarkerColor(kRed+1);
  h_Z_dn->SetLineStyle(7);
  h_Z_dn->Draw("HIST SAME");

  TLegend *legend=new TLegend(0.48,0.69,0.85,0.94);
  legend->SetHeader("Z+jets reno./fact. " + region);
  if (region == "VRPhiHigh")
    legend->SetHeader("Z+jets reno./fact. 2<DPhijj<2.5");
  else if (region == "Njet")
    legend->SetHeader("Z+jets reno./fact. Njet>2");
  else if (region == "METlow")
    legend->SetHeader("Z+jets reno./fact. 160 < MET < 200 GeV");
  legend->SetTextFont(62);
  legend->SetTextSize(0.04);
  legend->AddEntry(h_Z_up, "Up variation","l");
  legend->AddEntry(h_Z_dn, "Down variation","l");
  legend->Draw();

  ATLASLabel(0.2,0.87,"Internal");
  // Write
  c1->Print("output/"+folder+"/plots/unc/Z_"+procV+"_"+region+"_env_tf.pdf");


// W process

  TCanvas *c2 = new TCanvas( "Envelope W" , "Envelope W" );
  TPad* p2 = new TPad("p2","p2",0.0,0.25,1.0,1.0,-22);
  p2->SetBottomMargin(0.02);
  p2->Draw();

  // Up
  TH1F* h_W_up = (TH1F*) h[2][0]->Clone();
  h_W_up->Divide(h[3][0]);
  for (int i=0; i<h_W_up->GetNbinsX(); i++) {
    h_W_up->SetBinContent(i+1, fabs(100*(h_W_up->GetBinContent(i+1)-1)));
    h_W_up->SetBinError(i+1, fabs(100*(h_W_up->GetBinError(i+1))));
  }
  h_W_up->GetXaxis()->SetLabelOffset(0.01);
  h_W_up->SetTitle("");
  h_W_up->GetYaxis()->SetTitle("Transfer Factor Uncertainty (%)");
  h_W_up->SetMinimum(min_def);
  h_W_up->SetMaximum(max_def);
  h_W_up->SetLineColor(kRed+1);
  h_W_up->SetMarkerColor(kRed+1);
  h_W_up->Draw("HIST");

// Down
  TH1F* h_W_dn = (TH1F*) h[2][1]->Clone();
  h_W_dn->Divide(h[3][1]);
  for (int i=0; i<h_W_dn->GetNbinsX(); i++) {
    h_W_dn->SetBinContent(i+1, fabs(100*(h_W_dn->GetBinContent(i+1)-1)));
    h_W_dn->SetBinError(i+1, fabs(100*(h_W_dn->GetBinError(i+1))));
  }
  h_W_dn->GetXaxis()->SetLabelOffset(0.01);
  h_W_dn->SetTitle("");
  h_W_dn->GetYaxis()->SetTitle("Transfer Factor Uncertainty (%)");
  h_W_dn->SetMinimum(min_def);
  h_W_dn->SetMaximum(max_def);
  h_W_dn->SetLineColor(kRed+1);
  h_W_dn->SetMarkerColor(kRed+1);
  h_W_dn->SetLineStyle(7);
  h_W_dn->Draw("HIST SAME");

  legend=new TLegend(0.48,0.69,0.85,0.94);
  legend->SetHeader("W+jets reno./fact. " + region);
  if (region == "VRPhiHigh")
    legend->SetHeader("W+jets reno./fact. 2<DPhijj<2.5");
  else if (region == "Njet")
    legend->SetHeader("W+jets reno./fact. Njet>2");
  else if (region == "METlow")
    legend->SetHeader("W+jets reno./fact. 160 < MET < 200 GeV");
  legend->SetTextFont(62);
  legend->SetTextSize(0.04);
  legend->AddEntry(h_W_up, "Up variation","l");
  legend->AddEntry(h_W_dn, "Down variation","l");
  legend->Draw();
  ATLASLabel(0.2,0.87,"Internal");
  // Write
  c2->Print("output/"+folder+"/plots/unc/W_"+procV+"_"+region+"_env_tf.pdf");

  hList->Write();
  fOut->Close();
}
