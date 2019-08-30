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

training_name = '_zstrong_ttbar_wstrong_zewk_15var'
COL_7 = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]', 'met_soft_tst_et']
COL_15 = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]', 'met_soft_tst_et', 'jet_phi[0]', 'jet_phi[1]', 'n_jet', 'maxCentrality', 'max_mj_over_mjj', 'met_cst_jet', 'met_tight_tst_et', 'met_tenacious_tst_et']
COLS = COL_15

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
model_filename = 'model'+training_name+'.hdf5'
model = load_model(model_dir+model_filename, custom_objects={'focal_loss': focal_loss, 'sig_eff': sig_eff})

# score predictions
score_test = model.predict(X_test)

# define sig/bkg regions
sig_test = (y_test == 1)
bkg_test = (y_test == 0)

# select sig/bkg for train/test and weights
signal_test = score_test[sig_test]
#wsignal_test = w_test[sig_test]
background_test = score_test[bkg_test]
#wbackground_test = w_test[bkg_test]

print('VARIABLE,SIGNAL,BACKGROUND')
print('\"{}\",{},{}'.format('baseline', np.median(signal_test), np.median(background_test)))

for i in range(len(COLS)):
    X_test_modified = np.copy(X_test)
    X_test_modified[:,i] += 0.01
    score_test = model.predict(X_test_modified)

    # define sig/bkg regions
    sig_test = (y_test == 1)
    bkg_test = (y_test == 0)
    
    # select sig/bkg for train/test and weights
    signal_test = score_test[sig_test]
    #wsignal_test = w_test[sig_test]
    background_test = score_test[bkg_test]
    #wbackground_test = w_test[bkg_test]
    
    print('\"{}\",{},{}'.format(COLS[i], np.median(signal_test), np.median(background_test)))

test = model.evaluate(X_test, y_test, verbose=0)
loss = test[0]
acc = test[1]
print('VARIABLE,LOSS,ACCURACY')
print('\"{}\",{},{}'.format('baseline', loss, acc))

for i in range(len(COLS)):
    X_test_shuffled = np.copy(X_test)
    np.random.shuffle(X_test_shuffled[:,i])
    score_test = model.predict(X_test_shuffled)
    
    # define sig/bkg regions
    sig_test = (y_test == 1)
    bkg_test = (y_test == 0)
    
    # select sig/bkg for train/test and weights
    signal_test = score_test[sig_test]
    #wsignal_test = w_test[sig_test]
    background_test = score_test[bkg_test]
    #wbackground_test = w_test[bkg_test]
    
    test = model.evaluate(X_test_shuffled, y_test, verbose=0)
    loss = test[0]
    acc = test[1]
    print('\"{}\",{},{}'.format(COLS[i], loss, acc))
    
