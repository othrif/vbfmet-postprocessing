// HFInput includes
#include "HFInputAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
#include "TLorentzVector.h"
#include "TFile.h"
#include <math.h>

HFInputAlg::HFInputAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){
  declareProperty("currentVariation", currentVariation = "Nominal", "current systematics, NONE means nominal");
  declareProperty("currentSample", currentSample = "W_strong", "current samples");
  declareProperty("isMC", isMC = true, "isMC flag, true means the sample is MC");
  declareProperty("year", year = 2016, "year, 2017 and 2018 to set the lumi");
  declareProperty("isMadgraph", isMadgraph = false, "isMadgraph flag, true means the sample is Madgraph");
  declareProperty("mergeKTPTV", mergeKTPTV = false, "mergeKTPTV flag, true means merge kT Sherpa samples");
  declareProperty("ExtraVars", m_extraVars = 7, "0=20.7 analysis, 1=lepton veto, object def, 2=loose cuts, 3=no met soft cut, 4=no xe SF for muons, 5=lepTrigOnly for muCR, 6=met trig only for muCR, 7=metORLep for muCR (default)" );
  declareProperty("Binning", m_binning = 11, "0=rel20p7 binning. Other options with >0, 11 is default" );
  declareProperty("METDef", m_metdef = 0, "0=loose. 1=tenacious" );
  declareProperty("METCut", m_METCut = -1, "METCut forced overwrite" );
  declareProperty("singleHist", singleHist = false, "singleHist flag, true for running one histogram with bins for the SRs and CRs");
  declareProperty("isHigh", isHigh = true, "isHigh flag, true for upward systematics");
  declareProperty("doLowNom", doLowNom = false, "isMC flag, true means the sample is MC");
  declareProperty("doTMVA", doTMVA = false, "doTMVA flag, true means use the MVA");
  declareProperty("doDoubleRatio", doDoubleRatio = false, "doDoubleRatio flag, true means use the doDoubleRatio method");
  declareProperty("doHighDphijj", doHighDphijj = false, "doHighDphijj flag, true means use the doHighDphijj region");  
  declareProperty("weightSyst", weightSyst = false, "weightSyst flag, true for weight systematics");
  declareProperty("doPlot", doPlot =false, "doPlot flag, true means the output contains variable distributions");
  declareProperty("doVBFMETGam", doVBFMETGam =false, "doVBFMETGam flag, true means run the VBF+MET+photon analysis");
  declareProperty("doMTFit", doMTFit =false, "doMTFit flag, true means run the VBF+MET+photon analysis with an MT fit");  
  declareProperty("v26Ntuples", v26Ntuples = false, "v26Ntuples flag, true means the setting for backward compatibility with v26 ntuples");
  declareProperty("doDuplicateCheck", doDuplicateCheck =false, "doDuplicateCheck flag, true means the run and event numbers are printed");
  //declareProperty( "Property", m_nProperty = 0, "My Example Integer Property" ); //example property declaration
}


HFInputAlg::~HFInputAlg() {}

bool HFInputAlg::replace(std::string& str, const std::string& from, const std::string& to) {
  size_t start_pos = str.find(from);
  if(start_pos == std::string::npos)
    return false;
  str.replace(start_pos, from.length(), to);
  return true;
}

StatusCode HFInputAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");
  //
  //This is called once, before the start of the event loop
  //Retrieves of tools you have configured in the joboptions go here
  //
  mu_charge= new std::vector<int>(0);
  basemu_charge= new std::vector<int>(0);
  mu_pt= new std::vector<float>(0);
  mu_phi= new std::vector<float>(0);
  mu_eta= new std::vector<float>(0);
  el_charge= new std::vector<int>(0);
  baseel_charge= new std::vector<int>(0);
  el_pt= new std::vector<float>(0);
  el_phi= new std::vector<float>(0);
  el_eta= new std::vector<float>(0);
  ph_pt= new std::vector<float>(0);
  ph_phi= new std::vector<float>(0);
  ph_eta= new std::vector<float>(0);
  jet_pt= new std::vector<float>(0);
  jet_phi= new std::vector<float>(0);
  jet_eta= new std::vector<float>(0);
  jet_m= new std::vector<float>(0);
  jet_timing= new std::vector<float>(0); 
  jet_passJvt= new std::vector<int>(0); 
  jet_fjvt= new std::vector<float>(0);
  jet_NTracks = new std::vector<unsigned short>(0);
  baseel_pt= new std::vector<float>(0);
  baseel_eta= new std::vector<float>(0);
  baseel_phi= new std::vector<float>(0);
  basemu_pt= new std::vector<float>(0);
  basemu_eta= new std::vector<float>(0);
  basemu_phi= new std::vector<float>(0);
  lep_trig_match=1; // init to 1 for older ntuples
  
  cout<<"NAME of input tree in intialize ======="<<currentVariation<<endl;
  if (currentSample == "data") isMC = false;
  cout<< "CURRENT  sample === "<< currentSample<<endl;
  std::cout << "Running Extra Veto? " << m_extraVars << std::endl;
  std::cout << "is a weightSyst? " << weightSyst << std::endl;
  std::cout << "binning? " << m_binning << std::endl;

  std::string syst;
  bool replacedHigh = false;
  bool replacedLow = false;
  if (isMC) {
    syst=currentVariation;
    cout << "CURRENT syst === " << syst << endl;
    if (syst != "Nominal") {
      replacedHigh = replace(syst, "__1up", "High");
      replacedLow = replace(syst, "__1down", "Low");
      if (doLowNom){
	if (replacedHigh) replace(syst, "High", "Low"); else syst.append("Low");
      } else{
	if (isHigh && !replacedHigh) replacedHigh = replace(syst, "Up", "High");
	if (isHigh && !replacedHigh) syst.append("High");
	if (!isHigh && !replacedLow) replacedLow = replace(syst, "Down", "Low");
	if (!isHigh && !replacedLow) syst.append("Low");
      }
    } else {
      syst = "Nom";
    }
  }
  int bins = 4;
  if(m_binning==1)       bins=5; 
  else if(m_binning==-1) bins=7; // first pass of the qgtagging 
  else if(m_binning==2)  bins=5;
  else if(m_binning==3)  bins=7; // mjj binning
  else if(m_binning==4)  bins=7; // mjj binning
  else if(m_binning==5)  bins=7; // mjj binning
  else if(m_binning==6)  bins=8; // mjj binning + njet bin
  else if(m_binning==7)  bins=10; // mjj binning + njet bin + dphijj by 2 mjj>800
  else if(m_binning==8)  bins=10; // mjj binning + mjj>800 + njet bin
  else if(m_binning==9)  bins=9; // mjj binning + mjj>800 + No njet bin
  else if(m_binning==10) bins=12; // mjj binning + njet bin + dphijj by 2 mjj>800
  else if(m_binning==11) bins=12; // mjj binning + njet bin + dphijj by 2 mjj>800
  else if(m_binning==12) bins=12; // mjj binning + njet bin + dphijj by 2 mjj>800
  else if(m_binning==13) bins=5; // mjj binning mjj>250
  else if(m_binning==21) bins=14; // trying new njet binning. mjj binning + 3 njet bin + dphijj by 2 mjj>800
  else if(m_binning==22) bins=17; // trying new njet binning. mjj binning + 3 njet bin + dphijj by 2 mjj>800 + 3 bins low MET
  else if(m_binning==23) bins=12; // trying new njet binning. mjj binning + 3 njet bin + 3 bins low MET

  // multivariate number of bins
  if(doTMVA &&  doVBFMETGam) bins=5;
  if(doTMVA && !doVBFMETGam){
    //if(m_binning==11) bins=7;
    bins=12;
  }
  totalBins = bins-1;

  // merging the sherpa kt samples
  std::string currentSamplePlot = currentSample;
  if(mergeKTPTV && currentSample=="Z_strongExt") currentSamplePlot = "Z_strong";
  if(mergeKTPTV && currentSample=="W_strongExt") currentSamplePlot = "W_strong";
  if(year==2018 && currentSample=="Z_strongPTVExt") currentSamplePlot = "Z_strong";

  if(!singleHist){
    for (int c=1;c<bins;c++) {
      hSR.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("SR"+to_string(c)),to_string(c), syst, isMC), string("SR"+to_string(c))));
      hCRWe.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneEleCR"+to_string(c)),to_string(c), syst, isMC), string("oneEleCR"+to_string(c))));
      //hCRWep.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC), string("oneElePosCR"+to_string(c))));
      //hCRWen.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC), string("oneEleNegCR"+to_string(c))));
      hCRWeLowSig.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneEleLowSigCR"+to_string(c)),to_string(c), syst, isMC), string("oneEleLowSigCR"+to_string(c))));
      //hCRWepLowSig.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC), string("oneElePosLowSigCR"+to_string(c))));
      //hCRWenLowSig.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC), string("oneEleNegLowSigCR"+to_string(c))));
      hCRWm.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneMuCR"+to_string(c)),to_string(c), syst, isMC), string("oneMuCR"+to_string(c))));
      hCRWmMT.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneMuMTCR"+to_string(c)),to_string(c), syst, isMC), string("oneMuMTCR"+to_string(c))));
      //hCRWmp.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC), string("oneMuPosCR"+to_string(c))));
      //hCRWmn.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC), string("oneMuNegCR"+to_string(c))));
      hCRFJVT.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("FJVTCR"+to_string(c)),to_string(c), syst, isMC), string("FJVTCR"+to_string(c))));
      hCRZll.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("twoLepCR"+to_string(c)),to_string(c), syst, isMC), string("twoLepCR"+to_string(c))));
      //hCRZee.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC), string("twoEleCR"+to_string(c))));
      hCRZmm.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC), string("twoMuCR"+to_string(c))));
      vector <std::pair<vector <TH1F*>, std::string>> hnames;
      hnames.push_back(std::make_pair(hSR.back(),HistoNameMaker(currentSamplePlot,string("SR"+to_string(c)),to_string(c), syst, isMC)));
      hnames.push_back(std::make_pair(hCRWe.back(), HistoNameMaker(currentSamplePlot,string("oneEleCR"+to_string(c)),to_string(c), syst, isMC)));
      //hnames.push_back(std::make_pair(hCRWep.back(), HistoNameMaker(currentSamplePlot,string("oneElePosCR"+to_string(c)),to_string(c), syst, isMC)));
      //hnames.push_back(std::make_pair(hCRWen.back(), HistoNameMaker(currentSamplePlot,string("oneEleNegCR"+to_string(c)),to_string(c), syst, isMC)));
      hnames.push_back(std::make_pair(hCRWeLowSig.back(), HistoNameMaker(currentSamplePlot,string("oneEleLowSigCR"+to_string(c)),to_string(c), syst, isMC)));
      //hnames.push_back(std::make_pair(hCRWepLowSig.back(), HistoNameMaker(currentSamplePlot,string("oneElePosLowSigCR"+to_string(c)),to_string(c), syst, isMC)));
      //hnames.push_back(std::make_pair(hCRWenLowSig.back(), HistoNameMaker(currentSamplePlot,string("oneEleNegLowSigCR"+to_string(c)),to_string(c), syst, isMC)));
      hnames.push_back(std::make_pair(hCRWm.back(), HistoNameMaker(currentSamplePlot,string("oneMuCR"+to_string(c)),to_string(c), syst, isMC)));
      hnames.push_back(std::make_pair(hCRWmMT.back(), HistoNameMaker(currentSamplePlot,string("oneMuMTCR"+to_string(c)),to_string(c), syst, isMC)));
      //hnames.push_back(std::make_pair(hCRWmp.back(), HistoNameMaker(currentSamplePlot,string("oneMuPosCR"+to_string(c)),to_string(c), syst, isMC)));
      //hnames.push_back(std::make_pair(hCRWmn.back(), HistoNameMaker(currentSamplePlot,string("oneMuNegCR"+to_string(c)),to_string(c), syst, isMC)));
      hnames.push_back(std::make_pair(hCRZll.back(), HistoNameMaker(currentSamplePlot,string("twoLepCR"+to_string(c)),to_string(c), syst, isMC)));
      hnames.push_back(std::make_pair(hCRFJVT.back(), HistoNameMaker(currentSamplePlot,string("FJVTCR"+to_string(c)),to_string(c), syst, isMC)));
      //hnames.push_back(std::make_pair(hCRZee.back(), HistoNameMaker(currentSamplePlot,string("twoEleCR"+to_string(c)),to_string(c), syst, isMC)));
      //hnames.push_back(std::make_pair(hCRZmm.back(), HistoNameMaker(currentSamplePlot,string("twoMuCR"+to_string(c)),to_string(c), syst, isMC)));
      CheckHists(hnames);
    }
    // Adding the ACR for double ratio for 500-800/1000GeV
    if(doDoubleRatio){
      std::string binNameDR="DoubleRatio";
      hSR.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("AVBFCR1"),binNameDR, syst, isMC), string("AVBFCR")));
      hCRWep.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneElePosACR1"),binNameDR, syst, isMC), string("oneElePosACR")));
      hCRWen.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneEleNegACR1"),binNameDR, syst, isMC), string("oneEleNegACR")));
      hCRWepLowSig.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneElePosLowSigACR1"),binNameDR, syst, isMC), string("oneElePosLowSigACR")));
      hCRWenLowSig.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneEleNegLowSigACR1"),binNameDR, syst, isMC), string("oneEleNegLowSigACR")));
      hCRWmp.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneMuPosACR1"),binNameDR, syst, isMC), string("oneMuPosACR")));
      hCRWmn.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("oneMuNegACR1"),binNameDR, syst, isMC), string("oneMuNegACR")));
      hCRZee.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("twoEleACR1"),binNameDR, syst, isMC), string("twoEleACR")));
      hCRZmm.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("twoMuACR1"),binNameDR, syst, isMC), string("twoMuACR")));
      vector <std::pair<vector <TH1F*>, std::string>> hnames;
      hnames.push_back(std::make_pair(hSR.back(),HistoNameMaker(currentSamplePlot,string("AVBFCR1"),binNameDR, syst, isMC)));
      hnames.push_back(std::make_pair(hCRWep.back(), HistoNameMaker(currentSamplePlot,string("oneElePosACR1"),binNameDR, syst, isMC)));
      hnames.push_back(std::make_pair(hCRWen.back(), HistoNameMaker(currentSamplePlot,string("oneEleNegACR1"),binNameDR, syst, isMC)));
      hnames.push_back(std::make_pair(hCRWepLowSig.back(), HistoNameMaker(currentSamplePlot,string("oneElePosLowSigACR1"),binNameDR, syst, isMC)));
      hnames.push_back(std::make_pair(hCRWenLowSig.back(), HistoNameMaker(currentSamplePlot,string("oneEleNegLowSigACR1"),binNameDR, syst, isMC)));
      hnames.push_back(std::make_pair(hCRWmp.back(), HistoNameMaker(currentSamplePlot,string("oneMuPosACR1"),binNameDR, syst, isMC)));
      hnames.push_back(std::make_pair(hCRWmn.back(), HistoNameMaker(currentSamplePlot,string("oneMuNegACR1"),binNameDR, syst, isMC)));
      hnames.push_back(std::make_pair(hCRZee.back(), HistoNameMaker(currentSamplePlot,string("twoEleACR1"),binNameDR, syst, isMC)));
      hnames.push_back(std::make_pair(hCRZmm.back(), HistoNameMaker(currentSamplePlot,string("twoMuACR1"),binNameDR, syst, isMC)));
      CheckHists(hnames);
    }
  }else{//one histogram in SR
    int c=1;
    hSR.push_back(HistoAppend(HistoNameMaker(currentSamplePlot,string("SR"+to_string(c)),to_string(c), syst, isMC), string("SR"+to_string(c)), totalBins));
    vector <std::pair<vector <TH1F*>, std::string>> hnames;
    hnames.push_back(std::make_pair(hSR.back(),HistoNameMaker(currentSamplePlot,string("SR"+to_string(c)),to_string(c), syst, isMC)));
    CheckHists(hnames);
  }

  return StatusCode::SUCCESS;
}

