#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
import ROOT
import math
import sys

parser = argparse.ArgumentParser( description = " MJ root", add_help=True , fromfile_prefix_chars='@')
parser.add_argument("--input", dest='input', default='mj2017.root', help="Input")
parser.add_argument("--output", dest='output', default='foutLoose2017_skim.root', help="output")
args, unknown = parser.parse_known_args()

def GetPUProb(jet_pt, jet_eta, jet_jvt, avgmu, jet_fjvt):
    unc=0.0
    if abs(jet_eta)<2.4:
        if jet_pt<30:
            if jet_jvt<0.11:      unc = 1;
            elif jet_jvt<0.25: unc = 0.0730 + 0.0024 * avgmu + 0.00001 * avgmu * avgmu;
            elif jet_jvt<0.85: unc = 0.0995 + 0.0031 * avgmu + 0.00005 * avgmu * avgmu;
            elif jet_jvt<0.95: unc = 0.0311 + 0.0025 * avgmu + 0.00005 * avgmu * avgmu;
            else:  unc = 0.0308 -0.0010 * avgmu + 0.00006 * avgmu * avgmu ;
        elif jet_pt<40:
            if jet_jvt<0.11:      unc = 1.;
            elif jet_jvt<0.25: unc = 1.;
            elif jet_jvt<0.85: unc = -0.0188 + 0.0039 * avgmu + 0.00002 * avgmu * avgmu;
            elif jet_jvt<0.95: unc = 0.0252 -0.0009 * avgmu + 0.00006 * avgmu * avgmu  ;
            else:                  unc = 0.0085 -0.0003 * avgmu + 0.00002 * avgmu * avgmu  ;
        elif jet_pt<50:
            if jet_jvt<0.11:      unc = 1;
            elif jet_jvt<0.25: unc = 0.0345 -0.0006 * avgmu + 0.00004 * avgmu * avgmu  ;
            elif jet_jvt<0.85: unc = 0.1078 -0.0051 * avgmu + 0.00011 * avgmu * avgmu  ;
            elif jet_jvt<0.95: unc = -0.0026 + 0.0005 * avgmu + 0.00002 * avgmu * avgmu;
            else:                  unc = 0.0090 -0.0004 * avgmu + 0.00001 * avgmu * avgmu  ;
        elif jet_pt<60:
            if jet_jvt<0.11:      unc = 1;
            elif jet_jvt<0.25: unc = -0.0321 + 0.0030 * avgmu -0.00002 * avgmu * avgmu;
            elif jet_jvt<0.85: unc = 0.0260 -0.0007 * avgmu + 0.00003 * avgmu * avgmu ;
            else:                  unc = -0.0040 + 0.0003 * avgmu;
        elif jet_pt<100:
            unc = 0.9492 -2.0757 * jet_jvt + 1.13328 * jet_jvt * jet_jvt;
        elif jet_pt<150:
            unc = 0.7888 -1.8372 * jet_jvt + 1.05539 * jet_jvt * jet_jvt;
    elif jet_eta<2.6:
        if jet_pt<30:
            if jet_jvt<0.11:      unc = 0.2633 + 0.0091 * avgmu + -0.00009 * avgmu * avgmu;
            elif jet_jvt<0.25: unc = 0.1841 + 0.0144 * avgmu + -0.00008 * avgmu * avgmu;
            elif jet_jvt<0.85: unc = 0.1401 + 0.0048 * avgmu + 0.00006 * avgmu * avgmu ;
            elif jet_jvt<0.95: unc = -0.0118 + 0.0076 * avgmu + 0.00003 * avgmu * avgmu;
            else:              unc = 0.0534 + -0.0011 * avgmu + 0.00010 * avgmu * avgmu;
        elif jet_pt<40:
            if jet_jvt<0.11:      unc = 0.1497 + 0.0133 * avgmu + -0.00015 * avgmu * avgmu  ;
            elif jet_jvt<0.25: unc = -0.2260 + 0.0276 * avgmu + -0.00021 * avgmu * avgmu ;
            elif jet_jvt<0.85: unc = 0.2743 + -0.0093 * avgmu + 0.00022 * avgmu * avgmu  ;
            elif jet_jvt<0.95: unc = 0.0604 + 0.0006 * avgmu + 0.00006 * avgmu * avgmu   ;
            else:                  unc = 0.0478 + -0.0009 * avgmu + 0.00004 * avgmu * avgmu  ;
        elif jet_pt<50:
            if jet_jvt<0.11:      unc = -0.2187 + 0.0317 * avgmu + -0.00037 * avgmu * avgmu ;
            elif jet_jvt<0.25: unc = 0.0964 + 0.0053 * avgmu + 0.00002 * avgmu * avgmu   ;
            elif jet_jvt<0.85: unc = 1.1730 + -0.0624 * avgmu + 0.00088 * avgmu * avgmu  ;
            elif jet_jvt<0.95: unc = -0.2011 + 0.0151 * avgmu + -0.00018 * avgmu * avgmu ;
            else:                  unc = 0.0145 + -0.0003 * avgmu + 0.00002 * avgmu * avgmu  ;
        elif jet_pt<60:
            if jet_jvt<0.11:      unc = 0.0051 + 0.0113 * avgmu + -0.00008 * avgmu * avgmu  ;
            elif jet_jvt<0.25: unc = -0.1024 + 0.0109 * avgmu + -0.00006 * avgmu * avgmu ;
            elif jet_jvt<0.85: unc = 1.2491 + -0.0501 * avgmu + 0.00052 * avgmu * avgmu  ;
            else:                  unc = 0.0267 + -0.0014 * avgmu + 0.00003 * avgmu * avgmu  ;
        elif jet_pt<100:
            unc = 0.8951 -2.4995 * jet_jvt + 1.63229 * jet_jvt * jet_jvt;
        elif jet_pt<150:
            unc = 0.9998 -1.7319 * jet_jvt + 0.72680 * jet_jvt * jet_jvt;
    elif jet_eta<2.7:
        if jet_pt<30:
            if jet_jvt<0.11:      unc = 0.3001 + 0.0054 * avgmu -0.00004 * avgmu * avgmu  ;
            elif jet_jvt<0.25: unc = 0.0663 + 0.0198 * avgmu -0.00013 * avgmu * avgmu  ;
            elif jet_jvt<0.85: unc = -0.0842 + 0.0163 * avgmu -0.00008 * avgmu * avgmu ;
            elif jet_jvt<0.95: unc = -0.0219 + 0.0080 * avgmu + 0.00003 * avgmu * avgmu;
            else:                  unc = 0.0461 -0.0003 * avgmu + 0.00012 * avgmu * avgmu  ;
        elif jet_pt<40:
            if jet_jvt<0.11:      unc = 0.1885 + 0.0083 * avgmu -0.00006 * avgmu * avgmu ;
            elif jet_jvt<0.25: unc = -0.0286 + 0.0150 * avgmu -0.00007 * avgmu * avgmu;
            elif jet_jvt<0.85: unc = 0.0152 + 0.0028 * avgmu + 0.00005 * avgmu * avgmu;
            elif jet_jvt<0.95: unc = 0.1815 -0.0076 * avgmu + 0.00018 * avgmu * avgmu ;
            else:                  unc = 0.0192 -0.0003 * avgmu + 0.00007 * avgmu * avgmu ;
        elif jet_pt<50:
            if jet_jvt<0.11:      unc = 0.1257 + 0.0074 * avgmu -0.00004 * avgmu * avgmu  ;
            elif jet_jvt<0.25: unc = -0.0276 + 0.0080 * avgmu + 0.00000 * avgmu * avgmu;
            elif jet_jvt<0.85: unc = 0.1403 -0.0051 * avgmu + 0.00009 * avgmu * avgmu  ;
            elif jet_jvt<0.95: unc = 0.2078 -0.0101 * avgmu + 0.00017 * avgmu * avgmu  ;
            else:                  unc = 0.2597 -0.0132 * avgmu + 0.00020 * avgmu * avgmu  ;
        elif jet_pt<60:
            if jet_jvt<0.11:      unc = 0.1111 + 0.0045 * avgmu -0.00000 * avgmu * avgmu ;
            elif jet_jvt<0.25: unc = 0.0975 -0.0011 * avgmu + 0.00008 * avgmu * avgmu ;
            elif jet_jvt<0.85: unc = 0.0920 -0.0053 * avgmu + 0.00013 * avgmu * avgmu ;
            else:                  unc = -0.0071 + 0.0016 * avgmu -0.00001 * avgmu * avgmu;
        elif jet_pt<100:
            unc = 0.4660 -1.2116 * jet_jvt + 0.78807 * jet_jvt * jet_jvt;
        elif jet_pt<150:
            unc = 0.2254 -0.5476 * jet_jvt + 0.32617 * jet_jvt * jet_jvt;
    #} end eta 2.7
    else: #forward jets
        fjvt = jet_fjvt; 
        if jet_fjvt>0.6:
            fjvt= 0.6; # the pileup more or less plateaus at 0.6
        if jet_pt<30:       unc = 0.5106 + 1.2566 * fjvt -1.15060  * fjvt * fjvt;
        elif jet_pt<40:  unc = 0.2972 + 1.9418 * fjvt -1.82694  * fjvt * fjvt;
        elif jet_pt<50:  unc = 0.1543 + 1.9864 * fjvt -1.48429  * fjvt * fjvt;
        elif jet_pt<60:  unc = 0.1050 + 1.3196 * fjvt + 0.03554 * fjvt * fjvt;
        elif jet_pt<120: unc = 0.0400 + 0.5653 * fjvt + 1.96323 * fjvt * fjvt;
        # max of 0.9 seems reasonable
        if jet_fjvt>0.6: unc = 0.9; 

    unc = min(unc, 1.0);
    unc = max(unc, 0.0);
    return unc;

