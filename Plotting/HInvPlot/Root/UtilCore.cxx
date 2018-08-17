
// C/C++
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <sstream>
#include <sys/stat.h>
//#include <stdint.h>
#include <stdexcept>

// ROOT
#include "TDirectory.h"
#include "TH1.h"
#include "TObjArray.h"
#include "TTree.h"
#include "TStopwatch.h"
#include "TVector2.h"
#include "TLorentzVector.h"

// Local
#include "HInvPlot/UtilCore.h"

using namespace std;

//-----------------------------------------------------------------------------
void Msl::StringTok(std::vector<std::string>& ls,
		    const std::string& str,
		    const std::string& tok)
{
  //======================================================================
  // Split a long string into a set of shorter strings spliting along
  // divisions makers by the characters listed in the token string
  //======================================================================
  const string::size_type S = str.size();
  string::size_type  i = 0;  

  while (i < S) {
    // eat leading whitespace
    while (i < S && tok.find(str[i]) != string::npos) {
      ++i;
    }
    if (i == S) break;  // nothing left but WS
    
    // find end of word
    string::size_type  j = i+1;
    while (j < S && tok.find(str[j]) == string::npos) {
      ++j;
    }
    
    // add word
    ls.push_back(str.substr(i,j-i));
    
    // set up for next loop
    i = j+1;
  }  
}

//-----------------------------------------------------------------------------
TDirectory* Msl::GetDir(std::string path, TDirectory *dir)
{
  //
  // Recursively create directory path in dir
  //
  if(!dir || path.empty() || path == "/") {
    return dir;
  }
  
  // remove trailing slash if present
  if(path.substr(path.size() - 1, 1) == "/") {
    path = path.substr(0, path.size() - 1);
  }
  
  std::string::size_type pos = path.find_last_of('/');
  if(pos != std::string::npos) {
    // recursively walk upward until all slash characters are removed
    dir = Msl::GetDir(path.substr(0, pos), dir);
    
    // make directory path of last substring without slash
    path = path.substr(pos + 1, path.size() - pos);
  }
  
  if(dir -> Get(path.c_str())) {
    return dynamic_cast<TDirectory *>(dir -> Get(path.c_str()));
  }
  
  return dir -> mkdir(path.c_str());
}

//-----------------------------------------------------------------------------
TDirectory* Msl::GetDir(TDirectory *dir, std::string path)
{
  return Msl::GetDir(path, dir);
}

//-----------------------------------------------------------------------------
TH1* Msl::SetDir(TH1 *h, TDirectory *dir, const string &name)
{
  if(!h) return h;

  if(!name.empty()) {
    h -> SetName(name.c_str());
  }

  h -> SetDirectory(dir);

  return h;
}

//---------------------------------------------------------------------------------
pair<string, string>  Msl::Round2Pair(double value, double error, int nprec)
{
   //
   // Round value using error
   //
   stringstream valueS, errorS;
  
   if(error < 0.0)
   {
      valueS << static_cast<int64_t>(value);
      return pair<string, string>(valueS.str(), errorS.str());  
   }
   if(!(error > 0.0))
   {
      valueS << value;
      errorS << error;
      return pair<string, string>(valueS.str(), errorS.str());  
   }
   if(nprec>10){
      valueS << value;
      errorS << error;
      return pair<string, string>(valueS.str(), errorS.str());       
   }
   
   //
   // Get base 10 power for decimal place in error
   //
   short elogi = 0;
   if(error < 1.0)
   {
      elogi = -static_cast<int>(std::ceil(std::fabs(std::log10(error))));
   }
   else
   {
      elogi = +static_cast<int>(std::floor(std::fabs(std::log10(error))));
   }
      
   //
   // Scale factor to place top two digits in error between 0 and 99
   //
   const double factor = 10.0*std::pow(10.0, -elogi);
      
   //
   // Scale value and error up and round off parts after decimal place
   //
   const double valueD = factor*std::fabs(value);
   const double errorD = factor*error;
      
   int64_t errorI = static_cast<int64_t>(std::floor(errorD));
   int64_t valueI = static_cast<int64_t>(std::floor(valueD));
   
   if(errorD - std::floor(errorD) > 0.5) ++errorI;
   if(valueD - std::floor(valueD) > 0.5) ++valueI;  

   //
   // Get precision for error
   //
   int64_t valueP = 0;
   if     (elogi == 0) valueP = 1;
   else if(elogi  < 0) valueP = 1 - elogi;

   if(value < 0.0) valueS << "-";

   valueS << std::fixed
	  << std::setprecision(valueP) << static_cast<double>(valueI)/factor;
   errorS << std::fixed
	  << std::setprecision(valueP) << static_cast<double>(errorI)/factor;
   
   return pair<string, string>(valueS.str(), errorS.str());
}

