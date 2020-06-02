/// This script converts electrons to photons, applies the fake rates, and it prepares ntuples with the correct format
// To run this, it only takes the ntuple name and produces a new ntuple
// root -l -q makeEFakePh.C\(\"Wg_strong\"\)
// The code assumes that the input files are in a directory called /tmp/v41Agam/
// The output is an ntuple that can be used to make the normal selections called  /tmp/smallWg_strong.root

// we collecting the TightLH electrons and we want to map the missing efficiency for MediumLH electrons that the fake rates are derived for.
// https://link.springer.com/content/pdf/10.1140/epjc/s10052-019-7140-6.pdf
float getTightEtoMedium(float pt, float eta){

  if(pt<20.0e3) return 1.2;
  else if(pt>70e3) return 1.06;
  // linearly correct from 20 to 70 GeV
  return 1.2 - (pt-20.0e3)*0.0028*0.001; 
  
  //return 1.13; //average correction for electron pT>15 GeV
}

/// fake rates for an electron with MediumLH+FCLoose -> Tight Photon + Tight Iso
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
  out.push_back(fr*getTightEtoMedium(pt,eta));
  out.push_back(stat);
  out.push_back(wind);
  out.push_back(bkg);
  out.push_back(en);
  return out;
}

void makeEFakePh(std::string treeNmae="Wg_strong") {
  // Example of Root macro to copy a subset of a Tree to a new Tree
  // Only selected entries are copied to the new Tree.
  // The input file has been generated by the program in $ROOTSYS/test/Event
  // with   Event 1000 1 99 1
  //Author: Rene Brun
  
  //gSystem->Load("$ROOTSYS/test/libEvent");

  //Get old file, old tree and set top branch address
  //TFile *oldfile = new TFile("/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Loose/v37ALoose/Z_strong.root");
  std::string oldfileNmae="/tmp/v41Agam/"+treeNmae+".root";
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
  std::string outfileName="/tmp/small"+treeNmae+".root";
  TFile *newfile = new TFile(outfileName.c_str(),"recreate");
  TTree *newtree = oldtree->CloneTree(0);
  newtree->SetName("EFakePhNominal");
  newtree->SetTitle("EFakePhNominal");
  float wEFakePhWindow__1up = 0.0;
  float wEFakePhWindow__1down = 0.0;
  float wEFakePhStat__1up = 0.0;
  float wEFakePhStat__1down = 0.0;
  float wEFakePhBkgSub__1up = 0.0;
  float wEFakePhBkgSub__1down = 0.0;
  float wEFakePhEn__1up = 0.0;
  float wEFakePhEn__1down = 0.0;  
    
  newtree->Branch("wEFakePhWindow__1up",&wEFakePhWindow__1up);
  newtree->Branch("wEFakePhWindow__1down",&wEFakePhWindow__1down);
  newtree->Branch("wEFakePhStat__1up",&wEFakePhStat__1up);
  newtree->Branch("wEFakePhStat__1down",&wEFakePhStat__1down);
  newtree->Branch("wEFakePhBkgSub__1up",&wEFakePhBkgSub__1up);
  newtree->Branch("wEFakePhBkgSub__1down",&wEFakePhBkgSub__1down);
  newtree->Branch("wEFakePhEn__1up",&wEFakePhEn__1up);
  newtree->Branch("wEFakePhEn__1down",&wEFakePhEn__1down);  
  TVector3 met,met_nolep,newel,jet1,jet2;
  for (Long64_t i=0;i<nentries; i++) {
    if((i%100000)==0) std::cout <<"evt: " << i << std::endl;
    oldtree->GetEntry(i); //n_baseel==0 && n_basemu==0 
    if (n_ph==0 && n_el==1 && n_el_w==1 && n_baseel==1){// extrapolating from the TightLH+FCLoose
      ph_pointing_z=0.0;//setting arbitrary 0 because this is an electron with vertex confirmation, so it should pass
      n_ph=1;
      n_el=0;
      n_el_w=0;
      n_baseel=0;
      ph_pt->push_back(el_pt->at(0));
      ph_eta->push_back(el_eta->at(0));
      ph_phi->push_back(el_phi->at(0));
      // acceptance cuts
      if(fabs(ph_eta->at(0))>1.37 && fabs(ph_eta->at(0))<1.52) continue;
      if(ph_pt->at(0)<10e3) continue;
      
      //add electron
      std::vector<float> new_fake_w=getFakeWeight(ph_pt->at(0),ph_eta->at(0));
      float wold = w;
      w*=new_fake_w.at(0);
      wEFakePhWindow__1up=wold*(new_fake_w.at(0)+new_fake_w.at(1));
      wEFakePhWindow__1down=wold*(new_fake_w.at(0)-new_fake_w.at(1));
      wEFakePhStat__1up=wold*(new_fake_w.at(0)+new_fake_w.at(2));
      wEFakePhStat__1down=wold*(new_fake_w.at(0)-new_fake_w.at(2));
      wEFakePhBkgSub__1up=wold*(new_fake_w.at(0)+new_fake_w.at(3));
      wEFakePhBkgSub__1down=wold*(new_fake_w.at(0)-new_fake_w.at(3));
      wEFakePhEn__1up=wold*(new_fake_w.at(0)+new_fake_w.at(4));
      wEFakePhEn__1down=wold*(new_fake_w.at(0)-new_fake_w.at(4));
      
      newel.SetPtEtaPhi(ph_pt->at(0),0.0,ph_phi->at(0));
      met.SetPtEtaPhi(met_tst_et,0.0,met_tst_phi);
      met_nolep.SetPtEtaPhi(met_tst_nolep_et,0.0,met_tst_nolep_phi);
      //met+=newel;
      //met_nolep+=newel;
      //met_tst_et=met.Pt();
      //met_tst_phi=met.Phi();
      //met_tst_nolep_et=met_nolep.Pt();
      //met_tst_nolep_phi=met_nolep.Phi();
      met_tst_nolep_et=met_tst_et;
      met_tst_nolep_phi=met_tst_phi;

      if(jet_pt->size()>1){
	jet1.SetPtEtaPhi(jet_pt->at(0),jet_eta->at(0),jet_phi->at(0));
	jet2.SetPtEtaPhi(jet_pt->at(1),jet_eta->at(1),jet_phi->at(1));
	met_tst_j1_dphi=fabs(jet1.DeltaPhi(met));
	met_tst_j2_dphi=fabs(jet2.DeltaPhi(met));
	met_tst_nolep_j1_dphi=fabs(jet1.DeltaPhi(met_nolep));
	met_tst_nolep_j2_dphi=fabs(jet2.DeltaPhi(met_nolep));	
      }
      
      el_pt->clear();
      el_eta->clear();
      el_phi->clear();
      baseel_pt->clear();
      baseel_eta->clear();
      baseel_phi->clear();      
      newtree->Fill();
    }else if (n_ph==0 && n_el==2 && n_baseel==2 && n_el_w==2){ // extrapolating from the TightLH+FCLoose
      for(unsigned iele=0; iele<2; ++iele){
	if(iele==0){
	  copy_el_pt = *el_pt;
	  copy_el_phi = *el_phi;
	  copy_el_eta = *el_eta;
	  copy_baseel_pt = *baseel_pt;
	  copy_baseel_phi = *baseel_phi;
	  copy_baseel_eta = *baseel_eta;
	}
	ph_pointing_z=0.0;//setting arbitrary 0 because this is an electron with vertex confirmation, so it should pass
	n_ph=1;
	n_el=1;
	n_el_w=1;
	n_baseel=1;
	ph_pt->push_back(copy_el_pt.at(iele));
	ph_eta->push_back(copy_el_eta.at(iele));
	ph_phi->push_back(copy_el_phi.at(iele));

	// rm crack
	if(fabs(ph_eta->at(0))>1.37 && fabs(ph_eta->at(0))<1.52) continue;
	if(ph_pt->at(0)<10e3) continue;
	
	//add electron
	std::vector<float> new_fake_w=getFakeWeight(ph_pt->at(0),ph_eta->at(0));
	float wold = w;
	w*=new_fake_w.at(0);
	wEFakePhWindow__1up=wold*(new_fake_w.at(0)+new_fake_w.at(1));
	wEFakePhWindow__1down=wold*(new_fake_w.at(0)-new_fake_w.at(1));
	wEFakePhStat__1up=wold*(new_fake_w.at(0)+new_fake_w.at(2));
	wEFakePhStat__1down=wold*(new_fake_w.at(0)-new_fake_w.at(2));
	wEFakePhBkgSub__1up=wold*(new_fake_w.at(0)+new_fake_w.at(3));
	wEFakePhBkgSub__1down=wold*(new_fake_w.at(0)-new_fake_w.at(3));
	wEFakePhEn__1up=wold*(new_fake_w.at(0)+new_fake_w.at(4));
	wEFakePhEn__1down=wold*(new_fake_w.at(0)-new_fake_w.at(4));
	newel.SetPtEtaPhi(ph_pt->at(0),0.0,ph_phi->at(0));
	met.SetPtEtaPhi(met_tst_et,0.0,met_tst_phi);
	met_nolep.SetPtEtaPhi(met_tst_nolep_et,0.0,met_tst_nolep_phi);
	//met+=newel;
	met_nolep+=newel;
	//met_tst_et=met.Pt();
	//met_tst_phi=met.Phi();
	met_tst_nolep_et=met_nolep.Pt();
	met_tst_nolep_phi=met_nolep.Phi();

	if(jet_pt->size()>1){
	  jet1.SetPtEtaPhi(jet_pt->at(0),jet_eta->at(0),jet_phi->at(0));
	  jet2.SetPtEtaPhi(jet_pt->at(1),jet_eta->at(1),jet_phi->at(1));
	  met_tst_j1_dphi=fabs(jet1.DeltaPhi(met));
	  met_tst_j2_dphi=fabs(jet2.DeltaPhi(met));
	  met_tst_nolep_j1_dphi=fabs(jet1.DeltaPhi(met_nolep));
	  met_tst_nolep_j2_dphi=fabs(jet2.DeltaPhi(met_nolep));	
	}

	el_pt->clear(); el_pt->push_back(copy_el_pt.at(iele));
	el_eta->clear(); el_eta->push_back(copy_el_eta.at(iele));
	el_phi->clear(); el_phi->push_back(copy_el_phi.at(iele));
	baseel_pt->clear(); baseel_pt->push_back(copy_baseel_pt.at(iele));
	baseel_eta->clear(); baseel_eta->push_back(copy_baseel_eta.at(iele));
	baseel_phi->clear();  baseel_phi->push_back(copy_baseel_phi.at(iele));
	
	newtree->Fill();
      }
    }
    //event->Clear();
  }
  newtree->Print();
  newtree->AutoSave();
  delete oldfile;
  delete newfile;
}