def RotateXY(mat, phi):

    V11 = mat[0][0]*math.cos(phi)**2+math.sin(phi)**2*mat[1][1]
    V12 = -math.cos(phi)*math.sin(phi)*( mat[0][0] - mat[1][1] )
    V21 = -math.cos(phi)*math.sin(phi)*( mat[0][0] - mat[1][1] )
    V22 = mat[0][0]*math.sin(phi)**2+math.cos(phi)**2*mat[1][1]
    
    #mat_new=[[math.cos(phi)*mat[0][0],-math.sin(phi)*mat[1][0]],[math.sin(phi)*mat[1][0],-math.cos(phi)*mat[1][1]]]
    mat_new=[[V11,V12],[V21,V22]]
    return mat_new

def MultMatrix(Xcom, X, mat):

    mat_new=[[math.cos(phi)*mat[0][0],-math.sin(phi)*mat[1][0]],[math.sin(phi)*mat[1][0],-math.cos(phi)*mat[1][1]]]
    return mat_new

def InvertMatrix(mat):

    det = mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
    #print det
    m=[[0.0,0.0],[0.0,0.0]]    
    if det==0.0:
        return m

    m[0][0]=1.0/det*(mat[1][1])
    m[1][0]=-1.0/det*(mat[1][0])
    m[0][1]=-1.0/det*(mat[0][1])
    m[1][1]=1.0/det*(mat[0][0])
    return m

