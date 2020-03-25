// Plot the transfer factor theory uncertainty and compare two sets of uncertainties:
// 1 > Rel21
// 2 > Rel20

void plot_TF_unc(TString folder= "theoVariation_met160_020220",TString procV = "strong", TString region = "PhiHigh"){

  using namespace TMath;

  //  SetAtlasStyle();
  gStyle->SetMarkerSize(0.9);
  gStyle->SetLegendBorderSize(0);
  gStyle->SetTextSize(0.04);
  gROOT->ForceStyle();
  TH1::AddDirectory(kFALSE);

  gSystem->Exec("mkdir -p output/"+folder+"/plots/unc/");

  const int numbins = 5;
  const int numfiles = 4;
  TString Ax_SR[numbins] = {"0.8 TeV < m_{jj} < 1 TeV","1 TeV < m_{jj} < 1.5 TeV","1.5 TeV < m_{jj} < 2 TeV", "2 < m_{jj} < 3.5 TeV", "m_{jj} > 3.5 TeV"};

  double max_def = 15;
  double min_def = -6;

  TString files[] = {"Z_"+procV+"_SR"+region,"Z_"+procV+"_CRZ"+region,"W_"+procV+"_SR"+region,"W_"+procV+"_CRW"+region};
  TString legend_files[] = {"Z "+procV+" SR","Z "+procV+" CRZ","W "+procV+" SR","W "+procV+" CRW"};


  TString var[] = {"pdf"};
  int numvars =1;

  double uncStatOld[numfiles][numbins], uncStatOld_up[numfiles][numbins], uncStatOld_dn[numfiles][numbins], uncSysOld_up[numfiles][numbins], uncSysOld_dn[numfiles][numbins];

  for (int ifile =0; ifile< numfiles; ifile++)
    for (int jvar =0; jvar< numvars; jvar++){

      TString file_in = "output/"+folder+"/reweight_"+files[ifile]+".root";
      TFile *fIn = new TFile( file_in );

      TH1F  *h_sys_up = (TH1F*)fIn->Get( var[jvar]+"_up" );
      TH1F  *h_sys_dn = (TH1F*)fIn->Get( var[jvar]+"_down" );

      for (int i = 0; i < numbins; i++){
        uncSysOld_up[ifile][i] = h_sys_up->GetBinContent(i+1);
        uncSysOld_dn[ifile][i] = h_sys_dn->GetBinContent(i+1);
        uncStatOld_up[ifile][i] = h_sys_up->GetBinError(i+1);
        uncStatOld_dn[ifile][i] = h_sys_dn->GetBinError(i+1);
      }

      TString namefile = files[ifile];
      TString file_inError = "output/"+folder+"/variedYields_"+files[ifile]+".root";
      TFile *fInError = new TFile( file_inError );

      TH1F  *h_Error = (TH1F*)fInError->Get( "h_nominal" );
      TAxis *axis = h_Error->GetXaxis();
      double err[numbins],bin[numbins];
      bin[0] = h_Error->IntegralAndError(axis->FindBin(0.8),axis->FindBin(1),err[0]);
      bin[1] = h_Error->IntegralAndError(axis->FindBin(1),axis->FindBin(1.5),err[1]);
      bin[2] = h_Error->IntegralAndError(axis->FindBin(1.5),axis->FindBin(2),err[2]);
      bin[3] = h_Error->IntegralAndError(axis->FindBin(2),axis->FindBin(3.5),err[3]);
      bin[4] = h_Error->IntegralAndError(axis->FindBin(3.5),h_Error->GetNbinsX()+1,err[4]);

      uncStatOld[ifile][0] = err[0]/bin[0];
      uncStatOld[ifile][1] = err[1]/bin[1];
      uncStatOld[ifile][2] = err[2]/bin[2];
      uncStatOld[ifile][3] = err[3]/bin[3];
      uncStatOld[ifile][4] = err[4]/bin[4];

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

// Old
  TH1F* h_Z =  new TH1F("h_Z_Old_up", "h_Z_Old_up", numbins,1000 , 2500);
  hList->Add(h_Z);
  for (int i=0; i<numbins; i++) {
    double A = uncSysOld_up[0][i];
    double dA = uncStatOld_up[0][i];
    double B = uncSysOld_up[1][i];
    double dB = uncStatOld_up[1][i];
    double tmp_tf = fabs((A)/(B)-1)*100.0;
    double tmp_tf_stat = fabs(Sqrt(Power(dA/B,2)+Power(A*dB/(B*B),2)));//*100;
    std::cout << "UP: Z SR: " << A << " +- " << dA << ", Z CR: " << B << " +- " << dB << std::endl;
    std::cout << "UP: Z_SR/Z_CR: " << tmp_tf << " +- " << tmp_tf_stat << std::endl;
    h_Z->SetBinContent(i+1, tmp_tf);
    h_Z->SetBinError(i+1, tmp_tf_stat);
    h_Z->GetXaxis()->SetBinLabel(i+1,Ax_SR[i]);
  }

  h_Z->GetXaxis()->SetLabelOffset(0.01);
  h_Z->SetTitle("");
  h_Z->GetYaxis()->SetTitle("Transfer Factor Uncertainty (%)");
  h_Z->SetMinimum(min_def);
  h_Z->SetMaximum(max_def);

  h_Z->SetLineColor(kRed+1);
  h_Z->SetMarkerColor(kRed+1);
  h_Z->Draw("HIST E");

// Old
  TH1F* h_Z_dn =  new TH1F("h_Z_Old_dn", "h_Z_Old_dn", numbins,1000 , 2500);
  hList->Add(h_Z_dn);
  for (int i=0; i<numbins; i++) {
    double A = uncSysOld_dn[0][i];
    double dA = uncStatOld_dn[0][i];
    double B = uncSysOld_dn[1][i];
    double dB = uncStatOld_dn[1][i];
    double tmp_tf = fabs((A)/(B)-1)*100.0;
    double tmp_tf_stat = Sqrt(Power(dA/B,2)+Power(A*dB/(B*B),2));//*100;
    std::cout << "DN: Z SR: " << A << " +- " << dA << ", Z CR: " << B << " +- " << dB << std::endl;
    std::cout << "DN: Z_SR/Z_CR: " << tmp_tf << " +- " << tmp_tf_stat << std::endl;
    h_Z_dn->SetBinContent(i+1, tmp_tf);
    h_Z_dn->SetBinError(i+1, tmp_tf_stat);
    h_Z_dn->GetXaxis()->SetBinLabel(i+1,Ax_SR[i]);
  }

  h_Z_dn->SetLineColor(kRed+1);
  h_Z_dn->SetMarkerColor(kRed+1);
  h_Z_dn->SetLineStyle(7);
  h_Z_dn->Draw("HIST E SAME");



  TLegend *legend=new TLegend(0.58,0.69,0.85,0.94);
  legend->SetHeader("Z+jets " + procV + " reno./fact.");
  legend->SetTextFont(62);
  legend->SetTextSize(0.04);
  legend->AddEntry(h_Z, "Up variation","l");
  legend->AddEntry(h_Z_dn, "Down variation","l");
  legend->Draw();

  // Write
  c1->Print("output/"+folder+"/plots/unc/Z_"+procV+"_"+region+"_env_tf.pdf");

// W process

  TCanvas *c2 = new TCanvas( "Envelope W" , "Envelope W" );
  TPad* p2 = new TPad("p2","p2",0.0,0.25,1.0,1.0,-22);
  p2->SetBottomMargin(0.02);
  p2->Draw();

// Old
  TH1F* h_W =  new TH1F("h_W_Old_up", "h_W_Old_up", numbins,1000 , 2500);
  hList->Add(h_W);
  for (int i=0; i<numbins; i++) {
    double A = uncSysOld_up[2][i];
    double dA = uncStatOld_up[2][i];
    double B = uncSysOld_up[3][i];
    double dB = uncStatOld_up[3][i];
    double tmp_tf = fabs((A)/(B)-1)*100.0;
    double tmp_tf_stat = Sqrt(Power(dA/B,2)+Power(A*dB/(B*B),2));//*100;
    std::cout << "UP: W SR: " << A << " +- " << dA << ", W CR: " << B << " +- " << dB << std::endl;
    std::cout << "UP: W_SR/Z_CR: " << tmp_tf << " +- " << tmp_tf_stat << std::endl;
    h_W->SetBinContent(i+1, tmp_tf);
    h_W->SetBinError(i+1, tmp_tf_stat);
    h_W->GetXaxis()->SetBinLabel(i+1,Ax_SR[i]);
  }

  h_W->GetXaxis()->SetLabelOffset(0.01);
  h_W->SetTitle("");
  h_W->GetYaxis()->SetTitle("Transfer Factor Uncertainty (%)");
  h_W->SetMinimum(min_def);
  h_W->SetMaximum(max_def);

  h_W->SetLineColor(kRed+1);
  h_W->SetMarkerColor(kRed+1);
  h_W->Draw("HIST E");

// Old
  TH1F* h_W_dn =  new TH1F("h_W_Old_dn", "h_W_Old_dn", numbins,1000 , 2500);
  hList->Add(h_W_dn);
  for (int i=0; i<numbins; i++) {
    double A = uncSysOld_dn[2][i];
    double dA = uncStatOld_dn[2][i];
    double B = uncSysOld_dn[3][i];
    double dB = uncStatOld_dn[3][i];
    double tmp_tf = fabs((A)/(B)-1)*100.0;
    double tmp_tf_stat = Sqrt(Power(dA/B,2)+Power(A*dB/(B*B),2));//*100;
    std::cout << "DN: W SR: " << A << " +- " << dA << ", W CR: " << B << " +- " << dB << std::endl;
    std::cout << "DN: W_SR/Z_CR: " << tmp_tf << " +- " << tmp_tf_stat << std::endl;
    h_W_dn->SetBinContent(i+1, tmp_tf);
    h_W_dn->SetBinError(i+1, tmp_tf_stat);
    h_W_dn->GetXaxis()->SetBinLabel(i+1,Ax_SR[i]);
  }

  h_W_dn->SetLineColor(kRed+1);
  h_W_dn->SetMarkerColor(kRed+1);
  h_W_dn->SetLineStyle(7);
  h_W_dn->Draw("HIST E SAME");

  TLegend *legendW=new TLegend(0.58,0.69,0.85,0.94);
  legendW->SetHeader("W+jets " + procV + " reno./fact.");
  legendW->SetTextFont(62);
  legendW->SetTextSize(0.04);
  legendW->AddEntry(h_W, "Up variation","l");
  legendW->AddEntry(h_W_dn, "Down variation","l");
  legendW->Draw();

     // Write
  c2->Print( "output/"+folder+"/plots/unc/W_"+procV+"_"+region+"_env_tf.pdf");

  hList->Write();
  fOut->Close();
}
