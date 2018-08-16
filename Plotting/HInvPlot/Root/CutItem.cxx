
// C/C++
#include <iomanip>
#include <sstream>

// ROOT
#include "TDirectory.h"

// Local
#include "HInvPlot/Event.h"
#include "HInvPlot/Registry.h"
#include "HInvPlot/CutItem.h"

using namespace std;

namespace Msl
{
  static unsigned cut_name_width = 0;
}

//-----------------------------------------------------------------------------
Msl::CutItem::CutItem():
  fDebug    (false),
  fPassN    (0),
  fFailN    (0),
  fNoneN    (0),
  fTotal    (0)
{
}

//-----------------------------------------------------------------------------
bool Msl::CutItem::InitCut(const Registry &reg)
{
  //
  // Read cut configuration(s)
  //

  if(!reg.Get("CutName", fCutName)) {
    cout << "CutItem::InitCut - missing name" << endl;
    return false;
  }

  //
  // Read self-configuration
  //
  string config, wkey;

  reg.Get("CutConf",  config);
  reg.Get("CutDebug", fDebug);

  //
  // Read and parse weight key - if set
  //
  fWeights = Mva::ReadVars(reg, "CutWeightKey", fCutName);
  
  //
  // Initialize comparison points
  //
  std::vector<string> configs;
  
  const bool isOR  = config.find("||") != string::npos;
  const bool isAND = config.find("&&") != string::npos;

  if(isOR && isAND) {
    log() << "InitCut - invalid configuration string: " << config << endl;
    return false;
  }
  
  if(isOR) { 
    Msl::StringTok(configs, config, "|"); 

    for(unsigned i = 0; i < configs.size(); ++i) {
      AddComparePoint(reg, configs.at(i), true);
    }
  }
  else {
    Msl::StringTok(configs, config, "&"); 

    for(unsigned i = 0; i < configs.size(); ++i) {
      AddComparePoint(reg, configs.at(i), false);
    }    
  }

  //
  // Save name width for pretty printing of many cuts
  //
  cut_name_width = std::max<unsigned>(cut_name_width, fCutName.size());
  
  //
  // Read sub-cuts: AND
  //
  vector<string> olist, alist;

  reg.Get("ListAND", alist);
  reg.Get("ListOR",  olist);

  for(unsigned i = 0; i < alist.size(); ++i) {
    Registry creg;
    
    if(!reg.Get(alist.at(i), creg)) {
      continue;
    }

    fCutA.push_back(CutItem());
    fCutA.back().InitCut(creg);
  }

  for(unsigned i = 0; i < olist.size(); ++i) {
    Registry creg;
    
    if(!reg.Get(olist.at(i), creg)) {
      continue;
    }

    fCutO.push_back(CutItem());
    fCutO.back().InitCut(creg);
  }

  return true;
}

//-----------------------------------------------------------------------------
void Msl::CutItem::AddCut(const CutItem &rhs)
{
  //
  // Increment "this" counts by counts from "rhs"
  //
  fPassN  += rhs.fPassN;
  fFailN  += rhs.fFailN;
  fNoneN  += rhs.fNoneN;
  fTotal  += rhs.fTotal;
}

//-----------------------------------------------------------------------------
void Msl::CutItem::PrintConfig(std::ostream &os, const std::string &pad) const
{  
  os << ConfigAsString(pad);
}

//-----------------------------------------------------------------------------
void Msl::CutItem::PrintCounts(std::ostream &os, const std::string &pad) const
{
  os << CountsAsString(pad);
}

//-----------------------------------------------------------------------------
std::string Msl::CutItem::ConfigAsString(const string &pad) const
{
  //
  // Print config
  //
  stringstream os;

  const string name = Msl::PadStrBack(GetName(), cut_name_width);
  
  if(!fCompA.empty()) {
    os << pad << "CutItem - " << name << ": print " << fCompA.size() << " AND condition(s):" << endl;

    for(ComVec::const_iterator cit = fCompA.begin(); cit != fCompA.end(); ++cit) {
      os << pad << "          " << setw(20) << std::left << cit->var << " "
	 << std::setw(2) << std::left << GetString(cit->compare) << " " << cit->cut << endl;
    }
  }

  if(!fCompO.empty()) {
    os << pad << "CutItem - " << name << ": print " << fCompO.size() << " OR  condition(s):" << endl;

    for(ComVec::const_iterator cit = fCompO.begin(); cit != fCompO.end(); ++cit) {
      os << pad << "          " << setw(20) << std::left << cit->var << " "
	 << std::setw(2) << std::left << GetString(cit->compare) << " " << cit->cut << endl;
    }
  }
  
  if(!fCutA.empty()) {
    os << pad << "CutItem - " << name << ": print  " << fCutA.size() << " AND cuts(s):" << endl;

    for(CutVec::const_iterator cit = fCutA.begin(); cit != fCutA.end(); ++cit) {
      os << cit->ConfigAsString(pad+"   ");
    }
  }

  
  if(!fCutO.empty()) {
    os << pad << "CutItem - " << name << ": print  " << fCutO.size() << " OR  cuts(s):" << endl;

    for(CutVec::const_iterator cit = fCutO.begin(); cit != fCutO.end(); ++cit) {
      os << cit->ConfigAsString(pad+"   ");
    }
  }

  if(!fWeights.empty()) {
    os << pad << "Number of weight variable(s): " << fWeights.size() << endl;

    for(unsigned i = 0; i < fWeights.size(); ++i) {
      os << pad << "    " << Mva::AsStr(fWeights.at(i)) << endl;
    }
  }

  return os.str();
}