def AddMatrix(X, Y):

    mat_new=[[0.0,0.0],[0.0,0.0]]
    mat_new[0][0]=X[0][0]+Y[0][0]
    mat_new[0][1]=X[0][1]+Y[0][1]
    mat_new[1][0]=X[1][0]+Y[1][0]
    mat_new[1][1]=X[1][1]+Y[1][1]
    return mat_new

def METSig(e, allJets):

    # add tight cleaning
    # add met tenacious
    # add met sig
    met_reso=0.0
    #SUM_MATRIX=[[0.0,0.0],[0.0,0.0]]
    SUM_MATRIX=[[10.0,0.0],[0.0,10.0]] # met soft
    SUM_ET=[0.0,0.0]
    MET_TENAC=[0.0,0.0]
    #print 'MET: ',e.MET,' soft: ',e.METsoft
    jet_et=[0.0,0.0]
    njet=0
    ht=0
    for j in range(0,allJets):
        #print 'pT: ',e.JetPt[j]
        if abs(e.JetEta[j])<2.4 and e.JetJVT[j]<0.59:
            continue
        #MET_TENAC[0]+=
        #MET_TENAC[1]+=
        met_reso+=e.JetPt[j]*0.03
        ht+=e.JetPt[j]
        jet_et[0]+=e.JetPt[j]*math.cos(e.JetPhi[j])
        jet_et[1]+=e.JetPt[j]*math.sin(e.JetPhi[j])
        if (abs(e.JetEta[j])>2.4 and e.JetPt[j]>35.0e3) or (abs(e.JetEta[j])<2.5 and abs(e.JetJVT[j])>0.11):
            if (abs(e.JetEta[j])<2.4 and abs(e.JetJVT[j])>0.91 and e.JetPt[j]<40.0e3):
                MET_TENAC[0]+=e.JetPt[j]*math.cos(e.JetPhi[j])
                MET_TENAC[1]+=e.JetPt[j]*math.sin(e.JetPhi[j])
            if  (abs(e.JetEta[j])>2.4 and (e.JetFJVT[j]<0.5 or e.JetPt[j]>120e3)):
                MET_TENAC[0]+=e.JetPt[j]*math.cos(e.JetPhi[j])
                MET_TENAC[1]+=e.JetPt[j]*math.sin(e.JetPhi[j])                
        njet+=1
        jet_2v = [e.JetPt[j]*math.cos(e.JetPhi[j]),e.JetPt[j]*math.sin(e.JetPhi[j])]
        pu_prob = GetPUProb(e.JetPt[j], e.JetEta[j], e.JetJVT[j], e.avIntPerXing, e.JetFJVT[j])
        jet_pt_reso = math.hypot(pu_prob,0.03)
        jet_u = [[(e.JetPt[j]*jet_pt_reso)**2,0.0],[0.0,(e.JetPt[j]*0.02)**2]]
        #if e.JetJVT[j]<0.05 and abs(e.JetEta[j])<2.7:
        #    jet_u = [[(e.JetPt[j]*0.95)**2,0.0],[0.0,(e.JetPt[j]*0.02)**2]]
        #elif e.JetJVT[j]<0.59 and abs(e.JetEta[j])<2.7:
        #    jet_u = [[(e.JetPt[j]*0.40)**2,0.0],[0.0,(e.JetPt[j]*0.02)**2]]
        #elif abs(e.JetEta[j])>2.7 and e.JetPt[j]<40.0e3:
        #    jet_u = [[(e.JetPt[j]*0.95)**2,0.0],[0.0,(e.JetPt[j]*0.02)**2]]
        #elif abs(e.JetEta[j])>2.7:
        #    jet_u = [[(e.JetPt[j]*0.1)**2,0.0],[0.0,(e.JetPt[j]*0.02)**2]]
        #else:
        #    jet_u = [[(e.JetPt[j]*0.06)**2,0.0],[0.0,(e.JetPt[j]*0.02)**2]]
        jet_xy_V = RotateXY(jet_u,-1.0*e.JetPhi[j])
        SUM_MATRIX=AddMatrix(SUM_MATRIX,jet_xy_V)
        SUM_ET=[jet_2v[0]+SUM_ET[0], jet_2v[1]+SUM_ET[1]]

    # Multiply S = E . V-1. E
    met_x = e.MET*math.cos(e.METphi) 
    met_y = e.MET*math.sin(e.METphi) 
    SUM_MATRIX=InvertMatrix(SUM_MATRIX)
    SUM_ET=[met_x, met_y]
    V1 = SUM_MATRIX[0][0]*SUM_ET[0] + SUM_MATRIX[0][1]*SUM_ET[1]
    V2 = SUM_MATRIX[1][0]*SUM_ET[0] + SUM_MATRIX[1][1]*SUM_ET[1]
    S = V1*SUM_ET[0] + V2*SUM_ET[1]
    met_over_sqrtht = 0
    if ht>0.0:
        met_over_sqrtht=(e.MET)/math.sqrt(ht)

    #print 'before met_x: ',met_x,met_y,jet_et[0],jet_et[1]
    met_x += jet_et[0]
    met_y += jet_et[1]
    #print 'met_x: ',met_x,met_y
    #print math.sqrt(met_x*met_x+met_y*met_y),' soft: ',e.METsoft
    met_tenac_x = met_x - MET_TENAC[0]
    met_tenac_y = met_y - MET_TENAC[1]
    met_tenac_et = math.hypot(met_tenac_x,met_tenac_y)# math.sqrt(met_tenac_x*met_tenac_x+met_tenac_y*met_tenac_y)
    
    met_tenac_phi = math.atan2(met_tenac_y,met_tenac_x)
    #print met_tenac_et,e.MET,math.sqrt(S)
    return met_over_sqrtht,met_tenac_et,met_tenac_phi,math.sqrt(S)

