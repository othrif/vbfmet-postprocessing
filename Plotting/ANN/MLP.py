import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras import optimizers
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import pickle
from scipy import stats
import numpy as np

# read in events from pickle
pickle_out = open("dict7a.pickle","rb")
inputEvts = pickle.load(pickle_out)
vbf = inputEvts['vbf']
z_strong = inputEvts['z_strong']

# organize input events
events = vbf + z_strong # make event list
labels = np.ones(len(vbf)).tolist() + np.zeros(len(z_strong)).tolist() # make label list
labelled_events = [tuple(event) for event in np.c_[events, labels]] # label events
data = np.array(labelled_events, dtype=[('WEIGHT', float), ('JJ_MASS', float), ('JJ_DETA', float), ('MET_TST_ET', float), ('JJ_DPHI', float), ('JET_PT0', float), ('JET_PT1', float), ('MET_SOFT_TST_ET', float), ('LABEL', int)]) # convert to recarray
np.random.shuffle(data) # shuffle data

# define training/testing data (80-20 ratio)
COLS =  ['JJ_MASS', 'JJ_DETA', 'MET_TST_ET', 'JJ_DPHI', 'JET_PT0', 'JET_PT1', 'MET_SOFT_TST_ET']
#COLS = [ 'JJ_MASS', 'JJ_DETA', 'MET_TST_ET', 'JJ_DPHI', 'JET_PT0', 'JET_PT1']
print('cols = {}'.format(COLS))
X = data[COLS]
print(X)
y = data['LABEL']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
#print X_train['WEIGHT']
#print X_train.dtype.names
#print X_train
X_train = X_train.view((float, len(X_train.dtype.names))) # destructure data
X_test = X_test.view((float, len(X_test.dtype.names)))# destructure data

# preprocess data
scaler = preprocessing.StandardScaler().fit(X_train) # scaler to standardize data
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
# Save it
from sklearn.externals import joblib
scaler_filename = "my_scaler_7varnjet.save"
joblib.dump(scaler, scaler_filename) 

# Load it 
#scaler = joblib.load(scaler_file) 

# define the classifier model
model = Sequential()
model.add(Dense(64, kernel_initializer='normal', activation='relu', input_dim=len(COLS)))
#model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy']) # best
#sgd = optimizers.SGD(lr=0.8, momentum=0.0, decay=0.0, nesterov=False)
#model.compile(optimizer='sgd',
#              loss='binary_crossentropy',
#              metrics=['binary_accuracy']) # good
#model.compile(loss='mean_squared_error',
#              optimizer='sgd',
#              metrics=['mae', 'acc']) # worst

# train the classifier model
model.fit(X_train, y_train, epochs=4, batch_size=64)#,sample_weight=np.array(sample_weights_train))

y_pred = model.predict(X_test)

# saving the model
model_name='my_model_7varnjet.h5'
model.save(model_name)  # creates a HDF5 file 'my_model.h5'
del model  # deletes the existing model
print('Done')
###############################################################################

# returns a compiled model
from keras.models import load_model
# identical to the previous one
model = load_model(model_name)

import sklearn.metrics as metrics
# calculate the fpr and tpr for all thresholds of the classification
probs = model.predict_proba(X_test)
preds = probs.ravel()
fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
roc_auc = metrics.auc(fpr, tpr)

import matplotlib.pyplot as plt
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()

#plt.hist(y_train, histtype='step', label='y_train')
#plt.hist(y_test, histtype='step', label='y_test')
#plt.legend(loc='upper left')
#plt.show()

# score predictions
score_train = model.predict(np.array(X_train))
score_test = model.predict(np.array(X_test))
#print(stats.ks_2samp(y_train, y_test))
print(stats.ks_2samp(np.concatenate(score_train), np.concatenate(score_test)))

# define sig/bkg regions
sig_train = (y_train == 1)
sig_test = (y_test == 1)
bkg_train = (y_train == 0)
bkg_test = (y_test == 0)

# select sig/bkg for train/test and weights
signal_train = score_train[sig_train]
wsignal_train = X_train[sig_train][:,0]
signal_test = score_test[sig_test]
wsignal_test = X_test[sig_test][:,0]
background_train = score_train[bkg_train]
wbackground_train = X_train[bkg_train][:,0]
background_test = score_test[bkg_test]
wbackground_test = X_test[bkg_test][:,0]

# output distribution
bins = np.linspace(min(0.0,min(background_test)), max(1.0,max(signal_train)), 100)
plt.hist(signal_train, bins, alpha=0.5, label='Signal Train')
plt.hist(signal_test, bins, alpha=0.5, label='Signal Test')
plt.hist(background_test, bins, alpha=0.5, label='Background Test')
plt.hist(background_train, bins, alpha=0.5, label='Background Train')
#plt.hist(signal_train, bins, alpha=0.5, label='Signal Train',weights=wsignal_train)
#plt.hist(signal_test, bins, alpha=0.5, label='Signal Test',weights=wsignal_test)
#plt.hist(background_test, bins, alpha=0.5, label='Background Test',weights=wbackground_test)
#plt.hist(background_train, bins, alpha=0.5, label='Background Train',weights=wbackground_train)
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([min(0.0,min(background_test)), max(1.0,max(signal_train)), 0, 300.0])
plt.grid(True)
plt.legend(loc='upper right')
plt.show()

