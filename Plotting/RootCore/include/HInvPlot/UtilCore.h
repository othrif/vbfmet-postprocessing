#ifndef MSL_UTILCORE_H
#define MSL_UTILCORE_H

// C/C++
#include <iostream>
//#include <stdint.h> // The stdint.h of OSX 10.9 is too complex for CINT to process. Problem will go away in ROOT 6.
#include <string>
#include <vector>

// ROOT
#include "TStopwatch.h"
#include "TVector3.h"
#include "TLorentzVector.h"

// Local
class TDirectory;
class TH1;
class TTree;

namespace Msl
{
  void StringTok(std::vector<std::string>& ls,
		 const std::string& str,
		 const std::string& tok);
  
  // Recursively make ROOT directories
  TDirectory* GetDir(std::string path, TDirectory *dir);
  TDirectory* GetDir(TDirectory *dir, std::string path);

  // Set histogram directory and name (if not empty)
  TH1* SetDir(TH1 *h, TDirectory *dir, const std::string &name = "");

  // Round variable using error as guidance
  std::pair<std::string, std::string> Round2Pair(double value, double error, int nprec=5);

  // Pad string with blanks
  std::string PadStrFront(std::string str, int width);
  std::string PadStrBack (std::string str, int width);

  // Get file size in MB
  double file_size(const std::string &path);

  // Make HTML link
  std::string MakeLink(const std::string &link, const std::string &text);

  std::vector<int>         GetIntVec   (const std::string &list);
  std::vector<std::string> GetStringVec(const std::string &list);

  bool HasBranch(TTree *tree, const std::string &branch, bool debug = false);

  //
  // Hash function (copied from TrigConfHLTData/src/HLTUtils.cxx)
  //
  unsigned long int String2Hash( const std::string &s, const std::string &category = ""); // was uint32_t - see comment next to stdint.h
  
  //
  // Print string to hash map
  //
  void PrintHashMap();

  //
  // Print stopwatch stat
  //
  std::string PrintResetStopWatch(TStopwatch &watch);

  //
  // Helper class for timing events
  //
  class TimerScopeHelper
  {
  public:
    
    explicit TimerScopeHelper(TStopwatch &timer) 
      :fTimer(timer) { fTimer.Start(false); }
    ~TimerScopeHelper() { fTimer.Stop(); }
    
  private:
      
    TStopwatch &fTimer;
  };

  //
  // Compute delta R
  //
  double GetDR(double eta1, double phi1, double eta2, double phi2);
  double GetDPhi(const double &phi1, const double &phi2);
  
  //
  // Sorting algorithm
  //
  struct SortPhysicsObject {

    SortPhysicsObject(const std::string &key = "") :fKey(key) {}

    //template<class M, class T>
    bool operator()(const TLorentzVector &lhs, const TLorentzVector &rhs) const;
    bool operator()(const TVector3       &lhs, const TVector3       &rhs) const;

    public:

    std::string fKey;
  };

}

//
// Templates
//
namespace Hww
{
  template <class T> void Print(const std::vector<T> &tvec, std::ostream &os) {
    if(tvec.empty()) return;
    for(unsigned int i = 0; i < tvec.size(); ++i) os << tvec[i] << " ";
    os << std::endl;
  }
}

#endif
