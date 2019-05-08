
// ROOT
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"

// Local
#include "HInvPlot/PlotEvent.h"
#include "HInvPlot/UtilCore.h"

using namespace std;

//-----------------------------------------------------------------------------
Msl::PlotEvent::PlotEvent():      fPassAlg(0), 
				  hTruthMuPt(0), hTruthMuEta(0),
				  hBaseMuPt(0), hBaseMuEta(0),
				  hTruthElPt(0), hTruthElEta(0),
				  hBaseElPt(0), hBaseElEta(0),
				  hTruthTauPt(0), hTruthTauEta(0),
				  hminDRLep(0),
				  hmj34(0),
				  hmax_j_eta(0),
				  hdRj1(0),
				  hdRj2(0),
				  hminDR(0),
				  hmj1(0),
				  hmj2(0),
				  hminDRmj2(0),
				  hmin_mj3(0),
				  hmin_mj3_over_mjj(0),
				  hcentrality(0),
				  hZMCIDQCD(0), hWMCIDQCD(0),
				  hZMadMCIDQCD(0), hZMad2MCIDQCD(0),
				  hWMadMCIDQCD(0),
				  hZPowMCIDQCD(0),
				  hqgTagPerf(0),
				  hqgTagNTrack(0),
				  hqgTagTrackWidth(0),
				  hqgTagSum(0),
				  hQGTaggerSim(0),
				  hQGTaggerSimLog(0),
				  hQGTaggerSimLin(0),
				  hnTrackCut0(0),
				  hnTrackCut1(0),
				  hTrackWidthCut0(0),
				  hTrackWidthCut1(0),
				  hnTrackCutSum(0),
				  hTrackWidthCutSum(0),
				  hnTrackSum(0),
				  hTrackWidthSum(0),
				  hjetNTracks025(0),
				  hjetNTracks125(0),
				  hjetTrackWidth025(0),
				  hjetTrackWidth125(0),
				  hjetNTracks021(0),
				  hjetNTracks121(0),
				  hjetTrackWidth021(0),
				  hjetTrackWidth121(0),
				  hjetNTracks02125(0),
				  hjetNTracks12125(0),
				  hjetTrackWidth02125(0),
				  hjetTrackWidth12125(0),
				  hjetNTrackPT(0),
				  hjetNTrackPTq(0),
				  hjetNTrackPTg(0),
				  hjetNTrackPTpu(0)

{
}

//-----------------------------------------------------------------------------
Msl::PlotEvent::~PlotEvent()
{
}

