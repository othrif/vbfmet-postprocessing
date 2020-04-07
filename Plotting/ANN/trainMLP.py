#!/usr/bin/env python
"""
Train MLP classifer to identify vector-boson fusion Higgs against background
"""
__author__ = "Sid Mau, Doug Schaefer"

###############################################################################
# Import libraries
##################
training_name='_test'

# Tensorflow and Keras
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM
#from keras import optimizers
#from keras import regularizers
import keras.backend as K
from custom_loss import *
# Scikit-learn
import sklearn.metrics as metrics
#from sklearn.metrics import classification_report, average_precision_score, precision_recall_curve, confusion_matrix
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import preprocessing
from sklearn.utils import class_weight
#from keras.wrappers.scikit_learn import KerasClassifier
#from sklearn.model_selection import GridSearchCV

# Scipy
from scipy import stats
import numpy as np
import numpy.lib.recfunctions as recfn

# Matplotlib
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt

###############################################################################

###############################################################################
# Load data
###########

# VBFH125 (signal)
VBFH125 = np.load('VBFH125.npy')
label_VBFH125 = np.ones(len(VBFH125))
VBFH125_labelled = recfn.rec_append_fields(VBFH125, 'label', label_VBFH125)
VBFH125_labelled['w']*=10.0 # adding weight to center the distribution

# Z_strong (background)
Z_strong = np.load('Z_strong.npy')
label_Z_strong = np.zeros(len(Z_strong))
Z_strong_labelled = recfn.rec_append_fields(Z_strong, 'label', label_Z_strong)

# Z_EWK (background)
Z_EWK = np.load('Z_EWK.npy')
label_Z_EWK = np.zeros(len(Z_EWK))
Z_EWK_labelled = recfn.rec_append_fields(Z_EWK, 'label', label_Z_EWK)

# ttbar (background)
ttbar = np.load('ttbar.npy')
label_ttbar = np.zeros(len(ttbar))
ttbar_labelled = recfn.rec_append_fields(ttbar, 'label', label_ttbar)

# W_strong (background)
W_strong = np.load('W_strong.npy')
label_W_strong = np.zeros(len(W_strong))
W_strong_labelled = recfn.rec_append_fields(W_strong, 'label', label_W_strong)

###############################################################################

###############################################################################
# Concatenate and shuffle data
##############################

data = np.concatenate([VBFH125_labelled, Z_strong_labelled])
#data = np.concatenate([VBFH125_labelled, Z_strong_labelled, ttbar_labelled, W_strong_labelled])
np.random.shuffle(data) # shuffle data

###############################################################################

###############################################################################
# Select variables
##################

##COLS = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
#COLS = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]']
#print('cols = {}'.format(COLS))
#X = data[COLS]
#y = data['label']
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
#X_train = X_train.astype([(name, '<f8') for name in X_train.dtype.names]).view(('<f8', len(X_train.dtype.names))) # convert from recarray to array
#X_test = X_test.astype([(name, '<f8') for name in X_test.dtype.names]).view(('<f8', len(X_test.dtype.names))) # convert from recarray to array

COLS  = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
COLS += ['n_jet', 'maxCentrality', 'max_mj_over_mjj']
COLS_nj2 = COLS
COLS_j3 = COLS + ['j3_centrality[0]', 'j3_min_mj_over_mjj', 'jet_pt[2]'] #'j3_centrality[1]', 
#COLS = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]']
#COLS  = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]','n_jet']
COLS  = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']

print('cols = {}'.format(COLS))

###############################################################################

###############################################################################
# Split train/test data
#######################

