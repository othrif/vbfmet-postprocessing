#ifndef MSL_VAREVENT_H
#define MSL_VAREVENT_H

/**********************************************************************************
 * @Package: MonojetSoftLepton
 * @Author : Rustem Ospanov, Doug Schaefer
 *
 * @Brief  :
 * 
 *  List of event variables for monojet analysis
 * 
 **********************************************************************************/

// C/C++
#include <string>
#include <vector>
//#include <stdint.h> // The stdint.h of OSX 10.9 is too complex for CINT to process. Problem will go away in ROOT 6.

// ROOT
#include "Rtypes.h"

namespace Msl
{
  class Registry;

  namespace Mva 
  {
    enum Var 
    {
      //
      // Variables added by ReadEvent and FillEvent algorithms
      //
      NONE = 0, 
      jj_deta,
      jj_dphi,
      jj_mass,

      trigger_met,
      trigger_lep,
      passJetCleanTight,
      //
      // KInematic variables read directly from standard ntuples
      //   - enum name must match branch name from HWW tree
      //
      met_tst_et,
      met_tst_phi,      
      met_tst_nolep_et,
      n_jet,
      n_el,
      n_mu,
      met_tst_j1_dphi,
      met_tst_j2_dphi,
      met_tst_nolep_j1_dphi,
      met_tst_nolep_j2_dphi,
      jetPt0,
      jetPt1,
      etaj0TimesEtaj1,
      lepPt0,
      lepPt1,
      lepCh0,
      lepCh1,
      chanFlavor,
      mll,
      ptll,
      mt,
      charge,
      timing,
      j0timing,
      j1timing
    };

    std::string       AsStr(Var var);
    std::string Convert2Str(Var var);
    Var         Convert2Var(const std::string &var);   
    Var         Convert2Var(unsigned long int           key); // was uint32_t - see comment next to stdint.h

    
    Msl::Mva::Var ReadVar(const Msl::Registry &reg, 
			  const std::string &key, 
			  const std::string &caller = "ReadVar");
    
    std::vector<Msl::Mva::Var> ReadVars(const Msl::Registry &reg, 
					const std::string &key, 
					const std::string &caller = "ReadVars");

    std::vector<Msl::Mva::Var> ReadVars(const std::string &config,
					const std::string &caller = "ReadVars");

    const std::vector<std::string>  & GetAllVarNames();
    const std::vector<Msl::Mva::Var>& GetAllVarEnums();
  }
}

#endif
