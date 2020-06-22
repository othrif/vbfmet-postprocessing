/// This script converts loose photons to photons, applies the fake rates, and it prepares ntuples with the correct format
// To run this, it only takes the ntuple name and produces a new ntuple
// root -l -q makeJetFakePh.C\(\"data\"\,\"A\"\)
// if you run with data, then set the letter to the period that you are running: A, D, E
// The code assumes that the input files are in a directory called /tmp/v41Agam/
// The output is an ntuple that can be used to make the normal selections called  /tmp/smallJdata.root

/// fake rates loose photon passing the full selection
std::vector<float> getFakeWeight(float pt, float eta){
  std::vector<float> out;
  float fr=0.0;
  float stat=0.0;
  float wind=0.0;
  float bkg=0.0;
  float en=0.0;
  if(fabs(eta)<=0.8){
    if(pt<15.0e3)       { fr=0.0147; stat=0.0000; wind=0.0016; bkg=0.0025; en=0.0015; }
    else if(pt<25.0e3) 	{ fr=0.0147; stat=0.0000; wind=0.0016; bkg=0.0025; en=0.0015; }
    else if(pt<35.0e3) 	{ fr=0.0147; stat=0.0000; wind=0.0016; bkg=0.0025; en=0.0015; }
    else if(pt<45.0e3) 	{ fr=0.0172; stat=0.0000; wind=0.0003; bkg=0.0003; en=0.0007; }
    else if(pt<55.0e3) 	{ fr=0.0161; stat=0.0000; wind=0.0004; bkg=0.0014; en=0.0015; }
    else if(pt<65.0e3) 	{ fr=0.0188; stat=0.0001; wind=0.0007; bkg=0.0007; en=0.0010; }
    else if(pt<75.0e3) 	{ fr=0.0199; stat=0.0001; wind=0.0007; bkg=0.0008; en=0.0014; }
    else if(pt<100.0e3)	{ fr=0.0188; stat=0.0002; wind=0.0001; bkg=0.0022; en=0.0016; }
    else if(pt<150.0e3)	{ fr=0.0190; stat=0.0003; wind=0.0003; bkg=0.0029; en=0.0012; }
    else if(pt<250.0e3)	{ fr=0.0217; stat=0.0006; wind=0.0012; bkg=0.0002; en=0.0010; }
  }else if(fabs(eta)<=1.15){
    if(pt<15.0e3)      { fr=0.0183; stat=0.0001; wind=0.0016; bkg=0.0015; en=0.0033; }
    else if(pt<25.0e3) { fr=0.0183; stat=0.0001; wind=0.0016; bkg=0.0015; en=0.0033; }
    else if(pt<35.0e3) { fr=0.0183; stat=0.0001; wind=0.0016; bkg=0.0015; en=0.0033; }
    else if(pt<45.0e3) { fr=0.0198; stat=0.0000; wind=0.0004; bkg=0.0008; en=0.0005; }
    else if(pt<55.0e3) { fr=0.0196; stat=0.0001; wind=0.0005; bkg=0.0006; en=0.0018; }
    else if(pt<65.0e3) { fr=0.0211; stat=0.0001; wind=0.0000; bkg=0.0014; en=0.0010; }
    else if(pt<75.0e3) { fr=0.0233; stat=0.0003; wind=0.0005; bkg=0.0010; en=0.0015; }
    else if(pt<100.0e3){ fr=0.0215; stat=0.0003; wind=0.0001; bkg=0.0026; en=0.0019; }
    else if(pt<150.0e3){ fr=0.0223; stat=0.0005; wind=0.0003; bkg=0.0029; en=0.0013; }    
    else if(pt<250.0e3){ fr=0.0240; stat=0.0010; wind=0.0012; bkg=0.0003; en=0.0013; }
  }else if(fabs(eta)<=1.37){
    if(pt<15.0e3)      { fr=0.0256; stat=0.0001; wind=0.0007; bkg=0.0008; en=0.0019; }
    else if(pt<25.0e3) { fr=0.0256; stat=0.0001; wind=0.0007; bkg=0.0008; en=0.0019; }
    else if(pt<35.0e3) { fr=0.0256; stat=0.0001; wind=0.0007; bkg=0.0008; en=0.0019; }
    else if(pt<45.0e3) { fr=0.0291; stat=0.0001; wind=0.0009; bkg=0.0008; en=0.0017; }
    else if(pt<55.0e3) { fr=0.0278; stat=0.0001; wind=0.0004; bkg=0.0009; en=0.0029; }
    else if(pt<65.0e3) { fr=0.0303; stat=0.0002; wind=0.0008; bkg=0.0010; en=0.0028; }
    else if(pt<75.0e3) { fr=0.0303; stat=0.0004; wind=0.0007; bkg=0.0016; en=0.0029; }
    else if(pt<100.0e3){ fr=0.0315; stat=0.0005; wind=0.0010; bkg=0.0020; en=0.0023; }
    else if(pt<150.0e3){ fr=0.0301; stat=0.0002; wind=0.0000; bkg=0.0034; en=0.0031; }    
    else if(pt<250.0e3){ fr=0.0319; stat=0.0015; wind=0.0002; bkg=0.0023; en=0.0020; }
  }else if(fabs(eta)<=1.81){
    if(pt<15.0e3)      { fr=0.0363; stat=0.0001; wind=0.0005; bkg=0.0008; en=0.0009; }
    else if(pt<25.0e3) { fr=0.0363; stat=0.0001; wind=0.0005; bkg=0.0008; en=0.0009; }
    else if(pt<35.0e3) { fr=0.0363; stat=0.0001; wind=0.0005; bkg=0.0008; en=0.0009; }
    else if(pt<45.0e3) { fr=0.0379; stat=0.0001; wind=0.0001; bkg=0.0008; en=0.0014; }
    else if(pt<55.0e3) { fr=0.0372; stat=0.0001; wind=0.0005; bkg=0.0002; en=0.0035; }
    else if(pt<65.0e3) { fr=0.0398; stat=0.0003; wind=0.0003; bkg=0.0013; en=0.0036; }
    else if(pt<75.0e3) { fr=0.0411; stat=0.0002; wind=0.0000; bkg=0.0001; en=0.0038; }
    else if(pt<100.0e3){ fr=0.0418; stat=0.0005; wind=0.0007; bkg=0.0020; en=0.0042; }
    else if(pt<150.0e3){ fr=0.0439; stat=0.0009; wind=0.0002; bkg=0.0033; en=0.0058; }    
    else if(pt<250.0e3){ fr=0.0437; stat=0.0018; wind=0.0005; bkg=0.0040; en=0.0025; }
  }else if(fabs(eta)<=2.01){
    if(pt<15.0e3)      { fr=0.0443; stat=0.0002; wind=0.0002; bkg=0.0003; en=0.0019; }
    else if(pt<25.0e3) { fr=0.0443; stat=0.0002; wind=0.0002; bkg=0.0003; en=0.0019; }
    else if(pt<35.0e3) { fr=0.0443; stat=0.0002; wind=0.0002; bkg=0.0003; en=0.0019; }
    else if(pt<45.0e3) { fr=0.0471; stat=0.0001; wind=0.0001; bkg=0.0004; en=0.0017; }
    else if(pt<55.0e3) { fr=0.0477; stat=0.0002; wind=0.0003; bkg=0.0002; en=0.0023; }
    else if(pt<65.0e3) { fr=0.0530; stat=0.0004; wind=0.0012; bkg=0.0012; en=0.0023; }
    else if(pt<75.0e3) { fr=0.0519; stat=0.0007; wind=0.0003; bkg=0.0003; en=0.0025; }
    else if(pt<100.0e3){ fr=0.0536; stat=0.0008; wind=0.0008; bkg=0.0016; en=0.0039; }
    else if(pt<150.0e3){ fr=0.0556; stat=0.0015; wind=0.0005; bkg=0.0028; en=0.0050; }   
    else if(pt<250.0e3){ fr=0.0543; stat=0.0029; wind=0.0011; bkg=0.0022; en=0.0051; }   
  }else if(fabs(eta)<=2.37){
    if(pt<15.0e3)      { fr=0.0657; stat=0.0002; wind=0.0026; bkg=0.0005; en=0.0028; }
    else if(pt<25.0e3) { fr=0.0657; stat=0.0002; wind=0.0026; bkg=0.0005; en=0.0028; }
    else if(pt<35.0e3) { fr=0.0657; stat=0.0002; wind=0.0026; bkg=0.0005; en=0.0028; }
    else if(pt<45.0e3) { fr=0.0741; stat=0.0001; wind=0.0033; bkg=0.0005; en=0.0035; }
    else if(pt<55.0e3) { fr=0.0772; stat=0.0002; wind=0.0048; bkg=0.0004; en=0.0039; }
    else if(pt<65.0e3) { fr=0.0826; stat=0.0005; wind=0.0026; bkg=0.0003; en=0.0046; }
    else if(pt<75.0e3) { fr=0.0855; stat=0.0008; wind=0.0027; bkg=0.0004; en=0.0050; }
    else if(pt<100.0e3){ fr=0.0862; stat=0.0009; wind=0.0059; bkg=0.0028; en=0.0047; }
    else if(pt<150.0e3){ fr=0.0833; stat=0.0016; wind=0.0050; bkg=0.0025; en=0.0050; }    
    else if(pt<250.0e3){ fr=0.0906; stat=0.0035; wind=0.0051; bkg=0.0027; en=0.0060; }
  }
  // output
  out.push_back(fr);
  out.push_back(stat);
  out.push_back(wind);
  out.push_back(bkg);
  out.push_back(en);
  return out;
}

