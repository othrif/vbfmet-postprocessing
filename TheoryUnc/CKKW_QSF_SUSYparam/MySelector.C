#define MySelector_cxx
// The class definition in MySelector.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.

// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// Root > T->Process("MySelector.C")
// Root > T->Process("MySelector.C","some options")
// Root > T->Process("MySelector.C+")
//

#include "MySelector.h"
#include <TH2.h>
#include <TStyle.h>

#include <TH1.h>
#include <TVector2.h>
#include <TLorentzVector.h>
#include <TLegend.h>
#include <TCanvas.h>
#include <TPad.h>
#include <TROOT.h>
#include <algorithm>
#include <TMath.h>
#include <iostream>
#include <fstream>

Float_t bins_Mjj[] = { 400, 600, 800, 1000, 1500, 2000, 3500, 5000};
Int_t  binnum_Mjj = sizeof(bins_Mjj) / sizeof(Float_t) - 1;


void MySelector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
   suffix = option;
     // create file
   TString filename =  "outFile_" + suffix + ".root";
   m_prooffile = new TProofOutputFile(filename, "LOCAL");
   m_outfile = m_prooffile->OpenFile("RECREATE");

   regions.push_back("Incl");
   for (TString reg : {"","PhiHigh", "PhiLow", "Njet"}){
    regions.push_back("SR"+reg);
    regions.push_back("CRZ"+reg);
    regions.push_back("CRW"+reg);
   }

   samples.push_back("Z_strong");
   samples.push_back("W_strong");

   vjSysts.push_back("Nominal");
   vjSysts.push_back("weight_ckkw15");
   vjSysts.push_back("weight_ckkw30");
   vjSysts.push_back("weight_fac025");
   vjSysts.push_back("weight_fac4");
   vjSysts.push_back("weight_qsf025");
   vjSysts.push_back("weight_qsf4");
   vjSysts.push_back("weight_renorm025");
   vjSysts.push_back("weight_renorm4");

   for (TString region : regions) {
      for (TString sample : samples) {
         for (TString vjSyst : vjSysts){
            h_vjSyst[region][sample][vjSyst] = new TH1F("jj_mass_" + sample + "_" + region + "_" + vjSyst, "", binnum_Mjj, bins_Mjj);
            std::cout << "Name " <<   h_vjSyst[region][sample][vjSyst]->GetName() << std::endl;
         }
      }
   }

}

void MySelector::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();



}

