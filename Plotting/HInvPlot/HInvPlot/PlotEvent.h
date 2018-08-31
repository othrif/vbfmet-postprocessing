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
    TH1                        *hMu;
    std::map<Mva::Var,TH1*>    fHistVec;
  };
}

#endif