#ifndef MSL_XSecData_H
#define MSL_XSecData_H

/**********************************************************************************
 * @Package: MonojetSoftLepton
 * @Class  : XSecData
 * @Author : Doug Schaefer
 *
 * @Brief  :
 * 
 *  Class to read and hold XS info
 *     - ****NOTE: class is only used to apply the appropriate background categorization!!!!*******
 *     - XS is normalized by the SUSY CODE!!!!
 **********************************************************************************/

// C/C++
#include <set>
#include <vector>

// ROOT
#include "TTree.h"

// Local
#include "Event.h"
#include "IExecAlg.h"
#include "Registry.h"

class TFile;

namespace Msl
{
  namespace Ntuple
  {
    enum Type {
      kNoType,
      kCommonData,
      kCommonMC
    };

    enum Version {
      kNoVersion,
      kCommonV1
      
    };

    std::string AsStr(Type t);
  }

  //
  // Helper class to read xsec values via registry (processed in python)
  //
  struct XSecData
  {
    XSecData();
    explicit XSecData(const Registry &reg);
    
    void   Print () const;
    double Weight() const;

    int          run;
    double       xsec;
    double       kfactor;
    double       feff;
    int          hmass;
    double       weight;

    std::string  process;
    std::string  data_type;
    std::string  key;

    double       escale;
    double       inputw;
    double       inlumi;
    unsigned     eventn;
    unsigned     evente;
    double       eventw;

    Mva::Sample  sample;
  };

  //
  // Class to help with computing event normalization for specific ntuple types
  //
  struct FileData
  {
    FileData();

    std::string   opt;
    std::string   name;
    std::string   path;
    std::string   run;
    std::string   mcchan;

    TDirectory   *dir;
    
    Ntuple::Type     ntuple; 
    Ntuple::Version  version;
  };

  //
  // Helper class to read float/double tree branch
  //
  struct VarData 
  {
    enum Type {
      kNone,
      kFloat,
      kDouble,
      kInt,
      kUInt,
      kBool
    };

    VarData();
    ~VarData() {}
    
    void Clear();

    void Print() const;
    
    double GetVal() const;
    
    bool SetVarBranch(TTree *tree);

    Type GetType(const std::string &t) const;

    bool operator<(const VarData &rhs) const { return key < rhs.key; }

    std::string  key;
    Mva::Var     var;
    Type         type;

    Double_t     vald;
    Float_t      valf;
    Int_t        vali;
    UInt_t       valu;
    Bool_t       valb;
  };

  //-----------------------------------------------------------------------------
  // Helper functions for reading trees
  //
  template<class T> TBranch* SetBranch(TTree *tree, const std::string &branch, T &var)
  {
    if(!tree) {
      return 0;
    }
    
    TBranch *b = 0;

    if(tree->GetBranch(branch.c_str())) {
      tree->SetBranchStatus (branch.c_str(),    1);
      tree->SetBranchAddress(branch.c_str(), &var, &b); 
    }

    return b;
  }

  template<class T> TBranch* SetBranch(TTree *tree, const std::string &branch, T *&var)
  {
    if(!tree) {
      return 0;
    }

    TBranch *b = 0;
    
    if(tree->GetBranch(branch.c_str())) {
      tree->SetBranchStatus (branch.c_str(),    1);
      tree->SetBranchAddress(branch.c_str(), &var, &b); 
    }

    return b;
  }
}
#endif
