{
#include "TFile.h"
#include "TH1F.h"
#include <vector>
#include <iostream>
#include <string>

  //TFile *_file0 = TFile::Open("/tmp/miniT.root");
  TFile *_file0 = TFile::Open("/tmp/miniG.root");
  //TTree *VBFH125Nominal = static_cast<TTree *>(_file0->Get("VBFH125Nominal"));
  TTree *VBFH125Nominal = static_cast<TTree *>(_file0->Get("MiniNtuple"));  
  std::vector<TH1F *> myplots,myplotsdphi;
  // TH1F *hmjj145 = new TH1F("hmjj145","hmjj145",50, 0.0,5000.0);
  float binsjjmass [9] = { 0.0, 200.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0, 3500.0, 5000.0 }; 
  //hjj_mass_variableBin = GetTH1("jj_mass_variableBin",  8,  binsjjmass); 
  //hjj_mass_variableBin = GetTH1("jj_mass_variableBin",  8,  binsjjmass); 
  unsigned offset=0; //0,8,16
  unsigned start = 145;
  bool doggF=true;
  if(doggF){
    start=180;
  }
  string hist_name="";
  string var_name="";  
  string cut_name="";  
  hist_name="hmjjNom";
  TH1F *hnom = new TH1F(hist_name.c_str(),hist_name.c_str(),8,  binsjjmass);
  //TH1F *hnom = new TH1F(hist_name.c_str(),hist_name.c_str(),50, 0.0,5000.0);
  myplots.push_back(hnom);
  var_name="truthF_jj_mass/1.0e3>>hmjjNom";// VBF109, ggf 111
  if(doggF) cut_name="mcEventWeights[111]*(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 &&  n_jet_truth==2  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
  else cut_name="mcEventWeights[109]*(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 &&  n_jet_truth==2  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
  VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());

  TH1F *hdphijjNom = new TH1F("hdphijjNom","hdphijjNom",8, 0.0,2.0);
  var_name="truthF_jj_dphi>>hdphijjNom";// VBF109, ggf 111
  if(doggF) cut_name="mcEventWeights[111]*(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 &&  n_jet_truth==2  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
  else cut_name="mcEventWeights[109]*(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 &&  n_jet_truth==2  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
  VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());
  myplotsdphi.push_back(hdphijjNom);

  //for(unsigned i=start; i<169; ++i){
  //for(unsigned i=(start+offset); i<(154+offset); ++i){
  for(unsigned i=(start+offset); i<(start+8+offset); ++i){
    hist_name="hmjj"+std::to_string(i);
    TH1F *hh = new TH1F(hist_name.c_str(),hist_name.c_str(), 8,  binsjjmass);
    myplots.push_back(hh);
    var_name="truthF_jj_mass/1.0e3>>hmjj"+std::to_string(i);
    cut_name="mcEventWeights["+std::to_string(i)+"]*(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 && n_jet_truth==2 && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
    VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str()) ;

    hist_name="hdphi"+std::to_string(i);
    TH1F *hhd = new TH1F(hist_name.c_str(),hist_name.c_str(),8, 0.0,2.0);
    myplotsdphi.push_back(hhd);
    var_name="truthF_jj_dphi>>hdphi"+std::to_string(i);
    cut_name="mcEventWeights["+std::to_string(i)+"]*(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 && n_jet_truth==2 && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
    VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());
  }

  TLegend *leg = new TLegend(0.2,0.2,0.4,0.4);
  leg->SetBorderSize(0);
  leg->SetFillColor(0);
  std::vector<std::string> lab = {"Nominal","Var3cUp", "Var3cDown", "isr:muRfac=2.0_fsr:muRfac=2.0", "isr:muRfac=2.0_fsr:muRfac=1.0", "isr:muRfac=2.0_fsr:muRfac=0.5",
				  "isr:muRfac=1.0_fsr:muRfac=2.0", "isr:muRfac=1.0_fsr:muRfac=0.5", "isr:muRfac=0.5_fsr:muRfac=2.0", "isr:muRfac=0.5_fsr:muRfac=1.0", "isr:muRfac=0.5_fsr:muRfac=0.5",
				  "isr:muRfac=1.75_fsr:muRfac=1.0","isr:muRfac=1.5_fsr:muRfac=1.0", "isr:muRfac=1.25_fsr:muRfac=1.0","isr:muRfac=0.625_fsr:muRfac=1.0","isr:muRfac=0.75_fsr:muRfac=1.0",
				  "isr:muRfac=0.875_fsr:muRfac=1.0","isr:muRfac=1.0_fsr:muRfac=1.75", "isr:muRfac=1.0_fsr:muRfac=1.5","isr:muRfac=1.0_fsr:muRfac=1.25","isr:muRfac=1.0_fsr:muRfac=0.625",
				  "isr:muRfac=1.0_fsr:muRfac=0.75","isr:muRfac=1.0_fsr:muRfac=0.875","hardHi", "hardLo"};

  TCanvas *can = new TCanvas("can","can",700,500);
  unsigned color=1;
  for(unsigned i=0; i<myplots.size(); ++i){
    myplots.at(i)->GetXaxis()->SetTitle("Truth m_{jj} [GeV]");
    myplots.at(i)->GetYaxis()->SetTitle("Events [arb units]");
    myplots.at(i)->SetLineColor(color);
    ++color;
    if(i==0){ myplots.at(0)->Draw(); leg->AddEntry(myplots.at(0),lab[0].c_str()); }
    else { myplots.at(i)->Draw("same"); leg->AddEntry(myplots.at(i),lab[i+offset].c_str()); }
    
  }
  leg->Draw();
  can->Update();
  //can->WaitPrimitive();
  can->SaveAs("plt3.root");
  can->SaveAs("plt3.pdf");

  for(unsigned i=1; i<myplots.size(); ++i){  

    TH1F *r = static_cast<TH1F *>(myplots.at(i)->Clone());
    r->GetYaxis()->SetTitle("var / Nominal");
    r->Divide(myplots.at(0));
    if(i==1) r->Draw();
    else r->Draw("same");
  }
  leg->Draw();
  can->Update();
  //can->WaitPrimitive();
  can->SaveAs("pltratio3.root");
  can->SaveAs("pltratio3.pdf");
  
  color=1;
  for(unsigned i=0; i<myplotsdphi.size(); ++i){
    myplotsdphi.at(i)->GetXaxis()->SetTitle("Truth #Delta#phi_{jj}");
    myplotsdphi.at(i)->GetYaxis()->SetTitle("Events [arb units]");
    myplotsdphi.at(i)->SetLineColor(color);
    ++color;
    if(i==0) myplotsdphi.at(0)->Draw();
    else myplotsdphi.at(i)->Draw("same");
    //leg->AddEntry(myplotsdphi.at(i),lab[i].c_str());
  }
  leg->Draw();
  can->Update();
  //can->WaitPrimitive();
  can->SaveAs("pltdphi3.root");
  can->SaveAs("pltdphi3.pdf");

  for(unsigned i=1; i<myplotsdphi.size(); ++i){  
    TH1F *r = static_cast<TH1F *>(myplotsdphi.at(i)->Clone());
    r->GetYaxis()->SetTitle("var / Nominal");
    r->Divide(myplotsdphi.at(0));
    if(i==1) r->Draw();
    else r->Draw("same");
  }
  leg->Draw();
  can->Update();
  //can->WaitPrimitive();
  can->SaveAs("pltdphiratio3.root");
  can->SaveAs("pltdphiratio3.pdf");


}/// move to this one: INFO CutBookkeeper CutBookkeepers StreamAOD LHE3Weight_PDFset=90400 Cyc=5 N=500 weight^2=7685.83
// from INFO CutBookkeeper CutBookkeepers StreamAOD LHE3Weight_nominal Cyc=5 N=500 weight^2=7063.31
// if we use the sum of event weights of 90400, then the yields decreases by 8%.
// save this variable LHE3Weight_PDFset=90400



