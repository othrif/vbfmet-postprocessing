
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
    case trigger_met_encoded:	  return "trigger_met_encoded";
    case trigger_met_encodedv2:	  return "trigger_met_encodedv2";
    case trigger_met_byrun:	  return "trigger_met_byrun";
    case runPeriod:	          return "runPeriod";
    case trigger_lep:	          return "trigger_lep";
    case lep_trig_match:	  return "lep_trig_match";
    case passJetCleanTight:	  return "passJetCleanTight";
    case vjWeight:    return "vjWeight";
    case xeSFTrigWeight:	  return "xeSFTrigWeight";
    case xeSFTrigWeight__1up:	  return "xeSFTrigWeight__1up";
    case xeSFTrigWeight__1down:	  return "xeSFTrigWeight__1down";
    case xeSFTrigWeight_nomu:	     return "xeSFTrigWeight_nomu";
    case xeSFTrigWeight_nomu__1up:   return "xeSFTrigWeight_nomu__1up";
    case xeSFTrigWeight_nomu__1down: return "xeSFTrigWeight_nomu__1down";

    case met_truth_et:	          return "met_truth_et";
    case met_truth_phi:	          return "met_truth_phi";
    case met_tst_et:	          return "met_tst_et";
    case met_tst_cut:	          return "met_tst_cut";
    case met_tst_phi:	          return "met_tst_phi";
    case met_tst_nolep_et:	  return "met_tst_nolep_et";
    case met_tst_nolep_phi:	  return "met_tst_nolep_phi";
    case met_tenacious_tst_nolep_et:	  return "met_tenacious_tst_nolep_et";
    case met_tenacious_tst_nolep_phi:	  return "met_tenacious_tst_nolep_phi";
    case met_significance:	  return "met_significance";
    case alljet_metsig:           return "alljet_metsig";
    case metsig_tst:	          return "metsig_tst";
    case met_tenacious_tst_et:	  return "met_tenacious_tst_et";
    case met_tight_tst_et:	  return "met_tight_tst_et";
    case met_tighter_tst_et:	  return "met_tighter_tst_et";
    case met_soft_tst_et:	  return "met_soft_tst_et";
    case met_tenacious_tst_phi:	  return "met_tenacious_tst_phi";
    case met_tight_tst_phi:	  return "met_tight_tst_phi";
    case met_tighter_tst_phi:	  return "met_tighter_tst_phi";
    case met_soft_tst_phi:	  return "met_soft_tst_phi";
    case met_soft_tst_sumet:	  return "met_soft_tst_sumet";
    case met_cst_jet:	          return "met_cst_jet";
    case met_cst_tst_ratio:	  return "met_cst_tst_ratio";
    case met_cst_tst_sub:	  return "met_cst_tst_sub";
    case n_jet:	                  return "n_jet";
    case n_bjet:	          return "n_bjet";
    case n_jet_fwd:	          return "n_jet_fwd";
    case n_jet_fwdj:	          return "n_jet_fwdj";
    case n_jet_fwdj30:	          return "n_jet_fwdj30";
    case n_jet_fwdj40:	          return "n_jet_fwdj40";
    case n_jet_fwdj50:	          return "n_jet_fwdj50";
    case n_jet_cen:	          return "n_jet_cen";
    case n_jet_cenj:	          return "n_jet_cenj";
    case n_jet_cenj30:	          return "n_jet_cenj30";
    case n_jet_cenj40:	          return "n_jet_cenj40";
    case n_jet_cenj50:	          return "n_jet_cenj50";
    case n_el:	                  return "n_el";
    case n_mu:	                  return "n_mu";
    case n_tau:	                  return "n_tau";
    case n_baseel:	          return "n_baseel";
    case n_basemu:	          return "n_basemu";
    case n_mu_baseline_noOR:	  return "n_mu_baseline_noOR";
    case n_mu_w:	          return "n_mu_w";
    case n_el_w:	          return "n_el_w";
    case n_lep_w:	          return "n_lep_w";
    case n_baselep:	          return "n_baselep";
    case n_siglep:	          return "n_siglep";
    case n_ph:	                  return "n_ph";
    case n_truth_tau:	          return "n_truth_tau";
    case met_tst_j1_dphi:	  return "met_tst_j1_dphi";
    case met_tst_j2_dphi:	  return "met_tst_j2_dphi";
    case met_tst_j3_dphi:	  return "met_tst_j3_dphi";
    case met_tst_nolep_j1_dphi:	  return "met_tst_nolep_j1_dphi";
    case met_tst_nolep_j2_dphi:	  return "met_tst_nolep_j2_dphi";
    case met_tenacious_tst_j1_dphi:	  return "met_tenacious_tst_j1_dphi";
    case met_tenacious_tst_j2_dphi:	  return "met_tenacious_tst_j2_dphi";
    case met_tenacious_tst_nolep_j1_dphi: return "met_tenacious_tst_nolep_j1_dphi";
    case met_tenacious_tst_nolep_j2_dphi: return "met_tenacious_tst_nolep_j2_dphi";
    case jetPt0:	          return "jetPt0";
    case jetPt1:	          return "jetPt1";
    case jetEta0:	          return "jetEta0";
    case jetEta1:	          return "jetEta1";
    case jetHT:                   return "jetHT";
    case etaj0TimesEtaj1:	  return "etaj0TimesEtaj1";
    case lepPt0:	          return "lepPt0";
    case lepPt1:	          return "lepPt1";
    case lepCh0:	          return "lepCh0";
    case lepCh1:	          return "lepCh1";
    case baselepPt0:	      return "baselepPt0";
    case baselepCh0:	      return "baselepCh0";
    case mll:	                  return "mll";
    case ptll:	                  return "ptll";
    case mllg:	                  return "mllg";
    case ptllg:	                  return "ptllg";
    case mt:	                  return "mt";
    case averageIntPerXing:	  return "averageIntPerXing";
    case lb:	                  return "lb";
    case n_vx:	                  return "n_vx";
    case BCIDDistanceFromFront:	  return "BCIDDistanceFromFront";
    case chanFlavor:	          return "chanFlavor";
    case charge:	          return "charge";
    case ptvarcone20:	          return "ptvarcone20";
    case ptvarcone30:	          return "ptvarcone30";
    case topoetcone20:	          return "topoetcone20";
    case baselep_ptvarcone_0:	  return "baselep_ptvarcone_0";
    case timing:	          return "timing";
    case jvt:	                  return "jvt";
    case fjvt:	                  return "fjvt";
    case j0timing:	          return "j0timing";
    case j1timing:	          return "j1timing";
    case j0jvt:	                  return "j0jvt";
    case j1jvt:	                  return "j1jvt";
    case j0fjvt:	          return "j0fjvt";
    case j1fjvt:	          return "j1fjvt";
    case TruthFilter:	          return "TruthFilter";
    case truth_jj_mass:	          return "truth_jj_mass";
    case truth_max_jj_mass:	  return "truth_max_jj_mass";
    case FilterMet:	          return "FilterMet";
    case truth_jj_deta:	          return "truth_jj_deta";
    case truth_jj_dphi:	          return "truth_jj_dphi";
    case truth_j1_pt:	          return "truth_j1_pt";
    case truth_j2_pt:	          return "truth_j2_pt";
    case SherpaVTruthPt:	  return "SherpaVTruthPt";
    case truthJet1Pt:	  return "truthJet1Pt";
    case nTruthJetMatch:	  return "nTruthJetMatch";
    case jetPt3:	          return "jetPt3";
    case maxCentrality:	          return "maxCentrality";
    case avgCentrality:	          return "avgCentrality";
    case phcentrality:	          return "phcentrality";
    case maxmj3_over_mjj:	  return "maxmj3_over_mjj";
    case avgmj3_over_mjj:	  return "avgmj3_over_mjj";
    case max_j3_dr:	          return "max_j3_dr";
    case Mtt:	                  return "Mtt";
    case phPt:	                  return "phPt";
    case phEta:	                  return "phEta";
    case met_tst_ph_dphi:	  return "met_tst_ph_dphi";
    case passVjetsFilter:	  return "passVjetsFilter";
    case passVjetsFilterTauEl:	  return "passVjetsFilterTauEl";      
    case passVjetsPTV:	          return "passVjetsPTV";
    case jetBtagWeight:           return "jetBtagWeight";
    case jetTrackWidth:           return "jetTrackWidth";
    case jetTrackWidth0:          return "jetTrackWidth0";
    case jetTrackWidth1:	  return "jetTrackWidth1";
    case jetNTracks:              return "jetNTracks";
    case jetNTracks0:             return "jetNTracks0";
    case jetNTracks1:	          return "jetNTracks1";
    case jetPartonTruthLabelID:   return "jetPartonTruthLabelID";
    case jetPartonTruthLabelID0:  return "jetPartonTruthLabelID0";
    case jetPartonTruthLabelID1:  return "jetPartonTruthLabelID1";
    case tmva:                    return "tmva";
    case bcid:                    return "bcid";
    case bcidPos:                 return "bcidPos";
    case in_vy_overlap:           return "in_vy_overlap";
    case in_vy_overlapCut:        return "in_vy_overlapCut";

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
  if(var == "trigger_met_encoded")     return trigger_met_encoded;
  if(var == "trigger_met_encodedv2")   return trigger_met_encodedv2;
  if(var == "trigger_met_byrun")          return trigger_met_byrun;
  if(var == "runPeriod")          return runPeriod;
  if(var == "trigger_lep")   return trigger_lep;
  if(var == "lep_trig_match")   return lep_trig_match;
  if(var == "passJetCleanTight")   return passJetCleanTight;
  if(var == "vjWeight")   return vjWeight;
  if(var == "xeSFTrigWeight")   return xeSFTrigWeight;
  if(var == "xeSFTrigWeight__1up")   return xeSFTrigWeight__1up;
  if(var == "xeSFTrigWeight__1down")   return xeSFTrigWeight__1down;
  if(var == "xeSFTrigWeight_nomu")   return xeSFTrigWeight_nomu;
  if(var == "xeSFTrigWeight_nomu__1up")   return xeSFTrigWeight_nomu__1up;
  if(var == "xeSFTrigWeight_nomu__1down")   return xeSFTrigWeight_nomu__1down;
  if(var == "met_truth_et")    return met_truth_et;
  if(var == "met_truth_phi")    return met_truth_phi;
  if(var == "met_tst_et")    return met_tst_et;
  if(var == "met_tst_cut")    return met_tst_cut;
  if(var == "met_tst_phi")    return met_tst_phi;
  if(var == "met_tst_nolep_et")  return met_tst_nolep_et;
  if(var == "met_tst_nolep_phi")  return met_tst_nolep_phi;
  if(var == "met_tenacious_tst_nolep_et")  return met_tenacious_tst_nolep_et;
  if(var == "met_tenacious_tst_nolep_phi")  return met_tenacious_tst_nolep_phi;
  if(var == "met_significance")  return met_significance;
  if(var == "metsig_tst")          return metsig_tst;
  if(var == "alljet_metsig")       return alljet_metsig;
  if(var == "met_tenacious_tst_et")return met_tenacious_tst_et;
  if(var == "met_tight_tst_et")    return met_tight_tst_et;
  if(var == "met_tighter_tst_et")  return met_tighter_tst_et;
  if(var == "met_soft_tst_et")     return met_soft_tst_et;
  if(var == "met_tenacious_tst_phi")return met_tenacious_tst_phi;
  if(var == "met_tight_tst_phi")    return met_tight_tst_phi;
  if(var == "met_tighter_tst_phi")  return met_tighter_tst_phi;
  if(var == "met_soft_tst_phi")     return met_soft_tst_phi;
  if(var == "met_soft_tst_sumet")  return met_soft_tst_sumet;
  if(var == "met_cst_jet")         return met_cst_jet;
  if(var == "met_cst_tst_ratio")   return met_cst_tst_ratio;
  if(var == "met_cst_tst_sub")     return met_cst_tst_sub;
  if(var == "n_jet")             return n_jet;
  if(var == "n_bjet")             return n_bjet;
  if(var == "n_jet_fwd")         return n_jet_fwd;
  if(var == "n_jet_fwdj")        return n_jet_fwdj;
  if(var == "n_jet_fwdj30")        return n_jet_fwdj30;
  if(var == "n_jet_fwdj40")        return n_jet_fwdj40;
  if(var == "n_jet_fwdj50")        return n_jet_fwdj50;
  if(var == "n_jet_cen")         return n_jet_cen;
  if(var == "n_jet_cenj")        return n_jet_cenj;
  if(var == "n_jet_cenj30")        return n_jet_cenj30;
  if(var == "n_jet_cenj40")        return n_jet_cenj40;
  if(var == "n_jet_cenj50")        return n_jet_cenj50;
  if(var == "n_el")              return n_el;
  if(var == "n_mu")              return n_mu;
  if(var == "n_tau")             return n_tau;
  if(var == "n_baseel")          return n_baseel;
  if(var == "n_basemu")          return n_basemu;
  if(var == "n_mu_baseline_noOR")  return n_mu_baseline_noOR;
  if(var == "n_mu_w")              return n_mu_w;
  if(var == "n_el_w")              return n_el_w;
  if(var == "n_lep_w")              return n_lep_w;
  if(var == "n_baselep")          return n_baselep;
  if(var == "n_siglep")          return n_siglep;
  if(var == "n_ph")               return n_ph;
  if(var == "n_truth_tau")       return n_truth_tau;
  if(var == "met_tst_j1_dphi")   return met_tst_j1_dphi;
  if(var == "met_tst_j2_dphi")   return met_tst_j2_dphi;
  if(var == "met_tst_j3_dphi")   return met_tst_j3_dphi;
  if(var == "met_tst_nolep_j1_dphi")   return met_tst_nolep_j1_dphi;
  if(var == "met_tst_nolep_j2_dphi")   return met_tst_nolep_j2_dphi;
  if(var == "met_tenacious_tst_j1_dphi")       return met_tenacious_tst_j1_dphi;
  if(var == "met_tenacious_tst_j2_dphi")       return met_tenacious_tst_j2_dphi;
  if(var == "met_tenacious_tst_nolep_j1_dphi") return met_tenacious_tst_nolep_j1_dphi;
  if(var == "met_tenacious_tst_nolep_j2_dphi") return met_tenacious_tst_nolep_j2_dphi;
  if(var == "jetPt0")            return jetPt0;
  if(var == "jetPt1")            return jetPt1;
  if(var == "jetEta0")           return jetEta0;
  if(var == "jetEta1")           return jetEta1;
  if(var == "jetHT")             return jetHT;
  if(var == "etaj0TimesEtaj1")   return etaj0TimesEtaj1;
  if(var == "lepPt0")            return lepPt0;
  if(var == "lepPt1")            return lepPt1;
  if(var == "lepCh0")            return lepCh0;
  if(var == "lepCh1")            return lepCh1;
  if(var == "baselepPt0")        return baselepPt0;
  if(var == "baselepCh0")        return baselepCh0;
  if(var == "mll")               return mll;
  if(var == "ptll")              return ptll;
  if(var == "mllg")               return mllg;
  if(var == "ptllg")              return ptllg;
  if(var == "mt")                return mt;
  if(var == "averageIntPerXing") return averageIntPerXing;
  if(var == "lb")                return lb;
  if(var == "n_vx")              return n_vx;
  if(var == "BCIDDistanceFromFront") return BCIDDistanceFromFront;
  if(var == "chanFlavor")        return chanFlavor;
  if(var == "charge")            return charge;
  if(var == "ptvarcone20")       return ptvarcone20;
  if(var == "ptvarcone30")       return ptvarcone30;
  if(var == "topoetcone20")      return topoetcone20;
  if(var == "baselep_ptvarcone_0")  return baselep_ptvarcone_0;
  if(var == "timing")            return timing;
  if(var == "jvt")               return jvt;
  if(var == "fjvt")              return fjvt;
  if(var == "j0timing")          return j0timing;
  if(var == "j1timing")          return j1timing;
  if(var == "j0jvt")             return j0jvt;
  if(var == "j1jvt")             return j1jvt;
  if(var == "j0fjvt")            return j0fjvt;
  if(var == "j1fjvt")            return j1fjvt;
  if(var == "TruthFilter")       return TruthFilter;
  if(var == "truth_jj_mass")     return truth_jj_mass;
  if(var == "truth_max_jj_mass") return truth_max_jj_mass;  
  if(var == "FilterMet")         return FilterMet;
  if(var == "truth_jj_deta")     return truth_jj_deta;
  if(var == "truth_jj_dphi")     return truth_jj_dphi;
  if(var == "truth_j1_pt")       return truth_j1_pt;
  if(var == "truth_j2_pt")       return truth_j2_pt;
  if(var == "SherpaVTruthPt")    return SherpaVTruthPt;
  if(var == "truthJet1Pt")       return truthJet1Pt;
  if(var == "nTruthJetMatch")    return nTruthJetMatch;
  if(var == "jetPt3")	         return jetPt3;
  if(var == "maxCentrality")	 return maxCentrality;
  if(var == "avgCentrality")	 return avgCentrality;
  if(var == "phcentrality")	 return phcentrality;
  if(var == "maxmj3_over_mjj")	 return maxmj3_over_mjj;
  if(var == "avgmj3_over_mjj")	 return avgmj3_over_mjj;
  if(var == "max_j3_dr")	 return max_j3_dr;
  if(var == "Mtt")	         return Mtt;
  if(var == "phPt")	         return phPt;
  if(var == "phEta")	         return phEta;
  if(var == "met_tst_ph_dphi")	 return met_tst_ph_dphi;
  if(var == "passVjetsFilter")	 return passVjetsFilter;
  if(var == "passVjetsFilterTauEl") return passVjetsFilterTauEl;  
  if(var == "passVjetsPTV")	 return passVjetsPTV;
  if(var == "jetBtagWeight")     return jetBtagWeight;
  if(var == "jetTrackWidth")     return jetTrackWidth;
  if(var == "jetTrackWidth0")    return jetTrackWidth0;
  if(var == "jetTrackWidth1")    return jetTrackWidth1;
  if(var == "jetNTracks")        return jetNTracks;
  if(var == "jetNTracks0")       return jetNTracks0;
  if(var == "jetNTracks1")	 return jetNTracks1;
  if(var == "jetPartonTruthLabelID") return jetPartonTruthLabelID;
  if(var == "jetPartonTruthLabelID0") return jetPartonTruthLabelID0;
  if(var == "jetPartonTruthLabelID1") return jetPartonTruthLabelID1;
  if(var == "tmva")                   return tmva;
  if(var == "bcid")                   return bcid;
  if(var == "bcidPos")                return bcidPos;
  if(var == "in_vy_overlap")          return in_vy_overlap;
  if(var == "in_vy_overlapCut")       return in_vy_overlapCut;

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
  const vector<Var>::const_iterator vit = std::find(vars.begin(), vars.end(), Convert2Var(key));

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
    vars.push_back(trigger_met_encoded);
    vars.push_back(trigger_met_encodedv2);
    vars.push_back(trigger_met_byrun);
    vars.push_back(runPeriod);
    vars.push_back(trigger_lep);
    vars.push_back(lep_trig_match);
    vars.push_back(passJetCleanTight);
    vars.push_back(vjWeight);
    vars.push_back(xeSFTrigWeight);
    vars.push_back(xeSFTrigWeight__1up);
    vars.push_back(xeSFTrigWeight__1down);
    vars.push_back(xeSFTrigWeight_nomu);
    vars.push_back(xeSFTrigWeight_nomu__1up);
    vars.push_back(xeSFTrigWeight_nomu__1down);

    vars.push_back(met_truth_et);
    vars.push_back(met_truth_phi);
    vars.push_back(met_tst_et);
    vars.push_back(met_tst_cut);
    vars.push_back(met_tst_phi);
    vars.push_back(met_tst_nolep_et);
    vars.push_back(met_tst_nolep_phi);
    vars.push_back(met_tenacious_tst_nolep_et);
    vars.push_back(met_tenacious_tst_nolep_phi);
    vars.push_back(met_significance);
    vars.push_back(metsig_tst);
    vars.push_back(alljet_metsig);
    vars.push_back(met_tenacious_tst_et);
    vars.push_back(met_tight_tst_et);
    vars.push_back(met_tighter_tst_et);
    vars.push_back(met_soft_tst_et);
    vars.push_back(met_tenacious_tst_phi);
    vars.push_back(met_tight_tst_phi);
    vars.push_back(met_tighter_tst_phi);
    vars.push_back(met_soft_tst_phi);
    vars.push_back(met_soft_tst_sumet);
    vars.push_back(met_cst_jet);
    vars.push_back(met_cst_tst_ratio);
    vars.push_back(met_cst_tst_sub);
    vars.push_back(n_jet);
    vars.push_back(n_bjet);
    vars.push_back(n_jet_fwd);
    vars.push_back(n_jet_fwdj);
    vars.push_back(n_jet_fwdj30);
    vars.push_back(n_jet_fwdj40);
    vars.push_back(n_jet_fwdj50);
    vars.push_back(n_jet_cen);
    vars.push_back(n_jet_cenj);
    vars.push_back(n_jet_cenj30);
    vars.push_back(n_jet_cenj40);
    vars.push_back(n_jet_cenj50);
    vars.push_back(n_el);
    vars.push_back(n_mu);
    vars.push_back(n_tau);
    vars.push_back(n_baseel);
    vars.push_back(n_basemu);
    vars.push_back(n_mu_baseline_noOR);
    vars.push_back(n_mu_w);
    vars.push_back(n_el_w);
    vars.push_back(n_lep_w);
    vars.push_back(n_baselep);
    vars.push_back(n_siglep);
    vars.push_back(n_ph);
    vars.push_back(n_truth_tau);
    vars.push_back(met_tst_j1_dphi);
    vars.push_back(met_tst_j2_dphi);
    vars.push_back(met_tst_j3_dphi);
    vars.push_back(met_tst_nolep_j1_dphi);
    vars.push_back(met_tst_nolep_j2_dphi);
    vars.push_back(met_tenacious_tst_j1_dphi);
    vars.push_back(met_tenacious_tst_j2_dphi);
    vars.push_back(met_tenacious_tst_nolep_j1_dphi);
    vars.push_back(met_tenacious_tst_nolep_j2_dphi);
    vars.push_back(jetPt0);
    vars.push_back(jetPt1);
    vars.push_back(jetEta0);
    vars.push_back(jetEta1);
    vars.push_back(jetHT);
    vars.push_back(etaj0TimesEtaj1);
    vars.push_back(lepPt0);
    vars.push_back(lepPt1);
    vars.push_back(lepCh0);
    vars.push_back(lepCh1);
    vars.push_back(baselepPt0);
    vars.push_back(baselepCh0);
    vars.push_back(mll);
    vars.push_back(ptll);
    vars.push_back(mllg);
    vars.push_back(ptllg);    
    vars.push_back(mt);
    vars.push_back(averageIntPerXing);
    vars.push_back(lb);
    vars.push_back(n_vx);
    vars.push_back(BCIDDistanceFromFront);
    vars.push_back(chanFlavor);
    vars.push_back(charge);
    vars.push_back(ptvarcone20);
    vars.push_back(ptvarcone30);
    vars.push_back(topoetcone20);
    vars.push_back(baselep_ptvarcone_0);
    vars.push_back(timing);
    vars.push_back(jvt);
    vars.push_back(fjvt);
    vars.push_back(j0timing);
    vars.push_back(j1timing);
    vars.push_back(j0jvt);
    vars.push_back(j1jvt);
    vars.push_back(j0fjvt);
    vars.push_back(j1fjvt);
    vars.push_back(TruthFilter);
    vars.push_back(truth_jj_mass);
    vars.push_back(truth_max_jj_mass);    
    vars.push_back(FilterMet);
    vars.push_back(truth_jj_deta);
    vars.push_back(truth_jj_dphi);
    vars.push_back(truth_j1_pt);        
    vars.push_back(truth_j2_pt);
    vars.push_back(SherpaVTruthPt);
    vars.push_back(truthJet1Pt);
    vars.push_back(nTruthJetMatch);
    vars.push_back(jetPt3);
    vars.push_back(maxCentrality);
    vars.push_back(avgCentrality);
    vars.push_back(phcentrality);
    vars.push_back(maxmj3_over_mjj);
    vars.push_back(avgmj3_over_mjj);
    vars.push_back(max_j3_dr);
    vars.push_back(Mtt);
    vars.push_back(phPt);
    vars.push_back(phEta);
    vars.push_back(met_tst_ph_dphi);
    vars.push_back(passVjetsFilter);
    vars.push_back(passVjetsFilterTauEl);    
    vars.push_back(passVjetsPTV);
    vars.push_back(jetBtagWeight);
    vars.push_back(jetTrackWidth);
    vars.push_back(jetTrackWidth0);
    vars.push_back(jetTrackWidth1);
    vars.push_back(jetNTracks);
    vars.push_back(jetNTracks0);
    vars.push_back(jetNTracks1);
    vars.push_back(jetPartonTruthLabelID);
    vars.push_back(jetPartonTruthLabelID0);
    vars.push_back(jetPartonTruthLabelID1);
    vars.push_back(tmva);
    vars.push_back(bcid);
    vars.push_back(bcidPos);
    vars.push_back(in_vy_overlap);
    vars.push_back(in_vy_overlapCut);
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
