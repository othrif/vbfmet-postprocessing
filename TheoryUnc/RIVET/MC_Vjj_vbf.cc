#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/ChargedLeptons.hh"
#include "Rivet/Projections/MissingMomentum.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/DressedLeptons.hh"
#include "Rivet/Projections/MissingMomentum.hh"

namespace Rivet {

  class Re_Vjj_vbf : public Analysis {

#include "NLOHisto1D.cc"


  public:

    /// Minimal constructor
    Re_Vjj_vbf(string name="Re_Vjj_vbf") : Analysis(name)
    {
	_mode = 1; //Z->ee
	_cuts  = 1;
    }

    double cut_R  = 0.4;
    double cut_etaj = 4.5;
    double cut_pTj1  = 50.;
    double cut_pTj2  = 50.;
    double cut_pTV  = 150.;
    double cut_mTW = 0.;
    double cut_MET = 0.;
    double cut_mjj = 500.;
    double cut_detajj = 2.5;

    /// @name Analysis methods
    //@{

    /// Set up projections and book histograms
    void init() {

      // Base final state definition
      const FinalState fs;

      // Visible final state for lepton isolation
      VisibleFinalState visfs;
      addProjection(visfs, "visfs");

      // Neutrinos for MET
      IdentifiedFinalState neutrinos;
      neutrinos.acceptNeutrinos();
      addProjection(neutrinos, "Neutrinos");

      // Get photons used to dress leptons
      IdentifiedFinalState photons(fs);
      photons.acceptId(PID::PHOTON);

      // Use all bare electrons & muons as input to the DressedLeptons projection
      IdentifiedFinalState bareleptons(fs);
      bareleptons.acceptChLeptons();

      const Cut eta_l_ranges = Cuts::abseta < 99999.;
      DressedLeptons all_leptons(photons, bareleptons, 0.1, eta_l_ranges, true, true);
      DressedLeptons leptons(photons, bareleptons, 0.1, eta_l_ranges && Cuts::pT > 0*GeV, true, true);
      declare(leptons, "leptons");

      // Jet clustering
      VetoedFinalState vfs(fs);
      vfs.addVetoOnThisFinalState(all_leptons);
      vfs.addVetoOnThisFinalState(neutrinos);

      FastJets jets(vfs, FastJets::ANTIKT, cut_R);
      addProjection(jets, "Jets");


      const std::vector<double> bins_Mjj {0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2500,3000,3500,4000,6000,8000,10000,13000};
      const std::vector<double> bins_pTV = {10,20,30,40,50,75,100,125,150,175,200,225,250,275,300,350,400,450,500,600,700,800,900,1000,2000,3000,13000};

      // Booking of histograms
      _histos["SCALUP"] = bookNLOHisto1D("SCALUP", logspace(100, 50.0, 5000.0));
      _histos["ht"] = bookNLOHisto1D("ht", logspace(100, 50.0, 5000.0));
      _histos["SCALUP_over_ht"] = bookNLOHisto1D("SCALUP_over_ht", logspace(40, 0.1, 10));
      _histos["inc"] = bookNLOHisto1D("incl", 1, 0, 1);
      _histos["j1j2_M_log"] = bookNLOHisto1D("j1j2_M_log", logspace(100, 10.0, 5000.0));
      _histos["j1j2_M"] = bookNLOHisto1D("j1j2_M", bins_Mjj);
      _histos["V_pT"] = bookNLOHisto1D("V_pT", bins_pTV);
      _histos["V_pT_log"] = bookNLOHisto1D("V_pT_log", logspace(100, 10.0, 5000.0));
      _histos["j1j2_deta"] = bookNLOHisto1D("j1j2_deta", 20, 0, 7);
      _histos["j1j2_dphi"] = bookNLOHisto1D("j1j2_dphi", 20, 0, M_PI);
      _histos["j1j2_pT"] = bookNLOHisto1D("j1j2_pT", logspace(100, 30.0, 3000.0));
      _histos["j1_pT"] = bookNLOHisto1D("j1_pT", logspace(100, 30.0, 3000.0));
      _histos["j2_pT"] = bookNLOHisto1D("j2_pT", logspace(100, 30.0, 3000.0));
      _histos["j3_pT"] = bookNLOHisto1D("j3_pT", logspace(100, 10.0, 1000.0));
      _histos["j1_eta"] = bookNLOHisto1D("j1_eta", 20, -7, 7);
      _histos["j2_eta"] = bookNLOHisto1D("j2_eta", 20, -7, 7);
      _histos["j3_eta"] = bookNLOHisto1D("j3_eta", 20, -7, 7);
      _histos["l1_pT"] = bookNLOHisto1D("l1_pT", logspace(100, 25.0, 2500.0));
      _histos["l2_pT"] = bookNLOHisto1D("l2_pT", logspace(100, 25.0, 2500.0));
      _histos["l1_eta"] = bookNLOHisto1D("l1_eta", 10, -3, 3);
      _histos["l2_eta"] = bookNLOHisto1D("l2_eta", 10, -3, 3);
      _histos["l1l2_M"] = bookNLOHisto1D("l1l2_M", 40, 20, 200);

      _histos["cjv_inc"] = bookNLOHisto1D("cjv_incl", 1, 0, 1);
      _histos["cjv_j1j2_M_log"] = bookNLOHisto1D("cjv_j1j2_M_log", logspace(100, 600.0, 6000.0));
      _histos["cjv_j1j2_M"] = bookNLOHisto1D("cjv_j1j2_M", bins_Mjj);
      _histos["cjv_V_pT"] = bookNLOHisto1D("cjv_V_pT", bins_pTV);
      _histos["cjv_V_pT_log"] = bookNLOHisto1D("cjv_V_pT_log", logspace(100, 50.0, 5000.0));
      _histos["cjv_j1j2_deta"] = bookNLOHisto1D("cjv_j1j2_deta", 20, 0, 7);
      _histos["cjv_j1j2_dphi"] = bookNLOHisto1D("cjv_j1j2_dphi", 20, 0, M_PI);
      _histos["cjv_j1j2_pT"] = bookNLOHisto1D("cjv_j1j2_pT", logspace(100, 30.0, 3000.0));
      _histos["cjv_j1_pT"] = bookNLOHisto1D("cjv_j1_pT", logspace(100, 30.0, 3000.0));
      _histos["cjv_j2_pT"] = bookNLOHisto1D("cjv_j2_pT", logspace(100, 30.0, 3000.0));
      _histos["cjv_j1_eta"] = bookNLOHisto1D("cjv_j1_eta", 20, -7, 7);
      _histos["cjv_j2_eta"] = bookNLOHisto1D("cjv_j2_eta", 20, -7, 7);
      _histos["cjv_l1_pT"] = bookNLOHisto1D("cjv_l1_pT", logspace(100, 25.0, 2500.0));
      _histos["cjv_l2_pT"] = bookNLOHisto1D("cjv_l2_pT", logspace(100, 25.0, 2500.0));
      _histos["cjv_l1_eta"] = bookNLOHisto1D("cjv_l1_eta", 10, -3, 3);
      _histos["cjv_l2_eta"] = bookNLOHisto1D("cjv_l2_eta", 10, -3, 3);
      _histos["cjv_l1l2_M"] = bookNLOHisto1D("cjv_l1l2_M", 40, 20, 200);

      _histos["lcuts_inc"] = bookNLOHisto1D("lcuts_incl", 1, 0, 1);
      _histos["lcuts_j1j2_M_log"] = bookNLOHisto1D("lcuts_j1j2_M_log", logspace(100, 600.0, 6000.0));
      _histos["lcuts_j1j2_M"] = bookNLOHisto1D("lcuts_j1j2_M", bins_Mjj);
      _histos["lcuts_V_pT"] = bookNLOHisto1D("lcuts_V_pT", bins_pTV);
      _histos["lcuts_V_pT_log"] = bookNLOHisto1D("lcuts_V_pT_log", logspace(100, 50.0, 5000.0));
      _histos["lcuts_j1j2_deta"] = bookNLOHisto1D("lcuts_j1j2_deta", 20, 0, 7);
      _histos["lcuts_j1j2_dphi"] = bookNLOHisto1D("lcuts_j1j2_dphi", 20, 0, M_PI);
      _histos["lcuts_j1j2_pT"] = bookNLOHisto1D("lcuts_j1j2_pT", logspace(100, 30.0, 3000.0));
      _histos["lcuts_j1_pT"] = bookNLOHisto1D("lcuts_j1_pT", logspace(100, 30.0, 3000.0));
      _histos["lcuts_j2_pT"] = bookNLOHisto1D("lcuts_j2_pT", logspace(100, 30.0, 3000.0));
      _histos["lcuts_j3_pT"] = bookNLOHisto1D("lcuts_j3_pT", logspace(100, 30.0, 3000.0));
      _histos["lcuts_j1_eta"] = bookNLOHisto1D("lcuts_j1_eta", 20, -7, 7);
      _histos["lcuts_j2_eta"] = bookNLOHisto1D("lcuts_j2_eta", 20, -7, 7);
      _histos["lcuts_j3_eta"] = bookNLOHisto1D("lcuts_j3_eta", 20, -7, 7);
      _histos["lcuts_l1_pT"] = bookNLOHisto1D("lcuts_l1_pT", logspace(100, 25.0, 2500.0));
      _histos["lcuts_l2_pT"] = bookNLOHisto1D("lcuts_l2_pT", logspace(100, 25.0, 2500.0));
      _histos["lcuts_l1_eta"] = bookNLOHisto1D("lcuts_l1_eta", 10, -3, 3);
      _histos["lcuts_l2_eta"] = bookNLOHisto1D("lcuts_l2_eta", 10, -3, 3);
      _histos["lcuts_l1l2_M"] = bookNLOHisto1D("lcuts_l1l2_M", 40, 20, 200);

      _histos["lcuts_cjv_inc"] = bookNLOHisto1D("lcuts_cjv_incl", 1, 0, 1);
      _histos["lcuts_cjv_j1j2_M_log"] = bookNLOHisto1D("lcuts_cjv_j1j2_M_log", logspace(100, 600.0, 6000.0));
      _histos["lcuts_cjv_j1j2_M"] = bookNLOHisto1D("lcuts_cjv_j1j2_M", bins_Mjj);
      _histos["lcuts_cjv_V_pT"] = bookNLOHisto1D("lcuts_cjv_V_pT", bins_pTV);
      _histos["lcuts_cjv_V_pT_log"] = bookNLOHisto1D("lcuts_cjv_V_pT_log", logspace(100, 50.0, 5000.0));
      _histos["lcuts_cjv_j1j2_deta"] = bookNLOHisto1D("lcuts_cjv_j1j2_deta", 20, 0, 7);
      _histos["lcuts_cjv_j1j2_dphi"] = bookNLOHisto1D("lcuts_cjv_j1j2_dphi", 20, 0, M_PI);
      _histos["lcuts_cjv_j1j2_pT"] = bookNLOHisto1D("lcuts_cjv_j1j2_pT", logspace(100, 30.0, 3000.0));
      _histos["lcuts_cjv_j1_pT"] = bookNLOHisto1D("lcuts_cjv_j1_pT", logspace(100, 30.0, 3000.0));
      _histos["lcuts_cjv_j2_pT"] = bookNLOHisto1D("lcuts_cjv_j2_pT", logspace(100, 30.0, 3000.0));
      _histos["lcuts_cjv_j1_eta"] = bookNLOHisto1D("lcuts_cjv_j1_eta", 20, -7, 7);
      _histos["lcuts_cjv_j2_eta"] = bookNLOHisto1D("lcuts_cjv_j2_eta", 20, -7, 7);
      _histos["lcuts_cjv_l1_pT"] = bookNLOHisto1D("lcuts_cjv_l1_pT", logspace(100, 25.0, 2500.0));
      _histos["lcuts_cjv_l2_pT"] = bookNLOHisto1D("lcuts_cjv_l2_pT", logspace(100, 25.0, 2500.0));
      _histos["lcuts_cjv_l1_eta"] = bookNLOHisto1D("lcuts_cjv_l1_eta", 10, -3, 3);
      _histos["lcuts_cjv_l2_eta"] = bookNLOHisto1D("lcuts_cjv_l2_eta", 10, -3, 3);
      _histos["lcuts_cjv_l1l2_M"] = bookNLOHisto1D("lcuts_cjv_l1l2_M", 40, 20, 200);


    }


