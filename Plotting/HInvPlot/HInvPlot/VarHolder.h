#ifndef MSL_VARHOLDER_H
#define MSL_VARHOLDER_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : VarHolder
 * @Author : Rustem Ospanov
 *
 * @Brief  :
 * 
 *  VarHolder stores variables as int, double pairs
 *  
 **********************************************************************************/

// C/C++
#include <algorithm>
#include <functional>
#include <iostream>

// Local
#include "VarEvent.h"
#include "VarEntry.h"

namespace Msl
{
  class VarHolder 
  {
  public:

    VarHolder() {}
    virtual ~VarHolder() {}
    
    virtual std::string GetObjectType() const { return "VarHolder"; }

    bool   RepVar(unsigned key, double  value);
    bool   AddVar(unsigned key, double  value);
    bool   DelVar(unsigned key);

    bool   GetVar(unsigned key, double &value) const;
    double GetVar(unsigned key) const;

    bool   HasKey(unsigned key) const;
    bool   HasVar(unsigned key) const;

    unsigned GetSize() const { return fVars.size(); }

          VarEntryVec& GetVars()       { return fVars; }
    const VarEntryVec& GetVars() const { return fVars; }
    
    std::vector<double> GetVars(const std::vector<Msl::Mva::Var> &vars) const;

    void ClearVars();

    void Print(std::ostream &os = std::cout) const;

  private:

    VarEntryVec fVars;
  };
  
  //
  // Helper struct for sorting by variable
  //
  struct VarComp: public std::binary_function<VarHolder, VarHolder, bool> 
  {
    explicit VarComp(const Mva::Var var, bool reverse=false) :fVar(var), fRev(reverse) {}

    bool operator()(const VarHolder &lhs, const VarHolder &rhs) const;

    private:

    Mva::Var fVar;
    bool     fRev;
  };


  //
  // Inlined functions
  //
  inline bool VarHolder::RepVar(const unsigned key, const double value) {

    bool pass = DelVar(key);
    pass = (AddVar(key,value) || pass);

    return pass;
  }

  inline bool VarHolder::AddVar(const unsigned key, const double value) {

    VarEntryVec::iterator vit = std::lower_bound(fVars.begin(), fVars.end(), key);
    
    if(vit == fVars.end() || vit->GetKey() != key) {
      fVars.insert(vit, VarEntry(key, value));
      return true;
    }
    
    std::cout << GetObjectType() << "::AddVar(" << key << ", " << value << ") - key already exists " << Mva::Convert2Str(static_cast<Mva::Var>(key)) << std::endl;

    return false;
  }

  inline bool VarHolder::DelVar(const unsigned key) {

    VarEntryVec::iterator vit = std::lower_bound(fVars.begin(), fVars.end(), key);

    if(vit != fVars.end() && vit->GetKey() == key) {
      fVars.erase(vit);
      return true;
    }

    return false;
  }

  inline bool VarHolder::HasKey(unsigned key) const {
    const VarEntryVec::const_iterator vit = std::lower_bound(fVars.begin(), fVars.end(), key);

    return (vit != fVars.end() && vit->GetKey() == key);
  }

  inline bool VarHolder::HasVar(unsigned key) const {
    return HasKey(key);
  }
    
  inline bool VarHolder::GetVar(unsigned key, double &value) const {
    //
    // Read variable
    //
    const VarEntryVec::const_iterator ivar = std::lower_bound(fVars.begin(), fVars.end(), key);

    if(ivar != fVars.end() && ivar->GetKey() == key) {
      value = ivar->getData();
      return true;
    }
    
    return false;
  }

  inline double VarHolder::GetVar(const unsigned key) const {
    //
    // Find and return, if exists, value stored at key
    //
    double val = -1.0e9;
    GetVar(key, val);    
    return val;
  }

  inline void VarHolder::ClearVars() {
    fVars.clear();
  }
}

#endif
