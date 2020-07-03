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
import glob
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
    df_sample = []
    for path, file, start, stop, entry in up.iterate(
            infiles+treename+"*.root",
            treename,
            branches=branches,
            reportpath=True, reportfile=True, reportentries=True):

        print('==> Processing sample: %s ...'%path)
        tree = up.open(path)[treename]

        df_sample.append(tree.pandas.df(branches,flatten=False))
    df_sample = pd.concat(df_sample)
    return df_sample

def calcmT(met,ph):
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
    # Converting weights to true yield
    df['w'] = df['w'] * 36000
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

def makePlots(df_bkg,df_sig,var,units,cuts):
    ### Plot some of the distributions for the signal and bkg
    fig,ax = plt.subplots(1,1)
    bkg = np.array(df_bkg[var])
    sig = np.array(df_sig[var])
    if var == 'ph_pt':
        bkg = np.concatenate(np.asarray(df_bkg[var])).ravel()
        sig = np.concatenate(np.asarray(df_sig[var])).ravel()
    #max_val = max(np.concatenate([bkg,sig]))
    # scaling based on signal data
    max_val = max(sig)
    #print(var,min(sig),max_val)
    if var == 'mll':
        xmin = 60
        xmax = 120
    else: 
        xmin = 0
        xmax = max_val
    
    if cuts is not None:
        for cut in cuts:
            if var == cut[0].split()[0]: 
                is_lowerbound = ">" in cut[0]
                for v in cut[1]:
                    line = ax.axvline(v,color='black',linestyle='--')
                    ax.legend([line], ["lower bound" if is_lowerbound else "upper bound"])
            
    ax.hist(bkg, weights = df_bkg['w'].to_numpy(), bins=50, range=(xmin, xmax), histtype='step', color='Red',label='bkg')
    ax.hist(sig, weights = df_sig['w'].to_numpy(), bins=50, range=(xmin, xmax), histtype='step', color='Blue',label='sig')
    ax.set_xlabel(var+' [' + units + ']')
    ax.set_ylabel('Events')
    ax.set_yscale('log')
    plt.savefig("w_hist_" + var+ ".pdf",format="pdf")

def get_selection(multi_index,cuts):
    ## Selects the cut values from the list of cuts after ahoi optimization 
    expr_list = []
    for i, (expr, vals) in zip(multi_index, cuts):
        if i == 0:
            continue
        expr_list.append("({})".format(expr.format(vals[i-1])))
    return expr_list

def get_metric(s, b,metric):
    ## Metric for optimization, variety of different options
    if metric == "reg":
        return np.sqrt(2*((s+b)*np.log(1+s/b)-s))
    # Adding 10 for regularization, not sure why
    if metric == "ams":
        return np.sqrt(2*((s+b+10)*np.log(1+s/(b+10))-s))
    if metric == "sb":
        return s/b
    if metric == "ssqrt(b)":
        # added absolute value b/c this is apparently negative?
        return s/np.sqrt(np.abs(b))

def ahoi_opt(cuts,df_sig,df_bkg):
    ## Implements ahoi optimization given cuts, signal, background
    # First combine the dataframes with a label for signal or background
    df_bkg['Label'] = np.full(len(df_bkg),"b")
    df_sig['Label'] = np.full(len(df_sig),"s")
    
    df = pd.concat([df_bkg,df_sig])
    # masks_list is a 2D array of booleans that tells us if sig/bkg passes cut
    masks_list = []
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
    sumw_s = sumw[1]
    sumw_b = sumw[0]
    # Filling ROC curve for accuracy
    base_b = df[(df.Label=="b")].w.sum()
    base_s = df[(df.Label=="s")].w.sum()
    fpr, tpr, roc_ids = ahoi.roc_curve(sumw, base_b, base_s, bins=100)
    # total rates for signal and background on the ROC curve
    sumw_s_roc = sumw_s.ravel()[roc_ids]
    sumw_b_roc = sumw_b.ravel()[roc_ids]

    metrics = ["reg","ams","sb","ssqrt(b)"]
    selections = []

    for m in metrics:
        vals = get_metric(sumw_s_roc, sumw_b_roc, m)
        argmax = np.argmax(vals)
        cut_indices = np.unravel_index(roc_ids[argmax], counts.shape)[2:]
        selections.append(get_selection(cut_indices,cuts))
        # Plotting metric
        fig,ax = plt.subplots(1,1)
        ax.plot(tpr, get_metric(sumw_s_roc, sumw_b_roc,m))
        ax.set_xlabel("True Positive Rate")
        ax.set_ylabel(m)
        #ax.legend()
        plt.savefig("cuts_"+ m + ".pdf", format = "pdf")
    
    return selections
        