# create output
ROOT.gROOT.ProcessLine(
"struct MyStruct {\
   Float_t   jj_mass;\
   Float_t   jj_dphi;\
   Float_t   jj_deta;\
   Float_t   w;\
   Float_t   TriggerEffWeight;\
   Float_t   TriggerEffWeightBDT;\
   Float_t   met_tenacious_tst_j1_dphi;\
   Float_t   met_tenacious_tst_j2_dphi;\
   Float_t   met_tenacious_tst_et;\
   Float_t   met_tenacious_tst_nolep_et;\
   Float_t   met_tenacious_tst_phi;\
   Float_t   met_cst_jet;\
   Float_t   met_soft_tst_et;\
   Float_t   met_significance;\
   Float_t   max_mj_over_mjj;\
   Float_t   maxCentrality;\
   std::vector<Float_t>   *jet_pt;\
   std::vector<Float_t>   *jet_eta;\
   std::vector<Float_t>   *jet_phi;\
   std::vector<Float_t>   *jet_m;\
   std::vector<Float_t>   *jet_timing;\
   std::vector<Float_t>   *jet_jvt;\
   std::vector<Float_t>   *jet_fjvt;\
   std::vector<unsigned short>   *jet_NTracks;\
   Int_t     n_vx;\
   Int_t     n_tau;\
   Int_t     n_el;\
   Int_t     n_ph;\
   Int_t     n_mu_w;\
   Int_t     n_jetPU;\
   Int_t     n_jetHS;\
   Int_t     n_el_w;\
   Int_t     n_mu_baseline_noOR;\
   Int_t     lep_trig_match;\
   Int_t     n_mu;\
   Int_t     n_baseel;\
   Int_t     n_basemu;\
   Int_t     n_jet;\
   Int_t     n_bjet;\
   Int_t     trigger_met;\
   Int_t     trigger_lep;\
   Int_t     runNumber;\
   Int_t     trigger_met_encoded;\
   Int_t     trigger_met_encodedv2;\
   Bool_t     passVjetsFilter;\
   Bool_t     passVjetsFilterTauEl;\
   Bool_t     passVjetsPTV;\
   Int_t     passJetCleanTight;\
   Float_t   met_tst_phi;\
   Float_t   met_tst_nolep_phi;\
   Float_t   met_soft_tst_phi;\
   Float_t   met_soft_tst_sumet;\
   Float_t   met_tight_tst_et;\
   Float_t   met_tight_tst_phi;\
   Float_t   met_truth_et;\
   Float_t   met_tst_et;\
   Float_t   met_tst_j1_dphi;\
   Float_t   met_tst_j2_dphi;\
   Float_t   met_tst_nolep_et;\
   Float_t   met_tst_nolep_j1_dphi;\
   Float_t   met_tst_nolep_j2_dphi;\
   Float_t   metsig_tst;\
   Float_t   averageIntPerXing;\
   ULong64_t     eventNumber;\
};" );

