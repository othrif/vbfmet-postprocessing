#ifndef MSL_CUTITEM_H
#define MSL_CUTITEM_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : CutItem
 * @Author : Doug Schaefer
 *
 * @Brief  :
 * 
 *  CutItem is a helper class:
 *    - read cut definitions from Registry
 *    - check if variable passes cut
 *    - count total and passed events
 * 
 **********************************************************************************/

// C/C++
#include <iostream>
#include <string>

// Local
#include "Event.h"

namespace Msl
{
  class Registry;

  //
  // Enum for event selection
  //
  namespace Select
  {
    enum State { Fail=0, Pass=1, None=2 };
  }

  class CutItem
  {
  public:

    CutItem();
    ~CutItem() {}

    bool InitCut(const Registry &reg);

    void AddCut(const CutItem &rhs);

    Select::State PassCut(Event &event);

    const std::string& GetName() const { return fCutName; }
    
    unsigned GetFailN() const { return fFailN; }
    unsigned GetPassN() const { return fPassN; }
    unsigned GetNoneN() const { return fNoneN; }
    unsigned GetTotal() const { return fTotal; }

    void PrintCounts(std::ostream &os = std::cout, const std::string &pad = "") const;
    void PrintConfig(std::ostream &os = std::cout, const std::string &pad = "") const;

    std::string ConfigAsString(const std::string &pad) const;
    std::string CountsAsString(const std::string &pad) const;
    
    const std::vector<Msl::Mva::Var>& GetWeightVars() const { return fWeights; }

  public:
   
    enum Compare { None, Less, LessOrEqual, Greater, GreaterOrEqual, Equal };

    struct ComparePoint
    {
    ComparePoint() :compare(None), cut(0.0), key(0) {}

      Select::State Pass(const VarHolder &vars) const 
      {
	double val = 0.0;

	if(!vars.GetVar(key, val)) {
	  return Select::None;
	}
	
	if     (compare == Less            &&   val < cut  )                 return Select::Pass;
	else if(compare == LessOrEqual     && !(val > cut) )                 return Select::Pass;
	else if(compare == Greater         &&   val > cut  )                 return Select::Pass;
	else if(compare == GreaterOrEqual  && !(val < cut) )                 return Select::Pass;
	else if(compare == Equal           && !(val < cut) && !(val > cut) ) return Select::Pass;

	return Select::Fail;
      }

      Compare     compare;
      double      cut;
      unsigned long int    key; // was uint32_t - see comment next to stdint.h

      std::string opr;
      std::string var;
    };

    typedef std::vector<ComparePoint>  ComVec;
    typedef std::vector<CutItem>       CutVec;
    typedef std::vector<Msl::Mva::Var> VarVec;
  
    static std::string GetString(Compare comp, bool print_nice=true);

    static const std::vector<Msl::CutItem::Compare>& GetAllComp();

  private:

    Select::State Count(Select::State pass);

    std::ostream& log() const;

    bool AddComparePoint(const Registry &reg, const std::string &comp, bool isOR);
    
    Compare GetCompare(const std::string &val) const;
    
    std::string StripSpaces(const std::string &s) const;

  private:  
    
    //
    // Configuration
    //
    std::string  fCutName;

    bool         fDebug;
    VarVec       fWeights;

    ComVec       fCompA;
    ComVec       fCompO;
    CutVec       fCutA;
    CutVec       fCutO;

    //
    // Counters
    // 
    unsigned long int     fPassN; // was uint32_t - see comment next to stdint.h
    unsigned long int     fFailN; // was uint32_t - see comment next to stdint.h
    unsigned long int     fNoneN; // was uint32_t - see comment next to stdint.h
    unsigned long int     fTotal; // was uint32_t - see comment next to stdint.h
  };
  
  //
  // Inlined member functions
  //
  inline Select::State CutItem::Count(Select::State pass)
  {
    //
    // Count events
    //
    switch(pass) {      
    case Select::Pass: fPassN++;
    case Select::Fail: fFailN++;
    case Select::None: fNoneN++;
    default: break;
    }

    fTotal++;
    return pass;
  }

  inline Select::State CutItem::PassCut(Event &event) 
  {
    //
    // Check if value passes cut
    //
    Select::State pass = Select::None;
    
    if(!fCompA.empty()) {
      pass = Select::Pass;

      for(ComVec::const_iterator cit = fCompA.begin(); cit != fCompA.end(); ++cit) {
	if(cit->Pass(event) != Select::Pass) {
	  pass = Select::Fail;
	  break;
	}
      }
    }
    else if(!fCompO.empty()) {
      pass = Select::Fail;

      for(ComVec::const_iterator cit = fCompO.begin(); cit != fCompO.end(); ++cit) {
	if(cit->Pass(event) == Select::Pass) {
	  pass = Select::Pass;
	  break;
	}
      }
    }

    if(!fCutA.empty() && pass != Select::Fail) {
      pass = Select::Pass;

      for(CutVec::iterator cit = fCutA.begin(); cit != fCutA.end(); ++cit) {	
	if(cit->PassCut(event) != Select::Pass) {
	  pass = Select::Fail;
	  break;
	}
      }
    }

    if(!fCutO.empty() && pass != Select::Fail) {
      pass = Select::Fail;

      for(CutVec::iterator cit = fCutO.begin(); cit != fCutO.end(); ++cit) {	
	if(cit->PassCut(event) == Select::Pass) {
	  pass = Select::Pass;
	  break;
	}
      }
    }

    if(!fWeights.empty() && pass == Select::Pass) {
      //
      // Scale event weight for passed events
      //
      for(unsigned i = 0; i < fWeights.size(); ++i) {
	double weight = 0.0;
	
	if(event.GetVar(fWeights.at(i), weight)) {
	  event.AddWeight(weight);
	}
	else {
	  if(fDebug) {
	    log() << "PassCut - missing weight key: " << Mva::AsStr(fWeights.at(i)) << std::endl;
	  }
	}
      }
    }

    return pass;
  }
}

#endif
