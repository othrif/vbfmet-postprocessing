
// C/C++
#include <iomanip>

// Local
#include "HInvPlot/Sample.h"

using namespace std;

//-----------------------------------------------------------------------------
std::string Msl::Mva::Convert2Str(Sample s)
{
  switch(s) 
    {
    case kData:  return "data";
    case kHggf:  return "hggf";
    case kHvbf:  return "hvbf";
    case kHvh:   return "hvh";            
    case kWewk:  return "wewk";      
    case kWqcd:  return "wqcd";      
    case kZewk:  return "zewk";      
    case kZqcd:  return "zqcd";      
    case kWhww:  return "whww";
    case kTthw:  return "tthw";
    case kHtau:  return "htau";
    case kHwww:  return "hwww";
    case kHzww:  return "hzww";
    case kZjet:  return "zjet";
    case kZjee:  return "zjee";
    case kZjmm:  return "zjmm";
    case kZjtt:  return "zjtt";
    case kZldy:  return "zldy";
    case kZlee:  return "zlee";
    case kZlmm:  return "zlmm";
    case kZltt:  return "zltt";
    case kZjhf:  return "zjhf";
    case kZgam:  return "zgam";
    case kZgas:  return "zgas";
    case kZvbf:  return "zvbf";
    case kZvbe:  return "zvbe";
    case kZvbm:  return "zvbm";
    case kZvbt:  return "zvbt";
    case kVbfZ:  return "vbfz";
    case kVbfZll:  return "vbfzll";
    case kVbfZtt:  return "vbfztt";
    case kVbfZl: return "vbfzl";
    case kVbfZh: return "vbfzh";
    case kWjet:  return "wjet";
    case kWjdt:  return "wjdt";
    case kWjdtm: return "wjdtm";
    case kWjdte: return "wjdte";
    case kQFlip: return "qflip";
    case kQCD:   return "dqcd";
    case kQCD_MC:   return "mqcd";
    case kWjhf:  return "wjhf";
    case kWgam:  return "wgam";
    case kWgas:  return "wgas";
    case kWZZZ:  return "wzzz";
    case kZZ:  return "zz";
    case kWZ:  return "wz";
    case kggww:  return "ggww";
    case kqqww:  return "qqww";
    case kewww:  return "ewww";
    case ktop1:  return "top1";
    case ktop2:  return "top2";
    case kWDPI:  return "wdpi";
    case kttv:   return "ttv";
    case kttg:   return "ttg";
    case kpho:   return "pho";
    case kphoAlt:   return "phoAlt";
    case kvvv:   return "vvv";
    case kJPsi:  return "jpsi";
    case kUpsl:  return "upsl";
    case kZqcdPow:  return "zqcdPow";
    case kZqcdMad:  return "zqcdMad";      
    case kWqcdMad:  return "wqcdMad";      
    default: break;
    }

  return "none";
}

//-----------------------------------------------------------------------------
std::string Msl::Mva::Convert2Std(Sample s)
{
  switch(s) 
    {
    case kData: return "Data";
    case kHggf:  return "hggf";
    case kHvbf:  return "hvbf";
    case kHvh:   return "hvh";            
    case kWewk:  return "wewk";      
    case kWqcd:  return "wqcd";      
    case kZewk:  return "zewk";      
    case kZqcd:  return "zqcd";
    case kWhww: return "HWW_wh";
    case kTthw: return "HWW_tth";
    case kHtau: return "H_tautau";
    case kHwww: return "HWW_hww";
    case kHzww: return "HWW_hwz";
    case kZjet: return "Zjets";
    case kZjee: return "Zj_ee";
    case kZjmm: return "Zj_mm";
    case kZjtt: return "Zj_tt";
    case kZldy: return "ZjetsLM";
    case kZlee: return "Zj_eeLM";
    case kZlmm: return "Zj_mmLM";
    case kZltt: return "Zj_ttLM";
    case kZjhf: return "ZjetsHF";
    case kZgam: return "Zjets_gamma";
    case kZgas: return "Zjets_gamma*";
    case kZvbf: return "ZjetsVBF_Filter";
    case kZvbe: return "Zj_eeVBF_Filter";
    case kZvbm: return "Zj_mmVBF_Filter";
    case kZvbt: return "Zj_ttVBF_Filter";
    case kVbfZ: return "VBF_Z";
    case kVbfZll: return "Zj_VBF_ll";
    case kVbfZtt: return "Zj_VBF_tautau";
    case kVbfZl: return "Zj_VBF_lomass";
    case kVbfZh: return "Zj_VBF_himass";
    case kWjet: return "Wjets";
    case kWjdt: return "Wjets_data";
    case kWjdtm: return "Wjets_data_muFake";
    case kWjdte: return "Wjets_data_eFake";
    case kQFlip: return "Charge_flip";
    case kQCD:   return "QCD";
    case kQCD_MC:   return "QCD_MC";
    case kWjhf: return "WjetsHF";
    case kWgam: return "Wgamma";
    case kWgas: return "Wgamma_star";
    case kWZZZ: return "WZ-ZZ";
    case kZZ: return "ZZ";
    case kWZ: return "WZ";
    case kggww: return "ggWW";
    case kqqww: return "qqWW";
    case kewww: return "ewWW";
    case ktop1: return "SingleTop";
    case ktop2: return "ttbar";
    case kWDPI: return "wdpi";
    case kttv:  return "ttv";
    case kttg:  return "ttg";
    case kpho:  return "pho";
    case kphoAlt:  return "phoAlt";
    case kvvv:  return "vvv";
    case kJPsi: return "jpsi";
    case kUpsl: return "upsl";
    case kZqcdPow: return "zqcdPow";
    case kZqcdMad: return "zqcdMad";
    case kWqcdMad: return "wqcdMad";            
    default: break;
    }

  return "none";
}

