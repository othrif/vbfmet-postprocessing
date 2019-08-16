#!/usr/bin/env python
"""
Train MLP classifer to identify vector-boson fusion Higgs against background
"""
__author__ = "Sid Mau, Doug Schaefer"

###############################################################################
# Import libraries
##################

# Scikit-learn
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import preprocessing
from sklearn import decomposition
from sklearn.utils import class_weight
from sklearn.externals import joblib

# Scipy
import numpy as np
import numpy.lib.recfunctions as recfn

###############################################################################

###############################################################################
# Global variabls
#################

training_name = '_zstrong_ttbar_wstrong_zewk_15var'
#training_name = '_zstrong_ttbar_wstrong_zewk_7var'
#training_name = '_zstrong_15var'

###############################################################################

###############################################################################
# Load data
###########

# VBFH125 (signal)
VBFH125 = np.load('VBFH125.npy')
label_VBFH125 = np.ones(len(VBFH125))
#label_VBFH125 = np.array(['VBFH125' for e in VBFH125])
VBFH125_labelled = recfn.rec_append_fields(VBFH125, 'label', label_VBFH125)
#VBFH125_labelled['w']*=10.0 # adding weight to center the distribution
np.random.shuffle(VBFH125_labelled)

# Z_strong (background)
Z_strong = np.load('Z_strong.npy')
label_Z_strong = np.zeros(len(Z_strong))
#label_Z_strong = np.array(['Z_strong' for e in Z_strong])
Z_strong_labelled = recfn.rec_append_fields(Z_strong, 'label', label_Z_strong)
np.random.shuffle(Z_strong_labelled)

# Z_EWK (background)
Z_EWK = np.load('Z_EWK.npy')
label_Z_EWK = np.zeros(len(Z_EWK))
#label_Z_EWK = np.array(['Z_EWK' for e in Z_EWK])
Z_EWK_labelled = recfn.rec_append_fields(Z_EWK, 'label', label_Z_EWK)
np.random.shuffle(Z_EWK_labelled)

# ttbar (background)
ttbar = np.load('ttbar.npy')
label_ttbar = np.zeros(len(ttbar))
#label_ttbar = np.array(['ttbar' for e in ttbar])
ttbar_labelled = recfn.rec_append_fields(ttbar, 'label', label_ttbar)
np.random.shuffle(ttbar_labelled)

# W_strong (background)
W_strong = np.load('W_strong.npy')
label_W_strong = np.zeros(len(W_strong))
#label_W_strong = np.array(['W_strong' for e in W_strong])
W_strong_labelled = recfn.rec_append_fields(W_strong, 'label', label_W_strong)
np.random.shuffle(W_strong_labelled)

###############################################################################

###############################################################################
# Concatenate and shuffle data
##############################

#Z_strong_labelled = Z_strong_labelled[:round(len(VBFH125_labelled)*3/4)]
#Z_EWK_labelled = Z_EWK_labelled[:round(len(VBFH125_labelled)*1/8)]
#W_strong_labelled = W_strong_labelled[:round(len(VBFH125_labelled)*1/16)]
#ttbar_labelled = ttbar_labelled[:round(len(VBFH125_labelled)*1/16)]

#Z_strong_labelled = Z_strong_labelled[:len(Z_strong_labelled)]
#data = np.concatenate([VBFH125_labelled, Z_strong_labelled])
#data = np.concatenate([VBFH125_labelled, Z_strong_labelled, ttbar_labelled])
#data = np.concatenate([VBFH125_labelled, Z_strong_labelled, ttbar_labelled, W_strong_labelled])
data = np.concatenate([VBFH125_labelled, Z_strong_labelled, ttbar_labelled, W_strong_labelled, Z_EWK_labelled])
np.random.shuffle(data) # shuffle data

###############################################################################

###############################################################################
# Select variables
##################

COL_7 = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]', 'met_soft_tst_et']
COL_15 = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]', 'met_soft_tst_et', 'jet_phi[0]', 'jet_phi[1]', 'n_jet', 'maxCentrality', 'max_mj_over_mjj', 'met_cst_jet', 'met_tight_tst_et', 'met_tenacious_tst_et']