flts=['met_soft_tst_phi',
  'met_soft_tst_sumet',
  'met_tight_tst_et',
  'met_tight_tst_phi',
  'met_truth_et',
  'met_tst_et',
  'met_tst_j1_dphi',
  'met_tst_j2_dphi',
  'met_tst_nolep_et',
  'met_tst_nolep_j1_dphi',
  'met_tst_nolep_j2_dphi',
  'met_tst_nolep_phi',
  'met_tst_phi',
  'metsig_tst',]
ints =['passJetCleanTight',
  'trigger_met_encoded',
  'trigger_met_encodedv2',]
bols=[  'passVjetsFilter','passVjetsFilterTauEl',
  'passVjetsPTV',]
from ROOT import MyStruct
mystruct = MyStruct()
tree_out = ROOT.TTree( 'QCDDDNominal', 'Nominal data driven QCD' )
#tree_out.Branch( 'myfloats', mystruct, 'jj_mass/F:jj_dphi/F:jj_deta/F' )
tree_out.Branch( 'jj_mass', ROOT.AddressOf( mystruct, 'jj_mass' ), 'jj_mass/F' )
tree_out.Branch( 'jj_dphi', ROOT.AddressOf( mystruct, 'jj_dphi' ), 'jj_dphi/F' )
tree_out.Branch( 'jj_deta', ROOT.AddressOf( mystruct, 'jj_deta' ), 'jj_deta/F' )
tree_out.Branch( 'w', ROOT.AddressOf( mystruct, 'w' ), 'w/F' )
tree_out.Branch( 'TriggerEffWeight', ROOT.AddressOf( mystruct, 'TriggerEffWeight' ), 'TriggerEffWeight/F' )
tree_out.Branch( 'TriggerEffWeightBDT', ROOT.AddressOf( mystruct, 'TriggerEffWeightBDT' ), 'TriggerEffWeightBDT/F' )
tree_out.Branch( 'met_tenacious_tst_j1_dphi', ROOT.AddressOf( mystruct, 'met_tenacious_tst_j1_dphi' ), 'met_tenacious_tst_j1_dphi/F' )
tree_out.Branch( 'met_tenacious_tst_j2_dphi', ROOT.AddressOf( mystruct, 'met_tenacious_tst_j2_dphi' ), 'met_tenacious_tst_j2_dphi/F' )
tree_out.Branch( 'met_tenacious_tst_et', ROOT.AddressOf( mystruct, 'met_tenacious_tst_et' ), 'met_tenacious_tst_et/F' )
tree_out.Branch( 'met_tenacious_tst_nolep_et', ROOT.AddressOf( mystruct, 'met_tenacious_tst_nolep_et' ), 'met_tenacious_tst_nolep_et/F' )
tree_out.Branch( 'met_tenacious_tst_phi', ROOT.AddressOf( mystruct, 'met_tenacious_tst_phi' ), 'met_tenacious_tst_phi/F' )
tree_out.Branch( 'met_cst_jet', ROOT.AddressOf( mystruct, 'met_cst_jet' ), 'met_cst_jet/F' )
tree_out.Branch( 'met_soft_tst_et', ROOT.AddressOf( mystruct, 'met_soft_tst_et' ), 'met_soft_tst_et/F' )
tree_out.Branch( 'met_significance', ROOT.AddressOf( mystruct, 'met_significance' ), 'met_significance/F' )
tree_out.Branch( 'max_mj_over_mjj', ROOT.AddressOf( mystruct, 'max_mj_over_mjj' ), 'max_mj_over_mjj/F' )
tree_out.Branch( 'maxCentrality', ROOT.AddressOf( mystruct, 'maxCentrality' ), 'maxCentrality/F' )
tree_out.Branch( 'n_vx', ROOT.AddressOf( mystruct, 'n_vx' ), 'n_vx/I' )
tree_out.Branch( 'n_tau', ROOT.AddressOf( mystruct, 'n_tau' ), 'n_tau/I' )
#tree_out.Branch( 'n_pv', ROOT.AddressOf( mystruct, 'n_pv' ), 'n_pv/I' )
tree_out.Branch( 'n_el', ROOT.AddressOf( mystruct, 'n_el' ), 'n_el/I' )
tree_out.Branch( 'n_ph', ROOT.AddressOf( mystruct, 'n_ph' ), 'n_ph/I' )
tree_out.Branch( 'n_jetPU', ROOT.AddressOf( mystruct, 'n_jetPU' ), 'n_jetPU/I' )
tree_out.Branch( 'n_jetHS', ROOT.AddressOf( mystruct, 'n_jetHS' ), 'n_jetHS/I' )
tree_out.Branch( 'n_mu', ROOT.AddressOf( mystruct, 'n_mu' ), 'n_mu/I' )
tree_out.Branch( 'n_baseel', ROOT.AddressOf( mystruct, 'n_baseel' ), 'n_baseel/I' )
tree_out.Branch( 'n_mu_w', ROOT.AddressOf( mystruct, 'n_mu_w' ), 'n_mu_w/I' )
tree_out.Branch( 'n_el_w', ROOT.AddressOf( mystruct, 'n_el_w' ), 'n_el_w/I' )
tree_out.Branch( 'n_mu_baseline_noOR', ROOT.AddressOf( mystruct, 'n_mu_baseline_noOR' ), 'n_mu_baseline_noOR/I' )
tree_out.Branch( 'lep_trig_match', ROOT.AddressOf( mystruct, 'lep_trig_match' ), 'lep_trig_match/I' )
tree_out.Branch( 'n_basemu', ROOT.AddressOf( mystruct, 'n_basemu' ), 'n_basemu/I' )
tree_out.Branch( 'n_jet', ROOT.AddressOf( mystruct, 'n_jet' ), 'n_jet/I' )
tree_out.Branch( 'n_bjet', ROOT.AddressOf( mystruct, 'n_bjet' ), 'n_bjet/I' )
tree_out.Branch( 'trigger_met', ROOT.AddressOf( mystruct, 'trigger_met' ), 'trigger_met/I' )
tree_out.Branch( 'trigger_lep', ROOT.AddressOf( mystruct, 'trigger_lep' ), 'trigger_lep/I' )
tree_out.Branch( 'runNumber', ROOT.AddressOf( mystruct, 'runNumber' ), 'runNumber/I' )
tree_out.Branch( 'averageIntPerXing', ROOT.AddressOf( mystruct, 'averageIntPerXing' ), 'averageIntPerXing/F' )
tree_out.Branch( 'eventNumber', ROOT.AddressOf( mystruct, 'eventNumber' ), 'eventNumber/l' )
for v in flts:
    tree_out.Branch( v, ROOT.AddressOf( mystruct, v ), v+'/F' )
