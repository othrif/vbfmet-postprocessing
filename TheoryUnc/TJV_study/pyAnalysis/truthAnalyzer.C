#define truthAnalyzer_cxx


#include "truthAnalyzer.h"
#include <TH2.h>
#include <TStyle.h>


//bool debug = false;
void truthAnalyzer::Begin(TTree * /*tree*/)
{

 TString option = GetOption();
}

void truthAnalyzer::SlaveBegin(TTree * /*tree*/)
{
 TString option = GetOption();
 std::vector<std::string> options = getTokens(option, ",");
 nentries = std::stoi(string(options.at(0)));
 TString outputDir = options.at(1);
 TString output = options.at(2);
 lumi = 36.1;

  // create file
 TString subdir(outputDir);
 std::cout<<"subdir "<<subdir<<std::endl;
 system ("mkdir -p "+subdir);
 TString filename =  output;
 m_prooffile = new TProofOutputFile(TString(subdir+"/"+filename+".root").Data(), "LOCAL");
 m_outfile = m_prooffile->OpenFile("RECREATE");

    //book minitree
 newtree = new TTree("nominal", "nominal");
 BookMinitree();
}

Bool_t truthAnalyzer::Process(Long64_t entry)
{

   fProcessed++; // processed events
   fReader.SetEntry(entry);
   fStatus++; // selected events

  //if(fProcessed>nentries)
  //return kTRUE;

   if (fProcessed  == 0)
    Info("Process", "Started to process %d events...", nentries);
  else if ( fProcessed % 10000 == 0)
    Info("Process", "Processed %lld / %d events... ", fProcessed - 1, nentries);



   // speed up
  Bool_t saveMe = ( (*n_jet) > 1 && jet_pt[0] >= 60e3 && jet_pt[1] >= 40e3);
  saveMe &= ( (*jj_mass) > 200e3 && (*jj_deta) > 2.5 && (*jj_dphi)<2.4);
  saveMe &= ( (*met_et) > 100e3 || (*met_nolep_et) > 100e3);

  if (saveMe){
    FillMinitree();
    newtree->Fill();
  }

  return kTRUE;
}

void truthAnalyzer::SlaveTerminate()
{
   // save
  m_outfile->Write();
  m_outfile->Close();

   /*
 m_outfile->cd();
 newtree->Write();
 TDirectory *savedir = gDirectory;
 savedir->cd();
 m_prooffile->Print();
 fOutput->Add(m_prooffile);
 m_outfile->Close();*/
}

void truthAnalyzer::Terminate()
{

 if (!fInput) Info("Terminate", "processed %lld events", fProcessed);

}

void truthAnalyzer::BookMinitree()
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

  Info("SlaveBegin", "Booked minitree");
}

