#ifndef MSL_PASSEVENT_H
#define MSL_PASSEVENT_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : PassEvent
 * @Author : Rustem Ospanov
 *
 * @Brief  :
 * 
 *  Algorithm for selecting events
 * 
 **********************************************************************************/

// C/C++
#include <iostream>
#include <map>

// Local
#include "IExecAlg.h"
#include "CutItem.h"
#include "CutPoll.h"
#include "Registry.h"

class TH1;

namespace Msl
{
  class PassEvent: public virtual IExecAlg
  {
  public:

    PassEvent();
    virtual ~PassEvent();
    
    void DoConf(const Registry &reg);       

    bool DoExec(Event &event);

    void DoSave(TDirectory *dir);

  public:

    struct Cut 
    {
      CutItem icut;
      CutPoll poll;
    };

    struct Pad
    {
      Pad() :valw(0), errw(0), hdrw(0) {}
      
      unsigned GetCellWidth(const std::string &pm) const
      {
	return std::max<unsigned>(hdrw, valw+errw+pm.size());
      }

      unsigned valw;
      unsigned errw;
      unsigned hdrw;
    };

    typedef std::vector<Msl::PassEvent::Cut> CutVec;
    typedef std::vector<Msl::Mva::SampleSet> SetVec;
    typedef std::vector<Msl::CutPoll>        PollVec;
    typedef std::vector<Msl::Event>          EventVec;
    typedef std::map<std::string, Pad>       PadMap;

  private:

    void ProcessJets(Event &event);
    void ProcessVeto(Event &event);

    void AddCut(const std::string &key, const Registry &reg);
    
    TH1* FillCounts(const std::string &pref, const Mva::SampleSet &sample);
    
    void PrintCounts(std::ostream &os = std::cout, 
		     const std::string &pad = "", 
		     const bool writeTex=false,
		     const bool writeRaw=false);

    void ComputePads(const bool writeTex=false);

    Pad FillPad(const Mva::SampleSet &s) const;

    void PrintEvents(const Mva::Sample &sample, std::ostream &os) const;

  private:

    // Properties:
    bool                        fPassAll;
    bool                        fPrintRaw;
    bool                        fPrintEvents;
    int                         fPrecision;

    // Variables:
    CutVec                      fCuts;
    SetVec                      fSets;
    PadMap                      fPads;
    EventVec                    fEvents;

    PollVec                     fPollAll;
    CutPoll                     fPollInput;
  };

  //
  // Helper class to store all cut-flows into a single tex file
  //
  class CutFlowMan
  {
  public:
    
    static CutFlowMan& Instance();
    
    void AddCutFlow(const std::string &name, const std::string &cutflow) { fCutFlows[name] = cutflow; }
    void AddRawFlow(const std::string &name, const std::string &rawflow) { fRawFlows[name] = rawflow; }
    
    void WriteCutFlows(const std::string &path) const;
    void WriteRawFlows(const std::string &path) const;

    void SetWriteAll(const bool s) { fWriteAll=s; }

  private:     
    
    CutFlowMan() : fWriteAll(false) {}
    ~CutFlowMan() {}
    
    CutFlowMan(const CutFlowMan &);
    const CutFlowMan& operator=(const CutFlowMan &);
    
    void WriteFlows     (const std::string &path, const std::map<std::string, std::string> &flows) const;
    void WriteFlowsIndiv(const std::string &path, const std::map<std::string, std::string> &flows) const;
    
    std::string ReplaceUnderscore(std::string str) const;

  private:
    
    std::map<std::string, std::string> fCutFlows;
    std::map<std::string, std::string> fRawFlows;
    bool  fWriteAll;
  };
}

#endif
