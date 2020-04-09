// Terminology on ratios needed
// Processes:
// VBF_SR, ggF_SR
// Zvv_QCD_SR, Zvv_EWK_SR
// Zll_QCD_SR, Zll_EWK_SR
// Wlv_QCD_SR, Wlv_EWK_SR
// Zll_QCD_CR, Zll_EWK_CR
// Wlv_QCD_CR, Wlv_EWK_CR
//
// Process ratios:
// Zvv_QCD_SR/Wlv_QCD_CR, Zvv_EWK_SR/Wlv_EWK_CR
// Zvv_QCD_SR/Zll_QCD_CR, Zvv_EWK_SR/Zll_EWK_CR
// Wlv_QCD_SR/Wlv_QCD_CR, Wlv_EWK_SR/Wlv_EWK_CR
// Zvv_QCD_SR/Wlv_QCD_SR, Zvv_EWK_SR/Wlv_EWK_SR
// Zvv_QCD_SR/Zvv_EWK_SR

#define N_CUT 4
#define N_HIST 1

void plotTJVCutMjj(TString outAREA = "/Users/othmanerifki/vbf/161219/"){

  gSystem->Exec("mkdir -p "+outAREA+"/plots/Mjj");
  gSystem->Exec("mkdir -p "+outAREA+"/plots/Ratio");
  gSystem->Exec("mkdir -p "+outAREA+"/plots/TJV");

// processes histogram names and caption
  std::map<TString,TString> processname;
  //processname["VBF_SR"]="VBF H(125 ) #rightarrow inv., SR";
  //processname["ggF_SR"]="ggF H(125 ) #rightarrow inv., SR";
  processname["Zvv_EWK_SR"]="Z #rightarrow #nu#nu EWK, SR";
  processname["Zvv_QCD_SR"]="Z #rightarrow #nu#nu QCD, SR";
  //processname["Zll_EWK_SR"]="Z #rightarrow ll EWK, SR";
  //processname["Zll_QCD_SR"]="Z #rightarrow ll QCD, SR";
  //processname["Wlv_EWK_SR"]="W #rightarrow #slash{l}#nu EWK, SR";
  //processname["Wlv_QCD_SR"]="W #rightarrow #slash{l}#nu QCD, SR";
  //processname["Wlv_EWK_CR"]="W #rightarrow l#nu EWK, CRW";
  //processname["Wlv_QCD_CR"]="W #rightarrow l#nu QCD, CRW";
  processname["Zll_EWK_CR"]="Z #rightarrow ll EWK, CRZ";
  processname["Zll_QCD_CR"]="Z #rightarrow ll QCD, CRZ";

// naming of cuts and histograms
  TString cuts[] = {"Mjj2", "Mjj3","Mjj4", "Mjj5"}; // "Mjj1",
  TString names_cut[]   = {"0.8 < m_{jj} < 1 TeV", "1 < m_{jj} < 1.5 TeV", "1.5 < m_{jj} < 2 TeV", "m_{jj} > 2 TeV"};  // {"0.2 < m_{jj} < 0.8 TeV",
  //TString cuts[] = {"Mjj1", "Mjj2", "Mjj3"};
  //TString names_cut[]   = {"1 < m_{jj} < 1.5 TeV", "1.5 < m_{jj} < 2 TeV", "m_{jj} > 2 TeV"};
  TString histos[]      = {"j3_pt"};
  TString names_histo[] = {"p_{T}^{j3, VETO} [GeV]"};

// store histograms
  std::map < TString, std::map <TString, std::map < TString, TH1D*> > > h_store; // process, variable, cut, TH1D
  std::map < TString, std::map < TString, TH1D*> > h_sum; // variable, cut, TH1D

  int colors[] = {kRed, kBlue, kViolet, kOrange, kCyan+1, kMagenta-10};

  double maxYratio = 1.1;
  double minYratio = -.1;

  std::map<TString,TH1D*[N_CUT]> hProcCut;
  for (auto const& x : processname){
    TString process = x.first;
    std::cout << "Looking at process: " << process << std::endl;
    TString additional ="_5TJV";
    bool ratio = true;
    const char separator    = ' ';
    const int nameWidth     = 20;
    const int numWidth      = 8;
    TFile *f = new TFile(outAREA+"/hists_extract_"+process+".root");
    TFile *fout= new TFile(outAREA+"/out_"+process+".root","RECREATE");
//    TList *list = new TList();
    int histocounter=0;
    for (int i_h = 0; i_h < N_HIST; i_h++) // histograms
    {
     TString name; name.Form("%d",i_h);
     TCanvas *myCanvas = new TCanvas("myCanvas"+name+"_"+process, "",0,0,600,500);
     TLegend *l = new TLegend(0.72,0.67,0.92,0.91);
       TPad* p1 = new TPad("p1","p1",0.0,0.33,1.0,1.0,-22); // xlow,ylow,xup,yup
       TPad* p2 = new TPad("p2","p2",0.0,0.0,1.0,0.33,-21);
       p1->SetBottomMargin(0.02);
       p2->SetTopMargin(0.05);
       p2->SetBottomMargin(0.4);
       if(ratio){
         p1->Draw();
         p2->Draw();
       }
    for (int i_cut=0; i_cut<N_CUT; i_cut++) // cuts
    {
      if(ratio)
       p1->cd();
     p1->SetLogy();
     TString histname = histos[i_h];
     histocounter++;
     TString a = "all/"+cuts[i_cut]+"/";
     TString b = histos[i_h];
     TString h_path = a+b;
     TH1D  *htmp = (TH1D*)f->Get(h_path);
     if(!htmp){
       std::cout << "Problem with histogram " << histname << std::endl;
       break;
     }
     // store all histograms
     h_store[process][histname][cuts[i_cut]] = (TH1D*)htmp->Clone();
     h_store[process][histname][cuts[i_cut]]->SetDirectory(0);

     // Now the magic
     TH1D  *h = (TH1D*)htmp->Clone();
     h->Reset();
     TH1D  *hNoTJV = (TH1D*)h->Clone();
     int low_bin = 0;
     int high_bin = htmp->GetNbinsX();
     //std::cout << "Total Integral = " << htmp->Integral(low_bin,high_bin) << std::endl;
     for (int i = low_bin; i <= high_bin; i++) {
      //std::cout << "Bin " << i << ": " << htmp->Integral(0,i) << std::endl;
      h->SetBinContent(i,htmp->Integral(0,i));
      hNoTJV->SetBinContent(i,htmp->Integral(0,high_bin));
    }

    h->SetLineColor(colors[i_cut]); h->SetLineWidth(2);
    h->GetXaxis()->SetTitle(names_histo[i_h]);
    h->GetXaxis()->SetLabelOffset(999);
    h->GetYaxis()->SetTitle("Events");
    h->GetYaxis()->SetTitleOffset(0.9);
    h->GetYaxis()->SetTitleSize(0.07);
    h->GetYaxis()->SetTitleFont(42);
    h->GetYaxis()->SetLabelSize(0.07);
    if(histname.Contains("j3_pt")){
      h->GetYaxis()->SetTitleSize(0.045);
      h->GetYaxis()->SetTitleOffset(1.5);
      h->GetYaxis()->SetTitle("#int^{p_{T}^{j3, VETO}} p_{T}^{j3} d p_{T}");
    }
    if(i_cut==0){
       //h->SetMaximum(h->GetMaximum()*1.5);
     h->SetMaximum(0.2 * pow(h->GetMaximum() / 0.2, 1.5));
     h->SetMinimum(10);
     h->Draw("e hist same");
   }    else
   h->Draw("e hist same");

   l->SetHeader(processname[process],"l");
   l->AddEntry(h,names_cut[i_cut],"l");
   l->Draw("same");
   if(ratio){
      // Second Pad
    p2->cd();
    TH1D* h_Nom;
    TH1D* href = (TH1D*)h->Clone(cuts[i_cut]);
    h_Nom = (TH1D*)hNoTJV->Clone("nom");
    href->Divide( h_Nom );
    href->SetMaximum(maxYratio);
    href->SetMinimum(minYratio);
    href->GetXaxis()->SetLabelSize(0.13);
    href->GetXaxis()->SetTitleSize(0.15);
    href->GetXaxis()->SetTitleOffset(1.25);
    href->GetXaxis()->SetLabelOffset(0.045);
    href->GetYaxis()->SetTitle("Ratio to no TJV");
    href->GetYaxis()->SetNdivisions(505);
    href->GetYaxis()->SetLabelFont(42);
    href->GetYaxis()->SetLabelSize(0.12);
    href->GetYaxis()->SetTitleSize(0.12);
    href->GetYaxis()->SetTitleOffset(0.5);
    href->GetYaxis()->SetTitleFont(42);
    if(i_cut==0){
      href->Draw("AXIS");
      href->Draw(" HIST ");
    }else
    href->Draw(" HIST SAME");
//    list->Add(href);

    TF1 *line = new TF1("line","1",-100000,100000);
    line->SetLineColor(kBlack);
    line->SetLineWidth(1);
//                line->Draw("same");
    if(i_h==0){
      hProcCut[process][i_cut] = (TH1D*) href->Clone();
      hProcCut[process][i_cut]->SetDirectory(0);
    }
  }
}
myCanvas->SaveAs(outAREA+"/plots/Mjj/histo_"+histos[i_h]+"_"+process+additional+".pdf");
//myCanvas->SaveAs(outAREA+"/plots/Mjj/histo_"+histos[i_h]+"_"+process+additional+".C");
//list->Write("histlist", TObject::kSingleKey);
}
}

// Process ratios:
// Zvv_QCD_SR/Wlv_QCD_CR, Zvv_EWK_SR/Wlv_EWK_CR > P_Z_W_QCD/EWK
// Zvv_QCD_SR/Zll_QCD_CR, Zvv_EWK_SR/Zll_EWK_CR > P_Z_Z_QCD/EWK
// Wlv_QCD_SR/Wlv_QCD_CR, Wlv_EWK_SR/Wlv_EWK_CR > P_W_W_QCD/EWK
// Zvv_QCD_SR/Wlv_QCD_SR, Zvv_EWK_SR/Wlv_EWK_SR > S_Z_W_QCD/EWK
// Zvv_QCD_SR/Zvv_EWK_SR > F_Z_Z

std::map<TString,std::array<string,5>> processratio;
//processratio["P_Z_W_QCD"]=std::array<std::string, 5>{"Zvv_QCD_SR","Wlv_QCD_CR","Z(vv)/W(lv) QCD"  , "0.6", "1.4"};
//processratio["P_Z_W_EWK"]=std::array<std::string, 5>{"Zvv_EWK_SR","Wlv_EWK_CR","Z(vv)/W(lv) EWK"  , "0.85", "1.2"};
processratio["P_Z_Z_QCD"]=std::array<std::string, 5>{"Zvv_QCD_SR","Zll_QCD_CR","Z(vv)/Z(ll) QCD"  , "0.8", "1.4"};
processratio["P_Z_Z_EWK"]=std::array<std::string, 5>{"Zvv_EWK_SR","Zll_EWK_CR","Z(vv)/Z(ll) EWK"  , "0.8", "1.4"};
//processratio["P_W_W_QCD"]=std::array<std::string, 5>{"Wlv_QCD_SR","Wlv_QCD_CR","W(v)/W(lv) QCD"   , "0.6", "1.35"};
//processratio["P_W_W_EWK"]=std::array<std::string, 5>{"Wlv_EWK_SR","Wlv_EWK_CR","W(v)/W(lv) EWK"   , "0.6", "1.4"};
//processratio["S_Z_W_QCD"]=std::array<std::string, 5>{"Zvv_QCD_SR","Wlv_QCD_SR","Z(vv)/W(v) QCD"   , "0.8", "1.4"};
//processratio["S_Z_W_EWK"]=std::array<std::string, 5>{"Zvv_EWK_SR","Wlv_EWK_SR","Z(vv)/W(v) EWK"   , "0.95", "1.7"};
//processratio["F_Z_Z"]    =std::array<std::string, 5>{"Zvv_QCD_SR","Zvv_EWK_SR","Z(vv)QCD/Z(vv)EWK", "0", "1.9"};

int i=0;
for (auto const& x : processratio){
  TString process = x.first;
  TString name; name.Form("%d",i++);
  TCanvas *myCanvas2 = new TCanvas("myCanvas2"+name, "",0,0,600,500);
  TLegend *l2 = new TLegend(0.72,0.67,0.92,0.91);
   for (int i_cut=0; i_cut<N_CUT; i_cut++) // cuts
   {
    TH1D* hproc = (TH1D*)hProcCut[processratio[process][0]][i_cut]->Clone("ZWQCD");
    hproc->Divide( hProcCut[processratio[process][1]][i_cut] );
    hproc->GetXaxis()->SetTitle(names_histo[0]);
    hproc->SetLineColor(colors[i_cut]); hproc->SetLineWidth(2);
    hproc->SetMaximum( std::stof (processratio[process][4],nullptr));
    hproc->SetMinimum( std::stof (processratio[process][3],nullptr));
    hproc->GetXaxis()->SetLabelSize(0.045);
    hproc->GetXaxis()->SetTitleSize(0.05);
    //hproc->GetXaxis()->SetTitleOffset(0.1);
    hproc->GetXaxis()->SetLabelOffset(0.025);
    hproc->GetYaxis()->SetTitle(processratio[process][2].c_str());
    hproc->GetYaxis()->SetNdivisions(505);
    hproc->GetYaxis()->SetLabelFont(42);
    hproc->GetYaxis()->SetLabelSize(0.05);
    hproc->GetYaxis()->SetTitleSize(0.05);
    hproc->GetYaxis()->SetTitleOffset(0.);
    hproc->GetYaxis()->SetTitleFont(42);
    TH1D* h2 = (TH1D*) hproc->Clone();
    h2->Draw("hist same e");
    l2->SetHeader(processratio[process][2].c_str());
    l2->AddEntry(hproc,names_cut[i_cut],"l");
    l2->Draw("same");
  }
  myCanvas2->SaveAs(outAREA+"/plots/Mjj/eff_"+process+".pdf");
  //myCanvas2->SaveAs(outAREA+"/plots/Mjj/eff_"+process+".C");
}

/*
// Manipulate input histograms
std::vector <TString> samples;
samples.push_back("Zvv_EWK_SR");
samples.push_back("Zvv_QCD_SR");
samples.push_back("Zll_EWK_SR");
samples.push_back("Zll_QCD_SR");
samples.push_back("Wlv_EWK_SR");
samples.push_back("Wlv_QCD_SR");
int nBkgSamples = samples.size();
samples.push_back("VBF_SR");
samples.push_back("ggF_SR");
int nSamples = samples.size();
int nSignalSamples = nSamples - nBkgSamples;
TH1D  *hBkg      [N_CUT];
TH1D  *hSig      [N_CUT];
TH1D  *hBkgNoTJV [N_CUT];
TH1D  *hSigNoTJV [N_CUT];
TH1D  *hSoB      [N_CUT];
TH1D  *hSsB      [N_CUT];
for (UInt_t i_h = 0; i_h < N_HIST; i_h++) {
  for (UInt_t i_c = 0; i_c < N_CUT; i_c++) {
    TString name; name.Form("%d%d",i_c,i_h);
    TCanvas *myCanvas3 = new TCanvas("myCanvas3"+name, "",0,0,600,500);
    TLegend *l3 = new TLegend(0.6,0.7,0.9,0.9);
    l3->SetHeader(names_cut[i_c]);
    myCanvas3->SetLogy();
    for (UInt_t k = 0; k < nBkgSamples; k++) {
      if (k == 0) h_sum[histos[i_h]][cuts[i_c]] = (TH1D*)h_store[samples[k]][histos[i_h]][cuts[i_c]]->Clone("hsum_" + histos[i_h] + "_" + cuts[i_c] + "_clone");
      else h_sum[histos[i_h]][cuts[i_c]]->Add((TH1D  *)h_store[samples[k]][histos[i_h]][cuts[i_c]]);
    }
    //std::cout << "Total background in bin " << i_c << ": "<< " " << h_sum[histos[i_h]][cuts[i_c]]->Integral() << std::endl;
    h_sum[histos[i_h]][cuts[i_c]]->SetMinimum(1);
    h_sum[histos[i_h]][cuts[i_c]]->SetMaximum(h_sum[histos[i_h]][cuts[i_c]]->GetMaximum()*1.2);
    h_sum[histos[i_h]][cuts[i_c]]->SetFillStyle(3001);
    h_sum[histos[i_h]][cuts[i_c]]->SetFillColor(kGray);
    h_sum[histos[i_h]][cuts[i_c]]->GetXaxis()->SetTitle(names_histo[i_h]);
    h_sum[histos[i_h]][cuts[i_c]]->GetYaxis()->SetTitle("Events");
    h_sum[histos[i_h]][cuts[i_c]]->Draw("hist");
    l3->AddEntry(h_sum[histos[i_h]][cuts[i_c]],"Background Sum","l");
    for (UInt_t s = nBkgSamples; s < nSamples; s++) {
      //std::cout << "Signal " << samples[s] << " in bin " << i_c << ": " << " " << h_store[samples[s]][histos[i_h]][cuts[i_c]]->Integral() << std::endl;
      h_store[samples[s]][histos[i_h]][cuts[i_c]]->SetLineStyle(2);
      h_store[samples[s]][histos[i_h]][cuts[i_c]]->SetLineWidth(2);
      h_store[samples[s]][histos[i_h]][cuts[i_c]]->SetLineColor(colors[s-nBkgSamples+1]);
  //h_store[samples[s]][histos[i_h]][cuts[i_c]]->Scale(1, "width");
      h_store[samples[s]][histos[i_h]][cuts[i_c]]->Draw("same hist");
      l3->AddEntry( h_store[samples[s]][histos[i_h]][cuts[i_c]],samples[s],"l");
    }
    l3->Draw("same");
    hBkg      [i_c]= (TH1D*)h_sum[histos[i_h]][cuts[i_c]]->Clone(); hBkg[i_c]->Reset();
    hSig      [i_c]= (TH1D*)h_store[samples[nBkgSamples]][histos[i_h]][cuts[i_c]]->Clone(); hSig[i_c]->Reset();
    hBkgNoTJV [i_c]= (TH1D*)hBkg[i_c]->Clone();
    hSigNoTJV [i_c]= (TH1D*)hBkg[i_c]->Clone();
    hSoB      [i_c]= (TH1D*)hBkg[i_c]->Clone();
    hSsB      [i_c]= (TH1D*)hBkg[i_c]->Clone();
    int low_bin = 0;
    int high_bin = hBkg[i_c]->GetNbinsX();
    for (int i = low_bin; i <= high_bin; i++) {
      double n_bkg_i = h_sum[histos[i_h]][cuts[i_c]]->Integral(0,i);
      double n_sig_i = h_store[samples[nBkgSamples]][histos[i_h]][cuts[i_c]]->Integral(0,i);
  //      std::cout << n_bkg_i << " " << n_sig_i << " " << n_sig_i/sqrt(n_bkg_i) << " " << RooStats::NumberCountingUtils::BinomialExpZ(n_sig_i,n_bkg_i,0.0000001) << " " << n_sig_i/n_bkg_i << std::endl;
      hBkg[i_c]->SetBinContent(i,n_bkg_i);
      hSoB[i_c]->SetBinContent(i,n_sig_i/n_bkg_i);
      hSsB[i_c]->SetBinContent(i,n_sig_i/sqrt(n_bkg_i));
      hSig[i_c]->SetBinContent(i,n_sig_i);
      hBkgNoTJV[i_c]->SetBinContent(i,h_sum[histos[i_h]][cuts[i_c]]->Integral(0,high_bin));
      hSigNoTJV[i_c]->SetBinContent(i,h_store[samples[nBkgSamples]][histos[i_h]][cuts[i_c]]->Integral(0,high_bin));
    }
    myCanvas3->SaveAs(outAREA+"/plots/Mjj/bkgsig_"+histos[i_h]+"_"+cuts[i_c]+".pdf");
    //myCanvas3->SaveAs(outAREA+"/plots/Mjj/bkgsig_"+histos[i_h]+".C");
  }
}
// Now the magic with 3rd jet pt
int i_h = 0;
TCanvas *myCanvas4 = new TCanvas("myCanvas4", "",0,0,600,500);
TLegend *l4 = new TLegend(0.72,0.67,0.92,0.91);
for (UInt_t i_c = 0; i_c < N_CUT; i_c++) {
  hSoB[i_c]->SetMaximum(2);
  hSoB[i_c]->SetMinimum(0);
  hSoB[i_c]->SetFillStyle(0);
  hSoB[i_c]->GetXaxis()->SetTitle(names_histo[i_h]);
  hSoB[i_c]->GetYaxis()->SetTitle("S/B");
  hSoB[i_c]->SetLineColor(colors[i_c]); hSoB[i_c]->SetLineWidth(2);
  l4->AddEntry(hSoB[i_c],names_cut[i_c],"l");
  l4->Draw("same");
  if(i_c==0){
    hSoB[i_c]->Draw("AXIS");
    hSoB[i_c]->Draw(" HIST ");
  }else
  hSoB[i_c]->Draw(" HIST SAME");
}
myCanvas4->SaveAs(outAREA+"/plots/Mjj/SoB_"+histos[i_h]+".pdf");
//myCanvas4->SaveAs(outAREA+"/plots/Mjj/SoB_"+histos[i_h]+".C");
TCanvas *myCanvas5 = new TCanvas("myCanvas5", "",0,0,600,500);
TLegend *l5 = new TLegend(0.72,0.67,0.92,0.91);
for (UInt_t i_c = 0; i_c < N_CUT; i_c++) {
  hSsB[i_c]->SetMaximum(25);
  hSsB[i_c]->SetMinimum(0);
  hSsB[i_c]->SetFillStyle(0);
  hSsB[i_c]->GetXaxis()->SetTitle(names_histo[i_h]);
  hSsB[i_c]->GetYaxis()->SetTitle("S/#sqrt{B}");
  hSsB[i_c]->SetLineColor(colors[i_c]); hSsB[i_c]->SetLineWidth(2);
  l5->AddEntry(hSsB[i_c],names_cut[i_c],"l");
  l5->Draw("same");
  if(i_c==0){
    hSsB[i_c]->Draw("AXIS");
    hSsB[i_c]->Draw(" HIST ");
  }else
  hSsB[i_c]->Draw(" HIST SAME");
}
myCanvas5->SaveAs(outAREA+"/plots/Mjj/SsB_"+histos[i_h]+".pdf");
//myCanvas5->SaveAs(outAREA+"/plots/Mjj/SsB_"+histos[i_h]+".C");
*/
}