//-----------------------------------------------------------------------------
std::string Msl::Mva::Convert2Tex(const SampleSet &s)
{
  if(s.GetName() == "data")  return "Data";
  if(s.GetName() == "hggf")  return "HInv ggF";  
  if(s.GetName() == "hvbf")  return "HInv VBF";  
  if(s.GetName() == "hvh")   return "HInv VH";  
  if(s.GetName() == "wewk")  return "W EWK";  
  if(s.GetName() == "wqcd")  return "W QCD";
  if(s.GetName() == "zewk")  return "Z EWK";  
  if(s.GetName() == "zqcd")  return "Z QCD";    
  if(s.GetName() == "whww")  return "HWW wh";
  if(s.GetName() == "tthw")  return "HWW tth";
  if(s.GetName() == "zjet")  return "Z$+$jets";
  if(s.GetName() == "zjee")  return "Z$+$jets ee";
  if(s.GetName() == "zjuu")  return "Z$+$jets $\\mu\\mu$";
  if(s.GetName() == "zjtt")  return "Z$+$jets $\\tau\\tau$";
  if(s.GetName() == "zjhf")  return "Z$+$jets HF";
  if(s.GetName() == "zvbf")  return "Z$+$jets VBF";
  if(s.GetName() == "zall")  return "Z$+$jets";
  if(s.GetName() == "zldy")  return "Z$+$jets";
  if(s.GetName() == "wjet")  return "W$+$jets";
  if(s.GetName() == "wjdt")  return "W$+$jets data";
  if(s.GetName() == "wjdtm")  return "W$+$jets data (muon Fake)";
  if(s.GetName() == "wjdte")  return "W$+$jets data (e Fake)";
  if(s.GetName() == "qflip")  return "Charge Flip";
  if(s.GetName() == "wgam")  return "W$\\gamma$";
  if(s.GetName() == "wgas")  return "W$\\gamma$*";
  if(s.GetName() == "wzzz")  return "WZ/ZZ$";
  if(s.GetName() == "zz")    return "ZZ";
  if(s.GetName() == "wz")    return "WZ";
  if(s.GetName() == "top1")  return "SingleTop";
  if(s.GetName() == "top2")  return "$t\\bar{t}$";
  if(s.GetName() == "wdpi")  return "$WW$ DPI";
  if(s.GetName() == "ttv")   return "$t\\bar{t}+V$";
  if(s.GetName() == "ttg")   return "$t\\bar{t}+\\gamma$";
  if(s.GetName() == "pho")   return "$\\gamma$";
  if(s.GetName() == "phoAlt")   return "$\\gamma$";
  if(s.GetName() == "vvv")   return "VVV";
  if(s.GetName() == "jpsi")  return "$J/\\psi$";
  if(s.GetName() == "upsl")  return "$\\upsilon$";

  return s.GetName();
}

