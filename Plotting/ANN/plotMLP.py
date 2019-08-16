import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM, GaussianNoise, LeakyReLU
from keras.optimizers import SGD
from keras import optimizers
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
from scipy import stats
import numpy as np
from keras.utils import plot_model
import matplotlib.pyplot as plt
import numpy.lib.recfunctions as recfn
import keras.backend as K
import sklearn.metrics as metrics

from custom_loss import *

#training_name = '_zstrong_ttbar_wstrong_zewk_15var'
training_name = '_zstrong_ttbar_wstrong_zewk_15var'
#training_name = '_zstrong_15var'

data = np.load("data" + training_name + ".npz")
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']
w_train = data['w_train']
w_test = data['w_test']

# returns a compiled model
from keras.models import load_model
# identical to the previous one
model_dir='./'
model_dir='./'
model_filename = 'model'+training_name+'.hdf5'
model = load_model(model_dir+model_filename, custom_objects={'focal_loss': focal_loss, 'sig_eff': sig_eff})

# calculate the fpr and tpr for all thresholds of the classification
y_pred = model.predict(X_test)
fpr, tpr, threshold = metrics.roc_curve(y_test, y_pred)
roc_auc = metrics.auc(fpr, tpr)

#y_pred = np.concatenate(y_pred)
#scores = np.arange(0.01, 1.0, 0.01)
#sig_effs = []
#bkg_rejs = []
#for score in scores:
#    #sig_eff = len(y_test[(y_pred >= score) & (y_test == 1)]) / len(y_pred[y_pred >= score])
#    #bkg_eff = len(y_test[(y_pred >= score) & (y_test == 0)]) / len(y_pred[y_pred >= score])
#    #bkg_rej = 1 - bkg_eff
#    #bkg_rej = len(y_test[(y_pred < score) & (y_test == 0)]) / len(y_pred[y_pred < score])
#    sig_effs.append(sig_eff)
#    bkg_rejs.append(bkg_rej)
#sig_effs = np.array(sig_effs)
#bkg_rej = np.array(bkg_rejs)
#
#plt.figure()
#plt.fill_between(sig_effs, 0, bkg_rejs, facecolor='r', alpha=0.3, zorder=3)
#plt.plot(sig_effs, bkg_rejs, c='r', lw=2, ls='-', zorder=4)
#plt.xlabel('Signal Efficiency')
#plt.ylabel('Background Rejection')
#plt.savefig('rej-eff'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
#plt.close()

sig_eff = tpr # sensitivity
bkg_rej = 1 - fpr # specificity
plt.figure()
plt.fill_between(sig_eff, 0, bkg_rej, facecolor='r', alpha=0.3, zorder=3, label='AUC = {:0.3f}'.format(roc_auc))
plt.plot(sig_eff, bkg_rej, c='r', lw=2, ls='-', label='ROC Curve', zorder=4)
plt.legend(loc='upper left')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.xlabel('Signal Efficiency')
plt.ylabel('Background Rejection')
plt.title('Receiver Operating Characteristic (ROC)')
plt.savefig('rej-eff'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
plt.close()

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

print('mean signal train: {}'.format(np.mean(signal_train)))
print('mean signal test: {}'.format(np.mean(signal_test)))
print('median signal train: {}'.format(np.median(signal_train)))
print('median signal test: {}'.format(np.median(signal_test)))
print('mean background train: {}'.format(np.mean(background_train)))
print('mean background test: {}'.format(np.mean(background_test)))
print('median background train: {}'.format(np.median(background_train)))
print('median background test: {}'.format(np.median(background_test)))
#print('{}'.format(np.mean(signal_train)))
#print('{}'.format(np.mean(signal_test)))
#print('{}'.format(np.median(signal_train)))
#print('{}'.format(np.median(signal_test)))
#print('{}'.format(np.mean(background_train)))
#print('{}'.format(np.mean(background_test)))
#print('{}'.format(np.median(background_train)))
#print('{}'.format(np.median(background_test)))

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
plt.bar((edges[1:]+edges[:-1])/2, background_train_hist, align='center', width=width, edgecolor=None, facecolor='r', alpha=0.3, label='Background (train)', zorder=1, rasterized=True)
plt.errorbar((edges[1:]+edges[:-1])/2, background_test_hist, yerr=background_test_std, xerr=(edges[1:]-edges[:-1])/2, ecolor='r', elinewidth=1, fmt='none', label='Background (test)', zorder=2)
plt.bar((edges[1:]+edges[:-1])/2, signal_train_hist, align='center', width=width, edgecolor=None, facecolor='b', alpha=0.3, label='Signal (train)', zorder=1)
plt.errorbar((edges[1:]+edges[:-1])/2, signal_test_hist, yerr=signal_test_std, xerr=(edges[1:]-edges[:-1])/2, ecolor='b', elinewidth=1, fmt='none', label='Signal (test)', zorder=4)

plt.text(0.025, 0.825, 'KS sig (bkg) prob: {:0.3f} ({:0.3f})'.format(ks_signal, ks_background), transform=plt.gca().transAxes, horizontalalignment='left', verticalalignment='top')
plt.xlim(0, 1)
plt.ylim(bottom=0)
#plt.grid(zorder=0)
plt.legend(ncol=2, loc='upper left')
plt.xlabel('Keras ANN Score')
plt.ylabel('Events (Normalized)')
plt.title('Classifier Overtraining Check')
plt.savefig('overtrain'+training_name+'.pdf', bbox_inches='tight', rasterized=False)
plt.close()

###############################################################################
