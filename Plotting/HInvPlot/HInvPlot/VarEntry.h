#ifndef MSL_VARENTRY_H
#define MSL_VARENTRY_H

//
// One double variable with integer key
//

// C/C++
//#include <stdint.h> // The stdint.h of OSX 10.9 is too complex for CINT to process. Problem will go away in ROOT 6.
#include <iostream>
#include <vector> 

namespace Msl
{
  class VarEntry
  {
  public:
    
    VarEntry();
    VarEntry(unsigned key, double value);
    ~VarEntry() {}
    
    unsigned getKey () const { return fKey; }
    unsigned GetKey () const { return fKey; }

    double   getVar () const { return fData; }
    double   GetVar () const { return fData; }
    double   getData() const { return fData; }
    double   GetData() const { return fData; }
    
    void Print(std::ostream &os = std::cout) const;
  
  private:
    
    unsigned long int fKey;     // variable key // was uint32_t - see comment next to stdint.h
    double   fData;    // variable value
  };
 
  //
  // Vector for non-permanent variables
  //
  typedef std::vector<Msl::VarEntry> VarEntryVec;
  
  //
  // Inlined comparison operators
  //
  inline bool operator==(const VarEntry &lhs, const VarEntry &rhs) { 
    return lhs.getKey() == rhs.getKey();
  }
  inline bool operator <(const VarEntry &lhs, const VarEntry &rhs) { 
    return lhs.getKey() < rhs.getKey();
  }

  inline bool operator==(const VarEntry &var, unsigned key) { return var.getKey() == key; }
  inline bool operator==(unsigned key, const VarEntry &var) { return var.getKey() == key; }

  inline bool operator<(const VarEntry &var, unsigned key) { return var.getKey() < key; }
  inline bool operator<(unsigned key, const VarEntry &var) { return key < var.getKey(); }
}

#endif