//-----------------------------------------------------------------------------
Msl::Mva::Sample Msl::Mva::Convert2Sample(const std::string &s)
{
  if(s == "data") return kData;
  if(s == "hggf") return kHggf;
  if(s == "hvbf") return kHvbf;
  if(s == "hvh")  return kHvh;
  if(s == "wewk") return kWewk;  
  if(s == "wqcd") return kWqcd;  
  if(s == "zewk") return kZewk;  
  if(s == "zqcd") return kZqcd;  
  if(s == "whww") return kWhww;
  if(s == "tthw") return kTthw;
  if(s == "htau") return kHtau;
  if(s == "hwww") return kHwww;
  if(s == "hzww") return kHzww;
  if(s == "zjet") return kZjet;
  if(s == "zjee") return kZjee;
  if(s == "zjmm") return kZjmm;
  if(s == "zjtt") return kZjtt;
  if(s == "zldy") return kZldy;
  if(s == "zlee") return kZlee;
  if(s == "zlmm") return kZlmm;
  if(s == "zltt") return kZltt;
  if(s == "zjhf") return kZjhf;
  if(s == "zgam") return kZgam;
  if(s == "zgas") return kZgas;
  if(s == "zvbf") return kZvbf;
  if(s == "zvbe") return kZvbe;
  if(s == "zvbm") return kZvbm;
  if(s == "zvbt") return kZvbt;
  if(s == "vbfz") return kVbfZ;
  if(s == "vbfzll") return kVbfZll;
  if(s == "vbfztt") return kVbfZtt;
  if(s == "vbfzl") return kVbfZl;
  if(s == "vbfzh") return kVbfZh;
  if(s == "wjet") return kWjet;
  if(s == "wjdt") return kWjdt;
  if(s == "wjdtm") return kWjdtm;
  if(s == "wjdte") return kWjdte;
  if(s == "qflip") return kQFlip;
  if(s == "dqcd") return kQCD;
  if(s == "mqcd") return kQCD_MC;
  if(s == "wjhf") return kWjhf;
  if(s == "wgam") return kWgam;
  if(s == "wgas") return kWgas;
  if(s == "wzzz") return kWZZZ;
  if(s == "zz") return kZZ;
  if(s == "wz") return kWZ;
  if(s == "ggww") return kggww;
  if(s == "qqww") return kqqww;
  if(s == "ewww") return kewww;
  if(s == "top1") return ktop1;
  if(s == "top2") return ktop2;
  if(s == "wdpi") return kWDPI;
  if(s == "ttv")  return kttv;
  if(s == "ttg")  return kttg;
  if(s == "pho")  return kpho;
  if(s == "phoAlt")  return kphoAlt;
  if(s == "vvv")  return kvvv;
  if(s == "jpsi") return kJPsi;
  if(s == "upsl") return kUpsl;
  if(s == "zqcdPow") return kZqcdPow;
  if(s == "zqcdMad") return kZqcdMad;  
  if(s == "wqcdMad") return kWqcdMad;  

  std::cout << "ERROR - sample " << s << " is not defined in Sample.cxx" <<std::endl;
  return kNone;
}

//-----------------------------------------------------------------------------
const std::vector<Msl::Mva::Sample>& Msl::Mva::GetAllSamples()
{
  static vector<Msl::Mva::Sample> vars;

  if(vars.empty()) {
    //
    // Fill vector with all available enums
    //
    vars.push_back(kData);
    vars.push_back(kHggf);
    vars.push_back(kHvbf);
    vars.push_back(kHvh);
    vars.push_back(kWewk);
    vars.push_back(kWqcd);
    vars.push_back(kZewk);
    vars.push_back(kZqcd);
    vars.push_back(kWhww);
    vars.push_back(kHtau);
    vars.push_back(kTthw);
    vars.push_back(kHwww);
    vars.push_back(kHzww);
    vars.push_back(kZjet);
    vars.push_back(kZjee);
    vars.push_back(kZjmm);
    vars.push_back(kZjtt);
    vars.push_back(kZldy);
    vars.push_back(kZlee);
    vars.push_back(kZlmm);
    vars.push_back(kZltt);
    vars.push_back(kZjhf);
    vars.push_back(kZgam);
    vars.push_back(kZgas);
    vars.push_back(kZvbf);
    vars.push_back(kZvbe);
    vars.push_back(kZvbm);
    vars.push_back(kZvbt);
    vars.push_back(kVbfZ);
    vars.push_back(kVbfZll);
    vars.push_back(kVbfZtt);
    vars.push_back(kVbfZl);
    vars.push_back(kVbfZh);
    vars.push_back(kWjet);
    vars.push_back(kWjdt);
    vars.push_back(kWjdtm);
    vars.push_back(kWjdte);
    vars.push_back(kQFlip);
    vars.push_back(kQCD);
    vars.push_back(kQCD_MC);
    vars.push_back(kWjhf);
    vars.push_back(kWgam);
    vars.push_back(kWgas);
    vars.push_back(kWZZZ);
    vars.push_back(kZZ);
    vars.push_back(kWZ);
    vars.push_back(kggww);
    vars.push_back(kqqww);
    vars.push_back(kewww);
    vars.push_back(ktop1);
    vars.push_back(ktop2);
    vars.push_back(kWDPI);
    vars.push_back(kttv);
    vars.push_back(kttg);
    vars.push_back(kpho);
    vars.push_back(kphoAlt);
    vars.push_back(kvvv);
    vars.push_back(kJPsi);
    vars.push_back(kUpsl);
    vars.push_back(kZqcdPow);
    vars.push_back(kZqcdMad);    
    vars.push_back(kWqcdMad);    
  }
  
  return vars;
}