for v in bols:
    tree_out.Branch( v, ROOT.AddressOf( mystruct, v ), v+'/O' )
for v in ints:
    tree_out.Branch( v, ROOT.AddressOf( mystruct, v ), v+'/I' )
mystruct.jet_pt = ROOT.std.vector('float')()
mystruct.jet_eta = ROOT.std.vector('float')()
mystruct.jet_phi = ROOT.std.vector('float')()
mystruct.jet_m = ROOT.std.vector('float')()
mystruct.jet_timing = ROOT.std.vector('float')()
mystruct.jet_jvt = ROOT.std.vector('float')()
mystruct.jet_fjvt = ROOT.std.vector('float')()
mystruct.jet_NTracks = ROOT.std.vector('unsigned short')()

tree_out.Branch( 'jet_pt',  mystruct.jet_pt)
tree_out.Branch( 'jet_eta', mystruct.jet_eta)
tree_out.Branch( 'jet_phi', mystruct.jet_phi)
tree_out.Branch( 'jet_m', mystruct.jet_m)
tree_out.Branch( 'jet_timing', mystruct.jet_timing)
tree_out.Branch( 'jet_jvt', mystruct.jet_jvt)
tree_out.Branch( 'jet_fjvt', mystruct.jet_fjvt)
tree_out.Branch( 'jet_NTracks', mystruct.jet_NTracks)
#tree_out.Branch( 'jet_phi', ROOT.AddressOf( mystruct, 'jet_phi' ), 'jet_phi' )
#tree_out.Branch( 'jet_m', ROOT.AddressOf( mystruct, 'jet_m' ), 'jet_m' )
#tree_out.Branch( 'jet_timing', ROOT.AddressOf( mystruct, 'jet_timing' ), 'jet_timing' )
#tree_out.Branch( 'jet_jvt', ROOT.AddressOf( mystruct, 'jet_jvt' ), 'jet_jvt' )
#tree_out.Branch( 'jet_fjvt', ROOT.AddressOf( mystruct, 'jet_fjvt' ), 'jet_fjvt' )
#tree_out.Branch( 'jet_NTracks', ROOT.AddressOf( mystruct, 'jet_NTracks' ), 'jet_NTracks' )
 
#f = ROOT.TFile.Open('/eos/atlas/atlascerngroupdisk/penn-ww/out_QCD_Tenacious.root')
#f = ROOT.TFile.Open('out_QCD_Tenacious.root')
#f = ROOT.TFile.Open('out_QCD_Loose.root')
f = ROOT.TFile.Open(args.input)
IsLoose=False

GeV=1.0e3
tree = f.Get('PredictionTree')
fout = ROOT.TFile.Open(args.output,'RECREATE')
z=0
v1 = ROOT.TLorentzVector()
v2 = ROOT.TLorentzVector()
v3 = ROOT.TLorentzVector()
v4 = ROOT.TLorentzVector()
met = ROOT.TLorentzVector()

