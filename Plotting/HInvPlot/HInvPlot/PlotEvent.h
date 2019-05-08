#ifndef MSL_PLOTEVENT_H
#define MSL_PLOTEVENT_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : PlotEvent
 * @Author : Doug Schaefer
 *
 * @Brief  :
 * 
 *  Algorithm for plotting reconstructed variables for di-lepton pairs
 * 
 **********************************************************************************/

// Local
#include "IExecAlg.h"
#include "VarStore.h"
#include "Registry.h"

class TH1;
class TH2;
class TH3;

namespace Msl
{
  class PlotEvent: public virtual IExecAlg
  {
  public:

    PlotEvent();
    virtual ~PlotEvent();
    
    void DoConf(const Registry &reg);

    bool DoExec(Msl::Event &event);

    void DoSave(TDirectory *dir);
    
    void SetPassAlg(IExecAlg *alg) { fPassAlg = alg; }

    //
    // Specialized functions for working with stored variables
    //
    bool HasVar(Mva::Var var) const;    
    
    std::pair<double, double> GetMinMax(Mva::Var var) const;

    void PlotVar(const Mva::Var var);

    unsigned           GetNBinLim() const { return fNBinLim; }
    const std::string& GetSelKey () const { return fSelKey;  }
    const std::string& GetRegion () const { return fRegion;  }
    
    const std::vector<Msl::VarStore>& GetEvents() const { return fEvents; }

    void FillHist(TH1 *h, Mva::Var var) const;
    
    double FillHist(TH1 *h, Mva::Var var, const Msl::Event &event, double weight) const;

  public:

    typedef std::vector<Msl::Mva::Var> MvaVec;
    typedef std::vector<Msl::VarStore> EventVec;

  private:

    // Variables:
    unsigned                    fNBin;
    unsigned                    fNBinLim;
    unsigned                    fDetailLvl;

    std::string                 fSelKey;
    std::string                 fRegion;
    std::string                 fVarPref;

    IExecAlg                   *fPassAlg;
    Mva::SampleSet              fSample;
    
    MvaVec                      fVars;
    EventVec                    fEvents;

    // Plotting
    std::vector<Mva::Var>       fVarVec;
    std::vector<int>            fNBinVec;
    std::vector<double>         fLoVec;
    std::vector<double>         fHiVec;
    
    // Histograms:
    TH1                        *hTruthMuPt;
    TH1                        *hTruthMuEta;
    TH1                        *hBaseMuPt;
    TH1                        *hBaseMuEta;
    TH1                        *hTruthElPt;
    TH1                        *hTruthElEta;    
    TH1                        *hBaseElPt;
    TH1                        *hBaseElEta;
    TH1                        *hTruthTauPt;
    TH1                        *hTruthTauDR;
    TH1                        *hTruthTauEta;    
    TH1                        *hminDRLep;    
    TH1                        *hptvarcone20;
    TH1                        *hptvarcone30;
    TH1                        *htopoetcone20;
    
    TH1                        *hmj34;
    TH1                        *hmax_j_eta;    
    TH1                        *hdRj1;
    TH1                        *hdRj2;
    TH1                        *hminDR;
    TH1                        *hmj1;
    TH1                        *hmj2;
    TH1                        *hminDRmj2;    
    TH1                        *hmin_mj3;
    TH1                        *hmin_mj3_over_mjj;
    TH1                        *hcentrality;      
    TH1                        *hj3Pt;      
    TH1                        *hj3Eta;      
    TH1                        *hj3Jvt;      
    TH1                        *hj3FJvt;      
    TH1                        *hmuDR;      
    TH1                        *hmuEta;
    
    TH1                        *hZMCIDQCD;
    TH1                        *hWMCIDQCD;

    TH1                        *hZMadMCIDQCD;
    TH1                        *hZMad2MCIDQCD;    
    TH1                        *hWMadMCIDQCD;
    TH1                        *hZPowMCIDQCD;    

    TH1			       *hqgTagPerf;
    TH1			       *hqgTagNTrack;
    TH1			       *hqgTagTrackWidth;
    TH1			       *hqgTagSum;
    TH1			       *hQGTaggerSim;
    TH1			       *hQGTaggerSimLog;
    TH1			       *hQGTaggerSimLin;
    TH1			       *hnTrackCut0;
    TH1			       *hnTrackCut1;
    TH1			       *hTrackWidthCut0;
    TH1			       *hTrackWidthCut1;
    TH1			       *hnTrackCutSum;
    TH1			       *hTrackWidthCutSum;
    TH1			       *hnTrackSum;
    TH1			       *hTrackWidthSum;
    TH1			       *hjetNTracks025;
    TH1			       *hjetNTracks125;
    TH1			       *hjetTrackWidth025;
    TH1			       *hjetTrackWidth125;
    TH1			       *hjetNTracks021;
    TH1			       *hjetNTracks121;
    TH1			       *hjetTrackWidth021;
    TH1			       *hjetTrackWidth121;
    TH1			       *hjetNTracks02125;
    TH1			       *hjetNTracks12125;
    TH1			       *hjetTrackWidth02125;
    TH1			       *hjetTrackWidth12125;

    TH2			       *hjetNTrackPT;
    TH2			       *hjetNTrackPTq;
    TH2			       *hjetNTrackPTg;
    TH2			       *hjetNTrackPTpu;

    std::map<Mva::Var,TH1*>    fHistVec;
  };
}

#endif