Bool_t MySelector::Process(Long64_t entry)
{
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // It can be passed to either MySelector::GetEntry() or TBranch::GetEntry()
   // to read either all or the required parts of the data. When processing
   // keyed objects with PROOF, the object is already loaded and is available
   // via the fObject pointer.
   //
   // This function should contain the "body" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.



   fProcessed++; // processed events
   GetEntry(entry);
   fStatus++; // selected events

   if ((fProcessed - 1) == 0){
      nentries = fChain->GetEntries();
      Info("Process", "Started to process %d events...", nentries);
   }
   else if ((fProcessed - 1) % 100000 == 0)
      Info("Process", "Processed %lld / %d events... ", fProcessed - 1, nentries);

   // Assign samples
   for (TString sample : samples) b_samples[sample] = false;
      AssignRunToSamples();

   // Calculate variables needed
   // compute mll
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
  bool SR_lepVeto  = ((n_baseel == 0) && (n_mu_baseline_noOR == 0));
  bool We_lepVeto  = ((n_baseel == 1) && (n_mu_baseline_noOR == 0) && (n_el_w == 1));
  bool Wm_lepVeto  = ((n_baseel == 0) && (n_mu_baseline_noOR == 1) && (n_mu_w == 1));
  bool Zee_lepVeto = ((n_baseel == 2) && (n_mu_baseline_noOR == 0) && (n_el == 2));
  bool Zmm_lepVeto = ((n_baseel == 0) && (n_mu_baseline_noOR == 2) && (n_mu == 2));
  bool elPtCut = n_el>0 ? (el_pt->at(0)>30.0e3) : false;
  bool muPtCut = n_mu>0 ? (mu_pt->at(0)>30.0e3) : false;
  bool muSubPtCut = n_mu>1 ? (mu_pt->at(1)>7.0e3) : false;
  bool elSubPtCut = n_el>1 ? (el_pt->at(1)>7.0e3) : false;
  bool elChPos = n_el>0 ? (el_charge->at(0) > 0) : false;
  bool muChPos = n_mu>0 ? (mu_charge->at(0) > 0) : false;
  bool OppSignElCut = n_el>1 ? (el_charge->at(0)*el_charge->at(1) < 0) : false;
  bool OppSignMuCut = n_mu>1 ? (mu_charge->at(0)*mu_charge->at(1) < 0) : false;

   // Define regions
  Float_t met_to_use = 0;
  float METCut = 160.0e3;
  float LeadJetPtCut = 80.0e3;
  float subLeadJetPtCut = 50.0e3;
  float MjjCut =2e5;
  float DEtajjCut =3.8;
  float DPhijjCut =2.0;

  bool vbfSkim = (jet_pt->at(0) > LeadJetPtCut) & (jet_pt->at(1) > subLeadJetPtCut) && (jj_deta > DEtajjCut) && ((jet_eta->at(0) * jet_eta->at(1))<0) && (jj_mass > MjjCut) && (jj_dphi < DPhijjCut);

  isRegion["Incl"]  = kTRUE;

  isRegion["SRPhiHigh"]   = (vbfSkim && (n_jet == 2) && (1 <= jj_dphi && jj_dphi < 2.0)      && met_tst_et             > METCut && SR_lepVeto);
  isRegion["SRPhiLow"]    = (vbfSkim && (n_jet == 2) && (jj_dphi < 1.)                       && met_tst_et             > METCut && SR_lepVeto);
  isRegion["SRNjet"]      = (vbfSkim && (2 < n_jet && n_jet < 5)                             && met_tst_et             > METCut && SR_lepVeto);
  isRegion["SR"]          = (isRegion["SRPhiHigh"] || isRegion["SRPhiLow"] || isRegion["SRNjet"]);

  isRegion["CRZPhiHigh"]   = (vbfSkim && (n_jet == 2) && (1 <= jj_dphi && jj_dphi < 2.0)     && met_tst_nolep_et       > METCut && ( (Zee_lepVeto && OppSignElCut) || (Zmm_lepVeto && OppSignMuCut)) && (mll> 66.0e3 && mll<116.0e3) && (elPtCut || muPtCut) && (elSubPtCut || muSubPtCut) ) ;
  isRegion["CRZPhiLow"]    = (vbfSkim && (n_jet == 2) && (jj_dphi < 1.)                      && met_tst_nolep_et       > METCut && ( (Zee_lepVeto && OppSignElCut) || (Zmm_lepVeto && OppSignMuCut)) && (mll> 66.0e3 && mll<116.0e3) && (elPtCut || muPtCut) && (elSubPtCut || muSubPtCut) ) ;
  isRegion["CRZNjet"]      = (vbfSkim && (2 < n_jet && n_jet < 5)                            && met_tst_nolep_et       > METCut && ( (Zee_lepVeto && OppSignElCut) || (Zmm_lepVeto && OppSignMuCut)) && (mll> 66.0e3 && mll<116.0e3) && (elPtCut || muPtCut) && (elSubPtCut || muSubPtCut) ) ;
  isRegion["CRZ"]          = (isRegion["CRZPhiHigh"] || isRegion["CRZPhiLow"] || isRegion["CRZNjet"]);

  isRegion["CRWPhiHigh"]   = (vbfSkim && (n_jet == 2) && (1 <= jj_dphi && jj_dphi < 2.0)     && met_tst_nolep_et       > METCut && ( We_lepVeto || Wm_lepVeto) && (elPtCut || muPtCut) ) ;
  isRegion["CRWPhiLow"]    = (vbfSkim && (n_jet == 2) && (jj_dphi < 1.)                      && met_tst_nolep_et       > METCut && ( We_lepVeto || Wm_lepVeto) && (elPtCut || muPtCut) ) ;
  isRegion["CRWNjet"]      = (vbfSkim && (2 < n_jet && n_jet < 5)                            && met_tst_nolep_et       > METCut && ( We_lepVeto || Wm_lepVeto) && (elPtCut || muPtCut) ) ;
  isRegion["CRW"]          = (isRegion["CRWPhiHigh"] || isRegion["CRWPhiLow"] || isRegion["CRWNjet"]);


  for (TString region : regions)
   if(isRegion[region]){
      for (TString sample : samples)
         if (b_samples[sample]){
            for (TString vjSyst : vjSysts){
               Float_t w_vj_MC = 1;
               if ((fProcessed - 1) % 100000 == 0) Info("Process", "syst: %s",  std::string(vjSyst).c_str());
               if (vjSyst.Contains("Nominal")) w_vj_MC   = w;
               if (vjSyst.Contains("ckkw15")) w_vj_MC    = wvjets_ckkw15;
               if (vjSyst.Contains("ckkw30")) w_vj_MC    = wvjets_ckkw30;
               if (vjSyst.Contains("fac025")) w_vj_MC    = wvjets_fac025;
               if (vjSyst.Contains("fac4")) w_vj_MC      = wvjets_fac4;
               if (vjSyst.Contains("qsf025")) w_vj_MC    = wvjets_qsf025;
               if (vjSyst.Contains("qsf4")) w_vj_MC      = wvjets_qsf4;
               if (vjSyst.Contains("renorm025")) w_vj_MC = wvjets_renorm025;
               if (vjSyst.Contains("renorm4")) w_vj_MC   = wvjets_renorm4;
               if ((fProcessed - 1) % 100000 == 0) Info("Process", " %f",  w_vj_MC);

               h_vjSyst[region][sample][vjSyst]->Fill(jj_mass/1000 , w_vj_MC);
            }
         }
      }



      return kTRUE;
   }

   void MySelector::SlaveTerminate()
   {
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.

      for (TString region : regions) {
         for (TString sample : samples) {
            for (TString vjSyst : vjSysts){
               const Int_t nbinsx = h_vjSyst[region][sample][vjSyst]->GetNbinsX();
               const float overflow =  h_vjSyst[region][sample][vjSyst]->GetBinContent(nbinsx + 1);
               if (overflow > 0) {
                  const float last_bin =  h_vjSyst[region][sample][vjSyst]->GetBinContent(nbinsx);
                  h_vjSyst[region][sample][vjSyst]->SetBinContent(nbinsx, overflow + last_bin);
               }
            }
         }
      }


      WriteTable(suffix);

   // save
      m_outfile->Write();
      m_outfile->Close();
      TDirectory *savedir = gDirectory;
      savedir->cd();
//   m_prooffile->Print();
      fOutput->Add(m_prooffile);


   }

   void MySelector::Terminate()
   {
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

      if (!fInput) Info("Terminate", "processed %lld events", fProcessed);

   }


   void MySelector::WriteTable(TString suffix_)
   {


      ofstream outfile_vjSyst("python/Sherpa_syst_" + suffix_ + ".py");
      outfile_vjSyst << "evts = {}" << endl;

      if(std::find(vjSysts.begin(), vjSysts.end(), "Nominal") != vjSysts.end()){
         outfile_vjSyst.precision(10);
         for (TString sample : samples) {
            outfile_vjSyst << "evts[\'" << sample << "\'] = {} " << endl;
            for (TString region : regions) {
               for (Int_t b = 0; b < binnum_Mjj; b++) {
                  TString region_bin = TString::Format(region + "_%d", (Int_t)bins_Mjj[b]);
                  outfile_vjSyst << "evts[\'" << sample << "\'][\'" << region_bin << "\'] = {} " << endl;
                  for(TString vjSyst: vjSysts){
                   Double_t yield_syst = h_vjSyst[region][sample][vjSyst]->GetBinContent(b + 1);
                   Double_t err_syst = h_vjSyst[region][sample][vjSyst]->GetBinError(b + 1);
                   outfile_vjSyst << "evts[\'" << sample << "\'][\'" << region_bin << "\'][\'" << vjSyst << "\'] = [" << yield_syst << ", " << err_syst << "]" << endl;
                     } // end syst
                  } // end bins
               } // end regions
         } // end samples
      }
      outfile_vjSyst.close();
      cout << "Written python dictionary with vjets correction and uncertainties" << endl;
   }

   void MySelector::AssignRunToSamples()
   {

   if ( 308092 <= runNumber && runNumber <= 308095) // Zee,mm,tt,nn EWK
      b_samples["Z_EWK"]    = true;
   if ( 308096 <= runNumber && runNumber <= 308098) // We,m,t EWK
      b_samples["W_EWK"]    = true;
   if ( (364100 <= runNumber && runNumber <= 364141)) // Zee,mm,tt strong
      b_samples["Z_strong"] = true;
   if ( (364142 <= runNumber && runNumber <= 364155)) // Znn strong OLD
      b_samples["Z_strong"] = true;
  if ( (366010 <= runNumber && runNumber <= 366035)) // Znn strong NEW
   b_samples["Z_strong"] = true;
  if ( (364216 <= runNumber && runNumber <= 364223)) // Zee,mm,tt,nn PTV sliced
   b_samples["Z_strong"] = true;
   if ( (364156 <= runNumber && runNumber <= 364197)) // We,m,t strong
      b_samples["W_strong"] = true;
   if ( (364224 <= runNumber && runNumber <= 364229)) // We,m,t PTV sliced
      b_samples["W_strong"] = true;

   sample_name = "none";
   for (auto sample : b_samples) if (sample.second) {
      sample_name = sample.first;
      break;
   }

}


