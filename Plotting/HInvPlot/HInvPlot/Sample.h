#ifndef MSL_SAMPLE_H
#define MSL_SAMPLE_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : Sample
 * @Author : Rustem Ospanov, Doug Schaefer
 *
 * @Brief  :
 * 
 *  Enum for dataset keys (samples) and helper class for a set of samples
 * 
 **********************************************************************************/

// C/C++
#include <set>
#include <string>

// Local
#include "Registry.h"

namespace Msl
{
  namespace Mva 
  {
    //
    // Enums for unique (non-overlapping) dataset samples
    //
    enum Sample {
      kNone,
      kData,
      kHggf,
      kHvbf,
      kHvbf500,      
      kHvbf1k,      
      kHvbf3k,      
      kVbfg,
      kHvh,
      kWewk,
      kWqcd,
      kZewk,
      kZqcd,
      kWhww,
      kTthw,
      kTth,
      kHtau,
      kHwww,
      kHzww,
      kggww,
      kqqww,
      kewww,
      kWZZZ,
      kZZ,
      kWZ,
      kWgam,
      kWgas,
      ktop2,
      ktop1,
      kZjet,
      kZjee,
      kZjmm,
      kZjtt,
      kZldy,
      kZlee,
      kZlmm,
      kZltt,
      kWjet,
      kWjdt,
      kWjdtm,
      kWjdte,
      kQFlip,
      kQCD,
      kQCD_MC,
      kZjhf,
      kZgam,
      kZgamEWK,
      kWgamEWK,
      kZgas,
      kWjhf,
      kZvbf,
      kZvbe,      
      kZvbm,
      kZvbt,
      kVbfZ, 
      kVbfZll, 
      kVbfZtt, 
      kVbfZl,      
      kVbfZh,
      kWDPI,
      kttv,
      kttg,
      kvgg,
      kpho,
      kphoAlt,
      kvvv,
      kvv,
      kvvjj,
      kggvv,
      kJPsi,
      kUpsl,
      kZqcdPow,
      kZqcdMad,
      kWqcdMad
    };

    std::string Convert2Str   (Sample s);
    std::string Convert2Std   (Sample s);
    Sample      Convert2Sample(const std::string &s);

    bool IsWjdt(Sample sample);
    bool IsQCD (Sample sample);
    bool IsZjet(Sample sample);
    bool IsZldy(Sample sample);
    bool IsZvbf(Sample sample);
    
    const std::vector<Msl::Mva::Sample>& GetAllSamples();

    //
    // Helper class for set of samples
    //
    class SampleSet 
    {
    public:
      explicit SampleSet(Mva::Sample sample);
      SampleSet() {}
      ~SampleSet() {}
      
      void FillSample(const Registry &reg, const std::string &key);
      void FillSample(const std::vector<std::string> &samples);

      bool MatchSample(Mva::Sample sample) const { return fSamples.count(sample); }
      
      unsigned                     GetSize   () const { return fSamples.size(); }
      const std::string&           GetName   () const { return fName;           }
      const std::set<Mva::Sample>& GetSamples() const { return fSamples;        }

      void Print(std::ostream &os=std::cout, const std::string &pad = "") const;

    private:

      std::string           fName;
      std::set<Mva::Sample> fSamples;
    };

    std::string Convert2Tex(const SampleSet &s);

    std::vector<Msl::Mva::SampleSet> ReadSets(const Registry &reg, 
					      const std::string &key,
					      const std::string &caller="ReadSets");
    
    void PrintSets(const std::string &key, 
		   const std::vector<Msl::Mva::SampleSet> &sets,
		   std::ostream &os=std::cout);

    //
    // Global comparison operators
    //
    inline bool operator==(const SampleSet &lhs, const SampleSet &rhs)
    {
      return lhs.GetSamples() == rhs.GetSamples();
    }
    inline bool operator<(const SampleSet &lhs, const SampleSet &rhs)
    {
      return lhs.GetSamples() < rhs.GetSamples();
    }
  }
}

#endif
