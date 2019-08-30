import yaml      
import neuralNet
import sys
import numpy as np

with open(sys.argv[1]) as ymlfile:
    cfg = yaml.load(ymlfile)
    mlp = neuralNet.MLP(cfg)
    
model = mlp.load_model()
data = mlp.load_data()

X_train = data['X_train']
y_train = data['y_train']
w_train = data['w_train']
X_test = data['X_test']
y_test = data['y_test']
w_test = data['w_test']

y_pred = np.concatenate(model.predict(X_test)) # do on X_train?

sig_true = (y_test == 1)
bkg_true = (y_test == 0)

sig_pred = y_pred[sig_true]
bkg_pred = y_pred[bkg_true]

# Flatten signal distribution
sig_integral = np.sum(sig_pred)

n_bins = 7

events_per_bin = int(len(sig_pred) / n_bins)

# want to find bin edges satisfying events_per_bin
hist, bin_edges = np.histogram(sig_pred, bins=n_bins)
bin_iter = np.tile(0.0, len(bin_edges))
#print(hist)
#print(bin_edges)
#print()

i_bins = np.tile(0, n_bins + 1)
i_min = 0
i_max = len(sig_pred)
i_bins[-1] = -1
for i in range(2, n_bins+1):
    while np.abs(len(sig_pred[i_min:i_max]) - events_per_bin) > 1:
        i_min += 1
    
    #print(i_min, i_max, len(sig_pred[i_min:i_max]))
    i_bins[-i] = i_min
    i_max = i_min
    i_min = 0

bins = np.sort(sig_pred)[i_bins]
hist, bin_edges = np.histogram(sig_pred, bins=bins)

print(bin_edges)