data_train, data_test, label_train, label_test = train_test_split(data, data['label'], test_size=0.2, random_state=0) # 80%/20% train/test split
X_train = data_train[COLS] # use only COLS
#X_train_j3 = data_train[data_train['n_jet'] == 3][COLS + COLS_j3]
X_test = data_test[COLS] # use only COLS
#X_test_j3 = data_test[data_test['n_jet'] == 3][COLS + COLS_j3]
y_train = label_train
y_test = label_test
w_train = data_train['w'] # weights
w_test = data_test['w'] # weights
X_train = X_train.astype([(name, '<f8') for name in X_train.dtype.names]).view(('<f8', len(X_train.dtype.names))) # convert from recarray to array
#X_train_j3 = X_train_j3.astype([(name, '<f8') for name in X_train_j3.dtype.names]).view(('<f8', len(X_train_j3.dtype.names))) # convert from recarray to array
X_test = X_test.astype([(name, '<f8') for name in X_test.dtype.names]).view(('<f8', len(X_test.dtype.names))) # convert from recarray to array
#X_test_j3 = X_test_j3.astype([(name, '<f8') for name in X_test_j3.dtype.names]).view(('<f8', len(X_test_j3.dtype.names))) # convert from recarray to array

###############################################################################

###############################################################################
# Preprocess data
#################

# Make scaler for train data
scaler = preprocessing.RobustScaler(with_centering=True, with_scaling=True, quantile_range=(25, 75)).fit(X_train) # scaler to standardize data
X_train = scaler.transform(X_train) # apply to train data
X_test = scaler.transform(X_test) # apply to test data

# Save it
from sklearn.externals import joblib
scaler_filename = "scaler"+training_name+".save"
joblib.dump(scaler, scaler_filename) 

###############################################################################

###############################################################################
# Weigh classes
################

# This helps address the imbalanced nature of the data
class_weight = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)

###############################################################################

###############################################################################
# Define the classifier model
#############################

model = Sequential()
model.add(Dense(32, kernel_initializer='normal', activation='relu', input_dim=len(COLS)))
#model.add(Dense(16, kernel_initializer='normal', activation='relu'))
#model.add(Dense(4, kernel_initializer='normal', activation='relu'))
#model.add(Dense(2, kernel_initializer='normal', activation='relu'))
#model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
#model.compile(optimizer='nadam',
#              loss=focal_loss,
#              metrics=['accuracy'])
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy']) # best
print(model.summary())

###############################################################################

###############################################################################
# Train the classifier model
############################

# Fit the model
model.fit(X_train, y_train, validation_split=0.1, epochs=10, batch_size=32, class_weight=class_weight, sample_weight=w_train)

# Save the model
model_filename = 'model'+training_name+'.hf'
model.save(model_filename)

###############################################################################

###############################################################################
# Performance Plots
###################

## quick metrics
y_pred = model.predict(np.array(X_test))
#y_pred_bool = np.argmax(y_pred, axis=1)
#y_pred_bool = np.where(y_pred > 0.3, 1, 0)
#print(classification_report(y_test, y_pred_bool))
#print(confusion_matrix(y_test, y_pred_bool))

# calculate the fpr and tpr for all thresholds of the classification
y_pred = model.predict(np.array(X_test))
fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)