//-----------------------------------------------------------------------------
void Msl::PlotEvent::DoConf(const Registry &reg)
{
  //
  // Read self-configuration
  //
  IExecAlg::DoConf(reg);

  reg.Get("PlotEvent::NBin",      fNBin      = 50);
  reg.Get("PlotEvent::NBinLim",   fNBinLim   =  0);
  reg.Get("PlotEvent::DetailLvl", fDetailLvl =  0);

  reg.Get("PlotEvent::SelKey" , fSelKey);
  reg.Get("PlotEvent::Region" , fRegion);
  reg.Get("PlotEvent::VarPref", fVarPref);

  fVarVec =  Mva::ReadVars(reg, "PlotEvent::VarVec", GetAlgName());
  reg.Get("PlotEvent::NBinVec", fNBinVec);  
  reg.Get("PlotEvent::LoVec",   fLoVec);  
  reg.Get("PlotEvent::HiVec",   fHiVec);  

  //
  // Read configuration for selecting MC samples
  //
  fSample.FillSample(reg, "PlotEvent::Samples");

  //
  // Convert string keys to Mva::Key enum values
  //
  fVars = Mva::ReadVars(reg, "PlotEvent::Vars", fName);

  //
  // Created histograms
  //
  hTruthMuPt   = GetTH1("truthMuPt",    50,  0.0,   100.0);
  hTruthMuEta  = GetTH1("truthMuEta",   45,  -4.5,   4.5);  
  hBaseMuPt    = GetTH1("baseMuPt",    50,  0.0,   100.0);
  hBaseMuEta   = GetTH1("baseMuEta",   45,  -4.5,   4.5);
  hTruthElPt   = GetTH1("truthElPt",    50,  0.0,   100.0);
  hTruthElEta  = GetTH1("truthElEta",   45,  -4.5,   4.5);  
  hBaseElPt    = GetTH1("baseElPt",    50,  0.0,   100.0);
  hBaseElEta   = GetTH1("baseElEta",   45,  -4.5,   4.5);
  hTruthTauPt  = GetTH1("truthTauPt",    50,  0.0,   100.0);
  hTruthTauDR  = GetTH1("truthTauDR",    100,  0.0,   10.0);
  hTruthTauEta = GetTH1("truthTauEta",   45,  -4.5,   4.5);
  hminDRLep = GetTH1("minDRLep",   60,  0.0,   6.0);
  hptvarcone20  = GetTH1("ptvarcone20",   12,  -0.2,   1.0);  
  hptvarcone30  = GetTH1("ptvarcone30",   12,  -0.2,   1.0);  
  htopoetcone20 = GetTH1("topoetcone20",  12,  -0.2,   1.0);  
  
  // extra vars
  hmj34             = GetTH1("mj34",             50,  0.0,   1000.0);		  
  hmax_j_eta        = GetTH1("max_j_eta",        45,  0.0,   4.5);    	  
  hdRj1             = GetTH1("dRj1",             20,  0.0,   10.0);		  
  hdRj2             = GetTH1("dRj2",             20,  0.0,   10.0);		  
  hminDR            = GetTH1("minDR",            20,  0.0,  10.0);		  
  hmj1              = GetTH1("mj1",              50,  0.0,   2000.0);		  
  hmj2              = GetTH1("mj2",              50,  0.0,   2000.0);		  
  hminDRmj2         = GetTH1("minDRmj2",         50,  0.0,   2000.0);    	  
  hmin_mj3          = GetTH1("min_mj3",          50,  0.0,   2000.0);	  
  hmin_mj3_over_mjj = GetTH1("min_mj3_over_mjj", 25,  0.0,   1.0);
  hcentrality       = GetTH1("centrality",       25,  0.0,   1.0);
  hj3Pt             = GetTH1("j3Pt",             20,  0.0,   200.0);
  hj3Eta            = GetTH1("j3Eta",            22,  -4.5,  4.5);
  hj3Jvt            = GetTH1("j3Jvt",            12,  -0.2,  1.0);
  hj3FJvt           = GetTH1("j3FJvt",           22,  -0.2,  2.0);

  hmuDR           = GetTH1("muDR",           25,  0.0,  5.0);
  hmuEta          = GetTH1("muEta",          30,  0.0,  3.0);    
  
  hZMCIDQCD    = GetTH1("ZMCIDQCD",     100,  364099.5,364199.5);
  hWMCIDQCD    = GetTH1("WMCIDQCD",     100,  364155.5,364255.5);
  hZMadMCIDQCD = GetTH1("ZMadMCIDQCD",  10,  361509.5,361519.5);
  hZMad2MCIDQCD= GetTH1("ZMad2MCIDQCD", 100, 363122.5,363222.5);  
  hWMadMCIDQCD = GetTH1("WMadMCIDQCD",  74,  363599.5,363673.5);
  hZPowMCIDQCD = GetTH1("ZPowMCIDQCD",  19,  301019.5,301038.5);  

  hqgTagPerf = GetTH1("qgTagPerf",  9,  0.0, 9.0);  
  hqgTagNTrack = GetTH1("qgTagNTrack",  15,  0.0, 15.0);  
  hqgTagTrackWidth = GetTH1("qgTagTrackWidth",  13,  0.0, 13.0);  
  hqgTagSum = GetTH1("qgTagSum",  13,  0.0, 13.0);  
  hQGTaggerSim = GetTH1("qgTaggerSim",  7,  0.0, 7.0);  
  hQGTaggerSimLog = GetTH1("qgTaggerSimLog",  15,  0.0, 15.0);  
  hQGTaggerSimLin = GetTH1("qgTaggerSimLin",  15,  0.0, 15.0);  
  hnTrackCut0 = GetTH1("nTrackCut0",  40,  0.0, 40.0);  
  hnTrackCut1 = GetTH1("nTrackCut1",  40,  0.0, 40.0);  
  hTrackWidthCut0 = GetTH1("TrackWidthCut0",  80,  0.0, 0.4);  
  hTrackWidthCut1 = GetTH1("TrackWidthCut1",  80,  0.0, 0.4);  
  hnTrackSum = GetTH1("nTrackSum",  80,  0.0, 80.0);  
  hTrackWidthSum = GetTH1("TrackWidthSum",  160,  0.0, 0.8);  
  hnTrackCutSum = GetTH1("nTrackCutSum",  80,  0.0, 80.0);  
  hTrackWidthCutSum = GetTH1("TrackWidthCutSum",  160,  0.0, 0.8);  
  hjetNTracks025 = GetTH1("jetNTracks025",  40,  0.0, 40.0);  
  hjetNTracks125 = GetTH1("jetNTracks125",  40,  0.0, 40.0);  
  hjetTrackWidth025 = GetTH1("jetTrackWidth025",  50,  0.0, 1.0);  
  hjetTrackWidth125 = GetTH1("jetTrackWidth125",  50,  0.0, 1.0);  
  hjetNTracks021 = GetTH1("jetNTracks021",  40,  0.0, 40.0);  
  hjetNTracks121 = GetTH1("jetNTracks121",  40,  0.0, 40.0);  
  hjetTrackWidth021 = GetTH1("jetTrackWidth021",  50,  0.0, 1.0);  
  hjetTrackWidth121 = GetTH1("jetTrackWidth121",  50,  0.0, 1.0);  
  hjetNTracks02125 = GetTH1("jetNTracks02125",  40,  0.0, 40.0);  
  hjetNTracks12125 = GetTH1("jetNTracks12125",  40,  0.0, 40.0);  
  hjetTrackWidth02125 = GetTH1("jetTrackWidth02125",  50,  0.0, 1.0);  
  hjetTrackWidth12125 = GetTH1("jetTrackWidth12125",  50,  0.0, 1.0);  

  hjetNTrackPT = GetTH2("jetNTrackPT", 100, 0.0, 500.0, 40, 0.0, 40.0);  
  hjetNTrackPTq = GetTH2("jetNTrackPTq", 100, 0.0, 500.0, 40, 0.0, 40.0);  
  hjetNTrackPTg = GetTH2("jetNTrackPTg", 100, 0.0, 500.0, 40, 0.0, 40.0);  
  hjetNTrackPTpu = GetTH2("jetNTrackPTpu", 100, 0.0, 500.0, 40, 0.0, 40.0);  

  // creating histograms
  for(unsigned a=0; a<fVarVec.size(); ++a){
    fHistVec[fVarVec[a]] =  GetTH1(Mva::Convert2Str(fVarVec[a]),unsigned(fNBinVec[a]), float(fLoVec[a]), float(fHiVec[a]));
  }
  
    if(fDebug) {
      fSample.Print(std::cout, "   ");
    }
}