#COLS  = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]']
#COLS += ['met_soft_tst_et']
##COLS += ['jet_eta[0]', 'jet_eta[1]', 'jet_phi[0]', 'jet_phi[1]']
#COLS += ['jet_phi[0]', 'jet_phi[1]']
#COLS += ['n_jet', 'maxCentrality', 'max_mj_over_mjj']
##COLS += ['maxCentrality', 'max_mj_over_mjj']
#COLS += ['met_cst_jet', 'met_tight_tst_et', 'met_tenacious_tst_et']
####COLS += ['j3_centrality[0]', 'j3_min_mj_over_mjj', 'jet_pt[2]'] # 'j3_centrality[1]']
##COLS += ['jet_TrackWidth[0]', 'jet_TrackWidth[1]', 'jet_NTracks[0]', 'jet_NTracks[1]']
COLS = COL_7

print('COLS = {}'.format(COLS))

# select n_jet < 4 due to some variables problems
#data = data[data['n_jet'] < 4]
#data = data[data['n_jet'] == 2]

#data['jet_pt[2]'][np.where(data['n_jet'] == 2)]          = 0
#data['j3_centrality[0]'][np.where(data['n_jet'] == 2)]   = 0
##data['j3_centrality[1]'][np.where(data['n_jet'] == 2)]   = 0
#data['j3_min_mj_over_mjj'][np.where(data['n_jet'] == 2)] = 0

###############################################################################

extra_cols = ['jet_phi[0]', 'jet_phi[1]', 'n_jet', 'maxCentrality', 'max_mj_over_mjj', 'met_cst_jet', 'met_tight_tst_et', 'met_tenacious_tst_et']
for col in extra_cols:
    COLS += [col]
    num_cols = len(COLS)
    print('{} vars'.format(num_cols))
    training_name = '_zstrong_ttbar_wstrong_zewk_{}var'.format(num_cols)

    ###############################################################################
    # Split train/test data
    #######################
    
    data_train, data_test, label_train, label_test = train_test_split(data, data['label'], test_size=0.2, random_state=0, shuffle=True, stratify=data['label']) # 80%/20% train/test split
    X_train = data_train[COLS] # use only COLS
    X_test = data_test[COLS] # use only COLS
    y_train = label_train
    y_test = label_test
    w_train = data_train['w'] # weights
    #w_train = np.where(label_train == 0, data_train['w'], 3*data_train['w'])
    w_test = data_test['w'] # weights
    #w_test = np.where(label_test == 0, data_test['w'], 3*data_test['w'])
    
    X_train = X_train.astype([(name, '<f8') for name in X_train.dtype.names]).view(('<f8', len(X_train.dtype.names))) # convert from structured array to unstructed array
    X_test = X_test.astype([(name, '<f8') for name in X_test.dtype.names]).view(('<f8', len(X_test.dtype.names))) # convert from structured array to unstructed array
    
    ###############################################################################
    
    ###############################################################################
    # Preprocess data
    #################
    
    # Make scaler for train data
    scaler = preprocessing.RobustScaler(with_centering=True, with_scaling=True, quantile_range=(25, 75)).fit(X_train) # scaler to standardize data
    #scaler = preprocessing.RobustScaler(with_centering=True, with_scaling=True, quantile_range=(0, 100)).fit(X_train) # scaler to standardize data
    #scaler = preprocessing.MinMaxScaler().fit(X_train) # scaler to standardize data
    #scaler = preprocessing.StandardScaler().fit(X_train) # scaler to standardize data
    #scaler = preprocessing.QuantileTransformer(output_distribution='uniform').fit(X_train) # scaler to standardize data
    X_train = scaler.transform(X_train) # apply to train data
    X_test = scaler.transform(X_test) # apply to test data
    
    #pca = decomposition.PCA(n_components=None, whiten=True).fit(X_train)
    #X_train = pca.transform(X_train)
    #X_test = pca.transform(X_test)
    
    # Save it
    scaler_filename = "scaler"+training_name+".save"
    joblib.dump(scaler, scaler_filename) 
    
    #np.save("X_test" + training_name + ".npy", X_test)
    #np.save("X_train" + training_name + ".npy", X_train)
    #np.save("y_test" + training_name + ".npy", y_test)
    #np.save("y_train" + training_name + ".npy", y_train)
    np.savez("data" + training_name, X_test=X_test, X_train=X_train, y_test=y_test, y_train=y_train, w_test=w_test, w_train=w_train)
