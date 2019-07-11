import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import matplotlib.pyplot as plt
import pickle
import keras.backend as K

pickle_out = open("dict7a.pickle","rb")
inputEvts = pickle.load(pickle_out)
def kullback_leibler_divergenceB():
    def kullback_leibler_divergenceA(y_true, y_pred):
        y_true = K.clip(y_true, K.epsilon(), 1)
        y_pred = K.clip(y_pred, K.epsilon(), 1)
        return K.sum(y_true * K.log(y_true / y_pred), axis=-1)
    def meanErr(y_true, y_pred):
        return K.mean(K.square(y_pred - y_true), axis=-1)
    #return kullback_leibler_divergenceA
    return meanErr
def dice_coef(y_true, y_pred, smooth, thresh):
    y_pred = y_pred > thresh
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)

    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)
def dice_loss(smooth, thresh):
    def dice(y_true, y_pred):
        return -dice_coef(y_true, y_pred, smooth, thresh)
    return dice

# Define custom loss
def custom_loss(layer):

    # Create a loss function that adds the MSE loss to the mean of all squared activations of a specific layer
    def loss(y_true,y_pred):
        return K.mean(K.square(y_pred - y_true) + K.square(layer), axis=-1)
   
    # Return a function
    return loss

def setXYZ(v):

    for u in range(0,len(v)):
        if u==0:
            v[u] /=1.0e3
        elif u==2 or u==4 or u==5 or u==6:
            v[u] /=1.0e2
        else:
            v[u] /= 1.0    

#for a
#np.array()

# Generate dummy data
import numpy as np
vbf_len = (len(inputEvts['vbf'])/2)
z_len = (len(inputEvts['z_strong'])/2)
#print 'variable: ',vbf_len,z_len
ratio_bkg = vbf_len/float(z_len)
sample_weights_train=[]
sample_weights_test=[]
dataB_train=[]
dataB_test=[]
Qdata=[]
labels_test=[]
labels_train = [] #np.random.randint(2, size=(1000, 1))
Qdata_test = [] #np.random.random((10, 4))
z=0
wsignal_train=[]
wbkg_train=[]
wsignal_test=[]
wbkg_test=[]
nsignal_train=0
nsignal_test=0
nbkg_train=0
print ('Signal: %s'%len(inputEvts['vbf'])) 
for i in range(0,len(inputEvts['vbf'])):
    if np.random.uniform()>0.5 and nsignal_train<vbf_len:
        sample_weights_train+=[inputEvts['vbf'][i][0]]
        wsignal_train+=[36000.0*inputEvts['vbf'][i][0]]        
        dataB_train+=[inputEvts['vbf'][i][1:]]
        labels_train+=[[1]]
        setXYZ(dataB_train[len(dataB_train)-1])
        nsignal_train+=1

    else:
        sample_weights_test+=[[inputEvts['vbf'][i][0]]]
        wsignal_test+=[36000.0*inputEvts['vbf'][i][0]] 
        dataB_test+=[inputEvts['vbf'][i][1:]]
        setXYZ(dataB_test[len(dataB_test)-1])
        labels_test+=[[1]]
        nsignal_test+=1
        z+=1
        if z<10:
            Qdata_test+=[inputEvts['vbf'][i][1:]]
            setXYZ(Qdata_test[len(Qdata_test)-1])

larger_frac=2.0
for i in range(0,len(inputEvts['z_strong'])):
    #if np.random.uniform()>0.5 and nbkg_train<202489:
    if np.random.uniform()<(ratio_bkg*0.5*larger_frac) and nbkg_train<202489:        
        sample_weights_train+=[inputEvts['z_strong'][i][0]]
        wbkg_train+=[5*3600.0/larger_frac*inputEvts['z_strong'][i][0]]        
        dataB_train+=[inputEvts['z_strong'][i][1:]]
        setXYZ(dataB_train[len(dataB_train)-1])
        labels_train+=[[0]]
        nbkg_train+=1
    else:
        sample_weights_test+=[[inputEvts['z_strong'][i][0]]] 
        dataB_test+=[inputEvts['z_strong'][i][1:]]
        setXYZ(dataB_test[len(dataB_test)-1])
        wbkg_test+=[3600.0/larger_frac*inputEvts['z_strong'][i][0]]
        labels_test+=[[0]]
        
