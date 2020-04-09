#define slimSkim_cxx

#include "slimSkim.h"
#include <TH2.h>
#include <TStyle.h>

void slimSkim::Begin(TTree * /*tree*/)
{

 TString option = GetOption();

}

void slimSkim::SlaveBegin(TTree * /*tree*/)
{

 TString option = GetOption();
 std::vector<std::string> options = getTokens(option, ",");
 nentries = std::stoi(string(options.at(0)));
 TString outputDir = options.at(1);
 TString output = options.at(2);
 istringstream(options.at(3)) >> std::boolalpha >> debug;

   // create file
 std::cout << "Output file: " << TString(outputDir+"/"+output+".root").Data() << std::endl;
 m_outfile = new TFile(TString(outputDir+"/"+output+".root").Data(),"RECREATE");

   //book minitree
 newtree = new TTree("nominal", "nominal");
 BookMinitree();

}

Bool_t slimSkim::Process(Long64_t entry)
{

 fReader.SetLocalEntry(entry);
 if (entry % 10000 == 0) Info("Process", "Processing event %d", (Int_t)entry);


   // speed up
  Bool_t saveMe = ( (*njets) > 1 && jet_pt[0] >= 60e3 && jet_pt[1] >= 40e3);
  saveMe &= ( (*jj_mass) > 200e3 && (*jj_deta) > 2.5 && (*jj_dphi)<2.4);
  saveMe &= ( (*met_et) > 100e3 || (*met_nolep_et) > 100e3);
  saveMe = true;
  if (saveMe){
    FillMinitree();
    newtree->Fill();
  }


 return kTRUE;
}

void slimSkim::SlaveTerminate()
{

 m_outfile->Write();
 m_outfile->Close();

}

void slimSkim::Terminate()
{

}

void slimSkim::BookMinitree()
{
  newtree->Branch("w", &newtree_w);
  newtree->Branch("runNumber", &newtree_runNumber);
  newtree->Branch("eventNumber", &newtree_eventNumber);
  newtree->Branch("jj_deta", &newtree_jj_deta);
  newtree->Branch("jj_dphi", &newtree_jj_dphi);
  newtree->Branch("jj_mass", &newtree_jj_mass);
  newtree->Branch("n_jet", &newtree_n_jet);
  newtree->Branch("n_jet25", &newtree_n_jet25);
  newtree->Branch("n_jet30", &newtree_n_jet30);
  newtree->Branch("n_jet35", &newtree_n_jet35);
  newtree->Branch("n_jet40", &newtree_n_jet40);
  newtree->Branch("n_jet50", &newtree_n_jet50);
  newtree->Branch("jet_pt", &newtree_jet_pt);
  newtree->Branch("jet_eta", &newtree_jet_eta);
  newtree->Branch("met_et", &newtree_met_et);
  newtree->Branch("met_phi",&newtree_met_phi);
  newtree->Branch("met_nolep_et", &newtree_met_nolep_et);
  newtree->Branch("met_nolep_et_ReCalc", &newtree_met_nolep_et_ReCalc);
  newtree->Branch("n_el", &newtree_n_el);
  newtree->Branch("el_pt", &newtree_el_pt);
  newtree->Branch("el_eta", &newtree_el_eta);
  newtree->Branch("el_charge", &newtree_el_charge);
  newtree->Branch("n_mu", &newtree_n_mu);
  newtree->Branch("mu_pt", &newtree_mu_pt);
  newtree->Branch("mu_eta", &newtree_mu_eta);
  newtree->Branch("mu_charge", &newtree_mu_charge);
  newtree->Branch("n_nu", &newtree_n_nu);
  newtree->Branch("nu_pt", &newtree_nu_pt);
  newtree->Branch("nu_eta", &newtree_nu_eta);
  newtree->Branch("nu_pdgid", &newtree_nu_pdgid);
  newtree->Branch("n_boson", &newtree_n_boson);
  newtree->Branch("boson_pt", &newtree_boson_pt);
  newtree->Branch("boson_eta", &newtree_boson_eta);
  newtree->Branch("boson_pdgid", &newtree_boson_pdgid);
  newtree->Branch("mll", &newtree_mll);
  newtree->Branch("met_significance", &newtree_met_significance);
  newtree->Branch("lep_jet_dR", &newtree_lep_jet_dR);

  newtree->Branch("ee_pt", &newtree_ee_pt);
  newtree->Branch("ee_eta", &newtree_ee_eta);
  newtree->Branch("ee_phi", &newtree_ee_phi);
  newtree->Branch("ee_m", &newtree_ee_m);
  newtree->Branch("mumu_pt", &newtree_mumu_pt);
  newtree->Branch("mumu_eta", &newtree_mumu_eta);
  newtree->Branch("mumu_phi", &newtree_mumu_phi);
  newtree->Branch("mumu_m", &newtree_mumu_m);
  newtree->Branch("nunu_pt", &newtree_nunu_pt);
  newtree->Branch("nunu_eta", &newtree_nunu_eta);
  newtree->Branch("nunu_phi", &newtree_nunu_phi);
  newtree->Branch("nunu_m", &newtree_nunu_m);


  Info("SlaveBegin", "Booked minitree");
}