std::string HFInputAlg::HistoNameMaker(std::string currentSample, std::string currentCR, std::string bin, std::string syst, Bool_t isMC) {
  // merging the sherpa kt samples
  std::string currentSamplePlot = currentSample;
  if(mergeKTPTV && currentSample=="Z_strongExt") currentSamplePlot = "Z_strong";
  if(mergeKTPTV && currentSample=="W_strongExt") currentSamplePlot = "W_strong";
  if(year==2018 && currentSample=="Z_strongPTVExt") currentSamplePlot = "Z_strong";
  if (isMC) {
    if (bin == "") return "h"+currentSamplePlot+ "_"+syst+"_"+currentCR + "_obs";
    else if (bin == "DoubleRatio") return "h"+currentSamplePlot+ "_antiVBFSel_1"+syst+"_"+currentCR + "_obs";
    else if (currentSamplePlot.find("signal") != std::string::npos) return "h"+currentSamplePlot+syst+"_"+currentCR + "_obs";
    else return "h"+currentSamplePlot+ "_VBFjetSel_"+bin+syst+"_"+currentCR + "_obs";
  } else {
    return "h"+currentSamplePlot+ "_NONE_"+currentCR + "_obs";
  }
}

vector <TH1F*> HFInputAlg::HistoAppend(std::string name, std::string currentCR, int bins) {
  vector <TH1F*> h;
  if(!singleHist){
    h.push_back(new TH1F((name+"_cuts").c_str(), (name+"_cuts;;").c_str(), 1, 0.5, 1.5));
    if (!doPlot && doMTFit) {
      float binsmt [6] = { 0.0, 90.0, 130.0, 200.0, 300.0, 500.0 };
      h.push_back(new TH1F((name+"_mtgam").c_str(), (name+"_mtgam;;").c_str(), 5,  binsmt));
    } else if (doPlot) {
      //h.push_back(new TH1F((name+"_jj_mass").c_str(), (name+"_jj_mass;;").c_str(), 10, 0, 5000));
      if(doVBFMETGam){
	float binsjjmass [6] = { 0.0, 250.0, 500.0, 1000.0, 1500.0, 3000.0 };
	h.push_back(new TH1F((name+"_jj_mass").c_str(), (name+"_jj_mass;;").c_str(), 5,  binsjjmass));
      }else{
	float binsjjmass [12] = { 0.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 3500.0, 4000.0, 4500.0, 5000.0 };
	h.push_back(new TH1F((name+"_jj_mass").c_str(), (name+"_jj_mass;;").c_str(), 11,  binsjjmass));
      }
      h.push_back(new TH1F((name+"_jj_dphi").c_str(), (name+"_jj_dphi;;").c_str(), 6, 0, 3.0));
      h.push_back(new TH1F((name+"_met_et").c_str(), (name+"_met_et;;").c_str(), 10, 0, 800));
      h.push_back(new TH1F((name+"_lepmet_et").c_str(), (name+"_lepmet_et;;").c_str(), 10, 0, 800));
      if(doTMVA) h.push_back(new TH1F((name+"_tmva").c_str(), (name+"_tmva;;").c_str(), 2000, 0, 1.0));
      if(doMTFit){
	float binsmt [6] = { 0.0, 90.0, 130.0, 200.0, 300.0, 500.0 };
	h.push_back(new TH1F((name+"_mtgam").c_str(), (name+"_mtgam;;").c_str(), 5,  binsmt));
      }
    }
  }else{
    float maxBin = bins*9.0+0.5;
    int totBins = bins*9;
    h.push_back(new TH1F((name+"_cuts").c_str(), (name+"_cuts;;").c_str(), totBins, 0.5, maxBin));
  }
  return h;
}

StatusCode HFInputAlg::CheckHists(vector <std::pair<vector <TH1F*>, std::string>> hnames){
  for (auto hname : hnames) {
    CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_cuts", std::get<0>(hname)[0]));
    if(!doPlot && doMTFit) CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_mtgam", std::get<0>(hname)[1]));
    if (doPlot) {
      CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_jj_mass", std::get<0>(hname)[1]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_jj_dphi", std::get<0>(hname)[2]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_met_et", std::get<0>(hname)[3]));
      CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_lepmet_et", std::get<0>(hname)[4]));
      if(doTMVA){
	CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_tmva", std::get<0>(hname)[5]));
	if(doMTFit) CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_mtgam", std::get<0>(hname)[6]));
      }else if(doMTFit) CHECK(histSvc()->regHist("/MYSTREAM/"+std::get<1>(hname)+"_mtgam", std::get<0>(hname)[5]));
    }
  }
  return StatusCode::SUCCESS;
}


StatusCode HFInputAlg::finalize() {
  ATH_MSG_INFO ("Finalizing " << name() << "...");

  // write out the overlap trees
  for(std::map<unsigned, TTree *>::iterator treeIter = m_signalOverlapTreeMap.begin(); treeIter != m_signalOverlapTreeMap.end(); ++treeIter){
    m_signalOverlapFileMap[treeIter->first]->cd();
    treeIter->second->Write();
    m_signalOverlapFileMap[treeIter->first]->Close();
  }

  return StatusCode::SUCCESS;
}

