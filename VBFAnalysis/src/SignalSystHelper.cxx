#include <iostream>
#include <sstream>
#include <map>
#include <iostream>
#include <iomanip>
#include <numeric>
#include <cmath>
#include "SignalSystHelper.h"

SignalSystHelper::SignalSystHelper() {}

SignalSystHelper::~SignalSystHelper() {}

void SignalSystHelper::initialize(){

  // STXS bin definition can be found in the HXSWG gitlab respository:
  // https://gitlab.cern.ch/LHCHIGGSXS/LHCHXSWG2/STXS/blob/master/HiggsTemplateCrossSections.h
  // bin acceptances extracted from POWHEG VBFH (NLO) + PYTHIA8 for showering
  // note that the dipoleShower option in pythia8 is turned on 
  std::map<int, std::vector<double> > stxs_acc =
    {//STXS   TOT   ,  PTH200,  Mjj60 , Mjj120 , Mjj350 , Mjj700 ,Mjj1000 ,Mjj1500  ,  25       , JET01
      { 200 , {0.07  ,  0     , 0      , 0      , 0      , 0      , 0      , 0       ,        0  ,    0   }},
      { 201 , {0.0744,  0     , 0      , 0      , 0      , 0      , 0      , 0       ,        0  ,-0.1649 }}, // Jet0
      { 202 , {0.3367,  0     , 0      , 0      , 0      , 0      , 0      , 0       ,        0  ,-0.7464 }}, // Jet1
      { 203 , {0.0092,  0     ,-0.6571 , 0      , 0      , 0      , 0      , 0       ,   -0.0567 ,  0.0178}}, // Mjj 0-60,      PTHjj 0-25
   { 204 , {0.0143,  0     , 0.0282 ,-0.5951 , 0      , 0      , 0      , 0       ,   -0.0876 ,  0.0275}}, // Mjj 60-120,    PTHjj 0-25
   { 205 , {0.0455,  0     , 0.0902 , 0.0946 ,-0.3791 , 0      , 0      , 0       ,   -0.2799 ,  0.0877}}, // Mjj 120-350,   PTHjj 0-25
   { 206 , {0.0048,  0     ,-0.3429 , 0      , 0      , 0      , 0      , 0       ,   +0.0567 ,  0.0093}}, // Mjj 0-60,      PTHjj 25-inf
   { 207 , {0.0097,  0     , 0.0192 ,-0.4049 , 0      , 0      , 0      , 0       ,   +0.0876 ,  0.0187}}, // Mjj 60-120,    PTHjj 25-inf
   { 208 , {0.0746,  0     , 0.1477 , 0.0155 ,-0.6209 , 0      , 0      , 0       ,   +0.2799 ,  0.1437}}, // Mjj 120-350,   PTHjj 25-inf
   { 209 , {0.0375, 0.1166 , 0.0743 , 0.078  , 0.1039 ,-0.2757 , 0      , 0       ,   -0.2306 ,  0.0723}}, // Mjj 350-700,   PTHjj 0-25    , pTH 0-200
   { 210 , {0.0985, 0.3062 , 0.1951 , 0.2048 , 0.273  ,-0.7243 , 0      , 0       ,   +0.2306 ,  0.1898}}, // Mjj 350-700,   PTHjj 25-inf  , pTH 0-200
   { 211 , {0.0166, 0.0515 , 0.0328 , 0.0345 , 0.0459 , 0.0773 ,-0.2473 , 0       ,   -0.1019 ,  0.0319}}, // Mjj 700-1000,  PTHjj 0-25    , pTH 0-200
   { 212 , {0.0504, 0.1568 , 0.0999 , 0.1049 , 0.1398 , 0.2353 ,-0.7527 , 0       ,   +0.1019 ,  0.0972}}, // Mjj 700-1000,  PTHjj 25-inf  , pTH 0-200
   { 213 , {0.0137, 0.0426 , 0.0271 , 0.0285 , 0.0379 , 0.0639 , 0.0982 ,-0.2274  ,   -0.0842 ,  0.0264}}, // Mjj 1000-1500, PTHjj 0-25    , pTH 0-200
   { 214 , {0.0465, 0.1446 , 0.0922 , 0.0967 , 0.1289 , 0.2171 , 0.3335 ,-0.7726  ,   +0.0842 ,  0.0897}}, // Mjj 1000-1500, PTHjj 25-inf  , pTH 0-200
   { 215 , {0.0105, 0.0327 , 0.0208 , 0.0219 , 0.0291 , 0.0491 , 0.0754 , 0.1498  ,   -0.0647 ,  0.0203}}, // Mjj 1500-inf , PTHjj 0-25    , pTH 0-200
   { 216 , {0.048 , 0.1491 , 0.095  , 0.0998 , 0.133  , 0.2239 , 0.344  , 0.6836  ,   +0.0647 ,  0.0925}}, // Mjj 1500-inf , PTHjj 25-inf  , pTH 0-200
   { 217 , {0.0051,-0.1304 , 0.0101 , 0.0106 , 0.0141 , 0.0238 , 0.0366 , 0.0727  ,   -0.0314 ,  0.0098}}, // Mjj 350-700,   PTHjj 0-25    , pTH 200-inf
   { 218 , {0.0054,-0.1378 , 0.0107 , 0.0112 , 0.0149 , 0.0251 , 0.0386 , 0.0768  ,   +0.0314 ,  0.0104}}, // Mjj 350-700,   PTHjj 25-inf  , pTH 200-inf
   { 219 , {0.0032,-0.0816 , 0.0063 , 0.0066 , 0.0088 , 0.0149 , 0.0229 , 0.0455  ,   -0.0196 ,  0.0062}}, // Mjj 700-1000,  PTHjj 0-25    , pTH 200-inf
   { 220 , {0.0047,-0.1190 , 0.0092 , 0.0097 , 0.0129 , 0.0217 , 0.0334 , 0.0663  ,   +0.0196 ,  0.0090}}, // Mjj 700-1000,  PTHjj 25-inf  , pTH 200-inf
   { 221 , {0.0034,-0.0881 , 0.0068 , 0.0072 , 0.0096 , 0.0161 , 0.0247 , 0.0491  ,   -0.0212 ,  0.0066}}, // Mjj 1000-1500, PTHjj 0-25    , pTH 200-inf
   { 222 , {0.0056,-0.1440 , 0.0112 , 0.0117 , 0.0156 , 0.0263 , 0.0404 , 0.0802  ,   +0.0212 ,  0.0109}}, // Mjj 1000-1500, PTHjj 25-inf  , pTH 200-inf
   { 223 , {0.0036,-0.0929 , 0.0072 , 0.0076 , 0.0101 , 0.0169 , 0.026  , 0.0518  ,   -0.0223 ,  0.0070}}, // Mjj 1500-inf , PTHjj 0-25    , pTH 200-inf
   { 224 , {0.0081,-0.2062 , 0.016  , 0.0168 , 0.0223 , 0.0376 , 0.0578 , 0.1149  ,   +0.0223 ,  0.0155}}  // Mjj 1500-inf , PTHjj 25-inf  , pTH 200-inf
};
  m_stxs_acc = stxs_acc;

  // uncertainty sources extracted from proVBF NNLO
  // 10 nuissances:  1 x yield, 1 x 3rd jet veto, 6 x Mjj cuts, 1 x 01->2 jetBin, 1 x PTH cut
  //+--------------------+--------+-------+-------+--------+--------+--------+---------+---------+--------+--------+
  //|                    |  tot   |  200  | Mjj60 | Mjj120 | Mjj350 | Mjj700 | Mjj1000 | Mjj1500 |   25   |  2jet  |
  //+--------------------+--------+-------+-------+--------+--------+--------+---------+---------+--------+--------+
  //|   DELTA (POWHEG)   | 14.872 | 1.275 | 6.421 | 5.572  | 3.516  | 7.881  |  5.721  |  4.579  |  4.66  | 1.866  |
  //|     DELTA (FO)     | 14.867 | 0.394 | 9.762 | 6.788  | 7.276  | 3.645  |  2.638  |  1.005  | 20.073 | 18.094 |
  //+--------------------+--------+-------+-------+--------+--------+--------+---------+---------+--------+--------+
  std::vector<double> uncert_deltas({14.867, 0.394, 9.762, 6.788, 7.276, 3.645, 2.638, 1.005, 20.073, 18.094});
  m_uncert_deltas = uncert_deltas;
  // cross sections from different STXS bins
  // prediction at NLO from POWEHG VBFH + PYTHIA8(dipoleShower=on)
  
  std::map<int, double> powheg_xsec
  {{200,  273.952 },
   {201,  291.030 },
   {202, 1317.635 },
   {203,   36.095 },
   {204,   55.776 },
   {205,  178.171 },
   {206,   18.839 },
   {207,   37.952 },
   {208,  291.846 },
   {209,  146.782 },
   {210,  385.566 },
   {211,   64.859 },
   {212,  197.414 },
   {213,   53.598 },
   {214,  182.107 },
   {215,   41.167 },
   {216,  187.823 },
   {217,   19.968 },
   {218,   21.092 },
   {219,   12.496 },
   {220,   18.215 },
   {221,   13.490 },
   {222,   22.044 },
   {223,   14.220 },
   {224,   31.565 }};
  m_powheg_xsec = powheg_xsec;

  std::vector<std::string> m_selection({"tot","200","Mjj60","Mjj120","Mjj350","Mjj700","Mjj1000","Mjj1500","2jet"});
}

