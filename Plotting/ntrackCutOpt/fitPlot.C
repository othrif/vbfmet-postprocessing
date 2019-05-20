#include <iostream>
#include <cmath>
#include <string.h>
#include <vector>
#include <stdio.h>
#include <dirent.h> //for directory navigation


#include "TFile.h"
#include "TDirectory.h"
#include "TTreeReader.h"
#include "TTree.h"
#include "TBranch.h"
#include "TF1.h"
#include "TMath.h"
#include "TH2.h"

using namespace std;


string getFileName(string in){
  //convert string to C by copying it char by char so that it is not const
  vector<char> chars(in.begin(), in.end());
  char* str = &chars[0];

  //break path by delim and isolate lowest dir
  int length = strlen(str);
  char delim[]="/";
  char *ptr = strtok(str,delim);
  vector<string> dirs;
 
  while(ptr != NULL){
    dirs.push_back(ptr);
    ptr = strtok(NULL, delim);
  } 

  int endIndex = dirs.size()-1;

  return dirs[endIndex];
}


string getFileID(string in){

  size_t pos = in.find("_JZ");
  in.erase(0,pos+1);
  pos = in.find("W");
  in.erase(pos+1, -1);

  return in;
}


Double_t logFn(Double_t *x, Double_t *par)
{
   //define function in MeV
   Float_t xx =x[0];
   Double_t f = par[0]*TMath::Log10(xx*1000)+par[1];
   return f;
}

Double_t linFn(Double_t *x, Double_t *par)
{
   //define function in MeV
   Float_t xx =x[0];
   Double_t f = par[0]*xx*1000+par[1];
   return f;
}

void saveFnCanvas(string name, TF1* func){

  TCanvas *cann = new TCanvas(name.c_str(),"",600,600);
  func->Draw();
  func->SetLineColor(kRed);
  func->GetYaxis()->SetRangeUser(0,40);

  char outName[1024];
  snprintf(outName,sizeof outName,"%s%s",name.c_str(),".png");
  cann->SaveAs(outName);
}

void saveCanvas(string name, string xlabel, string ylabel, TH2D* hist, TF1* func){

  TCanvas *cann = new TCanvas(name.c_str(),"",600,600);
  hist->Draw("COLZ");
  func->Draw("same");
  func->SetLineColor(kRed);

  char title[1024];
  snprintf(title,sizeof title,"%s%s%s%s%s",name.c_str(),";",xlabel.c_str(),"; ",ylabel.c_str());
  hist->SetTitle(title);
  //cann->Write();
  char outName[1024];
  snprintf(outName,sizeof outName,"%s%s",name.c_str(),"_withFn.png");
  cann->SaveAs(outName);
}