StatusCode HFInputAlg::execute() {  
  ATH_MSG_DEBUG ("Executing " << name() << "...");
  setFilterPassed(false); //optional: start with algorithm not passed

  npevents++;
  if( (npevents%10000) ==0) std::cout <<" Processed "<< npevents << " Events"<<std::endl;
  bool SR = false;
  bool CRWep = false;
  bool CRWen = false;
  bool CRWepLowSig = false;
  bool CRWenLowSig = false;
  bool CRWmp = false;
  bool CRWmn = false;
  bool CRZee = false;
  bool CRZmm = false;
  bool CRFJVT = false;

  m_tree->GetEntry(m_tree->GetReadEntry());
  // check if we need to output the physics tree for signal overlap
  if(isMC && (runNumber==308276 || runNumber==346588 || runNumber==346600 || runNumber==312243 || runNumber==346605 || runNumber==346606 || runNumber==346607 || runNumber==345596 || runNumber==346632 || runNumber==346633 || runNumber==346634 || runNumber==346693 || runNumber==346694 || runNumber==345596 || runNumber==600069 || runNumber==600070 || runNumber==313343)){
    m_doSigOverlapTree=true;
    if(m_signalOverlapFileMap.find(runNumber)==m_signalOverlapFileMap.end()){
      stringstream soName;
      soName << "Overlap_vbfhinv_" << runNumber << ".root";
      m_signalOverlapFileMap[runNumber] = new TFile(soName.str().c_str(),"RECREATE");
      m_signalOverlapTreeMap[runNumber] = new TTree("physics","signal overlap tree");
      m_signalOverlapTreeMap[runNumber]->SetDirectory(m_signalOverlapFileMap[runNumber]);
      m_signalOverlapTreeMap[runNumber]->Branch("event", &m_sigOverlapEvent, "event/l");
      m_signalOverlapTreeMap[runNumber]->Branch("category",&m_sigOverlapCategory);
      m_signalOverlapTreeMap[runNumber]->Branch("dsid",&runNumber);
      m_signalOverlapTreeMap[runNumber]->Branch("year",&year);
    }
  }else{  m_doSigOverlapTree=false; }

  // Compute jet centrality
  float max_centrality=0.0, maxmj3_over_mjj=0.0;
  TLorentzVector j1v,j2v, tmp;
  if(jet_eta->size()>1){
    j1v.SetPtEtaPhiM(jet_pt->at(0), jet_eta->at(0), jet_phi->at(0), jet_m->at(0));
    j2v.SetPtEtaPhiM(jet_pt->at(1), jet_eta->at(1), jet_phi->at(1), jet_m->at(1));
  }
  for(unsigned iJet=2; iJet<jet_eta->size(); ++iJet){
    tmp.SetPtEtaPhiM(jet_pt->at(iJet), jet_eta->at(iJet), jet_phi->at(iJet), jet_m->at(iJet));
    float centrality = exp(-4.0/std::pow(jj_deta,2) * std::pow(jet_eta->at(iJet) - (jet_eta->at(0)+jet_eta->at(1))/2.0,2));
    if(max_centrality<centrality) max_centrality=centrality;
    float mj1 = (tmp+j1v).M();
    float mj2 = (tmp+j2v).M();
    float j3_over_mjj =std::min(mj1,mj2)/jj_mass;
    if(j3_over_mjj>maxmj3_over_mjj) maxmj3_over_mjj = j3_over_mjj;
  }

  // Cuts
  float METCut=180.0e3; // 150.0e3
  float jj_DPHICut=1.8;
  float jj_DPHILowCut=-100.0;
  float METCSTJetCut = 150.0e3; // 120.0e3
  float jj_detaCut = 4.8; // 4.0
  float jj_massCut = 1000.0e3; // 1000.0e3
  if((m_binning>=7 && m_binning<=12) || m_binning==21 || m_binning==22 || m_binning==23){ jj_massCut = 800.0e3; jj_DPHICut=2.0; } // 1000.0e3 
  if(doDoubleRatio) jj_massCut=500.0e3;
  bool jetCut = (n_jet ==2); //  (n_jet>1 && n_jet<5 && max_centrality<0.6 && maxmj3_over_mjj<0.05)
  bool nbjetCut = (n_bjet < 2); 
  if(doHighDphijj) { jj_DPHICut=10.0; jj_DPHILowCut=2.5; } // adjust cuts for high dphijj
    
  // decide if this MG or sherpa
  bool passSample=false;
  if(isMadgraph){ //311429 to 311453 MG filtered, 366010 to 366035 Znn rm, 364216 to 364229 PTV ,
    // NOTE this only works when the MG is merged!!
    if(currentSample=="W_strong") passSample=(runNumber >= 363600 && runNumber <= 363671) || (runNumber>=311445 && runNumber<=311453);
    else if(currentSample=="Z_strong") passSample=(runNumber >= 363147 && runNumber <= 363170) || (runNumber >= 363123 && runNumber <= 363146) || (runNumber >= 361510 && runNumber <= 361519) || (runNumber>=311429 && runNumber<=311444);
    else passSample=true;
  }else{
    if(currentSample=="W_strong") passSample=!(runNumber >= 363600 && runNumber <= 363671) && !(runNumber >= 311429 && runNumber <= 311453) && !(runNumber >= 364216 && runNumber <= 364229);
    else if(currentSample=="Z_strong"){
      passSample=!((runNumber >= 363147 && runNumber <= 363170) || (runNumber >= 363123 && runNumber <= 363146) || (runNumber >= 361510 && runNumber <= 361519)) && !(runNumber >= 311429 && runNumber <= 311453) && !(runNumber >= 366010 && runNumber <= 366035) && !(runNumber >= 364216 && runNumber <= 364229);
      if(year==2018)       passSample=!((runNumber >= 363147 && runNumber <= 363170) || (runNumber >= 363123 && runNumber <= 363146) || (runNumber >= 361510 && runNumber <= 361519)) && !(runNumber >= 311429 && runNumber <= 311453) && !(runNumber >= 364216 && runNumber <= 364221) && !(runNumber >= 364224 && runNumber <= 364229);
    }else if(currentSample=="Z_strongPTVExt"){
      if(year==2018)       passSample=!(runNumber >= 364216 && runNumber <= 364221) && !(runNumber >= 364224 && runNumber <= 364229);
      else passSample=true;
    } else passSample=true;
  }
  // remove the mg Zgam samples
  if(isMC && runNumber>=345775 && runNumber<=345784)  passSample=false;
  if(!passSample)  return StatusCode::SUCCESS;
  // if merging the sherpa sample from kt filtered, then require passVjetsFilter
  if(mergeKTPTV && passVjetsFilterTauEl<0.5) return  StatusCode::SUCCESS;
  /// register the vjets samples
  bool isVjets =(currentSample=="W_strong") || (currentSample=="Z_strong") || (currentSample=="Z_EWK") || (currentSample=="W_EWK") || (currentSample=="Z_strongPTVExt") || (currentSample=="Z_strongExt") || (currentSample=="Z_strong_VBFFilt") || (currentSample=="W_strongExt");
  bool isTop = (currentSample=="ttbar");
  bool isVBFH = (currentSample=="VBFH125");
  bool isVgjets = (currentSample=="ttg") || (currentSample=="Zg_strong") || (currentSample=="Wg_strong") || (currentSample=="Zg_EWK") || (currentSample=="Wg_EWK") || (currentSample=="VBFHgam125");
  if(isMC && runNumber>=364550 && runNumber<=364584) isVgjets=true; // vgg events. used for overlap

  // removed extra top samples:
  //std::cout << "runNumber:"<<runNumber << std::endl;
  if(runNumber==410649 || runNumber==410648 || runNumber==410472 || runNumber==410642 || runNumber==410643) return StatusCode::SUCCESS;

  //std::cout << "BEFORE met_tst_nolep_j1_dphi: " << met_tst_nolep_j1_dphi << " met_tst_nolep_j2_dphi: " << met_tst_nolep_j2_dphi << " met_tst_et: " << met_tst_et << " met_tst_nolep_et: " << met_tst_nolep_et
  //	    << " met_tst_j1_dphi: " << met_tst_j1_dphi << " met_tst_j2_dphi: " << met_tst_j2_dphi	    
  //<< std::endl;
  if(n_jet>1){ // recomputing variables
    met_tst_j1_dphi = fabs(GetDPhi(met_tst_phi, jet_phi->at(0)));
    met_tst_j2_dphi = fabs(GetDPhi(met_tst_phi, jet_phi->at(1)));
    met_tst_nolep_j1_dphi = fabs(GetDPhi(met_tst_nolep_phi, jet_phi->at(0)));
    met_tst_nolep_j2_dphi = fabs(GetDPhi(met_tst_nolep_phi, jet_phi->at(1)));
    //std::cout << "BEFORE-RECALC met_tst_nolep_j1_dphi: " << met_tst_nolep_j1_dphi << " met_tst_nolep_j2_dphi: " << met_tst_nolep_j2_dphi << " met_tst_et: " << met_tst_et << " met_tst_nolep_et: " << met_tst_nolep_et 
    //<< " met_tst_j1_dphi: " << met_tst_j1_dphi << " met_tst_j2_dphi: " << met_tst_j2_dphi	    
    //<< std::endl;
  }

  // modify the MET definition
  if(m_metdef==1 && n_jet>1){ // changing to tenacious
    met_tst_et = met_tenacious_tst_et;
    met_tst_phi = met_tenacious_tst_phi;
    met_tst_nolep_et = met_tenacious_tst_nolep_et;
    met_tst_j1_dphi = fabs(GetDPhi(met_tenacious_tst_phi, jet_phi->at(0)));
    met_tst_j2_dphi = fabs(GetDPhi(met_tenacious_tst_phi, jet_phi->at(1)));
    met_tst_nolep_j1_dphi = fabs(GetDPhi(met_tenacious_tst_nolep_phi, jet_phi->at(0)));
    met_tst_nolep_j2_dphi = fabs(GetDPhi(met_tenacious_tst_nolep_phi, jet_phi->at(1)));
  }
  //std::cout << "met_tst_nolep_j1_dphi: " << met_tst_nolep_j1_dphi << " met_tst_nolep_j2_dphi: " << met_tst_nolep_j2_dphi << " met_tst_et: " << met_tst_et << " met_tst_nolep_et: " << met_tst_nolep_et 
  //<< " met_tst_j1_dphi: " << met_tst_j1_dphi << " met_tst_j2_dphi: " << met_tst_j2_dphi
  //<< std::endl;

  // extra vetos  
  bool leptonVeto = false;
  bool metSoftVeto = false;
  bool fJVTVeto = false;
  bool fJVTLeadVeto = false;
  bool JetTimingVeto = false;
  bool JetQGTagger = false;
  if(m_extraVars>0){

    if(jet_NTracks && jet_NTracks->size()>0 && (fabs(jet_eta->at(0))<2.1 && jet_NTracks->at(0)>5))
      JetQGTagger=true;
    if(jet_NTracks && jet_NTracks->size()>1 && (fabs(jet_eta->at(1))<2.1 && jet_NTracks->at(1)>5))
      JetQGTagger=true;
    //leptonVeto = (n_baseel>0 || n_basemu>0) && !(((n_el+n_mu)==1 && (n_baseel+n_basemu)==1) || ((n_el+n_mu)==2 && (n_baseel+n_basemu)==2));
    metSoftVeto = met_soft_tst_et>20.0e3;
    if(m_extraVars==3) metSoftVeto=false;
    //if(doTMVA) metSoftVeto=false; // turn off the veto for ANN
    if(jet_fjvt->size()>1){
      fJVTVeto = fabs(jet_fjvt->at(0))>0.5 || fabs(jet_fjvt->at(1))>0.5;
      fJVTLeadVeto = fabs(jet_fjvt->at(0))>0.5;
    }else { fJVTVeto=true; fJVTLeadVeto=false; }
    if(jet_timing->size()>1)
      JetTimingVeto = fabs(jet_timing->at(0))>11.0 || fabs(jet_timing->at(1))>11.0;
    else JetTimingVeto = true;

    // tighten fjvt for the lower met events
    if(m_extraVars>1){
      if(n_baseel==0 && n_basemu==0){
	if(met_tst_et<200.0e3){
	  fJVTVeto = fabs(jet_fjvt->at(0))>0.2 || fabs(jet_fjvt->at(1))>0.2;
	  fJVTLeadVeto = fabs(jet_fjvt->at(0))>0.2;
	}
      }else{
	if(met_tst_nolep_et<200.0e3){
	  fJVTVeto = fabs(jet_fjvt->at(0))>0.2 || fabs(jet_fjvt->at(1))>0.2;
	  fJVTLeadVeto = fabs(jet_fjvt->at(0))>0.2;
	}
      }
    }
  
    // setting fjvt for photon analysis
    if(doVBFMETGam){
      metSoftVeto=false; // turn off the veto for gamma analysis
      if(jet_fjvt->size()>1){
	fJVTVeto = fabs(jet_fjvt->at(0))>0.4 || fabs(jet_fjvt->at(1))>0.4;
	fJVTLeadVeto = fabs(jet_fjvt->at(0))>0.4;
	//if(fabs(ph_pointing_z)>250.0) return StatusCode::SUCCESS;
	//if(n_ph_crackVetoCleaning>0) return StatusCode::SUCCESS; // met photon cleaning
      }
    }

    // veto events with tighter selections
    if(metSoftVeto || JetTimingVeto || leptonVeto) return StatusCode::SUCCESS;
  
    if(m_extraVars>1){
      METCut=160.0e3; // try 160
      METCSTJetCut=140.0e3; // try 140
      if(m_binning==12){ // this sets a met cut linearly from 150 to 200 for 800-2500 GeV in mjj
	METCut=200.0e3;
	if(jj_mass<2.5e6) METCut-=(jj_mass-800.0e3)*(0.0294118);
      }
      jj_detaCut=3.8;
      jetCut = (n_jet>1 && n_jet<5 && max_centrality<0.6 && maxmj3_over_mjj<0.05);
    }
  }
  // set MET cut if requested
  if(m_METCut>0.0){
    METCut=m_METCut;
    METCSTJetCut=m_METCut-20.0e3;
  }
  bool METCutForMETBinning = (met_tst_nolep_et > 200e3) && (met_cst_jet > 180e3);

  // setting MET cuts for photon analysis
  if(doVBFMETGam){
    METCut=150.0e3;
    METCSTJetCut=120.0e3;
  }

  xeSFTrigWeight=1.0;
  xeSFTrigWeight_nomu=1.0;
  unsigned metRunNumber = randomRunNumber;
  if(!isMC) metRunNumber=runNumber;
  if(isMC){ // the MET trigger SF is turned off in the up variation. so it will be =1.
    xeSFTrigWeight = weightXETrigSF(met_tst_et, metRunNumber, 0); // met was used in the end instead of jj.Pt() 
    xeSFTrigWeight_nomu = weightXETrigSF(met_tst_nolep_et, metRunNumber, 0); // met was used in the end instead of jj.Pt() 
    if(currentVariation=="xeSFTrigWeight__1up")   { xeSFTrigWeight = weightXETrigSF(met_tst_et, metRunNumber, 1); xeSFTrigWeight_nomu = weightXETrigSF(met_tst_nolep_et, metRunNumber, 1); }
    if(currentVariation=="xeSFTrigWeight__1down") { xeSFTrigWeight = weightXETrigSF(met_tst_et, metRunNumber, 2); xeSFTrigWeight_nomu = weightXETrigSF(met_tst_nolep_et, metRunNumber, 2); }
  }

  // Choose the met trigger
  bool passMETTrig = ((trigger_met &0x1) == 0x1);
  if(year==2017){
    //passMETTrig=0;
    //if     (325713<=metRunNumber && metRunNumber<=328393 && ((trigger_met_encodedv2 & 0x4)==0x4))   passMETTrig=1; //HLT_xe90_pufit_L1XE50;    // period B
    //else if(329385<=metRunNumber && metRunNumber<=330470 && ((trigger_met_encodedv2 & 0x40)==0x40)) passMETTrig=1; //HLT_xe100_pufit_L1XE55;   // period C
    //else if(330857<=metRunNumber && metRunNumber<=331975 && ((trigger_met_encodedv2 & 0x2)==0x2))   passMETTrig=1; //HLT_xe110_pufit_L1XE55;   // period D1-D5
    //else if(341649>=metRunNumber && metRunNumber>331975 && ((trigger_met_encodedv2 & 0x80)==0x80))  passMETTrig=1; //HLT_xe110_pufit_L1XE50;   // period D6-K  
    passMETTrig=0; if(((trigger_met_encodedv2 & 0x2)==0x2))    passMETTrig=1;
  }else if(year==2018){
    //passMETTrig=0;
    //if     (350067> metRunNumber && metRunNumber>=348197  && ((trigger_met_encodedv2 & 0x8)==0x8))    passMETTrig=1; // HLT_xe110_pufit_xe70_L1XE50
    //else if(350067<=metRunNumber && metRunNumber<=364292 && ((trigger_met_encodedv2 & 0x800)==0x800)) passMETTrig=1; // HLT_xe110_pufit_xe65_L1XE50
    //if     (metRunNumber>=355529  && ((trigger_met_encodedv2 & 0x4000)==0x4000))     trigger_met_encodedv2_new=10; // HLT_j70_j50_0eta490_invm1000j50_dphi24_xe90_pufit_xe50_L1MJJ-500-NFF
    //if     (metRunNumber>=355529  && ((trigger_met_encodedv2 & 0x8000)==0x8000))     trigger_met_encodedv2_new=11; // HLT_j70_j50_0eta490_invm1100j70_dphi20_deta40_L1MJJ-500-NFF
    passMETTrig=0; if(((trigger_met_encodedv2 & 0x8)==0x8))    passMETTrig=1;
  }

  // setup the photon + MET+ VBF analysis
  bool phSelectionCut = (n_ph==0);
  float phcentrality = 1.0;
  float phcentralityCut=0.4; // set to pass
  float met_tst_ph_dphi = 10.0;
  float met_tst_ph_dphiCut = 1.8;
  bool in_vy_overlapCut=true;
  bool jetPtCuts=(n_jet>1 && (jet_pt->at(0) > 80e3) && (jet_pt->at(1) > 50e3));
  mtgam=-1.0;
  if(doVBFMETGam){
    jetCut = (n_jet ==2 || n_jet==3);
    jetPtCuts=(n_jet>1 && (jet_pt->at(0) > 60e3) && (jet_pt->at(1) > 50e3));
    jj_detaCut=3.0;
    jj_massCut=250.0e3;
    jj_DPHICut=2.0;
    phSelectionCut=(n_ph==1 && ph_pt->at(0)<110e3);
    if(n_ph>0){
      phcentrality = exp(-4.0/std::pow(jj_deta,2) * std::pow(ph_eta->at(0) - (jet_eta->at(0)+jet_eta->at(1))/2.0,2));
      met_tst_ph_dphi = fabs(GetDPhi(met_tst_nolep_phi, ph_phi->at(0)));
      if(doMTFit) met_tst_ph_dphi=10.0; // set to pass for the mt fit
      mtgam = sqrt(2. * ph_pt->at(0) * met_tst_nolep_et * (1. - cos(ph_phi->at(0) - met_tst_nolep_phi)));
    }
    // if this is a vjets sample and it has a photon overlap, then remove it
    if(isVjets && in_vy_overlap) in_vy_overlapCut=false;
    if(isTop   && in_vy_overlap) in_vy_overlapCut=false;
    if(isVBFH  && in_vy_overlap) in_vy_overlapCut=false;
    if(isVgjets && !in_vy_overlap) in_vy_overlapCut=false;
    // need to remove the signal, apply this to the Vgamma samples
  }

  // basic selection.
  if (!((passJetCleanTight == 1) & nbjetCut & jetCut & jetPtCuts & (jj_dphi < jj_DPHICut) & (jj_dphi > jj_DPHILowCut) & (jj_deta > jj_detaCut) & ((jet_eta->at(0) * jet_eta->at(1))<0) & (jj_mass > jj_massCut) & (phSelectionCut) & (phcentrality>phcentralityCut) & (met_tst_ph_dphi>met_tst_ph_dphiCut) & (in_vy_overlapCut))) return StatusCode::SUCCESS; 

  int passMTCut=0;
  if(n_el==1) { met_significance = met_tst_et/1000/sqrt((el_pt->at(0)+jet_pt->at(0)+jet_pt->at(1))/1000.0); } else {  met_significance = 0; }
  if(n_mu==1) { 
    double MT = sqrt(2. * mu_pt->at(0) * met_tst_et * (1. - cos(mu_phi->at(0) - met_tst_phi)));
    passMTCut=(MT>20e3) ? 1 : 2;
  }
  if(doVBFMETGam) passMTCut=0;

  if(v26Ntuples) lep_trig_match=1;
  bool trigger_lep_bool = ((trigger_lep & 0x1)==0x1) && lep_trig_match>0; // note that lep_trig_match is only computed for signal lepton triggers. We assume it is perfect for dilepton triggers.
  bool trigger_lep_Zee_bool = trigger_lep_bool;
  bool trigger_lep_Zmm_bool = trigger_lep_bool;
  bool trigger_lep_Wmu_bool = trigger_lep_bool;
  if(m_extraVars<=5) xeSFTrigWeight_nomu=1.0;
  if(!v26Ntuples){
    if(m_extraVars>=5) { trigger_lep_Zmm_bool = (trigger_lep_bool || (trigger_lep & 0x20)==0x20);  trigger_lep_Zee_bool = (trigger_lep_bool || (trigger_lep & 0x400)==0x400); }
  }else{
    if(m_extraVars>=5) { trigger_lep_Zmm_bool = (trigger_lep>0);  trigger_lep_Zee_bool = (trigger_lep>0); }
  }

  if(m_extraVars==6) { trigger_lep_Zmm_bool=passMETTrig; trigger_lep_Wmu_bool = passMETTrig; }
  if(m_extraVars==7 && passMETTrig){ trigger_lep_Zmm_bool=true; trigger_lep_Wmu_bool=true; }
  if(m_extraVars==7 && !passMETTrig){ xeSFTrigWeight_nomu=1.0; } // remove the MET trigger SF for non-met triggered events
  // compute the mll
  float mll=-999.0;
  TLorentzVector l0, l1;
  if(n_el == 2){
    l0.SetPtEtaPhiM(el_pt->at(0), el_eta->at(0),  el_phi->at(0), 0.511);
    l1.SetPtEtaPhiM(el_pt->at(1), el_eta->at(1),  el_phi->at(1), 0.511);
    mll = (l0+l1).M();
  }
  if(n_mu == 2){
    l0.SetPtEtaPhiM(mu_pt->at(0), mu_eta->at(0),  mu_phi->at(0), 105.66);
    l1.SetPtEtaPhiM(mu_pt->at(1), mu_eta->at(1),  mu_phi->at(1), 105.66);
    mll = (l0+l1).M();
  }

  // lepton vetos
  bool SR_lepVeto = ((n_el == 0) && (n_mu == 0));
  bool We_lepVeto = ((n_el == 1) && (n_mu == 0));
  bool Wm_lepVeto = ((n_el == 0) && (n_mu == 1));
  bool Zee_lepVeto = ((n_el == 2) && (n_mu == 0));
  bool Zmm_lepVeto = ((n_el == 0) && (n_mu == 2));
  bool Zll_METVETO = (met_tst_et<70.0e3);
  if(!v26Ntuples){
    SR_lepVeto  = ((n_baseel == 0) && (n_basemu_noOR == 0));
    We_lepVeto  = ((n_baseel == 1) && (n_basemu_noOR == 0) && (n_el_w == 1));
    Wm_lepVeto  = ((n_baseel == 0) && (n_basemu_noOR == 1) && (n_mu_w == 1));
    //We_lepVeto  = ((n_baseel == 1) && (n_basemu_noOR == 0) && (n_el == 1));
    //Wm_lepVeto  = ((n_baseel == 0) && (n_basemu_noOR == 1) && (n_mu == 1));
    Zee_lepVeto = ((n_baseel == 2) && (n_basemu_noOR == 0) && (n_el == 2));
    Zmm_lepVeto = ((n_baseel == 0) && (n_basemu_noOR == 2) && (n_mu == 2));
  }else if(m_extraVars>0){
    SR_lepVeto  = ((n_baseel == 0) && (n_basemu == 0));
    We_lepVeto  = ((n_baseel == 1) && (n_basemu == 0) && (n_el == 1));
    Wm_lepVeto  = ((n_baseel == 0) && (n_basemu == 1) && (n_mu == 1));
    Zee_lepVeto = ((n_baseel == 2) && (n_basemu == 0) && (n_el == 2));
    Zmm_lepVeto = ((n_baseel == 0) && (n_basemu == 2) && (n_mu == 2));
  }

  bool elPtCut = n_el>0 ? (el_pt->at(0)>30.0e3) : false;
  bool muPtCut = n_mu>0 ? (mu_pt->at(0)>30.0e3) : false;
  bool muSubPtCut = n_mu>1 ? (mu_pt->at(1)>7.0e3) : false;
  bool elSubPtCut = n_el>1 ? (el_pt->at(1)>7.0e3) : false;
  bool ZelPtCut = elPtCut;
  bool ZmuPtCut = muPtCut;
  bool elChPos = n_el>0 ? (el_charge->at(0) > 0) : false;
  bool muChPos = n_mu>0 ? (mu_charge->at(0) > 0) : false;
  bool OppSignElCut = n_el>1 ? (el_charge->at(0)*el_charge->at(1) < 0) : false;
  bool OppSignMuCut = n_mu>1 ? (mu_charge->at(0)*mu_charge->at(1) < 0) : false;
  if(v26Ntuples){
    if(m_extraVars==4 || m_extraVars==5 || m_extraVars==6 || m_extraVars==7){
      ZelPtCut = n_baseel>0 ? (baseel_pt->at(0)>30.0e3): false;
      ZmuPtCut = n_basemu>0 ? (basemu_pt->at(0)>30.0e3): false;
      elSubPtCut = n_baseel>1 ? (baseel_pt->at(1)>7.0e3): false;
      muSubPtCut = n_basemu>1 ? (basemu_pt->at(1)>7.0e3): false;    
      Zee_lepVeto = ((n_baseel == 2) && (n_basemu == 0));
      Zmm_lepVeto = ((n_baseel == 0) && (n_basemu == 2)); 
      OppSignElCut = n_baseel>1 ? (baseel_charge->at(0)*baseel_charge->at(1) < 0) : false;
      OppSignMuCut = n_basemu>1 ? (basemu_charge->at(0)*basemu_charge->at(1) < 0) : false;

      // recompute mjll
      if(n_baseel == 2){
	l0.SetPtEtaPhiM(baseel_pt->at(0), baseel_eta->at(0),  baseel_phi->at(0), 0.511);
	l1.SetPtEtaPhiM(baseel_pt->at(1), baseel_eta->at(1),  baseel_phi->at(1), 0.511);
	mll = (l0+l1).M();
      }
      if(n_basemu == 2){
	l0.SetPtEtaPhiM(basemu_pt->at(0), basemu_eta->at(0),  basemu_phi->at(0), 105.66);
	l1.SetPtEtaPhiM(basemu_pt->at(1), basemu_eta->at(1),  basemu_phi->at(1), 105.66);
	mll = (l0+l1).M();
      }
    }
  }
  bool SRDPHIJETMET =  (met_tst_j1_dphi>1.0) && (met_tst_j2_dphi>1.0);
  bool CRDPHIJETMET = (met_tst_nolep_j1_dphi>1.0) && (met_tst_nolep_j2_dphi>1.0);
  SRDPHIJETMET=true;// remove these cuts as there is no impact
  CRDPHIJETMET=true;// remove these cuts as there is no impact 
  if ((passMETTrig) && !fJVTVeto && (met_tst_et > METCut) & (met_cst_jet > METCSTJetCut) & SRDPHIJETMET & (SR_lepVeto)) SR = true;
  if ((passMETTrig) && fJVTLeadVeto && (met_tst_et > METCut) & (met_cst_jet > METCSTJetCut) & SRDPHIJETMET & (SR_lepVeto)) CRFJVT = true;
  if ((trigger_lep_bool) && !fJVTVeto && (met_tst_nolep_et > METCut) && (met_cst_jet > METCSTJetCut) && CRDPHIJETMET && (We_lepVeto) && (elPtCut)){ if ((elChPos) & (doVBFMETGam?true:(met_significance > 4.0))) CRWep = true;}
  if ((trigger_lep_bool) && !fJVTVeto && (met_tst_nolep_et > METCut) && (met_cst_jet > METCSTJetCut) && CRDPHIJETMET && (We_lepVeto) && (elPtCut)){ if ((!elChPos) & (doVBFMETGam?true:(met_significance > 4.0))) CRWen = true;}
  if ((trigger_lep_bool) && !fJVTVeto && (met_tst_nolep_et > METCut) && (met_cst_jet > METCSTJetCut) && CRDPHIJETMET && (We_lepVeto) && (elPtCut)){ if ((elChPos) & (doVBFMETGam?false:(met_significance <= 4.0))) CRWepLowSig = true;}
  if ((trigger_lep_bool) && !fJVTVeto && (met_tst_nolep_et > METCut) && (met_cst_jet > METCSTJetCut) && CRDPHIJETMET && (We_lepVeto) && (elPtCut)){ if ((!elChPos) & (doVBFMETGam?false:(met_significance <= 4.0))) CRWenLowSig = true;}
  if ((trigger_lep_Wmu_bool) && !fJVTVeto && (met_tst_nolep_et > METCut) && (met_cst_jet > METCSTJetCut) && CRDPHIJETMET && (Wm_lepVeto) && (muPtCut)){ if ((muChPos)) CRWmp = true;}
  if ((trigger_lep_Wmu_bool) && !fJVTVeto && (met_tst_nolep_et > METCut) && (met_cst_jet > METCSTJetCut) && CRDPHIJETMET && (Wm_lepVeto) && (muPtCut)){ if ((!muChPos)) CRWmn = true;}
  if ((trigger_lep_Zee_bool) && !fJVTVeto && (met_tst_nolep_et > METCut) && (met_cst_jet > METCSTJetCut) && CRDPHIJETMET && Zll_METVETO && (Zee_lepVeto) && (ZelPtCut) && (elSubPtCut) && (mll> 66.0e3 && mll<116.0e3)){ if ((OppSignElCut)) CRZee = true;}
  if ((trigger_lep_Zmm_bool) && !fJVTVeto && (met_tst_nolep_et > METCut) && (met_cst_jet > METCSTJetCut) && CRDPHIJETMET && Zll_METVETO && (Zmm_lepVeto) && (ZmuPtCut) && (muSubPtCut) && (mll> 66.0e3 && mll<116.0e3)){ if ((OppSignMuCut)) CRZmm = true;}

  // do duplicate check
  if(doDuplicateCheck){
    if(CRZee || CRZmm) std::cout << "ZCR " << runNumber << " " << eventNumber << std::endl;
    if(SR) std::cout << "SR " << runNumber << " " << eventNumber << std::endl;
  }
  Float_t w_final = 1;
  Float_t lumi = 36.208;//36207.66
  if(year==2017)      lumi = 44.3074;
  else if(year==2018) lumi = 58.4501; //59.9372;
  if (isMC) w_final = w*1000.0*lumi;
  // reweight
  //if(isMC && year==2018){
  //  if(averageIntPerXing>39.0 && averageIntPerXing<52.1){
  //    if(n_jet>2) w_final*=1.2;
  //    if(n_jet>2 && fabs(jet_eta->at(2))>3.0) w_final*=1.3;
  //    if(n_jet==2) w_final*=1.07;
  //  }
  //}
  //%364250,364253,364254,364255,363355-363360,363489,363494,364242-364249, 1.78SYST on 0.56
  //check if this is VV/VVV. apply the NF 0.56
  if(isMC && (runNumber==364250 || (runNumber>=364253 && runNumber<=364255) || (runNumber==363355) || runNumber==363489 || runNumber==363494 
	      || (runNumber>=363355 && runNumber<=363360) || (runNumber>=364242 && runNumber<=364249) || (runNumber>=346190 && runNumber<=346194) || runNumber==345948)){
    w_final*=0.56;
    if(currentVariation=="vvUnc__1up") w_final*=(1.44);
    if(currentVariation=="vvUnc__1down") w_final/=1.44;
  }
  // hack for low pT w in 2016 that has a huge netative weight
  if(isMC && doVBFMETGam && runNumber==364170) w_final=5.0; // this is the average weight ~4 for 2016, 5 for 2017 and 10 for 2018

  int bin = 0;
  if(doTMVA){
    //float tmvaBinBoundaries[8] = {0.0, 0.75300000, 0.81700000, 0.86100000, 0.89500000, 0.92200000, 0.94600000, 1.0};
    //float tmvaBinBoundaries[8] = {0.0, 0.75300000, 0.8300000, 0.8800000, 0.9100000, 0.9400000, 0.9600000, 1.0};//var 11 run best    
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.69000000, 0.76500000, 0.80300000, 0.83300000, 0.86100000, 0.88780000,1.0 };//var5
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.71000000, 0.78400000, 0.82300000, 0.85300000, 0.88000000, 0.9078, 1.0 }; //var7
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.74000000, 0.80200000, 0.84000000, 0.86700000, 0.89000000, 0.91300000,1.0 };//var9
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.7300000, 0.83000000, 0.87700000, 0.90900000, 0.93400000, 0.9559,1.0 }; //var11
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.61600000, 0.72400000, 0.79000000, 0.83800000, 0.87700000, 0.91100000,1.0 };//var 11 -mjj500
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.69700000, 0.76800000, 0.81100000, 0.84500000, 0.87600000, 0.90950000,1.0 };// var8 - new tenacious cut
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.90250000, 0.93700000, 0.95100000, 0.95850000, 0.96400000, 0.96900000, 1.0 }; // var9 MG
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.66800000, 0.76700000, 0.82300000, 0.86250000, 0.89500000, 0.92800000, 1.0 }; // var9_noNjetCST

    if(doVBFMETGam){
      //float tmvaBinBoundaries[7] = { 0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0};
      float tmvaBinBoundaries[5] = {0.0, 0.55, 0.65 , 0.8, 1.0};
      for(unsigned i=0; i<4; ++i){ if(tmva>tmvaBinBoundaries[i] && tmva<=tmvaBinBoundaries[i+1]){ bin=i; break; } }
    }else{
      //float tmvaBinBoundaries[8] = { 0.0000000, 0.67050000, 0.74600000, 0.79600000, 0.83300000, 0.86450000, 0.89500000, 1.0 }; // var10_noNjet
      //float tmvaBinBoundaries[12] = {0.0, 0.75100000, 0.80770000, 0.83910000, 0.86250000, 0.88030000, 0.89640000, 0.90950000, 0.92100000, 0.93210000, 0.9448,1.0 }; // 11bins
      float tmvaBinBoundaries[12] = {0.0,  0.83490000, 0.86300000, 0.87740000, 0.88990000, 0.90140000, 0.91320000, 0.92450000, 0.93410000, 0.94210000, 0.94960000, 1.0};
      for(unsigned i=0; i<11; ++i){ if(tmva>tmvaBinBoundaries[i] && tmva<=tmvaBinBoundaries[i+1]){ bin=i; break; } } 
    }
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.71250000, 0.80000000, 0.84850000, 0.88300000, 0.91150000, 0.93800000,1.0 };// var 9 - new tenacious cut
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.74300000, 0.80700000, 0.84550000, 0.87400000, 0.89850000, 0.92500000,1.0 };// var 11 - new tenacious cut
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.70050000, 0.77450000, 0.81800000, 0.85200000, 0.88100000, 0.91050000,1.0 }; //var8
    //float tmvaBinBoundaries[8] = { 0.0000000, 0.73100000, 0.80450000, 0.84200000, 0.87050000, 0.89400000, 0.91800000,1.0 }; //var6
    // find the right bin
    //if(n_jet>2) bin=1; // test
    //std::cout << "tmva: " << tmva << " bin: " << bin << std::endl;
  }else{
    bool AddBelow1TeV=(m_binning>=7);
    if(!AddBelow1TeV){
      if (jj_mass < 1.5e6) bin = 0;
      else if (jj_mass < 2e6) bin = 1;
      else bin = 2;
    }else if(m_binning==7){
      if      (jj_mass < 1.0e6) bin = 0;
      else if (jj_mass < 1.5e6) bin = 1;
      else if (jj_mass < 2e6)   bin = 2;
      else bin = 3;
    }else if(m_binning==8 || m_binning==9){
      if      (jj_mass < 1.00e6) bin = 0;
      else if (jj_mass < 1.25e6) bin = 1;
      else if (jj_mass < 1.50e6) bin = 2;
      else if (jj_mass < 1.75e6) bin = 3;
      else if (jj_mass < 2.00e6) bin = 4;
      else if (jj_mass < 2.25e6) bin = 5;
      else if (jj_mass < 2.50e6) bin = 6;
      else bin = 7;
    }else if(m_binning==10){
      if      (jj_mass < 1.0e6) bin = 0;
      else if (jj_mass < 1.5e6) bin = 1;
      else if (jj_mass < 2e6)   bin = 2;
      else if (jj_mass < 3e6)   bin = 3;
      else bin = 4;
    }else if(m_binning==11 || m_binning==12){
      if      (jj_mass < 1.0e6) bin = 0;
      else if (jj_mass < 1.5e6) bin = 1;
      else if (jj_mass < 2e6)   bin = 2;
      else if (jj_mass < 3.5e6) bin = 3;
      else bin = 4;
    }else if(m_binning==13){
      if      (jj_mass < 0.5e6) bin = 0;
      else if (jj_mass < 1.0e6) bin = 1;
      else if (jj_mass < 1.5e6)   bin = 2;
      //else if (jj_mass < 2.0e6) bin = 3;
      else bin = 3;
    }else if(m_binning==21 || m_binning==22 || m_binning==23){
      if(METCutForMETBinning){
	if      (jj_mass < 1.0e6) bin = 0;
	else if (jj_mass < 1.5e6) bin = 1;
	else if (jj_mass < 2e6)   bin = 2;
	else if (jj_mass < 3.5e6) bin = 3;
	else bin = 4;
	if(jj_dphi>1 && m_binning!=23)  bin+=5; // separate dphijj
	if(n_jet>2 && !fJVTLeadVeto){
	  if (jj_mass < 1.5e6) return StatusCode::SUCCESS; // remove njet>2 and mjj<1.5 TeV
	  if(m_binning==23){// high dphijj so no dphijj binning
	    if (jj_mass < 2e6)   bin = 5;
	    else if (jj_mass < 3.5e6) bin = 6;
	    else bin = 7;
	  }else{
	    if (jj_mass < 2e6)   bin = 10;
	    else if (jj_mass < 3.5e6) bin = 11;
	    else bin = 12;
	  }
	}
      }else{// low met
	if(m_binning==21) return StatusCode::SUCCESS;
	else if(m_binning==23){// high dphijj so no dphijj binning. 
	  if ((jj_mass < 1.5e6)) return StatusCode::SUCCESS;
	  else if((n_jet>2) && !fJVTLeadVeto)  return StatusCode::SUCCESS; // allow for the fjvt crs
	  else if (jj_mass < 2e6)   bin = 8;
	  else if (jj_mass < 3.5e6) bin = 9;
	  else bin = 10;
	}else{
	  if ((jj_mass < 1.5e6)) return StatusCode::SUCCESS;
	  else if((n_jet>2) && !fJVTLeadVeto)  return StatusCode::SUCCESS; // allow for the fjvt crs
	  else if (jj_mass < 2e6)   bin = 13;
	  else if (jj_mass < 3.5e6) bin = 14;
	  else bin = 15;
	}
      }
    }

    // alternative binning approaches
    if(m_binning==-1 && JetQGTagger) bin+=3;
    if(m_binning==1 && ((met_tst_et<180.0e3 && SR) || (met_tst_nolep_et<180.0e3 && !SR)))  bin=3; // separate low MET bin
    if(m_binning==2 && (n_jet>2))  bin=3; // separate extra jets
    if(m_binning==3 && ((met_tst_et<180.0e3 && SR) || (met_tst_nolep_et<180.0e3 && !SR)))  bin+=3; // separate low MET bin, mjj binning
    if(m_binning==4 && (n_jet>2))    bin+=3; // separate extra jets, mjj binning
    if(m_binning==5 && (jj_dphi>1))  bin+=3; // separate dphijj, mjj binning
    // combo
    if(m_binning==6 && (jj_dphi>1))  bin+=3; // separate dphijj, mjj binning
    if(m_binning==6 && (n_jet>2))    bin=6; // separate dphijj, mjj binning, njet binning
    if(m_binning==7 && (jj_dphi>1))  bin+=4; // separate dphijj, mjj binning
    if(m_binning==7 && (n_jet>2))    bin=8; // separate dphijj, mjj binning, njet binning
    if(m_binning==8 && (n_jet>2))    bin=8; // separate dphijj, mjj binning, njet binning
    if(m_binning==10 && (jj_dphi>1))  bin+=5; // separate dphijj, mjj binning
    if(m_binning==10 && (n_jet>2))    bin=10; // separate dphijj, mjj binning, njet binning
    if(m_binning==11 && (jj_dphi>1))  bin+=5; // separate dphijj, mjj binning
    if(m_binning==11 && (!fJVTLeadVeto && n_jet>2))    bin=10; // separate dphijj, mjj binning, njet binning, not lead jet failing fjvt
    if(m_binning==12 && (jj_dphi>1))  bin+=5; // separate dphijj, mjj binning
    if(m_binning==12 && (n_jet>2))    bin=10; // separate dphijj, mjj binning, njet binning

    if(doDoubleRatio){
      if(m_binning==11 && (jj_mass < 800.0e3)){ bin=11; } 
      if(m_binning==12 && (jj_mass < 800.0e3)){ bin=11; } 
      if(m_binning==0  && (jj_mass < 1000.0e3)){ bin=4; } 
      if(m_binning==6  && (jj_mass < 1000.0e3)){ bin=7; } 
    }
  }

  if(isnan(w_final)) std::cout << "isnan w_final? " << w_final << std::endl;
  if(isnan(xeSFTrigWeight)) std::cout << "isnan xeSFTrigWeight? " << xeSFTrigWeight << std::endl;

  if(!singleHist){
    if (SR) HistoFill(hSR[bin],w_final*xeSFTrigWeight); // only apply the trigger SF to the SR. It is only where the MET trigger is used
    if (CRWep){       HistoFill(hCRWe[bin],w_final);                                                 if(hCRWep.size()>bin){       HistoFill(hCRWep[bin],w_final); } }
    if (CRWen){       HistoFill(hCRWe[bin],w_final);                                                 if(hCRWen.size()>bin){       HistoFill(hCRWen[bin],w_final); } }
    if (CRWepLowSig){ HistoFill(hCRWeLowSig[bin],w_final);                                           if(hCRWepLowSig.size()>bin){ HistoFill(hCRWepLowSig[bin],w_final); } }
    if (CRWenLowSig){ HistoFill(hCRWeLowSig[bin],w_final);                                           if(hCRWenLowSig.size()>bin){ HistoFill(hCRWenLowSig[bin],w_final); } }
    if (CRWmp){       HistoFill(hCRWm[bin],w_final*xeSFTrigWeight_nomu);                             if(hCRWmp.size()>bin){       HistoFill(hCRWmp[bin],w_final*xeSFTrigWeight_nomu); } }
    if (CRWmn && (passMTCut==0 || passMTCut==1)){ HistoFill(hCRWm[bin],w_final*xeSFTrigWeight_nomu); if(hCRWmn.size()>bin){       HistoFill(hCRWmn[bin],w_final*xeSFTrigWeight_nomu); } }
    if((CRWmn || CRWmp) && passMTCut==2){ HistoFill(hCRWmMT[bin],w_final*xeSFTrigWeight_nomu); }// low MT
    if (CRZee){       HistoFill(hCRZll[bin],w_final);                                                if(hCRZee.size()>bin){       HistoFill(hCRZee[bin],w_final); } }
    if (CRZmm){       HistoFill(hCRZll[bin],w_final*xeSFTrigWeight_nomu);                            if(hCRZmm.size()>bin){       HistoFill(hCRZmm[bin],w_final*xeSFTrigWeight_nomu); } }
    if (CRFJVT){      HistoFill(hCRFJVT[bin],w_final*xeSFTrigWeight); }
  }else{// one histogram, so need to find the real bin number
    float myWeight=w_final;
    if (CRWmp && CRWmn && CRZmm) myWeight=w_final*xeSFTrigWeight_nomu;
    if (SR) myWeight=w_final*xeSFTrigWeight;
    
    int nRegion = -1;
    if(SR) nRegion=8;
    if(CRZmm) nRegion=7;
    if(CRZee) nRegion=6;
    if(CRWmp) nRegion=5;
    if(CRWmn) nRegion=4;
    if(CRWep) nRegion=3;
    if(CRWen) nRegion=2;
    if(CRWepLowSig) nRegion=1;
    if(CRWenLowSig) nRegion=0;
    if(nRegion>-0.5){
      float binVal = totalBins*float(nRegion)+bin+1.0; // should start from 1
      hSR[0][0]->Fill(binVal,myWeight);
    }

  }
  //  add events to the signal overlap tree
  if(m_doSigOverlapTree && (SR || CRWep || CRWen || CRWepLowSig || CRWenLowSig || CRWmp || CRWmn || CRZee || CRZmm)){
    m_sigOverlapEvent = eventNumber;
    m_sigOverlapCategory.clear();
    stringstream evtCategory;
    evtCategory << 9;
    evtCategory << (n_ph==0 ? "0" : "5"); // 0 = VBF analysis, 5 = photon analysis 
    evtCategory << (SR ? "0" : (CRZee || CRZmm) ? "2" : "1");
    evtCategory << (SR ? "0" : "1");
    evtCategory << bin; // add the bin number. analysis specific   
    m_sigOverlapCategory.push_back(std::stoi(evtCategory.str()));
    m_signalOverlapTreeMap[runNumber]->Fill();
  }

  setFilterPassed(true); //if got here, assume that means algorithm passed
  return StatusCode::SUCCESS;
}

