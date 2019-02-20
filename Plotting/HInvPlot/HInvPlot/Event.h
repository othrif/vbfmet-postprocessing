#ifndef MSL_EVENT_H
#define MSL_EVENT_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : Event
 * @Author : Doug Schaefer
 *
 * @Brief  :
 * 
 *  Main event class - stores all event variables
 **********************************************************************************/

// C/C++
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

// ROOT
#include "Rtypes.h"
#include "TVector3.h"
#include "TLorentzVector.h"

// Local
#include "Sample.h"

// Variables
#include "RecParticle.h"
#include "VarEvent.h"
#include "VarHolder.h"

namespace Msl
{
  namespace Mva
  {
    enum Chan {
      aa = 0, // any lepton flavor - no channel cut
      ee = 1,
      eu = 2,
      uu = 3,
      ll = 5
    };

    std::string       AsStr (Chan c);
    Chan        Convert2Chan(const std::string &c);

    enum Flavor {
      FlavorUnknown = 0, // any lepton flavor - no channel cut
      e             = 1,
      u             = 2
    };

    std::string       AsStr (Flavor c);
    Flavor            Convert2Flavor(const std::string &c);

  }

  class Event: public VarHolder //, public SusyNtTools
  {
  public:

    enum Bits {
      NoBit = 0
    };

  public:

    Event();
    virtual ~Event() {}

    void AddWeight(double w);
    void AddWeight(float w);    
    void SetWeight(double w);
    
    double GetWeight() const;
      
    void SortLep           ();
    void SortJet           (const bool force_sort);
    void Clear             ();     
    void Print             () const;

    void AddBit  (Bits     b)       { bits |= b; }
    bool CheckBit(unsigned long int b) const { return (bits & b) == b && b != 0; } // was uint32_t - see comment next to stdint.h

    void Convert2GeV(const std::vector<Msl::Mva::Var> &vars);
    //void Convert2MeV(const std::vector<Msl::Mva::Var> &vars);

    void SetVars();

    double GetMll   () const;
    void GetX1X2(const TLorentzVector &lep1,
                 const TLorentzVector &lep2,
                 const std::pair<float,float> &met,
                 double& output_x1,
                 double& output_x2);

  public:

    //
    // Weights required to calculate event weight
    //
    bool        isMC;
    bool        fDebug;

    Mva::Sample sample;

    unsigned long int    bits; // was uint32_t - see comment next to stdint.h

    unsigned long int    RunNumber;
    unsigned long int    RandomRunNumber;    
    unsigned long int    EventNumber;

    double               totalWeight;

    ParticleVec          muons;
    ParticleVec          electrons;
    ParticleVec          taus;    
    ParticleVec          jets;
    ParticleVec          truth_jets;
    ParticleVec          truth_taus;
    ParticleVec          truth_el;
    ParticleVec          truth_mu;    
    ParticleVec          baseel;
    ParticleVec          basemu;
    ParticleVec          photons;
    TLorentzVector       met;
    TLorentzVector       met_nolep;
  };
}

  // 
  // Inlined Event functions: scalar operations
  //
  inline void Msl::Event::AddWeight(double w) {
    totalWeight *= w;
  }
  inline void Msl::Event::AddWeight(float w) {
    totalWeight *= w;
  }
  inline void Msl::Event::SetWeight(double w) {
    totalWeight = w;
  }
  inline double Msl::Event::GetWeight() const {
    return totalWeight;
  }
  inline double Msl::Event::GetMll() const {
    //return (GetLVLep0()+GetLVLep1()).M();
    return GetVar(Mva::mll);
  }
#endif