std::string SignalSystHelper::getVBFVarName(int selection){
  //(production mode VBF, ggF)_(STXS grouping qqH, etc)_(selection)
  return std::string("VBF_qqH_"+m_selection.at(selection));
}

// set VBF vars
void SignalSystHelper::setVBFVars(std::map<TString, Float_t> &tMapFloat, int category, std::vector<Float_t>* mcEventWeights){
  // add the VBF scale variations
  for(unsigned i=0; i<10; ++i){
    tMapFloat[getVBFVarName(i)+"__1up"]=vbf_uncert_stage_1_1(i,category,1.0);
  }

  // S-T jet veto
  tMapFloat["VBF_qqH_STJetVeto__1up"]=1.03;  
  tMapFloat["VBF_qqH_STJetVeto34__1up"]=1.05;

  if(!mcEventWeights && mcEventWeights->size()<169)
    std::cout << "SignalSystHelper::setVBFVars - Unknown event weights! " << std::endl;
  // value is 0
  unsigned DefaultVal=109;
  if(mcEventWeights->at(DefaultVal)!=0.0) return;
  
  // PDF variations for 90401 nloPDF with 30 variations
  for(unsigned i=1; i<31; ++i){
    tMapFloat["ATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up"]=mcEventWeights->at(DefaultVal+i)/mcEventWeights->at(DefaultVal);
  }
  // ATLAS_PDF4LHC_NLO_30_alphaS up 31 and down 32
  tMapFloat["ATLAS_PDF4LHC_NLO_30_alphaS__1up"]=mcEventWeights->at(DefaultVal+31)/mcEventWeights->at(DefaultVal);
  tMapFloat["ATLAS_PDF4LHC_NLO_30_alphaS__1down"]=mcEventWeights->at(DefaultVal+32)/mcEventWeights->at(DefaultVal);
}

