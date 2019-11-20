// C/C++
#include <set>
#include <math.h>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <algorithm>

#include <sstream>

#ifdef ANP_CPU_PROFILER
#include <google/profiler.h>
#endif

// ROOT
#include "TDirectory.h"
#include "TH1.h"
#include "TFile.h"
#include "TLeaf.h"
#include "TTree.h"
#include "TChain.h"
#include "TStopwatch.h"
#include "TLorentzVector.h"
#include "TSystem.h"

// Local
#include "HInvPlot/UtilCore.h"
#include "HInvPlot/PassEvent.h"
#include "HInvPlot/ReadEvent.h"

using namespace std;
//*****************************************************************************
//
// Starting ReadEvent code
//
//*****************************************************************************

//-----------------------------------------------------------------------------
Msl::ReadEvent::AlgData::AlgData(const std::string &key):
  alg_key(key),
  pre_sel(0)
{
}

//-----------------------------------------------------------------------------
Msl::ReadEvent::ReadEvent():
  fSystName     ("Nominal"),
  fWeightSystName("Nominal"),
  fTMVAReader   (nullptr),
  fTMVAWeightPath(""),
  fMVAName      (""),
  fDebug        (false),
  fPrint        (false),
  fPrintEvent   (false),
  fMaxNEvent(-1),
  fLumi         (1.0),
  fBTagCut     (-10),
  fYear         (2016),
  fLoadBaseLep  (false),
  fOverlapPh    (false),
  fIsDDQCD      (false),
  genCutFlow    (0),
  procCutFlow0  (0),
  rawCutFlow    (0)
{
}