//-----------------------------------------------------------------------------
bool Msl::PlotEvent::DoExec(Event &event)
{
  //
  // Select sample
  //
  if(fSample.GetSize() > 0 && !fSample.MatchSample(event.sample)) {
    return true;
  }

  double weight = event.GetWeight();
  if(fDebug) std::cout << "PlotEvent: " << weight << " " << GetAlgName() << std::endl;
  if(fPassAlg) {
    if(!(fPassAlg->GetPassStatus())) {
      return true;
    }
    weight = fPassAlg->GetPassWeight();
  }

  //
  // Fill and save new VarStore
  //
  //fEvents.push_back(VarStore(event, fVars));
  //fEvents.back().SetWeight(weight);
  
  //
  // Fill histograms
  //
  //std::cout << "Run:" << " " << event.RunNumber << " event: " << event.EventNumber << std::endl;
  //FillHist(hZMCIDQCD,   Mva::jj_deta, event, weight);
  hZMCIDQCD->Fill(event.RunNumber, weight);
  hWMCIDQCD->Fill(event.RunNumber, weight);
  hZMadMCIDQCD->Fill(event.RunNumber, weight);
  hZMad2MCIDQCD->Fill(event.RunNumber, weight);  
  hWMadMCIDQCD->Fill(event.RunNumber, weight);  
  hZPowMCIDQCD->Fill(event.RunNumber, weight);
  
  if(event.truth_mu.size()>0){
    hTruthMuPt ->Fill(event.truth_mu.at(0).pt, weight);
    hTruthMuEta->Fill(event.truth_mu.at(0).eta, weight);
  }
  if(event.truth_el.size()>0){
    hTruthElPt ->Fill(event.truth_el.at(0).pt, weight);
    hTruthElEta->Fill(event.truth_el.at(0).eta, weight);
  }

  if(event.muons.size()>1){
    hmuDR->Fill(event.muons.at(0).GetVec().DeltaR(event.muons.at(1).GetVec()), weight);
    hmuEta->Fill(event.muons.at(0).eta, weight);
    hmuEta->Fill(event.muons.at(1).eta, weight);        
  }
  if(event.electrons.size()>1){
    hmuDR->Fill(event.electrons.at(0).GetVec().DeltaR(event.electrons.at(1).GetVec()), weight);
    hmuEta->Fill(event.electrons.at(0).eta, weight);
    hmuEta->Fill(event.electrons.at(1).eta, weight);        
  }
  
  if(event.basemu.size()>0){
    hBaseMuPt ->Fill(event.basemu.at(0).pt, weight);
    hBaseMuEta->Fill(event.basemu.at(0).eta, weight);
  }
  if(event.baseel.size()>0){
    hBaseElPt ->Fill(event.baseel.at(0).pt, weight);
    hBaseElEta->Fill(event.baseel.at(0).eta, weight);
  }
  if(event.truth_taus.size()>0){
    hTruthTauPt ->Fill(event.truth_taus.at(0).pt, weight);
    for(unsigned iJet=0; iJet<event.jets.size(); ++iJet)
      hTruthTauDR ->Fill(event.truth_taus.at(0).GetVec().DeltaR(event.jets.at(iJet).GetVec()), weight);
    hTruthTauEta->Fill(event.truth_taus.at(0).eta, weight);
  }  

  //qg with Eta req
  if(-2.5<event.jets.at(0).eta and event.jets.at(0).eta<2.5) hjetNTracks025->Fill(event.GetVar(Mva::jetNTracks0),weight);
  if(-2.5<event.jets.at(1).eta and event.jets.at(1).eta<2.5) hjetNTracks125->Fill(event.GetVar(Mva::jetNTracks1),weight);
  if(-2.5<event.jets.at(0).eta and event.jets.at(0).eta<2.5) hjetTrackWidth025->Fill(event.GetVar(Mva::jetTrackWidth0),weight);
  if(-2.5<event.jets.at(1).eta and event.jets.at(1).eta<2.5) hjetTrackWidth125->Fill(event.GetVar(Mva::jetTrackWidth1),weight);
  if(-2.1<event.jets.at(0).eta and event.jets.at(0).eta<2.1) hjetNTracks021->Fill(event.GetVar(Mva::jetNTracks0),weight);
  if(-2.1<event.jets.at(1).eta and event.jets.at(1).eta<2.1) hjetNTracks121->Fill(event.GetVar(Mva::jetNTracks1),weight);
  if(-2.1<event.jets.at(0).eta and event.jets.at(0).eta<2.1) hjetTrackWidth021->Fill(event.GetVar(Mva::jetTrackWidth0),weight);
  if(-2.1<event.jets.at(1).eta and event.jets.at(1).eta<2.1) hjetTrackWidth121->Fill(event.GetVar(Mva::jetTrackWidth1),weight);
  if((-2.5<event.jets.at(0).eta and event.jets.at(0).eta<-2.1) || (2.1<event.jets.at(0).eta and event.jets.at(0).eta<2.5)) hjetNTracks02125->Fill(event.GetVar(Mva::jetNTracks0),weight);
  if((-2.5<event.jets.at(1).eta and event.jets.at(1).eta<-2.1) || (2.1<event.jets.at(0).eta and event.jets.at(0).eta<2.5)) hjetNTracks12125->Fill(event.GetVar(Mva::jetNTracks1),weight);
  if((-2.5<event.jets.at(0).eta and event.jets.at(0).eta<-2.1) || (2.1<event.jets.at(0).eta and event.jets.at(0).eta<2.5)) hjetTrackWidth02125->Fill(event.GetVar(Mva::jetTrackWidth0),weight);
  if((-2.5<event.jets.at(1).eta and event.jets.at(1).eta<-2.1) || (2.1<event.jets.at(0).eta and event.jets.at(0).eta<2.5)) hjetTrackWidth12125->Fill(event.GetVar(Mva::jetTrackWidth1),weight);

  //jetNTrackPT - 2D histogram for central jets NTrack vs pT
  float forw=2.5;
  bool isCentral0=true;
  bool isCentral1=true;
  if(event.jets.at(0).eta<-forw or forw<event.jets.at(0).eta) isCentral0=false;
  if(event.jets.at(1).eta<-forw or forw<event.jets.at(1).eta) isCentral1=false;


  for(int jet=0; jet<2;++jet){
    if(-forw<event.jets.at(jet).eta and event.jets.at(jet).eta<forw and jet==0){
	hjetNTrackPT->Fill(event.jets.at(jet).pt,event.GetVar(Mva::jetNTracks0),weight);
	if(event.GetVar(Mva::jetPartonTruthLabelID0)==21) hjetNTrackPTg->Fill(event.jets.at(jet).pt,event.GetVar(Mva::jetNTracks0),weight);	
	else if(event.GetVar(Mva::jetPartonTruthLabelID0)==0) hjetNTrackPTpu->Fill(event.jets.at(jet).pt,event.GetVar(Mva::jetNTracks0),weight);	
	else hjetNTrackPTq->Fill(event.jets.at(jet).pt,event.GetVar(Mva::jetNTracks0),weight);	
    }
    else if(-forw<event.jets.at(jet).eta and event.jets.at(jet).eta<forw and jet==1){
	hjetNTrackPT->Fill(event.jets.at(jet).pt,event.GetVar(Mva::jetNTracks1),weight);
	if(event.GetVar(Mva::jetPartonTruthLabelID1)==21) hjetNTrackPTg->Fill(event.jets.at(jet).pt,event.GetVar(Mva::jetNTracks1),weight);	
	else if(event.GetVar(Mva::jetPartonTruthLabelID1)==0) hjetNTrackPTpu->Fill(event.jets.at(jet).pt,event.GetVar(Mva::jetNTracks1),weight);	
	else hjetNTrackPTq->Fill(event.jets.at(jet).pt,event.GetVar(Mva::jetNTracks1),weight);	
    }
  }

  //for qgTagPerf
  /*
  if(event.GetVar(Mva::passPerfCTagging)==2) hqgTagPerf->Fill(6.0, weight);
  else hqgTagPerf->Fill(7.0,weight);
  if(event.GetVar(Mva::passPerfFTagging)==2) hqgTagPerf->Fill(4.0, weight);
  else hqgTagPerf->Fill(5.0,weight);
  if(event.GetVar(Mva::jj_nmbGluons)==0) hqgTagPerf->Fill(2.0, weight);
  else hqgTagPerf->Fill(3.0,weight);
  */

  bool isQuark0=true;
  bool isQuark1=true;
  if(event.GetVar(Mva::jetPartonTruthLabelID0)==21 or event.GetVar(Mva::jetPartonTruthLabelID0)==0) isQuark0=false;
  if(event.GetVar(Mva::jetPartonTruthLabelID1)==21 or event.GetVar(Mva::jetPartonTruthLabelID1)==0) isQuark1=false;

  hqgTagPerf->Fill(1.0,weight);

  if(isQuark0 and isQuark1) hqgTagPerf->Fill(2.0,weight);
  else hqgTagPerf->Fill(3.0,weight);
  
  if(((not isCentral0 and isQuark0) or isCentral0)and((not isCentral1 and isQuark1) or isCentral1)) hqgTagPerf->Fill(4.0,weight);
  else hqgTagPerf->Fill(5.0,weight);

  if(((isCentral0 and isQuark0) or not isCentral0)and((isCentral1 and isQuark1) or not isCentral1)) hqgTagPerf->Fill(6.0,weight);
  else hqgTagPerf->Fill(7.0,weight);



  hqgTagPerf->GetXaxis()->SetBinLabel(1," ");
  hqgTagPerf->GetXaxis()->SetBinLabel(2,"No Tagging");
  hqgTagPerf->GetXaxis()->SetBinLabel(3,"Full Tagging");
  hqgTagPerf->GetXaxis()->SetBinLabel(4,"Fail Full Tagging");
  hqgTagPerf->GetXaxis()->SetBinLabel(5,"Forward Tagging");
  hqgTagPerf->GetXaxis()->SetBinLabel(6,"Fail Forward Tagging");
  hqgTagPerf->GetXaxis()->SetBinLabel(7,"Central Tagging");
  hqgTagPerf->GetXaxis()->SetBinLabel(8,"Fail Central Tagging");



  //qgTagNTrack
  hqgTagNTrack->Fill(1.0,weight);
  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<3) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<3) or not isCentral1) hqgTagNTrack->Fill(2.0,weight);
    else hqgTagNTrack->Fill(3.0,weight);
  }
  else hqgTagNTrack->Fill(3.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<5) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<5) or not isCentral1) hqgTagNTrack->Fill(4.0,weight);
    else hqgTagNTrack->Fill(5.0,weight);
  }
  else hqgTagNTrack->Fill(5.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<5) or not isCentral0) hqgTagNTrack->Fill(6.0,weight);
  else hqgTagNTrack->Fill(7.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<10) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<10) or not isCentral1) hqgTagNTrack->Fill(8.0,weight);
    else hqgTagNTrack->Fill(9.0,weight);
  }
  else hqgTagNTrack->Fill(9.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<12) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<12) or not isCentral1) hqgTagNTrack->Fill(10.0,weight);
    else hqgTagNTrack->Fill(11.0,weight);
  }
  else hqgTagNTrack->Fill(11.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<12) or not isCentral0) hqgTagNTrack->Fill(12.0,weight);
  else hqgTagNTrack->Fill(13.0,weight);

  hqgTagNTrack->GetXaxis()->SetBinLabel(1," ");
  hqgTagNTrack->GetXaxis()->SetBinLabel(2,"No Tagging");
  hqgTagNTrack->GetXaxis()->SetBinLabel(3,"NTracks<3");
  hqgTagNTrack->GetXaxis()->SetBinLabel(4,"Fail NTracks<3");
  hqgTagNTrack->GetXaxis()->SetBinLabel(5,"NTracks<5");
  hqgTagNTrack->GetXaxis()->SetBinLabel(6,"Fail NTracks<5");
  hqgTagNTrack->GetXaxis()->SetBinLabel(7,"NTracks0<5");
  hqgTagNTrack->GetXaxis()->SetBinLabel(8,"Fail NTracks0<5");
  hqgTagNTrack->GetXaxis()->SetBinLabel(9,"NTracks<10");
  hqgTagNTrack->GetXaxis()->SetBinLabel(10,"Fail NTracks<10");
  hqgTagNTrack->GetXaxis()->SetBinLabel(11,"NTracks<12");
  hqgTagNTrack->GetXaxis()->SetBinLabel(12,"Fail NTracks<12");
  hqgTagNTrack->GetXaxis()->SetBinLabel(13,"NTracks0<12");
  hqgTagNTrack->GetXaxis()->SetBinLabel(14,"Fail NTracks0<12");


  //qgTagTrackWidth
  hqgTagTrackWidth->Fill(1.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetTrackWidth0)<0.05) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetTrackWidth1)<0.05) or not isCentral1) hqgTagTrackWidth->Fill(2.0,weight);
    else hqgTagTrackWidth->Fill(3.0,weight);
  }
  else hqgTagTrackWidth->Fill(3.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetTrackWidth0)<0.08) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetTrackWidth1)<0.08) or not isCentral1) hqgTagTrackWidth->Fill(4.0,weight);
    else hqgTagTrackWidth->Fill(5.0,weight);
  }
  else hqgTagTrackWidth->Fill(5.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetTrackWidth0)<0.08) or not isCentral0)hqgTagTrackWidth->Fill(6.0,weight);
  else hqgTagTrackWidth->Fill(7.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetTrackWidth0)<0.1) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetTrackWidth1)<0.1) or not isCentral1) hqgTagTrackWidth->Fill(8.0,weight);
    else hqgTagTrackWidth->Fill(9.0,weight);
  }
  else hqgTagTrackWidth->Fill(9.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetTrackWidth0)<0.18) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetTrackWidth1)<0.18) or not isCentral1) hqgTagTrackWidth->Fill(10.0,weight);
    else hqgTagTrackWidth->Fill(11.0,weight);
  }
  else hqgTagTrackWidth->Fill(11.0,weight);

  hqgTagTrackWidth->GetXaxis()->SetBinLabel(1," ");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(2,"No Tagging");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(3,"TrackWidth<0.05");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(4,"Fail TrackWidth<0.05");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(5,"TrackWidth<0.08");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(6,"Fail TrackWidth<0.08");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(7,"TrackWidth0<0.08");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(8,"Fail TrackWidth0<0.08");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(9,"TrackWidth<0.1");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(10,"Fail TrackWidth<0.1");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(11,"TrackWidth<0.18");
  hqgTagTrackWidth->GetXaxis()->SetBinLabel(12,"Fail TrackWidth<0.18");


  //qgTagSum
  hqgTagSum->Fill(1.0,weight);

  if (event.GetVar(Mva::jetNTracks0)+event.GetVar(Mva::jetNTracks1)<5) hqgTagSum->Fill(2.0,weight);
  else hqgTagSum->Fill(3.0,weight);  

  if (event.GetVar(Mva::jetNTracks0)+event.GetVar(Mva::jetNTracks1)<10) hqgTagSum->Fill(4.0,weight);
  else hqgTagSum->Fill(5.0,weight);  

  if (event.GetVar(Mva::jetNTracks0)+event.GetVar(Mva::jetNTracks1)<15) hqgTagSum->Fill(6.0,weight);
  else hqgTagSum->Fill(7.0,weight);  

  if (event.GetVar(Mva::jetTrackWidth0)+event.GetVar(Mva::jetTrackWidth1)<0.05) hqgTagSum->Fill(8.0,weight);
  else hqgTagSum->Fill(9.0,weight);  

  if (event.GetVar(Mva::jetTrackWidth0)+event.GetVar(Mva::jetTrackWidth1)<0.1) hqgTagSum->Fill(10.0,weight);
  else hqgTagSum->Fill(11.0,weight);  

  hqgTagSum->GetXaxis()->SetBinLabel(1," ");
  hqgTagSum->GetXaxis()->SetBinLabel(2,"No Tagging");
  hqgTagSum->GetXaxis()->SetBinLabel(3,"NTrackSum<5");
  hqgTagSum->GetXaxis()->SetBinLabel(4,"Fail NTrackSum<5");
  hqgTagSum->GetXaxis()->SetBinLabel(5,"NTrackSum<10");
  hqgTagSum->GetXaxis()->SetBinLabel(6,"Fail NTrackSum<10");
  hqgTagSum->GetXaxis()->SetBinLabel(7,"NTrackSum<15");
  hqgTagSum->GetXaxis()->SetBinLabel(8,"Fail NTrackSum<15");
  hqgTagSum->GetXaxis()->SetBinLabel(9,"TrackWidthSum<0.05");
  hqgTagSum->GetXaxis()->SetBinLabel(10,"Fail TrackWidthSum<0.05");
  hqgTagSum->GetXaxis()->SetBinLabel(11,"Fail TrackWidthSum<0.1");
  hqgTagSum->GetXaxis()->SetBinLabel(12,"Fail TrackWidthSum<0.1");

  //QGTaggerSim - values/method taken from defaults in Reconstruction/Jet/BoostedJetTaggers for JetQGTagger
  //use pT in MeV
  float slope=9.779;
  float intercept=-32.28;
  float lin0 = (slope*event.jets.at(0).pt*1000)+intercept;
  float lin1 = (slope*event.jets.at(1).pt*1000)+intercept;
  float log0 = (slope*TMath::Log10(event.jets.at(0).pt*1000))+intercept;
  float log1 = (slope*TMath::Log10(event.jets.at(1).pt*1000))+intercept;

  hQGTaggerSim->Fill(1.0,weight);
  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<lin0) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<lin1) or not isCentral1) hQGTaggerSim->Fill(2.0,weight);
    else hQGTaggerSim->Fill(3.0,weight);
  }
  else hQGTaggerSim->Fill(3.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<log0) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<log1) or not isCentral1) hQGTaggerSim->Fill(4.0,weight);
    else hQGTaggerSim->Fill(5.0,weight);
  }
  else hQGTaggerSim->Fill(5.0,weight);

  hQGTaggerSim->GetXaxis()->SetBinLabel(1," ");
  hQGTaggerSim->GetXaxis()->SetBinLabel(2,"No Tagging");
  hQGTaggerSim->GetXaxis()->SetBinLabel(3,"Default linear_pt");
  hQGTaggerSim->GetXaxis()->SetBinLabel(4,"Fail Default linear_pt");
  hQGTaggerSim->GetXaxis()->SetBinLabel(5,"Default log_pt");
  hQGTaggerSim->GetXaxis()->SetBinLabel(6,"Fail Default log_pt");

  float log10pt0 = TMath::Log10(event.jets.at(0).pt*1000);
  float log10pt1 = TMath::Log10(event.jets.at(1).pt*1000);

  hQGTaggerSimLog->Fill(1.0,weight);
  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(7*log10pt0-20)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(7*log10pt1-20)) or not isCentral1) hQGTaggerSimLog->Fill(2.0,weight);
    else hQGTaggerSimLog->Fill(3.0,weight);
  }
  else hQGTaggerSimLog->Fill(3.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(8*log10pt0-25)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(8*log10pt1-25)) or not isCentral1) hQGTaggerSimLog->Fill(4.0,weight);
    else hQGTaggerSimLog->Fill(5.0,weight);
  }
  else hQGTaggerSimLog->Fill(5.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(9*log10pt0-30)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(9*log10pt1-30)) or not isCentral1) hQGTaggerSimLog->Fill(6.0,weight);
    else hQGTaggerSimLog->Fill(7.0,weight);
  }
  else hQGTaggerSimLog->Fill(7.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(10*log10pt0-35)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(10*log10pt1-35)) or not isCentral1) hQGTaggerSimLog->Fill(8.0,weight);
    else hQGTaggerSimLog->Fill(9.0,weight);
  }
  else hQGTaggerSimLog->Fill(9.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(11*log10pt0-40)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(11*log10pt1-40)) or not isCentral1) hQGTaggerSimLog->Fill(10.0,weight);
    else hQGTaggerSimLog->Fill(11.0,weight);
  }
  else hQGTaggerSimLog->Fill(11.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(12*log10pt0-45)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(12*log10pt1-45)) or not isCentral1) hQGTaggerSimLog->Fill(12.0,weight);
    else hQGTaggerSimLog->Fill(13.0,weight);
  }
  else hQGTaggerSimLog->Fill(13.0,weight);

  hQGTaggerSimLog->GetXaxis()->SetBinLabel(1," ");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(2,"No Tagging");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(3,"7Log10(pT)-20");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(4,"Fail");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(5,"8Log10(pT)-25");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(6,"Fail");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(7,"9Log10(pT)-30");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(8,"Fail");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(9,"10Log10(pT)-35");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(10,"Fail");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(11,"11Log10(pT)-40");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(12,"Fail");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(13,"12Log10(pT)-45");
  hQGTaggerSimLog->GetXaxis()->SetBinLabel(14,"Fail");

  float pt0 = event.jets.at(0).pt*1000;
  float pt1 = event.jets.at(1).pt*1000;

  hQGTaggerSimLin->Fill(1.0,weight);
  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(0.00006*pt0+5)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(0.00006*pt1+5)) or not isCentral1) hQGTaggerSimLin->Fill(2.0,weight);
    else hQGTaggerSimLin->Fill(3.0,weight);
  }
  else hQGTaggerSimLin->Fill(3.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(0.00008*pt0+5)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(0.00008*pt1+5)) or not isCentral1) hQGTaggerSimLin->Fill(4.0,weight);
    else hQGTaggerSimLin->Fill(5.0,weight);
  }
  else hQGTaggerSimLin->Fill(5.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(0.00009*pt0+5)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(0.00009*pt1+5)) or not isCentral1) hQGTaggerSimLin->Fill(6.0,weight);
    else hQGTaggerSimLin->Fill(7.0,weight);
  }
  else hQGTaggerSimLin->Fill(7.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(0.0001*pt0+5)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(0.0001*pt1+5)) or not isCentral1) hQGTaggerSimLin->Fill(8.0,weight);
    else hQGTaggerSimLin->Fill(9.0,weight);
  }
  else hQGTaggerSimLin->Fill(9.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(0.00011*pt0+5)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(0.00011*pt1+5)) or not isCentral1) hQGTaggerSimLin->Fill(10.0,weight);
    else hQGTaggerSimLin->Fill(11.0,weight);
  }
  else hQGTaggerSimLin->Fill(11.0,weight);

  if((isCentral0 and event.GetVar(Mva::jetNTracks0)<(0.00012*pt0+5)) or not isCentral0){
    if((isCentral1 and event.GetVar(Mva::jetNTracks1)<(0.00012*pt1+5)) or not isCentral1) hQGTaggerSimLin->Fill(12.0,weight);
    else hQGTaggerSimLin->Fill(13.0,weight);
  }
  else hQGTaggerSimLin->Fill(13.0,weight);

  hQGTaggerSimLin->GetXaxis()->SetBinLabel(1," ");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(2,"No Tagging");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(3,"6e-5pT+5");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(4,"Fail");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(5,"8e-5pT+5");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(6,"Fail");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(7,"9e-5pT+5");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(8,"Fail");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(9,"10e-5pT+5");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(10,"Fail");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(11,"11e-5pT+5");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(12,"Fail");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(13,"12e-5pT+5");
  hQGTaggerSimLin->GetXaxis()->SetBinLabel(14,"Fail");



  //QG variable distributions with eta requirements
  for(int cut=0; cut<40; cut++){
    if(event.GetVar(Mva::jetNTracks0)<cut) hnTrackCut0->Fill(cut,weight);
    if(event.GetVar(Mva::jetNTracks1)<cut) hnTrackCut1->Fill(cut,weight);
  }

  for(float cut2=0.00025; cut2<0.4; cut2+=0.005){
    if(event.GetVar(Mva::jetTrackWidth0)<cut2) hTrackWidthCut0->Fill(cut2,weight);
    if(event.GetVar(Mva::jetTrackWidth1)<cut2) hTrackWidthCut1->Fill(cut2,weight);
  }

  for(int cut=0; cut<80; cut++){
    if(event.GetVar(Mva::jetNTracks0)+event.GetVar(Mva::jetNTracks1)<cut) hnTrackCutSum->Fill(cut,weight);
  }

  for(float cut2=0.00025; cut2<0.8; cut2+=0.005){
    if(event.GetVar(Mva::jetTrackWidth0)+event.GetVar(Mva::jetTrackWidth1)<cut2) hTrackWidthCutSum->Fill(cut2,weight);
  }

  hnTrackSum->Fill(event.GetVar(Mva::jetNTracks0)+event.GetVar(Mva::jetNTracks1),weight);
  hTrackWidthSum->Fill(event.GetVar(Mva::jetTrackWidth0)+event.GetVar(Mva::jetTrackWidth1),weight);


  // testing
  float max_j_eta=fabs(event.jets.at(0).eta);
  if(event.jets.size()>1)
    if(fabs(event.jets.at(1).eta)>max_j_eta) max_j_eta= fabs(event.jets.at(1).eta);
  if(hmax_j_eta)  hmax_j_eta->Fill(max_j_eta, weight);
  if(event.jets.size()>2){
         
    TLorentzVector tmp;
    const TLorentzVector j1v = event.jets.at(0).GetLVec();
    const TLorentzVector j2v = event.jets.at(1).GetLVec();
    for(unsigned iJet=2; iJet<event.jets.size(); ++iJet){
      tmp=event.jets.at(iJet).GetLVec();
      hcentrality->Fill(event.GetVar(Mva::maxCentrality), weight);
      
      float dRj1=tmp.DeltaR(j1v);
      float dRj2=tmp.DeltaR(j2v);
      hdRj1->Fill(dRj1, weight);
      hdRj2->Fill(dRj2, weight);
      hminDR->Fill(std::min(dRj1,dRj2), weight);
      
      float mj1 =  (tmp+j1v).M();
      float mj2 =  (tmp+j2v).M();
      hmj1->Fill(mj1, weight);
      hmj2->Fill(mj2, weight);
      hminDRmj2->Fill((dRj1<dRj2 ? mj1 : mj2), weight);
      hmin_mj3->Fill(std::min(mj1,mj2), weight);
      hmin_mj3_over_mjj->Fill(event.GetVar(Mva::maxmj3_over_mjj), weight);
    }
    if(event.jets.size()>3){
      float mj34 = (event.jets.at(2).GetLVec()+event.jets.at(3).GetLVec()).M();
      if(hmj34) hmj34->Fill(mj34, weight);
    }
    if(hj3Pt) hj3Pt->Fill(event.jets.at(2).pt, weight);
    if(hj3Eta) hj3Eta->Fill(event.jets.at(2).eta, weight);
    if(hj3Jvt) hj3Jvt->Fill(event.jets.at(2).GetVar(Mva::jvt), weight);
    if(hj3FJvt) hj3FJvt->Fill(event.jets.at(2).GetVar(Mva::fjvt), weight);
  }
  // end testing

  // jet DR
  float minDR=999.0;
  for(unsigned il=0; il<event.muons.size(); ++il){
    if(hptvarcone20 && event.muons.at(il).HasVar(Mva::ptvarcone20)) hptvarcone20->Fill(event.muons.at(il).GetVar(Mva::ptvarcone20), weight);
    if(hptvarcone30 && event.muons.at(il).HasVar(Mva::ptvarcone30)) hptvarcone30->Fill(event.muons.at(il).GetVar(Mva::ptvarcone30), weight);
    if(htopoetcone20 && event.muons.at(il).HasVar(Mva::topoetcone20)) htopoetcone20->Fill(event.muons.at(il).GetVar(Mva::topoetcone20), weight);     
    for(unsigned ij=0; ij<event.jets.size(); ++ij){
      float qDR = event.jets.at(ij).GetVec().DeltaR(event.muons.at(il).GetVec());
      if(minDR>qDR) minDR = qDR;
    }
  }
  for(unsigned il=0; il<event.electrons.size(); ++il){
    if(hptvarcone20 && event.electrons.at(il).HasVar(Mva::ptvarcone20)) hptvarcone20->Fill(event.electrons.at(il).GetVar(Mva::ptvarcone20), weight);
    if(hptvarcone30 && event.electrons.at(il).HasVar(Mva::ptvarcone30)) hptvarcone30->Fill(event.electrons.at(il).GetVar(Mva::ptvarcone30), weight);
    if(htopoetcone20 && event.electrons.at(il).HasVar(Mva::topoetcone20)) htopoetcone20->Fill(event.electrons.at(il).GetVar(Mva::topoetcone20), weight);        
    for(unsigned ij=0; ij<event.jets.size(); ++ij){
      float qDR = event.jets.at(ij).GetVec().DeltaR(event.electrons.at(il).GetVec());
      if(minDR>qDR) minDR = qDR;
    }
  }  
  hminDRLep->Fill(minDR, weight);
  
  // fill stored variables
  for(unsigned a=0; a<fVarVec.size(); ++a){
    FillHist(fHistVec[fVarVec[a]], fVarVec[a], event, weight);
  }  
  return true;
}