print('labels_test:%s' %len(labels_test))
print('data_test:%s' %len(dataB_test))
print('sample_weights_test:%s' %len(sample_weights_test))
print('sample_weights_train:%s' %len(sample_weights_train))
print('labels_train:%s' %len(labels_train))
print('data_train:%s' %len(dataB_train))

model = Sequential()
layer1=model.add(Dense(32, activation='relu', input_dim=len(dataB_train[0])))
#model.add(Dense(20, activation='relu', input_dim=32))
layer2=model.add(Dense(1, activation='sigmoid'))
model_dice = dice_loss(smooth=1e-5, thresh=0.5)
model.compile(optimizer='rmsprop',
                  #loss=custom_loss(layer2), #'binary_crossentropy',
                  #loss=model_dice, #'binary_crossentropy',
                  #loss='mean_squared_logarithmic_error',
                  #loss=kullback_leibler_divergenceB(),
                  loss='mean_squared_error',
              metrics=['accuracy'])

# Train the model, iterating on the data in batches of 32 samples
model.fit(np.array(dataB_train), np.array(labels_train), epochs=20, batch_size=32,sample_weight=np.array(sample_weights_train))
#model.fit(data_train, labels_train, epochs=2)#,sample_weight=np.array(sample_weights_train))
#score = model.evaluate(data_test, labels_test)#,sample_weight=np.array(sample_weights_test)) #,show_accuracy=True
#print score
#print 'Qdata_test:',Qdata_test
a=model.predict(np.array(Qdata_test))
print('%s' %a)

a=model.predict(np.array(Qdata_test))

score_train=model.predict(np.array(dataB_train))
score_test=model.predict(np.array(dataB_test))
#b=model.predict(np.array(bcheck))

# saving the model
model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'
del model  # deletes the existing model

# returns a compiled model
#from keras.models import load_model
# identical to the previous one
#model = load_model('my_model.h5')

# Draw the scores
# the histogram of the data
#n, bins, patches = plt.hist(score_train, 50, normed=1, facecolor='g', alpha=0.75)
signal_train=score_train[:nsignal_train]
signal_test=score_test[:nsignal_test]
bkg_train=score_train[nsignal_train:]
bkg_test=score_test[nsignal_test:]

bins = np.linspace(min(0.0,min(bkg_test)), max(1.0,max(signal_train)), 100)

if False:
    plt.hist(score_train, bins, alpha=0.5, label='Train')
    plt.hist(score_test, bins, alpha=0.5, label='Test')
    plt.legend(loc='upper right')
    #plt.show()

    plt.xlabel('ANN Score')
    plt.ylabel('Events')
    #plt.semilogy(bins, np.exp(-bins/5.0))
    plt.title('Histogram of IQ')
    plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    plt.axis([0, 1, 0, 5000.0])
    plt.grid(True)
    plt.show()



if False:
    #print "wsignal_train: ",len(wsignal_train),len(signal_train)
    #print "wbkg_train: ",len(wbkg_train),len(bkg_train)
    plt.hist(signal_train, bins, alpha=0.5, label='Signal',weights=wsignal_train)
    plt.hist(bkg_train, bins, alpha=0.5, label='Background',weights=wbkg_train)
    plt.legend(loc='upper right')
    #plt.show()

    plt.xlabel('ANN Score')
    plt.ylabel('Events')
    #plt.semilogy(bins, np.exp(-bins/5.0))
    plt.title('Histogram of IQ')
    plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    #plt.axis([0, 1, 0, 300.0])
    plt.axis([0, 1, 0, 25.0])
    plt.grid(True)
    plt.show()

    plt.clf()
    
#print "wsignal_train: ",len(wsignal_test),len(signal_test)
#print "wbkg_train: ",len(wbkg_test),len(bkg_test)    
plt.hist(signal_train, bins, alpha=0.5, label='Signal Train',weights=wsignal_train)
plt.hist(signal_test, bins, alpha=0.5, label='Signal Test',weights=wsignal_test)
plt.hist(bkg_test, bins, alpha=0.5, label='Background Test',weights=wbkg_test)
plt.hist(bkg_train, bins, alpha=0.5, label='Background Train',weights=wbkg_train)
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([0, 1, 0, 300.0])
plt.axis([min(0.0,min(bkg_test)), max(1.0,max(signal_train)), 0, 300.0])
plt.grid(True)
plt.legend(loc='upper right')
plt.show()
