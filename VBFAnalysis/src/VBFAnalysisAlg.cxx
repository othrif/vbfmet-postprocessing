// VBFAnalysis includes
#include "VBFAnalysisAlg.h"
#include "SUSYTools/SUSYCrossSection.h"
#include "PathResolver/PathResolver.h"
//#include "xAODEventInfo/EventInfo.h"




VBFAnalysisAlg::VBFAnalysisAlg( const std::string& name, ISvcLocator* pSvcLocator ) : AthAnalysisAlgorithm( name, pSvcLocator ){

  //declareProperty( "Property", m_nProperty = 0, "My Example Integer Property" ); //example property declaration

}


VBFAnalysisAlg::~VBFAnalysisAlg() {}


StatusCode VBFAnalysisAlg::initialize() {
  ATH_MSG_INFO ("Initializing " << name() << "...");
  //
  //This is called once, before the start of the event loop
  //Retrieves of tools you have configured in the joboptions go here
  //
  
  bool isMC = true;
  currentVariation = "Nominal";
  cout<<"NAME of input tree in intialize ======="<<currentVariation<<endl;
  //  cout<<"NAME of output before ======="<<newtree->GetName()<<endl;                                                                                                                                             
  currentSample = "ttbar";
  cout<< "CURRENT  sample === "<< currentSample<<endl;

  TString histoName="";
  histoName = "_" + currentSample;
  cout<<"currentVariation.substr(currentVariation.find_first_of(_)+1); "<<currentVariation.substr(currentVariation.find_first_of("_")+1)<<endl;
  //double crossSection;
  if(isMC){
    //SUSY::CrossSectionDB *my_XsecDB;
      std::string xSecFilePath = "dev/PMGTools/PMGxsecDB_mc15.txt";
      xSecFilePath = PathResolverFindCalibFile(xSecFilePath);
      my_XsecDB = new SUSY::CrossSectionDB(xSecFilePath);
  }//iSMC
  else  {
      if(runNumber >= 276262 && runNumber <= 284484) is2015 =true;
      else if(runNumber >= 296939 && runNumber <= 311481) is2016 =true;
      else throw std::invalid_argument("runNumber could not be identified with a dataset :o");
  }//Not MC 

  //Create new output TTree
  m_tree_out = new TTree(treeNameOut, treeTitleOut);
  m_tree_out->Branch("met_tst_et", &met_tst_et);
  m_tree_out->Branch("xs", &crossSection);
  m_tree_out->Branch("weight",&weight); 
  //Register the output TTree 
  CHECK(histSvc()->regTree("/MYSTREAM/nominal",m_tree_out));

  MapNgen(); //fill std::map with dsid->Ngen 

  return StatusCode::SUCCESS;
}

StatusCode VBFAnalysisAlg::finalize() {
  ATH_MSG_INFO ("Finalizing " << name() << "...");
  //
  //Things that happen once at the end of the event loop go here
  //


  return StatusCode::SUCCESS;
}

StatusCode VBFAnalysisAlg::MapNgen(){
  TFile *f = new TFile("f_out_total.root","READ");
  h_Gen = (TH1F*) f->Get("h_total");
  if(!h_Gen)ATH_MSG_WARNING("Number of events not found");

  for(int i=1; i<=h_Gen->GetNbinsX();i++){
    TString tmp = h_Gen->GetXaxis()->GetBinLabel(i);
    int dsid = tmp.Atoi(); 
    float N = h_Gen->GetBinContent(i); 
    Ngen[dsid]=N; 
   }
  
  return StatusCode::SUCCESS; 

}

StatusCode VBFAnalysisAlg::execute() {  
  ATH_MSG_DEBUG ("Executing " << name() << "...");
  //setFilterPassed(false); //optional: start with algorithm not passed
  m_tree->GetEntry(m_tree->GetReadEntry());

  crossSection = my_XsecDB->xsectTimesEff(runNumber);//xs in pb 
  if(Ngen[runNumber]>0)  weight = crossSection/Ngen[runNumber]; 
  else ATH_MSG_WARNING("Ngen " << Ngen[runNumber] << " dsid " << runNumber ); 

  if (met_tst_et < 150e3) return StatusCode::SUCCESS;
  m_tree_out->Fill();
  //  if (!(passGRL) || !(trigger_decision)) return StatusCode::SUCCESS;

  //setFilterPassed(true); //if got here, assume that means algorithm passed
  return StatusCode::SUCCESS;
}

StatusCode VBFAnalysisAlg::beginInputFile() { 
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

  m_treeName = "MiniNtuple";
  m_tree = static_cast<TTree*>(currentFile()->Get(m_treeName));
  m_tree->SetBranchStatus("*",0);
  m_tree->SetBranchStatus("runNumber", 1);
  m_tree->SetBranchStatus("averageIntPerXing", 1);
  m_tree->SetBranchStatus("mcEventWeight", 1);
  m_tree->SetBranchStatus("puWeight", 1);
  m_tree->SetBranchStatus("jvtSFWeight", 1);
  m_tree->SetBranchStatus("elSFWeight", 1);
  m_tree->SetBranchStatus("muSFWeight", 1);
  m_tree->SetBranchStatus("elSFTrigWeight", 1);
  m_tree->SetBranchStatus("muSFTrigWeight", 1);
  m_tree->SetBranchStatus("trigger_HLT_mu*", 1);
  m_tree->SetBranchStatus("trigger_HLT_e*", 1);
  m_tree->SetBranchStatus("trigger_HLT_xe*", 1);
  m_tree->SetBranchStatus("passJetClean", 1);
  m_tree->SetBranchStatus("passJetCleanTight", 1);
  m_tree->SetBranchStatus("muSFWeight", 1);
  m_tree->SetBranchStatus("muSFWeight", 1);
  m_tree->SetBranchStatus("muSFWeight", 1);
  m_tree->SetBranchStatus("met_tst_et", 1);
  // m_tree->SetBranchStatus("", 1);
  // m_tree->SetBranchStatus("", 1);
  // m_tree->SetBranchStatus("", 1);
  // m_tree->SetBranchStatus("", 1);
  // m_tree->SetBranchStatus("", 1);
  // m_tree->SetBranchStatus("", 1);
  
  m_tree->SetBranchAddress("runNumber", &runNumber);
  m_tree->SetBranchAddress("averageIntPerXing", &averageIntPerXing);
  m_tree->SetBranchAddress("mcEventWeight", &mcEventWeight);
  m_tree->SetBranchAddress("puWeight", &puWeight);
  m_tree->SetBranchAddress("jvtSFWeight", &jvtSFWeight);
  m_tree->SetBranchAddress("elSFWeight", &elSFWeight);
  m_tree->SetBranchAddress("muSFWeight", &muSFWeight);
  m_tree->SetBranchAddress("elSFTrigWeight", &elSFTrigWeight);
  m_tree->SetBranchAddress("muSFTrigWeight", &muSFTrigWeight);
  //  m_tree->SetBranchAddress("trigger_HLT_mu*", );
  //  m_tree->SetBranchAddress("trigger_HLT_e*", 1);
  //  m_tree->SetBranchAddress("trigger_HLT_xe*", 1);
  m_tree->SetBranchAddress("passJetClean", &passJetClean);
  m_tree->SetBranchAddress("passJetCleanTight", &passJetCleanTight);
  m_tree->SetBranchAddress("met_tst_et", &met_tst_et);
  
  return StatusCode::SUCCESS;
}

