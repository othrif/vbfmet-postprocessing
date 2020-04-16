#ifndef slimSkim_h
#define slimSkim_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

// Headers needed by this particular selector
#include <vector>

#define muon_mass             105.6583715   // in MeV
#define electron_mass         0.510998928   // in MeV
#define nu_mass         0   // in MeV

class slimSkim : public TSelector {
   public :

   TFile *m_outfile; //!

   TTreeReader     fReader;  //!the tree reader
   TTree          *fChain = 0;   //!pointer to the analyzed TTree or TChain
   TTree          *newtree; //!
   bool           debug; //!
   Int_t nentries; //!
   //Analysis Methods
   void BookMinitree();
   void FillMinitree();

   Float_t         newtree_w;
   UInt_t          newtree_runNumber;
   ULong64_t       newtree_eventNumber;
   Int_t           newtree_n_jet;
   Int_t           newtree_n_el;
   Int_t           newtree_n_mu;
   Int_t           newtree_n_nu;
   Int_t           newtree_n_boson;
   Float_t         newtree_jj_mass;
   Float_t         newtree_jj_deta;
   Float_t         newtree_jj_dphi;
   Float_t         newtree_met_et;
   Float_t         newtree_met_nolep_et;
   Float_t         newtree_met_nolep_et_ReCalc;
   Float_t         newtree_met_phi;
   Float_t         newtree_met_nolep_phi;
   vector<float>   newtree_mu_charge;
   vector<float>   newtree_mu_pt;
   vector<float>   newtree_el_charge;
   vector<float>   newtree_el_pt;
   vector<float>   newtree_mu_phi;
   vector<float>   newtree_el_phi;
   vector<float>   newtree_mu_eta;
   vector<float>   newtree_el_eta;
   vector<float>   newtree_jet_pt;
   vector<float>   newtree_jet_eta;
   vector<float>   newtree_jet_phi;
   vector<float>   newtree_jet_E;
   vector<float>   newtree_nu_pt;
   vector<float>   newtree_nu_eta;
   vector<float>   newtree_nu_phi;
   vector<int>   newtree_nu_pdgid;
   vector<float>   newtree_boson_m;
   vector<float>   newtree_boson_pt;
   vector<float>   newtree_boson_eta;
   vector<float>   newtree_boson_phi;
   vector<float>   newtree_boson_pdgid;
   vector<float>   newtree_j3_centrality;
   vector<float>   newtree_j3_dRj1;
   vector<float>   newtree_j3_dRj2;
   vector<float>   newtree_j3_minDR;
   vector<float>   newtree_j3_mjclosest;
   vector<float>   newtree_j3_min_mj;
   vector<float>   newtree_j3_min_mj_over_mjj;
   vector<float>           newtree_lep_jet_dR;
   Float_t         newtree_mj34;
   Float_t         newtree_max_j_eta;
   Int_t           newtree_n_jet25;
   Int_t           newtree_n_jet30;
   Int_t           newtree_n_jet35;
   Int_t           newtree_n_jet40;
   Int_t           newtree_n_jet50;
   Double_t        newtree_mll;
   Float_t         newtree_met_significance;

   Double_t newtree_ee_pt ;
   Double_t newtree_ee_eta;
   Double_t newtree_ee_phi;
   Double_t newtree_ee_m  ;

   Double_t newtree_mumu_pt ;
   Double_t newtree_mumu_eta;
   Double_t newtree_mumu_phi;
   Double_t newtree_mumu_m  ;

   Double_t newtree_nunu_pt ;
   Double_t newtree_nunu_eta;
   Double_t newtree_nunu_phi;
   Double_t newtree_nunu_m  ;