void slimSkim::FillMinitree()
{

  newtree_jet_pt.clear();
  newtree_jet_eta.clear();
  newtree_el_pt.clear();
  newtree_el_charge.clear();
  newtree_el_eta.clear();
  newtree_mu_pt.clear();
  newtree_mu_eta.clear();
  newtree_mu_charge.clear();
  newtree_nu_pt.clear();
  newtree_nu_eta.clear();
  newtree_nu_pdgid.clear();
  newtree_lep_jet_dR.clear();
  newtree_boson_pt.clear();
  newtree_boson_pdgid.clear();
  newtree_boson_eta.clear();

  newtree_w = *w;
  newtree_runNumber = *runNumber;
  newtree_eventNumber = *eventNumber;
  newtree_jj_deta = *jj_deta;
  newtree_jj_dphi = *jj_dphi;
  newtree_jj_mass = *jj_mass;
  newtree_met_et = *met_et;
  newtree_met_nolep_et = *met_nolep_et;

  // Njets
  int njet25=0, njet30=0, njet35=0, njet40=0, njet50=0;
  for(auto j : jet_pt){
    if(j > 25e3) njet25++;
    if(j > 30e3) njet30++;
    if(j > 35e3) njet35++;
    if(j > 40e3) njet40++;
    if(j > 50e3) njet50++;
  }
  newtree_n_jet25 = njet25;
  newtree_n_jet30 = njet30;
  newtree_n_jet35 = njet35;
  newtree_n_jet40 = njet40;
  newtree_n_jet50 = njet50;

  // Mll
  double mll_tmp=-1;
  Double_t ee_m(-9999), ee_pt(-9999), ee_eta(-9999), ee_phi(-9999);
  Double_t mumu_m(-9999), mumu_pt(-9999), mumu_eta(-9999), mumu_phi(-9999);
  Double_t nunu_m(-9999), nunu_pt(-9999), nunu_eta(-9999), nunu_phi(-9999);

  TLorentzVector el_tlv[2];
  if (el_pt.GetSize() > 1){
    for(int i=0; i<2; i++) el_tlv[i].SetPtEtaPhiM(el_pt[i], el_eta[i], el_phi[i], electron_mass);
      TLorentzVector lep_sum = el_tlv[0] + el_tlv[1];
    mll_tmp = (lep_sum).M();
    ee_pt  = (lep_sum).Pt();
    ee_eta = (lep_sum).Eta();
    ee_phi = (lep_sum).Phi();
    ee_m   = (lep_sum).M();
  }

  TLorentzVector mu_tlv[2];
  if (mu_pt.GetSize() > 1){
   for(int i=0; i<2; i++) mu_tlv[i].SetPtEtaPhiM(mu_pt[i], mu_eta[i], mu_phi[i], muon_mass);
    TLorentzVector lep_sum = mu_tlv[0] + mu_tlv[1];
  mll_tmp = (lep_sum).M();
  mumu_pt  = (lep_sum).Pt();
  mumu_eta = (lep_sum).Eta();
  mumu_phi = (lep_sum).Phi();
  mumu_m   = (lep_sum).M();
}

  TLorentzVector nu_tlv[2];
  if (nu_pt.GetSize() > 1){
   for(int i=0; i<2; i++) nu_tlv[i].SetPtEtaPhiM(nu_pt[i], nu_eta[i], nu_phi[i], nu_mass);
    TLorentzVector lep_sum = nu_tlv[0] + nu_tlv[1];
  mll_tmp = (lep_sum).M();
  nunu_pt  = (lep_sum).Pt();
  nunu_eta = (lep_sum).Eta();
  nunu_phi = (lep_sum).Phi();
  nunu_m   = (lep_sum).M();
}

if(mll_tmp)
  newtree_mll = mll_tmp;

newtree_ee_pt  = ee_pt ;
newtree_ee_eta = ee_eta;
newtree_ee_phi = ee_phi;
newtree_ee_m   = ee_m  ;

newtree_mumu_pt  = mumu_pt ;
newtree_mumu_eta = mumu_eta;
newtree_mumu_phi = mumu_phi;
newtree_mumu_m   = mumu_m  ;

newtree_nunu_pt  = nunu_pt ;
newtree_nunu_eta = nunu_eta;
newtree_nunu_phi = nunu_phi;
newtree_nunu_m   = nunu_m  ;

if(debug) std::cout << "Mass ll=" << mll_tmp << ", ee=" << ee_m << ", mumu=" << mumu_m << ", nunu=" << nunu_m << std::endl;
int njets=0;
for (uint iJet = 0; iJet < jet_pt.GetSize(); ++iJet)
  if(jet_pt[iJet]>25e3 && fabs(jet_eta[iJet])<4.5){
   newtree_jet_pt.push_back(jet_pt[iJet]);
   newtree_jet_eta.push_back(jet_eta[iJet]);
   if(debug) std::cout << "jet" << iJet << " / " <<newtree_jet_pt.size()  << ", pt=" << jet_pt[iJet]*1e-3 << ", eta=" << jet_eta[iJet] << std::endl;
   njets++;
 }
 newtree_n_jet = njets;

 Float_t px = 0;
 Float_t py = 0;
 int nel=0;
 for (uint iEl = 0; iEl < el_pt.GetSize(); ++iEl)
   if(el_pt[iEl]>10e3 && fabs(el_eta[iEl])<2.5){
     newtree_el_pt.push_back(el_pt[iEl]);
     newtree_el_charge.push_back(el_charge[iEl]);
     newtree_el_eta.push_back(el_eta[iEl]);
     px += el_pt[iEl] * TMath::Cos(el_phi[iEl]);
     py += el_pt[iEl] * TMath::Sin(el_phi[iEl]);
     if(debug) std::cout << "el" << iEl << " , pt=" << el_pt[iEl]*1e-3 << ", eta=" << el_eta[iEl] << std::endl;
     nel++;
   }
   newtree_n_el = nel;
   int nmu=0;
   for (uint iMu = 0; iMu < mu_pt.GetSize(); ++iMu)
     if(mu_pt[iMu]>10e3 && fabs(mu_eta[iMu])<2.5){
       newtree_mu_pt.push_back(mu_pt[iMu]);
       newtree_mu_charge.push_back(mu_charge[iMu]);
       newtree_mu_eta.push_back(mu_eta[iMu]);
       px += mu_pt[iMu] * TMath::Cos(mu_phi[iMu]);
       py += mu_pt[iMu] * TMath::Sin(mu_phi[iMu]);
       if(debug) std::cout << "mu" << iMu << " , pt=" << mu_pt[iMu]*1e-3 << ", eta=" << mu_eta[iMu] << std::endl;
       nmu++;
     }
     newtree_n_mu = nmu;
     Float_t mpx = *met_et*TMath::Cos(*met_phi) + px;
     Float_t mpy = *met_et*TMath::Sin(*met_phi) + py;
     Float_t new_met_nolep = TMath::Sqrt(mpx*mpx+mpy*mpy);
     newtree_met_nolep_et_ReCalc = new_met_nolep;

     Float_t px_nu = 0;
     Float_t py_nu = 0;
     int nnu=0;
     for (uint inu = 0; inu < nu_pt.GetSize(); ++inu)
       if(nu_pt[inu]>10e3 && fabs(nu_eta[inu])<2.5){
         newtree_nu_pt.push_back(nu_pt[inu]);
	 //         newtree_nu_pdgid.push_back(nu_pdgid[inu]);
         newtree_nu_eta.push_back(nu_eta[inu]);
         px_nu += nu_pt[inu] * TMath::Cos(nu_phi[inu]);
         py_nu += nu_pt[inu] * TMath::Sin(nu_phi[inu]);
         if(debug) std::cout << "nu" << inu << " , pt=" << nu_pt[inu]*1e-3 << ", eta=" << nu_eta[inu] << std::endl;
         nnu++;
       }
       newtree_n_nu = nnu;

       int nboson=0;
       for (uint iboson = 0; iboson < boson_pt.GetSize(); ++iboson)
       {
         newtree_boson_pt.push_back(boson_pt[iboson]);
         newtree_boson_pdgid.push_back(boson_pdgid[iboson]);
         newtree_boson_eta.push_back(boson_eta[iboson]);
         if(debug) std::cout << "boson" << iboson << " , pt=" << boson_pt[iboson]*1e-3 << ", eta=" << boson_eta[iboson] << std::endl;
         nboson++;
       }
       newtree_n_boson = nboson;

       Float_t new_met_nu = TMath::Sqrt(px_nu*px_nu+py_nu*py_nu);
       newtree_met_significance = *met_significance;

       for (uint ilep_jet = 0; ilep_jet < lep_jet_dR.GetSize(); ++ilep_jet)
       {
         newtree_lep_jet_dR.push_back(lep_jet_dR[ilep_jet]);
       }

     }
