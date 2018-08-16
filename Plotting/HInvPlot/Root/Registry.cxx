// C/C++
#include <cstring>
#include <fstream>
#include <sstream>

// Local
#include "HInvPlot/UtilCore.h"
#include "HInvPlot/Registry.h"

using namespace std;

//----------------------------------------------------------------------------------
void Msl::Registry::Merge(const Registry &rhs)
{
  //
  // Copy rhs into this: replace value if key already exists
  //
  for(unsigned int i = 0; i < rhs.fStr.size(); ++i) Set(rhs.fStr[i].Key(), rhs.fStr[i].Data());
  for(unsigned int i = 0; i < rhs.fDbl.size(); ++i) Set(rhs.fDbl[i].Key(), rhs.fDbl[i].Data());
  for(unsigned int i = 0; i < rhs.fReg.size(); ++i) Set(rhs.fReg[i].Key(), rhs.fReg[i].Data());
}

//----------------------------------------------------------------------------------
void Msl::Registry::SetValueDouble(const std::string &key, const std::string &value)
{
  if(value.empty()) {
    cout << "Registry::SetValueDouble(" << key << ", " << value << ") - invalid value" << endl;
    return;
  }

  std::stringstream str;
  str << value;

  long double val = -1.0e100;
  str >> val;
 
  if(!str.fail()) {
    Set(key, val);
  }
  else {
    cout << "Registry::SetValueDouble(" << key << ", " << value << ") - failed to read value: " 
	 << val << endl
	 << "   eofbit= " << (str.rdstate() & std::ios_base::eofbit)  << endl
	 << "   badbit= " << (str.rdstate() & std::ios_base::badbit)  << endl
	 << "   failbit=" << (str.rdstate() & std::ios_base::failbit) << endl;
  }
}

//----------------------------------------------------------------------------------
void Msl::Registry::SetValueLong(const std::string &key, const std::string &value)
{
  if(value.empty()) {
    cout << "Registry::SetValueLong(" << key << ", " << value << ") - invalid value" << endl;
    return;
  }

  std::stringstream str;
  str << value;

  long double val = -100;
  str >> val;

  if(!str.fail()) {
    Set(key, val);
  }
  else {
    cout << "Registry::SetValueLong(" << key << ", " << value << ") - failed to read value: " 
	 << val << endl
	 << "   eofbit= " << (str.rdstate() & std::ios_base::eofbit)  << endl
	 << "   badbit= " << (str.rdstate() & std::ios_base::badbit)  << endl
	 << "   failbit=" << (str.rdstate() & std::ios_base::failbit) << endl;
  }
}

//----------------------------------------------------------------------------------
void Msl::Registry::SetVal(const std::string &key, float val)
{
  Set<double>(key, val);
}

//----------------------------------------------------------------------------------
void Msl::Registry::SetVal(const std::string &key, double val)
{
  Set<double>(key, val);
}

//----------------------------------------------------------------------------------
void Msl::Registry::SetVal(const std::string &key, int val)
{
  Set<double>(key, val);
}

//----------------------------------------------------------------------------------
void Msl::Registry::SetVal(const std::string &key, const std::string &val)
{
  Set<std::string>(key, val);
}

//----------------------------------------------------------------------------------
void Msl::Registry::SetVal(const std::string &key, const Registry &val)
{
  Set<Registry>(key, val);
}

//----------------------------------------------------------------------------------
void Msl::Registry::Add(const Registry &rhs)
{
  //
  // Merge registry by adding new string values to already existing strings
  //
  for(unsigned int i = 0; i < rhs.fDbl.size(); ++i) { 
    Set(rhs.fDbl[i].Key(), rhs.fDbl[i].Data());
  }

  for(unsigned int i = 0; i < rhs.fStr.size(); ++i) { 
    const string &key = rhs.fStr[i].Key();

    string val;
    if(Get(key, val)) {
      val += rhs.fStr[i].Data();
    }
    else {
      val  = rhs.fStr[i].Data();
    }

    Set(key, val);
  }

  for(unsigned int i = 0; i < rhs.fReg.size(); ++i) { 
    const string &key = rhs.fReg[i].Key();

    Registry val;
    if(Get(key, val)) {
      val.Add(fReg[i].Data());
    }
    else {
      val = rhs.fReg[i].Data();
    }

    Set(key, val);
  }
}

//----------------------------------------------------------------------------------
bool Msl::Registry::KeyExists(const std::string &key) const
{
  if(Msl::KeyExists<std::string>(fStr, key)) return true;
  if(Msl::KeyExists<long double>(fDbl, key)) return true;
  if(Msl::KeyExists<Registry>   (fReg, key)) return true;

  return false;
}

