// Local
#include "HInvPlot/Registry.h"
#include "HInvPlot/VarEvent.h"

using namespace std;

//-----------------------------------------------------------------------------
std::string Msl::Mva::AsStr(Var var)
{
  return Convert2Str(var);
}

//-----------------------------------------------------------------------------
std::string Msl::Mva::Convert2Str(Var var)
{
  switch(var) 
    {
    case jj_deta:	          return "jj_deta";
    case jj_dphi:	          return "jj_dphi";
    case jj_mass:	          return "jj_mass";
      
    case trigger_met:	          return "trigger_met";
    case trigger_lep:	          return "trigger_lep";
    case passJetCleanTight:	  return "passJetCleanTight";

    case met_tst_et:	          return "met_tst_et";
    case met_tst_phi:	          return "met_tst_phi";
    case met_tst_nolep_et:	  return "met_tst_nolep_et";
    case met_tst_nolep_phi:	  return "met_tst_nolep_phi";
    case met_significance:	  return "met_significance";
    case n_jet:	                  return "n_jet";
    case n_el:	                  return "n_el";
    case n_mu:	                  return "n_mu";
    case met_tst_j1_dphi:	  return "met_tst_j1_dphi";
    case met_tst_j2_dphi:	  return "met_tst_j2_dphi";
    case met_tst_nolep_j1_dphi:	  return "met_tst_nolep_j1_dphi";
    case met_tst_nolep_j2_dphi:	  return "met_tst_nolep_j2_dphi";
    case jetPt0:	          return "jetPt0";
    case jetPt1:	          return "jetPt1";
    case etaj0TimesEtaj1:	  return "etaj0TimesEtaj1";
    case lepPt0:	          return "lepPt0";      
    case lepPt1:	          return "lepPt1";
    case lepCh0:	          return "lepCh0";      
    case lepCh1:	          return "lepCh1";            
    case mll:	                  return "mll";
    case ptll:	                  return "ptll";
    case mt:	                  return "mt";
    case chanFlavor:	          return "chanFlavor";      
    case charge:	          return "charge";
    case timing:	          return "timing";
    case j0timing:	          return "j0timing";
    case j1timing:	          return "j1timing";

    case NONE: return "NONE";
    default  : break;
    }
  
  cout << "Msl::Mva::Convert2Str - unknown enum: " << var << endl;
  return "NONE";
}

//-----------------------------------------------------------------------------
Msl::Mva::Var Msl::Mva::Convert2Var(const std::string &var)
{
  if(var == "NONE")          return NONE;
  if(var == "jj_deta")       return jj_deta;
  if(var == "jj_dphi")       return jj_dphi;
  if(var == "jj_mass")       return jj_mass;
  if(var == "trigger_met")   return trigger_met;  
  if(var == "trigger_lep")   return trigger_lep;  
  if(var == "passJetCleanTight")   return passJetCleanTight;  
  if(var == "met_tst_et")    return met_tst_et;
  if(var == "met_tst_phi")    return met_tst_phi;  
  if(var == "met_tst_nolep_et")  return met_tst_nolep_et;
  if(var == "met_tst_nolep_phi")  return met_tst_nolep_phi;
  if(var == "met_significance")  return met_significance;
  if(var == "n_jet")             return n_jet;
  if(var == "n_el")              return n_el;
  if(var == "n_mu")              return n_mu;
  if(var == "met_tst_j1_dphi")   return met_tst_j1_dphi;
  if(var == "met_tst_j2_dphi")   return met_tst_j2_dphi;
  if(var == "met_tst_nolep_j1_dphi")   return met_tst_nolep_j1_dphi;
  if(var == "met_tst_nolep_j2_dphi")   return met_tst_nolep_j2_dphi;
  if(var == "jetPt0")            return jetPt0;
  if(var == "jetPt1")            return jetPt1;
  if(var == "etaj0TimesEtaj1")   return etaj0TimesEtaj1;
  if(var == "lepPt0")            return lepPt0;
  if(var == "lepPt1")            return lepPt1;
  if(var == "lepCh0")            return lepCh0;
  if(var == "lepCh1")            return lepCh1;
  if(var == "mll")               return mll;
  if(var == "ptll")              return ptll;
  if(var == "mt")                return mt;
  if(var == "chanFlavor")        return chanFlavor;  
  if(var == "charge")            return charge;
  if(var == "timing")            return timing;
  if(var == "j0timing")          return j0timing;
  if(var == "j1timing")          return j1timing;

  cout << "Msl::Mva::Convert2Var - unknown enum: " << var << endl;
  return NONE;
}