//-----------------------------------------------------------------------------
std::string Msl::PadStrFront(std::string str, int width)
{
  // Pad str with blanks
  if(width < 1) return str; 

  const int osize = str.size();
  for(int i = 0; i < width; ++i) {
    if(i >= osize) str.insert(str.begin(), ' ');
  }
  
  return str;
}

//-----------------------------------------------------------------------------
std::string Msl::PadStrBack(std::string str, int width)
{
  // Pad str with blanks
  if(width < 1) return str; 

  const int osize = str.size();
  for(int i = 0; i < width; ++i) {
    if(i >= osize) str.push_back(' ');
  }
  
  return str;
}

//------------------------------------------------------------------------------------------
double Msl::file_size(const std::string &path)
{
   //
   // Return file size in megabytes
   //
   struct stat result;
   if(stat(path.c_str(), &result) != 0)
   {
      return 0.0;
   }
   
   return double(result.st_size)/1038336.0;
}

//------------------------------------------------------------------------------------------
std::string Msl::MakeLink(const std::string &link, const std::string &text)
{
  //
  // Return html code to hyperlink to this group
  //
  stringstream lstr;
  lstr << "<a STYLE=\"text-decoration:none\" href=\""
       << link
       << "\"" << ">" << text << "</a>";
  
  return lstr.str();
}

//-----------------------------------------------------------------------------------------      
// Helper functions for converting comma delimated string to vector of values
//
vector<int> Msl::GetIntVec(const string &list)
{
   vector<string> namelist;
   Msl::StringTok(namelist, list, ", ");
   
   vector<int> ivec;
   for(vector<string>::const_iterator sit = namelist.begin(); sit != namelist.end(); ++sit)
   {
      const int newbase = std::atoi(sit -> c_str());
      if(newbase != 0)
      {
	 ivec.push_back(newbase);
      }
   }
   
   return ivec;
}

vector<string> Msl::GetStringVec(const string &list)
{
   vector<string> namelist;
   Msl::StringTok(namelist, list, ", ");

   vector<string> nvec;
   for(vector<string>::const_iterator sit = namelist.begin(); sit != namelist.end(); ++sit)
   {
      if(!sit -> empty())
      {
	 nvec.push_back(*sit);
      }
   }
   
   return nvec;
}

//-----------------------------------------------------------------------------------------      
bool Msl::HasBranch(TTree *tree, const std::string &branch, bool debug)
{
  //
  // Return true if tree has a branch
  //
  if(!tree) {
    return false;
  }
  
  TObjArray *list = tree->GetListOfBranches();
  if(!list) {
    return false;
  }

  if(debug) {
    cout << "HasBranch - tree name: " << tree->GetName() 
	 << " with " << list->GetLast() << " branch(es)" << endl;
  }

  for(int i = 0; i <= list->GetLast(); ++i) {
    TObject *obj = list->At(i);
    if(!obj) {
      continue;
    }
    
    if(debug) {
      cout << "  branch: " << obj->GetName() << endl;
    }

    if(obj->GetName() == branch) {
      return true;
    }
  }
  
  return false;
}

//-----------------------------------------------------------------------------------------      
namespace HashChecking
{
  static std::map<std::string,  std::map<unsigned int, std::string> > AllHashesByCategory;
  
  void CheckGeneratedHash (unsigned int hash,  const std::string& s,   const std::string& category)
  {
    //
    // \brief function used to generate uniqu  ID (integer) from string
    //        In fact uniqueness is not 100% guaranteed
    //
    // \param s string to be hashed
    //
    std::map<unsigned int, std::string>& hashes = AllHashesByCategory[category];

    const std::map<unsigned int, std::string>::const_iterator sit = hashes.find(hash);
    if ( sit == hashes.end()) {
      hashes[hash] = s;
    }
    else if ( sit->second != s ) {
      throw std::domain_error("Hashes the same for category: "+category
			      + " and elements "+ hashes[hash] + " "+ s );
    }
  }
}