def main(): 
    """ Run script"""
    options = getArgumentParser().parse_args()
    ### Make all the bkg and signal dataframes
    ## Z+jets
    df_zjets  = sampleDataframe(options.indir,"Z_strongNominal")
    df_zjets  = df_zjets.append(sampleDataframe(options.indir,"Z_EWKNominal"))
    ## Z+photon
    df_zgamma = sampleDataframe(options.indir,"Zg_strongNominal")

    ## ttbar/single top/Wt/ttbar+V
    df_top    = sampleDataframe(options.indir,"ttbarNominal")
    df_top    = df_top.append(sampleDataframe(options.indir,"ttVNominal"))

    ## Triboson
    df_VVV    = sampleDataframe(options.indir,"VVVNominal")
    df_VVV    = df_VVV.append(sampleDataframe(options.indir,"VVyNominal"))

    ## Diboson
    df_VV     = sampleDataframe(options.indir,"VVNominal")
    df_VV     = df_VV.append(sampleDataframe(options.indir,"VV_ewkNominal"))
    df_VV     = df_VV.append(sampleDataframe(options.indir,"ggZZNominal"))
    df_VV     = df_VV.append(sampleDataframe(options.indir,"ggWWNominal"))

    ## H->Zy
    df_HZy    = sampleDataframe(options.indir,"ggH125ZyNominal")
    df_HZy    = df_HZy.append(sampleDataframe(options.indir,"ttH125ZyNominal"))
    df_HZy    = df_HZy.append(sampleDataframe(options.indir,"VBFH125ZyNominal"))
    df_HZy    = df_HZy.append(sampleDataframe(options.indir,"VH125ZyNominal"))

    ## signal
    df_sig = sampleDataframe(options.indir,"HyGrNominal")


    ## Remove overlapping Z+jets events
    df_zjets = df_zjets[df_zjets['in_vy_overlap'] > 0]
    ## Make collective Z+jets/Z+photon bkg dataframe
    df_bkg = df_zjets
    df_bkg = df_bkg.append(df_zgamma).append(df_top).append(df_VVV).append(df_VV).append(df_HZy)
    ##df_bkg = pd.concat(df_bkg,df_top,df_VVV,df_VV,df_HZy)
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
    df_sig['mu_mass'] = list(np.full((len(df_sig),2),105.6))
    ## The TLorentzVector class contains a method called "from_ptetaphim": 
    ## https://github.com/scikit-hep/uproot-methods/blob/master/uproot_methods/classes/TLorentzVector.py#L978
    # Apply more preliminary cuts
    df_bkg = calcVars(df_bkg)
    df_bkg = df_bkg[(df_bkg['mll'] > 66) &
                    (df_bkg['mll'] < 116) &
                    (df_bkg['lep1pt'] > 26)]
    df_sig = calcVars(df_sig)
    df_sig = df_sig[(df_sig['mll'] > 66) &
                    (df_sig['mll'] < 116) &
                    (df_sig['lep1pt'] > 26)]

    # list of variables to make histograms of
    varCuts = ['met_tight_tst_et','met_tight_tst_phi','ph_pt','mT','dPhiLepMet','AbsPt','Ptll','mllg','lep1pt','lep2pt','mll']
    units = ['GeV','Radians','GeV','GeV','Radians','GeV','GeV','GeV','GeV','GeV','GeV']
    
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
    ncuts = 10
    cuts_test = [
        ("lep1pt > {}", list(np.linspace(30,40,ncuts,dtype=int))),
        ("lep2pt > {}", list(np.linspace(5,15,ncuts,dtype=int))),
        ("mll > {}", list(np.linspace(80,90,ncuts,dtype=int))),
        ("mll < {}", list(np.linspace(100,110,ncuts,dtype=int))),
        ("mllg > {}", list(np.linspace(85,100,ncuts,dtype=int))),
        ("AbsPt < {}", list(np.linspace(27,37,ncuts,dtype=int)))
        ]
    
    cuts_test2 = [
        ("lep2pt > {}", list(np.linspace(7,15,ncuts,dtype=int))),
        ("met_tight_tst_et > {}", list(np.linspace(50,110,ncuts,dtype=int))),
        ("mll > {}", list(np.linspace(66,80,ncuts,dtype=int))),   
        ("mllg > {}", list(np.linspace(85,100,ncuts,dtype=int))),   
        ("dPhiLepMet > {}", list(np.linspace(0,1.5,ncuts,dtype=int))),
        ("Ptll > {}", list(np.linspace(0,100,ncuts,dtype=int))),
        ("AbsPt < {}", list(np.linspace(10,30,ncuts,dtype=int)))        
    ]
    for i in range(0,len(varCuts)):
        makePlots(df_bkg,df_sig,varCuts[i],units[i],cuts=cuts_test2)

    ahoi_test = ahoi_opt(cuts_test2,df_sig,df_bkg)
    print(ahoi_test)
    
if __name__ == '__main__':
    main()
