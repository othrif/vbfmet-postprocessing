#!/usr/bin/env python
"""
Train MLP classifer to identify vector-boson fusion Higgs against background
"""
__author__ = "Sid Mau, Doug Schaefer"

###############################################################################
# Import libraries
##################

# Tensorflow and Keras
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM, Conv1D, Flatten
from keras import optimizers
#from keras import regularizers
import keras.backend as K
from custom_loss import *
from keras.callbacks import ModelCheckpoint

# Scikit-learn
import sklearn.metrics as metrics
#from sklearn.metrics import classification_report, average_precision_score, precision_recall_curve, confusion_matrix
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import preprocessing
from sklearn import decomposition
from sklearn.utils import class_weight
from sklearn.externals import joblib
#from keras.wrappers.scikit_learn import KerasClassifier
#from sklearn.model_selection import GridSearchCV

# Scipy
from scipy import stats
import numpy as np
import numpy.lib.recfunctions as recfn

# Matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

###############################################################################

###############################################################################
# Global variabls
#################

#training_name = '_zstrong_ttbar_wstrong_zewk_15var'
training_name = '_zstrong_ttbar_wstrong_zewk_7var'
#training_name = '_zstrong_15var'

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

################################################################################
#
#def separation(y_true, y_pred):
#    # https://root.cern.ch/doc/v606/Tools_8cxx_source.html#l00136
#    # (1/2) Int_-oo…+oo { (S^2(x) - B^2(x))/(S(x) + B(x)) dx }
#
#    sig_true = (y_true == 1)
#    bkg_true = (y_true == 0)
#
#    sig_pred = y_pred[sig_true]
#    bkg_pred = y_pred[bkg_true]
#
#    nbins = 51
#    bins = np.linspace(0, 1, nbins)
#    sig_counts, edges = np.histogram(sig_pred, bins=bins, density=True) #, weights=wsignal_test)
#    bkg_counts, edges = np.histogram(bkg_pred, bins=bins, density=True) #, weights=wbackground_test)
#    width = np.diff(edges)
#
#    sep = (1/2) * np.sum([(s**2 - b**2)/(s+b)*width[0] for s, b in zip(sig_counts, bkg_counts)])
#
#    return(-np.abs(sep))
#
#
################################################################################
## Load data
############
#
## VBFH125 (signal)
#VBFH125 = np.load('VBFH125.npy')
#label_VBFH125 = np.ones(len(VBFH125))
##label_VBFH125 = np.array(['VBFH125' for e in VBFH125])
#VBFH125_labelled = recfn.rec_append_fields(VBFH125, 'label', label_VBFH125)
##VBFH125_labelled['w']*=10.0 # adding weight to center the distribution
#np.random.shuffle(VBFH125_labelled)
#
## Z_strong (background)
#Z_strong = np.load('Z_strong.npy')
#label_Z_strong = np.zeros(len(Z_strong))
##label_Z_strong = np.array(['Z_strong' for e in Z_strong])
#Z_strong_labelled = recfn.rec_append_fields(Z_strong, 'label', label_Z_strong)
#np.random.shuffle(Z_strong_labelled)
#
## Z_EWK (background)
#Z_EWK = np.load('Z_EWK.npy')
#label_Z_EWK = np.zeros(len(Z_EWK))
##label_Z_EWK = np.array(['Z_EWK' for e in Z_EWK])
#Z_EWK_labelled = recfn.rec_append_fields(Z_EWK, 'label', label_Z_EWK)
#np.random.shuffle(Z_EWK_labelled)
#
## ttbar (background)
#ttbar = np.load('ttbar.npy')
#label_ttbar = np.zeros(len(ttbar))
##label_ttbar = np.array(['ttbar' for e in ttbar])
#ttbar_labelled = recfn.rec_append_fields(ttbar, 'label', label_ttbar)
#np.random.shuffle(ttbar_labelled)
#
## W_strong (background)
#W_strong = np.load('W_strong.npy')
#label_W_strong = np.zeros(len(W_strong))
##label_W_strong = np.array(['W_strong' for e in W_strong])
#W_strong_labelled = recfn.rec_append_fields(W_strong, 'label', label_W_strong)
#np.random.shuffle(W_strong_labelled)
#
################################################################################
#
################################################################################
## Concatenate and shuffle data
###############################
#
##Z_strong_labelled = Z_strong_labelled[:len(Z_strong_labelled)]
##data = np.concatenate([VBFH125_labelled, Z_strong_labelled])
##data = np.concatenate([VBFH125_labelled, Z_strong_labelled, ttbar_labelled])
##data = np.concatenate([VBFH125_labelled, Z_strong_labelled, ttbar_labelled, W_strong_labelled])
#data = np.concatenate([VBFH125_labelled, Z_strong_labelled, ttbar_labelled, W_strong_labelled, Z_EWK_labelled])
#np.random.shuffle(data) # shuffle data
#
################################################################################
#
################################################################################
## Select variables
###################
#
#COL_7 = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]', 'met_soft_tst_et']
#COL_15 = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]', 'met_soft_tst_et', 'jet_phi[0]', 'jet_phi[1]', 'n_jet', 'maxCentrality', 'max_mj_over_mjj', 'met_cst_jet', 'met_tight_tst_et', 'met_tenacious_tst_et']
#
##COLS  = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]']
##COLS += ['met_soft_tst_et']
###COLS += ['jet_eta[0]', 'jet_eta[1]', 'jet_phi[0]', 'jet_phi[1]']
##COLS += ['jet_phi[0]', 'jet_phi[1]']
##COLS += ['n_jet', 'maxCentrality', 'max_mj_over_mjj']
###COLS += ['maxCentrality', 'max_mj_over_mjj']
##COLS += ['met_cst_jet', 'met_tight_tst_et', 'met_tenacious_tst_et']
#####COLS += ['j3_centrality[0]', 'j3_min_mj_over_mjj', 'jet_pt[2]'] # 'j3_centrality[1]']
###COLS += ['jet_TrackWidth[0]', 'jet_TrackWidth[1]', 'jet_NTracks[0]', 'jet_NTracks[1]']
#COLS = COL_15
#
#print('COLS = {}'.format(COLS))
#
## select n_jet < 4 due to some variables problems
##data = data[data['n_jet'] < 4]
#
##data['jet_pt[2]'][np.where(data['n_jet'] == 2)]          = 0
##data['j3_centrality[0]'][np.where(data['n_jet'] == 2)]   = 0
###data['j3_centrality[1]'][np.where(data['n_jet'] == 2)]   = 0
##data['j3_min_mj_over_mjj'][np.where(data['n_jet'] == 2)] = 0
#
################################################################################
#
################################################################################
## Split train/test data
########################
#
#data_train, data_test, label_train, label_test = train_test_split(data, data['label'], test_size=0.2, random_state=0, shuffle=True, stratify=data['label']) # 80%/20% train/test split
#X_train = data_train[COLS] # use only COLS
#X_test = data_test[COLS] # use only COLS
#y_train = label_train
#y_test = label_test
#w_train = data_train['w'] # weights
##w_train = np.where(label_train == 0, data_train['w'], 3*data_train['w'])
#w_test = data_test['w'] # weights
##w_test = np.where(label_test == 0, data_test['w'], 3*data_test['w'])
#
#X_train = X_train.astype([(name, '<f8') for name in X_train.dtype.names]).view(('<f8', len(X_train.dtype.names))) # convert from structured array to unstructed array
#X_test = X_test.astype([(name, '<f8') for name in X_test.dtype.names]).view(('<f8', len(X_test.dtype.names))) # convert from structured array to unstructed array
#
################################################################################
#
################################################################################
## Preprocess data
##################
#
## Make scaler for train data
#scaler = preprocessing.RobustScaler(with_centering=True, with_scaling=True, quantile_range=(25, 75)).fit(X_train) # scaler to standardize data
##scaler = preprocessing.RobustScaler(with_centering=True, with_scaling=True, quantile_range=(0, 100)).fit(X_train) # scaler to standardize data
##scaler = preprocessing.MinMaxScaler().fit(X_train) # scaler to standardize data
##scaler = preprocessing.StandardScaler().fit(X_train) # scaler to standardize data
##scaler = preprocessing.QuantileTransformer(output_distribution='uniform').fit(X_train) # scaler to standardize data
#X_train = scaler.transform(X_train) # apply to train data
#X_test = scaler.transform(X_test) # apply to test data
#
##pca = decomposition.PCA(n_components=None, whiten=True).fit(X_train)
##X_train = pca.transform(X_train)
##X_test = pca.transform(X_test)
#
## Save it
#scaler_filename = "scaler"+training_name+".save"
#joblib.dump(scaler, scaler_filename) 
#
#np.save("X_test" + training_name + ".npy", X_test)
#np.save("X_train" + training_name + ".npy", X_train)
#np.save("y_test" + training_name + ".npy", y_test)
#np.save("y_train" + training_name + ".npy", y_train)
#np.savez("data" + training_name, X_test=X_test, X_train=X_train, y_test=y_test, y_train=y_train, w_test=w_test, w_train=w_train)
#
#################################################################################
#
#################################################################################
### Custom loss functions
#########################
##
### https://towardsdatascience.com/handling-imbalanced-datasets-in-deep-learning-f48407a0e758
##def focal_loss(y_true, y_pred):
##    gamma = 0.1 #2.0
##    alpha = 0.95 #0.25 #0.95
##    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
##    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
##    return(-K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1))-K.sum((1-alpha) * K.pow( pt_0, gamma) * K.log(1. - pt_0)))
##
### signal efficiency
##def sig_loss(y_true, y_pred):
##    #for (signal):
##    #    loss +=  (s / sqrt(7*b)) )**2;
##    #loss = math.sqrt(1/loss);
##    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
##    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
##    sig = K.sum(((1.-pt_1) / K.pow(7*(1-pt_0), 0.5))**2)
##    loss = K.pow(1/sig, 0.5)
##    return(loss)
##
### signal efficiency
##def sig_eff(y_true, y_pred):
##    #for (signal):
##    #    loss +=  (s / sqrt(7*b)) )**2;
##    #loss = math.sqrt(1/loss);
##    #pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
##    #pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
##    #sig_eff = K.pow(K.sum((pt_1 / K.pow(7*(1-pt_0), 0.5))**2), 0.5)
##    sig = tf.where(tf.equal(y_true, 1), y_pred, tf.zeros_like(y_pred))
##    bkg = tf.where(tf.equal(y_true, 0), y_pred, tf.ones_like(y_pred))
##    sig = K.sum(sig)
##    bkg = K.sum(1-bkg)
##    sig_eff = sig/K.pow(bkg, 0.5)
##    return(sig_eff)
##
##def custom_loss(y_true, y_pred):
##    alpha = 0.8
##    focal = focal_loss(y_true, y_pred)
##    sig = 1/sig_eff(y_true, y_pred)
##    loss = K.pow(K.pow(alpha*focal, 2) + K.pow((1-alpha)*sig, 2), 0.5)
##    return(loss)
##
#################################################################################