//-----------------------------------------------------------------------------
void Msl::PlotEvent::DoSave(TDirectory *idir)
{
  //
  // Plot stored variables
  //
  for(unsigned i = 0; i < fVars.size(); ++i) {
    PlotVar(fVars.at(i));
  }

  //
  // Save histograms
  //
  IExecAlg::DoSave(idir);
}

//-----------------------------------------------------------------------------
void Msl::PlotEvent::PlotVar(const Mva::Var var)
{
  //
  // Make and fill histogram for output variables
  //
  if(!HasVar(var)) {
    return;
  }

  const pair<double, double> res = GetMinMax(var); 
  if(!(res.first < res.second)) {
    return;
  }

  //
  // Book histogram
  //
  const double vpad = 0.01*(res.second-res.first);

  TH1 *h = GetTH1(fVarPref+Mva::Convert2Str(var), fNBin, res.first-vpad, res.second+vpad);

  h->GetXaxis()->CenterTitle();
  h->GetXaxis()->SetTitle(Mva::Convert2Str(var).c_str());

  //
  // Fill histogram
  //
  FillHist(h, var);
}

//-----------------------------------------------------------------------------
bool Msl::PlotEvent::HasVar(Mva::Var var) const
{
  return std::find(fVars.begin(), fVars.end(), var) != fVars.end();
}