//----------------------------------------------------------------------------------
bool Msl::Registry::RemoveKey(const std::string &key)
{
  if(Msl::RemoveKey<std::string>(fStr, key)) return true;
  if(Msl::RemoveKey<long double>(fDbl, key)) return true;
  if(Msl::RemoveKey<Registry>   (fReg, key)) return true;

  return false;
}

//----------------------------------------------------------------------------------
void Msl::Registry::Clear()
{
  fStr.clear();
  fDbl.clear();
  fReg.clear();
}

//----------------------------------------------------------------------------------
bool Msl::Registry::Get(const std::string &key, std::vector<std::string> &val) const
{
  std::string tmp;
  if(!Msl::GetVal<std::string>(fStr, key, tmp)) return false;
  Msl::StringTok(val, tmp, ", ");
  return true;
}

//----------------------------------------------------------------------------------
bool Msl::Registry::Get(const std::string &key, std::vector<int> &val) const
{
  return GetVec<int>(key, val);
}

//----------------------------------------------------------------------------------
bool Msl::Registry::Get(const std::string &key, std::vector<double> &val) const
{
  return GetVec<double>(key, val);
}

//----------------------------------------------------------------------------------
namespace Reg
{
  std::ostream& Pad(std::ostream &os, unsigned int margin) {
    for(unsigned int i = 0; i < margin; ++i) {
      os << ' ';
    }
    
    return os;
  }
}

//----------------------------------------------------------------------------------
void Msl::Registry::Print(std::ostream &os,
			  unsigned int margin,
			  const std::string &key) const
{
  Reg::Pad(os, margin) << "Registry::Print" << std::endl;

  Msl::Print<std::string>(fStr, os, "STRING", margin, key);
  Msl::Print<long double>(fDbl, os, "DOUBLE", margin, key);

  for(unsigned int i = 0; i < fReg.size(); ++i) {
    if(!key.empty() && fReg[i].Key().find(key) == std::string::npos) continue;

    Reg::Pad(os, margin) << "\"" << fReg[i].Key() << "\"" << std::endl;
    fReg[i].Data().Print(os, margin+3);
  }  
}

//----------------------------------------------------------------------------------
void Msl::Registry::Read(std::istream &) const
{
}

//----------------------------------------------------------------------------------
void Msl::Registry::PrintConfig(std::ostream &os, const std::string &key) const
{
  bool print_config = false; 
  if(Get(key+"::PrintConfig", print_config) && print_config) {
    os << key << "::PrintConfig" << std::endl;
    Print(os, 3, key);
  } 
}

//----------------------------------------------------------------------------------
void Msl::Registry::WriteXML(const std::string &path, unsigned left_pad) const
{
  //
  // Write self as XML file to "path"
  //
  
  std::ofstream outf(path.c_str());
  if(!outf.is_open()) { 
    cout << "Registry::WriteXML - failed to open file: " << path << endl;    
    return;
  }
  
  WriteXML(outf, left_pad);
}

//----------------------------------------------------------------------------------
namespace Msl
{
  string ConvertKey2Xml(const std::string &key) 
  {
    string res;

    for(unsigned i = 0; i < key.size(); ++i) {
      if(key.at(i) == '<') {
	res.push_back('&');
	res.push_back('l');
	res.push_back('t');
	res.push_back(';');
      }
      else if(key.at(i) == '>') {
	res.push_back('&');
	res.push_back('g');
	res.push_back('t');
	res.push_back(';');
      }
      else {
	res.push_back(key.at(i));
      }
    }

    return res;
  }
}

