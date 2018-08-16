// C/C++
#include <iomanip>
#include <sstream>

// Local
#include "HInvPlot/UtilCore.h"
#include "HInvPlot/CutPoll.h"

using namespace std;

//-----------------------------------------------------------------------------
Msl::CutPoll::CutPoll():
  fUseRaw(false)
{
}

//-----------------------------------------------------------------------------
void Msl::CutPoll::Print(const std::string &key) const
{
  //
  // Print event count
  //
  cout << "-----------------------------------------------------------" << endl;
  cout << "   " << key << endl;

  for(SampleMap::const_iterator it = fSamples.begin(); it != fSamples.end(); ++it) {
    cout << "   " << key << " " << Mva::Convert2Str(it->first) << ": " 
	 << Convert2Str(it->second.sumw, std::sqrt(it->second.sumw2)) << endl;
  }
}

//-----------------------------------------------------------------------------
std::string Msl::CutPoll::Convert2Str(double val, double err) const
{
  //
  // Convert result to string
  //
  const pair<string, string> res = Msl::Round2Pair(val, err);
  
  //
  // Print nice counts
  //
  stringstream str;
  
  str << std::setw(11) << std::left << res.first
      << " +/- " 
      << std::setw(11) << std::left << res.second;

  return str.str();
}

//-----------------------------------------------------------------------------
bool Msl::CutPoll::GetCountError(const Mva::Sample sample, double &val, double &err) const
{
  //
  // Read counts and error for sample, return false if sample is missing
  //
  GetCountError(Mva::SampleSet(sample), val, err);
  
  return true;
}

//-----------------------------------------------------------------------------
bool Msl::CutPoll::GetCountError(const Mva::SampleSet &sample, double &val, double &err) const
{
  //
  // Read counts and error for sample, return false if sample is missing
  //
  const std::set<Mva::Sample> &samples = sample.GetSamples();

  unsigned sumn  = 0;
  double   sumw  = 0.0;
  double   sumw2 = 0.0;

  for(set<Mva::Sample>::const_iterator sit = samples.begin(); sit != samples.end(); ++sit) {  
    
    const SampleMap::const_iterator cit = fSamples.find(*sit);
    
    if(cit != fSamples.end()) {
      sumn  += cit->second.sumn;
      sumw  += cit->second.sumw;
      sumw2 += cit->second.sumw2;
    }
  }

  if(sumn == 0) {
    return false;
  }

  if(fUseRaw) {
    val = sumn;
    err = std::sqrt(double(sumn));
  }
  else {
    val = sumw;
    err = std::sqrt(sumw2);   
  }

  return true;
}

//-----------------------------------------------------------------------------
std::pair<std::string, std::string> Msl::CutPoll::GetCountErrorAsPair(const Mva::Sample sample, const int prec) const
{
  //
  // Return count and error as 
  //
  return GetCountErrorAsPair(Mva::SampleSet(sample), prec);
}

//-----------------------------------------------------------------------------
std::pair<std::string, std::string> Msl::CutPoll::GetCountErrorAsPair(const Mva::SampleSet &sample, const int prec) const
{
  //
  // Return count and error as 
  //
  double val = 0.0, err = 0.0;
  
  //
  // Special case to select data: do not round off data counts
  //
  static set<Mva::Sample> sdata;
  
  if(sdata.empty()) {
    sdata.insert(Mva::kData);
  }

  if(GetCountError(sample, val, err)) {
    pair<string, string> res = Msl::Round2Pair(val, err, prec);

    if(fUseRaw || sample.GetSamples() == sdata) {
      //
      // HACK: for data keep exact event counts
      //
      stringstream dstr;
      dstr << static_cast<long>(val);
      
      res.first = dstr.str();
      return res;
    }
    else {
      return res;
    }
  }

  return std::pair<std::string, std::string>();
}
