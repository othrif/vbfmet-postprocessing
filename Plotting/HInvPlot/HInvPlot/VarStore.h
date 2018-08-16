#ifndef MSL_VARSTORE_H
#define MSL_VARSTORE_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : VarStore
 * @Author : Rustem Ospanov
 *
 * @Brief  :
 * 
 *  Light weight class to hold:
 *     - variables for MVA
 *     - event weight, MC sample
 *  Should really be called simpleEvent
 **********************************************************************************/

// Local
#include "Event.h"
#include "VarHolder.h"

namespace Msl
{
  class VarStore: public VarHolder
  {
  public:

    enum Bits {
      NoBit  = 0,
      kTrain = 0x1,
      kTest  = 0x2,
      kSig   = 0x4,
      kBkg   = 0x8
    };

  public:

    VarStore();
    VarStore(const Msl::Event &event, const std::vector<Msl::Mva::Var> &vars);
    virtual ~VarStore() {}

    void Clear();

    void SetWeight(double w) { fWeight  = w; }
    void AddWeight(double w) { fWeight *= w; }
    void AddBit   (Bits   b) { fBits   |= b; }

    bool CheckBit(unsigned long int b) const { return (fBits & b) == b && b != 0; } // was uint32_t - see comment next to stdint.h
    
    void FillStore(const Msl::Event &event, const std::vector<Msl::Mva::Var> &vars);

    double   GetWeight() const { return fWeight; }
    unsigned long int GetBits  () const { return fBits;   } // was uint32_t - see comment next to stdint.h

    Msl::Mva::Sample GetSample() const { return fSample; }
    
  public:

    UInt_t       RunNumber;
    UInt_t       EventNumber;

  private:
    
    double       fWeight;
    unsigned long int     fBits; // was uint32_t - see comment next to stdint.h

    Mva::Sample  fSample; //!
  };
}

#endif