// set ggF vars
void SignalSystHelper::setggFVars(std::map<TString, Float_t> &tMapFloat, std::vector<Float_t>* mcEventWeights){

  if(!mcEventWeights && mcEventWeights->size()<200)
    std::cout << "SignalSystHelper::setVBFVars - Unknown event weights! " << std::endl;
  // value is 0
  unsigned DefaultVal=111;
  if(mcEventWeights->at(DefaultVal)!=0.0) return;
  
  // PDF variations for 90401 nloPDF with 30 variations
  for(unsigned i=1; i<31; ++i){
    tMapFloat["ATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up"]=mcEventWeights->at(DefaultVal+i)/mcEventWeights->at(DefaultVal);
  }
  // ATLAS_PDF4LHC_NLO_30_alphaS up 31 and down 32
  tMapFloat["ATLAS_PDF4LHC_NLO_30_alphaS__1up"]=mcEventWeights->at(DefaultVal+31)/mcEventWeights->at(DefaultVal);
  tMapFloat["ATLAS_PDF4LHC_NLO_30_alphaS__1down"]=mcEventWeights->at(DefaultVal+32)/mcEventWeights->at(DefaultVal);
  
}

// create variations
void SignalSystHelper::initggFVars(std::map<TString, Float_t> &tMapFloat, std::map<TString, Float_t> &tMapFloatW, TTree *tree){
  std::string var_name = "";
  // add the ggF PDF variations
  for(unsigned i=1; i<31; ++i){    
    tMapFloat["ATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up"]=1.0;
    tMapFloatW["ATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up"]=1.0;
    var_name="wATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up";
    tree->Branch(var_name.c_str(),&(tMapFloatW["ATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up"]));
  }
  // ATLAS_PDF4LHC_NLO_30_alphaS up 31 and down 32
  tMapFloat["ATLAS_PDF4LHC_NLO_30_alphaS__1up"]=1.0;
  tMapFloatW["ATLAS_PDF4LHC_NLO_30_alphaS__1up"]=1.0;
  tree->Branch("wATLAS_PDF4LHC_NLO_30_alphaS__1up",&(tMapFloatW["ATLAS_PDF4LHC_NLO_30_alphaS__1up"]));
  tMapFloat["ATLAS_PDF4LHC_NLO_30_alphaS__1down"]=1.0;
  tMapFloatW["ATLAS_PDF4LHC_NLO_30_alphaS__1down"]=1.0;
  tree->Branch("wATLAS_PDF4LHC_NLO_30_alphaS__1down",&(tMapFloatW["ATLAS_PDF4LHC_NLO_30_alphaS__1down"]));
}