//-----------------------------------------------------------------------------
Msl::ReadEvent::~ReadEvent()
{
  if(fTMVAReader){ delete fTMVAReader; fTMVAReader = nullptr; }
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::Conf(const Registry &reg)
{
  evt_map.clear();
  //
  // Read configuration
  //
  reg.Get("ReadEvent::Name",          fName);
  reg.Get("ReadEvent::CutFlowFile",   fCutFlowFile);
  reg.Get("ReadEvent::RawFlowFile",   fRawFlowFile);
  reg.Get("ReadEvent::METChoice",     fMETChoice);
  reg.Get("ReadEvent::Trees",         fTrees);
  reg.Get("ReadEvent::Files",         fFiles);
  reg.Get("ReadEvent::MaxNEvent",     fMaxNEvent);

  reg.Get("ReadEvent::TMVAWeightPath",     fTMVAWeightPath);

  reg.Get("ReadEvent::JetVetoPt",     fJetVetoPt);
  reg.Get("ReadEvent::LoadBaseLep",   fLoadBaseLep);
  reg.Get("ReadEvent::OverlapPh",     fOverlapPh);
  reg.Get("ReadEvent::mergeExt",      fMergeExt);
  reg.Get("ReadEvent::mergePTV",      fMergePTV);
  reg.Get("ReadEvent::BTagCut",       fBTagCut);
  reg.Get("ReadEvent::noVjWeight",      fnoVjWeight);
  reg.Get("ReadEvent::Year",          fYear);  

  reg.Get("ReadEvent::Debug",         fDebug        = false);
  reg.Get("ReadEvent::Print",         fPrint        = false);
  reg.Get("ReadEvent::PrintEvent",    fPrintEvent   = false);
  reg.Get("ReadEvent::MCEventCount",  fMCEventCount = false);
  reg.Get("ReadEvent::Lumi",          fLumi = 1.0);
  fDir="";

  if(fTMVAWeightPath!=""){
    fTMVAReader = new TMVA::Reader( "!Color:!Silent" );
    fMVAName =  "BDT method";
    for(unsigned i=0; i<7; ++i) fTMVAVars.push_back(0.0);
    fTMVAReader->AddVariable("jj_mass", &fTMVAVars[0]);
    fTMVAReader->AddVariable("jj_dphi", &fTMVAVars[1]);
    fTMVAReader->AddVariable("jj_deta", &fTMVAVars[2]);
    fTMVAReader->AddVariable("met_tst_et", &fTMVAVars[3]);
    fTMVAReader->AddVariable("met_soft_tst_et", &fTMVAVars[4]);
    fTMVAReader->AddVariable("jet1_pt", &fTMVAVars[5]);
    fTMVAReader->AddVariable("jet2_pt", &fTMVAVars[6]);
    fTMVAReader->BookMVA( fMVAName, fTMVAWeightPath);
  }

  // set met phi
  fMETChoice_phi = fMETChoice;
  fMETChoice_phi.replace(fMETChoice_phi.end()-2, fMETChoice_phi.end(),"phi");
  fMETChoice_nolep = fMETChoice;
  fMETChoice_nolep_phi = fMETChoice_phi;
  fMETChoice_nolep.replace(fMETChoice_nolep.find("_tst"), 4, "_tst_nolep");
  fMETChoice_nolep_phi.replace(fMETChoice_nolep_phi.find("_tst"), 4, "_tst_nolep");

  std::vector<std::string> mcids, samples;
  reg.Get("ReadEvent::MCIDs",   mcids);
  reg.Get("ReadEvent::Samples", samples);
  fSampleMap.clear();
  for(unsigned iID=0; iID<mcids.size(); ++iID){
    fSampleMap[std::stoi(mcids.at(iID))]=samples.at(iID);
  }
  //
  // Make list of additional input variables (from tree)
  //
  AddVars("ReadEvent::InputVars", reg);

  //
  // Get Mva::Var for conversion to MeV
  //
  fVarMeV = Mva::ReadVars(reg, "ReadEvent::VarMeV", GetAlgName());


  cout << "   Number of input var(s): " << fVarVec.size() << endl;

  for(VarVec::const_iterator it = fVarVec.begin(); it != fVarVec.end(); ++it) {
    cout << "      " << Mva::Convert2Str(it->var) << endl;
  }

  cout << "   Number of MeV var(s): " << fVarMeV.size() << endl;

  for(unsigned i = 0; i < fVarMeV.size(); ++i) {
    cout << "      " << Mva::Convert2Str(fVarMeV.at(i)) << endl;
  }

  // declare vectors
  //
  el_charge  = new std::vector<float>();
  el_pt      = new std::vector<float>();
  el_eta     = new std::vector<float>();
  el_phi     = new std::vector<float>();
  mu_charge  = new std::vector<float>();
  mu_pt      = new std::vector<float>();
  mu_eta     = new std::vector<float>();
  mu_phi     = new std::vector<float>();
  tau_charge  = new std::vector<float>();
  tau_pt      = new std::vector<float>();
  tau_eta     = new std::vector<float>();
  tau_phi     = new std::vector<float>();
  jet_timing = new std::vector<float>();
  jet_pt     = new std::vector<float>();
  jet_eta    = new std::vector<float>();
  jet_phi    = new std::vector<float>();
  jet_m      = new std::vector<float>();
  jet_jvt    = new std::vector<float>();
  jet_fjvt   = new std::vector<float>();
  jet_btag_weight    = new std::vector<float>();
  jet_TrackWidth   = new std::vector<float>();
  jet_NTracks   = new std::vector<unsigned short>();
  jet_PartonTruthLabelID   = new std::vector<float>();
  truth_el_pt  = new std::vector<float>();
  truth_el_eta = new std::vector<float>();
  truth_el_phi = new std::vector<float>();
  truth_mu_pt  = new std::vector<float>();
  truth_mu_eta = new std::vector<float>();
  truth_mu_phi = new std::vector<float>();
  truth_tau_pt  = new std::vector<float>();
  truth_tau_eta = new std::vector<float>();
  truth_tau_phi = new std::vector<float>();
  truth_jet_pt  = new std::vector<float>();
  truth_jet_eta = new std::vector<float>();
  truth_jet_phi = new std::vector<float>();
  basemu_pt     = new std::vector<float>();
  basemu_charge = new std::vector<int>();
  basemu_eta    = new std::vector<float>();
  basemu_phi    = new std::vector<float>();
  basemu_ptvarcone20    = new std::vector<float>();
  basemu_ptvarcone30    = new std::vector<float>();
  basemu_topoetcone20   = new std::vector<float>();
  baseel_pt       = new std::vector<float>();
  baseel_charge   = new std::vector<int>();
  baseel_eta      = new std::vector<float>();
  baseel_phi      = new std::vector<float>();
  baseel_ptvarcone20    = new std::vector<float>();
  baseel_ptvarcone30    = new std::vector<float>();
  baseel_topoetcone20    = new std::vector<float>();
  ph_pt     = new std::vector<float>();
  ph_eta    = new std::vector<float>();
  ph_phi    = new std::vector<float>();

#ifdef ANP_CPU_PROFILER
  string profile_file = "cpu-profile-readevent";

  log() << "Exec - compiled with perftools:" << endl
	<< "   ProfilerStart(" << profile_file << ")" << endl;

  ProfilerStart(profile_file.c_str());
#endif
}

/*--------------------------------------------------------------------------------*/
// Init is called when TTree or TChain is attached
/*--------------------------------------------------------------------------------*/
void Msl::ReadEvent::Init(TTree* tree)
{
  // Init
  for(unsigned i=0; i<fVarVec.size(); ++i)
    fVarVec.at(i).SetVarBranch(tree);
  vjWeight=1.0;
  xeSFTrigWeight=1.0;
  xeSFTrigWeight__1up=1.0;
  xeSFTrigWeight__1down=1.0;
  xeSFTrigWeight_nomu=1.0;
  xeSFTrigWeight_nomu__1up=1.0;
  xeSFTrigWeight_nomu__1down=1.0;
  tree->SetBranchStatus("vjWeight", 1);
  tree->SetBranchAddress("vjWeight", &vjWeight);
  tree->SetBranchAddress("xeSFTrigWeight",&xeSFTrigWeight);
  tree->SetBranchAddress("xeSFTrigWeight_nomu",&xeSFTrigWeight_nomu);
  if(fWeightSystName=="Nominal" || fIsDDQCD){
    tree->SetBranchAddress("w",        &fWeight);
    // xe SF runs with the weight syst set to Nominal
    if(fSystName=="Nominal"){
      tree->SetBranchAddress("xeSFTrigWeight__1up",&xeSFTrigWeight__1up);
      tree->SetBranchAddress("xeSFTrigWeight__1down",&xeSFTrigWeight__1down);
      tree->SetBranchAddress("xeSFTrigWeight_nomu__1up",&xeSFTrigWeight_nomu__1up);
      tree->SetBranchAddress("xeSFTrigWeight_nomu__1down",&xeSFTrigWeight_nomu__1down);
    }
  }
  else{
    // add the systematics weights to the nominal
    bool found_weight_syst=false;
    TObjArray *var_list = tree->GetListOfBranches();
    for(unsigned a=0; a<unsigned(var_list->GetEntries()); ++a) {
      TString var_name = var_list->At(a)->GetName();
      if(var_name.Contains("__1up") || var_name.Contains("__1down")){
	tree->SetBranchStatus(var_name, 1);
	if(var_name.Contains(fWeightSystName)){
	  tree->SetBranchAddress(var_name, &fWeight);
	  found_weight_syst=true;
	  break;
	}
      }
    }
    if(!found_weight_syst) std::cout << "ERROR - Failed to find weight for " << fWeightSystName << std::endl;
  }
  tree->SetBranchAddress("runNumber",&fRunNumber);
  tree->SetBranchAddress("randomRunNumber",&fRandomRunNumber);
  tree->SetBranchAddress("eventNumber",&fEventNumber);
  tree->SetBranchAddress("el_charge",&el_charge);
  tree->SetBranchAddress("el_pt",    &el_pt);
  tree->SetBranchAddress("el_eta",   &el_eta);
  tree->SetBranchAddress("el_charge",&el_charge);
  tree->SetBranchAddress("el_pt",    &el_pt);
  tree->SetBranchAddress("el_eta",   &el_eta);
  tree->SetBranchAddress("el_phi",   &el_phi);
  tree->SetBranchAddress("mu_charge",&mu_charge);
  tree->SetBranchAddress("mu_pt",    &mu_pt);
  tree->SetBranchAddress("mu_eta",   &mu_eta);
  tree->SetBranchAddress("mu_phi",   &mu_phi);
  tree->SetBranchAddress("tau_charge",&tau_charge);
  tree->SetBranchAddress("tau_pt",    &tau_pt);
  tree->SetBranchAddress("tau_eta",   &tau_eta);
  tree->SetBranchAddress("tau_phi",   &tau_phi);
  tree->SetBranchAddress("jet_timing",&jet_timing);
  tree->SetBranchAddress("jet_pt",    &jet_pt);
  tree->SetBranchAddress("jet_m",     &jet_m);
  tree->SetBranchAddress("jet_eta",   &jet_eta);
  tree->SetBranchAddress("jet_phi",   &jet_phi);
  tree->SetBranchAddress("jet_jvt",   &jet_jvt);
  tree->SetBranchAddress("jet_fjvt",   &jet_fjvt);
  tree->SetBranchAddress("jet_btag_weight",   &jet_btag_weight);
  tree->SetBranchAddress("jet_TrackWidth",   &jet_TrackWidth);
  tree->SetBranchAddress("jet_NTracks",   &jet_NTracks);
  tree->SetBranchAddress("jet_PartonTruthLabelID",   &jet_PartonTruthLabelID);

  if(fisMC){
    tree->SetBranchAddress("truth_jet_pt",    &truth_jet_pt);
    tree->SetBranchAddress("truth_jet_eta",   &truth_jet_eta);
    tree->SetBranchAddress("truth_jet_phi",   &truth_jet_phi);
    tree->SetBranchAddress("truth_tau_pt",    &truth_tau_pt);
    tree->SetBranchAddress("truth_tau_eta",   &truth_tau_eta);
    tree->SetBranchAddress("truth_tau_phi",   &truth_tau_phi);
    tree->SetBranchAddress("truth_el_pt",    &truth_el_pt);
    tree->SetBranchAddress("truth_el_eta",   &truth_el_eta);
    tree->SetBranchAddress("truth_el_phi",   &truth_el_phi);
    tree->SetBranchAddress("truth_mu_pt",    &truth_mu_pt);
    tree->SetBranchAddress("truth_mu_eta",   &truth_mu_eta);
    tree->SetBranchAddress("truth_mu_phi",   &truth_mu_phi);
  }
  tree->SetBranchAddress("baseel_pt",    &baseel_pt);
  tree->SetBranchAddress("baseel_charge",    &baseel_charge);
  tree->SetBranchAddress("baseel_eta",   &baseel_eta);
  tree->SetBranchAddress("baseel_phi",   &baseel_phi);
  tree->SetBranchAddress("baseel_ptvarcone20",   &baseel_ptvarcone20);
  tree->SetBranchAddress("baseel_ptvarcone30",   &baseel_ptvarcone30);
  tree->SetBranchAddress("baseel_topoetcone20",   &baseel_topoetcone20);
  tree->SetBranchAddress("basemu_pt",    &basemu_pt);
  tree->SetBranchAddress("basemu_charge",    &basemu_charge);
  tree->SetBranchAddress("basemu_eta",   &basemu_eta);
  tree->SetBranchAddress("basemu_phi",   &basemu_phi);
  tree->SetBranchAddress("basemu_ptvarcone20",   &basemu_ptvarcone20);
  tree->SetBranchAddress("basemu_ptvarcone30",   &basemu_ptvarcone30);
  tree->SetBranchAddress("basemu_topoetcone20",   &basemu_topoetcone20);
  // load photons
  tree->SetBranchAddress("ph_pt",    &ph_pt);
  tree->SetBranchAddress("ph_eta",   &ph_eta);
  tree->SetBranchAddress("ph_phi",   &ph_phi);
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::AddCommonAlg(IExecAlg *alg)
{
  if(!alg) {
    log() << "AddCommonAlg - ERROR: null IExecAlg pointer" << endl;
    exit(1);
  }

  if(MatchAlg(alg)) {
    log() << "AddCommonAlg - ERROR: duplicate IExecAlg pointer" << endl;
    exit(1);
  }
  else {
    fAlgCommon.push_back(alg);
    fAlgAll   .push_back(alg);
  }
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::AddNormalAlg(const std::string &key, IExecAlg *alg)
{
  if(!alg) {
    log() << "AddNormalAlg - ERROR: null IExecAlg pointer: " << key << endl;
    exit(1);
  }

  if(MatchAlg(alg)) {
    log() << "AddNormalAlg - ERROR: duplicate IExecAlg pointer: " << key << endl;
    exit(1);
  }

  //
  // Find/make algorithm data
  //
  AlgList::iterator ialg = std::find(fAlgNormal.begin(), fAlgNormal.end(), AlgData(key));

  if(ialg == fAlgNormal.end()) {
    //
    // Make new alg sequence
    //
    ialg = fAlgNormal.insert(fAlgNormal.end(), AlgData(key));
  }

  //
  // Save algorithm pointer
  //
  ialg->alg_vec.push_back(alg);
  fAlgAll.push_back(alg);
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::AddPreSelAlg(const std::string &key, IExecAlg *alg)
{
  if(!alg) {
    log() << "AddPreSelAlg - ERROR: null IExecAlg pointer: " << key << endl;
    exit(1);
  }

  //
  // Find/make algorithm data
  //
  AlgList::iterator ialg = std::find(fAlgNormal.begin(), fAlgNormal.end(), AlgData(key));

  if(ialg == fAlgNormal.end()) {
    //
    // Make new alg sequence
    //
    ialg = fAlgNormal.insert(fAlgNormal.end(), AlgData(key));
  }

  //
  // Check for existing pre-selection algorithm pointer
  //
  if(ialg->pre_sel) {
    log() << "AddPreSelAlg - already hold valid IExecAlg pointer: " << key << endl;
    exit(1);
  }

  //
  // Save pre-selection algorithm
  //
  ialg->pre_sel = alg;

  if(!MatchAlg(alg)) {
    fAlgPreSel.push_back(alg);
    fAlgAll   .push_back(alg);
  }
}

//-----------------------------------------------------------------------------
bool Msl::ReadEvent::MatchAlg(IExecAlg *alg) const
{
  //
  // Check if we already have this algorithm pointer
  //
  return std::find(fAlgAll.begin(), fAlgAll.end(), alg) != fAlgAll.end();
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::PrintAlgs(std::ostream &os) const
{
  os << "------------------------------------------------------------------" << endl
     << GetAlgName() << " - print algs..." << endl;

  //
  // Print common algorithm(s)
  //
  os << "   Print " << setw(3) << fAlgCommon.size() << " top common algorithm(s): " << endl;
  for(AlgVec::const_iterator it = fAlgCommon.begin(); it != fAlgCommon.end(); ++it) {
    os << "      " << (*it)->GetAlgName() << endl;
  }

  //
  // Print pre-selection algorithm(s)
  //
  os << "   Print " << setw(3) << fAlgPreSel.size() << " pre-select algorithm(s): " << endl;
  for(AlgVec::const_iterator it = fAlgPreSel.begin(); it != fAlgPreSel.end(); ++it) {
    os << "      " << (*it)->GetAlgName() << endl;
  }

  //
  // Print normal algorithm(s)
  //
  os << "   Print " << fAlgNormal.size() << " sequence key(s): " << endl;

  unsigned aw = 0;
  for(AlgList::const_iterator it = fAlgNormal.begin(); it != fAlgNormal.end(); ++it) {
    aw = std::max(aw, unsigned(it->alg_key.size()));
    os << "      " << it->alg_key << endl;
  }

  for(AlgList::const_iterator it = fAlgNormal.begin(); it != fAlgNormal.end(); ++it) {
    const string name = it->alg_key;

    os << "   " << setw(aw) << std::left << setfill(' ') << name
       << ": contains " << setw(2) << it->alg_vec.size() << " algorithm(s):" << endl;

    for(unsigned ialg = 0; ialg < it->alg_vec.size(); ++ialg) {
      os << "      " << it->alg_vec.at(ialg)->GetAlgName() << endl;
    }
  }
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::RunConfForAlgs()
{
  //
  // Print list of all algs
  //
  PrintAlgs();

  //
  // Configure common algorithm(s)
  //
  cout << "------------------------------------------------------------------" << endl
       << GetAlgName() << " - configure " << fAlgCommon.size() << " top common algorithm(s)" << endl;

  for(AlgVec::iterator it = fAlgCommon.begin(); it != fAlgCommon.end(); ++it) {
    (*it)->RunAlgConf();
  }

  //
  // Configure pre-selection algorithm(s)
  //
  cout << "------------------------------------------------------------------" << endl
       << GetAlgName() << " - configure " << fAlgPreSel.size() << " pre-select algorithm(s)" << endl;

  for(AlgVec::iterator it = fAlgPreSel.begin(); it != fAlgPreSel.end(); ++it) {
    (*it)->RunAlgConf();
  }

  //
  // Configure normal algorithm(s)
  //
  for(AlgList::const_iterator it = fAlgNormal.begin(); it != fAlgNormal.end(); ++it) {
    //
    // Configure one sequence
    //
    cout << "------------------------------------------------------------------" << endl
	  << GetAlgName() << " - configure sequence key: " << it->alg_key << endl;

    for(unsigned ialg = 0; ialg < it->alg_vec.size(); ++ialg) {
      it->alg_vec.at(ialg)->RunAlgConf();
    }
  }
}

//--------------------------------------------------------------------------------------
void Msl::ReadEvent::Read(const std::string &path)
{
  //
  // Open input file
  //
  TStopwatch timer;
  timer.Start();

  TFile *file = 0;
  if(path.find("/eos/atlas") != string::npos) { file = TFile::Open(("root://eosatlas/"+path).c_str(), "READ"); }
  else { file = TFile::Open(path.c_str(), "READ"); }

  if(!file || !(file -> IsOpen())) {
    log() << "Read - failed to open ROOT file: " << path << endl;
    return;
  }

  //
  // Extract TDirectory if requested and find TTree
  //
  TDirectory *dir = file;

  if(!fDir.empty()) {
    dir = dynamic_cast<TDirectory *>(file->Get(fDir.c_str()));
  }

  if(!dir) {
    log() << "Read - missing input TDirectory:" << endl
	  << "   path: " << path << endl
	  << "   dir:  " << fDir << endl;

    file->Close();
    return;
  }

  //
  // Process common ntuples
  //
  cout << "------------------------------------------------------------------" << endl;
  log() << "Read - process new file: "                         << endl
	<< "   path:      " << path                            << endl;
  //
  // Read events from tree(s) and call sub-algorithms for processing
  //
  // setting up auto discovery of trees
  bool autoDiscovery=false;
  if(fTrees.size()==0){
    for(const auto &key: *dir->GetListOfKeys()){
      if(fTreesMap.find(std::string(key->GetName()))==fTreesMap.end()){ // remove duplicate trees if they appear
	fTrees.push_back(std::string(key->GetName()));
	fTreesMap.insert(std::string(key->GetName()));
	std::cout << "Tree Name: " << key->GetName() << std::endl;
      }
    }
    autoDiscovery=true;
  }

  for(unsigned i = 0; i < fTrees.size(); ++i) {

    TTree *rtree = dynamic_cast<TTree *>(dir->Get(fTrees.at(i).c_str()));
    if(!rtree) {
      if(fPrint){
      log() << "Read - WARNING - could not find input TTree: "
	    << fTrees.at(i).c_str() << endl;
      }
      continue;
    }

    //
    // Identify the systematic type
    //
    fIsDDQCD=(fTrees.at(i).find("QCDDD")!=std::string::npos); // QCDDD
    if(fTrees.at(i).find(fSystName)==std::string::npos && !fIsDDQCD) continue;

    log() << "Read - Running systematic: " << fSystName << " on tree: " << fTrees.at(i) <<std::endl;

    //
    // Read common ntuples
    //
    std::string treeName = std::string(rtree->GetName());
    fisMC = (treeName.find("data")==std::string::npos);
    fIsDDQCD=(treeName.find("QCDDDNominal")!=std::string::npos); // QCDDD
    Init(rtree);
    ReadTree(rtree); // Processes the events

  }
  file->Close();
  //
  // remove the trees afterward to search the next file
  //
  if(autoDiscovery){  fTrees.clear(); fTreesMap.clear(); }
  log() << "Read - processing time: " << Msl::PrintResetStopWatch(timer) << endl;
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::ReadTree(TTree *rtree)
{
  //
  // Process events and fill the event data structure
  //
  Event *event = new Event();

  //
  // Read tree
  //
  int nevent = rtree->GetEntries();
  if(fMaxNEvent > 0) {
    nevent = std::min<int>(fMaxNEvent, rtree->GetEntries());
  }

  // identify the data based upon the tree name
  std::string treeName = std::string(rtree->GetName());
  fisMC = (treeName.find("data")==std::string::npos);

  Event alg_evt;

  // vars to skip loading in QCD
  std::set<Mva::Var> fSkipVarsQCD;
  fSkipVarsQCD.insert(Mva::met_tenacious_tst_nolep_et);
  fSkipVarsQCD.insert(Mva::met_tenacious_tst_nolep_phi);
  fSkipVarsQCD.insert(Mva::bcid);
  fSkipVarsQCD.insert(Mva::BCIDDistanceFromFront);
  fSkipVarsQCD.insert(Mva::lb);
  fSkipVarsQCD.insert(Mva::n_mu_w);
  fSkipVarsQCD.insert(Mva::n_el_w);
  fSkipVarsQCD.insert(Mva::n_mu_baseline_noOR);
  fSkipVarsQCD.insert(Mva::lep_trig_match);
  fSkipVarsQCD.insert(Mva::truth_jj_deta);  
  fSkipVarsQCD.insert(Mva::truth_jj_dphi);  
  fSkipVarsQCD.insert(Mva::truth_jj_mass);  
  fSkipVarsQCD.insert(Mva::truth_j1_pt);  
  fSkipVarsQCD.insert(Mva::truth_j2_pt);  

  for(int i = 0; i < nevent; i++) {
    //
    // Clear event
    //
    event->Clear();

    // read in tree
    rtree->GetEntry(i);


    if(fRunNumber==-123) fIsDDQCD=true;

    // Fill event
    for(unsigned a=0; a<fVarVec.size(); ++a){
      if(fIsDDQCD && fSkipVarsQCD.find(fVarVec.at(a).var)!=fSkipVarsQCD.end()) continue;//skip missing vars in QCD
      event->AddVar(fVarVec.at(a).var, fVarVec.at(a).GetVal());
    }

    if(fIsDDQCD){
      event->RepVar(Mva::n_mu_w, 0);
      event->RepVar(Mva::n_el_w, 0);
      event->RepVar(Mva::n_mu_baseline_noOR, 0);
      event->RepVar(Mva::lep_trig_match, 0);
    }

    event->RunNumber = fRunNumber;
    event->RandomRunNumber = fRandomRunNumber;
    event->EventNumber = fEventNumber;
    event->isMC = fisMC;
    // identify the sample
    if(!fisMC){
      event->sample = Mva::kData;
      if(!fMCEventCount) event->SetWeight(fWeight);
      else event->SetWeight(1.0);
    }else{
      if(!fMCEventCount) {
        if(fnoVjWeight) event->SetWeight((fWeight*fLumi/vjWeight)); // assume vjweight is already applied to the nominal weight
        else event->SetWeight(fWeight*fLumi);
      }
      else  event->SetWeight(1.0);
      if(fIsDDQCD) event->SetWeight(fWeight);
      if(!fIsDDQCD && fCurrRunNumber!=fRunNumber){
	if(fSampleMap.find(fRunNumber)==fSampleMap.end()){
	  log() << "ERROR - please define sample in Input.py" << fRunNumber << std::endl;
	  event->sample = Mva::kNone;
	}else{
	  event->sample = Mva::Convert2Sample(fSampleMap.find(fRunNumber)->second);
	  fCurrSample = event->sample;
	  fCurrRunNumber=fRunNumber;
	  if(fDebug) std::cout << "sample: " << event->sample << std::endl;
	}
      }else{
	event->sample = fCurrSample;
      }
      if(fIsDDQCD) event->sample=Mva::kQCD;
    }
    // Load XS trigger SF
    event->RepVar(Mva::xeSFTrigWeight,        xeSFTrigWeight);
    event->RepVar(Mva::xeSFTrigWeight__1up,   xeSFTrigWeight__1up);
    event->RepVar(Mva::xeSFTrigWeight__1down, xeSFTrigWeight__1down);
    event->RepVar(Mva::xeSFTrigWeight_nomu,        xeSFTrigWeight_nomu);
    event->RepVar(Mva::xeSFTrigWeight_nomu__1up,   xeSFTrigWeight_nomu__1up);
    event->RepVar(Mva::xeSFTrigWeight_nomu__1down, xeSFTrigWeight_nomu__1down);

    if(fLoadBaseLep && false){
      // Fill Electrons with the baseline electrons for this looser lepton selection
      for(unsigned iEle=0; iEle<baseel_pt->size(); ++iEle){
	RecParticle new_ele;
	new_ele.pt  = baseel_pt->at(iEle)/1.0e3;
	new_ele.eta = baseel_eta->at(iEle);
	new_ele.phi = baseel_phi->at(iEle);
	new_ele.m   = 0.000511;
	new_ele.AddVar(Mva::charge,baseel_charge->at(iEle));
	if(baseel_ptvarcone20 && baseel_ptvarcone20->size()>iEle) new_ele.AddVar(Mva::ptvarcone20,baseel_ptvarcone20->at(iEle)/baseel_pt->at(iEle));
	if(baseel_ptvarcone30 && baseel_ptvarcone30->size()>iEle) new_ele.AddVar(Mva::ptvarcone30,baseel_ptvarcone30->at(iEle)/baseel_pt->at(iEle));
	if(baseel_topoetcone20 && baseel_topoetcone20->size()>iEle) new_ele.AddVar(Mva::topoetcone20,baseel_topoetcone20->at(iEle)/baseel_pt->at(iEle));
	event->electrons.push_back(new_ele);
      }

      // Fill Muons
      for(unsigned iMuo=0; iMuo<basemu_pt->size(); ++iMuo){
	RecParticle new_muo;
	new_muo.pt  = basemu_pt->at(iMuo)/1.0e3;
	new_muo.eta = basemu_eta->at(iMuo);
	new_muo.phi = basemu_phi->at(iMuo);
	new_muo.m   = 0.10566;
	new_muo.AddVar(Mva::charge,basemu_charge->at(iMuo));
	if(basemu_ptvarcone20 && basemu_ptvarcone20->size()>iMuo) new_muo.AddVar(Mva::ptvarcone20,basemu_ptvarcone20->at(iMuo)/basemu_pt->at(iMuo));
	if(basemu_ptvarcone30 && basemu_ptvarcone30->size()>iMuo) new_muo.AddVar(Mva::ptvarcone30,basemu_ptvarcone30->at(iMuo)/basemu_pt->at(iMuo));
	if(basemu_topoetcone20 && basemu_topoetcone20->size()>iMuo) new_muo.AddVar(Mva::topoetcone20,basemu_topoetcone20->at(iMuo)/basemu_pt->at(iMuo));
	event->muons.push_back(new_muo);
      }
    }else{
      // Fill Electrons
      for(unsigned iEle=0; iEle<el_pt->size(); ++iEle){
	RecParticle new_ele;
	new_ele.pt  = el_pt->at(iEle)/1.0e3;
	new_ele.eta = el_eta->at(iEle);
	new_ele.phi = el_phi->at(iEle);
	new_ele.m   = 0.000511;
	new_ele.AddVar(Mva::charge,el_charge->at(iEle));
	event->electrons.push_back(new_ele);
      }

      // Fill Muons
      for(unsigned iMuo=0; iMuo<mu_pt->size(); ++iMuo){
	RecParticle new_muo;
	new_muo.pt  = mu_pt->at(iMuo)/1.0e3;
	new_muo.eta = mu_eta->at(iMuo);
	new_muo.phi = mu_phi->at(iMuo);
	new_muo.m   = 0.10566;
	new_muo.AddVar(Mva::charge,mu_charge->at(iMuo));
	event->muons.push_back(new_muo);
      }
    }

    // Fill Taus
    for(unsigned iTau=0; iTau<tau_pt->size(); ++iTau){
      RecParticle new_tau;
      new_tau.pt  = tau_pt->at(iTau)/1.0e3;
      new_tau.eta = tau_eta->at(iTau);
      new_tau.phi = tau_phi->at(iTau);
      new_tau.m   = 1.777;
      //new_tau.AddVar(Mva::charge,tau_charge->at(iTau));
      event->taus.push_back(new_tau);
    }
    event->AddVar(Mva::n_tau,event->taus.size());

    // Fill Jets
    unsigned nJet=0;
    unsigned nJet_fwd=0;
    unsigned nJet_fwdj=0;
    unsigned nJet_fwdj30=0;
    unsigned nJet_fwdj40=0;
    unsigned nJet_fwdj50=0;
    unsigned nJet_cen=0;
    unsigned nJet_cenj=0;
    unsigned nJet_cenj30=0;
    unsigned nJet_cenj40=0;
    unsigned nJet_cenj50=0;
    //unsigned nJet30=0;
    //unsigned nJet40=0;
    for(unsigned iJet=0; iJet<jet_pt->size(); ++iJet){
      RecParticle new_jet;
      new_jet.pt  = jet_pt->at(iJet)/1.0e3;
      if(jet_m && jet_m->size()>iJet) new_jet.m   = jet_m->at(iJet)/1.0e3;
      new_jet.eta = jet_eta->at(iJet);
      new_jet.phi = jet_phi->at(iJet);
      new_jet.AddVar(Mva::timing,jet_timing->at(iJet));
      if(jet_btag_weight && jet_btag_weight->size()>iJet) new_jet.AddVar(Mva::jetBtagWeight,jet_btag_weight->at(iJet));
      if(jet_TrackWidth && jet_TrackWidth->size()>iJet) new_jet.AddVar(Mva::jetTrackWidth,jet_TrackWidth->at(iJet));
      if(jet_NTracks && jet_NTracks->size()>iJet) new_jet.AddVar(Mva::jetNTracks,jet_NTracks->at(iJet));
      if(jet_PartonTruthLabelID && jet_PartonTruthLabelID->size()>iJet) new_jet.AddVar(Mva::jetPartonTruthLabelID,jet_PartonTruthLabelID->at(iJet));

      if(jet_jvt && jet_jvt->size()>iJet){
	float jvt = jet_jvt->at(iJet);
	if(fabs(new_jet.eta)>2.5) jvt=jvt<0? jvt : -0.15;
	if(fabs(new_jet.pt)>120.0) jvt=-0.2;
	new_jet.AddVar(Mva::jvt,jvt);
      }
      if(jet_fjvt && jet_fjvt->size()>iJet)new_jet.AddVar(Mva::fjvt,jet_fjvt->at(iJet));
      if(jet_pt->at(iJet)>fJetVetoPt) ++nJet;
      event->jets.push_back(new_jet);
    }

    TLorentzVector tmp;
    const TLorentzVector j1v = event->jets.at(0).GetLVec();
    const TLorentzVector j2v = event->jets.at(1).GetLVec();
    float maxCentrality = -9999.0;
    float avgCentrality = 0.0;
    float maxmj3_over_mjj = -9999.0;
    float avgmj3_over_mjj = 0.0;
    for(unsigned iJet=2; iJet<event->jets.size(); ++iJet){
      tmp=event->jets.at(iJet).GetLVec();
      float centrality = exp(-4.0/std::pow(event->GetVar(Mva::jj_deta),2) * std::pow(tmp.Eta() - (j1v.Eta()+j2v.Eta())/2.0,2));
      if(centrality>maxCentrality) maxCentrality = centrality;
      avgCentrality+=centrality;

      float mj1 =  (tmp+j1v).M();
      float mj2 =  (tmp+j2v).M();
      float tmp_maxmj3_over_mjj = (1000.0*std::min(mj1,mj2)/event->GetVar(Mva::jj_mass));
      if(maxmj3_over_mjj<tmp_maxmj3_over_mjj) maxmj3_over_mjj = tmp_maxmj3_over_mjj;
      avgmj3_over_mjj+=tmp_maxmj3_over_mjj;
    }
    event->AddVar(Mva::maxCentrality, maxCentrality);
    if(event->jets.size()-2>0) avgCentrality/=float(event->jets.size()-2);
    event->AddVar(Mva::avgCentrality, avgCentrality);
    float jetPt3=-9999.0; if(event->jets.size()>2) jetPt3 = event->jets.at(2).pt;
    event->AddVar(Mva::jetPt3, jetPt3);
    event->AddVar(Mva::maxmj3_over_mjj, maxmj3_over_mjj);
    if(event->jets.size()-2>0) avgmj3_over_mjj/=float(event->jets.size()-2);
    event->AddVar(Mva::avgmj3_over_mjj, avgmj3_over_mjj);

    // forward jets relative to the leading two jets
    float maxPosEta=0.0, maxNegEta=0.0;
    unsigned nBjet=0;
    if(event->jets.size()>1){
      maxPosEta=std::max(event->jets.at(0).eta,event->jets.at(1).eta);
      maxNegEta=std::min(event->jets.at(0).eta,event->jets.at(1).eta);
    }
    for(unsigned iJet=2; iJet<event->jets.size(); ++iJet){
      if((event->jets.at(iJet).eta>maxPosEta) || (event->jets.at(iJet).eta<maxNegEta)) ++nJet_fwdj;
      if(event->jets.at(iJet).pt>30.0 && (event->jets.at(iJet).eta>maxPosEta || event->jets.at(iJet).eta<maxNegEta)) ++nJet_fwdj30;
      if(event->jets.at(iJet).pt>40.0 && (event->jets.at(iJet).eta>maxPosEta || event->jets.at(iJet).eta<maxNegEta)) ++nJet_fwdj40;
      if(event->jets.at(iJet).pt>50.0 && (event->jets.at(iJet).eta>maxPosEta || event->jets.at(iJet).eta<maxNegEta)) ++nJet_fwdj50;
      if(fabs(event->jets.at(iJet).eta)>2.5) ++nJet_fwd;
      else  ++nJet_cen;
      if((event->jets.at(iJet).eta<maxPosEta) && (event->jets.at(iJet).eta>maxNegEta)) ++nJet_cenj;
      if(event->jets.at(iJet).pt>30.0 && (event->jets.at(iJet).eta<maxPosEta && event->jets.at(iJet).eta>maxNegEta)) ++nJet_cenj30;
      if(event->jets.at(iJet).pt>40.0 && (event->jets.at(iJet).eta<maxPosEta && event->jets.at(iJet).eta>maxNegEta)) ++nJet_cenj40;
      if(event->jets.at(iJet).pt>50.0 && (event->jets.at(iJet).eta<maxPosEta && event->jets.at(iJet).eta>maxNegEta)) ++nJet_cenj50;
    }
    // recompute the number of b-tagged jets
    if(fBTagCut>-5.0){
      for(unsigned iJet=0; iJet<event->jets.size(); ++iJet){
	if(fabs(event->jets.at(iJet).eta)<2.5 && event->jets.at(iJet).HasVar(Mva::jetBtagWeight) && fBTagCut<event->jets.at(iJet).GetVar(Mva::jetBtagWeight)) ++nBjet;
      }
      event->RepVar(Mva::n_bjet, nBjet);
    }
    if(fJetVetoPt>0.0)
      event->RepVar(Mva::n_jet, nJet);
    //if(nJet25!=event->GetVar(Mva::n_jet)) std::cout << "error in jet counting" << nJet25 << " "  << event->GetVar(Mva::n_jet) << std::endl;

    // other jet calculations
    event->AddVar(Mva::n_jet_fwd, nJet_fwd);
    event->AddVar(Mva::n_jet_fwdj, nJet_fwdj);
    event->AddVar(Mva::n_jet_fwdj30, nJet_fwdj30);
    event->AddVar(Mva::n_jet_fwdj40, nJet_fwdj40);
    event->AddVar(Mva::n_jet_fwdj50, nJet_fwdj50);
    event->AddVar(Mva::n_jet_cen, nJet_cen);
    event->AddVar(Mva::n_jet_cenj, nJet_cenj);
    event->AddVar(Mva::n_jet_cenj30, nJet_cenj30);
    event->AddVar(Mva::n_jet_cenj40, nJet_cenj40);
    event->AddVar(Mva::n_jet_cenj50, nJet_cenj50);


    // Fill Truth Els
    if(truth_el_pt && fisMC){
      for(unsigned iEl=0; iEl<truth_el_pt->size(); ++iEl){
	RecParticle new_el;
	new_el.pt  = truth_el_pt->at(iEl)/1.0e3;
	new_el.eta = truth_el_eta->at(iEl);
	new_el.phi = truth_el_phi->at(iEl);
	event->truth_el.push_back(new_el);
      }
      //event->RepVar(Mva::n_truth_el, truth_el_pt->size());
    }

    // Fill Truth Mus
    if(truth_mu_pt && fisMC){
      for(unsigned iMu=0; iMu<truth_mu_pt->size(); ++iMu){
	RecParticle new_mu;
	new_mu.pt  = truth_mu_pt->at(iMu)/1.0e3;
	new_mu.eta = truth_mu_eta->at(iMu);
	new_mu.phi = truth_mu_phi->at(iMu);
	new_mu.m   = 0.10566;
	event->truth_mu.push_back(new_mu);
      }
      //event->RepVar(Mva::n_truth_mu, truth_mu_pt->size());
    }

    // Fill Truth Taus
    if(truth_tau_pt && fisMC){
      for(unsigned iTau=0; iTau<truth_tau_pt->size(); ++iTau){
	RecParticle new_tau;
	new_tau.pt  = truth_tau_pt->at(iTau)/1.0e3;
	new_tau.eta = truth_tau_eta->at(iTau);
	new_tau.phi = truth_tau_phi->at(iTau);
	// overlap remove the taus
	bool eMuVeto=false;
	for(unsigned iMuo=0; iMuo<event->truth_mu.size(); ++iMuo)
	  if(event->truth_mu.at(iMuo).GetVec().DeltaR(new_tau.GetVec())<0.4) eMuVeto=true;
	for(unsigned iEle=0; iEle<event->truth_el.size(); ++iEle)
	  if(event->truth_el.at(iEle).GetVec().DeltaR(new_tau.GetVec())<0.4) eMuVeto=true;
	if(!eMuVeto) event->truth_taus.push_back(new_tau);
      }
      event->RepVar(Mva::n_truth_tau, truth_tau_pt->size());
    }

    // Fill Truth Jets
    if(truth_jet_pt && fisMC){
      for(unsigned iJet=0; iJet<truth_jet_pt->size(); ++iJet){
	RecParticle new_jet;
	new_jet.pt  = truth_jet_pt->at(iJet)/1.0e3;
	new_jet.eta = truth_jet_eta->at(iJet);
	new_jet.phi = truth_jet_phi->at(iJet);
	bool skipJet=false;
	for(unsigned iLep=0; iLep<(event->truth_el.size()); ++iLep)  if(new_jet.GetVec().DeltaR(event->truth_el.at(iLep).GetVec())<0.3 && event->truth_el.at(iLep).pt>20.0){ skipJet=true; break; }
	for(unsigned iLep=0; iLep<(event->truth_taus.size()); ++iLep)  if(new_jet.GetVec().DeltaR(event->truth_taus.at(iLep).GetVec())<0.3 && event->truth_taus.at(iLep).pt>20.0){ skipJet=true; break; }
	if(!skipJet) event->truth_jets.push_back(new_jet);
      }
    }

    // Truth match the jets
    int nTruthJetMatch=0;
    if(fisMC){
      for(unsigned iJet=0; iJet<event->jets.size(); ++iJet){
	bool matchTruth=false;
	for(unsigned iTJet=0; iTJet<event->truth_jets.size(); ++iTJet){
	  if(event->jets.at(iJet).GetVec().DeltaR(event->truth_jets.at(iTJet).GetVec())<0.4){
	    matchTruth=true;
	    break;
	  }
	}
	if(matchTruth) ++nTruthJetMatch;
      }
    }
    event->AddVar(Mva::nTruthJetMatch, nTruthJetMatch);

    // Fill Base electrons
    unsigned n_baselep=0;
    unsigned n_wlep=0;
    unsigned n_siglep=0;
    if(baseel_pt){
      //unsigned n_baseel=0;
      for(unsigned iEl=0; iEl<baseel_pt->size(); ++iEl){
	RecParticle new_ele;
        float base_pt = baseel_pt->at(iEl);
	new_ele.pt  = base_pt/1.0e3;
	new_ele.eta = baseel_eta->at(iEl);
	new_ele.phi = baseel_phi->at(iEl);
	new_ele.m   = 0.000511;
        new_ele.AddVar(Mva::charge, baseel_charge->at(iEl));

        // Store the ptvarcone{20,30} and the topoetcone.
        if (baseel_ptvarcone20 && baseel_ptvarcone20->size()>iEl) new_ele.AddVar(Mva::ptvarcone20,baseel_ptvarcone20->at(iEl)/base_pt);
        if (baseel_ptvarcone30 && baseel_ptvarcone30->size()>iEl) new_ele.AddVar(Mva::ptvarcone30,baseel_ptvarcone30->at(iEl)/base_pt);
        if (baseel_topoetcone20 && baseel_topoetcone20->size()>iEl) new_ele.AddVar(Mva::topoetcone20,baseel_topoetcone20->at(iEl)/base_pt);

	//new_ele.AddVar(Mva::ptvarcone20,jet_timing->at(iJet));
	//if(!(fabs(new_ele.eta)>1.37 && fabs(new_ele.eta)<1.52 && new_ele.pt<27.0)){
	//++n_baseel;
	event->baseel.push_back(new_ele);
      }
      //event->RepVar(Mva::n_baseel, n_baseel);
    }

    // Fill Base muons
    if(basemu_pt){
      //unsigned n_basemu=0;
      for(unsigned iMu=0; iMu<basemu_pt->size(); ++iMu){
	RecParticle new_muo;

        float base_pt = basemu_pt->at(iMu);
	new_muo.pt  = base_pt/1.0e3;
	new_muo.eta = basemu_eta->at(iMu);
	new_muo.phi = basemu_phi->at(iMu);
	new_muo.m   = 0.10566;
        new_muo.AddVar(Mva::charge, basemu_charge->at(iMu));

        // Store the ptvarcone{20,30} and the topoetcone.
        if (basemu_ptvarcone20 && basemu_ptvarcone20->size()>iMu) new_muo.AddVar(Mva::ptvarcone20,basemu_ptvarcone20->at(iMu)/base_pt);
        if (basemu_ptvarcone30 && basemu_ptvarcone30->size()>iMu) new_muo.AddVar(Mva::ptvarcone30,basemu_ptvarcone30->at(iMu)/base_pt);
        if (basemu_topoetcone20 && basemu_topoetcone20->size()>iMu) new_muo.AddVar(Mva::topoetcone20,basemu_topoetcone20->at(iMu)/base_pt);

	//++n_basemu;
	event->basemu.push_back(new_muo);
      }
      //event->RepVar(Mva::n_basemu, n_basemu);
      //n_baselep+=n_basemu;
    }
    n_baselep+=event->GetVar(Mva::n_baseel);
    //if(fv26Ntuples) n_baselep+=event->GetVar(Mva::n_basemu);
    n_baselep+=event->GetVar(Mva::n_mu_baseline_noOR);
    event->RepVar(Mva::n_baselep, n_baselep);
    n_siglep+=event->GetVar(Mva::n_el);
    n_siglep+=event->GetVar(Mva::n_mu);
    event->RepVar(Mva::n_siglep, n_siglep);
    n_wlep+=event->GetVar(Mva::n_el_w);
    n_wlep+=event->GetVar(Mva::n_mu_w);
    event->RepVar(Mva::n_lep_w, n_wlep);

    // Fill signal photons
    if(ph_pt){
      //unsigned n_ph=0;
      for(unsigned iPh=0; iPh<ph_pt->size(); ++iPh){
	RecParticle new_ph;
	new_ph.pt  = ph_pt->at(iPh)/1.0e3;
	new_ph.eta = ph_eta->at(iPh);
	new_ph.phi = ph_phi->at(iPh);
	//++n_ph;
	event->photons.push_back(new_ph);
      }
      //event->RepVar(Mva::n_ph, n_ph);
    }

    // convert variables to GeV
    event->Convert2GeV(fVarMeV);

    // Reset MET?
    if(fMETChoice!="met_tst_et"){
      Mva::Var my_met = Mva::Convert2Var(fMETChoice);
      Mva::Var my_met_phi = Mva::Convert2Var(fMETChoice_phi);

      // fill the met alternative
      event->met_nolep.SetPtEtaPhiM(event->GetVar(my_met),0.0,event->GetVar(my_met_phi),0.0);
      for(unsigned iLep=0; iLep<event->electrons.size(); ++iLep)
	event->met_nolep+=event->electrons.at(iLep).GetLVec();
      for(unsigned iLep=0; iLep<event->muons.size(); ++iLep)
	event->met_nolep+=event->muons.at(iLep).GetLVec();
      //std::cout << "    met after leptons: " << event->met_nolep.Pt()
      //		<< " nEle: " << event->electrons.size()
      //		<< " nMuo: " << event->muons.size()
      //		<< std::endl;
      // replace
      event->RepVar(Mva::met_tst_phi,       event->GetVar(my_met_phi));
      event->RepVar(Mva::met_tst_et,        event->GetVar(my_met));
      event->RepVar(Mva::met_tst_nolep_phi, event->met_nolep.Phi());
      event->RepVar(Mva::met_tst_nolep_et,  event->met_nolep.Pt());
    }

    // Fill MET
    if(event->HasVar(Mva::met_tst_phi))
      event->met.SetPtEtaPhiM(event->GetVar(Mva::met_tst_et),0.0,event->GetVar(Mva::met_tst_phi),0.0);
    if(event->HasVar(Mva::met_tst_nolep_phi))
      event->met_nolep.SetPtEtaPhiM(event->GetVar(Mva::met_tst_nolep_et),0.0,event->GetVar(Mva::met_tst_nolep_phi),0.0);

    // refill the deltaPhi met jet
    if(fMETChoice!="met_tst_et" || true){
      if(event->jets.size()>1){
	event->RepVar(Mva::met_tst_j1_dphi,fabs(event->met.DeltaPhi(event->jets.at(0).GetLVec())));
	event->RepVar(Mva::met_tst_j2_dphi,fabs(event->met.DeltaPhi(event->jets.at(1).GetLVec())));
	event->RepVar(Mva::met_tst_nolep_j1_dphi,fabs(event->met_nolep.DeltaPhi(event->jets.at(0).GetLVec())));
	event->RepVar(Mva::met_tst_nolep_j2_dphi,fabs(event->met_nolep.DeltaPhi(event->jets.at(1).GetLVec())));
      }
    }


    // extra jets - computing the dPhi
    float met_tst_j3_dphi=-999.0;
    float max_j3_dr = -999.0;
    if(event->jets.size()>1){
      const TLorentzVector j1v = event->jets.at(0).GetLVec();
      const TLorentzVector j2v = event->jets.at(1).GetLVec();
      for(unsigned iJ=2; iJ<event->jets.size(); ++iJ){
	const TLorentzVector j3v = event->jets.at(iJ).GetLVec();
	if(met_tst_j3_dphi<fabs(event->met.DeltaPhi(j3v)))
	  met_tst_j3_dphi=fabs(event->met.DeltaPhi(j3v));
	float tmp_max_j3_dr = std::min(j1v.DeltaR(j3v), j2v.DeltaR(j3v));
	if(max_j3_dr<tmp_max_j3_dr) max_j3_dr = tmp_max_j3_dr;
      }
    }
    event->RepVar(Mva::met_tst_j3_dphi, met_tst_j3_dphi);
    event->RepVar(Mva::max_j3_dr, max_j3_dr);

    //
    // Checking the truth filtering
    //
    int truthFilter=0;
    double truth_deta_jj=-10.0, truth_jj_mass=-10.0, filterMet=-10.0, truthJet1=-10.0;
    if(event->truth_jets.size()>1){
      float tmet_px=0.0, tmet_py=0.0;
      TVector3 tmet;
      //tmet.SetPtEtaPhi(event->GetVar(Mva::met_truth_et), 0, event->GetVar(Mva::met_truth_phi)); // removed due to speed
      tmet_px=event->GetVar(Mva::met_truth_et)*cos(event->GetVar(Mva::met_truth_phi));
      tmet_py=event->GetVar(Mva::met_truth_et)*sin(event->GetVar(Mva::met_truth_phi));
      tmet.SetXYZ(tmet_px,tmet_py,0.0);
      //if(event->sample==Mva::kZqcd) std::cout << "met before: " << tmet.Pt() << std::endl;
      //std::cout << "met: " << tmet.Pt() << std::endl;
      for(unsigned iLep=0; iLep<(event->truth_mu.size()); ++iLep)  tmet+=event->truth_mu.at(iLep).GetVec();
      for(unsigned iLep=0; iLep<(event->truth_el.size()); ++iLep)  tmet+=event->truth_el.at(iLep).GetVec();
      for(unsigned iLep=0; iLep<(event->truth_taus.size()); ++iLep) tmet+=event->truth_taus.at(iLep).GetVec();
      TLorentzVector truth_jj = event->truth_jets.at(0).GetLVec() + event->truth_jets.at(1).GetLVec();
      truthJet1 = event->truth_jets.at(1).pt;
      if(truthJet1>35.0){
	truth_deta_jj = fabs(event->truth_jets.at(0).eta - event->truth_jets.at(1).eta);
	truth_jj_mass=truth_jj.M();
      }
      //filterMet = sqrt(tmet_px*tmet_px+tmet_py*tmet_py);//tmet.Pt();
      filterMet = sqrt(tmet.Px()*tmet.Px()+tmet.Py()*tmet.Py()); // needed for speed issues
      //if(event->sample==Mva::kZqcd) std::cout << "met after: " << tmet.Pt() << std::endl;
      if(truth_jj_mass>500.0 && truth_deta_jj>4.0
	 && event->truth_jets.at(1).pt>35.0 && filterMet>100.0) truthFilter=1;
      //std::cout << "truthFilter: " << truthFilter << " met: " << tmet.Pt()
      //<< " mjj: " << truth_jj.M() << " truthJetPt: " << event->truth_jets.at(1).pt
      //	<< std::endl;
    }
    event->RepVar(Mva::truth_jj_mass, truth_jj_mass);
    event->RepVar(Mva::truth_jj_deta, truth_deta_jj);
    if(event->truth_jets.size()>0){ event->RepVar(Mva::truth_j1_pt,   event->truth_jets.at(0).pt);    } else  event->RepVar(Mva::truth_j1_pt, 0.0);
    if(event->truth_jets.size()>1){ event->RepVar(Mva::truth_j2_pt,   event->truth_jets.at(1).pt);    } else  event->RepVar(Mva::truth_j2_pt, 0.0);    
    event->AddVar(Mva::FilterMet,     filterMet);
    event->AddVar(Mva::TruthFilter,   truthFilter);
    event->AddVar(Mva::truthJet1Pt,   truthJet1);

    // update for photon
    if(fOverlapPh) AddPhoton(*event);

    // fill emu variables
    ComputeLepVars(*event);

    // Fill remaining variables
    FillEvent(*event);

    // decode trigger_lep
    int trigger_lep = event->GetVar(Mva::trigger_lep);
    int trigger_lep_new = ((trigger_lep&0x1)>0) ? 1 : 0;
    if( event->GetVar(Mva::lep_trig_match)<0.5) trigger_lep_new=0;
    if(trigger_lep_new==0 && (trigger_lep&0x20)==0x20) trigger_lep_new = 2;
    if(trigger_lep_new==0 && (trigger_lep&0x400)==0x400) trigger_lep_new = 3;
    event->RepVar(Mva::trigger_lep, trigger_lep_new);

    // decode trigger_met
    int trigger_met_encodedv2 = event->GetVar(Mva::trigger_met_encodedv2);
    int trigger_met_encodedv2_new=0;
    if((trigger_met_encodedv2 & 0x2)==0x2) trigger_met_encodedv2_new=1; // HLT_xe110_pufit_L1XE55 2017
    if((trigger_met_encodedv2 & 0x4)==0x4) trigger_met_encodedv2_new=2; // HLT_xe90_pufit_L1XE50 2017
    if((trigger_met_encodedv2 & 0x8)==0x8) trigger_met_encodedv2_new=3; // HLT_xe110_pufit_xe70_L1XE50 2018

    // run selected for 2017 => value 4 for 2017
    if(!fisMC) fRandomRunNumber = fRunNumber;
    //if     (325713<=fRandomRunNumber && fRandomRunNumber<=328393 && ((trigger_met_encodedv2 & 0x4)==0x4))   trigger_met_encodedv2_new=4; //HLT_xe90_pufit_L1XE50;    // period B
    //else if(329385<=fRandomRunNumber && fRandomRunNumber<=330470 && ((trigger_met_encodedv2 & 0x40)==0x40)) trigger_met_encodedv2_new=4; //HLT_xe100_pufit_L1XE55;   // period C
    //else if(330857<=fRandomRunNumber && fRandomRunNumber<=331975 && ((trigger_met_encodedv2 & 0x2)==0x2))   trigger_met_encodedv2_new=4; //HLT_xe110_pufit_L1XE55;   // period D1-D5
    //else if(341649>=fRandomRunNumber && fRandomRunNumber>331975 && ((trigger_met_encodedv2 & 0x80)==0x80))  trigger_met_encodedv2_new=4; //HLT_xe110_pufit_L1XE50;   // period D6-K
    if(325713<=fRandomRunNumber && fRandomRunNumber<=341649 && ((trigger_met_encodedv2 & 0x2)==0x2))   trigger_met_encodedv2_new=4; //HLT_xe110_pufit_L1XE55;   // All periods

    if     (fRandomRunNumber>=355529  && ((trigger_met_encodedv2 & 0x4000)==0x4000))     trigger_met_encodedv2_new=10; // HLT_j70_j50_0eta490_invm1000j50_dphi24_xe90_pufit_xe50_L1MJJ-500-NFF
    if     (fRandomRunNumber>=355529  && ((trigger_met_encodedv2 & 0x8000)==0x8000))     trigger_met_encodedv2_new=11; // HLT_j70_j50_0eta490_invm1100j70_dphi20_deta40_L1MJJ-500-NFF
    // 2018 update trigger for later periods => value 5 for
    //if     (350067>fRandomRunNumber  && fRandomRunNumber>=348197  && ((trigger_met_encodedv2 & 0x8)==0x8))    trigger_met_encodedv2_new=5; // HLT_xe110_pufit_xe70_L1XE50
    //else if(350067<=fRandomRunNumber && fRandomRunNumber<=364292 && ((trigger_met_encodedv2 & 0x800)==0x800)) trigger_met_encodedv2_new=5; // HLT_xe110_pufit_xe65_L1XE50
    if(364292>=fRandomRunNumber  && fRandomRunNumber>=348197  && ((trigger_met_encodedv2 & 0x8)==0x8))    trigger_met_encodedv2_new=5; // HLT_xe110_pufit_xe70_L1XE50    
    if(fIsDDQCD){
      if(fYear==2017) trigger_met_encodedv2_new=4;
      else if(fYear==2018) trigger_met_encodedv2_new=5;      
      else trigger_met_encodedv2_new=1;       // 2015+2016
    }
    event->RepVar(Mva::trigger_met_encodedv2, trigger_met_encodedv2_new);
    if(trigger_met_encodedv2_new==0 || trigger_met_encodedv2_new>6){
      xeSFTrigWeight_nomu=1.0; xeSFTrigWeight_nomu__1up=1.0; xeSFTrigWeight_nomu__1down=1.0; }
    // 2015+2016 encoding
    int trigger_met_encoded = event->GetVar(Mva::trigger_met_encoded);
    int runPeriod = 0;
    //int midRun = 303982; // was 302872
    int midRun = 302872; // was 302872
    if(fRandomRunNumber<=284484)                                  runPeriod = 1;
    else if(fRandomRunNumber >284484 && fRandomRunNumber<=midRun) runPeriod = 2; // 2016
    else if(fRandomRunNumber >midRun && fRandomRunNumber< 325713) runPeriod = 3; // 2016
    else if(325713<=fRandomRunNumber && fRandomRunNumber<=328393) runPeriod = 10; // 2017 HLT_xe90_pufit_L1XE50
    else if(329385<=fRandomRunNumber && fRandomRunNumber<=330470) runPeriod = 11; // 2017 HLT_xe100_pufit_L1XE55
    else if(330857<=fRandomRunNumber && fRandomRunNumber<=331975) runPeriod = 12; // 2017 HLT_xe110_pufit_L1XE55
    else if(341649>=fRandomRunNumber && fRandomRunNumber>331975 ) runPeriod = 13; // 2017 HLT_xe110_pufit_L1XE50
    if(350067>fRandomRunNumber  && fRandomRunNumber>=348197)      runPeriod = 30; // 2018 xe70 trigger ...348197
    else if(350067<=fRandomRunNumber && fRandomRunNumber<=364292) runPeriod = 31; // 2018 xe65 trigger
    if(fRandomRunNumber>=355529) runPeriod = 20; // 2018 VBF Topo triggers

    int trigger_met_byrun=0; // for the computation of the met trigger SF
    if(fRandomRunNumber<=284484 && (trigger_met_encoded & 0x8))                             { trigger_met_byrun=1;  }// 2015
    if(fRandomRunNumber >284484 && fRandomRunNumber<=midRun && (trigger_met_encoded & 0x4)) { trigger_met_byrun=2;  }// 2016 -D3
    if(fRandomRunNumber >midRun && (trigger_met_encoded & 0x2))                             { trigger_met_byrun=3;  }// 2016
    if(trigger_met_byrun==0 && (trigger_met_encoded & 0x10) == 0x10 ){
      if(fRandomRunNumber<=284484)                                  trigger_met_byrun = 4;
      else if(fRandomRunNumber >284484 && fRandomRunNumber<=midRun) trigger_met_byrun = 5;
      else if(fRandomRunNumber >midRun)                             trigger_met_byrun = 6;
    }// 2015+2016
    event->RepVar(Mva::trigger_met_byrun, trigger_met_byrun);
    event->RepVar(Mva::runPeriod,         runPeriod);

    // apply the overlap
    if(fOverlapPh && fisMC){
      bool in_vy_overlap = event->GetVar(Mva::in_vy_overlap);
      bool isVjets =(event->sample==Mva::kWqcdMad) || (event->sample==Mva::kWqcd) || (event->sample==Mva::kZqcd) || (event->sample==Mva::kZqcdMad) || (event->sample==Mva::kZewk) || (event->sample==Mva::kWewk) || (event->sample==Mva::kZqcdPow);
      bool isTop = (event->sample==Mva::ktop2);
      bool isVgjets = (event->sample==Mva::kttg) || (event->sample==Mva::kZgam) || (event->sample==Mva::kWgam) || (event->sample==Mva::kZgamEWK) || (event->sample==Mva::kWgamEWK);
      event->RepVar(Mva::in_vy_overlapCut,1.0);
      if(isVjets && in_vy_overlap)   event->RepVar(Mva::in_vy_overlapCut,0.0);
      if(isTop   && in_vy_overlap)   event->RepVar(Mva::in_vy_overlapCut,0.0);
      if(isVgjets && !in_vy_overlap) event->RepVar(Mva::in_vy_overlapCut,0.0);
    }else{
      event->RepVar(Mva::in_vy_overlapCut,1.0);
    }

    // Change the leptons to base leptons - after filling the event
    if(fLoadBaseLep) ChangeLep(*event);

    if(i % 10000 == 0 && i > 0) {
      cout << "Processed " << setw(10) << right << i << " events" << endl;
    }

    ++fCountEvents;

    // Process TMVA
    if(fTMVAReader){
      // fill the variables
      fTMVAVars[0]=event->GetVar(Mva::jj_mass)*1.0e3;
      fTMVAVars[1]=event->GetVar(Mva::jj_dphi);
      fTMVAVars[2]=event->GetVar(Mva::jj_deta);
      fTMVAVars[3]=event->GetVar(Mva::met_tst_et)*1.0e3;
      fTMVAVars[4]=event->GetVar(Mva::met_soft_tst_et)*1.0e3;
      fTMVAVars[5]=event->GetVar(Mva::jetPt0)*1.0e3;
      fTMVAVars[6]=event->GetVar(Mva::jetPt1)*1.0e3;
      event->RepVar(Mva::tmva, fTMVAReader->EvaluateMVA( fTMVAVars, fMVAName ));
      //std::cout << "inputs: " << fTMVAVars[0] << " " << fTMVAVars[1] << " " << fTMVAVars[2] << " " << fTMVAVars[3] << " " << fTMVAVars[4] << " " << fTMVAVars[5] << " " << event->GetVar(Mva::tmva) << std::endl;
    }else if(!event->HasVar(Mva::tmva)) { event->AddVar(Mva::tmva, 0.0); }

    //
    // Process sub-algorithms
    //
    ProcessAlgs(*event, alg_evt);
  }

  //
  // Clean up memory
  //
  //delete var;
  delete event;
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::Save(TDirectory *dir)
{
#ifdef ANP_CPU_PROFILER
  log() << "Save - compiled with perftools: ProfilerStop." << endl;
  ProfilerStop();
#endif

  if(!dir) {
    log() << "Save - no valid output file... nothing to do" << endl;
    return;
  }

  log() << "Save - will save algorithm data..." << endl;

  //
  // Save common algorithm(s)
  //
  for(AlgVec::iterator it = fAlgCommon.begin(); it != fAlgCommon.end(); ++it) {
    (*it)->DoSave(dir);
  }

  //
  // Save pre-selection algorithm(s)
  //
  for(AlgVec::iterator it = fAlgPreSel.begin(); it != fAlgPreSel.end(); ++it) {
    (*it)->DoSave(dir);
  }

  //
  // Save normal algorithm(s)
  //
  for(AlgList::const_iterator it = fAlgNormal.begin(); it != fAlgNormal.end(); ++it) {
    //
    // Create sequence directory
    //
    TDirectory *adir = Msl::GetDir(it->alg_key, dir);

    for(unsigned ialg = 0; ialg < it->alg_vec.size(); ++ialg) {
      it->alg_vec.at(ialg)->DoSave(adir);
    }
  }

  //
  // Save tex file with all cut-flows
  //
  //if(!fCutFlowFile.empty()) {
  //  CutFlowMan::Instance().WriteCutFlows(fCutFlowFile);
  //}
  //if(!fRawFlowFile.empty()) {
  //  CutFlowMan::Instance().WriteRawFlows(fRawFlowFile);
  //}

}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::FillEvent(Event &event)
{

  //
  // Compute xsec weight and classify event as data/signal/background
  //
  if(event.jets.size()>0){
    event.AddVar(Mva::jetPt0,  event.jets.at(0).pt);
    event.AddVar(Mva::jetEta0, event.jets.at(0).eta);
    event.AddVar(Mva::j0timing,event.jets.at(0).GetVar(Mva::timing));
    event.AddVar(Mva::j0jvt,event.jets.at(0).GetVar(Mva::jvt));
    event.AddVar(Mva::j0fjvt,event.jets.at(0).GetVar(Mva::fjvt));
    event.AddVar(Mva::jetTrackWidth0,  event.jets.at(0).GetVar(Mva::jetTrackWidth));
    event.AddVar(Mva::jetNTracks0,  event.jets.at(0).GetVar(Mva::jetNTracks));
    event.AddVar(Mva::jetPartonTruthLabelID0,  event.jets.at(0).GetVar(Mva::jetPartonTruthLabelID));
  }
  if(event.jets.size()>1){
    event.AddVar(Mva::jetPt1,  event.jets.at(1).pt);
    event.AddVar(Mva::jetEta1, event.jets.at(1).eta);
    event.AddVar(Mva::j1timing,event.jets.at(1).GetVar(Mva::timing));
    event.AddVar(Mva::j1jvt,event.jets.at(1).GetVar(Mva::jvt));
    event.AddVar(Mva::j1fjvt,event.jets.at(1).GetVar(Mva::fjvt));
    event.AddVar(Mva::etaj0TimesEtaj1,event.jets.at(0).eta*event.jets.at(1).eta);
    event.AddVar(Mva::jetTrackWidth1,  event.jets.at(1).GetVar(Mva::jetTrackWidth));
    event.AddVar(Mva::jetNTracks1,  event.jets.at(1).GetVar(Mva::jetNTracks));
    event.AddVar(Mva::jetPartonTruthLabelID1,  event.jets.at(1).GetVar(Mva::jetPartonTruthLabelID));
  }

  if(event.electrons.size()>0 && event.muons.size()>0){

    TLorentzVector leadL = event.electrons.at(0).GetLVec();
    if(event.electrons.at(0).pt<event.muons.at(0).pt){
      leadL=event.muons.at(0).GetLVec();
      event.AddVar(Mva::lepCh0,  event.muons.at(0).GetVar(Mva::charge));
      event.AddVar(Mva::lepCh1,  event.electrons.at(0).GetVar(Mva::charge));
      event.AddVar(Mva::lepPt1,  event.electrons.at(0).pt);
    }else{
      event.AddVar(Mva::lepCh0,  event.electrons.at(0).GetVar(Mva::charge));
      event.AddVar(Mva::lepCh1,  event.muons.at(0).GetVar(Mva::charge));
      event.AddVar(Mva::lepPt1,  event.muons.at(0).pt);
    }
    event.AddVar(Mva::lepPt0,  leadL.Pt());
    double MT = sqrt(2. * leadL.Pt() * event.met.Pt() * (1. - cos(leadL.Phi() - event.met.Phi())));
    event.AddVar(Mva::mt, MT);

    TLorentzVector Z = (event.electrons.at(0).GetLVec()+event.muons.at(0).GetLVec());
    event.RepVar(Mva::mll,  Z.M());
    event.RepVar(Mva::ptll, Z.Pt());

  }else{
    // electrons
    if(event.electrons.size()>0){
      event.AddVar(Mva::lepPt0,  event.electrons.at(0).pt);
      event.AddVar(Mva::lepCh0,  event.electrons.at(0).GetVar(Mva::charge));
      double MT = sqrt(2. * event.electrons.at(0).pt * event.met.Pt() * (1. - cos(event.electrons.at(0).phi - event.met.Phi())));
      event.AddVar(Mva::mt, MT);
    }
    if(event.electrons.size()>1){
      event.AddVar(Mva::lepPt1,  event.electrons.at(1).pt);
      event.AddVar(Mva::lepCh1,  event.electrons.at(1).GetVar(Mva::charge));
      TLorentzVector Z = (event.electrons.at(1).GetLVec()+event.electrons.at(0).GetLVec());
      event.RepVar(Mva::mll,  Z.M());
      event.RepVar(Mva::ptll, Z.Pt());
    }

    // muons
    if(event.muons.size()>0){
      event.AddVar(Mva::lepPt0,  event.muons.at(0).pt);
      event.AddVar(Mva::lepCh0,  event.muons.at(0).GetVar(Mva::charge));
      double MT = sqrt(2. * event.muons.at(0).pt * event.met.Pt() * (1. - cos(event.muons.at(0).phi - event.met.Phi())));
      event.AddVar(Mva::mt, MT);
    }
    if(event.muons.size()>1){
      event.AddVar(Mva::lepPt1, event.muons.at(1).pt);
      event.AddVar(Mva::lepCh1, event.muons.at(1).GetVar(Mva::charge));
      TLorentzVector Z = (event.muons.at(1).GetLVec()+event.muons.at(0).GetLVec());
      event.RepVar(Mva::mll,  Z.M());
      event.RepVar(Mva::ptll, Z.Pt());
    }
  }

  // Store the base lepton pT and charge.
  // Also store the ptvarcone-- ptvarcone30 for muons, ptvarcone20 for electrons.
  // Note that the ptvarcone was already divided by the pT above.
  if (event.baseel.size() > 0 || event.basemu.size() > 0) {
    TLorentzVector leadBaseEl;
    TLorentzVector leadBaseMu;

    if (event.baseel.size() > 0) {
      leadBaseEl = event.baseel.at(0).GetLVec();
    }

    if (event.basemu.size() > 0) {
      leadBaseMu = event.basemu.at(0).GetLVec();
    }

    // Store whichever is larger. The uninitialized pT should be 0!
    if (leadBaseEl.Pt() >= leadBaseMu.Pt()) {
      event.RepVar(Mva::baselepPt0, leadBaseEl.Pt());
      event.RepVar(Mva::baselepCh0, event.baseel.at(0).GetVar(Mva::charge));
      event.RepVar(Mva::baselep_ptvarcone_0, event.baseel.at(0).GetVar(Mva::ptvarcone20));
    } else {
      event.RepVar(Mva::baselepPt0, leadBaseMu.Pt());
      event.RepVar(Mva::baselepCh0, event.basemu.at(0).GetVar(Mva::charge));
      event.RepVar(Mva::baselep_ptvarcone_0, event.basemu.at(0).GetVar(Mva::ptvarcone30));
    }
  }

  // Lepton Channels
  unsigned chanFlavor = 0;
  if(event.muons.size()==0 && event.electrons.size()==0) chanFlavor=1;
  if(event.muons.size()==1 && event.electrons.size()==0 && event.muons.at(0).GetVar(Mva::charge)>0) chanFlavor=2;
  if(event.muons.size()==1 && event.electrons.size()==0 && event.muons.at(0).GetVar(Mva::charge)<0) chanFlavor=3;
  if(event.electrons.size()==1 && event.muons.size()==0 && event.electrons.at(0).GetVar(Mva::charge)>0) chanFlavor=4;
  if(event.electrons.size()==1 && event.muons.size()==0 && event.electrons.at(0).GetVar(Mva::charge)<0) chanFlavor=5;
  if(event.muons.size()==2 && (event.muons.at(0).GetVar(Mva::charge)*event.muons.at(1).GetVar(Mva::charge))>0) chanFlavor=6;
  if(event.muons.size()==2 && (event.muons.at(0).GetVar(Mva::charge)*event.muons.at(1).GetVar(Mva::charge))<0) chanFlavor=7;
  if(event.electrons.size()==2 && (event.electrons.at(0).GetVar(Mva::charge)*event.electrons.at(1).GetVar(Mva::charge))>0) chanFlavor=8;
  if(event.electrons.size()==2 && (event.electrons.at(0).GetVar(Mva::charge)*event.electrons.at(1).GetVar(Mva::charge))<0) chanFlavor=9;
  if(event.muons.size()==1 && event.electrons.size()==1 && event.muons.at(0).GetVar(Mva::charge)*event.electrons.at(0).GetVar(Mva::charge)>0) chanFlavor=10;
  if(event.muons.size()==1 && event.electrons.size()==1 && event.muons.at(0).GetVar(Mva::charge)*event.electrons.at(0).GetVar(Mva::charge)<0) chanFlavor=11;
  event.AddVar(Mva::chanFlavor, chanFlavor);
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::ProcessAlgs(Event &top_event, Event &alg_event)
{
  //
  // Print debug info
  //
  //if(fDebug) {
    top_event.Print();
    //}

  //
  // Run top common algorithm(s)
  //
  for(AlgVec::iterator it = fAlgCommon.begin(); it != fAlgCommon.end(); ++it) {
    if(!((*it)->DoExec(top_event))) {
      std::cout << "rejected...top common" << std::endl;
      return;
    }
  }

  //
  // Run pre-select algorithm(s)
  //
  for(AlgVec::iterator it = fAlgPreSel.begin(); it != fAlgPreSel.end(); ++it) {
    if((*it)->DoExec(top_event)) {
      (*it)->SetPassStatus(true);
    }
    else {
      (*it)->SetPassStatus(false);
    }
  }

  //
  // Run normal algorithm(s)
  //
  for(AlgList::iterator it = fAlgNormal.begin(); it != fAlgNormal.end(); ++it) {
    //
    // Check pre-select algorithm decision - if set
    //
    if(it->pre_sel && !(it->pre_sel->GetPassStatus())) {
      std::cout << "rejected...normal" << std::endl;
      continue;
    }

    //
    // Sequence passed pre-selection - run algorithms using local event
    //
    alg_event = top_event;

    for(unsigned ialg = 0; ialg < it->alg_vec.size(); ++ialg) {
      //
      // Process sub-algorithms with their own copies of Event
      //
      if(fDebug) cout << it->alg_vec.at(ialg)->GetAlgName() << endl;
      if(!(it->alg_vec.at(ialg)->DoExec(alg_event))) {
	break;
      }
    }
  }
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::ComputeLepVars(Event &event)
{
  // fill leptons
  std::vector<TLorentzVector> my_leps;
  for(unsigned i=0; i<event.electrons.size(); ++i)
    my_leps.push_back(event.electrons.at(i).GetLVec());

  for(unsigned i=0; i<event.muons.size(); ++i)
      my_leps.push_back(event.muons.at(i).GetLVec());

  ////////////////////////////////
  // Mtt   // assumes collinear approximation
  ////////////////////////////////
  double x1=-999., x2=-999.,mtt=-999.;
  // leading two
  if(my_leps.size()>1){

    // fill met
    TVector3 met_beforeRemove;
    met_beforeRemove.SetPtEtaPhi(event.met.Pt(), 0.0, event.met.Phi());

    std::sort(my_leps.begin(),my_leps.end(),SortPhysicsObject("pt"));

    TLorentzVector Z = (my_leps.at(1)+my_leps.at(0));
    event.AddVar(Mva::mll,  Z.M());
    event.AddVar(Mva::ptll, Z.Pt());
    event.GetX1X2(my_leps.at(0), my_leps.at(1),
    make_pair<float,float>(met_beforeRemove.Px(), met_beforeRemove.Py()),
    x1, x2);
  if(x1>0.0 && x2>0.0) mtt=event.GetVar(Mva::mll)/TMath::Sqrt(x1*x2);
  }
  event.RepVar(Mva::Mtt, mtt);
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::ChangeLep(Event &event)
{
  // change to using baseleptons with loose iso.
  //n_el,n_mu,met_tst_nolep_j1_dphi,met_tst_nolep_j2_dphi
  // met_tst_nolep_et,met_tst_nolep_phi, ptll, mll, lepPt0, lepPt1, lepCh0, lepCh1
  //event->baseel;
  //event->basemu; mtautau
  //
  //unsigned n_el=0;
  //unsigned n_mu=0;
  std::vector<TLorentzVector> my_leps;
  for(unsigned i=0; i<event.baseel.size(); ++i){
    my_leps.push_back(event.baseel.at(i).GetLVec());
  }
  if(event.baseel.size()==2 && event.basemu.size()==0){
    event.RepVar(Mva::lepCh0, event.baseel.at(0).GetVar(Mva::charge));
    event.RepVar(Mva::lepCh1, event.baseel.at(1).GetVar(Mva::charge));

    unsigned chanFlavor=0;
    if(event.baseel.size()==2 && (event.baseel.at(0).GetVar(Mva::charge)*event.baseel.at(1).GetVar(Mva::charge))>0) chanFlavor=8;
    if(event.baseel.size()==2 && (event.baseel.at(0).GetVar(Mva::charge)*event.baseel.at(1).GetVar(Mva::charge))<0) chanFlavor=9;
    if(chanFlavor>0)
      event.RepVar(Mva::chanFlavor, chanFlavor);
  }
  if(event.baseel.size()==0 && event.basemu.size()==2){
    event.RepVar(Mva::lepCh0, event.basemu.at(0).GetVar(Mva::charge));
    event.RepVar(Mva::lepCh1, event.basemu.at(1).GetVar(Mva::charge));

    unsigned chanFlavor=0;
    if(event.basemu.size()==2 && (event.basemu.at(0).GetVar(Mva::charge)*event.basemu.at(1).GetVar(Mva::charge))>0) chanFlavor=6;
    if(event.basemu.size()==2 && (event.basemu.at(0).GetVar(Mva::charge)*event.basemu.at(1).GetVar(Mva::charge))<0) chanFlavor=7;
    if(chanFlavor>0)
      event.RepVar(Mva::chanFlavor, chanFlavor);
  }
  if(event.baseel.size()==1 && event.basemu.size()==1){
    if(event.baseel.at(0).pt>event.basemu.at(0).pt ){
      event.RepVar(Mva::lepCh0, event.baseel.at(0).GetVar(Mva::charge));
      event.RepVar(Mva::lepCh1, event.basemu.at(0).GetVar(Mva::charge));
    }else{
      event.RepVar(Mva::lepCh0, event.basemu.at(0).GetVar(Mva::charge));
      event.RepVar(Mva::lepCh1, event.baseel.at(0).GetVar(Mva::charge));
    }
  }
  //  if(baseel_ptvarcone20->at(i)/baseel_pt->at(i)<0.2){
  //    met+=event.baseel.at(i).GetVec();
  //    ++n_el;
  //    my_leps.push_back(event.baseel.at(i).GetLVec());
  //  }
  for(unsigned i=0; i<event.basemu.size(); ++i)
    my_leps.push_back(event.basemu.at(i).GetLVec());
  //  if(basemu_ptvarcone20->at(i)/basemu_pt->at(i)<0.2){
  //    met+=event.basemu.at(i).GetVec();
  //    ++n_mu;
  //
  //  }

  // removing the leptons
  //event.RepVar(Mva::met_tst_nolep_et,  met.Pt());
  //event.RepVar(Mva::met_tst_nolep_phi, met.Phi());
  //if(event.jets.size()>1){
  //  event.RepVar(Mva::met_tst_nolep_j1_dphi, met.DeltaPhi(event.jets.at(0).GetVec()));
  //  event.RepVar(Mva::met_tst_nolep_j2_dphi, met.DeltaPhi(event.jets.at(1).GetVec()));
  //}
  //event.RepVar(Mva::n_el, n_el);
  //event.RepVar(Mva::n_mu, n_mu);
  // sort leptons
  std::sort(my_leps.begin(),my_leps.end(),SortPhysicsObject("pt"));
  if(my_leps.size()>0)  event.RepVar(Mva::lepPt0, my_leps.at(0).Pt());
  if(my_leps.size()>1){
    event.RepVar(Mva::lepPt1, my_leps.at(1).Pt());
    TLorentzVector dilep = my_leps.at(0)+my_leps.at(1);
    event.RepVar(Mva::ptll, dilep.Pt());
    event.RepVar(Mva::mll, dilep.M());
  }

  ////////////////////////////////
  // Mtt   // assumes collinear approximation
  ////////////////////////////////
  double x1=-999., x2=-999.,mtt=-999.;
  if(my_leps.size()>1)
    event.GetX1X2(my_leps.at(0), my_leps.at(1),
		  make_pair<float,float>(event.met.Px(), event.met.Py()),  x1, x2);
  if(x1>0.0 && x2>0.0) mtt=event.GetVar(Mva::mll)/TMath::Sqrt(x1*x2);
  event.RepVar(Mva::Mtt, mtt);
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::AddPhoton(Event &event)
{
  // remove the jet overlapping
  // recompute jj_mass, jj_deta, etaj0TimesEtaj1, jetPt0, jetPt1, j0fjvt, j1fjvt, j0jvt, j1jvt, j0timing, j1timing,
  // add photon centrality?
  bool jet_change=false;
  unsigned nph = event.photons.size();
  for(unsigned i=0; i<nph; ++i){
    bool erase=false;
    TVector3 photon = event.photons.at(i).GetVec();

    for(unsigned j=0; j<event.baseel.size(); ++j){
      if(photon.DeltaR(event.baseel.at(j).GetVec())<0.2){
	erase=true;break;
      }
    }
    for(unsigned j=0; j<event.basemu.size(); ++j){
      if(photon.DeltaR(event.basemu.at(j).GetVec())<0.2){
	erase=true;break;
      }
    }
    if(erase){ event.photons.erase(event.photons.begin()+i); --i; --nph; continue; }

    // if photon is not removed by lepton, then remove jets nearby
    unsigned nj = event.jets.size();
    for(unsigned j=0; j<nj; ++j){
      if(photon.DeltaR(event.jets.at(j).GetVec())<0.2){
      	jet_change=true;
	event.jets.erase(event.jets.begin()+j);
	--j; --nj;
      }
    }
  }

  if(jet_change){
    event.RepVar(Mva::n_jet, event.jets.size());
    if(event.jets.size()>1){
      TLorentzVector jj = event.jets.at(0).GetLVec() + event.jets.at(1).GetLVec();
      event.RepVar(Mva::jj_mass, jj.M());
      event.RepVar(Mva::jj_deta, fabs(event.jets.at(0).eta - event.jets.at(1).eta));
      event.RepVar(Mva::jj_dphi, fabs(event.jets.at(0).GetVec().DeltaR(event.jets.at(1).GetVec())));
      //event.RepVar(Mva::etaj0TimesEtaj1,(event.jets.at(0).eta * event.jets.at(1).eta));
      //event.RepVar(Mva::jetPt0,event.jets.at(0).pt);
      //event.RepVar(Mva::jetPt1,event.jets.at(1).pt);
    }
  }
  float centrality=-999;
  float phPt = -999.0;
  float phEta = -999.0;
  float met_tst_ph_dphi = -999.;
  if(event.photons.size()>0 && event.jets.size()>1){
    centrality = exp(-4.0/std::pow(event.GetVar(Mva::jj_deta),2) * std::pow(event.photons.at(0).eta - (event.jets.at(0).eta+event.jets.at(1).eta)/2.0,2));
    phPt = event.photons.at(0).pt;
    phEta = event.photons.at(0).eta;
    met_tst_ph_dphi = fabs(event.photons.at(0).GetVec().DeltaPhi(event.met.Vect()));
  }
  event.RepVar(Mva::phcentrality,centrality);

  event.AddVar(Mva::met_tst_ph_dphi, met_tst_ph_dphi);
  event.AddVar(Mva::phPt, phPt);
  event.AddVar(Mva::phEta, phEta);
}

//-----------------------------------------------------------------------------
std::ostream& Msl::ReadEvent::log() const
{
  std::cout << "ReadEvent::";
  return std::cout;
}

//-----------------------------------------------------------------------------
void Msl::ReadEvent::AddVars(const std::string &key, const Registry &reg)
{
  //
  // Add input variables - type will be determined in real time when reading trees
  //
  vector<string> vars;
  reg.Get(key, vars);

  for(vector<string>::const_iterator vit = vars.begin(); vit != vars.end(); ++vit) {
    VarData data;

    data.key = *vit;
    data.var = Mva::Convert2Var(*vit);

    if(data.var == Mva::NONE) {
      continue;
    }

    bool found = false;

    for(VarVec::const_iterator it = fVarVec.begin(); it != fVarVec.end(); ++it) {
      if(it->var == data.var) {
    	found = true;
      }
    }

    if(found) {
      log() << "Conf - ignore duplicate var: " << *vit << endl;
    }
    else {
      fVarVec.push_back(data);
    }
  }

  //
  // Sort variables
  //
  std::sort(fVarVec.begin(), fVarVec.end());
}
