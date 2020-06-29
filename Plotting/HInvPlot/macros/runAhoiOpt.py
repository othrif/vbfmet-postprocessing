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
    
    for path, file, start, stop, entry in up.iterate(
            infiles+"*.root",
            treename,
            branches=branches,
            reportpath=True, reportfile=True, reportentries=True):

        print('==> Processing sample: %s ...'%path)
        tree = up.open(path)[treename]

        df_sample = tree.pandas.df(branches,flatten=False)
        return df_sample

def main(): 
    """ Run script"""
    options = getArgumentParser().parse_args()

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
    df_bkg['mu_mass'] = pd.array([105.6,105.6])

    df_sig = df_sig[(df_sig['trigger_lep']>0) &
                    (df_sig['passJetCleanTight']==1) &
                    (df_sig['n_ph']==1) & 
                    (df_sig['n_mu']==2) &
                    (df_sig['n_bjet']==0)]
    
    #    print(df_sig['mu_pt[0]'])

    ## Compute compound variables, like mll, mT(met,ph_pt)...
    ## Info on how to use TLorentzVectors in uproot: https://github.com/scikit-hep/uproot#special-physics-objects-lorentz-vectors
    ## The TLorentzVector class contains a method called "from_ptetaphim": 
    ## https://github.com/scikit-hep/uproot-methods/blob/master/uproot_methods/classes/TLorentzVector.py#L978
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

    
if __name__ == '__main__':
    main()
