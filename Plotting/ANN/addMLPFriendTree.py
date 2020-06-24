#!/usr/bin/env python
import numpy as np
import numpy.lib.recfunctions as recfn
import os,sys
from root_numpy import root2array, tree2array
from root_numpy import array2tree, array2root
from custom_loss import *

import ROOT
from keras.models import Sequential
from sklearn import preprocessing
import pickle
from array import array

###
### the below block should be the only changes that are required
###
RegN='E'
#model_dir='/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/MVA/models/April15_trainAE/' # directory with the keras model
model_dir='/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/MVA/models/' # directory with the keras model
#name_model='_v37syst' # model partial name
name_model='_zstrong_ttbar_wstrong_zewk_qg_v34A_test_4_best' # model partial name
#idir='/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37ESyst/' # input directory
idir='/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37/v37'+RegN+'Tight/' # input directory
#idir='/eos/atlas/atlascerngroupdisk/penn-ww/schae/VBFHPlots/MJSystKerasv1/v37'+RegN+'MJSyst/'
#idir='/eos/atlas/atlascerngroupdisk/penn-ww/schae/v37MJSyst/v37'+RegN+'MJSyst/'
#idir='/tmp/v37Esyst'+name_model+'/' # output directory. will copy all files here because we will add a variable to the ntuples. do not want to risk damaging the files
#idir='/tmp/mj_noMJ/'
#idir='/tmp/mj/'
#idir='/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37/v37DTight/'
#odir='/tmp/v37Esyst'+name_model+'/' # output directory. will copy all files here because we will add a variable to the ntuples. do not want to risk damaging the files
#odir='/tmp/mj_noMJ/'
#odir='/tmp/mj/'
#odir='/eos/atlas/atlascerngroupdisk/penn-ww/schae/v37Esyst'+name_model+'/' # output directory. will copy all files here because we will add a variable to the ntuples. do not want to risk damaging the files
odir='/eos/atlas/atlascerngroupdisk/penn-ww/schae/v37TightApr15b/v37'+RegN+'syst'+name_model+'/' # output directory. will copy all files here because we will add a variable to the ntuples. do not want to risk damaging the files
#odir='/eos/atlas/atlascerngroupdisk/penn-ww/schae/VBFHPlots/MJSystKerasv1/v37'+RegN+'MJSyst/'
#odir='/eos/atlas/atlascerngroupdisk/penn-ww/schae/v37MJSyst/v37'+RegN+'MJSyst/'
#odir='/tmp/mj_noMJ/'
#variables used for training:
#COLS  = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
#COLS= ['jj_mass', 'jj_dphi', 'jj_deta', 'jet_pt[0]', 'jet_pt[1]',  'met_tst_et', 'met_tenacious_tst_et',  'met_soft_tst_et', 'met_cst_jet',  'n_jet', 'maxCentrality']
#COLS = ['jj_mass', 'jj_deta','maxCentrality', 'jj_dphi', 'met_soft_tst_et', 'n_jet', 'met_tst_nolep_et', 'met_cst_jet', 'jet_pt[0]', 'jet_pt[1]', 'met_tenacious_tst_nolep_et'] # ava
COLS = ['jj_mass', 'jj_dphi', 'jj_deta', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]', 'met_tenacious_tst_nolep_et', 'met_soft_tst_et', 'met_cst_jet', 'n_jet'] # george
###
### the above block should be the only changes that are required
###

# create the output directory
if not os.path.exists(odir):
    os.mkdir(odir)

# returns a compiled model
from keras.models import load_model

# load the keras model
model = load_model(model_dir+'model'+name_model+'.hf',custom_objects={'focal_loss': focal_loss, 'sig_eff': sig_eff})
# load the scaler
from sklearn.externals import joblib
scaler = joblib.load(model_dir+'scaler'+name_model+'.save') 

if not os.path.exists(idir):
    print('path does not exist: %s' %(idir))
listdir = os.listdir(idir)
print(listdir)

# copy the inputs to a new directory because we will overwrite
for i in listdir:
    cpcmd='cp '+idir.rstrip('/')+'/'+i+' '+odir.rstrip('/')+'/'+i
    print(cpcmd)
    os.system(cpcmd)

#prepare the list of files
fs=[] #fs =['/tmp/v37Egam/VBFHgam125.root']
for i in listdir:
    fs+=[odir.rstrip('/')+'/'+i]
print(fs)

#branches =  ['w', 'runNumber', 'n_jet']
#branches = ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
branches = ['jj_mass', 'jj_dphi', 'jj_deta', 'met_tst_et', 'jet_pt[0]', 'jet_pt[1]', 'met_tenacious_tst_nolep_et', 'met_soft_tst_et', 'met_cst_jet', 'n_jet'] # george
#branches += ['jet_pt[2]', 'j3_centrality[0]', 'j3_centrality[1]', 'j3_min_mj_over_mjj'] # for n_jet >= 2
#branches += ['maxCentrality', 'max_mj_over_mjj']

# cross checking we have all of the variables. probably could just merge them in if not, but for now killing the job.
for C in COLS:
    if C not in branches:
        print('all variables must be in the branches!!! Missing... %s. it will be added for you' %C)
        branches+=[C]

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
            if not key.GetName().count('Nominal'):
                continue
            print(key.GetName())
            TreeList+=[key.GetName()]
    myfile.Close()
    # iterate through the trees
    for treeName in TreeList:
        print('Loading {}/{}'.format(f, treeName))
        print('branches = {}'.format(branches))
        print('selection = {}'.format(selection))
        arr = root2array(f, treeName, branches=branches, selection=selection)

        if 'maxCentrality' in arr.dtype.names and ('QCDDD' in treeName):
            print('correcting maxcentrality %s' %(treeName))
            loadCen = arr['maxCentrality']
            loadCen[loadCen <-0.1]=0.0
        if 'max_mj_over_mjj' in arr.dtype.names and ('QCDDD' in treeName):
            print('correcting max_mj_over_mjjy %s' %(treeName))
            loadCen = arr['max_mj_over_mjj']
            loadCen[loadCen <-0.1]=0.0

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
        #tree = array2tree(y_pred, name=treeName+'TMVA')
        tree = array2tree(y_pred, name=treeName)
        
        # Or write directly into a ROOT file without using PyROOT
        #array2root(y_pred, name+'TMVA.root', treeName+'TMVA')
        array2root(y_pred, f, treeName)

print('Done')
