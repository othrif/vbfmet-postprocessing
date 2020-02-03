int checkduplicates(){

  //  TFile *f= TFile::Open("/share/t3data2/schae/PileupStudies/Jan29/mc16e/v37ETight/data.root","READ");
  TFile *f= TFile::Open("/share/t3data2/schae/PileupStudies/Jan29/mc16a/v37ATight/data.root","READ");
  //TFile *f= TFile::Open("/share/t3data2/schae/PileupStudies/Jan29/mc16d/v37DTight/data.root","READ");
  TTree *t = static_cast<TTree *>(f->Get("dataNominal"));

  std::set<ULong64_t> evts;
  std::map<unsigned, std::set<ULong64_t> > runmap;

  Int_t runNumber=0;
  ULong64_t eventNumber=0;
  t->SetBranchAddress("runNumber",&runNumber);
  t->SetBranchAddress("eventNumber",&eventNumber);
  unsigned totalEvt = t->GetEntries();
  std::cout << "Processing events: " << totalEvt << std::endl;
  for (unsigned i=0; i<totalEvt; ++i){
    t->GetEntry(i);
    if(runmap.find(runNumber)==runmap.end()){

      std::set<ULong64_t> evtsNew;
      runmap[runNumber]=evtsNew;
      runmap[runNumber].insert(eventNumber);
    }else{
      if(runmap[runNumber].find(eventNumber)!=runmap[runNumber].end()) {

	std::cout << "we have a duplicate!: " << runNumber << " evt: " << eventNumber << std::endl;
      }
      runmap[runNumber].insert(eventNumber);
    }
  }
  
  std::cout << "Runs: " << runmap.size() << std::endl;
  return 1;
}
