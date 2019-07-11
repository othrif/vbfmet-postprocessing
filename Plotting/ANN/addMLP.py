import numpy as np
import ROOT
from keras.models import Sequential
from sklearn import preprocessing
import pickle
import ROOT
import os,sys
from array import array
ann_score = array( 'f', [ 0.0 ] )

# input directory
#idir='/share/t3data2/schae/v26LooseNoExtSystMETTrigSYST/'
idir='/share/t3data2/schae/v26Loose_BTAGW_TightSkim/'
odir='/share/t3data2/schae/v26Loose_BTAGW_TightSkim_7var/'
dlist = os.listdir(idir)

# returns a compiled model
from keras.models import load_model
# identical to the previous one                          
model = load_model('my_model_7var.h5')
# load the scaler
from sklearn.externals import joblib
scaler = joblib.load('my_scaler_7var.save') 

for d in dlist:
    print(d)
    sys.stdout.flush()
    #if not d.count('VBF'):
    #    continue
    fin1 = ROOT.TFile.Open(idir+d)
    file_tree_list = fin1.GetListOfKeys()
    for key in file_tree_list:
        print('%s %s' %(key.GetName(),key.GetClassName()))
        #if key.GetClassName()=='TTree':
        if key.GetClassName()=='TTree' and key.GetName().count('Nominal'):

            tree_in = fin1.Get(key.GetName())

            vbf=[]
            n=0
            for e in tree_in:
                #vbf+=[[e.jj_mass/1.0e3,e.jj_deta,e.met_tst_et/1.0e3,e.jj_dphi,e.jet_pt[0]/1.0e3,e.jet_pt[1]/1.0e3]]
                vbf+=[[e.jj_mass/1.0e3,e.jj_deta,e.met_tst_et/1.0e3,e.jj_dphi,e.jet_pt[0]/1.0e3,e.jet_pt[1]/1.0e3,e.met_soft_tst_et/1.0e3]]
                n+=1
                #if n>100:
                #    break
            # preprocess data
            X_train = np.array(vbf)
            X_train = scaler.transform(X_train)
            y_pred = model.predict(X_train)
            #print(y_pred)

            # create the output file and output tree
            fout = ROOT.TFile.Open(odir+d,'RECREATE')
            tree_out = tree_in.CloneTree(0)
            tree_out.Branch("tmva",ann_score,'tmva/f')
            tree_out.SetDirectory(fout)
            
            nent = tree_in.GetEntries()    
            print('Nentries: %s %s'%(nent,d))
            
            
            n=0
            for e in range(0,nent):
                if n%1e5==0:
                    print('   Processed: %s' %n)
                tree_in.GetEntry(e)
                ann_score[0]=y_pred[e]
                tree_out.Fill()
                n+=1
                #if n>100:
                #    break;
                
            # write the output tree 
            tree_out.Write()
            fout.Close()
            fin1.Close()
print('DONE')