//----
void correctMET(TVector3 &metv, TLorentzVector jetv,bool add){
  TVector3 jetvm = jetv.Vect();
  if(add){
    metv+=jetvm;
  }else{
    metv-=jetvm;
  }
}

bool passMETSelection(TLorentzVector jet, float jvt){
  if(jet.Pt()<20e3) return false;
  if(fabs(jet.Eta())>2.4) return true;
  if(fabs(jvt)<=0.5 && jet.Pt()<60e3) return false;
  return true;
}

void makeJetFakePh(std::string treeNmae="data", std::string period="A") {
  // Example of Root macro to copy a subset of a Tree to a new Tree
  // Only selected entries are copied to the new Tree.
  // The input file has been generated by the program in $ROOTSYS/test/Event
  // with   Event 1000 1 99 1

  //Get old file, old tree and set top branch address
  //TFile *oldfile = new TFile("/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Loose/v37ALoose/Z_strong.root");
  std::string oldfileNmae="/tmp/"+treeNmae+".root";
  TFile *oldfile = new TFile(oldfileNmae.c_str());
  std::string oldtreeNmae=treeNmae+"Nominal";
  TTree *oldtree = (TTree*)oldfile->Get(oldtreeNmae.c_str());
  Long64_t nentries = oldtree->GetEntries();

  // turn off weights
  for(const auto &pleaf : *(oldtree->GetListOfLeaves())){
    std::string leafName = pleaf->GetName();
    if(leafName.size()>1 && leafName[0]==string("w")){
      oldtree->SetBranchStatus(leafName.c_str(),0);
      std::cout << "Turned off: " << leafName << std::endl;
    }
  }

  float scaleWeight=1.0;
  if(treeNmae.find("data")!=std::string::npos){
    if(period=="A") scaleWeight/=36207.66;
    if(period=="D") scaleWeight/=44307.4;
    if(period=="E") scaleWeight/=58450.1;
  }else{// subtracting the MC
    scaleWeight*=-1.0;
  }
  
  std::vector<float> copy_el_pt;
  std::vector<float> copy_el_phi;
  std::vector<float> copy_el_eta;
  std::vector<float> copy_baseel_pt;
  std::vector<float> copy_baseel_phi;
  std::vector<float> copy_baseel_eta;
  
  std::vector<float> *el_pt=new std::vector<float>();
  std::vector<float> *el_phi=new std::vector<float>();  
  std::vector<float> *el_eta=new std::vector<float>();
  std::vector<float> *baseel_pt=new std::vector<float>();
  std::vector<float> *baseel_phi=new std::vector<float>();  
  std::vector<float> *baseel_eta=new std::vector<float>(); 
  std::vector<float> *ph_phi=new std::vector<float>();
  std::vector<float> *ph_eta=new std::vector<float>();
  std::vector<float> *ph_pt=new std::vector<float>();
  std::vector<float> *jet_phi=new std::vector<float>();
  std::vector<float> *jet_eta=new std::vector<float>();
  std::vector<float> *jet_pt=new std::vector<float>();

  // additional photon variables
  std::vector<unsigned> *ph_isEM=new std::vector<unsigned>();
  std::vector<bool>     *ph_iso=new std::vector<bool>();  
  std::vector<int>      *ph_truthOrigin=new std::vector<int>();  
  std::vector<int>      *ph_truthType=new std::vector<int>();
  std::vector<float>    *ph_topoetcone40=new std::vector<float>();
  std::vector<float>    *ph_ptcone20=new std::vector<float>();
  // base photons
  std::vector<unsigned> *baseph_isEM=new std::vector<unsigned>();
  std::vector<bool> *baseph_iso=new std::vector<bool>();  
  std::vector<int> *baseph_truthOrigin=new std::vector<int>();  
  std::vector<int> *baseph_truthType=new std::vector<int>();
  std::vector<float> *baseph_phi=new std::vector<float>();
  std::vector<float> *baseph_eta=new std::vector<float>();
  std::vector<float> *baseph_pt=new std::vector<float>();
  std::vector<float> *baseph_topoetcone40=new std::vector<float>();
  std::vector<float> *baseph_ptcone20=new std::vector<float>();
  
  int runNumber   = 0;
  int n_baseel   = 0;
  int n_el   = 0;
  int n_el_w   = 0;
  int n_ph   = 0;
  int n_basemu   = 0;
  float met_truth_et=0;
  float met_tst_et=0;
  float met_tst_nolep_et=0;
  float met_tst_phi=0;
  float met_tst_nolep_phi=0;
  float SherpaVTruthPt=0;
  float ph_pointing_z=0;
  float truth_V_dressed_pt=0;
  double truth_jj_mass=0;
  float w=0.0;
  double met_tst_j1_dphi =0;
  double met_tst_j2_dphi =0;
  double met_tst_nolep_j1_dphi =0;
  double met_tst_nolep_j2_dphi =0;
  oldtree->SetBranchAddress("w",&w);
  oldtree->SetBranchAddress("runNumber",&runNumber);
  oldtree->SetBranchAddress("n_baseel",&n_baseel);
  oldtree->SetBranchAddress("n_el",&n_el);
  oldtree->SetBranchAddress("n_ph",&n_ph);
  oldtree->SetBranchAddress("el_pt",&el_pt);
  oldtree->SetBranchAddress("el_eta",&el_eta);
  oldtree->SetBranchAddress("el_phi",&el_phi);
  oldtree->SetBranchAddress("baseel_pt",&baseel_pt);
  oldtree->SetBranchAddress("baseel_eta",&baseel_eta);
  oldtree->SetBranchAddress("baseel_phi",&baseel_phi);
  
  oldtree->SetBranchAddress("jet_pt",&jet_pt);
  oldtree->SetBranchAddress("jet_eta",&jet_eta);
  oldtree->SetBranchAddress("jet_phi",&jet_phi);
  oldtree->SetBranchAddress("met_tst_j1_dphi",&met_tst_j1_dphi);
  oldtree->SetBranchAddress("met_tst_j2_dphi",&met_tst_j2_dphi);
  oldtree->SetBranchAddress("met_tst_nolep_j1_dphi",&met_tst_nolep_j1_dphi);
  oldtree->SetBranchAddress("met_tst_nolep_j2_dphi",&met_tst_nolep_j2_dphi);  

  // base photon inputs
  oldtree->SetBranchAddress("baseph_isEM",&baseph_isEM);
  oldtree->SetBranchAddress("baseph_iso",&baseph_iso);
  oldtree->SetBranchAddress("baseph_truthOrigin",&baseph_truthOrigin);
  oldtree->SetBranchAddress("baseph_truthType",&baseph_truthType);
  oldtree->SetBranchAddress("baseph_topoetcone40",&baseph_topoetcone40);
  oldtree->SetBranchAddress("baseph_ptcone20",&baseph_ptcone20);
  oldtree->SetBranchAddress("baseph_pt",&baseph_pt);  
  oldtree->SetBranchAddress("baseph_eta",&baseph_eta);
  oldtree->SetBranchAddress("baseph_phi",&baseph_phi);
  // input signal photons
  oldtree->SetBranchAddress("ph_isEM",&ph_isEM);
  oldtree->SetBranchAddress("ph_iso",&ph_iso);
  oldtree->SetBranchAddress("ph_truthOrigin",&ph_truthOrigin);
  oldtree->SetBranchAddress("ph_truthType",&ph_truthType);
  oldtree->SetBranchAddress("ph_topoetcone40",&ph_topoetcone40);
  oldtree->SetBranchAddress("ph_ptcone20",&ph_ptcone20);
  oldtree->SetBranchAddress("ph_pt",&ph_pt);  
  oldtree->SetBranchAddress("ph_pointing_z",&ph_pointing_z);
  oldtree->SetBranchAddress("ph_eta",&ph_eta);
  oldtree->SetBranchAddress("ph_phi",&ph_phi);
  oldtree->SetBranchAddress("n_el_w",&n_el_w);
  oldtree->SetBranchAddress("n_basemu",&n_basemu);
  oldtree->SetBranchAddress("met_truth_et",&met_truth_et);
  oldtree->SetBranchAddress("met_tst_et",&met_tst_et);
  oldtree->SetBranchAddress("met_tst_nolep_et",&met_tst_nolep_et);
  oldtree->SetBranchAddress("met_tst_phi",&met_tst_phi);
  oldtree->SetBranchAddress("met_tst_nolep_phi",&met_tst_nolep_phi);
  
  oldtree->SetBranchAddress("truth_jj_mass",&truth_jj_mass);
  oldtree->SetBranchAddress("truth_V_dressed_pt",&truth_V_dressed_pt);
  oldtree->SetBranchAddress("SherpaVTruthPt",&SherpaVTruthPt);

  //Create a new file + a clone of old tree in new file
  std::string outfileName="/tmp/smallJ"+treeNmae+".root";
  TFile *newfile = new TFile(outfileName.c_str(),"recreate");
  TTree *newtree = oldtree->CloneTree(0);
  newtree->SetName("JetFakePhNominal");
  newtree->SetTitle("JetFakePhNominal");
  float wJetFakePhTight3__1up = 0.0;
  float wJetFakePhTight5__1up = 0.0;
  float wJetFakePhWindow__1up = 0.0;
  float wJetFakePhWindow__1down = 0.0;
  float wJetFakePhStat__1up = 0.0;
  float wJetFakePhStat__1down = 0.0;
  float wJetFakePhBkgSub__1up = 0.0;
  float wJetFakePhBkgSub__1down = 0.0;
  float wJetFakePhEn__1up = 0.0;
  float wJetFakePhEn__1down = 0.0;  
    
  newtree->Branch("wJetFakePhTight3__1up",&wJetFakePhTight3__1up);
  newtree->Branch("wJetFakePhTight5__1up",&wJetFakePhTight5__1up);
  newtree->Branch("wJetFakePhWindow__1up",&wJetFakePhWindow__1up);  
  newtree->Branch("wJetFakePhWindow__1down",&wJetFakePhWindow__1down);
  newtree->Branch("wJetFakePhStat__1up",&wJetFakePhStat__1up);
  newtree->Branch("wJetFakePhStat__1down",&wJetFakePhStat__1down);
  newtree->Branch("wJetFakePhBkgSub__1up",&wJetFakePhBkgSub__1up);
  newtree->Branch("wJetFakePhBkgSub__1down",&wJetFakePhBkgSub__1down);
  newtree->Branch("wJetFakePhEn__1up",&wJetFakePhEn__1up);
  newtree->Branch("wJetFakePhEn__1down",&wJetFakePhEn__1down);  
  TVector3 met,met_nolep,newel,jet1,jet2;

  // Use tight-4 and 3 and 5 are used for systematic uncertainties
  //tight-3:Fside,∆E,ws
  //tight-4:Fside,∆E,ws3,Eratio
  //tight-5:Fside,∆E,ws3,Eratio,wst
  // pass tight iso
  const int fside  = 0x080000;
  const int ws3    = 0x100000;
  const int deltaE = 0x020000;
  const int Eratio = 0x200000;
  const int wst    = 0x040000;
  const int tight3Mask = fside+ws3+deltaE;
  const int tight4Mask = fside+ws3+deltaE+Eratio;
  const int tight5Mask = fside+ws3+deltaE+Eratio+wst;
  TLorentzVector vjet,vphoton;
  
  for (Long64_t i=0;i<nentries; i++) {
    if((i%100000)==0) std::cout <<"evt: " << i << std::endl;
    oldtree->GetEntry(i);
    // require 0 signal photons
    if (!(n_ph==0 && baseph_pt))  continue;

    for(unsigned iph=0; iph<baseph_pt->size(); ++iph){
      //if (n_ph==0 && baseph_pt && baseph_pt->size()==1){// extrapolating from a base photon with selection X
      //ph_pointing_z=0.0;//setting arbitrary 0 because this is an electron with vertex confirmation, so it should pass.. load vtxpos. should already be set to the leading base photon for n_ph=0

      // apply the selections that we want. maybe label them?
      // note that these base photons are not in the MET, so we may need to correct for that. it's a tough question because the isolation wouldn't be included for the cross-checks
      // could move to EM scale although that is also problematic
      // start by setting the selections for various loosened PID requirements
      int baseph_isEM_tight3 = baseph_isEM->at(iph);
      int baseph_isEM_tight4 = baseph_isEM->at(iph);
      int baseph_isEM_tight5 = baseph_isEM->at(iph);
      // setting bit to 0 for the selections. If the value is greater than zero, then remove it! This applies all bits but those that are loosened.
      baseph_isEM_tight3 |= tight3Mask; baseph_isEM_tight3 ^= tight3Mask;
      baseph_isEM_tight4 |= tight4Mask; baseph_isEM_tight4 ^= tight4Mask;
      baseph_isEM_tight5 |= tight5Mask; baseph_isEM_tight5 ^= tight5Mask;

      // pass isolation, make sure only the required bits are loosened. Make sure one of the loosened bits fired.
      bool istight3iso = (baseph_iso->at(iph) && (baseph_isEM_tight3==0) && ((baseph_isEM->at(iph) & tight3Mask) >0));
      bool istight4iso = (baseph_iso->at(iph) && (baseph_isEM_tight4==0) && ((baseph_isEM->at(iph) & tight4Mask) >0));
      bool istight5iso = (baseph_iso->at(iph) && (baseph_isEM_tight5==0) && ((baseph_isEM->at(iph) & tight5Mask) >0));
      // selecting tight4+isolation
      if(!(istight4iso || istight3iso || istight5iso)) continue;
      // if this is MC, then clean it up to require that it is a real photon. Removing fakes from mesons like pi0->gamgam
      bool isPromptPhoton = (baseph_truthOrigin->at(iph)==39 || baseph_truthOrigin->at(iph)==40 || baseph_truthOrigin->at(iph)<22); // includes e->gam fakes from MC
      //bool isPromptPhoton = (baseph_truthType->at(iph)<15);
      if(scaleWeight<0.0 && !isPromptPhoton) continue;
      unsigned newisEM = 0;
      if(istight3iso) newisEM+=0x1;
      if(istight4iso) newisEM+=0x2;
      if(istight5iso) newisEM+=0x4;
      
      n_ph=1;
      runNumber=-1; // setting to arbitrary number
      // clear
      ph_pt->clear();
      ph_eta->clear();
      ph_phi->clear();
      // filling
      ph_pt->push_back(baseph_pt->at(iph));
      ph_eta->push_back(baseph_eta->at(iph));
      ph_phi->push_back(baseph_phi->at(iph));
      if(ph_isEM){                                 ph_isEM->clear();         ph_isEM->push_back(newisEM); } // setting this to values 3,4,5 for the tight varied inputs
      if(ph_truthOrigin && baseph_truthOrigin){    ph_truthOrigin->clear();  ph_truthOrigin->push_back(baseph_truthOrigin->at(iph)); }
      if(ph_truthType && baseph_truthType){        ph_truthType->clear();    ph_truthType->push_back(baseph_truthType->at(iph)); }
      if(ph_topoetcone40 && baseph_topoetcone40) { ph_topoetcone40->clear(); ph_topoetcone40->push_back(baseph_topoetcone40->at(iph)); }
      if(ph_ptcone20 && baseph_ptcone20) {         ph_ptcone20->clear();     ph_ptcone20->push_back(baseph_ptcone20->at(iph)); }
      // acceptance cuts
      if(fabs(ph_eta->at(0))>1.37 && fabs(ph_eta->at(0))<1.52) continue;
      if(ph_pt->at(0)<15e3) continue;
      
      //add electron
      std::vector<float> new_fake_w=getFakeWeight(ph_pt->at(0),ph_eta->at(0));
      float wold = w*scaleWeight;
      w*=new_fake_w.at(0)*scaleWeight;
      if(!istight4iso) w=0.0;
      if(istight5iso) wJetFakePhTight5__1up=wold*(new_fake_w.at(0));
      else wJetFakePhTight5__1up=0.0;
      if(istight3iso) wJetFakePhTight3__1up=wold*(new_fake_w.at(0));
      else wJetFakePhTight3__1up=0.0;
      
      wJetFakePhWindow__1up   =wold*(new_fake_w.at(0)+new_fake_w.at(1));
      wJetFakePhWindow__1down =wold*(new_fake_w.at(0)-new_fake_w.at(1));
      wJetFakePhStat__1up     =wold*(new_fake_w.at(0)+new_fake_w.at(2));
      wJetFakePhStat__1down   =wold*(new_fake_w.at(0)-new_fake_w.at(2));
      wJetFakePhBkgSub__1up   =wold*(new_fake_w.at(0)+new_fake_w.at(3));
      wJetFakePhBkgSub__1down =wold*(new_fake_w.at(0)-new_fake_w.at(3));
      wJetFakePhEn__1up       =wold*(new_fake_w.at(0)+new_fake_w.at(4));
      wJetFakePhEn__1down     =wold*(new_fake_w.at(0)-new_fake_w.at(4));

      // checking the MET
      // step 1: does the photon overlap with a jet?
      //if(baseph_pt->at(iph)>20e3){
      //	vphoton.SetPtEtaPhiM(0.5*baseph_pt->at(iph),baseph_eta->at(iph), baseph_phi->at(iph),0.0);
      //	
      //}
      
      newtree->Fill();
    }
    //event->Clear();
  }
  newtree->Print();
  newtree->AutoSave();
  delete oldfile;
  delete newfile;
}
