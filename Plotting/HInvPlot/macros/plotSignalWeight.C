{
  TFile *_file0 = TFile::Open("/tmp/VBFH125Nominal346600.root");
  TTree *VBFH125Nominal = static_cast<TTree *>(_file0->Get("VBFH125Nominal"));
  //TTree *VBFH125Nominal = static_cast<TTree *>(_file0->Get("MiniNtuple"));  
  std::vector<TH1F *> myplots;
  // TH1F *hmjj145 = new TH1F("hmjj145","hmjj145",50, 0.0,5000.0);

  string hist_name="";
  string var_name="";  
  string cut_name="";  
  //for(unsigned i=145; i<169; ++i){
  for(unsigned i=145; i<150; ++i){
    hist_name="hmjj"+std::to_string(i);
    TH1F *hh = new TH1F(hist_name.c_str(),hist_name.c_str(),50, 0.0,5000.0);
    myplots.push_back(hh);
    var_name="truthF_jj_mass/1.0e3>>hmjj"+std::to_string(i);
    cut_name="mcEventWeights["+std::to_string(i)+"]*(met_truth_et>150.0e3 && jet_truthjet_pt[0]>80.0e3 && jet_truthjet_pt[1]>50.0e3 && n_jet<4 && truthF_jj_deta>3.8 && truthF_jj_dphi<2 && truthF_jj_mass>800e3)";
      //MiniNtuple->Draw(var_name.c_str(),cut_name.c_str()) ;
      VBFH125Nominal->Draw(var_name.c_str(),cut_name.c_str()) ;
  }

  myplots.at(1)->SetLineColor(2);
  myplots.at(2)->SetLineColor(3);
  myplots.at(3)->SetLineColor(4);
  myplots.at(0)->Draw();
  myplots.at(1)->Draw("same");
  myplots.at(2)->Draw("same");
  myplots.at(3)->Draw("same");    

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