h1= ROOT.TH1F("cutflow","cutflow",20, 0.5, 20.5)
h1.SetDirectory(fout)
#tree_out.SetDirectory(fout)
print 'Total: ',tree.GetEntries()
for e in tree:
    if z%10000 ==0:
        print 'Event: ',z
        sys.stdout.flush()
    #if z>100000:
    #    break
    z+=1
    
    # remove those with ntries not >0. -2 is the unsmeared events
    if e.Ntries<0.2:
        continue

    # weight is trigger and event  
    # and divide by 20, which is the number of pseudo samples
    #weight = e.Weight*e.TriggerWeight/20.0 #/36100.0
    weight = e.TotalWeight;

    if not (e.JetPt[0]>70.0):
        continue
    if not (e.JetPt[1]>40.0):
        continue
    # apply MET cuts
    if not (e.MET>100.0):
        continue
    # counting njet
    mystruct.n_jet=0
    allJets=0
    for jetPt in e.JetPt:
        allJets+=1
        if jetPt>25.0:
            mystruct.n_jet+=1
    minNjet = min(5,mystruct.n_jet)
    
    # apply jet cut
    if mystruct.n_jet>4 or mystruct.n_jet<2:
        continue
    h1.Fill(2, weight)

    mystruct.jet_pt.clear();
    mystruct.jet_eta.clear();
    mystruct.jet_phi.clear();
    mystruct.jet_m.clear();
    mystruct.jet_timing.clear();
    mystruct.jet_jvt.clear();
    mystruct.jet_fjvt.clear();
    mystruct.jet_NTracks.clear();    
    ijetUsed=0
    for i in range(0,allJets):
        if not (e.JetPt[i]>25.0):
            continue
        mystruct.jet_pt.push_back(e.JetPt[i]*GeV)
        mystruct.jet_eta.push_back(e.JetEta[i])
        mystruct.jet_phi.push_back(e.JetPhi[i])
        mystruct.jet_m.push_back(e.JetM[i]*GeV)
        mystruct.jet_timing.push_back(0.0)
        mystruct.jet_jvt.push_back(e.JetJVT[i])
        mystruct.jet_NTracks.push_back(e.JetNTracks[i])
        mystruct.jet_fjvt.push_back(e.JetFJVT[i])
    
    # jet cuts
    met.SetPtEtaPhiM(e.MET, 0.0, e.METphi, 0.0)
    v1.SetPtEtaPhiM(mystruct.jet_pt[0],mystruct.jet_eta[0],mystruct.jet_phi[0],mystruct.jet_m[0])
    v2.SetPtEtaPhiM(mystruct.jet_pt[1],mystruct.jet_eta[1],mystruct.jet_phi[1],mystruct.jet_m[1])
    if mystruct.n_jet>2:
        v3.SetPtEtaPhiM(mystruct.jet_pt[2],mystruct.jet_eta[2],mystruct.jet_phi[2],mystruct.jet_m[2])
    if mystruct.n_jet>3:
        v4.SetPtEtaPhiM(mystruct.jet_pt[3],mystruct.jet_eta[3],mystruct.jet_phi[3],mystruct.jet_m[3])

    # compute vars
    #j1_met_dphi=3
    #j2_met_dphi=3
    j1_met_dphi = abs(v1.DeltaPhi(met))
    j2_met_dphi = abs(v2.DeltaPhi(met))
    jj_deta = abs(mystruct.jet_eta[0] - mystruct.jet_eta[1])
    jj_dphi = abs(v1.DeltaPhi(v2))
    # dphijj cut
    #if jj_dphi >2.0:
    #    continue
    
    #jj_dphi=5
    jj_mass = (v1+v2).M()
    if jj_mass<200.0e3:
        continue
    # write output tree
    met_over_sqrtht,met_tenac_et,met_tenac_phi,metsig_tst = METSig(e, allJets)
    mystruct.jj_mass = jj_mass
    mystruct.jj_dphi = jj_dphi
    mystruct.jj_deta = jj_deta
    mystruct.w = weight
    mystruct.TriggerEffWeight = e.TriggerEffWeight
    mystruct.TriggerEffWeightBDT = e.TriggerEffWeightBDT
    mystruct.met_tenacious_tst_j1_dphi = j1_met_dphi
    mystruct.met_tenacious_tst_j2_dphi = j2_met_dphi
    mystruct.met_tenacious_tst_et = met_tenac_et*GeV
    mystruct.met_tenacious_tst_nolep_et = met_tenac_et*GeV
    mystruct.met_tenacious_tst_phi = met_tenac_phi
    mystruct.met_cst_jet = e.MHTDefReb*GeV 
    mystruct.met_soft_tst_et = e.METsoft*GeV
    mystruct.met_significance=met_over_sqrtht  #e.METsig
    mystruct.max_mj_over_mjj=-9999.0
    mystruct.maxCentrality=-9999.0
    mystruct.trigger_met_encoded=1
    mystruct.trigger_met_encodedv2=1
    mystruct.passVjetsFilter=1
    mystruct.passVjetsFilterTauEl=1
    mystruct.passVjetsPTV=1
    mystruct.passJetCleanTight=1
    mystruct.met_tst_phi = e.METphi
    mystruct.met_tst_nolep_phi = e.METphi
    mystruct.met_soft_tst_phi=0.0
    mystruct.met_soft_tst_sumet=0.0
    mystruct.met_tight_tst_et = e.MET*GeV
    mystruct.met_tight_tst_phi = e.METphi
    mystruct.met_truth_et=0
    mystruct.met_tst_et = e.MET*GeV
    mystruct.met_tst_j1_dphi = j1_met_dphi
    mystruct.met_tst_j2_dphi = j2_met_dphi
    mystruct.met_tst_nolep_et = e.MET*GeV
    mystruct.met_tst_nolep_j1_dphi = j1_met_dphi
    mystruct.met_tst_nolep_j2_dphi = j2_met_dphi
    mystruct.metsig_tst=metsig_tst #e.METsig = value from the seed jets
            
    #print minNjet
    for j in range(2,minNjet):
        centrality = math.exp(-4.0/jj_deta**2 * (mystruct.jet_eta[j] - (mystruct.jet_eta[0]+mystruct.jet_eta[1])/2.0)**2);
        if centrality>mystruct.maxCentrality:
            mystruct.maxCentrality = centrality
        if j==2:
            mj1 = (v1+v3).M()
            mj2 = (v2+v3).M()
            maxmj3_over_mjj = min(mj1,mj2)/jj_mass;
            mystruct.max_mj_over_mjj = max(mystruct.max_mj_over_mjj, maxmj3_over_mjj)
            #print '3 jet: ', maxmj3_over_mjj,  mystruct.max_mj_over_mjj            
        elif j==3:
            mj1 = (v1+v4).M()
            mj2 = (v2+v4).M()
            maxmj3_over_mjj = min(mj1,mj2)/jj_mass;
            mystruct.max_mj_over_mjj = max(mystruct.max_mj_over_mjj, maxmj3_over_mjj)
            #print '4jet: ', maxmj3_over_mjj,  mystruct.max_mj_over_mjj
    #if(maxmj3_over_mjj<tmp_maxmj3_over_mjj) maxmj3_over_mjj = tmp_maxmj3_over_mjj;
    mystruct.runNumber=e.Run
    mystruct.eventNumber=abs(e.Event)
    mystruct.averageIntPerXing=e.avIntPerXing
    #mystruct.n_pv=e.NVtx
    mystruct.n_tau=0
    mystruct.n_ph=e.NPhotons
    mystruct.n_jetPU=e.NjetsPU
    mystruct.n_jetHS=e.NjetsHS
    mystruct.n_el=0
    mystruct.n_mu_w=0
    mystruct.n_el_w=0
    mystruct.n_mu_baseline_noOR=0
    mystruct.lep_trig_match=0
    mystruct.n_mu=0
    mystruct.n_basemu=0
    mystruct.n_baseel=0
    #mystruct.n_jet=e.NJets
    mystruct.n_bjet=e.BTags
    mystruct.n_vx=int(e.NVtx)
    mystruct.trigger_met=1
    mystruct.trigger_lep=0

    tree_out.Fill()
    
    h1.Fill(1, weight)
    # apply MET cuts
    if not (e.MET>150.0):
        continue
    h1.Fill(3, weight)
    if not (e.MHTDefReb>120.0):
        continue
    h1.Fill(4, weight)
    if mystruct.n_jet!=2:
        continue
    h1.Fill(5, weight)
    # met soft
    if not (e.METsoft<20.0):
        continue
    h1.Fill(6, weight)

    # jet pT cuts
    if not (mystruct.jet_pt[0]>80.0):
        continue
    h1.Fill(7, weight)
    if not (mystruct.jet_pt[1]>50.0):
        continue
    h1.Fill(8, weight)

    # Deltaphi cuts
    if j1_met_dphi<1.0:
        continue
    h1.Fill(9, weight)
    if j2_met_dphi<1.0:
        continue
    h1.Fill(10, weight)
    # opposite hemi
    oppHemi = (mystruct.jet_eta[0] * mystruct.jet_eta[1])
    if oppHemi>0:
        continue
    h1.Fill(11, weight)

    # detajj cut
    if not (jj_deta>3.8):
        continue
    h1.Fill(12, weight)    

    # dphijj cut
    if not (jj_dphi < 1.8):
        continue
    h1.Fill(13, weight)
    # mjj cut
    if not (jj_mass >1000.0):
        continue
    h1.Fill(14, weight)

    if not IsLoose:
        # loose fjvt
        if e.JetFJVT[0]>0.5:
            continue
        if e.JetFJVT[1]>0.5:
            continue
    h1.Fill(15, weight)

    if not IsLoose:
        # very tight fjvt
        if e.MET<180.0:
            if e.JetFJVT[0]>0.2:
                continue
            if e.JetFJVT[1]>0.2:
                continue
        
    h1.Fill(16, weight)

fout.cd()
tree_out.Write()
fout.Write()
fout.Close()
f.Close()
print 'DONE'