void HFInputAlg::HistoFill(vector<TH1F*> hs, double w){
  hs[0]->Fill(1,w);
  if(!doPlot && doMTFit) hs[1]->Fill(mtgam/(1e3),w);
  if (doPlot) {
    hs[1]->Fill(jj_mass/(1e3),w);
    hs[2]->Fill(jj_dphi,w);
    hs[3]->Fill(met_tst_et/(1e3),w);
    hs[4]->Fill(met_tst_nolep_et/(1e3),w);
    if(doTMVA){
      hs[5]->Fill(tmva,w);
      if(doMTFit) hs[6]->Fill(mtgam/(1e3),w);
    }else if(doMTFit) hs[5]->Fill(mtgam/(1e3),w);
  }
  return ;
}


StatusCode HFInputAlg::beginInputFile() { 
  //
  //This method is called at the start of each input file, even if
  //the input file contains no events. Accumulate metadata information here
  //

  //example of retrieval of CutBookkeepers: (remember you will need to include the necessary header files and use statements in requirements file)
  // const xAOD::CutBookkeeperContainer* bks = 0;
  // CHECK( inputMetaStore()->retrieve(bks, "CutBookkeepers") );

  //example of IOVMetaData retrieval (see https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/AthAnalysisBase#How_to_access_file_metadata_in_C)
  //float beamEnergy(0); CHECK( retrieveMetadata("/TagInfo","beam_energy",beamEnergy) );
  //std::vector<float> bunchPattern; CHECK( retrieveMetadata("/Digitiation/Parameters","BeamIntensityPattern",bunchPattern) );
  if (doLowNom || weightSyst) {
    m_treeName = currentSample+"Nominal";
  } else{
    m_treeName = currentSample+currentVariation;
  }
  std::cout << "Tree Name: " <<m_treeName <<std::endl;
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  std::cout << "Tree Entries: " <<m_tree->GetEntries() <<std::endl;
  m_tree->SetBranchStatus("*",0);
  if(weightSyst && currentVariation!="xeSFTrigWeight__1up"  && currentVariation!="xeSFTrigWeight__1down" && currentVariation!="vvUnc__1up" && currentVariation!="vvUnc__1down"){// MET trigger SF systematic is computed differently. The variable is saved. So here we just pickup the nominal weights
    bool found=false;
    TObjArray *var_list = m_tree->GetListOfBranches();
    for(unsigned a=0; a<unsigned(var_list->GetEntries()); ++a) { 
      TString var_name = var_list->At(a)->GetName();
      if(var_name.Contains(currentVariation)){
	if(var_name.Contains("ANTISF") && currentVariation.find("ANTISF")==std::string::npos) continue; // checking that the antiID SF are treated separately. skipping if they dont match to avoid picking the ID SF
	m_tree->SetBranchStatus(var_name, 1);
	m_tree->SetBranchAddress(var_name, &w);
	found=true;
	break;
      }
    }  
    if(!found){
      std::cout << "ERROR - did not find the correct weight systematic for " << currentVariation <<std::endl;
      m_tree->SetBranchStatus("w", 1);
      m_tree->SetBranchAddress("w", &w);
    }
  }else{
    m_tree->SetBranchStatus("w", 1);
    m_tree->SetBranchAddress("w", &w);
  }
  m_tree->SetBranchStatus("runNumber", 1);
  m_tree->SetBranchStatus("randomRunNumber", 1);
  m_tree->SetBranchStatus("eventNumber", 1);
  m_tree->SetBranchStatus("passVjetsFilter", 1);
  m_tree->SetBranchStatus("passVjetsFilterTauEl", 1);
  m_tree->SetBranchStatus("in_vy_overlap", 1);
  m_tree->SetBranchStatus("passJetCleanTight", 1);
  m_tree->SetBranchStatus("averageIntPerXing", 1);
  m_tree->SetBranchStatus("trigger_met", 1);
  m_tree->SetBranchStatus("trigger_met_encodedv2", 1);
  m_tree->SetBranchStatus("trigger_lep", 1);
  m_tree->SetBranchStatus("lep_trig_match", 1);
  m_tree->SetBranchStatus("n_jet",1);
  m_tree->SetBranchStatus("n_bjet",1);
  m_tree->SetBranchStatus("n_ph",1);
  m_tree->SetBranchStatus("n_ph_crackVetoCleaning",1);  
  m_tree->SetBranchStatus("n_el",1);
  m_tree->SetBranchStatus("n_mu",1);
  m_tree->SetBranchStatus("n_el_w",1);
  m_tree->SetBranchStatus("n_mu_w",1);
  m_tree->SetBranchStatus("n_baseel",1);
  m_tree->SetBranchStatus("n_basemu",1);
  m_tree->SetBranchStatus("n_el_baseline_noOR",1); //n_mu_baseline_noOR
  m_tree->SetBranchStatus("n_mu_baseline_noOR",1);
  m_tree->SetBranchStatus("n_el_baseline_iso",1);
  m_tree->SetBranchStatus("n_mu_baseline_iso",1);
  if(doTMVA) m_tree->SetBranchStatus("tmva",1);
  m_tree->SetBranchStatus("jj_mass",1);
  m_tree->SetBranchStatus("jj_deta",1);
  m_tree->SetBranchStatus("jj_dphi",1);
  m_tree->SetBranchStatus("met_tst_j1_dphi",1);
  m_tree->SetBranchStatus("met_tst_j2_dphi",1);
  m_tree->SetBranchStatus("met_tst_nolep_j1_dphi",1);
  m_tree->SetBranchStatus("met_tst_nolep_j2_dphi",1);
  m_tree->SetBranchStatus("met_tst_et",1);
  m_tree->SetBranchStatus("met_tst_nolep_et",1);
  m_tree->SetBranchStatus("met_tst_phi",1);
  m_tree->SetBranchStatus("met_tst_nolep_phi",1);
  m_tree->SetBranchStatus("met_cst_jet",1);
  m_tree->SetBranchStatus("ph_pointing_z",1);  
  m_tree->SetBranchStatus("mu_charge",1);
  m_tree->SetBranchStatus("basemu_charge",1);
  m_tree->SetBranchStatus("mu_pt",1);
  m_tree->SetBranchStatus("mu_phi",1);
  m_tree->SetBranchStatus("mu_eta",1);
  m_tree->SetBranchStatus("el_charge",1);
  m_tree->SetBranchStatus("baseel_charge",1);
  m_tree->SetBranchStatus("el_pt",1);
  m_tree->SetBranchStatus("el_phi",1);
  m_tree->SetBranchStatus("el_eta",1);
  m_tree->SetBranchStatus("ph_pt",1);
  m_tree->SetBranchStatus("ph_phi",1);
  m_tree->SetBranchStatus("ph_eta",1);
  m_tree->SetBranchStatus("jet_pt",1);
  m_tree->SetBranchStatus("jet_phi",1);
  m_tree->SetBranchStatus("jet_eta",1);
  m_tree->SetBranchStatus("jet_m",1);
  m_tree->SetBranchStatus("jet_timing",1);

  m_tree->SetBranchAddress("runNumber",&runNumber);
  m_tree->SetBranchAddress("randomRunNumber",&randomRunNumber);
  m_tree->SetBranchAddress("eventNumber",&eventNumber);
  m_tree->SetBranchAddress("averageIntPerXing", &averageIntPerXing);
  m_tree->SetBranchAddress("trigger_met", &trigger_met);
  m_tree->SetBranchAddress("trigger_met_encodedv2", &trigger_met_encodedv2);
  m_tree->SetBranchAddress("trigger_lep", &trigger_lep);
  m_tree->SetBranchAddress("lep_trig_match", &lep_trig_match);
  m_tree->SetBranchAddress("in_vy_overlap", &in_vy_overlap);
  m_tree->SetBranchAddress("passVjetsFilter", &passVjetsFilter);
  m_tree->SetBranchAddress("passVjetsFilterTauEl", &passVjetsFilterTauEl);
  m_tree->SetBranchAddress("passJetCleanTight", &passJetCleanTight);
  m_tree->SetBranchAddress("n_jet",&n_jet);
  m_tree->SetBranchAddress("n_bjet",&n_bjet);
  m_tree->SetBranchAddress("n_ph",&n_ph);
  m_tree->SetBranchAddress("n_ph_crackVetoCleaning",&n_ph_crackVetoCleaning);  
  m_tree->SetBranchAddress("n_el",&n_el);
  m_tree->SetBranchAddress("n_mu",&n_mu);
  m_tree->SetBranchAddress("n_el_w",&n_el_w);
  m_tree->SetBranchAddress("n_mu_w",&n_mu_w);
  m_tree->SetBranchAddress("n_baseel",&n_baseel);
  m_tree->SetBranchAddress("n_basemu",&n_basemu);
  m_tree->SetBranchAddress("n_el_baseline_noOR",&n_baseel_noOR);
  m_tree->SetBranchAddress("n_mu_baseline_noOR",&n_basemu_noOR);
  m_tree->SetBranchAddress("n_el_baseline_iso",&n_baseel_iso);
  m_tree->SetBranchAddress("n_mu_baseline_iso",&n_basemu_iso);
  if(doTMVA) m_tree->SetBranchAddress("tmva",&tmva);
  m_tree->SetBranchAddress("jj_mass",&jj_mass);
  m_tree->SetBranchAddress("jj_deta",&jj_deta);
  m_tree->SetBranchAddress("jj_dphi",&jj_dphi);
  m_tree->SetBranchAddress("met_tst_j1_dphi",&met_tst_j1_dphi);
  m_tree->SetBranchAddress("met_tst_j2_dphi",&met_tst_j2_dphi);
  m_tree->SetBranchAddress("met_tst_nolep_j1_dphi",&met_tst_nolep_j1_dphi);
  m_tree->SetBranchAddress("met_tst_nolep_j2_dphi",&met_tst_nolep_j2_dphi);
  m_tree->SetBranchAddress("met_tst_et",&met_tst_et);
  m_tree->SetBranchAddress("met_tst_nolep_et",&met_tst_nolep_et);
  m_tree->SetBranchAddress("met_tst_phi",&met_tst_phi);
  m_tree->SetBranchAddress("met_tst_nolep_phi",&met_tst_nolep_phi);
  m_tree->SetBranchAddress("met_cst_jet",&met_cst_jet);
  m_tree->SetBranchAddress("ph_pointing_z",&ph_pointing_z);  
  m_tree->SetBranchAddress("mu_charge",&mu_charge);
  m_tree->SetBranchAddress("basemu_charge",&basemu_charge);
  m_tree->SetBranchAddress("mu_pt",&mu_pt);
  m_tree->SetBranchAddress("el_charge",&el_charge);
  m_tree->SetBranchAddress("baseel_charge",&baseel_charge);
  m_tree->SetBranchAddress("el_pt",&el_pt);
  m_tree->SetBranchAddress("ph_pt",&ph_pt);
  m_tree->SetBranchAddress("jet_pt",&jet_pt);
  m_tree->SetBranchAddress("jet_timing",&jet_timing);
  m_tree->SetBranchAddress("mu_phi",&mu_phi);
  m_tree->SetBranchAddress("el_phi",&el_phi);
  m_tree->SetBranchAddress("ph_phi",&ph_phi);
  m_tree->SetBranchAddress("mu_eta",&mu_eta);
  m_tree->SetBranchAddress("el_eta",&el_eta);
  m_tree->SetBranchAddress("ph_eta",&ph_eta);
  m_tree->SetBranchAddress("jet_phi",&jet_phi);
  m_tree->SetBranchAddress("jet_eta",&jet_eta);
  m_tree->SetBranchAddress("jet_m",&jet_m);

  if(m_extraVars>0 || m_metdef>0){  
    m_tree->SetBranchStatus("met_soft_tst_et",1);
    m_tree->SetBranchStatus("met_tenacious_tst_et",1);
    m_tree->SetBranchStatus("met_tenacious_tst_phi",1);
    m_tree->SetBranchStatus("met_tenacious_tst_nolep_et",1);
    m_tree->SetBranchStatus("met_tenacious_tst_nolep_phi",1);
    //m_tree->SetBranchStatus("met_tighter_tst_et",1);
    m_tree->SetBranchStatus("met_tight_tst_et",1);
    m_tree->SetBranchStatus("jet_fjvt",1);
    if(m_binning==-1) m_tree->SetBranchStatus("jet_NTracks",1);
    m_tree->SetBranchStatus("baseel_pt",1);
    m_tree->SetBranchStatus("baseel_eta",1);
    m_tree->SetBranchStatus("baseel_phi",1);
    m_tree->SetBranchStatus("basemu_pt",1);
    m_tree->SetBranchStatus("basemu_eta",1);
    m_tree->SetBranchStatus("basemu_phi",1);

    m_tree->SetBranchAddress("met_soft_tst_et",        &met_soft_tst_et);
    m_tree->SetBranchAddress("met_tenacious_tst_et",   &met_tenacious_tst_et);
    m_tree->SetBranchAddress("met_tenacious_tst_phi",   &met_tenacious_tst_phi);
    m_tree->SetBranchAddress("met_tenacious_tst_nolep_et",   &met_tenacious_tst_nolep_et);
    m_tree->SetBranchAddress("met_tenacious_tst_nolep_phi",   &met_tenacious_tst_nolep_phi);
    m_tree->SetBranchAddress("met_tight_tst_et",       &met_tight_tst_et);
    //m_tree->SetBranchAddress("met_tighter_tst_et",     &met_tighter_tst_et);    
    m_tree->SetBranchAddress("jet_fjvt",            &jet_fjvt);
    if(m_binning==-1) m_tree->SetBranchAddress("jet_NTracks",         &jet_NTracks);
    m_tree->SetBranchAddress("baseel_pt",           &baseel_pt);
    m_tree->SetBranchAddress("baseel_eta",           &baseel_eta);
    m_tree->SetBranchAddress("baseel_phi",           &baseel_phi);
    m_tree->SetBranchAddress("basemu_pt",           &basemu_pt);
    m_tree->SetBranchAddress("basemu_eta",           &basemu_eta);
    m_tree->SetBranchAddress("basemu_phi",           &basemu_phi);
  }
  return StatusCode::SUCCESS;
}