//-----------------------------------------------------------------------------
std::pair<double, double> Msl::PlotEvent::GetMinMax(Mva::Var var) const
{
  //
  // Compute min/max value for stored variable
  //
  pair<double, double> res(0.0, 0.0);

  if(var == Mva::NONE) {
    return res;
  }

  for(unsigned i = 0; i < fEvents.size(); ++i) {
    const VarStore &event = fEvents.at(i);
    
    double val = 0.0;
    if(event.GetVar(var, val)) {
      res.first  = std::min<double>(res.first,  val);
      res.second = std::max<double>(res.second, val);
    }
  }

  return res;
}

//-----------------------------------------------------------------------------
void Msl::PlotEvent::FillHist(TH1 *h, Mva::Var var) const
{
  //
  // Fill histogram
  //
  if(var == Mva::NONE || !h) {
    return;
  }

  for(unsigned i = 0; i < fEvents.size(); ++i) {
    const VarStore &event = fEvents.at(i);

    double val = 0.0;
    if(event.GetVar(var, val)) {
      h->Fill(val, event.GetWeight());
    }
  }
}

//-----------------------------------------------------------------------------
double Msl::PlotEvent::FillHist(TH1 *h, Mva::Var var, const Event &event, double weight) const
{
  double val = 0.0;

  if(!h) {
    return val;
  }

  if(event.GetVar(var, val)) {
    h->Fill(val, weight);
  }

  return val;
}
