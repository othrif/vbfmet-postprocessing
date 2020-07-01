#!/usr/bin/env python
"""
Optimize cuts in the signal region for the ZH dark photon analysis without using ROOT!"
"""
__author__ = "Stanislava Sevova"
###############################################################################                                   
# Import libraries                                                                                                
################## 
import argparse
import ahoi
import os
import re
import uproot as up
import uproot_methods
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
ahoi.tqdm = tqdm # use notebook progress bars in ahoi
import matplotlib.pyplot as plt
import math
###############################################################################                                   
# Command line arguments
######################## 
def getArgumentParser():
    """ Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Script for running optimization for the ZH dark photon SR")
    parser.add_argument('-i',
                        '--indir',
                        dest='indir',
                        help='Directory with input files',
                        default="/afs/cern.ch/work/s/ssevova/public/dark-photon-atlas/plotting/trees/v04/")
    parser.add_argument('-o',
                        '--output',
                        dest='outdir',
                        help='Output directory to put file list(s) into',
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'outdir'))
    
    return parser
###############################################################################                                   
# Dataframes for each sample
############################ 
def sampleDataframe(infiles,treename): 
    """ Open the ROOT file(s) corresponding to the treename
    and put the relevant branches into a dataframe """
    
    ## Branches to read in 
    branches = ["w","in_vy_overlap",
                "trigger_lep",
                "passJetCleanTight",
                "n_mu","n_ph","n_bjet",
                "ph_pt","ph_eta","ph_phi",
                "met_tight_tst_et", "met_tight_tst_phi",
                "mu_pt","mu_eta", "mu_phi",
                "eventNumber"]
<<<<<<< HEAD
=======
    
>>>>>>> e0a52ad2fef5202459a18317778777d168792524
    for path, file, start, stop, entry in up.iterate(
            infiles+"*.root",
            treename,
            branches=branches,
            reportpath=True, reportfile=True, reportentries=True):

        print('==> Processing sample: %s ...'%path)
        tree = up.open(path)[treename]
<<<<<<< HEAD
        
        df_sample = tree.pandas.df(branches,flatten=False)
        return df_sample

def calcmT(met,ph):
    #ph_pt = np.concatenate(ph.pt).ravel()
    #ph_phi = np.concatenate(ph.phi).ravel()
    # Can't multiply two lorentz vectors?
    return np.sqrt(2*met.pt*ph.pt*(1-np.cos(ph.phi-met.phi)))

def calcPhiLepMet(lep1,lep2,met,ph):
    phi_lep = (lep1+lep2).phi
    phi_ph_met = (met+ph).phi
    return phi_ph_met-phi_lep
    
def calcAbsPt(lep1,lep2,met,ph):
    pt_lep = (lep1+lep2).pt
    pt_ph_met = (met+ph).pt    
    return np.abs(pt_ph_met-pt_lep)/pt_lep

def getLorentzVec(df):
    """ Calculates Lorentz vectors for the leptons and photons for bkg/sig"""
    mu_pt = np.asarray(df.mu_pt.values.tolist())
    mu_eta = np.asarray(df.mu_eta.values.tolist())
    mu_phi = np.asarray(df.mu_phi.values.tolist())
    mu_mass = np.asarray(df.mu_mass.values.tolist())

    lep1 = uproot_methods.TLorentzVectorArray.from_ptetaphim(mu_pt[:,0],mu_eta[:,0],mu_phi[:,0],
                                                             mu_mass[:,0])
    lep2 = uproot_methods.TLorentzVectorArray.from_ptetaphim(mu_pt[:,1],mu_eta[:,1],mu_phi[:,1],
                                                             mu_mass[:,1])
    # Need to fix this -> gives an error when trying to add to lepton vectors                                                                  
    # Had to change to types for the photon variables                                                                                          
    vPh = uproot_methods.TLorentzVectorArray.from_ptetaphim(df['ph_pt'].to_numpy().astype(float),
                                                                df['ph_eta'].to_numpy().astype(float),
                                                                df['ph_phi'].to_numpy().astype(float),
                                                                0.00)
    met = uproot_methods.TLorentzVectorArray.from_ptetaphim(df['met_tight_tst_et'].to_numpy(),
                                                            0.00, df['met_tight_tst_phi'].to_numpy(), 0.00)
    return lep1,lep2,vPh,met

def calcVars(df):

    vLep_bkg1,vLep_bkg2,vPh_bkg,vMET_bkg = getLorentzVec(df)

    df['mT'] = calcmT(vMET_bkg,vPh_bkg)
    df['dPhiLepMet'] = calcPhiLepMet(vLep_bkg1,vLep_bkg2,vMET_bkg,vPh_bkg)
    df['AbsPt'] = calcAbsPt(vLep_bkg1,vLep_bkg2,vMET_bkg,vPh_bkg)
    df['Ptll'] = (vLep_bkg1 + vLep_bkg2).pt
    print((vLep_bkg1 + vLep_bkg2).pt)
    df['mllg'] = (vLep_bkg1+vLep_bkg2+vPh_bkg).mass
    return df

def main(): 
    """ Run script"""
    options = getArgumentParser().parse_args()
=======

        df_sample = tree.pandas.df(branches,flatten=False)
        return df_sample

def main(): 
    """ Run script"""
    options = getArgumentParser().parse_args()

>>>>>>> e0a52ad2fef5202459a18317778777d168792524
    ### Make all the bkg and signal dataframes!

    ## Z+jets
    df_zjets  = sampleDataframe(options.indir,"Z_strongNominal")
    df_zjets  = df_zjets.append(sampleDataframe(options.indir,"Z_EWKNominal"))

    ## Z+photon
    df_zgamma = sampleDataframe(options.indir,"Zg_strongNominal")

    # ## ttbar/single top/Wt/ttbar+V
    # df_top    = sampleDataframe(options.indir,"ttbarNominal")
    # df_top    = df_top.append(sampleDataframe(options.indir,"ttVNominal"))

    # ## Triboson
    # df_VVV    = sampleDataframe(options.indir,"VVVNominal")
    # df_VVV    = df_VVV.append(sampleDataframe(options.indir,"VVyNominal"))

    # ## Diboson
    # df_VV     = sampleDataframe(options.indir,"VVNominal")
    # df_VV     = df_VV.append(sampleDataframe(options.indir,"VV_ewkNominal"))
    # df_VV     = df_VV.append(sampleDataframe(options.indir,"ggZZNominal"))
    # df_VV     = df_VV.append(sampleDataframe(options.indir,"ggWWNominal"))

    # ## H->Zy
    # df_HZy    = sampleDataframe(options.indir,"ggH125ZyNominal")
    # df_HZy    = df_HZy.append(sampleDataframe(options.indir,"ttH125ZyNominal"))
    # df_HZy    = df_HZy.append(sampleDataframe(options.indir,"VBFH125ZyNominal"))
    # df_HZy    = df_HZy.append(sampleDataframe(options.indir,"VH125ZyNominal"))

    ## signal
    df_sig = sampleDataframe(options.indir,"HyGrNominal")


    ## Remove overlapping Z+jets events
    df_zjets = df_zjets[df_zjets['in_vy_overlap'] > 0]
    ## Make collective Z+jets/Z+photon bkg dataframe
    df_bkg = df_zjets 
    df_bkg = df_bkg.append(df_zgamma)
    
    ## Apply cuts 
    df_bkg = df_bkg[(df_bkg['trigger_lep']>0) &
                    (df_bkg['passJetCleanTight']==1) &
                    (df_bkg['n_ph']==1) & 
                    (df_bkg['n_mu']==2) &
                    (df_bkg['n_bjet']==0)]
    
    ## blegh this needs to be fixed    
<<<<<<< HEAD
    df_bkg['mu_mass'] = list(np.full((len(df_bkg),2),105.6))
=======
    df_bkg['mu_mass'] = pd.array([105.6,105.6])

>>>>>>> e0a52ad2fef5202459a18317778777d168792524
    df_sig = df_sig[(df_sig['trigger_lep']>0) &
                    (df_sig['passJetCleanTight']==1) &
                    (df_sig['n_ph']==1) & 
                    (df_sig['n_mu']==2) &
                    (df_sig['n_bjet']==0)]
    
    #    print(df_sig['mu_pt[0]'])
<<<<<<< HEAD
    # Seems like signal and background should have the same quantities b/c we're testing
    # how cuts can distinguish between signal and background
    df_sig['mu_mass'] = list(np.full((len(df_sig),2),105.6))
=======

>>>>>>> e0a52ad2fef5202459a18317778777d168792524
    ## Compute compound variables, like mll, mT(met,ph_pt)...
    ## Info on how to use TLorentzVectors in uproot: https://github.com/scikit-hep/uproot#special-physics-objects-lorentz-vectors
    ## The TLorentzVector class contains a method called "from_ptetaphim": 
    ## https://github.com/scikit-hep/uproot-methods/blob/master/uproot_methods/classes/TLorentzVector.py#L978
<<<<<<< HEAD
    df_bkg = calcVars(df_bkg)

    df_sig = calcVars(df_sig)
    # Calculate quantities of interest and put in dataframe for signal dataframe
    # See about other quantities eg mllg
    
    #lep1 = uproot_methods.TLorentzVectorArray.from_ptetaphim()
    ## Implement Ahoi stuff...
=======
    #MUON_MASS = 
    vLep = uproot_methods.TLorentzVectorArray.from_ptetaphim(df_bkg['mu_pt'].to_numpy(),
                                                                df_bkg['mu_eta'].to_numpy(),
                                                                df_bkg['mu_phi'].to_numpy(),
                                                                df_bkg['mu_mass'].to_numpy())
    print(vLep.pt)
    print(vLep.eta)
    print(vLep.phi)
    print(vLep.mass)
    #lep1 = uproot_methods.TLorentzVectorArray.from_ptetaphim()
    ## Implement Ahoi stuff...

    
>>>>>>> e0a52ad2fef5202459a18317778777d168792524
if __name__ == '__main__':
    main()