// create variations
void SignalSystHelper::initVBFVars(std::map<TString, Float_t> &tMapFloat, std::map<TString, Float_t> &tMapFloatW, TTree *tree){
  std::string var_name = "";
  // add the VBF scale variations
  for(unsigned i=0; i<10; ++i){
    tMapFloat[getVBFVarName(i)+"__1up"]=1.0;
    tMapFloatW[getVBFVarName(i)+"__1up"]=1.0;
    var_name = "w"+getVBFVarName(i)+"__1up";
    tree->Branch(var_name.c_str(),&(tMapFloatW[getVBFVarName(i)+"__1up"]));
  }
  // S-T jet veto nj=2
  tMapFloat["VBF_qqH_STJetVeto__1up"]=1.0;
  tMapFloatW["VBF_qqH_STJetVeto__1up"]=1.0;  
  tree->Branch("wVBF_qqH_STJetVeto__1up",&(tMapFloatW["wVBF_qqH_STJetVeto__1up"]));
  // S-T jet veto nj=3,4
  tMapFloat["VBF_qqH_STJetVeto34__1up"]=1.0;
  tMapFloatW["VBF_qqH_STJetVeto34__1up"]=1.0;
  tree->Branch("wVBF_qqH_STJetVeto34__1up",&(tMapFloatW["wVBF_qqH_STJetVeto34__1up"]));

  // add the VBF PDF variations
  for(unsigned i=1; i<31; ++i){    
    tMapFloat["ATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up"]=1.0;
    tMapFloatW["ATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up"]=1.0;
    var_name="wATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up";
    tree->Branch(var_name.c_str(),&(tMapFloatW["ATLAS_PDF4LHC_NLO_30_EV"+std::to_string(i)+"__1up"]));
  }
  // ATLAS_PDF4LHC_NLO_30_alphaS up 31 and down 32
  tMapFloat["ATLAS_PDF4LHC_NLO_30_alphaS__1up"]=1.0;
  tMapFloatW["ATLAS_PDF4LHC_NLO_30_alphaS__1up"]=1.0;
  tree->Branch("wATLAS_PDF4LHC_NLO_30_alphaS__1up",&(tMapFloatW["ATLAS_PDF4LHC_NLO_30_alphaS__1up"]));
  tMapFloat["ATLAS_PDF4LHC_NLO_30_alphaS__1down"]=1.0;
  tMapFloatW["ATLAS_PDF4LHC_NLO_30_alphaS__1down"]=1.0;
  tree->Branch("wATLAS_PDF4LHC_NLO_30_alphaS__1down",&(tMapFloatW["ATLAS_PDF4LHC_NLO_30_alphaS__1down"]));
  
}

// Propagation function
double SignalSystHelper::vbf_uncert_stage_1_1(int source, int event_STXS, double Nsigma){
  // return a single weight for a given souce
  if(source < 10){
    double delta_var = m_stxs_acc[event_STXS][source] * m_uncert_deltas[source];
    return  1.0 + Nsigma * (delta_var/m_powheg_xsec[event_STXS]);
  }else{
    return 0.0;
  }
}