//-----------------------------------------------------------------------------
Msl::Mva::Var Msl::Mva::Convert2Var(unsigned long int key)
{
  const vector<Var> &vars = GetAllVarEnums();
  
  //
  // Find matching enum by value
  //
  //const vector<Var>::const_iterator vit = std::find(vars.begin(), vars.end(), Convert2Var(key));
  const vector<Var>::const_iterator vit = std::find(vars.begin(), vars.end(), key);
  
  if(vit != vars.end()) {
    return *vit;
  }

  return NONE;
}

//-----------------------------------------------------------------------------
Msl::Mva::Var Msl::Mva::ReadVar(const Registry &reg, 
				const std::string &key, 
				const std::string &caller)
{
  //
  // Read vector of variable names and convert to Var enums
  //
  const vector<Var> vars = ReadVars(reg, key, caller);

  if(vars.size() == 1) {
    return vars.front();
  }

  return NONE;
}

//-----------------------------------------------------------------------------
std::vector<Msl::Mva::Var> Msl::Mva::ReadVars(const Registry &reg, 
					      const std::string &key, 
					      const std::string &caller)
{
  //
  // Read vector of variable names and convert to Var enums
  //
  vector<string> keys;
  reg.Get(key, keys);

  vector<Var> vars;  

  for(unsigned i = 0; i < keys.size(); ++i) {
    const Var var = Mva::Convert2Var(keys.at(i));
    if(var != NONE) {
      vars.push_back(var);
    }
    else {
      cout << caller << " - unknown variable name: " << keys.at(i) << endl;
    }
  }

  return vars;
}

//-----------------------------------------------------------------------------
std::vector<Msl::Mva::Var> Msl::Mva::ReadVars(const std::string &config, 
					      const std::string &caller)
{
  //
  // Read vector of variable names and convert to Var enums
  //
  vector<string> keys;
  Msl::StringTok(keys, config, ", ");

  vector<Var> vars;  

  for(unsigned i = 0; i < keys.size(); ++i) {
    const Var var = Mva::Convert2Var(keys.at(i));
    if(var != NONE) {
      vars.push_back(var);
    }
    else {
      cout << caller << " - unknown variable name: " << keys.at(i) << endl;
    }
  }

  return vars;
}

//-----------------------------------------------------------------------------
const std::vector<Msl::Mva::Var>& Msl::Mva::GetAllVarEnums()
{
  static vector<Var> vars;

  if(vars.empty()) {
    //
    // Fill vector with all available enums
    //
    vars.push_back(jj_deta);
    vars.push_back(jj_dphi);
    vars.push_back(jj_mass);
    vars.push_back(trigger_met);
    vars.push_back(trigger_lep);
    vars.push_back(passJetCleanTight);
    
    vars.push_back(met_tst_et);
    vars.push_back(met_tst_phi);
    vars.push_back(met_tst_nolep_et);
    vars.push_back(met_tst_nolep_phi);
    vars.push_back(met_significance);
    vars.push_back(n_jet);    
    vars.push_back(n_el);    
    vars.push_back(n_mu);    
    vars.push_back(met_tst_j1_dphi);    
    vars.push_back(met_tst_j2_dphi);    
    vars.push_back(met_tst_nolep_j1_dphi);    
    vars.push_back(met_tst_nolep_j2_dphi);    
    vars.push_back(jetPt0);    
    vars.push_back(jetPt1);    
    vars.push_back(etaj0TimesEtaj1);    
    vars.push_back(lepPt0);    
    vars.push_back(lepPt1);    
    vars.push_back(lepCh0);    
    vars.push_back(lepCh1);    
    vars.push_back(mll);    
    vars.push_back(ptll);    
    vars.push_back(mt);    
    vars.push_back(chanFlavor);    
    vars.push_back(charge);    
    vars.push_back(timing);     
    vars.push_back(j0timing);     
    vars.push_back(j1timing);     
  }
  
  return vars;
}

//-----------------------------------------------------------------------------
const std::vector<std::string>& Msl::Mva::GetAllVarNames()
{
  static vector<string> names;

  if(names.empty()) {
    const vector<Var> vars = Mva::GetAllVarEnums();

    for(unsigned i = 0; i < vars.size(); ++i) {
      const string name = Mva::AsStr(vars.at(i));

      if(name != Mva::AsStr(NONE)) {
	names.push_back(name);
      }
      else {
	cout << "GetAllVarNames - unknown var: " << vars.at(i) << endl;
      }
    }
  }

  return names;
}
