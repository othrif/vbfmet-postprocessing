#ifndef MSL_REGISTRY_H
#define MSL_REGISTRY_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : Registry
 * @Author : Rustem Ospanov
 *
 * @Brief  :
 *
 * Registry class helps with job configuration.
 * 
 * Class stores (key, value) pairs for following types for values:
 *  - string
 *  - double
 *  - Registry
 *
 *  - provides int, unsigned, const char * Get() functions which are 
 *    internally converted to/from the above three basic types
 *
 *  - provides access methods for reading ',' separated lists as vectors
 *
 *  Use partial template implementation of Get/Set functions.
 *
 **********************************************************************************/

// C/C++
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>
#include <vector>

// XML
//#include "libxml/parser.h"
//#include "libxml/tree.h"
//#include "libxml/xmlversion.h"
//#include "libxml/xmlstring.h"

// Local
#include "DataPair.h"
#include "UtilCore.h"

namespace Msl
{
  class Registry
  {
  public:

    typedef DataPair<std::string, std::string>   StrData;
    typedef DataPair<std::string, long double>   DblData;
    typedef DataPair<std::string, Registry>      RegData;

  public:
    
    Registry() :fUniqueKeys(true) {}
    ~Registry() {}

    // Deep copy of rhs into this Registry
    void Merge(const Registry& rhs);

    // Deep copy of rhs into this Registry: append to existing string values
    void Add(const Registry& rhs);
    
    bool KeyExists(const std::string &key) const;
    bool RemoveKey(const std::string &key);
    
    void AllowNonUniqueKeys() { fUniqueKeys = false; }

    // Full clear of this Registry 
    void Clear();
    
    //
    // Non-templated functions for cint
    //
    void SetVal(const std::string &key, float                val);
    void SetVal(const std::string &key, double               val);
    void SetVal(const std::string &key, int                  val);
    void SetVal(const std::string &key, const std::string   &val);
    void SetVal(const std::string &key, const Msl::Registry &val);

    //
    // Access functions - T=string, Registry or number
    //
    template<class T> bool Get(const std::string &alg, const std::string& key, T &val) const;   
    template<class T> bool Get(const std::string &key,                         T &val) const;

    //
    // Set functions - T=string, char, Registry or number
    //
    template<class T> void Set(const std::string &key, const T &val);
    template<class T> void Set(const std::string &key, const T *val);

    //
    // String values are interpreted as comma separated list of numbers
    //
    template<class T> bool GetVec(const std::string &key,                         std::vector<T> &val) const;
    template<class T> bool GetVec(const std::string &alg, const std::string &key, std::vector<T> &val) const;
									    
    //
    // Functions for python to C++ translation via strings
    //
    void SetValueDouble(const std::string &key, const std::string &value);
    void SetValueLong  (const std::string &key, const std::string &value);

    //
    // Read key value as string and then convert it to vector using ',' delimeter
    //
    bool Get(const std::string &key, std::vector<std::string> &val) const;
    bool Get(const std::string &key, std::vector<int>         &val) const;
    bool Get(const std::string &key, std::vector<double>      &val) const;

    // Get internal storage vectors
    const std::vector<Msl::Registry::StrData>& GetStr() const { return fStr; }
    const std::vector<Msl::Registry::DblData>& GetDbl() const { return fDbl; }
    const std::vector<Msl::Registry::RegData>& GetReg() const { return fReg; }

    // Print and read methods
    void Print(std::ostream &os = std::cout,
	       unsigned int margin = 0, const std::string &key = "") const;

    void Read(std::istream &is) const;
    
    void PrintConfig(std::ostream &os = std::cout, const std::string &key = "") const;
    
    void WriteXML(const std::string  &path, unsigned left_pad = 0) const;
    void WriteXML(std::ostream &outf, unsigned left_pad = 0) const;

    static int StringToBool(const std::string &val);

  private:
    
    bool                                 fUniqueKeys;
    std::vector<Msl::Registry::StrData>  fStr;              //! - do not make dictionary
    std::vector<Msl::Registry::DblData>  fDbl;              //! - do not make dictionary             
    std::vector<Msl::Registry::RegData>  fReg;              //! - do not make dictionary
  };

  //
  // XML parsing using lbxml2
  //
  inline Registry ParseXml(const std::string & /*fname*/, bool /*debug*/) {
    //LIBXML_TEST_VERSION
    //
    //  Registry reg;
    //reg.AllowNonUniqueKeys();
    //
    //if(debug) {
    //  std::cout << "ParseXml - read file: " << fname << std::endl;
    //}
    //
    ////
    //// Parse the file and get the DOM 
    ////
    //xmlDoc *doc = xmlReadFile(fname.c_str(), NULL, 0);
    //
    //if(doc == NULL) {
    //  std::cout << "ParseXml - failed to parse file: " << fname << std::endl;
    //  return reg;
    //}
    //
    ////
    ////Get the root element node 
    ////
    //xmlNode *root_element = xmlDocGetRootElement(doc);
    //
    //if(root_element == NULL || !(root_element->name)) {
    //  std::cout << "ParseXml - null root element pointer or missing name" << std::endl;
    //  xmlFreeDoc(doc);
    //  return reg;
    //}
    //
    //std::stringstream root_name;
    //root_name << root_element->name;
    //
    //reg.Set("RootElement", root_name.str());
    //
    ////
    //// Parse XML tree
    ////
    //ReadTree(root_element, reg, debug);
    //
    //if(debug) reg.Print();
    //
    ////
    //// Free document and free global variables that may have been allocated
    ////
    //xmlFreeDoc(doc);
    //xmlCleanupParser();
    //
    //return reg;
    std::cout << "ParseXml - this function is not implemented yet" << std::endl;
    return Registry();
  }

  //
  // Inlined functions
  //
  inline std::ostream& operator<<(std::ostream& os, const Msl::Registry &reg) {
    reg.Print(os);
    return os;
  }
}

#ifndef __CINT__
#include "Registry.icc"
#endif

#endif
