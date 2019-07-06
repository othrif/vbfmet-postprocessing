import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import pickle

pickle_out = open("dict.pickle","rb")
inputEvts = pickle.load(pickle_out)

#for a
#np.array()

# Generate dummy data
import numpy as np
vbf_len = (len(inputEvts['vbf'])/2)
z_len = (len(inputEvts['z_strong'])/2)
print vbf_len,z_len
dataA_train = np.array(inputEvts['vbf'][:vbf_len]+inputEvts['z_strong'][:z_len])
dataA_test = np.array(inputEvts['vbf'][(vbf_len+1):]+inputEvts['z_strong'][(z_len+1):])
sample_weights_train=[]
sample_weights_test=[]
dataB_train=[]
dataB_test=[]
for d in dataA_train:
    sample_weights_train+=[d[0]]
    dataB_train+=[d[1:]]
for d in dataA_test:
    sample_weights_test+=[d[0]]
    dataB_test+=[d[1:]]    
data_train=np.array(dataB_train)
data_test=np.array(dataB_test)
labels_train = [0 for i in range(vbf_len)] + [1 for i in range(z_len)]
vbf_test_length = len(inputEvts['vbf'])-(vbf_len+1)
zstrong_test_length = len(inputEvts['z_strong'])-(z_len+1)
labels_test = [0 for i in range(vbf_test_length)] + [1 for i in range(zstrong_test_length)]

print 'labels_test:',len(labels_test)
print 'data_test:',len(data_test)
print 'sample_weights_test:',len(sample_weights_test)
print 'sample_weights_train:',len(sample_weights_train)
print 'labels_train:',len(labels_train)
print 'data_train:',len(data_train)

model = Sequential()
# Dense(64) is a fully-connected layer with 64 hidden units.
# in the first layer, you must specify the expected input data shape:
# here, 20-dimensional vectors.
#model.add(Dense(32, activation='relu', input_dim=100))
#model.add(Dense(1, activation='sigmoid'))
model.add(Dense(32, activation='relu', input_dim=len(data_train[0])))
model.add(Dense(1, activation='sigmoid'))
#model.add(Dropout(0.5))
#model.add(Dense(64, activation='relu'))
#model.add(Dropout(0.5))
#model.add(Dense(10, activation='softmax'))
#model.add(Dense(1, activation='sigmoid'))

#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
#model.compile(loss='categorical_crossentropy',
#              optimizer=sgd,
#              metrics=['accuracy'])
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Train the model, iterating on the data in batches of 32 samples
model.fit(data_train, labels_train, epochs=2,sample_weight=np.array(sample_weights_train))
score = model.evaluate(data_test, labels_test,sample_weight=np.array(sample_weights_test))
print score

#n=0
#for d in data_test:
a=model.predict(data_test)

#for i in a:
#    print i

# saving the model
model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
del model  # deletes the existing model

# returns a compiled model
#from keras.models import load_model
# identical to the previous one
#model = load_model('my_model.h5')