void truthAnalyzer::FillMinitree()
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

  // Processing
  // Njets
  int njet25=0, njet30=0, njet35=0, njet40=0, njet50=0;
  for(auto j : jet_pt){
    if(j > 25e3) njet25++;
    if(j > 30e3) njet30++;
    if(j > 35e3) njet35++;
    if(j > 40e3) njet40++;
    if(j > 50e3) njet50++;
  }
  // Mll
  double mll_tmp=-1;
  TLorentzVector el_tlv[2];
  if (el_pt.GetSize() > 1){
    for(int i=0; i<2; i++)
      el_tlv[i].SetPtEtaPhiM(el_pt[i], el_eta[i], el_phi[i], electron_mass);
    TLorentzVector lep_sum = el_tlv[0] + el_tlv[1];
    mll_tmp = (lep_sum).M();
  }
  //std::cout << "\nrunNumber/eventNumber: " <<  *runNumber << "/" << *eventNumber << std::endl;
  //std::cout << "Mll in ee: " << mll_tmp << ", num e pt's:" << el_pt.GetSize() << ", Nel:" << *n_el << std::endl;
  TLorentzVector mu_tlv[2];
  if (mu_pt.GetSize() > 1){
    for(int i=0; i<2; i++)
      mu_tlv[i].SetPtEtaPhiM(mu_pt[i], mu_eta[i], mu_phi[i], muon_mass);
    TLorentzVector lep_sum = mu_tlv[0] + mu_tlv[1];
    mll_tmp = (lep_sum).M();
  }
  //std::cout << "Mll in mm: " << mll_tmp << ", num mu pt's:" << mu_pt.GetSize() << ", Nmu:" << *n_mu << std::endl;
  // Filling
  newtree_w = *w;
  newtree_runNumber = *runNumber;
  newtree_eventNumber = *eventNumber;
  newtree_jj_deta = *jj_deta;
  newtree_jj_dphi = *jj_dphi;
  newtree_jj_mass = *jj_mass;
  //newtree_n_jet = *n_jet;
  newtree_n_jet25 = njet25;
  newtree_n_jet30 = njet30;
  newtree_n_jet35 = njet35;
  newtree_n_jet40 = njet40;
  newtree_n_jet50 = njet50;
  //newtree_jet_pt = {jet_pt.begin(), jet_pt.end()};
  //newtree_jet_eta = {jet_eta.begin(), jet_eta.end()};
  /*if( *runNumber == 308095){
    if(debug) std::cout << "\n*Znunu > ";
  }
  else if( *runNumber == 308092){
    if(debug) std::cout << "\n*Zee > ";
  }
  else if( *runNumber == 308093){
    if(debug) std::cout << "\n*Zmm > ";
  }
  else if( *runNumber == 308094){
    if(debug) std::cout << "\n*Ztt > ";
  }
*/

  int njets=0;
  for (int iJet = 0; iJet < jet_pt.GetSize(); ++iJet)
    if(jet_pt[iJet]>25e3 && fabs(jet_eta[iJet])<4.5){
      newtree_jet_pt.push_back(jet_pt[iJet]);
      newtree_jet_eta.push_back(jet_eta[iJet]);
      //if(debug) std::cout << "jet" << iJet << " , pt=" << jet_pt[iJet]*1e-3 << ", eta=" << jet_eta[iJet] << std::endl;
      njets++;
    }
    newtree_n_jet = njets;
    newtree_met_et = *met_et;
    newtree_met_nolep_et = *met_nolep_et;
  //newtree_el_pt = {el_pt.begin(), el_pt.end()};
  //newtree_el_charge = {el_charge.begin(), el_charge.end()};
    Float_t px = 0;
    Float_t py = 0;
    int nel=0;
    for (int iEl = 0; iEl < el_pt.GetSize(); ++iEl)
      if(el_pt[iEl]>7e3 && fabs(el_eta[iEl])<2.5){
        newtree_el_pt.push_back(el_pt[iEl]);
        newtree_el_charge.push_back(el_charge[iEl]);
        newtree_el_eta.push_back(el_eta[iEl]);
        px += el_pt[iEl] * TMath::Cos(el_phi[iEl]);
        py += el_pt[iEl] * TMath::Sin(el_phi[iEl]);
//        if(debug) std::cout << "el" << iEl << " , pt=" << el_pt[iEl]*1e-3 << ", eta=" << el_eta[iEl] << std::endl;
        nel++;
      }
      /*if(*n_el==0){
        newtree_el_charge = {0.,0.};
        newtree_el_pt = {0.,0.};
        newtree_el_eta = {0.,0.};
      }*/
      newtree_n_el = nel;