//-----------------------------------------------------------------------------
std::string Msl::CutItem::CountsAsString(const string &pad) const
{
  //
  // Print counts
  //
  stringstream os;

  const string name = Msl::PadStrBack(GetName()+": ", cut_name_width+2);
  os << pad << "CutItem - " << name;
  
  os << " npassN=" << setw(8) << right << GetPassN() 
     << " nfailN=" << setw(8) << right << GetFailN()
     << " ntotal=" << setw(8) << right << GetTotal()
     << endl;

  
  if(!fCutA.empty()) {
    os << pad << "CutItem - " << name << ": print  " << fCutA.size() << " AND condition(s):" << endl;

    for(CutVec::const_iterator cit = fCutA.begin(); cit != fCutA.end(); ++cit) {
      os << cit->CountsAsString("   ");
    }
  }

  
  if(!fCutO.empty()) {
    os << pad << "CutItem - " << name << ": print  " << fCutO.size() << " OR  condition(s):" << endl;

    for(CutVec::const_iterator cit = fCutO.begin(); cit != fCutO.end(); ++cit) {
      os << cit->CountsAsString("   ");
    }
  }
  
  return os.str();
}

//-----------------------------------------------------------------------------
bool Msl::CutItem::AddComparePoint(const Registry &, const std::string &config, bool isOR)
{
  //
  // Add comparison point if exists
  //
  ComparePoint p;
  
  for(unsigned i = 0; i < GetAllComp().size(); ++i) {
    p.compare = GetAllComp().at(i);
    p.opr     = GetString(p.compare);

    //
    // Try to extract variable name and cut value
    //
    const size_t ipos = config.find(p.opr);
    
    if(ipos == string::npos) {
      if(fDebug) {
	log() << "AddComparePoint - " << p.opr << ": failed to parse config: " << config << endl;
      }
      continue;
    }

    //
    // Remove white spaces
    //
    const string part1 = StripSpaces(config.substr(0, ipos));
    const string part2 = StripSpaces(config.substr(ipos+p.opr.size()));

    //
    // Try to match variable name to enum
    //
    p.var = part1;
    p.key = Mva::Convert2Var(p.var);
    
    if(p.key == 0) {
      log() << "AddComparePoint - failed to match var: " << config << endl;
      return false;
    }
    
    //
    // Extact cut value
    //
    stringstream str;
    
    str << part2;
    str >> p.cut;
    
    if(str.fail()) {
      log() << "AddComparePoint - failed to extract value: " << config << endl;
      return false;
    }

    break;
  }

  if(p.key == 0) {
    log() << "AddComparePoint - failed to extract operator: " << config << endl;
    return false;
  }

  if(fDebug) {
    log() << "AddComparePoint - new comparison point: \"" << config << "\"" << endl;
  }

  if(isOR) {
    fCompO.push_back(p);
  }
  else {
    fCompA.push_back(p);
  }

  return true;
}

//-----------------------------------------------------------------------------
std::string Msl::CutItem::GetString(Compare comp, bool print_nice)
{
  if(print_nice) {

    switch(comp)
      {
      case Less:           return "<";
      case LessOrEqual:    return "<=";
      case Greater:        return ">";
      case GreaterOrEqual: return ">=";
      case Equal:          return "==";
      default  :           break;
      }
  }
  else {
    switch(comp)
      {
      case Less:           return "&lt;";
      case LessOrEqual:    return "&lt;=";
      case Greater:        return "&gt;";
      case GreaterOrEqual: return "&gt;=";
      case Equal:          return "&eq;";
      default  :           break;
      }
  }

  return "None";
}

//-----------------------------------------------------------------------------
Msl::CutItem::Compare Msl::CutItem::GetCompare(const std::string &val) const
{
  //
  // Get comparison operator from string
  //
  if     (val == GetString(Less))           return Less;
  else if(val == GetString(LessOrEqual))    return LessOrEqual;
  else if(val == GetString(Greater))        return Greater;
  else if(val == GetString(GreaterOrEqual)) return GreaterOrEqual;
  else if(val == GetString(Equal))          return Equal;

  return None;
}

//-----------------------------------------------------------------------------
std::ostream& Msl::CutItem::log() const
{
  std::cout << GetName() << "::";
  return std::cout;
}

//-----------------------------------------------------------------------------
const std::vector<Msl::CutItem::Compare>& Msl::CutItem::GetAllComp()
{
  static vector<Compare> cvec;

  if(cvec.empty()) {
    //
    // Fill vector of all operators - order matters!
    //
    cvec.push_back(LessOrEqual);
    cvec.push_back(Less);
    cvec.push_back(GreaterOrEqual);
    cvec.push_back(Greater);
    cvec.push_back(Equal);
  }

  return cvec;
}

//-----------------------------------------------------------------------------
std::string Msl::CutItem::StripSpaces(const std::string &s) const
{
  //
  // Strip leading and trailing whitespaces
  //
  if(s.empty()) {
    log() << "StripSpaces - empty string" << endl;
    return s;
  }

  //
  // Split string in separate parts separated by whitespace
  //
  std::vector<string> parts;
  Msl::StringTok(parts, s, " ");

  if(parts.size() != 1) {
    log() << "StripSpaces - invalid input string: \"" << s << "\"" << endl;
    return s;    
  }

  return parts.front();
}
