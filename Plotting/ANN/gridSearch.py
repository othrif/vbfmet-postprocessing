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

COLS = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
print('cols = {}'.format(COLS))
X = data[COLS]
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
X_train = X_train.astype([(name, '<f8') for name in X_train.dtype.names]).view(('<f8', len(X_train.dtype.names))) # convert from recarray to array
X_test = X_test.astype([(name, '<f8') for name in X_test.dtype.names]).view(('<f8', len(X_test.dtype.names))) # convert from recarray to array
#data_train, data_test, label_train, label_test = train_test_split(data, data['label'], test_size=0.2, random_state=0)
#X_train = data_train[COLS]
#X_test = data_test[COLS]
#y_train = label_train
#y_test = label_test
#w_train = data_train['w']
#w_test = data_test['w']
#X_train = X_train.astype([(name, '<f8') for name in X_train.dtype.names]).view(('<f8', len(X_train.dtype.names))) # convert from recarray to array
#X_test = X_test.astype([(name, '<f8') for name in X_test.dtype.names]).view(('<f8', len(X_test.dtype.names))) # convert from recarray to array

# preprocess data
scaler = preprocessing.RobustScaler(with_centering=True, with_scaling=True, quantile_range=(25, 75)).fit(X_train) # scaler to standardize data
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# The following is for doing a grid search over hyperparameters
# define the classifier model
def create_model(optimizer='rmsprop', init='glorot_uniform', loss='binary_crossentropy'):
    print('optimizer = {}'.format(optimizer))
    print('init = {}'.format(init))
    print('loss = {}'.format(loss))
    model = Sequential()
    model.add(Dense(32, kernel_initializer=init, activation='relu', input_dim=len(COLS)))
    model.add(Dense(16, kernel_initializer=init, activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=['accuracy', 'mae'])
    return(model)

# create model
model = KerasClassifier(build_fn=create_model, verbose=1)
# grid search epochs, batch size and optimizer
optimizers = ['nadam', 'sgd']
loss = ['mean_squared_error', 'logcosh', 'binary_crossentropy', 'poisson']
init = ['normal', 'uniform']
epochs = [10, 50, 100, 500, 1000]
batches = [10, 50, 100, 500, 1000]
param_grid = dict(optimizer=optimizers, epochs=epochs, batch_size=batches, init=init, loss=loss)
grid = GridSearchCV(estimator=model, param_grid=param_grid)
grid_result = grid.fit(X_train, y_train)
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))