extra_cols = ['jet_phi[0]', 'jet_phi[1]', 'n_jet', 'maxCentrality', 'max_mj_over_mjj', 'met_cst_jet', 'met_tight_tst_et', 'met_tenacious_tst_et']
for col in extra_cols:
    COLS += [col]
    num_cols = len(COLS)
    print('{} vars'.format(num_cols))
    training_name = '_zstrong_ttbar_wstrong_zewk_{}var'.format(num_cols)


    data = np.load("data" + training_name + ".npz")
    X_train = data['X_train']
    X_test = data['X_test']
    y_train = data['y_train']
    y_test = data['y_test']
    w_train = data['w_train']
    w_test = data['w_test']
    
    ###############################################################################
    # Weigh classes
    ###############
    
    # This helps address the imbalanced nature of the data
    class_weights = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
    
    ###############################################################################
    
    ###############################################################################
    # Define the classifier model
    #############################
    
    # Build the model
    model = Sequential()
    model.add(Dense(2*len(COLS), kernel_initializer='normal', activation='relu', input_dim=len(COLS)))
    model.add(Dropout(0.2))
    model.add(Dense(2*len(COLS), kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(len(COLS), kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    
    # Compile the model
    model.compile(optimizer='nadam',
                  loss='binary_crossentropy',
                  metrics=['accuracy', sig_eff])
    #model.compile(optimizer='rmsprop',
    #              loss='binary_crossentropy',
    #              metrics=['accuracy', sig_eff])
    #
    print(model.summary())
    
    model_filename = 'model'+training_name+'.hdf5'
    mcp = ModelCheckpoint(model_filename, monitor='val_loss',
                          save_best_only=True, save_weights_only=False,
                          verbose=1)
    
    ###############################################################################
    
    ###############################################################################
    # Train the classifier model
    ############################
    
    # Fit the model
    #model.fit(X_train, y_train, validation_split=0.2, epochs=10, batch_size=128)
    #model.fit(X_train, y_train, validation_split=0.2, epochs=20, batch_size=128, sample_weight=w_train)
    #model.fit(X_train, y_train, validation_split=0.2, epochs=20, batch_size=128, class_weight=class_weights)
    model.fit(X_train, y_train,
              validation_split=0.2,
              epochs=10, batch_size=32,
              callbacks=[mcp],
              class_weight=class_weights, sample_weight=w_train) #batch_size=64, 8
    
    ## Save the model
    #model_filename = 'model'+training_name+'.h5'
    #model.save(model_filename)
    
    ###############################################################################
    
    ################################################################################
    ## Permutation importance
    #########################
    #
    ## score predictions
    #score_test = model.predict(X_test)
    #
    ## define sig/bkg regions
    #sig_test = (y_test == 1)
    #bkg_test = (y_test == 0)
    #
    ## select sig/bkg for train/test and weights
    #signal_test = score_test[sig_test]
    ##wsignal_test = w_test[sig_test]
    #background_test = score_test[bkg_test]
    ##wbackground_test = w_test[bkg_test]
    #
    #print('VARIABLE,SIGNAL,BACKGROUND')
    #print('\"{}\",{},{}'.format('baseline', np.median(signal_test), np.median(background_test)))
    #
    #for i in range(len(COLS)):
    #    X_test_modified = np.copy(X_test)
    #    X_test_modified[:,i] += 0.01
    #    score_test = model.predict(X_test_modified)
    #
    #    # define sig/bkg regions
    #    sig_test = (y_test == 1)
    #    bkg_test = (y_test == 0)
    #    
    #    # select sig/bkg for train/test and weights
    #    signal_test = score_test[sig_test]
    #    #wsignal_test = w_test[sig_test]
    #    background_test = score_test[bkg_test]
    #    #wbackground_test = w_test[bkg_test]
    #    
    #    print('\"{}\",{},{}'.format(COLS[i], np.median(signal_test), np.median(background_test)))
    #
    #test = model.evaluate(X_test, y_test, verbose=0)
    #loss = test[0]
    #acc = test[1]
    #print('VARIABLE,LOSS,ACCURACY')
    #print('\"{}\",{},{}'.format('baseline', loss, acc))
    #
    #for i in range(len(COLS)):
    #    X_test_shuffled = np.copy(X_test)
    #    np.random.shuffle(X_test_shuffled[:,i])
    #    score_test = model.predict(X_test_shuffled)
    #    
    #    # define sig/bkg regions
    #    sig_test = (y_test == 1)
    #    bkg_test = (y_test == 0)
    #    
    #    # select sig/bkg for train/test and weights
    #    signal_test = score_test[sig_test]
    #    #wsignal_test = w_test[sig_test]
    #    background_test = score_test[bkg_test]
    #    #wbackground_test = w_test[bkg_test]
    #    
    #    test = model.evaluate(X_test_shuffled, y_test, verbose=0)
    #    loss = test[0]
    #    acc = test[1]
    #    print('\"{}\",{},{}'.format(COLS[i], loss, acc))
    #    
    ################################################################################
    #
    ################################################################################
    ## Performance Plots
    ####################
    #
    ### quick metrics
    #y_pred = model.predict(np.array(X_test))
    ##y_pred_bool = np.argmax(y_pred, axis=1)
    ##y_pred_bool = np.where(y_pred > 0.3, 1, 0)
    ##print(classification_report(y_test, y_pred_bool))
    ##print(confusion_matrix(y_test, y_pred_bool))
    #
    ## calculate the fpr and tpr for all thresholds of the classification
    #y_pred = model.predict(np.array(X_test))
    #fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
    #roc_auc = metrics.auc(fpr, tpr)
    #
    ## plot ROC curve
    #plt.figure()
    #plt.fill_between(fpr, 0, tpr, facecolor='b', alpha=0.3, label='AUC = {:0.3f}'.format(roc_auc), zorder=0)
    #plt.plot([0, 1], [0, 1], c='gray', lw=1, ls='--', zorder=1)
    #plt.plot(fpr, tpr, c='b', lw=2, ls='-', label='ROC Curve', zorder=2)
    #plt.legend(loc='upper left')
    #plt.xlim([0, 1])
    #plt.ylim([0, 1])
    #plt.xlabel('False Positive Rate')
    #plt.ylabel('True Positive Rate')
    #plt.title('Receiver Operating Characteristic (ROC)')
    #plt.savefig('ROC'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
    #plt.close()
    #
    ### plot PR curve
    ##average_precision = average_precision_score(y_test, y_pred)
    ##print('Average precision-recall score: {0:0.2f}'.format(average_precision))
    ##
    ##precision, recall, _ = precision_recall_curve(y_test, y_pred)
    ##
    ##plt.figure()
    ##plt.fill_between(recall, precision, alpha=0.2, color='b')
    ##plt.xlabel('Recall')
    ##plt.ylabel('Precision')
    ##plt.ylim([0.0, 1.05])
    ##plt.xlim([0.0, 1.0])
    ##plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
    ##plt.savefig('PR'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
    ##plt.close()
    #
    ## score predictions
    #score_train = np.concatenate(model.predict(np.array(X_train)))
    #score_test = np.concatenate(model.predict(np.array(X_test)))
    #print('KS test for score_train/score_test: {}'.format(stats.ks_2samp(score_train, score_test)))
    #
    ## define sig/bkg regions
    #sig_train = (y_train == 1)
    #sig_test = (y_test == 1)
    #bkg_train = (y_train == 0)
    #bkg_test = (y_test == 0)
    #
    ## select sig/bkg for train/test and weights
    #signal_train = score_train[sig_train]
    #wsignal_train = w_train[sig_train]
    #signal_test = score_test[sig_test]
    #wsignal_test = w_test[sig_test]
    #background_train = score_train[bkg_train]
    #wbackground_train = w_train[bkg_train]
    #background_test = score_test[bkg_test]
    #wbackground_test = w_test[bkg_test]
    #
    #print('mean signal train: {}'.format(np.mean(signal_train)))
    #print('mean signal test: {}'.format(np.mean(signal_test)))
    #print('median signal train: {}'.format(np.median(signal_train)))
    #print('median signal test: {}'.format(np.median(signal_test)))
    #print('mean background train: {}'.format(np.mean(background_train)))
    #print('mean background test: {}'.format(np.mean(background_test)))
    #print('median background train: {}'.format(np.median(background_train)))
    #print('median background test: {}'.format(np.median(background_test)))
    ##print('{}'.format(np.mean(signal_train)))
    ##print('{}'.format(np.mean(signal_test)))
    ##print('{}'.format(np.median(signal_train)))
    ##print('{}'.format(np.median(signal_test)))
    ##print('{}'.format(np.mean(background_train)))
    ##print('{}'.format(np.mean(background_test)))
    ##print('{}'.format(np.median(background_train)))
    ##print('{}'.format(np.median(background_test)))
    #
    ## make histograms
    #nbins = 51
    #bins = np.linspace(0, 1, nbins)
    #signal_train_counts, edges = np.histogram(signal_train, bins=bins, density=False, weights=wsignal_train)
    #signal_test_counts, edges = np.histogram(signal_test, bins=bins, density=False, weights=wsignal_test)
    #background_train_counts, edges = np.histogram(background_train, bins=bins, density=False, weights=wbackground_train)
    #background_test_counts, edges = np.histogram(background_test, bins=bins, density=False, weights=wbackground_test)
    #width = np.diff(edges)
    #signal_train_hist = signal_train_counts / np.sum(np.multiply(signal_train_counts, width))
    #signal_test_hist = signal_test_counts / np.sum(np.multiply(signal_test_counts, width))
    #background_train_hist = background_train_counts / np.sum(np.multiply(background_train_counts, width))
    #background_test_hist = background_test_counts / np.sum(np.multiply(background_test_counts, width))
    #
    #signal_test_std = np.array([np.sqrt(np.sum((wsignal_test[np.where(np.digitize(signal_test, edges)-1==nbin)[0]])**2)) for nbin in range(nbins-1)]) / np.sum(np.multiply(signal_test_counts, width))
    #background_test_std = np.array([np.sqrt(np.sum((wbackground_test[np.where(np.digitize(background_test, edges)-1==nbin)[0]])**2)) for nbin in range(nbins-1)]) / np.sum(np.multiply(background_test_counts, width))
    #
    ## compute KS for sig/bkg prob
    #ks_signal = stats.ks_2samp(signal_train, signal_test)[1]
    #ks_background = stats.ks_2samp(background_train, background_test)[1]
    #
    ## plot output distribution
    #plt.figure()
    #plt.bar((edges[1:]+edges[:-1])/2, background_train_hist, align='center', width=width, edgecolor=None, facecolor='r', alpha=0.3, label='Background (train)', zorder=1)
    #plt.errorbar((edges[1:]+edges[:-1])/2, background_test_hist, yerr=background_test_std, xerr=(edges[1:]-edges[:-1])/2, ecolor='r', elinewidth=1, fmt='none', label='Background (test)', zorder=2)
    #plt.bar((edges[1:]+edges[:-1])/2, signal_train_hist, align='center', width=width, edgecolor=None, facecolor='b', alpha=0.3, label='Signal (train)', zorder=1)
    #plt.errorbar((edges[1:]+edges[:-1])/2, signal_test_hist, yerr=signal_test_std, xerr=(edges[1:]-edges[:-1])/2, ecolor='b', elinewidth=1, fmt='none', label='Signal (test)', zorder=4)
    #
    #plt.text(0.025, 0.825, 'KS sig (bkg) prob: {:0.3f} ({:0.3f})'.format(ks_signal, ks_background), transform=plt.gca().transAxes, horizontalalignment='left', verticalalignment='top')
    #plt.xlim(0, 1)
    #plt.ylim(bottom=0)
    ##plt.grid(zorder=0)
    #plt.legend(ncol=2, loc='upper left')
    #plt.xlabel('Keras ANN Score')
    #plt.ylabel('Events (Normalized)')
    #plt.title('Classifier Overtraining Check')
    #plt.savefig('overtrain'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
    #plt.close()
    #
    ################################################################################