//  newtree_mu_pt = {mu_pt.begin(), mu_pt.end()};
//  newtree_mu_charge = {mu_charge.begin(), mu_charge.end()};
      int nmu=0;
      for (int iMu = 0; iMu < mu_pt.GetSize(); ++iMu)
        if(mu_pt[iMu]>7e3 && fabs(mu_eta[iMu])<2.5){
          newtree_mu_pt.push_back(mu_pt[iMu]);
          newtree_mu_charge.push_back(mu_charge[iMu]);
          newtree_mu_eta.push_back(mu_eta[iMu]);
          px += mu_pt[iMu] * TMath::Cos(mu_phi[iMu]);
          py += mu_pt[iMu] * TMath::Sin(mu_phi[iMu]);
//          if(debug) std::cout << "mu" << iMu << " , pt=" << mu_pt[iMu]*1e-3 << ", eta=" << mu_eta[iMu] << std::endl;
          nmu++;
        }
       /* if(*n_mu==0){
          newtree_mu_charge = {0.,0.};
          newtree_mu_pt = {0.,0.};
          newtree_mu_eta = {0.,0.};
        }*/
        newtree_n_mu = nmu;
          Float_t mpx = *met_et*TMath::Cos(*met_phi) + px;
          Float_t mpy = *met_et*TMath::Sin(*met_phi) + py;
          Float_t new_met_nolep = TMath::Sqrt(mpx*mpx+mpy*mpy);
          newtree_met_nolep_et_ReCalc = new_met_nolep;

    Float_t px_nu = 0;
    Float_t py_nu = 0;
        int nnu=0;
        for (int inu = 0; inu < nu_pt.GetSize(); ++inu)
          if(nu_pt[inu]>7e3 && fabs(nu_eta[inu])<2.5){
            newtree_nu_pt.push_back(nu_pt[inu]);
            newtree_nu_pdgid.push_back(nu_pdgid[inu]);
            newtree_nu_eta.push_back(nu_eta[inu]);
            px_nu += nu_pt[inu] * TMath::Cos(nu_phi[inu]);
            py_nu += nu_pt[inu] * TMath::Sin(nu_phi[inu]);
//            if(debug) std::cout << "nu" << inu << " , pt=" << nu_pt[inu]*1e-3 << ", eta=" << nu_eta[inu] << std::endl;
            nnu++;
          }
          newtree_n_nu = nnu;

        int nboson=0;
        for (int iboson = 0; iboson < boson_pt.GetSize(); ++iboson)
          if(boson_pt[iboson]>7e3 && fabs(boson_eta[iboson])<2.5){
            newtree_boson_pt.push_back(boson_pt[iboson]);
            newtree_boson_pdgid.push_back(boson_pdgid[iboson]);
            newtree_boson_eta.push_back(boson_eta[iboson]);
//            if(debug) std::cout << "boson" << iboson << " , pt=" << boson_pt[iboson]*1e-3 << ", eta=" << boson_eta[iboson] << std::endl;
            nboson++;
          }
          newtree_n_boson = nboson;

          Float_t new_met_nu = TMath::Sqrt(px_nu*px_nu+py_nu*py_nu);

           /* if( *runNumber == 308095){
              if(debug) std::cout << "MET=" << *met_et*1e-3 << ", MET noLep=" << *met_nolep_et*1e-3 << ", met nu's=" << new_met_nu*1e-3 << std::endl;
            }
            else if( *runNumber == 308092){
              if(debug) std::cout << "MET=" << *met_et*1e-3 << ", MET noLep=" << *met_nolep_et*1e-3 << ", met nu's=" << new_met_nu*1e-3 << std::endl;
            }
            else if( *runNumber == 308093){
              if(debug) std::cout << "*MET=" << *met_et*1e-3 << ", MET noLep=" << *met_nolep_et*1e-3 << ", met nu's=" << new_met_nu*1e-3 << std::endl;
            }
            else if( *runNumber == 308094){
              if(debug) std::cout << "*MET=" << *met_et*1e-3 << ", MET noLep=" << *met_nolep_et*1e-3 << ", met nu's=" << new_met_nu*1e-3  << std::endl;
            }*/

          newtree_mll = mll_tmp;
          newtree_met_significance = *met_significance;

          for (int ilep_jet = 0; ilep_jet < lep_jet_dR.GetSize(); ++ilep_jet)
          {
            newtree_lep_jet_dR.push_back(lep_jet_dR[ilep_jet]);
          }

        }
