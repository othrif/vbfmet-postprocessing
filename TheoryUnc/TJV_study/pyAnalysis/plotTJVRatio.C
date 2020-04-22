// Terminology on ratios needed
// Processes:
// Zvv_QCD
// Zll_QCD
// Wlv_QCD

// Process ratios:
// Zvv_QCD/Wlv_QCD
// Zvv_QCD/Zll_QCD

void plotTJVRatio(TString outAREA="./processed"){

  //gSystem->Exec("mkdir -p "+outAREA+"/plots/Mjj");
  gSystem->Exec("mkdir -p "+outAREA+"/plots/Ratio");
  //gSystem->Exec("mkdir -p "+outAREA+"/plots/TJV");

  std::map<TString,TString> processname;
  processname["Zvv_QCD"]="Z #rightarrow #nu#nu QCD";
  processname["Wlv_QCD"]="W #rightarrow l#nu QCD";
  processname["Zll_QCD"]="Z #rightarrow ll QCD";


  TString cuts[]       = {"SRmTJV", "SR25"}; //{"SRmTJV", "SR50", "SR40", "SR35", "SR30", "SR25"};
  TString names_cut[]  = {"No jet veto", "p_{T}^{j3} #leq 25 GeV"}; //, "p_{T}^{j3} #leq 50 GeV", "p_{T}^{j3} #leq 40 GeV", "p_{T}^{j3} #leq 35 GeV", "p_{T}^{j3} #leq 30 GeV", "p_{T}^{j3} #leq 25 GeV"};
  TString histos[] = {"jj_mass"};
  TString names_histo[]  = {"m_{jj} [GeV]"};
  int colors[] = {kRed, kBlue, kViolet, kOrange, kCyan+1, kMagenta-10};

  double maxYratio = 1.1;
  double minYratio = -.1;

  std::map<TString,TH1D*[2]> hProcCut;
  for (auto const& x : processname){
    TString process = x.first;
    std::cout << "Looking at process: " << process << std::endl;
    TString additional ="_2TJV";
    bool ratio = true;
    const char separator    = ' ';
    const int nameWidth     = 20;
    const int numWidth      = 8;

    TFile *f = new TFile(outAREA+"/hists_tjv_extract_"+process+".root");
    TFile *fout= new TFile(outAREA+"/out_"+process+".root","RECREATE");
    TList *list = new TList();

    int histocounter=0;
    for (int i_h = 0; i_h < 1; i_h++) // histograms
    {
     TString name; name.Form("%d",i_h);
     TCanvas *myCanvas = new TCanvas("myCanvas"+name+process, "",0,0,600,500);
     TLegend *l = new TLegend(0.72,0.49,0.92,0.91);
       TPad* p1 = new TPad("p1","p1",0.0,0.33,1.0,1.0,-22);
       TPad* p2 = new TPad("p2","p2",0.0,0.0,1.0,0.33,-21);
       p1->SetBottomMargin(0.02);
       p2->SetTopMargin(0.05);
       p2->SetBottomMargin(0.4);
       if(ratio){
         p1->Draw();
         p2->Draw();
       }
    for (int i_cut=0; i_cut<2; i_cut++) // cuts
    {
      if(ratio)
       p1->cd();
     //p1->SetLogy();
     TString histname = histos[i_h];
     histocounter++;
     TString a = "all/"+cuts[i_cut]+"/";
     TString b = histos[i_h];
     TString h_path = a+b;
     TH1D  *h = (TH1D*)f->Get(h_path);
     if(!h){
       std::cout << "Problem with histogram " << histname << std::endl;
       break;}
       h->SetLineColor(colors[i_cut]); h->SetLineWidth(2);h->SetMarkerColor(colors[i_cut]);
       h->GetXaxis()->SetTitle(names_histo[i_h]);
       h->GetXaxis()->SetLabelOffset(999);
       h->GetYaxis()->SetTitle("Events");
       h->GetYaxis()->SetTitleOffset(0.9);
       h->GetYaxis()->SetTitleSize(0.07);
       h->GetYaxis()->SetLabelSize(0.07);
       h->GetYaxis()->SetTitleFont(42);
       if(i_cut==0){
         h->SetMaximum(h->GetMaximum()*1.5);
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
        if(i_cut==0){
          TH1D* href = (TH1D*)h->Clone(cuts[i_cut]);
          h_Nom = (TH1D*)h->Clone("nom");
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
          href->Draw("AXIS");
          list->Add(href);

          TF1 *line = new TF1("line","1",-100000,100000);
          line->SetLineColor(kBlack);
          line->SetLineWidth(1);
//                line->Draw("same");
          hProcCut[process][i_cut] = (TH1D*) href->Clone();
          hProcCut[process][i_cut]->SetDirectory(0);
        }
        else{
          TH1D* hvar = (TH1D*)h->Clone(cuts[i_cut]);
          hvar->Divide( h_Nom );
          list->Add(hvar);
          hvar->Draw(" HIST SAME");
          hProcCut[process][i_cut] = (TH1D*) hvar->Clone();
          hProcCut[process][i_cut]->SetDirectory(0);
        }
      }
    }
    myCanvas->SaveAs(outAREA+"/plots/Ratio/"+histos[i_h]+"_"+process+additional+".pdf");
    //myCanvas->SaveAs(outAREA+"/plots/Ratio/"+histos[i_h]+"_"+process+additional+".C");
    list->Write("histlist", TObject::kSingleKey);
  }
}

// Process ratios:
// Zvv_QCD/Wlv_QCD
// Zvv_QCD/Zll_QCD
// Zll_QCD/Wlv_QCD

std::map<TString,std::array<string,5>> processratio;
processratio["ratio_Zvv_W_QCD"]=std::array<std::string, 5>{"Zvv_QCD","Wlv_QCD","Z(vv)/W(lv) QCD"  , "0.6", "1.4"};
processratio["ratio_Z_Z_QCD"]=std::array<std::string, 5>{"Zvv_QCD","Zll_QCD","Z(vv)/Z(ll) QCD"  , "0.8", "1.4"};
processratio["ratio_Zll_W_QCD"]=std::array<std::string, 5>{"Zll_QCD","Wlv_QCD","Z(vv)/W(v) QCD"   , "0.8", "1.4"};


int i=0;
for (auto const& x : processratio){
  TString process = x.first;
  TString name; name.Form("%d",i++);
  TCanvas *myCanvas2 = new TCanvas("myCanvas2"+name, "",0,0,600,500);
  TLegend *l2 = new TLegend(0.72,0.61,0.92,0.91);
   for (int i_cut=0; i_cut<2; i_cut++) // cuts
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
  myCanvas2->SaveAs(outAREA+"/plots/Ratio/"+process+".pdf");
    //myCanvas2->SaveAs("./plots/Ratio/"+process+".C");
}


}