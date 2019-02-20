#ifndef MSL_VAREVENT_H
#define MSL_VAREVENT_H

/**********************************************************************************
 * @Package: HInvPlot
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
      trigger_met_encoded,      
      trigger_met_encodedv2,
      trigger_lep,
      passJetCleanTight,
      xeSFTrigWeight,
      xeSFTrigWeight__1up,
      xeSFTrigWeight__1down,
      //
      // KInematic variables read directly from standard ntuples
      //   - enum name must match branch name from HWW tree
      //
      met_truth_et,
      met_truth_phi,
      met_tst_et,
      met_tst_phi,
      met_tst_nolep_et,
      met_tst_nolep_phi,
      met_tenacious_tst_nolep_et,
      met_tenacious_tst_nolep_phi,
      met_significance,
      metsig_tst,
      met_tenacious_tst_et,
      met_tight_tst_et,
      met_tighter_tst_et,
      met_soft_tst_et,
      met_tenacious_tst_phi,
      met_tight_tst_phi,
      met_tighter_tst_phi,
      met_soft_tst_phi,
      met_soft_tst_sumet,
      met_cst_jet,
      n_jet,
      n_bjet,
      n_jet_fwd,
      n_jet_fwdj,
      n_jet_fwdj30,
      n_jet_fwdj40,
      n_jet_fwdj50,
      n_jet_cen,
      n_jet_cenj,
      n_jet_cenj30,
      n_jet_cenj40,
      n_jet_cenj50,
      n_el,
      n_mu,
      n_tau,
      n_baseel,
      n_basemu,
      n_baselep,
      n_siglep,
      n_ph,
      n_truth_tau,
      met_tst_j1_dphi,
      met_tst_j2_dphi,
      met_tst_j3_dphi,
      met_tst_nolep_j1_dphi,
      met_tst_nolep_j2_dphi,
      met_tenacious_tst_j1_dphi,
      met_tenacious_tst_j2_dphi,
      met_tenacious_tst_nolep_j1_dphi,
      met_tenacious_tst_nolep_j2_dphi,
      jetPt0,
      jetPt1,
      jetEta0,
      jetEta1,
      etaj0TimesEtaj1,
      lepPt0,
      lepPt1,
      lepCh0,
      lepCh1,
      baselepPt0,
      baselepCh0,
      chanFlavor,
      mll,
      ptll,
      mt,
      charge,
      ptvarcone20,
      ptvarcone30,
      topoetcone20,
      baselep_ptvarcone_0,
      timing,
      jvt,
      fjvt,
      j0timing,
      j1timing,
      j0jvt,
      j1jvt,
      j0fjvt,
      j1fjvt,
      TruthFilter,
      truth_jj_mass,
      FilterMet,
      truth_jj_deta,
      truthJet1Pt,
      nTruthJetMatch,
      jetPt3,
      maxCentrality,
      avgCentrality,
      phcentrality,
      maxmj3_over_mjj,
      avgmj3_over_mjj,
      max_j3_dr,
      Mtt,phPt,
      phEta,
      met_tst_ph_dphi,
      passVjetsFilter,
      passVjetsPTV,
      jetTrackWidth,
      jetTrackWidth0,
      jetTrackWidth1,
      jetNTracks,
      jetNTracks0,
      jetNTracks1,
      jetPartonTruthLabelID,
      jetPartonTruthLabelID0,
      jetPartonTruthLabelID1
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
