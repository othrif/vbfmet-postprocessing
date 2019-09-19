#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include <iostream>
#include <vector>

int plotTruth()
{
  //TFile *fout = TFile::Open("365510b_VBFTruth_out.root","RECREATE");
  //TFile *fout = TFile::Open("enhanced_ptgam_out.root","RECREATE");
  TFile *fout = TFile::Open("mc.365520_ptgam15_out.root","RECREATE");
  //TFile *fout = TFile::Open("mc.366000_ptgam15_out.root","RECREATE");    
  //TFile *fout = TFile::Open("365500_VBFTruth_out.root","RECREATE");  
  TH1F *hph_pt = new TH1F("ph_pt","ph_pt",500, 0.0,1000.0);
  hph_pt->Sumw2(1);
  hph_pt->SetDirectory(fout);
  TH1F *hph_pt_lead = new TH1F("ph_pt_lead","ph_pt_lead",500, 0.0,1000.0);
  hph_pt_lead->Sumw2(1);
  hph_pt_lead->SetDirectory(fout);
  TH1F *hph_eta_lead = new TH1F("ph_eta_lead","ph_eta_lead",90, -4.5,4.5);
  hph_eta_lead->Sumw2(1);
  hph_eta_lead->SetDirectory(fout);

  TH2F *hph_pt_vs_w = new TH2F("ph_pt_vs_w","ph_pt_vs_w",100, 0.0,500.0,100,-20.0,20.0);
  hph_pt_vs_w->Sumw2(1);
  hph_pt_vs_w->SetDirectory(fout);

  TH2F *helneg_pt_vs_w = new TH2F("elneg_pt_vs_w","elneg_pt_vs_w",100, 0.0,500.0,100,-20.0,20.0);
  helneg_pt_vs_w->Sumw2(1);
  helneg_pt_vs_w->SetDirectory(fout);
  TH2F *helpos_pt_vs_w = new TH2F("elpos_pt_vs_w","elpos_pt_vs_w",100, 0.0,500.0,100,-20.0,20.0);
  helpos_pt_vs_w->Sumw2(1);
  helpos_pt_vs_w->SetDirectory(fout);
  
  TH1F *hph_eta = new TH1F("ph_eta","ph_eta",90, -4.5,4.5);
  hph_eta->Sumw2(1);
  hph_eta->SetDirectory(fout);

  TH1F *helneg_pt = new TH1F("elneg_pt","elneg_pt",500, 0.0,1000.0);
  helneg_pt->Sumw2(1);
  helneg_pt->SetDirectory(fout);
  TH1F *helpos_pt = new TH1F("elpos_pt","elpos_pt",500, 0.0,1000.0);
  helpos_pt->Sumw2(1);
  helpos_pt->SetDirectory(fout);  
  
  TH1F *hboson_eta = new TH1F("boson_eta","boson_eta",90, -4.5,4.5);
  hboson_eta->Sumw2(1);
  hboson_eta->SetDirectory(fout);
  TH1F *hboson_pt = new TH1F("boson_pt","boson_pt",500, 0.0,1000.0);
  hboson_pt->Sumw2(1);
  hboson_pt->SetDirectory(fout);
  TH1F *hnjet = new TH1F("njet","njet",10, -0.5,9.5);
  hnjet->Sumw2(1);
  hnjet->SetDirectory(fout);

  TH1F *hdr_ph_el = new TH1F("dr_ph_el","dr_ph_el",90, 0.0,9.0);
  hdr_ph_el->Sumw2(1);
  hdr_ph_el->SetDirectory(fout);
  TH1F *hdr_ph_j = new TH1F("dr_ph_j","dr_ph_j",90, 0.0,9.0);
  hdr_ph_j->Sumw2(1);
  hdr_ph_j->SetDirectory(fout);  
  TH1F *hdr_ph_boson = new TH1F("dr_ph_boson","dr_ph_boson",90, 0.0,9.0);
  hdr_ph_boson->Sumw2(1);
  hdr_ph_boson->SetDirectory(fout);  
  
  //TFile *fin = TFile::Open("365510b_VBFTruth.root");
  //TFile *fin = TFile::Open("enhanced_ptgam.root");
  TFile *fin = TFile::Open("mc.365520_ptgam15.root");
  //TFile *fin = TFile::Open("mc.366000_ptgam15.root");  
  //TFile *fin = TFile::Open("365500_VBFTruth.root");  
  TTree *truthTree = static_cast<TTree*>(fin->Get("MiniNtuple"));
  truthTree->SetBranchStatus("*",1);
   int                 m_njets;                                                                                                                                                                 
   std::vector<float> *m_jet_E;
   std::vector<float> *m_jet_pt;
   std::vector<float> *m_jet_eta;
   std::vector<float> *m_jet_phi;
   std::vector<float> *m_jet_m;
   std::vector<int> *  m_jet_label; 
      int                 m_nels;
   std::vector<float> *m_el_m;
   std::vector<float> *m_el_pt;                                                                                                                                                                 
   std::vector<float> *m_el_eta;                                                                                                                                                                
   std::vector<float> *m_el_phi;                                                                                                                                                                
   std::vector<uint> * m_el_type;                                                                                                                                                               
   std::vector<uint> * m_el_origin;                                                                                                                                                             
   std::vector<float> *m_el_ptcone30;                                                                                                                                                           
   std::vector<float> *m_el_etcone20;                                                                                                                                                           
   std::vector<int> *  m_el_pdgid;                                                                                                                                                              

   int                 m_nphs;                                                                                                                                                                  
   std::vector<float> *m_ph_m;                                                                                                                                                                  
   std::vector<float> *m_ph_pt;                                                                                                                                                                 
   std::vector<float> *m_ph_eta;                                                                                                                                                                
   std::vector<float> *m_ph_phi;                                                                                                                                                                
   std::vector<uint> * m_ph_type;                                                                                                                                                               
   std::vector<uint> * m_ph_origin;                                                                                                                                                             
   std::vector<float> *m_ph_ptcone30;                                                                                                                                                           
   std::vector<float> *m_ph_etcone20;                                                                                                                                                           
   std::vector<int> *  m_ph_pdgid;    

   int                 m_nnus;                                                                                                                                                                  
   std::vector<float> *m_nu_e;                                                                                                                                                                  
   std::vector<float> *m_nu_m;                                                                                                                                                                  
   std::vector<float> *m_nu_pt;                                                                                                                                                                 
   std::vector<float> *m_nu_eta;                                                                                                                                                                
   std::vector<float> *m_nu_phi;                                                                                                                                                                
   std::vector<uint> * m_nu_type;                                                                                                                                                               
   std::vector<uint> * m_nu_origin;                                                                                                                                                             
   std::vector<float> *m_nu_ptcone30;                                                                                                                                                           
   std::vector<float> *m_nu_etcone20;                                                                                                                                                           
   std::vector<int> *  m_nu_pdgid;        

   int                 m_nbosons;                                                                                                                                                               
   std::vector<float> *m_boson_e;                                                                                                                                                               
   std::vector<float> *m_boson_m;                                                                                                                                                               
   std::vector<float> *m_boson_pt;                                                                                                                                                              
   std::vector<float> *m_boson_eta;                                                                                                                                                             
   std::vector<float> *m_boson_phi;                                                                                                                                                             
   std::vector<int> *  m_boson_pdgid; 

   std::vector<float> *m_EventWeightSys;                                                                                                                                                        


  m_EventWeightSys = new std::vector<float>();
     m_jet_E     = new std::vector<float>();
   m_jet_pt    = new std::vector<float>();
   m_jet_eta   = new std::vector<float>();
   m_jet_phi   = new std::vector<float>();
   m_jet_m     = new std::vector<float>();
   m_jet_label = new std::vector<int>();
  m_el_m        = new std::vector<float>();
  m_el_pt       = new std::vector<float>();
  m_el_eta      = new std::vector<float>();
  m_el_phi      = new std::vector<float>();
  m_el_type     = new std::vector<uint>();
  m_el_origin   = new std::vector<uint>();
  m_el_pdgid   = new std::vector<int>();

  m_ph_m        = new std::vector<float>();
  m_ph_pt       = new std::vector<float>();
  m_ph_eta      = new std::vector<float>();
  m_ph_phi      = new std::vector<float>();
  m_ph_type     = new std::vector<uint>();
  m_ph_origin   = new std::vector<uint>();  
   m_boson_e     = new std::vector<float>();
   m_boson_m     = new std::vector<float>();
   m_boson_pt    = new std::vector<float>();
   m_boson_eta   = new std::vector<float>();
   m_boson_phi   = new std::vector<float>();
   m_boson_pdgid = new std::vector<int>();  
   m_nu_e      = new std::vector<float>();
   m_nu_m      = new std::vector<float>();
   m_nu_pt     = new std::vector<float>();
   m_nu_eta    = new std::vector<float>();
   m_nu_phi    = new std::vector<float>();
   m_nu_type   = new std::vector<uint>();
   m_nu_origin = new std::vector<uint>();
   m_nu_pdgid  = new std::vector<int>();
   m_boson_e     = new std::vector<float>();
   m_boson_m     = new std::vector<float>();
   m_boson_pt    = new std::vector<float>();
   m_boson_eta   = new std::vector<float>();
   m_boson_phi   = new std::vector<float>();
   m_boson_pdgid = new std::vector<int>();
   truthTree->SetBranchAddress("EventWeightSys", &m_EventWeightSys);
   //
   //// Jets                                                                                                                                                                                         
   truthTree->SetBranchAddress("njets", &m_njets);
   truthTree->SetBranchAddress("jet_E", &m_jet_E);
   truthTree->SetBranchAddress("jet_pt", &m_jet_pt);
   truthTree->SetBranchAddress("jet_eta", &m_jet_eta);
   truthTree->SetBranchAddress("jet_phi", &m_jet_phi);
   truthTree->SetBranchAddress("jet_m", &m_jet_m);
   truthTree->SetBranchAddress("jet_label", &m_jet_label);
   //
   //// Electrons                                                                                                                                                                                    
   truthTree->SetBranchAddress("nels", &m_nels);
   truthTree->SetBranchAddress("el_m", &m_el_m);
   truthTree->SetBranchAddress("el_pt", &m_el_pt);
   truthTree->SetBranchAddress("el_eta", &m_el_eta);
   truthTree->SetBranchAddress("el_phi", &m_el_phi);
   truthTree->SetBranchAddress("el_type", &m_el_type);
   //truthTree->SetBranchAddress("el_origin", &m_el_origin);
   truthTree->SetBranchAddress("el_pdgid", &m_el_pdgid);
   //
   //// Photons                                                                                                                                                                                      
   truthTree->SetBranchAddress("nphs",        &m_nphs);
   truthTree->SetBranchAddress("ph_m",        &m_ph_m);
   truthTree->SetBranchAddress("ph_pt",       &m_ph_pt);
   truthTree->SetBranchAddress("ph_eta",      &m_ph_eta);
   truthTree->SetBranchAddress("ph_phi",      &m_ph_phi);
   //truthTree->SetBranchAddress("ph_type",     &m_ph_type);
   //truthTree->SetBranchAddress("ph_origin",   &m_ph_origin);
   //truthTree->SetBranchAddress("ph_pdgid",    &m_ph_pdgid);
   //// Bosons                                                                                                                                                                                       
   truthTree->SetBranchAddress("nbosons", &m_nbosons);
   truthTree->SetBranchAddress("boson_m", &m_boson_m);
   truthTree->SetBranchAddress("boson_pt", &m_boson_pt);
   truthTree->SetBranchAddress("boson_eta", &m_boson_eta);
   truthTree->SetBranchAddress("boson_phi", &m_boson_phi);
   truthTree->SetBranchAddress("boson_pdgid", &m_boson_pdgid);

   //m_jet_E->clear();
   //m_jet_pt->clear();
   //m_jet_eta->clear();
   //m_jet_phi->clear();
   //m_jet_m->clear();
   //m_jet_label->clear();
   //
   //m_el_m->clear();
   //m_el_pt->clear();
   //m_el_eta->clear();
   //m_el_phi->clear();
   //m_el_type->clear();
   //m_el_origin->clear();
   ////m_el_pdgid->clear();
   //m_ph_m->clear();
   //m_ph_pt->clear();
   //m_ph_eta->clear();
   //m_ph_phi->clear();
   //m_ph_type->clear();
   //m_ph_origin->clear();
   //m_ph_pdgid->clear();
   //m_boson_e->clear();
   //m_boson_m->clear();
   //m_boson_pt->clear();
   //m_boson_eta->clear();
   //m_boson_phi->clear();
   //m_boson_pdgid->clear();
   //
   //m_nu_e->clear();
   //m_nu_m->clear();
   //m_nu_pt->clear();
   //m_nu_eta->clear();
   //m_nu_phi->clear();
   //m_nu_type->clear();
   //m_nu_origin->clear();
   //m_nu_pdgid->clear();
   //m_EventWeightSys->clear();

   for(long unsigned nevt=0; nevt<truthTree->GetEntries(); ++nevt){
     truthTree->GetEntry(nevt);
     //std::cout << "Weight: " << m_EventWeightSys->at(0) << std::endl;
     float weight =  m_EventWeightSys->at(0);

     if(m_ph_pt->size()>0){     hph_pt_lead->Fill(m_ph_pt->at(0)/1.0e3,weight); hph_pt_vs_w->Fill(m_ph_pt->at(0)/1.0e3,weight); }
     if(m_ph_eta->size()>0)    hph_eta_lead->Fill(m_ph_eta->at(0),weight);
     if(m_boson_pt->size()>0)  hboson_pt->Fill(m_boson_pt->at(0)/1.0e3,weight);
     if(m_boson_eta->size()>0) hboson_eta->Fill(m_boson_eta->at(0),weight);

     TVector3 phvec,jvec, evec,bvec;

     for(unsigned ne=0; ne<m_el_pt->size(); ++ne){
       evec.SetPtEtaPhi(m_el_pt->at(ne)/1.0e3, m_el_eta->at(ne), m_el_phi->at(ne));
       if(evec.Pt()>10.0 && m_el_pdgid->at(ne)<0){
	 helneg_pt->Fill(m_el_pt->at(ne)/1.0e3,weight);
	 helneg_pt_vs_w->Fill(m_el_pt->at(ne)/1.0e3,weight);
       }
       if(evec.Pt()>10.0 && m_el_pdgid->at(ne)>0){
	 helpos_pt->Fill(m_el_pt->at(ne)/1.0e3,weight);
	 helpos_pt_vs_w->Fill(m_el_pt->at(ne)/1.0e3,weight);
       }
     }
     
     for(unsigned nph=0; nph<m_ph_pt->size(); ++nph){
       phvec.SetPtEtaPhi(m_ph_pt->at(nph)/1.0e3, m_ph_eta->at(nph), m_ph_phi->at(nph));
       hph_pt ->Fill(m_ph_pt->at(nph)/1.0e3,weight);
       hph_eta->Fill(m_ph_eta->at(nph),     weight);

       for(unsigned nj=0; nj<m_jet_pt->size(); ++nj){
	 jvec.SetPtEtaPhi(m_jet_pt->at(nj)/1.0e3, m_jet_eta->at(nj), m_jet_phi->at(nj));
	 if(phvec.Pt()>15.0 && jvec.Pt()>20.0) hdr_ph_j->Fill(phvec.DeltaR(jvec),weight);
       }
       for(unsigned ne=0; ne<m_el_pt->size(); ++ne){
	 evec.SetPtEtaPhi(m_el_pt->at(ne)/1.0e3, m_el_eta->at(ne), m_el_phi->at(ne));
	 if(phvec.Pt()>15.0 && evec.Pt()>15.0) hdr_ph_el->Fill(phvec.DeltaR(evec),weight);
       }
       if(phvec.Pt()>15.0 && m_boson_pt->size()>0){
	 bvec.SetPtEtaPhi(m_boson_pt->at(0)/1.0e3, m_boson_eta->at(0), m_boson_phi->at(0));
	 hdr_ph_boson->Fill( bvec.DeltaR(phvec),weight);
	   }
     }
     unsigned tnj=0;
     for(unsigned nj=0; nj<m_jet_pt->size(); ++nj){
       jvec.SetPtEtaPhi(m_jet_pt->at(nj)/1.0e3, m_jet_eta->at(nj), m_jet_phi->at(nj));
       bool phor= false;
       for(unsigned nph=0; nph<m_ph_pt->size(); ++nph){
	 phvec.SetPtEtaPhi(m_ph_pt->at(nph)/1.0e3, m_ph_eta->at(nph), m_ph_phi->at(nph));
	 if(phvec.DeltaR(jvec)<0.2) phor=true;
       }
       if(phor) continue;
       if(m_jet_pt->at(nj)>20.0e3) ++tnj;
     }
     hnjet->Fill(tnj,weight);
   }

   fout->Write();
   fout->Close();
  return 1;
}