    void analyze(const Event& event) {

     if (_cuts == -1) {
	cut_pTj1 = 100.;
	cut_pTj2 = 100.;
	cut_pTV = 10.;
	cut_mjj = 0;
	cut_detajj = 0.;
     }  else if (_cuts == -2) {
	cut_pTj1 = 100.;
	cut_pTj2 = 50.;
	cut_pTV = 150.;
	cut_mjj = 500;
	cut_detajj = 2.5;
     } else {
	cut_pTj1 = 50.;
	cut_pTj2 = 50.;
	cut_pTV = 150.;
	cut_mjj = 500.;
	cut_detajj = 2.5;
     }



     const FastJets& jetproj = applyProjection<FastJets>(event, "Jets");

     // Apply cuts on jets
     Jets jets;
     double htjets = 0;
     foreach(const Jet& jet_iter,jetproj.jetsByPt( 0.*GeV )) {
      if( jet_iter.momentum().abseta() < cut_etaj ) {
        jets.push_back(jet_iter);
        htjets+=jet_iter.momentum().pT();
      }
     }


     //VBF selection
     if (jets.size() < 2) vetoEvent;
     if (jets[0].momentum().pT() < cut_pTj1) vetoEvent;
     if (jets[1].momentum().pT() < cut_pTj2) vetoEvent;

     double mjj=(jets[0].momentum()+jets[1].momentum()).mass();
     if (mjj < cut_mjj) vetoEvent;

     double detajj=deltaEta(jets[0].momentum(),jets[1].momentum());
     if (detajj < cut_detajj) vetoEvent;

     //MET
     FourMomentum met;
     ParticleVector neutrinos;
     foreach( const Particle & p, applyProjection<IdentifiedFinalState>(event, "Neutrinos").particlesByPt()) {
         neutrinos.push_back(p);
         met+=p.momentum();
     }


     //isolate leptons
     ParticleVector visible = applyProjection<FinalState>(event, "visfs").particles();
     const vector<DressedLepton>& leptons = apply<DressedLeptons>(event, "leptons").dressedLeptons();


     FourMomentum vec;
     bool lcuts = false;
     if (_mode == 1) {
	     //Z->ll selection
	     if (leptons.size() < 2) vetoEvent;
	     if ((leptons[0].momentum()+leptons[1].momentum()).mass() < 30) vetoEvent;
	     vec = leptons[0].momentum()+leptons[1].momentum();
	     if (leptons[0].momentum().pT() > 30 && abs(leptons[0].momentum().eta()) < 2.5
	      && leptons[1].momentum().pT() > 30 && abs(leptons[1].momentum().eta()) < 2.5
		) lcuts = true;
     } else if (_mode == 2) {
	     //W->ln selection
	     if (leptons.size() < 1 || neutrinos.size() < 1) vetoEvent;
	     vec = leptons[0].momentum()+neutrinos[0].momentum();
	     if (leptons[0].momentum().pT() > 30 && abs(leptons[0].momentum().eta()) < 2.5) lcuts = true;
     } else if (_mode == 3) {
	     //Z->nn selection
	     if (neutrinos.size() < 2) vetoEvent;
	     vec = neutrinos[0].momentum()+neutrinos[1].momentum();
	     lcuts = true;
     }

     double pTV = vec.pT();
     if (pTV < cut_pTV) vetoEvent;

     double ht = sqrt(vec.pT()*vec.pT()+vec.mass()*vec.mass());

     //third jet
     bool cjv = true;
     if (jets.size() > 2) {
	if (jets[2].momentum().pT() > 25) cjv = false;
     }

     double scalup=event.genEvent()->event_scale();
     _histos["SCALUP"]->fill( scalup ,event );
     _histos["ht"]->fill( ht ,event );
     _histos["SCALUP_over_ht"]->fill( (ht>0) ? scalup/ht : 0 ,event );
     _histos["inc"]->fill(0.5, event);
     _histos["j1j2_M"]->fill(mjj, event);
     _histos["j1j2_M_log"]->fill(mjj, event);
     _histos["j1j2_deta"]->fill(detajj, event);
     _histos["j1j2_dphi"]->fill(deltaPhi(jets[0].momentum(),jets[1].momentum()), event);
     _histos["j1j2_pT"]->fill((jets[0].momentum()+jets[1].momentum()).pT(), event);
     _histos["j1_pT"]->fill(jets[0].momentum().pT(), event);
     _histos["j2_pT"]->fill(jets[1].momentum().pT(), event);
     if (jets.size() > 2) _histos["j3_pT"]->fill(jets[2].momentum().pT(), event);
     _histos["j1_eta"]->fill(jets[0].momentum().eta(), event);
     _histos["j2_eta"]->fill(jets[1].momentum().eta(), event);
     if (jets.size() > 2) _histos["j3_eta"]->fill(jets[2].momentum().eta(), event);

     _histos["V_pT"]->fill(pTV, event);
     _histos["V_pT_log"]->fill(pTV, event);

     if(_mode == 1) {
	_histos["l1l2_M"]->fill((leptons[0].momentum()+leptons[1].momentum()).mass(), event);
	_histos["l1_pT"]->fill(leptons[0].momentum().pT(), event);
     	_histos["l2_pT"]->fill(leptons[1].momentum().pT(), event);
	_histos["l1_eta"]->fill(leptons[0].momentum().eta(), event);
     	_histos["l2_eta"]->fill(leptons[1].momentum().eta(), event);
     }
     if(_mode == 2) {
	_histos["l1_pT"]->fill(leptons[0].momentum().pT(), event);
     	_histos["l2_pT"]->fill(neutrinos[0].momentum().pT(), event);
	_histos["l1_eta"]->fill(leptons[0].momentum().eta(), event);
     	_histos["l2_eta"]->fill(neutrinos[0].momentum().eta(), event);
     }
     if(_mode == 3) {
	_histos["l1_pT"]->fill(neutrinos[0].momentum().pT(), event);
     	_histos["l2_pT"]->fill(neutrinos[1].momentum().pT(), event);
	_histos["l1_eta"]->fill(neutrinos[0].momentum().eta(), event);
     	_histos["l2_eta"]->fill(neutrinos[1].momentum().eta(), event);
     }


     if (cjv) {
	     _histos["cjv_inc"]->fill(0.5, event);
	     _histos["cjv_j1j2_M"]->fill(mjj, event);
	     _histos["cjv_j1j2_M_log"]->fill(mjj, event);
	     _histos["cjv_j1j2_deta"]->fill(detajj, event);
	     _histos["cjv_j1j2_dphi"]->fill(deltaPhi(jets[0].momentum(),jets[1].momentum()), event);
	     _histos["cjv_j1j2_pT"]->fill((jets[0].momentum()+jets[1].momentum()).pT(), event);
	     _histos["cjv_j1_pT"]->fill(jets[0].momentum().pT(), event);
	     _histos["cjv_j2_pT"]->fill(jets[1].momentum().pT(), event);
	     _histos["cjv_j1_eta"]->fill(jets[0].momentum().eta(), event);
	     _histos["cjv_j2_eta"]->fill(jets[1].momentum().eta(), event);

	     _histos["cjv_V_pT"]->fill(pTV, event);
	     _histos["cjv_V_pT_log"]->fill(pTV, event);

	     if(_mode == 1) {
		_histos["cjv_l1l2_M"]->fill((leptons[0].momentum()+leptons[1].momentum()).mass(), event);
		_histos["cjv_l1_pT"]->fill(leptons[0].momentum().pT(), event);
		_histos["cjv_l2_pT"]->fill(leptons[1].momentum().pT(), event);
		_histos["cjv_l1_eta"]->fill(leptons[0].momentum().eta(), event);
		_histos["cjv_l2_eta"]->fill(leptons[1].momentum().eta(), event);
	     }
	     if(_mode == 2) {
		_histos["cjv_l1_pT"]->fill(leptons[0].momentum().pT(), event);
		_histos["cjv_l2_pT"]->fill(neutrinos[0].momentum().pT(), event);
		_histos["cjv_l1_eta"]->fill(leptons[0].momentum().eta(), event);
		_histos["cjv_l2_eta"]->fill(neutrinos[0].momentum().eta(), event);
	     }
	     if(_mode == 3) {
		_histos["cjv_l1_pT"]->fill(neutrinos[0].momentum().pT(), event);
		_histos["cjv_l2_pT"]->fill(neutrinos[1].momentum().pT(), event);
		_histos["cjv_l1_eta"]->fill(neutrinos[0].momentum().eta(), event);
		_histos["cjv_l2_eta"]->fill(neutrinos[1].momentum().eta(), event);
	     }
     }


     if (lcuts) {

	     _histos["lcuts_inc"]->fill(0.5, event);
	     _histos["lcuts_j1j2_M"]->fill(mjj, event);
	     _histos["lcuts_j1j2_M_log"]->fill(mjj, event);
	     _histos["lcuts_j1j2_deta"]->fill(detajj, event);
	     _histos["lcuts_j1j2_dphi"]->fill(deltaPhi(jets[0].momentum(),jets[1].momentum()), event);
	     _histos["lcuts_j1j2_pT"]->fill((jets[0].momentum()+jets[1].momentum()).pT(), event);
	     _histos["lcuts_j1_pT"]->fill(jets[0].momentum().pT(), event);
	     _histos["lcuts_j2_pT"]->fill(jets[1].momentum().pT(), event);
	     if (jets.size() > 2) _histos["j3_pT"]->fill(jets[2].momentum().pT(), event);
	     _histos["lcuts_j1_eta"]->fill(jets[0].momentum().eta(), event);
	     _histos["lcuts_j2_eta"]->fill(jets[1].momentum().eta(), event);
	     if (jets.size() > 2) _histos["j3_eta"]->fill(jets[2].momentum().eta(), event);

	     _histos["lcuts_V_pT"]->fill(pTV, event);
	     _histos["lcuts_V_pT_log"]->fill(pTV, event);

	     if(_mode == 1) {
		_histos["lcuts_l1l2_M"]->fill((leptons[0].momentum()+leptons[1].momentum()).mass(), event);
		_histos["lcuts_l1_pT"]->fill(leptons[0].momentum().pT(), event);
		_histos["lcuts_l2_pT"]->fill(leptons[1].momentum().pT(), event);
		_histos["lcuts_l1_eta"]->fill(leptons[0].momentum().eta(), event);
		_histos["lcuts_l2_eta"]->fill(leptons[1].momentum().eta(), event);
	     }
	     if(_mode == 2) {
		_histos["lcuts_l1_pT"]->fill(leptons[0].momentum().pT(), event);
		_histos["lcuts_l2_pT"]->fill(neutrinos[0].momentum().pT(), event);
		_histos["lcuts_l1_eta"]->fill(leptons[0].momentum().eta(), event);
		_histos["lcuts_l2_eta"]->fill(neutrinos[0].momentum().eta(), event);
	     }
	     if(_mode == 3) {
		_histos["lcuts_l1_pT"]->fill(neutrinos[0].momentum().pT(), event);
		_histos["lcuts_l2_pT"]->fill(neutrinos[1].momentum().pT(), event);
		_histos["lcuts_l1_eta"]->fill(neutrinos[0].momentum().eta(), event);
		_histos["lcuts_l2_eta"]->fill(neutrinos[1].momentum().eta(), event);
	     }


	     if (cjv) {
		     _histos["lcuts_cjv_inc"]->fill(0.5, event);
		     _histos["lcuts_cjv_j1j2_M"]->fill(mjj, event);
		     _histos["lcuts_cjv_j1j2_M_log"]->fill(mjj, event);
		     _histos["lcuts_cjv_j1j2_deta"]->fill(detajj, event);
		     _histos["lcuts_cjv_j1j2_dphi"]->fill(deltaPhi(jets[0].momentum(),jets[1].momentum()), event);
		     _histos["lcuts_cjv_j1j2_pT"]->fill((jets[0].momentum()+jets[1].momentum()).pT(), event);
		     _histos["lcuts_cjv_j1_pT"]->fill(jets[0].momentum().pT(), event);
		     _histos["lcuts_cjv_j2_pT"]->fill(jets[1].momentum().pT(), event);
		     _histos["lcuts_cjv_j1_eta"]->fill(jets[0].momentum().eta(), event);
		     _histos["lcuts_cjv_j2_eta"]->fill(jets[1].momentum().eta(), event);

		     _histos["lcuts_cjv_V_pT"]->fill(pTV, event);
		     _histos["lcuts_cjv_V_pT_log"]->fill(pTV, event);

		     if(_mode == 1) {
			_histos["lcuts_cjv_l1l2_M"]->fill((leptons[0].momentum()+leptons[1].momentum()).mass(), event);
			_histos["lcuts_cjv_l1_pT"]->fill(leptons[0].momentum().pT(), event);
			_histos["lcuts_cjv_l2_pT"]->fill(leptons[1].momentum().pT(), event);
			_histos["lcuts_cjv_l1_eta"]->fill(leptons[0].momentum().eta(), event);
			_histos["lcuts_cjv_l2_eta"]->fill(leptons[1].momentum().eta(), event);
		     }
		     if(_mode == 2) {
			_histos["lcuts_cjv_l1_pT"]->fill(leptons[0].momentum().pT(), event);
			_histos["lcuts_cjv_l2_pT"]->fill(neutrinos[0].momentum().pT(), event);
			_histos["lcuts_cjv_l1_eta"]->fill(leptons[0].momentum().eta(), event);
			_histos["lcuts_cjv_l2_eta"]->fill(neutrinos[0].momentum().eta(), event);
		     }
		     if(_mode == 3) {
			_histos["lcuts_cjv_l1_pT"]->fill(neutrinos[0].momentum().pT(), event);
			_histos["lcuts_cjv_l2_pT"]->fill(neutrinos[1].momentum().pT(), event);
			_histos["lcuts_cjv_l1_eta"]->fill(neutrinos[0].momentum().eta(), event);
			_histos["lcuts_cjv_l2_eta"]->fill(neutrinos[1].momentum().eta(), event);
		     }
	     }

     }


    }

