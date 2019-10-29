{
#include "TFile.h"
#include "TH1F.h"
#include <vector>
#include <iostream>
#include <string>

  //TFile *_file0 = TFile::Open("/tmp/miniT.root");
  //TFile *_file0 = TFile::Open("miniAllggH.root");
  TFile *_file0 = TFile::Open("miniAllVBF.root");
  //TTree *VBFH125Nominal = static_cast<TTree *>(_file0->Get("VBFH125Nominal"));
  TTree *VBFH125Nominal = static_cast<TTree *>(_file0->Get("MiniNtuple"));  
  std::vector<TH1F *> myplots,myplotsdphi,myplotsweight, nomStatErr, systStatErr;
  // TH1F *hmjj145 = new TH1F("hmjj145","hmjj145",50, 0.0,5000.0);
  float binsjjmass [9] = { 0.0, 200.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0, 3500.0, 5000.0 }; 
  std::string binsjjmstr[8] = {"&&(truthF_jj_mass<200e3)", "&&(truthF_jj_mass>200e3 && truthF_jj_mass<500e3)","&&(truthF_jj_mass>500e3 && truthF_jj_mass<800e3)",
			       "&&(truthF_jj_mass>800e3 && truthF_jj_mass<1000e3)","&&(truthF_jj_mass>1000e3 && truthF_jj_mass<1500e3)","&&(truthF_jj_mass>1500e3 && truthF_jj_mass<2000e3)",
			       "&&(truthF_jj_mass>2000e3 && truthF_jj_mass<3500e3)","&&(truthF_jj_mass>3500e3)"};
  for(unsigned hj=0; hj<8;++hj){
    std::string n="mjjV"+std::to_string(hj);
    TH1F *hg = new TH1F(n.c_str(), n.c_str(), 50000, -50.0, 500.0);
    nomStatErr.push_back(hg);
    n="systmjjV"+std::to_string(hj);
    TH1F *hgs = new TH1F(n.c_str(), n.c_str(), 50000, -50.0, 500.0);
    systStatErr.push_back(hgs);
  }
  //hjj_mass_variableBin = GetTH1("jj_mass_variableBin",  8,  binsjjmass); 
  //hjj_mass_variableBin = GetTH1("jj_mass_variableBin",  8,  binsjjmass); 
  unsigned offset=0; //0,8,16
  unsigned start = 145;
  unsigned maxBin=24; // 24 max
  bool doggF=false;
  bool doScale=true;
  if(doScale){
    start=1;
    maxBin=8;
  }
  // nj==2
  //std::string totalCutDef="(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 &&  n_jet_truth==2  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
  //if(doScale) totalCutDef="(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 &&  n_jet_truth>=3  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
  //std::string totalCutDef="(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 &&  n_jet_truth==2  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>2000e3)";
  // nj==3,4
  //exp(-4.0/std::pow(truthF_jj_deta,2) * std::pow(jet_truthjet_eta[2] - (jet_truthjet_eta[0]+jet_truthjet_eta[1])/2.0,2))<0.6
  std::string totalCutDef="(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 && (n_jet_truth==3 || n_jet_truth==3) && (exp(-4.0/std::pow(truthF_jj_deta,2) * std::pow(jet_truthjet_eta[2] - (jet_truthjet_eta[0]+jet_truthjet_eta[1])/2.0,2))<0.6)  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
  if(doScale) totalCutDef="(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 && (n_jet_truth>=4) && (exp(-4.0/std::pow(truthF_jj_deta,2) * std::pow(jet_truthjet_eta[2] - (jet_truthjet_eta[0]+jet_truthjet_eta[1])/2.0,2))<0.6)  && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
  if(doggF){
    start=180;
  }
  string hist_name="";
  string var_name="";
  string cut_name="";
  hist_name="hmjjNom";
  TH1F *hnom = new TH1F(hist_name.c_str(),hist_name.c_str(),8,  binsjjmass);
  TH1F *hband = new TH1F("band","band",8,  binsjjmass);
  //TH1F *hnom = new TH1F(hist_name.c_str(),hist_name.c_str(),50, 0.0,5000.0);
  myplots.push_back(hnom);
  var_name="truthF_jj_mass/1.0e3>>hmjjNom";// VBF109, ggf 111
  if(doggF) cut_name="mcEventWeights[111]*"+totalCutDef;
  else cut_name="mcEventWeights[109]*"+totalCutDef;
  VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());
  // declare for stat unc.
  for(unsigned hj=0; hj<8;++hj){
    std::string n="mjjV"+std::to_string(hj);
    if(doggF) n="mcEventWeights[111]>>mjjV"+std::to_string(hj);
    else n="mcEventWeights[109]>>mjjV"+std::to_string(hj);
    //VBFH125Nominal->Draw(n.c_str(),cut_name.c_str());
  }

  TH1F *hdphijjNom = new TH1F("hdphijjNom","hdphijjNom",8, 0.0,2.0);
  var_name="truthF_jj_dphi>>hdphijjNom";// VBF109, ggf 111
  if(doggF) cut_name="mcEventWeights[111]*"+totalCutDef;
  else cut_name="mcEventWeights[109]*"+totalCutDef;
  VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());
  myplotsdphi.push_back(hdphijjNom);

  TH1F *hWNom = new TH1F("hWNom","hWNom",200, -5.0,5.0);
  var_name="((mcEventWeights[111]-mcEventWeights[109])/mcEventWeights[111])>>hWNom";// VBF109, ggf 111
  if(doggF) cut_name="mcEventWeights[111]*"+totalCutDef;
  else cut_name="mcEventWeights[109]*"+totalCutDef;
  VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());
  myplotsweight.push_back(hWNom);

  //for(unsigned i=start; i<169; ++i){
  //for(unsigned i=(start+offset); i<(154+offset); ++i){
  for(unsigned i=(start+offset); i<(start+maxBin+offset); ++i){
    hist_name="hmjj"+std::to_string(i);
    TH1F *hh = new TH1F(hist_name.c_str(),hist_name.c_str(), 8,  binsjjmass);
    myplots.push_back(hh);
    var_name="truthF_jj_mass/1.0e3>>hmjj"+std::to_string(i);
    cut_name="mcEventWeights["+std::to_string(i)+"]*"+totalCutDef;
    VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str()) ;

    // syst for mjj
    for(unsigned hj=3; hj<8;++hj){
      systStatErr.at(hj)->Reset();
      std::string n="mcEventWeights[109]>>systmjjV"+std::to_string(hj);
      if(doggF)  n="mcEventWeights[111]>>systmjjV"+std::to_string(hj);
      std::string qcuts = cut_name+binsjjmstr[hj];
      VBFH125Nominal->Draw(n.c_str(),qcuts.c_str()) ;
      //float binErr = (nomStatErr.at(hj).GetMean() - systStatErr.at(hj)->GetMean() )/systStatErr.at(hj)->GetMeanError();
      float binErr = fabs(systStatErr.at(hj)->GetMeanError()/( systStatErr.at(hj)->GetMean() ));
      hh->SetBinError(hj+1,binErr*hh->GetBinContent(1+hj));
      std::cout << "Mean error: " << systStatErr.at(hj)->GetMeanError() << " " << systStatErr.at(hj)->GetMean()  << std::endl;
    }

    hist_name="hdphi"+std::to_string(i);
    TH1F *hhd = new TH1F(hist_name.c_str(),hist_name.c_str(),8, 0.0,2.0);
    myplotsdphi.push_back(hhd);
    var_name="truthF_jj_dphi>>hdphi"+std::to_string(i);
    cut_name="mcEventWeights["+std::to_string(i)+"]*"+totalCutDef;
    VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());

    hist_name="hW"+std::to_string(i);
    TH1F *hhw = new TH1F(hist_name.c_str(),hist_name.c_str(),200, -1.0,1.0);
    myplotsweight.push_back(hhw);
    if(doggF) var_name="((mcEventWeights[111]-mcEventWeights["+std::to_string(i)+"])/mcEventWeights[111])>>hW"+std::to_string(i);
    else var_name="((mcEventWeights[109]-mcEventWeights["+std::to_string(i)+"])/mcEventWeights[109])>>hW"+std::to_string(i);
    cut_name=totalCutDef;
    std::cout << "var: " << var_name << std::endl;
    VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());

    hist_name="hWW"+std::to_string(i);
    TH1F *hhww = new TH1F(hist_name.c_str(),hist_name.c_str(),1000, -50.0,300.0);
    var_name="mcEventWeights["+std::to_string(i)+"]>>hWW"+std::to_string(i);
    VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str());
    std::cout << "var: " << i << " mean: " << hhww->GetMean() << " " << hhww->GetMeanError() << " " << hhww->GetRMS() << std::endl;
  }

  TLegend *leg = new TLegend(0.2,0.2,0.4,0.4);
  leg->SetBorderSize(0);
  leg->SetFillColor(0);
  std::vector<std::string> lab = {"Nominal","Var3cUp", "Var3cDown", "isr:muRfac=2.0_fsr:muRfac=2.0", "isr:muRfac=2.0_fsr:muRfac=1.0", "isr:muRfac=2.0_fsr:muRfac=0.5",
				  "isr:muRfac=1.0_fsr:muRfac=2.0", "isr:muRfac=1.0_fsr:muRfac=0.5", "isr:muRfac=0.5_fsr:muRfac=2.0", "isr:muRfac=0.5_fsr:muRfac=1.0", "isr:muRfac=0.5_fsr:muRfac=0.5",
				  "isr:muRfac=1.75_fsr:muRfac=1.0","isr:muRfac=1.5_fsr:muRfac=1.0", "isr:muRfac=1.25_fsr:muRfac=1.0","isr:muRfac=0.625_fsr:muRfac=1.0","isr:muRfac=0.75_fsr:muRfac=1.0",
				  "isr:muRfac=0.875_fsr:muRfac=1.0","isr:muRfac=1.0_fsr:muRfac=1.75", "isr:muRfac=1.0_fsr:muRfac=1.5","isr:muRfac=1.0_fsr:muRfac=1.25","isr:muRfac=1.0_fsr:muRfac=0.625",
				  "isr:muRfac=1.0_fsr:muRfac=0.75","isr:muRfac=1.0_fsr:muRfac=0.875","hardHi", "hardLo"};
  std::vector<std::string> labScale = {"Nominal",
				       " muR = 0.50, muF = 0.50"," muR = 1.00, muF = 0.50",
				       " muR = 2.00, muF = 0.50"," muR = 1.00, muF = 2.00",
				       " muR = 0.50, muF = 2.00"," muR = 2.00, muF = 2.00",
				       " muR = 0.50, muF = 1.00"," muR = 2.00, muF = 1.00"};
  if(doScale) lab=labScale;
  TCanvas *can = new TCanvas("can","can",700,500);
  unsigned color=1;
  for(unsigned i=0; i<myplots.size(); ++i){
    myplots.at(i)->GetXaxis()->SetTitle("Truth m_{jj} [GeV]");
    myplots.at(i)->GetYaxis()->SetTitle("Events [arb units]");
    myplots.at(i)->SetLineColor(color);
    myplots.at(i)->SetMarkerColor(color);
    ++color;
    if(i==0){ myplots.at(0)->Draw(); leg->AddEntry(myplots.at(0),lab[0].c_str()); }
    else { myplots.at(i)->Draw("same"); leg->AddEntry(myplots.at(i),lab[i+offset].c_str()); }
    std::cout << "Var " << i << " " << lab[i+offset] << " with Integral: " << myplots.at(i)->Integral(0,1000) << " ratio: " << (myplots.at(i)->Integral(0,1000)/myplots.at(0)->Integral()) << std::endl;     
  }
  leg->Draw();
  can->Update();
  //can->WaitPrimitive();
  std::string n="plt"+std::to_string(offset)+".root";
  can->SaveAs(n.c_str());
  n="plt"+std::to_string(offset)+".pdf";
  can->SaveAs(n.c_str());

  std::vector<float> minvals = {0,0,0,0,0,0,0,0,0,0,0,0};
  std::vector<float> maxvals = {0,0,0,0,0,0,0,0,0,0,0,0};
  for(unsigned jbins=0; jbins<myplots.at(0)->GetNbinsX()+2; ++jbins){ myplots.at(0)->SetBinError(jbins, 0.0); }
  for(unsigned i=1; i<myplots.size(); ++i){  
    TH1F *r = static_cast<TH1F *>(myplots.at(i)->Clone());
    r->GetYaxis()->SetTitle("var / Nominal");
    r->Divide(myplots.at(0));
    if(i==1) r->Draw();
    else r->Draw("same");
    for(unsigned u=3; u<hband->GetNbinsX()+2; ++u){ 
      //hband->GetBinContent()
      if(i==1){ minvals.at(u)=r->GetBinContent(u); maxvals.at(u)=r->GetBinContent(u); }
      else{
	if(minvals.at(u)> r->GetBinContent(u)) minvals.at(u)=r->GetBinContent(u);
	if(maxvals.at(u)< r->GetBinContent(u)) maxvals.at(u)=r->GetBinContent(u);
      }
    }
  }
  for(unsigned u=3; u<hband->GetNbinsX()+2; ++u){ 
    float avg = (maxvals.at(u)+minvals.at(u))/2.0;
    float avge = (maxvals.at(u)-minvals.at(u))/2.0;
    hband->SetBinContent(u,avg);
    hband->SetBinError(u,avge);
  }
  hband->SetLineColor(1);
  hband->SetMarkerColor(1);
  hband->SetFillColor(1);
  hband->SetMarkerSize(0);
  hband->SetFillStyle(3004);
  hband->Draw("sameE2");

  leg->Draw();
  can->Update();
  //can->WaitPrimitive();
  n="pltratio"+std::to_string(offset)+".root";
  can->SaveAs(n.c_str());
  n="pltratio"+std::to_string(offset)+".pdf";
  can->SaveAs(n.c_str());
  
  color=1;
  for(unsigned i=0; i<myplotsdphi.size(); ++i){
    myplotsdphi.at(i)->GetXaxis()->SetTitle("Truth #Delta#phi_{jj}");
    myplotsdphi.at(i)->GetYaxis()->SetTitle("Events [arb units]");
    myplotsdphi.at(i)->SetLineColor(color);
    myplotsdphi.at(i)->SetMarkerColor(color);
    ++color;
    if(i==0) myplotsdphi.at(0)->Draw();
    else myplotsdphi.at(i)->Draw("same");
    //leg->AddEntry(myplotsdphi.at(i),lab[i].c_str());
  }
  leg->Draw();
  can->Update();
  //can->WaitPrimitive();
  n="pltdphi"+std::to_string(offset)+".root";
  can->SaveAs(n.c_str());
  n="pltdphi"+std::to_string(offset)+".pdf";
  can->SaveAs(n.c_str());

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
  n="pltdphiratio"+std::to_string(offset)+".root";
  can->SaveAs(n.c_str());
  n="pltdphiratio"+std::to_string(offset)+".pdf";
  can->SaveAs(n.c_str());

  color=2;
  for(unsigned i=1; i<myplotsweight.size(); ++i){
    myplotsweight.at(i)->GetXaxis()->SetTitle("[NomW - varW]/NomW");
    myplotsweight.at(i)->GetYaxis()->SetTitle("Events [arb units]");
    myplotsweight.at(i)->SetLineColor(color);
    myplotsweight.at(i)->SetMarkerColor(color);
    ++color;
    if(i==1) myplotsweight.at(1)->Draw();
    else myplotsweight.at(i)->Draw("same");
    //leg->AddEntry(myplotsdphi.at(i),lab[i].c_str());
    std::cout << "Delta Var " << i << " " << lab[i+offset] << " with mean: " << myplotsweight.at(i)->GetMean() << " RMS: " << myplotsweight.at(i)->GetRMS() << " meanerror: "
	      << myplotsweight.at(i)->GetMeanError() << std::endl;
  }
  leg->Draw();
  can->Update();
  //can->WaitPrimitive();
  n="weight"+std::to_string(offset)+".root";
  can->SaveAs(n.c_str());
  n="weight"+std::to_string(offset)+".pdf";
  can->SaveAs(n.c_str());

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

//#ggH
//xrdcp root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/user/schae/fe/d8/user.schae.19126275._000001.MiniNtuple.root /tmp/miniAggH.root
//xrdcp root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/user/schae/ec/40/user.schae.19192039._000001.MiniNtuple.root /tmp/miniDggH.root
//xrdcp root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/user/schae/ae/98/user.schae.19276124._000002.MiniNtuple.root /tmp/miniEggH.root
// hadd miniAllggH.root /tmp/mini*ggH.root &>m1 &
//#VBF
//xrdcp root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/user/schae/b8/e8/user.schae.19224877._000001.MiniNtuple.root /tmp/miniAVBF.root
//xrdcp root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/user/schae/0f/0d/user.schae.19192040._000001.MiniNtuple.root /tmp/miniDVBF.root
//xrdcp root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/user/schae/87/93/user.schae.19126269._000001.MiniNtuple.root /tmp/miniEVBF.root
//hadd miniAllVBF.root /tmp/mini*VBF.root &>test.log &