//-----------------------------------------------------------------------------
Msl::Mva::SampleSet::SampleSet(Mva::Sample sample)  
{
  fName = Mva::Convert2Str(sample);
  fSamples.insert(sample);
}

//-----------------------------------------------------------------------------
void Msl::Mva::SampleSet::FillSample(const Registry &reg, const std::string &key)
{
  //
  // Fill samples from Registry holding vector of sample names
  //
  fName = key;
  vector<string> samples;
  reg.Get(key, samples);
  FillSample(samples);  
}

//-----------------------------------------------------------------------------
void Msl::Mva::SampleSet::FillSample(const std::vector<std::string> &samples)
{
  //
  // Fill samples from vector of sample names
  //
  for(unsigned i = 0; i < samples.size(); ++i) {
    const Sample sample = Convert2Sample(samples.at(i));

    if(sample != Mva::kNone) {
      fSamples.insert(sample);
    }
  }
}

//-----------------------------------------------------------------------------
void Msl::Mva::SampleSet::Print(std::ostream &os, const std::string &pad) const
{
  for(set<Mva::Sample>::const_iterator it = fSamples.begin(); it != fSamples.end(); ++it) {
    os << pad << Convert2Str(*it) << endl;
  }
}

//-----------------------------------------------------------------------------
std::vector<Msl::Mva::SampleSet> Msl::Mva::ReadSets(const Registry &reg, 
						    const std::string &key,
						    const std::string &)
{
  //
  // Read sets
  //
  vector<SampleSet> sets;
  
  //
  // Initialize cuts and sets of samples
  //
  vector<string> keys;
  reg.Get(key, keys);

  for(unsigned i = 0; i < keys.size(); ++i) {
    Mva::SampleSet s;
    //cout << keys.at(i) << endl;
    s.FillSample(reg, keys.at(i));
    //cout << " filled: " << keys.at(i) << endl;    
    if(s.GetSize() > 0) {
      sets.push_back(s);
    }
  }
  
  return sets;
}

//-----------------------------------------------------------------------------
void Msl::Mva::PrintSets(const std::string &key, 
			 const std::vector<Msl::Mva::SampleSet> &sets, 
			 std::ostream &os)
{
  //
  // Print a vector of sets
  //
  os << "   Number of " << key << ": " << sets.size() << endl;
  for(unsigned i = 0; i < sets.size(); ++i) { 
    std::cout << "   " << sets.at(i).GetName() << ":" << endl;
    sets.at(i).Print(std::cout, "      ");
  }
}

//-----------------------------------------------------------------------------
bool Msl::Mva::IsWjdt(Mva::Sample s)  
{
  switch(s) 
    {
    case kWjdte: return true;
    case kWjdtm: return true;
    case kWjdt:  return true;
      //case kQCD:   return true;
    default: break;
    }
  return false;
}

//-----------------------------------------------------------------------------
bool Msl::Mva::IsQCD(Mva::Sample s)  
{
  switch(s) 
    {
    case kQCD:   return true;
    default: break;
    }
  return false;
}

//-----------------------------------------------------------------------------
bool Msl::Mva::IsZjet(Mva::Sample s)  
{
  switch(s) 
    {
    case kZjet: return true;
    case kZjee: return true;
    case kZjmm: return true;
    case kZjtt: return true;
    default: break;
    }
  return false;
}

//-----------------------------------------------------------------------------
bool Msl::Mva::IsZldy(Mva::Sample s)  
{
  switch(s) 
    {
    case kZldy: return true;
    case kZlee: return true;
    case kZlmm: return true;
    case kZltt: return true;
    default: break;
    }
  return false;
}

//-----------------------------------------------------------------------------
bool Msl::Mva::IsZvbf(Mva::Sample s)  
{
  // these are vbf filtered z samples
  switch(s) 
    {
    case kZvbf: return true;
    case kZvbe: return true;
    case kZvbm: return true;
    case kZvbt: return true;
    default: break;
    }
  return false;
}