   // Readers to access the data (delete the ones you do not need).
   TTreeReaderValue<Float_t> w = {fReader, "w"};
   TTreeReaderValue<UInt_t> runNumber = {fReader, "runNumber"};
   TTreeReaderValue<ULong64_t> eventNumber = {fReader, "eventNumber"};
   TTreeReaderValue<Int_t> njets = {fReader, "njets"};
   TTreeReaderValue<Int_t> nels = {fReader, "nels"};
   TTreeReaderValue<Int_t> nmus = {fReader, "nmus"};
   TTreeReaderValue<Int_t> nnus = {fReader, "nnus"};
   TTreeReaderValue<Float_t> jj_mass = {fReader, "jj_mass"};
   TTreeReaderValue<Float_t> jj_deta = {fReader, "jj_deta"};
   TTreeReaderValue<Float_t> jj_dphi = {fReader, "jj_dphi"};
   TTreeReaderValue<Float_t> met_et = {fReader, "met_et"};
   TTreeReaderValue<Float_t> met_nolep_et = {fReader, "met_nolep_et"};
   TTreeReaderValue<Float_t> met_phi = {fReader, "met_phi"};
   TTreeReaderValue<Float_t> met_nolep_phi = {fReader, "met_nolep_phi"};
   TTreeReaderArray<float> mu_charge = {fReader, "mu_charge"};
   TTreeReaderArray<float> mu_pt = {fReader, "mu_pt"};
   TTreeReaderArray<float> el_charge = {fReader, "el_charge"};
   TTreeReaderArray<float> el_pt = {fReader, "el_pt"};
   TTreeReaderArray<float> mu_phi = {fReader, "mu_phi"};
   TTreeReaderArray<float> el_phi = {fReader, "el_phi"};
   TTreeReaderArray<float> mu_eta = {fReader, "mu_eta"};
   TTreeReaderArray<float> el_eta = {fReader, "el_eta"};
   TTreeReaderArray<float> jet_pt = {fReader, "jet_pt"};
   TTreeReaderArray<float> jet_eta = {fReader, "jet_eta"};
   TTreeReaderArray<float> jet_phi = {fReader, "jet_phi"};
   TTreeReaderArray<float> jet_E = {fReader, "jet_E"};
   TTreeReaderValue<Float_t> met_significance = {fReader, "met_significance"};
   TTreeReaderArray<float> lep_jet_dR = {fReader, "lep_jet_dR"};
   TTreeReaderArray<float> boson_m = {fReader, "boson_m"};
   TTreeReaderArray<float> boson_pt = {fReader, "boson_pt"};
   TTreeReaderArray<float> boson_phi = {fReader, "boson_phi"};
   TTreeReaderArray<float> boson_eta = {fReader, "boson_eta"};
   TTreeReaderArray<int> boson_pdgid = {fReader, "boson_pdgid"};
   TTreeReaderArray<float> nu_pt = {fReader, "nu_pt"};
   TTreeReaderArray<float> nu_phi = {fReader, "nu_phi"};
   TTreeReaderArray<float> nu_eta = {fReader, "nu_eta"};
   TTreeReaderArray<float> nu_pdgid = {fReader, "nu_pdgid"};
   TTreeReaderValue<Float_t> mll = {fReader, "mll"};
   TTreeReaderValue<Bool_t> hasZ = {fReader, "hasZ"};


   slimSkim(TTree * /*tree*/ =0) { }
   virtual ~slimSkim() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();
   std::vector<std::string> getTokens(TString line, TString delim);

   ClassDef(slimSkim,0);

};

#endif

#ifdef slimSkim_cxx
void slimSkim::Init(TTree *tree)
{

   fReader.SetTree(tree);
}

Bool_t slimSkim::Notify()
{
   return kTRUE;
}

std::vector<std::string> slimSkim::getTokens(TString line, TString delim)
{
   std::vector<std::string> vtokens;
   TObjArray *              tokens = TString(line).Tokenize(delim); // delimiters
   if (tokens->GetEntriesFast()) {
      TIter       iString(tokens);
      TObjString *os = 0;
      while ((os = (TObjString *)iString())) {
         vtokens.push_back(os->GetString().Data());
      }
   }
   delete tokens;
   return vtokens;
}

#endif // #ifdef slimSkim_cxx
