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

VBFH125 = np.load('VBFH125.npy')
label_VBFH125 = np.ones(len(VBFH125))
VBFH125_labelled = recfn.rec_append_fields(VBFH125, 'label', label_VBFH125)

Z_strong = np.load('Z_strong.npy')
label_Z_strong = np.zeros(len(Z_strong))
Z_strong_labelled = recfn.rec_append_fields(Z_strong, 'label', label_Z_strong)

Z_EWK = np.load('Z_EWK.npy')
label_Z_EWK = np.zeros(len(Z_EWK))
Z_EWK_labelled = recfn.rec_append_fields(Z_EWK, 'label', label_Z_EWK)

ttbar = np.load('ttbar.npy')
label_ttbar = np.zeros(len(ttbar))
ttbar_labelled = recfn.rec_append_fields(ttbar, 'label', label_ttbar)

W_strong = np.load('W_strong.npy')
label_W_strong = np.zeros(len(W_strong))
W_strong_labelled = recfn.rec_append_fields(W_strong, 'label', label_W_strong)

#data = np.concatenate([VBFH125_labelled, Z_strong_labelled])
data = np.concatenate([VBFH125_labelled, Z_strong_labelled, ttbar_labelled, W_strong_labelled])
np.random.shuffle(data) # shuffle data

#COLS = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
COLS = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]']
#COLS += ['met_tst_j1_dphi', 'met_tst_j2_dphi']
#COLS += ['met_significance', 'max_mj_over_mjj', 'maxCentrality']
#COLS += ['met_soft_tst_sumet', 'met_tenacious_tst_et']
print('cols = {}'.format(COLS))
X = data[COLS]
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
X_train = X_train.astype([(name, '<f8') for name in X_train.dtype.names]).view(('<f8', len(X_train.dtype.names))) # convert from recarray to array
X_test = X_test.astype([(name, '<f8') for name in X_test.dtype.names]).view(('<f8', len(X_test.dtype.names))) # convert from recarray to array


# load scaler
from sklearn.externals import joblib
scaler_filename = "scaler.save"
# Load it 
scaler = joblib.load(scaler_filename)

# preprocess data
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


# returns a compiled model
from keras.models import load_model
# identical to the previous one
model = load_model('model.h5')

# plot ROC curve
# calculate the fpr and tpr for all thresholds of the classification
preds = model.predict(np.array(X_test))
fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
roc_auc = metrics.auc(fpr, tpr)

plt.fill_between(fpr, 0, tpr, facecolor='b', alpha=0.3, label='AUC = {:0.3f}'.format(roc_auc), zorder=0)
plt.plot([0, 1], [0, 1], c='gray', lw=1, ls='--', zorder=1)
plt.plot(fpr, tpr, c='b', lw=2, ls='-', zorder=2)
plt.legend(loc='upper left')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Receiver Operating Characteristic (ROC)')
plt.savefig('ROC.pdf', bbox_inches='tight', rasterized=False)
plt.close()

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
#wsignal_train = X_train[sig_train][:,0]
signal_test = score_test[sig_test]
#wsignal_test = X_test[sig_test][:,0]
background_train = score_train[bkg_train]
#wbackground_train = X_train[bkg_train][:,0]
background_test = score_test[bkg_test]
#wbackground_test = X_test[bkg_test][:,0]

# make histograms
nbins = 51
bins = np.linspace(0, 1, nbins)
#signal_train_hist, edges = np.histogram(signal_train, bins=bins, density=True)
#signal_test_hist, edges = np.histogram(signal_test, bins=bins, density=True)
#background_train_hist, edges = np.histogram(background_train, bins=bins, density=True)
#background_test_hist, edges = np.histogram(background_test, bins=bins, density=True)

# compute KS for sig/bkg prob
ks_signal = stats.ks_2samp(signal_train, signal_test)[1]
ks_background = stats.ks_2samp(background_train, background_test)[1]

# plot output distribution
plt.hist(background_train, bins=bins, density=True, histtype='stepfilled', edgecolor=None, facecolor='r', alpha=0.3, label='Background Train', zorder=1)
plt.hist(background_test, bins=bins, density=True, histtype='step', edgecolor='r', label='Background Test', zorder=2)
#plt.errorbar((edges[1:]+edges[:-1])/2, background_test_hist, yerr=np.sqrt(background_test_hist), xerr=(edges[1:]-edges[:-1])/2, ecolor='r', elinewidth=1, fmt='none', label='Background Test', zorder=2)
plt.hist(signal_train, bins=bins, density=True, histtype='stepfilled', edgecolor=None, facecolor='b', alpha=0.3, label='Signal Train', zorder=3)
plt.hist(signal_test, bins=bins, density=True, histtype='step', edgecolor='b', label='Signal Test', zorder=4)
#plt.errorbar((edges[1:]+edges[:-1])/2, signal_test_hist, yerr=np.sqrt(signal_test_hist), xerr=(edges[1:]-edges[:-1])/2, ecolor='b', elinewidth=1, fmt='none', label='Signal Test', zorder=4)

#plt.hist(signal_train, bins=bins, histtype='step', label='Signal Train', weights=wsignal_train)
#plt.hist(signal_test, bins=bins, histtype='step', label='Signal Test', weights=wsignal_test)
#plt.hist(background_test, bins=bins, histtype='step', label='Background Test', weights=wbackground_test)
#plt.hist(background_train, bins=bins, histtype='step', label='Background Train', weights=wbackground_train)

plt.text(1-0.025, 0.825, 'KS sig (bkg) prob: {:0.3f} ({:0.3f})'.format(ks_signal, ks_background), transform=plt.gca().transAxes, horizontalalignment='right', verticalalignment='top')
plt.xlim(0, 1)
plt.ylim(bottom=0)
plt.grid(zorder=0)
plt.legend(ncol=2, loc='upper right')
plt.xlabel('Keras ANN Score')
plt.ylabel('Events (Normalized)')
plt.title('Classifier Overtraining Check')
plt.savefig('overtrain.pdf', bbox_inches='tight', rasterized=False)
plt.close()