# plot ROC curve
plt.figure()
plt.fill_between(fpr, 0, tpr, facecolor='b', alpha=0.3, label='AUC = {:0.3f}'.format(roc_auc), zorder=0)
plt.plot([0, 1], [0, 1], c='gray', lw=1, ls='--', zorder=1)
plt.plot(fpr, tpr, c='b', lw=2, ls='-', label='ROC Curve', zorder=2)
plt.legend(loc='upper left')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.savefig('ROC'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
plt.close()

## plot PR curve
#average_precision = average_precision_score(y_test, y_pred)
#print('Average precision-recall score: {0:0.2f}'.format(average_precision))
#
#precision, recall, _ = precision_recall_curve(y_test, y_pred)
#
#plt.figure()
#plt.fill_between(recall, precision, alpha=0.2, color='b')
#plt.xlabel('Recall')
#plt.ylabel('Precision')
#plt.ylim([0.0, 1.05])
#plt.xlim([0.0, 1.0])
#plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
#plt.savefig('PR'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
#plt.close()

# score predictions
score_train = np.concatenate(model.predict(np.array(X_train)))
score_test = np.concatenate(model.predict(np.array(X_test)))
print('KS test for score_train/score_test: {}'.format(stats.ks_2samp(score_train, score_test)))

# define sig/bkg regions
sig_train = (y_train == 1)
sig_test = (y_test == 1)
bkg_train = (y_train == 0)
bkg_test = (y_test == 0)

# select sig/bkg for train/test and weights
signal_train = score_train[sig_train]
wsignal_train = w_train[sig_train]
signal_test = score_test[sig_test]
wsignal_test = w_test[sig_test]
background_train = score_train[bkg_train]
wbackground_train = w_train[bkg_train]
background_test = score_test[bkg_test]
wbackground_test = w_test[bkg_test]

# make histograms
nbins = 51
bins = np.linspace(0, 1, nbins)
signal_train_counts, edges = np.histogram(signal_train, bins=bins, density=False, weights=wsignal_train)
signal_test_counts, edges = np.histogram(signal_test, bins=bins, density=False, weights=wsignal_test)
background_train_counts, edges = np.histogram(background_train, bins=bins, density=False, weights=wbackground_train)
background_test_counts, edges = np.histogram(background_test, bins=bins, density=False, weights=wbackground_test)
width = np.diff(edges)
signal_train_hist = signal_train_counts / np.sum(np.multiply(signal_train_counts, width))
signal_test_hist = signal_test_counts / np.sum(np.multiply(signal_test_counts, width))
background_train_hist = background_train_counts / np.sum(np.multiply(background_train_counts, width))
background_test_hist = background_test_counts / np.sum(np.multiply(background_test_counts, width))

signal_test_std = np.array([np.sqrt(np.sum((wsignal_test[np.where(np.digitize(signal_test, edges)-1==nbin)[0]])**2)) for nbin in range(nbins-1)]) / np.sum(np.multiply(signal_test_counts, width))
background_test_std = np.array([np.sqrt(np.sum((wbackground_test[np.where(np.digitize(background_test, edges)-1==nbin)[0]])**2)) for nbin in range(nbins-1)]) / np.sum(np.multiply(background_test_counts, width))

# compute KS for sig/bkg prob
ks_signal = stats.ks_2samp(signal_train, signal_test)[1]
ks_background = stats.ks_2samp(background_train, background_test)[1]

# plot output distribution
plt.figure()
plt.bar((edges[1:]+edges[:-1])/2, background_train_hist, align='center', width=width, edgecolor=None, facecolor='r', alpha=0.3, label='Background (train)', zorder=1)
plt.errorbar((edges[1:]+edges[:-1])/2, background_test_hist, yerr=background_test_std, xerr=(edges[1:]-edges[:-1])/2, ecolor='r', elinewidth=1, fmt='none', label='Background (test)', zorder=2)
plt.bar((edges[1:]+edges[:-1])/2, signal_train_hist, align='center', width=width, edgecolor=None, facecolor='b', alpha=0.3, label='Signal (train)', zorder=1)
plt.errorbar((edges[1:]+edges[:-1])/2, signal_test_hist, yerr=signal_test_std, xerr=(edges[1:]-edges[:-1])/2, ecolor='b', elinewidth=1, fmt='none', label='Signal (test)', zorder=4)

plt.text(1-0.025, 0.825, 'KS sig (bkg) prob: {:0.3f} ({:0.3f})'.format(ks_signal, ks_background), transform=plt.gca().transAxes, horizontalalignment='right', verticalalignment='top')
plt.xlim(0, 1)
plt.ylim(bottom=0)
#plt.grid(zorder=0)
plt.legend(ncol=2, loc='upper right')
plt.xlabel('Keras ANN Score')
plt.ylabel('Events (Normalized)')
plt.title('Classifier Overtraining Check')
plt.savefig('overtrain'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
plt.close()

###############################################################################
