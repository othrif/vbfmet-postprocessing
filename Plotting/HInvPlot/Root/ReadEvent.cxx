// C/C++
#include <set>
#include <math.h>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <fstream>

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
  fDebug        (false),
  fPrint        (false),
  fPrintEvent   (false),
  fLumi         (1.0),
  genCutFlow    (0),
  procCutFlow0  (0),
  rawCutFlow    (0)
{
}

//-----------------------------------------------------------------------------
Msl::ReadEvent::~ReadEvent()
{
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
  reg.Get("ReadEvent::SystList",      fSystNames);
  reg.Get("ReadEvent::Trees",         fTrees);
  reg.Get("ReadEvent::Files",         fFiles);

  reg.Get("ReadEvent::Debug",         fDebug        = false);
  reg.Get("ReadEvent::Print",         fPrint        = false);
  reg.Get("ReadEvent::PrintEvent",    fPrintEvent   = false);
  reg.Get("ReadEvent::MCEventCount",  fMCEventCount = false);
  reg.Get("ReadEvent::Lumi",          fLumi = 1.0);  
  fDir="";

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
  el_charge  = new std::vector<float>(0);
  el_pt      = new std::vector<float>(0);
  el_eta     = new std::vector<float>(0);
  el_phi     = new std::vector<float>(0);
  mu_charge  = new std::vector<float>(0);
  mu_pt      = new std::vector<float>(0);
  mu_eta     = new std::vector<float>(0);
  mu_phi     = new std::vector<float>(0);
  jet_timing = new std::vector<float>(0);
  jet_pt     = new std::vector<float>(0);
  jet_eta    = new std::vector<float>(0);
  jet_phi    = new std::vector<float>(0);    
  
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

  tree->SetBranchAddress("w",        &fWeight);
  tree->SetBranchAddress("runNumber",&fRunNumber);  
  tree->SetBranchAddress("el_charge",&el_charge);  
  tree->SetBranchAddress("el_pt",    &el_pt);  
  tree->SetBranchAddress("el_eta",   &el_eta);  
  tree->SetBranchAddress("el_phi",   &el_phi);
  tree->SetBranchAddress("mu_charge",&mu_charge);  
  tree->SetBranchAddress("mu_pt",    &mu_pt);  
  tree->SetBranchAddress("mu_eta",   &mu_eta);  
  tree->SetBranchAddress("mu_phi",   &mu_phi);
  tree->SetBranchAddress("jet_timing",&jet_timing);  
  tree->SetBranchAddress("jet_pt",    &jet_pt);  
  tree->SetBranchAddress("jet_eta",   &jet_eta);  
  tree->SetBranchAddress("jet_phi",   &jet_phi);    
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
    for(const auto &key: *dir->GetListOfKeys())  fTrees.push_back(std::string(key->GetName()));
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
    for(unsigned iSys=0; iSys<fSystNames.size(); ++iSys){
      if(fTrees.at(i).find(fSystNames.at(iSys))!=std::string::npos){
	fSystName = fSystNames.at(iSys);
	break;
      }
    }
    log() << "Read - Running systematic: " << fSystName <<std::endl;
    
    //
    // Read common ntuples
    //
    Init(rtree);
    ReadTree(rtree); // Processes the events
    
  }
  file->Close();
  //
  // remove the trees afterward to search the next file
  //
  if(autoDiscovery) fTrees.clear();
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
  bool isMC = (treeName.find("data")==std::string::npos);
  
  Event alg_evt;
  
  for(int i = 0; i < nevent; i++) {
    //
    // Clear event
    //
    event->Clear();

    // read in tree
    rtree->GetEntry(i);

    // Fill event
    for(unsigned a=0; a<fVarVec.size(); ++a){
      event->AddVar(fVarVec.at(a).var, fVarVec.at(a).GetVal());
    }
    event->RunNumber = fRunNumber;
    event->isMC = isMC;

    // identify the sample
    if(!isMC){
      event->sample = Mva::kData;
      event->SetWeight(fWeight);
    }else{
      event->SetWeight((fWeight*fLumi));      
      if(fCurrRunNumber!=fRunNumber){
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
    }


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

    // Fill Jets
    for(unsigned iJet=0; iJet<jet_pt->size(); ++iJet){
      RecParticle new_jet;
      new_jet.pt  = jet_pt->at(iJet)/1.0e3;
      new_jet.eta = jet_eta->at(iJet);
      new_jet.phi = jet_phi->at(iJet);
      new_jet.AddVar(Mva::timing,jet_timing->at(iJet));
      event->jets.push_back(new_jet);
    }    
    
    // convert variables to GeV
    event->Convert2GeV(fVarMeV);

    // Fill MET
    if(event->HasVar(Mva::met_tst_phi))
      event->met.SetPtEtaPhiM(event->GetVar(Mva::met_tst_et),0.0,event->GetVar(Mva::met_tst_phi),0.0);
    

    // Fill remaining variables
    FillEvent(*event);

    if(i % 10000 == 0 && i > 0) {
      cout << "Processed " << setw(10) << right << i << " events" << endl; 
    }

    ++fCountEvents;
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
    event.AddVar(Mva::j0timing,event.jets.at(0).GetVar(Mva::timing));
  }
  if(event.jets.size()>1){
    event.AddVar(Mva::jetPt1,  event.jets.at(1).pt);
    event.AddVar(Mva::j1timing,event.jets.at(1).GetVar(Mva::timing));
    event.AddVar(Mva::etaj0TimesEtaj1,event.jets.at(0).eta*event.jets.at(1).eta);
  }
  // electrons
  if(event.electrons.size()>0){
    event.AddVar(Mva::lepPt0,  event.electrons.at(0).pt);
    event.AddVar(Mva::lepCh0,  event.electrons.at(0).GetVar(Mva::charge));
    TLorentzVector W = event.electrons.at(0).GetLVec()+event.met;
    event.AddVar(Mva::mt, W.M());    
  }
  if(event.electrons.size()>1){
    event.AddVar(Mva::lepPt1,  event.electrons.at(1).pt);
    event.AddVar(Mva::lepCh1,  event.electrons.at(1).GetVar(Mva::charge));
    TLorentzVector Z = (event.electrons.at(1).GetLVec()+event.electrons.at(0).GetLVec());
    event.AddVar(Mva::mll,  Z.M());
    event.AddVar(Mva::ptll, Z.Pt());        
  }
  // muons
  if(event.muons.size()>0){
    event.AddVar(Mva::lepPt0,  event.muons.at(0).pt);
    event.AddVar(Mva::lepCh0,  event.muons.at(0).GetVar(Mva::charge));
    TLorentzVector W = event.muons.at(0).GetLVec()+event.met;
    event.AddVar(Mva::mt, W.M());    
  }
  if(event.muons.size()>1){
    event.AddVar(Mva::lepPt1, event.muons.at(1).pt);
    event.AddVar(Mva::lepCh1, event.muons.at(1).GetVar(Mva::charge));
    TLorentzVector Z = (event.muons.at(1).GetLVec()+event.muons.at(0).GetLVec());
    event.AddVar(Mva::mll,  Z.M());
    event.AddVar(Mva::ptll, Z.Pt());    
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
  if(fDebug) {
    top_event.Print();
  }
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
