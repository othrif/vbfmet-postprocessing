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
Qdata = np.random.random((1000, 4))
Qdata=[]
Qdata_test = np.random.random((10, 4))
labels_train = np.random.randint(2, size=(1000, 1))
#print 'labels_train:',labels_train
dataA_train = np.array(inputEvts['vbf'][:vbf_len]+inputEvts['z_strong'][:z_len])
dataA_test = np.array(inputEvts['vbf'][(vbf_len+1):]+inputEvts['z_strong'][(z_len+1):])
sample_weights_train=[]
sample_weights_test=[]
dataB_train=[]
dataB_test=[]
data_test=[]
check=[]
bcheck=[]
ncheck=0
nbcheck=0

# load data
it=0
for i in range(0,500):
    labels_train[i]=1
for i in range(500,1000):
    labels_train[i]=0
#labels_train = [1 for i in range(0,500)] + [0 for i in range(0,500)]
for de in range(0,1000):
    d=inputEvts['z_strong'][de]
    labels_train[de]=0
    if de%2==0:
        d=inputEvts['vbf'][de]
        labels_train[de]=1

    Qdata+=[d[1:]]
    for u in range(1,5):
        #Qdata[de][u-1] = d[u]
        if u==1:
            Qdata[de][u-1] = d[u]/1.0e4
        elif u==3:
            Qdata[de][u-1] = d[u]/1.0e3
        else:
            Qdata[de][u-1] = d[u]/10.0
#for d in dataA_train:
#    for u in range(1,5):
#        if u==1:
#            Qdata[it][u-1] = d[u]/1.0e3
#        elif u==3:
#            Qdata[it][u-1] = d[u]/1.0e2
#    it+=1
#    if it>499:
#        break
#for d in inputEvts['z_strong'][:z_len]:
#    for u in range(1,5):
#        if u==1:
#            Qdata[it][u-1] = d[u]/1.0e3
#        elif u==3:
#            Qdata[it][u-1] = d[u]/1.0e2
#    it+=1
#    if it>=999:
#        break
#end new loading

for d in dataA_train:
    sample_weights_train+=[d[0]]
    dataB_train+=[d[1:]]


for d in dataA_test:
    sample_weights_test+=[d[0]]
    data_test+=[d[1:]]
    #for u in range(1,5):
    #    data[it][u-1] = d[u]
    if ncheck<10:
        #Qdata_test+=[d[1:]]
        for u in range(1,5):
            #Qdata_test[ncheck][u-1] = d[u]
            if u==1:
                Qdata_test[ncheck][u-1] = d[u]/1.0e4
            elif u==3:
                Qdata_test[ncheck][u-1] = d[u]/1.0e3
            else:
                Qdata_test[ncheck][u-1] = d[u]/10.0
        check+=[d[1:]]
    ncheck+=1

for d in inputEvts['z_strong'][(z_len+1):]:
    if nbcheck<10:
        bcheck+=[d[1:]]
    nbcheck+=1
data_train=np.array(dataB_train)
data_test=np.array(dataB_test)
#labels_train = [1 for i in range(vbf_len)] + [0 for i in range(z_len)]
vbf_test_length = len(inputEvts['vbf'])-(vbf_len+1)
zstrong_test_length = len(inputEvts['z_strong'])-(z_len+1)
labels_test = [1 for i in range(vbf_test_length)] + [0 for i in range(zstrong_test_length)]
print 'check:',check
print 'background:',bcheck
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
##model.add(Dense(32, activation='relu', input_dim=100))
##model.add(Dense(1, activation='sigmoid'))
##model.add(Dense(32, activation='relu', input_dim=len(data_train[0])))
#model.add(Dense(32, activation='softmax', input_dim=len(data_train[0])))
##model.add(Dense(1, activation='sigmoid'))
#model.add(Dense(1, activation='softmax'))
##model.add(Dropout(0.5))
##model.add(Dense(64, activation='relu'))
##model.add(Dropout(0.5))
##model.add(Dense(10, activation='softmax'))
##model.add(Dense(1, activation='sigmoid'))
#
##sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
##model.compile(loss='categorical_crossentropy',
##              optimizer=sgd,
##              metrics=['accuracy'])
##rms = RMSprop()
#model.compile(loss='mean_squared_error',
#              optimizer='sgd',
#              metrics=['mae', 'acc'])
#
##model.compile(loss='binary_crossentropy',
##              optimizer='rmsprop',
##              metrics=['accuracy'])

#model.add(Dense(32, activation='relu', input_dim=4))
##model.add(Dense(10, activation='sigmoid'))
#model.add(Dense(1, activation='softmax'))
#model.compile(optimizer='rmsprop',
#              loss='binary_crossentropy',
#              metrics=['accuracy'])
#
#model = Sequential()
model.add(Dense(32, activation='relu', input_dim=4))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
#model.compile(loss='mean_squared_error',
#              optimizer='sgd',
#              metrics=['mae', 'acc'])
#print Qdata
#print labels_train
# Train the model, iterating on the data in batches of 32 samples
model.fit(np.array(Qdata), labels_train, epochs=20, batch_size=32)#,sample_weight=np.array(sample_weights_train))
#model.fit(data_train, labels_train, epochs=2)#,sample_weight=np.array(sample_weights_train))
#score = model.evaluate(data_test, labels_test)#,sample_weight=np.array(sample_weights_test)) #,show_accuracy=True
#print score
#print labels_test
#n=0
#for d in data_test:
a=model.predict(Qdata_test)
print a
#b=model.predict(np.array(bcheck))
#print b
#for i in a:
#    print i

# saving the model
model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
del model  # deletes the existing model

# returns a compiled model
#from keras.models import load_model
# identical to the previous one
#model = load_model('my_model.h5')
