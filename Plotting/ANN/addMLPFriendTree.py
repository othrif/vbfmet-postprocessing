import numpy as np
import numpy.lib.recfunctions as recfn
import os,sys
from root_numpy import root2array, tree2array
from root_numpy import array2tree, array2root

import ROOT
from keras.models import Sequential
from sklearn import preprocessing
import pickle
import ROOT
from array import array
from custom_loss import focal_loss
#ann_score = array( 'f', [ 0.0 ] )

# input directory
name_model='_test'
idir=''
odir='/tmp/v26Loose_BTAGW_TightSkim_7var'+name_model+'/'
if not os.path.exists(odir):
    os.mkdir(odir)
#dlist = os.listdir(idir)

# returns a compiled model
from keras.models import load_model
# identical to the previous one
model_dir='./training_set/'
model = load_model(model_dir+'model'+name_model+'.hf')
# load the scaler
from sklearn.externals import joblib
scaler = joblib.load(model_dir+'scaler'+name_model+'.save') 

fs =['/tmp/v37Egam/VBFHgam125.root']

#branches =  ['w', 'runNumber', 'n_jet']
branches = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
#branches += ['jet_pt[2]', 'j3_centrality[0]', 'j3_centrality[1]', 'j3_min_mj_over_mjj'] # for n_jet >= 2
#branches += ['maxCentrality', 'max_mj_over_mjj']

#variables used for training:
COLS  = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']

for C in COLS:
    if C not in branches:
        print('all variables must be in the branches!!! Missing... %s' %C)
        sys.exit(0)

# no selection here. we want to make a friend tree
selection = '1'

for f in fs:
    myfile=ROOT.TFile.Open(f)
    if not myfile:
        print('Missing file: %s' %f)
        continue

    TreeList=[]
    fname = os.path.basename(os.path.normpath(f))
    name = fname.replace('.root', '')
    #treeName = '{}Nominal'.format(name)
    # Collect the tree names
    for key in myfile.GetListOfKeys():
        if key.GetClassName()=='TTree':
            print(key.GetName())
            TreeList+=[key.GetName()]
    # iterate through the trees
    for treeName in TreeList:
        print('Loading {}/{}'.format(f, treeName))
        print('branches = {}'.format(branches))
        print('selection = {}'.format(selection))
        arr = root2array(f, treeName, branches=branches, selection=selection)
        
        print('Loaded numpy array {}.npy'.format(name))
        #Loading array
        label_arr = np.ones(len(arr))
        arr_labelled = recfn.rec_append_fields(arr, 'label', label_arr)
        # loading the correct set of variables used in the MVA
        X_train = arr_labelled[COLS] # use only COLS
        X_train = X_train.astype([(name, '<f8') for name in X_train.dtype.names]).view(('<f8', len(X_train.dtype.names))) # convert from recarray to array
        # transforming the variables
        X_train = scaler.transform(X_train)
        # running the MVA
        y_pred = model.predict(X_train)
        
        # Rename the fields    
        y_pred=np.array(y_pred,dtype=[('tmva', np.float32)])
        #y_pred.dtype.names = ('tmva')
        
        # Convert the NumPy array into a TTree
        tree = array2tree(y_pred, name=treeName+'TMVA')
        
        # Or write directly into a ROOT file without using PyROOT
        array2root(y_pred, name+'TMVA.root', treeName+'TMVA')