void saveFitCanvas(string name, string xlabel, string ylabel, TH2D* hist, TF1* func){

  TCanvas *cann = new TCanvas(name.c_str(),"",600,600);

  TH1D *histX = hist->ProjectionX();
  histX->Fit(func);
  histX->Draw();
  func->Draw("same");
  func->SetLineColor(kRed);

  char title[1024];
  snprintf(title,sizeof title,"%s%s%s%s%s",name.c_str(),";",xlabel.c_str(),"; ",ylabel.c_str());
  hist->SetTitle(title);
  //cann->Write();
  char outName[1024];
  snprintf(outName,sizeof outName,"%s%s",name.c_str(),"_fit.png");
  cann->SaveAs(outName);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Main 
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void fitPlot(string fileName=""){

  clock_t begin=clock();
  cout<<"Input file: "<<fileName<<endl;


  //detach all histograms from file
  TH1::AddDirectory(kFALSE);
  TH1::SetDefaultSumw2;

  //get histograms out
  TFile *oldfile = TFile::Open(fileName.c_str());

  auto d_plotEvent = oldfile->GetDirectory("plotEvent");
  d_plotEvent->cd();
  TH2D *h_jetNTrackPT_all = (TH2D*)d_plotEvent->Get("jetNTrackPT");
  h_jetNTrackPT_all->SetName("jetNTrackPT_all");
  TH2D *h_jetNTrackPTq_all = (TH2D*)d_plotEvent->Get("jetNTrackPTq");
  h_jetNTrackPTq_all->SetName("jetNTrackPTq_all");
  TH2D *h_jetNTrackPTg_all = (TH2D*)d_plotEvent->Get("jetNTrackPTg");
  h_jetNTrackPTg_all->SetName("jetNTrackPTg_all");

  auto d_sr  = oldfile->GetDirectory("pass_sr_allmjj_nn_Nominal");
  d_sr->cd();

  auto d_higgs = d_sr->GetDirectory("plotEvent_higgs");
  TH2D *h_jetNTrackPT_higgs = (TH2D*)d_higgs->Get("jetNTrackPT");
  h_jetNTrackPT_higgs->SetName("jetNTrackPT_higgs");
  TH2D *h_jetNTrackPTq_higgs = (TH2D*)d_higgs->Get("jetNTrackPTq");
  h_jetNTrackPTq_higgs->SetName("jetNTrackPTq_higgs");
  TH2D *h_jetNTrackPTg_higgs = (TH2D*)d_higgs->Get("jetNTrackPTg");
  h_jetNTrackPTg_higgs->SetName("jetNTrackPTg_higgs");

  auto d_bkgs = d_sr->GetDirectory("plotEvent_bkgs");
  TH2D *h_jetNTrackPT_bkgs = (TH2D*)d_bkgs->Get("jetNTrackPT");
  h_jetNTrackPT_bkgs->SetName("jetNTrackPT_bkgs");
  TH2D *h_jetNTrackPTq_bkgs = (TH2D*)d_bkgs->Get("jetNTrackPTq");
  h_jetNTrackPTq_bkgs->SetName("jetNTrackPTq_bkgs");
  TH2D *h_jetNTrackPTg_bkgs = (TH2D*)d_bkgs->Get("jetNTrackPTg");
  h_jetNTrackPTg_bkgs->SetName("jetNTrackPTg_bkgs");

  oldfile->Close();


  //Create output file and directory structure
  char newfileName[1024];
  size_t pos = fileName.find(".root");
  fileName.erase(pos, -1);
  snprintf(newfileName,sizeof newfileName,"%s%s",fileName.c_str(),"_NTrackPTFit.root");
  cout <<"output file: "<<newfileName<<"\n"<<endl;
  TFile *newfile = new TFile(newfileName,"recreate");
  TDirectory *d_rawHistograms = newfile->mkdir("rawHistograms");

  d_rawHistograms->cd();
  h_jetNTrackPT_all->Write();
  h_jetNTrackPT_higgs->Write();
  h_jetNTrackPT_bkgs->Write();
  h_jetNTrackPTq_all->Write();
  h_jetNTrackPTq_higgs->Write();
  h_jetNTrackPTq_bkgs->Write();
  h_jetNTrackPTg_all->Write();
  h_jetNTrackPTg_higgs->Write();
  h_jetNTrackPTg_bkgs->Write();

  //define default (log) fit function
  TF1 *f_defaultLog = new TF1("defaultLog",logFn,0,500,2);
  f_defaultLog->SetNpx(1000);
  f_defaultLog->SetParameters(9.779,-32.28);
  f_defaultLog->SetParNames("slope","intercept");
  saveFnCanvas("defaultLog",f_defaultLog);
  
  vector<TF1*> testLogFns;
  int count=-1;
  for(double slope=6; slope<13;++slope){   
    for(double interc=-20; interc>-50; interc-=5){
	//cout<<"s, i "<<slope<<interc<<"\n"<<endl;
	++count;
	char name[1024];
	char countChar[128];
	sprintf(countChar,"%d",count);
	snprintf(name,sizeof name,"%s%s","testLog",countChar);
	TF1 *f_testLog = new TF1(name,logFn,0,500,2);
	f_testLog->SetParameters(slope,interc);
	testLogFns.push_back(f_testLog);
	saveFnCanvas(name,f_testLog);
    }
  }

  //add log function from Natasha
  TF1 *f_logNat = new TF1("logNat",logFn,0,500,2);
  f_logNat->SetParameters(4,-5);
  testLogFns.push_back(f_logNat);

  vector<int> goodLogFns;
  goodLogFns.push_back(0);
  goodLogFns.push_back(6);
  goodLogFns.push_back(7);
  goodLogFns.push_back(13);
  goodLogFns.push_back(14);
  goodLogFns.push_back(20);
  goodLogFns.push_back(21);
  goodLogFns.push_back(27);
  goodLogFns.push_back(34);
  goodLogFns.push_back(35);
  goodLogFns.push_back(41);
  goodLogFns.push_back(42); //logNat

  for (auto i = 0; i<goodLogFns.size(); ++i){
    char name[1024];
    char nameq[1024];
    char nameg[1024];
    char fn[128];
    int index=goodLogFns[i];
    sprintf(fn,"%d",index);
    sprintf(name, "%s%s","jetNTrackPT_all_log",fn);
    sprintf(nameq, "%s%s","jetNTrackPTq_all_log",fn);
    sprintf(nameg, "%s%s","jetNTrackPTg_all_log",fn);
    saveCanvas(name,"p_T","NTracks",h_jetNTrackPT_all,testLogFns[index]);
    saveCanvas(nameq,"p_T","NTracks",h_jetNTrackPTq_all,testLogFns[index]);
    saveCanvas(nameg,"p_T","NTracks",h_jetNTrackPTg_all,testLogFns[index]);
  }

  vector<TF1*> testLinFns;
  count=-1;
  for(double slope=0.00006; slope<0.00013;slope+=0.00001){   
    for(double interc=-20; interc<10; interc+=5){
	//cout<<"s, i "<<slope<<interc<<"\n"<<endl;
	++count;
	char name[1024];
	char countChar[128];
	sprintf(countChar,"%d",count);
	snprintf(name,sizeof name,"%s%s","testLin",countChar);
	TF1 *f_testLin = new TF1(name,linFn,0,500,2);
	f_testLin->SetParameters(slope,interc);
	testLinFns.push_back(f_testLin);
	saveFnCanvas(name,f_testLin);
    }
  }

  vector<int> goodLinFns;
  goodLinFns.push_back(4);
  goodLinFns.push_back(5);
  goodLinFns.push_back(10);
  goodLinFns.push_back(11);
  goodLinFns.push_back(16);
  goodLinFns.push_back(17);
  goodLinFns.push_back(22);
  goodLinFns.push_back(23);
  goodLinFns.push_back(28);
  goodLinFns.push_back(29);
  goodLinFns.push_back(34);
  goodLinFns.push_back(35);
  goodLinFns.push_back(40);
  goodLinFns.push_back(41);

  for (auto i = 0; i<goodLinFns.size(); ++i){
    char name[1024];
    char nameq[1024];
    char nameg[1024];
    char fn[128];
    int index=goodLinFns[i];
    sprintf(fn,"%d",index);
    sprintf(name, "%s%s","jetNTrackPT_all_lin",fn);
    sprintf(nameq, "%s%s","jetNTrackPTq_all_lin",fn);
    sprintf(nameg, "%s%s","jetNTrackPTg_all_lin",fn);
    saveCanvas(name,"p_T","NTracks",h_jetNTrackPT_all,testLinFns[index]);
    saveCanvas(nameq,"p_T","NTracks",h_jetNTrackPTq_all,testLinFns[index]);
    saveCanvas(nameg,"p_T","NTracks",h_jetNTrackPTg_all,testLinFns[index]);
  }

  gFile->cd();
  saveCanvas("jetNTrackPT_all_defaultLog","p_T","NTracks",h_jetNTrackPT_all,f_defaultLog);
  saveCanvas("jetNTrackPT_higgs_defaultLog","p_T","NTracks",h_jetNTrackPT_higgs,f_defaultLog);
  saveCanvas("jetNTrackPT_bkgs_defaultLog","p_T","NTracks",h_jetNTrackPT_bkgs,f_defaultLog);
  saveCanvas("jetNTrackPTq_all_defaultLog","p_T","NTracks",h_jetNTrackPTq_all,f_defaultLog);
  saveCanvas("jetNTrackPTq_higgs_defaultLog","p_T","NTracks",h_jetNTrackPTq_higgs,f_defaultLog);
  saveCanvas("jetNTrackPTq_bkgs_defaultLog","p_T","NTracks",h_jetNTrackPTq_bkgs,f_defaultLog);
  saveCanvas("jetNTrackPTg_all_defaultLog","p_T","NTracks",h_jetNTrackPTg_all,f_defaultLog);
  saveCanvas("jetNTrackPTg_higgs_defaultLog","p_T","NTracks",h_jetNTrackPTg_higgs,f_defaultLog);
  saveCanvas("jetNTrackPTg_bkgs_defaultLog","p_T","NTracks",h_jetNTrackPTg_bkgs,f_defaultLog);
  
  saveFitCanvas("jetNTrackPT_all_defaultLog_fit","p_T","NTracks",h_jetNTrackPT_all,f_defaultLog);

  delete newfile;


  clock_t end = clock();
  double execTime=(double)(end-begin)/CLOCKS_PER_SEC;
  cout<<"Execution time: "<<execTime<<"s"<<endl;

}


int main(int argc, char** argv) {
  fitPlot(argv[1]);
  return 0;
}
