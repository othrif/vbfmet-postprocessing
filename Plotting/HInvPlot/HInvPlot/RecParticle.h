#ifndef MSL_RECPARTICLE_H
#define MSL_RECPARTICLE_H

//
// RecParticle - one reconstructed jet
//

// C/C++
#include <iostream>
#include <vector>

// ROOT
#include "Rtypes.h"
#include "TVector3.h"
#include "TLorentzVector.h"

// Local
#include "VarHolder.h"

namespace Msl
{
  class RecParticle: public VarHolder
  {
  public:

    enum Bits {
      NoBit  = 0,
      kBJet  = 0x1,
      kHS    = 0x2,
      kPU    = 0x4
    };

  public:

    RecParticle();
    virtual ~RecParticle() {}

    void Clear();     
    void Print() const;

    bool GetBit(Bits bit_ ) const { return bits  & bit_;  }
    void AddBit(Bits bit_ )       {        bits |= bit_;  }

    TVector3 GetVec              ();
    TVector3 GetVec              () const;
    TLorentzVector GetLVec       ();
    TLorentzVector GetLVec       () const;    

  public:

    Float_t    eta;
    Float_t    phi;
    Float_t    pt;
    Float_t    m;

    TVector3         v_jet;
    TLorentzVector   vl_jet;

    uint32_t   bits;
  };

  typedef std::vector<RecParticle> ParticleVec;

  //
  // Inlined RecJet functions
  //
  inline TVector3 Msl::RecParticle::GetVec() { 
    v_jet.SetPtEtaPhi(pt, eta, phi);
    return v_jet;
  }
  inline TVector3 Msl::RecParticle::GetVec() const { 
    TVector3 jet;
    jet.SetPtEtaPhi(pt, eta, phi);
    return jet;
  }
  inline TLorentzVector Msl::RecParticle::GetLVec() { 
    vl_jet.SetPtEtaPhiM(pt, eta, phi, m);
    return vl_jet;
  }
  inline TLorentzVector Msl::RecParticle::GetLVec() const { 
    TLorentzVector jet;
    jet.SetPtEtaPhiM(pt, eta, phi, m);
    return jet;
  }  
}

#endif
