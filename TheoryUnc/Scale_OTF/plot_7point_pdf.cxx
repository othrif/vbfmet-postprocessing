// Plot the 7 point variation, the envelope is not working
// root plot_7point.cxx
// Change path
//strong, EWK
// PhiHigh, PhiLow, Njet, METlow

#include "/afs/desy.de/user/o/othrif/atlasrootstyle/AtlasLabels.h"
#include "/afs/desy.de/user/o/othrif/atlasrootstyle/AtlasLabels.C"

void plot_7point_pdf(TString folder= "allregions_final", TString region = "Njet"){

  SetAtlasStyle();

  gStyle->SetMarkerSize(0.9);
  gStyle->SetLegendBorderSize(0);
  gStyle->SetTextSize(0.04);
  gROOT->ForceStyle();
  TH1::AddDirectory(kFALSE);

  gSystem->Exec("mkdir -p output/"+folder+"/plots/env/");

  int num = 5;
  TString procV = "strong";
  TString Ax_SR[5] = {"0.8 TeV < m_{jj} < 1 TeV","1 TeV < m_{jj} < 1.5 TeV","1.5 TeV < m_{jj} < 2 TeV", "2 < m_{jj} < 3.5 TeV", "m_{jj} > 3.5 TeV"};

  int numfiles;

  double max_def = 2.8;
  double min_def = 0.6;

  TString files[] = {"Z_"+procV+"_SR"+region,"Z_"+procV+"_CRZ"+region,"W_"+procV+"_SR"+region,"W_"+procV+"_CRW"+region};
  TString legend_files[] = {"Z "+procV+" SR","Z "+procV+" CRZ","W "+procV+" SR","W "+procV+" CRW"};
  numfiles = 4;

  for (int ifile =0; ifile< numfiles; ifile++){
    std::cout << files[ifile] << std::endl;

    TString file_in = "output/"+folder+"/reweight_"+files[ifile]+".root";
    TString file_out = "output/"+folder+"/plots/env/output.root";
    TString Legend = "Uncertainties";

    TFile *fIn = new TFile( file_in );
    TFile *fFinal = new TFile( file_out ,"recreate");

    TH1F  *h_Nom   = (TH1F*)fIn->Get( "pdf_down" );
    TH1F  *h_FUp   = (TH1F*)fIn->Get( "fac_up" );
    TH1F  *h_FDown = (TH1F*)fIn->Get( "fac_down" );
    TH1F  *h_RUp   = (TH1F*)fIn->Get( "renorm_up" );
    TH1F  *h_RDown = (TH1F*)fIn->Get( "renorm_down" );
    TH1F  *h_QUp   = (TH1F*)fIn->Get( "both_up" );
    TH1F  *h_QDown = (TH1F*)fIn->Get( "both_down" );
    TH1F  *h_EnvUp   = (TH1F*)fIn->Get( "pdf_up" );
    TH1F  *h_EnvDown = (TH1F*)fIn->Get( "pdf_down" );
    //h_Nom->SetLineColor(kWhite);
    //h_Nom->SetMarkerColor(kWhite);
    h_Nom->SetMarkerStyle(1);
    h_FUp->SetLineColor(kRed+1);
    h_FUp->SetMarkerColor(kRed+1);
    h_FDown->SetLineColor(kRed+1);
    h_FDown->SetMarkerColor(kRed+1);
    h_FDown->SetLineStyle(7);
    h_RUp->SetLineColor(kBlue+1);
    h_RUp->SetMarkerColor(kBlue+1);
    h_RDown->SetLineColor(kBlue+1);
    h_RDown->SetMarkerColor(kBlue+1);
    h_RDown->SetLineStyle(7);
    h_QUp->SetLineColor(kGreen+1);
    h_QUp->SetMarkerColor(kGreen+1);
    h_QDown->SetLineColor(kGreen+1);
    h_QDown->SetMarkerColor(kGreen+1);
    h_QDown->SetLineStyle(7);
    h_EnvUp->SetLineColor(kGray+1);
    h_EnvUp->SetMarkerColor(kGray+1);
    h_EnvDown->SetLineColor(kGray+1);
    h_EnvDown->SetMarkerColor(kGray+1);
    h_EnvDown->SetLineStyle(7);


    h_Nom->GetXaxis()->SetLabelOffset(0.01);
    h_Nom->GetXaxis()->SetTitle("");
    //h_Nom->GetXaxis()->SetNdivisions(0);
    //std::cout << h_Nom->GetXaxis()->GetNdivisions() << std::endl;
    h_Nom->SetTitle("");
    h_Nom->GetYaxis()->SetTitle("Ratio to Nominal");
  //  h_Nom->SetMaximum( std::max(h_QUp->GetMaximum(),
  //			      h_FUp->GetMaximum() )*1.2 );
    h_Nom->SetMinimum(min_def);
    h_Nom->SetMaximum(max_def);


  for (int i=1; i<=num; i++) {
    h_Nom->SetBinContent(i, 0);
    h_Nom->SetBinError(i, 0);
    h_Nom->GetXaxis()->SetBinLabel(i,Ax_SR[i-1]);
  }

    h_Nom->GetXaxis()->SetTickLength(0);

  TCanvas *c = new TCanvas( Form("SystVar%d",ifile) , "SystVar" );
  TPad* p1 = new TPad("p1","p1",0.0,0.25,1.0,1.0,-22);
  p1->SetBottomMargin(0.02);
  p1->Draw();

  h_Nom->Draw();
  //return 0;
  /*TH1F* envHi =  new TH1F("envhi", "envhi", num,800 , 2500);
  TH1F* envLo =  new TH1F("envhi", "envhi", num,800 , 2500);
  for (int j = 1; j <= num; ++j) {
    double yHi = h_EnvDown->GetBinContent(j); //cout << envHi->GetBinContent(j) << " -> " << yHi << endl;
    double yLow = h_EnvUp->GetBinContent(j); //cout << envLo->GetBinContent(j) << " -> " << yLow << endl;
    envHi->SetBinContent(j, yHi);
    envLo->SetBinContent(j, yLow);
  }*/

  TH1F* quadUp =  new TH1F("quadUp", "quadUp", num,800 , 2500);
  TH1F* quadLo =  new TH1F("quadLo", "quadLo", num,800 , 2500);
  for (int j = 1; j <= num; ++j) {
    double yU1 = h_RUp->GetBinContent(j)-1; //cout << "Up1 = " << yU1 << endl;
    double yU2 = h_FUp->GetBinContent(j)-1; //cout << "Up2 = " << yU2 << endl;
    double yL1 = h_RDown->GetBinContent(j)-1;
    double yL2 = h_FDown->GetBinContent(j)-1;
     quadUp->SetBinContent(j, 1-TMath::Sqrt(yU1*yU1+yU2*yU2)); //cout << "Up^2 = " << TMath::Sqrt(yU1*yU1+yU2*yU2) << endl;
     quadLo->SetBinContent(j, TMath::Sqrt(yL1*yL1+yL2*yL2)+1); //cout << "Dn = " << TMath::Sqrt(yL1*yL1+yL2*yL2) << endl;
   }
   quadUp->SetLineColor(kYellow+2);
   quadUp->SetMarkerColor(kYellow+2);
   quadLo->SetLineColor(kYellow+2);
   quadLo->SetMarkerColor(kYellow+2);
   quadLo->SetLineStyle(7);

   h_FDown->Draw("HIST   SAME ");
   h_RDown->Draw("HIST   SAME ");
   h_QDown->Draw("HIST   SAME ");
   h_EnvDown->Draw("HIST SAME ");

   h_QUp->Draw("HIST    SAME ");
   h_FUp->Draw("HIST    SAME ");
   h_RUp->Draw("HIST    SAME ");
   h_EnvUp->Draw("HIST  SAME ");
   quadUp->Draw("HIST   SAME ");
   quadLo->Draw("HIST   SAME ");


   h_Nom->Draw("AXIS same");
  ATLASLabel(0.2,0.87,"Internal");

   TLegend *legend=new TLegend(0.45,0.54,0.89,0.9);
   legend->SetTextFont(62);
   legend->SetTextSize(0.04);
   legend->SetHeader(legend_files[ifile]+" " +region);
  if (region == "VRPhiHigh")
    legend->SetHeader(legend_files[ifile]+" " +" 2<DPhijj<2.5");
  else if (region == "Njet")
  legend->SetHeader(legend_files[ifile]+" " +" Njet>2");
  else if (region == "METlow")
  legend->SetHeader(legend_files[ifile]+" " +" 160 < MET < 200 GeV");

   legend->AddEntry(h_FUp, "#mu_{F}=2","lp");
   legend->AddEntry(h_FDown, "#mu_{F}=0.5","lp");
   legend->AddEntry(h_RUp, "#mu_{R}=2","lp");
   legend->AddEntry(h_RDown, "#mu_{R}=0.5","lp");
   legend->AddEntry(h_QUp, "#mu_{F}=2,#mu_{R}=2","lp");
   legend->AddEntry(h_QDown, "#mu_{F}=0.5,#mu_{R}=0.5","lp");
   legend->AddEntry(h_EnvUp, "PDF up","lp");
   legend->AddEntry(h_EnvDown, "PDF down","lp");
   legend->Draw();

   TF1 *line = new TF1("line","1",-100000,100000);
   line->SetLineColor(kBlack);
   line->SetLineWidth(1);
   line->Draw("same");

  // Write
   c->Print( "output/"+folder+"/plots/scale_pdf_"+files[ifile]+".pdf");

 }
}
