#!/usr/bin/env python
"""
Optimize cuts in the signal region for the ZH dark photon analysis without using ROOT!"
"""
__author__ = "Stanislava Sevova, Elyssa Hofgard"
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
#ahoi.tqdm = tqdm # use notebook progress bars in ahoi
import matplotlib.pyplot as plt
import math
# import atlas_mpl_style as ampl
# # Set ATLAS style
# ampl.use_atlas_style()
# ampl.set_color_cycle(pal='ATLAS')
# plt.rcParams["font.size"] = 11
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

def calcmT(met,ph):
    # SS: one suggestion I have is to use delta_phi function from https://github.com/scikit-hep/uproot-methods/blob/master/uproot_methods/classes/TLorentzVector.py#L82
    # so then your calculation becomes np.sqrt(2*met.pt*ph.pt(1-np.cos(delta_phi(ph,met))))
    return np.sqrt(2*met.pt*ph.pt*(1-np.cos(ph.delta_phi(met))))

def calcPhiLepMet(lep1,lep2,met,ph):
    return (lep1+lep2).delta_phi(met+ph)
        
def calcAbsPt(lep1,lep2,met,ph):
    pt_lep = (lep1+lep2).pt
    pt_ph_met = (met+ph).pt    
    return np.abs(pt_ph_met-pt_lep)/pt_lep

def getLorentzVec(df):
    """ Calculates Lorentz vectors for the leptons and photons for bkg/sig:
    but first converts all pTs and masses from MeV to GeV"""

    df['mu_pt']   = df['mu_pt'].truediv(1000)
    df['mu_mass'] = df['mu_mass'].truediv(1000)
    df['ph_pt']   = df['ph_pt'].truediv(1000)
    df['met_tight_tst_et'] = df['met_tight_tst_et'].truediv(1000)
    
    mu_pt   = np.asarray(df.mu_pt.values.tolist())
    mu_eta  = np.asarray(df.mu_eta.values.tolist())
    mu_phi  = np.asarray(df.mu_phi.values.tolist())
    mu_mass = np.asarray(df.mu_mass.values.tolist())

    lep1 = uproot_methods.TLorentzVectorArray.from_ptetaphim(mu_pt[:,0],mu_eta[:,0],mu_phi[:,0],
                                                             mu_mass[:,0])
    lep2 = uproot_methods.TLorentzVectorArray.from_ptetaphim(mu_pt[:,1],mu_eta[:,1],mu_phi[:,1],
                                                             mu_mass[:,1])
    vPh = uproot_methods.TLorentzVectorArray.from_ptetaphim(df['ph_pt'].to_numpy().astype(float),
                                                            df['ph_eta'].to_numpy().astype(float),
                                                            df['ph_phi'].to_numpy().astype(float),
                                                            0.00)

    met = uproot_methods.TLorentzVectorArray.from_ptetaphim(df['met_tight_tst_et'].to_numpy(),
                                                            0.00, df['met_tight_tst_phi'].to_numpy(), 0.00)
    return lep1,lep2,vPh,met

def calcVars(df):

    vLep1,vLep2,vPh,vMET = getLorentzVec(df)

    df['mT'] = calcmT(vMET,vPh)
    df['dPhiLepMet'] = calcPhiLepMet(vLep1,vLep2,vMET,vPh)
    df['AbsPt'] = calcAbsPt(vLep1,vLep2,vMET,vPh)
    df['Ptll'] = (vLep1 + vLep2).pt
    df['mll'] = (vLep1 + vLep2).mass
    df['mllg'] = (vLep1+vLep2+vPh).mass
    df['lep1pt'] = vLep1.pt
    df['lep2pt'] = vLep2.pt
    return df

