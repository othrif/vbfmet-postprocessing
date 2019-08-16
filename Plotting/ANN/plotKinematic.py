#!/usr/bin/env python
"""
Train MLP classifer to identify vector-boson fusion Higgs against background
"""
__author__ = "Sid Mau, Doug Schaefer"

###############################################################################
# Import libraries
##################

# Scipy
import numpy as np

# Matplotlib
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

###############################################################################

###############################################################################
# Global variabls
#################

training_name = '_zstrong'

###############################################################################

###############################################################################
# Load data
###########

# VBFH125 (signal)
VBFH125 = np.load('VBFH125.npy')

# Z_strong (background)
Z_strong = np.load('Z_strong.npy')

# Z_EWK (background)
Z_EWK = np.load('Z_EWK.npy')

# ttbar (background)
ttbar = np.load('ttbar.npy')

# W_strong (background)
W_strong = np.load('W_strong.npy')

###############################################################################

###############################################################################
# Select variables
##################

COLS  = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]']
COLS += ['met_soft_tst_et']
COLS += ['jet_eta[0]', 'jet_eta[1]', 'jet_phi[0]', 'jet_phi[1]']
COLS += ['n_jet', 'maxCentrality', 'max_mj_over_mjj']
COLS += ['met_cst_jet', 'met_tight_tst_et', 'met_tenacious_tst_et']
###COLS += ['j3_centrality[0]', 'j3_min_mj_over_mjj', 'jet_pt[2]'] # 'j3_centrality[1]']
#COLS += ['jet_TrackWidth[0]', 'jet_TrackWidth[1]', 'jet_NTracks[0]', 'jet_NTracks[1]']

print('cols = {}'.format(COLS))

###############################################################################

for col in COLS:
    plt.figure()
    plt.hist(VBFH125[col].astype(float), density=True, bins=50, histtype='step', label='VBFH125')
    plt.hist(Z_strong[col].astype(float), density=True, bins=50, histtype='step', label='Z_strong')
    plt.legend(loc='upper right')
    plt.title(col)
    plt.savefig('{}.png'.format(col), bbox_inches='tight', rasterized=False)