//    "Var3cUp", "Var3cDown"145,146
//    "hardHi", hardLo"167,168
//    "isr:muRfac=2.0_fsr:muRfac=2.0", "isr:muRfac=2.0_fsr:muRfac=1.0", "isr:muRfac=2.0_fsr:muRfac=0.5" 148,149
//    "isr:muRfac=1.0_fsr:muRfac=2.0", "isr:muRfac=1.0_fsr:muRfac=0.5",150,151
//    "isr:muRfac=0.5_fsr:muRfac=2.0", "isr:muRfac=0.5_fsr:muRfac=1.0", "isr:muRfac=0.5_fsr:muRfac=0.5" 152,153
//    "isr:muRfac=1.75_fsr:muRfac=1.0", "isr:muRfac=0.625_fsr:muRfac=1.0" 155,158
//    "isr:muRfac=1.5_fsr:muRfac=1.0", "isr:muRfac=0.75_fsr:muRfac=1.0" 156,159
//    "isr:muRfac=1.25_fsr:muRfac=1.0", "isr:muRfac=0.875_fsr:muRfac=1.0"157,160
//    "isr:muRfac=1.0_fsr:muRfac=1.75", "isr:muRfac=1.0_fsr:muRfac=0.625",161,164
//    "isr:muRfac=1.0_fsr:muRfac=1.5", "isr:muRfac=1.0_fsr:muRfac=0.75"162,165
//    "isr:muRfac=1.0_fsr:muRfac=1.25", "isr:muRfac=1.0_fsr:muRfac=0.875" 163,166
//up to 166, 168 for hardRa