def makePlots(df_bkg,df_sig,var,units):
    ### Plot some of the distributions for the signal and bkg
    fig,ax = plt.subplots(1,1)
    bkg = np.array(df_bkg[var])
    sig = np.array(df_sig[var])
    if var == 'ph_pt':
        bkg = np.concatenate(np.asarray(df_bkg[var])).ravel()
        sig = np.concatenate(np.asarray(df_sig[var])).ravel()
    max_val = max(np.concatenate([bkg,sig]))
    ax.hist(bkg, bins=50, range=(0, max_val), histtype='step', color='Red',label='bkg')
    ax.hist(sig, bins=50, range=(0, max_val), histtype='step', color='Blue',label='sig')
    ax.set_xlabel(var+' [' + units + ']')
    ax.set_ylabel('Events')
    ax.set_yscale('log')
    ax.legend()
    plt.savefig("hist_" + var+ ".pdf",format="pdf")

def get_selection(multi_index,cuts):
    ## Selects the cut values from the list of cuts after ahoi optimization 
    expr_list = []
    for i, (expr, vals) in zip(multi_index, cuts):
        if i == 0:
            continue
        expr_list.append("({})".format(expr.format(vals[i-1])))
    return expr_list

def get_ams(s, b):
    ## Metric that the ahoi optimization tutorial used, could change this
    return np.sqrt(2*((s+b+10)*np.log(1+s/(b+10))-s))