//----------------------------------------------------------------------------------
void Msl::Registry::WriteXML(std::ostream &outf, unsigned left_pad) const
{
  string pad1(left_pad+0, ' ');
  string pad2(left_pad+2, ' ');
  
  outf << pad1 << "<Registry>" << endl
       << pad2 << "<AllowNonUniqueKeys>" << !fUniqueKeys << "</AllowNonUniqueKeys>" << endl; 

  outf << pad2 << "<StringVector>" << endl;
  for(unsigned i = 0; i < fStr.size(); ++i) {
    outf << pad2 << "  <DataPair>" << endl 
	 << pad2 << "    <key>"  << ConvertKey2Xml(fStr.at(i).Key())  << "</key>"  << endl
	 << pad2 << "    <data>" << ConvertKey2Xml(fStr.at(i).Data()) << "</data>" << endl
	 << pad2 << "  </DataPair>" << endl;
  }  
  outf << pad2 << "</StringVector>" << endl;

  outf << pad2 << "<DoubleVector>" << endl;
  for(unsigned i = 0; i < fDbl.size(); ++i) {
    outf << pad2 << "  <DataPair>" << endl 
	 << pad2 << "    <key>"  << ConvertKey2Xml(fDbl.at(i).Key())  << "</key>"  << endl
	 << pad2 << "    <data>" << setprecision(12) << fDbl.at(i).Data() << "</data>" << endl
	 << pad2 << "  </DataPair>" << endl;
  }  
  outf << pad2 << "</DoubleVector>" << endl;

  outf << pad2 << "<RegistryVector>" << endl;
  for(unsigned i = 0; i < fReg.size(); ++i) {
    outf << pad2 << "  <DataPair>" << endl 
	 << pad2 << "    <key>"  << fReg.at(i).Key()  << "</key>"  << endl;
    fReg.at(i).Data().WriteXML(outf, left_pad+6);
    outf << pad2 << "  </DataPair>" << endl;
  }
  outf << pad2 << "</RegistryVector>" << endl;

  outf << pad1 << "</Registry>" << endl;
}


//----------------------------------------------------------------------------------
// Help function for reading Registry from XML
//
namespace Msl
{
  void FillReg(Registry &in_reg, Registry &out_reg)
  {
    //
    // Read additional keys
    //
    int ukey = 0;
    if(in_reg.Get("AllowNonUniqueKeys", ukey)) {
      if(ukey == 1) out_reg.AllowNonUniqueKeys();
    }
    
    //
    // Read string registry objects
    //    
    Registry str_reg;
    if(in_reg.Get("StringVector", str_reg)) {

      while(str_reg.KeyExists("DataPair")) {
	//
	// Read registry for one key
	//
	Registry key_reg;
	str_reg.Get("DataPair", key_reg);
	str_reg.RemoveKey("DataPair");
	
	string key, data;

	if(key_reg.Get("key",  key) && 
	   key_reg.Get("data", data)) {
	  out_reg.Set(key, data);
	}
	else {
	  //
	  // Try to convert double to string
	  //
	  double data_dbl = 0.0;

	  if(key_reg.Get("key",  key) && 
	     key_reg.Get("data", data_dbl)) {
	    stringstream str;
	    str << data_dbl;
	    out_reg.Set(key, str.str());
	  }
	  else {
	    cout << "FillReg - error: bad DataPair in StringVector" << endl;
	    in_reg.Print();
	    key_reg.Print();
	  }
	}
      }
    }
  
    //
    // Read double registry objects
    //    
    Registry dbl_reg;
    if(in_reg.Get("DoubleVector", dbl_reg)) {

      while(dbl_reg.KeyExists("DataPair")) {
	//
	// Read registry for one key
	//
	Registry key_reg;
	dbl_reg.Get("DataPair", key_reg);
	dbl_reg.RemoveKey("DataPair");
	
	string key;
	long double data = -2.0e100;

	if(key_reg.Get("key",  key) && 
	   key_reg.Get("data", data)) {
	  out_reg.Set(key, data);
	}
	else {
	  cout << "FillReg - error: bad DataPair in DoubleVector: " << endl;
	  key_reg.Print();
	}
      }
    }
    
    //
    // Read "Registry" registry objects
    //    
    Registry reg_reg;
    if(in_reg.Get("RegistryVector", reg_reg)) {

      while(reg_reg.KeyExists("DataPair")) {
	//
	// Read registry for one key
	//
	Registry key_reg;
	reg_reg.Get("DataPair", key_reg);
	reg_reg.RemoveKey("DataPair");
	
	string key;
	Registry data;

	if(key_reg.Get("key",  key) && 
	   key_reg.Get("Registry", data)) {
	  //
	  // Recursive call to read child registry
	  //
	  Registry val;
	  FillReg(data, val);
	  out_reg.Set(key, val);
	}
	else {
	  cout << "FillReg - error: bad DataPair in RegistryVector" << endl;
	}
      }
    }
  }
}

//----------------------------------------------------------------------------------
int Msl::Registry::StringToBool(const std::string &val)
{
  //
  // Convert string to bool
  //
  if(val == "TRUE"  || val == "True"  || val == "true"  || val == "yes" || val == "Yes" || val == "YES") return 1;
  if(val == "FALSE" || val == "False" || val == "false" || val == "no"  || val == "No"  || val == "NO")  return 0;
  
  return -1;
}