    /// Finalize
    void finalize() {

       double NORM=crossSection()/sumOfWeights();

       for (std::map<string,NLOHisto1DPtr>::iterator hit=_histos.begin(); hit!=_histos.end();hit++) {
         hit->second->finalize();
         scale(hit->second,NORM);
       }

    }

  protected:
    size_t _mode;
    int _cuts;

  private:
	std::map<string,NLOHisto1DPtr> _histos;

  };


  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(Re_Vjj_vbf);

  //Additional hooks
  struct Re_Vjj_vbf_ee : public Re_Vjj_vbf {
   Re_Vjj_vbf_ee() : Re_Vjj_vbf("Re_Vjj_vbf_ee") { _mode = 1; }
  };
  DECLARE_RIVET_PLUGIN(Re_Vjj_vbf_ee);

  struct Re_Vjj_vbf_en : public Re_Vjj_vbf {
   Re_Vjj_vbf_en() : Re_Vjj_vbf("Re_Vjj_vbf_en") { _mode = 2; }
  };
  DECLARE_RIVET_PLUGIN(Re_Vjj_vbf_en);

 struct Re_Vjj_vbf_en_inc : public Re_Vjj_vbf {
   Re_Vjj_vbf_en_inc() : Re_Vjj_vbf("Re_Vjj_vbf_en_inc") { _mode = 2; _cuts=-1; }
  };
  DECLARE_RIVET_PLUGIN(Re_Vjj_vbf_en_inc);

