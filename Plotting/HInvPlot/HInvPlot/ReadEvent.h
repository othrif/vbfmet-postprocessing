#ifndef MSL_READEVENT_H
#define MSL_READEVENT_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : ReadEvent
 * @Author : Doug Schaefer
 *
 * @Brief  :
 * 
 *  Base class for C++ and python algorithms for reading basic events
 * 
 **********************************************************************************/

// C/C++
#include <set>
#include <vector>

// ROOT
#include "TTree.h"
#include "TChain.h"
#include "TH1D.h"

// Local
#include "Event.h"
#include "XSecData.h"
#include "IExecAlg.h"
#include "Registry.h"

class TFile;

namespace Msl
{

  class ReadEvent 
  {
  public:

    ReadEvent();
    virtual ~ReadEvent();

    enum CleaningCuts{ ALL=0, PassGRL, PassTTCVeto, IncompleteEvents, PassLarErr, PassTileErr, PassTileTrip, PassHotSpot, PassBadJet,
		       PassCaloJet, PassBCHTight, PassBCHMedium, PassGoodVtx, PassBadMuon, PassCosmic, PassHFOR, PassMCOverlap, 
		       PassGT2BaseLep, PassEQ2BaseLep, PassTrig, PassEQ2SRLep, PassNSigTau, PassEQ2SRLepNoTrig, CleaningCuts_N };

    // Init is called when TTree (or TChain) is attached
    void    Init(TTree* tree);

    // Main event loop function
    void UpdateCutflow(CleaningCuts cut,double weight);

    // configure
    void Conf(const Registry &reg);

    void AddCommonAlg(IExecAlg *alg);

    void AddNormalAlg(const std::string &key, IExecAlg *alg);

    void AddPreSelAlg(const std::string &key, IExecAlg *alg);

    void PrintAlgs(std::ostream &os = std::cout) const;
    
    void RunConfForAlgs();

    void Read(const std::string &path);
    void Save(TDirectory *dir);

    TH1D* GetgenCutFlow()   { return genCutFlow;   }
    TH1D* GetprocCutFlow0() { return procCutFlow0; }
    TH1D* GetrawCutFlow()   { return rawCutFlow;   }

    const std::string& GetAlgName() const { return fName; }

    std::ostream& log() const;

  public:
    
    typedef std::vector<IExecAlg *> AlgVec;
    typedef std::vector<VarData>    VarVec;

    struct AlgData
    {
      explicit AlgData(const std::string &key);
      
      std::string  alg_key;
      AlgVec       alg_vec;
      IExecAlg    *pre_sel;

      bool operator <(const AlgData &rhs) const { return alg_key  < rhs.alg_key; }
      bool operator==(const AlgData &rhs) const { return alg_key == rhs.alg_key; }
    };

    typedef std::vector<AlgData>                 AlgList;
  private:

    void ReadTree(TTree *rtree);

    void FillEvent(Event &event);
    
    void ProcessAlgs(Event &top_event, Event &alg_event);
    
    void AddVars(const std::string &key, const Registry &reg);

    bool MatchAlg(IExecAlg *alg) const;

  private:
    std::set<unsigned>          evt_map;
    // Properties:
    std::string                 fDir;
    std::string                 fName;
    std::string                 fSystName;
    std::string                 fCutFlowFile;
    std::string                 fRawFlowFile;
    std::string                 fAnalysisName;

    std::vector<std::string>    fTrees;
    std::vector<std::string>    fFiles;
    std::vector<std::string>    fSystNames;
    std::map<int,std::string>   fSampleMap; // mcid to plotting type

    std::vector<unsigned>       fEventIdVec;

    bool                        fDebug;
    bool                        fPrint;    
    bool                        fPrintEvent;    
    bool                        fMCEventCount;    
    int                         fMaxNEvent;

    std::vector<Msl::Mva::Var>  fVarMeV;       //! - do not make CINT dictionary
    VarVec                      fVarVec;       //! - do not make CINT dictionary
    
    // Algorithms:
    AlgVec                      fAlgAll;       //! - all unique algorithms
    AlgVec                      fAlgCommon;    //! - common algs - run on global event first
    AlgVec                      fAlgPreSel;    //! - presel algs - run on local event
    AlgList                     fAlgNormal;    //! - normal algs - run on local event

    unsigned                    fCountEvents;
    // External
    float                       fInputCount;
    float                       fLumi;

    // Input vars
    float fWeight;
    int   fRunNumber;
    int   fCurrRunNumber;
    Mva::Sample fCurrSample;

    std::vector<float> *el_charge;
    std::vector<float> *el_pt;
    std::vector<float> *el_eta;
    std::vector<float> *el_phi;
    std::vector<float> *mu_charge;
    std::vector<float> *mu_pt;
    std::vector<float> *mu_eta;
    std::vector<float> *mu_phi;
    std::vector<float> *jet_timing;
    std::vector<float> *jet_pt;
    std::vector<float> *jet_eta;
    std::vector<float> *jet_phi;
    
    
    // For event counting
    float                       fSumw;
    float                       fNraw;

    TH1D *genCutFlow;
    TH1D *procCutFlow0;
    TH1D *rawCutFlow;

  };

}
#endif