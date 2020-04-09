// Othmane Rifki
// usage: root plot_pdfAlt.cxx
// Plot the ckkw/qsf up and down variations in same canvas


// Change path
void plot_pdfAlt(TString folder= "theoVariation_260320",TString procV = "strong", TString region = "PhiLow"){

 // TString procV = "EWK"; // strong, EWK
//  TString region = "PhiLow"; // PhiHigh, PhiLow, Njet

  //  SetAtlasStyle();
  gStyle->SetMarkerSize(0.9);
  gStyle->SetLegendBorderSize(0);
  gStyle->SetTextSize(0.04);
  gROOT->ForceStyle();
  TH1::AddDirectory(kFALSE);

  gSystem->Exec("mkdir -p output/"+folder+"/plots/pdf/");

  const int num = 5;
  Double_t xbins[num+1] = {0.8, 1., 1.5, 2., 3.5,5};
  TString Ax_SR[num] = {"0.8 TeV < m_{jj} < 1 TeV","1 TeV < m_{jj} < 1.5 TeV","1.5 TeV < m_{jj} < 2 TeV", "2 < m_{jj} < 3.5 TeV", "m_{jj} > 3.5 TeV"};
  int numfiles;

  double max_def = 2.4;
  double min_def = 0.65;

  //TString files[] = {"Z_"+procV+"_SR"+region,"Z_"+procV+"_CRZ"+region,"W_"+procV+"_SR"+region,"W_"+procV+"_CRW"+region};
  TString files[] = {"Z_strong", "W_strong"};
  numfiles = 2;


  for (int ifile =0; ifile< numfiles; ifile++){
    std::cout << files[ifile] << std::endl;

    TString file_in = "input/"+folder+"/theoVariation_"+files[ifile]+".root";
    TString file_out = "output/"+folder+"/plots/pdf/output.root";
    TString Legend = "Uncertainties";

    TFile *fIn = new TFile( file_in );
    TFile *fFinal = new TFile( file_out ,"recreate");

    TH1F  *h_NomT   = (TH1F*)fIn->Get( "all/jj_mass_Incl_index_0" );
    TH1F  *h_FUpT   = (TH1F*)fIn->Get( "all/jj_mass_Incl_index_113" );
    TH1F  *h_FDownT = (TH1F*)fIn->Get( "all/jj_mass_Incl_index_114" );

    TH1F  *h_Nom = (TH1F*)h_NomT->Rebin(5,h_NomT->GetName(),xbins);
    TH1F  *h_FUp = (TH1F*)h_FUpT->Rebin(num, h_FUpT->GetName(), xbins);
    TH1F  *h_FDown = (TH1F*)h_FDownT->Rebin(num, h_FDownT->GetName(), xbins);


    h_Nom->SetLineColor(kBlack);
    h_FUp->SetLineColor(kRed+1);
    h_FUp->SetMarkerColor(kRed+1);
    h_FDown->SetLineColor(kRed+1);
    h_FDown->SetMarkerColor(kRed+1);
    h_FDown->SetLineStyle(7);

    h_Nom->GetXaxis()->SetLabelOffset(0.01);
    //h_Nom->GetXaxis()->SetNdivisions(0);
    //std::cout << h_Nom->GetXaxis()->GetNdivisions() << std::endl;
    h_Nom->SetTitle("");
    h_Nom->GetYaxis()->SetTitle("Events");
//    h_Nom->SetMinimum(min_def);
//    h_Nom->SetMaximum(max_def);


  /*for (int i=1; i<=num; i++) {
    h_Nom->SetBinContent(i, 0);
    h_Nom->SetBinError(i, 0);
    h_Nom->GetXaxis()->SetBinLabel(i,Ax_SR[i-1]);
  }*/

TLegend *legend=new TLegend(0.60,0.65,0.89,0.9);
   legend->SetTextFont(62);
   legend->SetTextSize(0.04);
   legend->SetHeader(files[ifile]);
  //  legend->SetHeader("#splitline{"+Legend+"}{W #rightarrow e#nu}");
  //  legend->AddEntry(h_Nom, "Nominal","lp");

   legend->AddEntry(h_Nom, "PDF NNPDF30 [Nom]","lp");
   legend->AddEntry(h_FUp, "PDF MMHT14 [Alt]","lp");
   legend->AddEntry(h_FDown, "PDF CT14 [Alt]","lp");

  TCanvas *c = new TCanvas( Form("SystVar%d",ifile) , "SystVar" );
  c->SetLogy();
  TPad* p1 = new TPad("p1","p1",0.0,0.25,1.0,1.0,-22);
  TPad* p2 = new TPad("p2","p2",0.0,0.0,1.0,0.25,-21);
  p1->SetBottomMargin(0.02);
  p2->SetTopMargin(0.05);
  p2->SetBottomMargin(0.5);
  p1->Draw();
  p2->Draw();

  // First Pad
  p1->cd();
  h_Nom->Draw("HIST E");
  h_FUp->Draw("HIST E SAME");
  h_FDown->Draw("HIST E SAME");
  ////  ATLASLabel(0.20,0.87,true);
  legend->Draw();

  p2->cd();
  TH1F* href = (TH1F*)h_Nom->Clone("ref");
  href->Divide( h_Nom );
  href->SetMaximum(1.03);
  href->SetMinimum(0.98);
  href->GetYaxis()->SetTitle("Ratio to Nominal");

  href->GetXaxis()->SetLabelSize(0.17);
  href->GetYaxis()->SetNdivisions(505);
  href->GetYaxis()->SetLabelSize(0.12);

  href->GetXaxis()->SetTitleSize(0.17);
  href->GetXaxis()->SetTitleOffset(1.35);
  href->GetYaxis()->SetTitleSize(0.12);
  href->GetYaxis()->SetTitleOffset(0.5);

  href->Draw("AXIS");

  TF1 *line = new TF1("line","1",-100000,100000);
  line->SetLineColor(kBlack);
  line->SetLineWidth(1);
  line->Draw("same");

  TH1F* hFup = (TH1F*)h_FUp->Clone("hFup");
  hFup->Divide( h_Nom );
  hFup->Draw(" HIST SAME");

  TH1F* hFdown = (TH1F*)h_FDown->Clone("hFdown");
  hFdown->Divide( h_Nom );
  hFdown->Draw("HIST SAME");


  // Write
   c->Print( "output/"+folder+"/plots/pdf/pdfAlt_"+files[ifile]+".pdf");
  //c->Write();
  //fFinal->Close();

 }
}