//-----------------------------------------------------------------------------------------      
unsigned long int Msl::String2Hash( const std::string& s, const std::string& category ) // was uint32_t - see comment next to stdint.h
{
  //
  // hash function (based on available elswhere ELF hash function)
  // uniqueness tested in MC way. Implemented by Tomasz Bold and
  // copied from  TrigConfHLTData/src/HLTUtils.cxx
  // 

  unsigned long int hash = 0xd2d84a61; // was uint32_t - see comment next to stdint.h

  for (int i = (int)s.size()-1; i >= 0; --i )
    hash ^= ( hash >> 5) + s[i] + ( hash << 7 );

  for (int i = 0; i < (int)s.size(); ++i )
    hash ^= ( hash >> 5) + s[i] + ( hash << 7 );

  //
  // Make sure that has is greater than 2^14=16382 to avoid collisions with user keys
  // 
  if(hash < 16383) hash += 16382;
    
  HashChecking::CheckGeneratedHash(hash, s, category);

  return hash;
}

//-----------------------------------------------------------------------------------------      
void Msl::PrintHashMap()
{
  cout << "PrintHashMap - print " << HashChecking::AllHashesByCategory.size() << " hash map(s)" << endl;

  std::map<std::string,  std::map<unsigned int, std::string> >::const_iterator it = HashChecking::AllHashesByCategory.begin();
  
  for(; it != HashChecking::AllHashesByCategory.end(); ++it) {
    cout << "   category: \"" << it->first << "\"" << endl;

    const std::map<unsigned int, std::string> &hmap = it->second;
    std::map<unsigned int, std::string>::const_iterator hit = hmap.begin();
    
    for(; hit != hmap.end(); ++hit) {
      cout << "      " << setw(10) << hit->first << ": " << hit->second << endl;
    }
  }
}

//-----------------------------------------------------------------------------
// "Nice" print function for stopwatch
//
std::string Msl::PrintResetStopWatch(TStopwatch &watch)
{
  watch.Stop();
  
  double realt = watch.RealTime();
  double cput  = watch.CpuTime();
  
  watch.Reset();
  watch.Start();
  
  const int hours = static_cast<int>(realt/3600.0);
  const int  min  = static_cast<int>(realt/60.0) - 60*hours;
  
  realt -= hours * 3600;
  realt -= min * 60;
  
  if (realt < 0) realt = 0;
  if (cput  < 0) cput  = 0;
  
  const int sec = static_cast<int>(realt);
  
  std::stringstream str;
  str << "Real time " 
      << setw(2) << setfill('0') << hours 
      << ":" << setw(2) << setfill('0') << min
      << ":" << setw(2) << setfill('0') << sec
      << " CPU time " << setprecision(3) << fixed << cput;
  
  return str.str();
}

//-----------------------------------------------------------------------------
double Msl::GetDR(double eta1, double phi1, double eta2, double phi2)
{
  //
  // Compute delta R
  //
  const double d1 = eta1-eta2;
  const double d2 = TVector2::Phi_mpi_pi(phi1-phi2);

  return std::sqrt(d1*d1 + d2*d2);
}

//-----------------------------------------------------------------------------
double Msl::GetDPhi(const double &phi1, const double &phi2)
{
  //
  // Compute delta R
  //
  //const double d2 = TVector2::Phi_mpi_pi(phi1-phi2);
  const double d2 = fabs(phi1-phi2)>3.14159 ? 6.2831 - fabs(phi1-phi2) : fabs(phi1-phi2);
  return d2;
}


//---------------------------------------------------------------------------------------
bool Msl::SortPhysicsObject::operator()(const TLorentzVector &lhs, const TLorentzVector &rhs) const
{

  //
  // Sort based on pt 
  //
  return lhs.Pt() > rhs.Pt();
}

//---------------------------------------------------------------------------------------
bool Msl::SortPhysicsObject::operator()(const TVector3 &lhs, const TVector3 &rhs) const
{

  //
  // Sort based on pt 
  //
  return lhs.Pt() > rhs.Pt();
}