def ahoi_opt(cuts,df_sig,df_bkg):
    ## Implements ahoi optimization given cuts, signal, background
    # First combine the dataframes with a label for signal or background
    df_bkg['Label'] = np.full(len(df_bkg),"b")
    df_sig['Label'] = np.full(len(df_sig),"s")
    
    df = pd.concat([df_bkg,df_sig])
    # Train/testing data
    random_selection = np.random.rand(len(df)) > 0.5
    # masks_list is a 2D array of booleans that tells us if sig/bkg passes cut
    masks_list = []
    # first selection is defined so that all variables pass
    masks_list.insert(0, np.array([random_selection, ~random_selection]))
    # tell if signal or background
    masks_list.insert(1, np.array([(df.Label=="b").values, (df.Label=="s").values]))
    for expr, vals in cuts:
        masks = [df.eval(expr.format(val)).values for val in vals]
        pass_all = np.ones(len(df), dtype=np.bool)
        # the first cut matches all combinations
        masks.insert(0, pass_all)
        masks_list.append(np.array(masks, dtype=np.bool))
    # Using w for the weights
    counts, sumw, sumw2 = ahoi.scan(masks_list, weights=df.w.values)
    # Sum for signal/background/train/test
    sumw_train_b = sumw[0][0]
    sumw_train_s = sumw[0][1]
    sumw_test_b = sumw[1][0]
    sumw_test_s = sumw[1][1]

    # Filling ROC curve for trail/test
    base_b = df[(df.Label=="b")].w.sum()
    base_s = df[(df.Label=="s")].w.sum()
    train_factor = np.count_nonzero(random_selection) / len(df) # we only selected a random subset
    base_b_train = base_b * train_factor
    base_s_train = base_s * train_factor
    fpr_train, tpr_train, roc_ids = ahoi.roc_curve(sumw[0], base_b_train, base_s_train, bins=100)

    test_factor = np.count_nonzero(~random_selection) / len(df)
    base_b_test = base_b * test_factor
    base_s_test = base_s * test_factor
    fpr_test = (sumw_test_b / base_b_test).ravel()[roc_ids]
    tpr_test = (sumw_test_s / base_s_test).ravel()[roc_ids]

    # correctly weighted total rates for signal and background on the ROC curve
    sumw_train_s_roc = sumw_train_s.ravel()[roc_ids] / train_factor
    sumw_train_b_roc = sumw_train_b.ravel()[roc_ids] / train_factor
    sumw_test_s_roc = sumw_test_s.ravel()[roc_ids] / test_factor
    sumw_test_b_roc = sumw_test_b.ravel()[roc_ids] / test_factor
    
    # Plotting ams
    plt.plot(tpr_train, get_ams(sumw_train_s_roc, sumw_train_b_roc), label="train")
    plt.plot(tpr_test, get_ams(sumw_test_s_roc, sumw_test_b_roc), label="test")
    plt.xlabel("true positive rate")
    plt.ylabel("AMS")
    plt.legend()
    plt.savefig("cuts_ams.pdf",format="pdf")
    
    # getting best ams values/cuts
    ## NOTE we may want to use a different metric
    ams_values = get_ams(sumw_test_s_roc, sumw_test_b_roc)
    ams_argmax = np.argmax(ams_values)
    print(ams_values.max)
    print(ams_argmax)
    cut_indices = np.unravel_index(roc_ids[ams_argmax], counts.shape)[2:]
    print(cut_indices)
    return  get_selection(cut_indices,cuts)

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
    
    df_bkg['mu_mass'] = list(np.full((len(df_bkg),2),105.6))
    df_sig = df_sig[(df_sig['trigger_lep']>0) &
                    (df_sig['passJetCleanTight']==1) &
                    (df_sig['n_ph']==1) & 
                    (df_sig['n_mu']==2) &
                    (df_sig['n_bjet']==0)]
    
    # Seems like signal and background should have the same quantities b/c we're testing
    # how cuts can distinguish between signal and background --> SS: yes absolutely correct! :)
    df_sig['mu_mass'] = list(np.full((len(df_sig),2),105.6))

    ## Compute compound variables, like mll, mT(met,ph_pt)...
    ## Info on how to use TLorentzVectors in uproot: https://github.com/scikit-hep/uproot#special-physics-objects-lorentz-vectors
    ## The TLorentzVector class contains a method called "from_ptetaphim": 
    ## https://github.com/scikit-hep/uproot-methods/blob/master/uproot_methods/classes/TLorentzVector.py#L978
    df_bkg = calcVars(df_bkg)

    df_sig = calcVars(df_sig)

    ## Plot some of the variables you calculated to see if they make sense
    ## including lep1.pt, lep2.pt, ph.pt, etc
    # list of variables to make histograms of
    varCuts = ['met_tight_tst_et','met_tight_tst_phi','ph_pt','mT','dPhiLepMet','AbsPt','Ptll','mllg','lep1pt','lep2pt','mll']
    #units = ['GeV','Radians','GeV','GeV','Radians','GeV','GeV','GeV','GeV','GeV']
    #for i in range(0,len(varCuts)):
    #makePlots(df_bkg,df_sig,'mll','GeV')
    
    # Ahoi -> stores large numpy arrays in memory so can't do large combinations locally
    # More systematic way to actually define cuts?
    # Possible variables/ranges to test based on histograms
    ncuts = 3
    cuts = [
        ("met_tight_tst_et > {}", [110,150,180,200]),
        ("ph_pt > {}", [50,100,150,200,325]),
        ("mT > {}", [25,50,100,150,200]),
        ("dPhiLepMet > {}", list(np.linspace(0.1,2.5,10))),
        ("AbsPt < {}", list(np.linspace(0.1,1,10))),
        ("Ptll > {}", list(np.linspace(20,350,ncuts))),
        ("mllg > {}", list(np.linspace(25,200,ncuts))),
        ("lep1pt > {}", list(np.linspace(0,50,ncuts))),
        ("lep2pt > {}", list(np.linspace(0,50,ncuts))),
        ("mll > {}", list(np.linspace(10,70,ncuts))),
        ("mll < {}", list(np.linspace(110,200,ncuts)))
        ]
    # Testing a few cuts
    ncuts = 20
    cuts_test = [
        ("lep1pt > {}", list(np.linspace(0,50,ncuts,dtype=int))),
        ("lep2pt > {}", list(np.linspace(0,50,ncuts,dtype=int))),
        ("mll > {}", list(np.linspace(10,70,ncuts,dtype=int))),
        ("mll < {}", list(np.linspace(110,200,ncuts,dtype=int))),
        ("mllg > {}", list(np.linspace(25,200,ncuts,dtype=int)))
        ]
    ahoi_test = ahoi_opt(cuts_test,df_sig,df_bkg)
    print(ahoi_test)
    # implementing ahoi
    # randomly select 50% of signal and background for train/test data
    
if __name__ == '__main__':
    main()
