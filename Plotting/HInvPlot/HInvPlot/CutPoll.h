#ifndef MSL_CUTPOLL_H
#define MSL_CUTPOLL_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : CutPoll
 * @Author : Rustem Ospanov
 *
 * @Brief  :
 * 
 *  Count events with weight by sample for cut-flows
 * 
 **********************************************************************************/

// C/C++
#include <map>

// Local
#include "Event.h"

namespace Msl
{
  class CutPoll
  {
  public:

    CutPoll();
    ~CutPoll() {}
    
    void CountEvent(const Event &event, double weight);
    
    void Print(const std::string &key) const;
    
    std::string Convert2Str(double val, double err) const;

    bool GetCountError(const Mva::Sample     sample, double &val, double &err) const;
    bool GetCountError(const Mva::SampleSet &sample, double &val, double &err) const;

    std::pair<std::string, std::string> GetCountErrorAsPair(const Mva::Sample     sample, const int prec) const;
    std::pair<std::string, std::string> GetCountErrorAsPair(const Mva::SampleSet &sample, const int prec) const;

    void SetName(const std::string &name) { fName   = name; }
    void UseRaw (bool               flag) { fUseRaw = flag; }

    const std::string& GetName() const { return fName; }

  private:

    struct Count 
    {
      Count() :sumn(0), sumw(0.0), sumw2(0.0) {}
      
      unsigned sumn;
      double   sumw;
      double   sumw2;
    };

  private:

    typedef std::map<Mva::Sample, Count> SampleMap;
    
  private:

    bool        fUseRaw;
    std::string fName;

    SampleMap   fSamples;    
  };

  //
  // Inlined functions
  //
  inline void Msl::CutPoll::CountEvent(const Event &event, double weight)
  {
    Count &c = fSamples[event.sample];

    c.sumn  += 1;
    c.sumw  += weight;
    c.sumw2 += weight*weight;
  }
}

#endif