double HFInputAlg::weightXETrigSF(const float met_pt, unsigned metRunNumber, int syst=0) {
  // 20.7 values
  //static const double p0 = 59.3407;
  //static const double p1 = 54.9134;
  // For MET tight
  //double p0 = 99.4255;
  //double p1 = 38.6145;
  // For MET Tenacious
  double p0 = 99.4255;
  double p1 = 38.6145;
  double e0 = 0.000784094;
  double e1 = 0.044;
  if(metRunNumber<=284484)                        { p0 = 110.396; p1 = 19.4147; e1 = 0.044; }  // 2015 xe70
  if(metRunNumber>284484 && metRunNumber<=302872) { p0 = 111.684; p1 = 19.147;  e1 = 0.04; }  // 2016 xe90
  if(metRunNumber>302872)                         { p0 = 68.8679; p1 = 54.0594; e1 = 0.044; }  // 2016 xe110 //p0 = 101.759; p1 = 36.5069;
  //if(325713<=metRunNumber && metRunNumber<=328393) { p0 = 86.6614; p1 = 49.8935; e1 = 0.05; } // 2017 xe90_pufit_L1XE50
  //if(329385<=metRunNumber && metRunNumber<=330470) { p0 = 103.780; p1 = 57.2547; e1 = 0.05; } // 2017 xe100_pufit_L1XE55
  //if(330857<=metRunNumber && metRunNumber<=331975) { p0 = 118.959; p1 = 32.2808; e1 = 0.05; } // 2017 xe110_pufit_L1XE55
  //if(331975< metRunNumber && metRunNumber<=341649) { p0 = 103.152; p1 = 38.6121; e1 = 0.05; } // 2017 xe110_pufit_L1XE50
  //if(350067> metRunNumber && metRunNumber>=348197) { p0 = 104.830; p1 = 38.5267; e1 = 0.05; } // 2018 xe110_xe70_L1XE50
  //if(350067<=metRunNumber && metRunNumber<=364292) { p0 = 107.509; p1 = 32.0065; e1 = 0.05; } // 2018 xe110_xe65_L1XE50
  if(325713<=metRunNumber && metRunNumber<=341649) { p0 = 118.959; p1 = 32.2808; e1 = 0.04; } // 2017 xe110_pufit_L1XE55
  if(364292>= metRunNumber && metRunNumber>=348197) { p0 = 104.830; p1 = 38.5267; e1 = 0.04; } // 2018 xe110_xe70_L1XE50

  // MET SFs for the sherpa KT merged samples
  if(mergeKTPTV){
    if(metRunNumber<=284484)                        { p0 = 74.08; p1 = 32.07; e1 = 0.044; }  // 2015 xe70
    if(metRunNumber>284484 && metRunNumber<=302872) { p0 = 80.72; p1 = 37.08;  e1 = 0.04; }  // 2016 xe90
    if(metRunNumber>302872)                         { p0 = 78.76; p1 = 34.62; e1 = 0.044; }  // 2016 xe110 //p0 = 101.759; p1 = 36.5069;
    if(325713<=metRunNumber && metRunNumber<=341649) { p0 = 62.3667; p1 = 54.946; e1 = 0.04; } // 2017 xe110_pufit_L1XE55
    if(364292>= metRunNumber && metRunNumber>=348197) { p0 = 74.018; p1 = 35.8145; e1 = 0.04; } // 2018 xe110_xe70_L1XE50
  }
  
  double x = met_pt / 1.0e3;
  if (x < 100) { return 0; }
  if (x > 240) { x = 240; }
  double sf = 0.5*(1+TMath::Erf((x-p0)/(TMath::Sqrt(2)*p1)));
  if(sf<0) sf=0.0;
  if(sf > 1.5) sf=1.5;

  // linear parameterization of the systematics
  if(syst==1){ // up variation
    if(x<210.0) sf+=((e0)*(150-x)+e1)*0.6;
    else sf=1.0;
  }else if(syst==2){ // down
    if(x<210.0)sf-=((e0)*(150-x)+e1)*0.6;
    else sf=1.0;
  }
  return sf;
}

float HFInputAlg::GetDPhi(const float phi1, const float phi2){
  float dphi = phi1-phi2;
  if ( dphi > M_PI ) {
    dphi -= 2.0*M_PI;
  } else if ( dphi <= -M_PI ) {
    dphi += 2.0*M_PI;
  }
  return dphi;
}