 struct Re_Vjj_vbf_en_asym : public Re_Vjj_vbf {
   Re_Vjj_vbf_en_asym() : Re_Vjj_vbf("Re_Vjj_vbf_en_asym") { _mode = 2; _cuts=-2; }
  };
  DECLARE_RIVET_PLUGIN(Re_Vjj_vbf_en_asym);

  struct Re_Vjj_vbf_nn : public Re_Vjj_vbf {
   Re_Vjj_vbf_nn() : Re_Vjj_vbf("Re_Vjj_vbf_nn") { _mode = 3; }
  };
  DECLARE_RIVET_PLUGIN(Re_Vjj_vbf_nn);

 struct Re_Vjj_vbf_nn_inc : public Re_Vjj_vbf {
   Re_Vjj_vbf_nn_inc() : Re_Vjj_vbf("Re_Vjj_vbf_nn_inc") { _mode = 3; _cuts=-1; }
  };
  DECLARE_RIVET_PLUGIN(Re_Vjj_vbf_nn_inc);

 struct Re_Vjj_vbf_nn_asym : public Re_Vjj_vbf {
   Re_Vjj_vbf_nn_asym() : Re_Vjj_vbf("Re_Vjj_vbf_nn_asym") { _mode = 3; _cuts=-2; }
  };
  DECLARE_RIVET_PLUGIN(Re_Vjj_vbf_nn_asym);



}
