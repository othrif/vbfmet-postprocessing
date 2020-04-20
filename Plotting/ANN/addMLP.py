import numpy as np
import ROOT
from keras.models import Sequential
from sklearn import preprocessing
import pickle
import ROOT
import os,sys
from array import array
from custom_loss import focal_loss
ann_score = array( 'f', [ 0.0 ] )

# input directory
#name_model='_VBFH125_Z_strong'
name_model='_zstrong'
#name_model='_zstrong'
#name_model='_njet'
#idir='/share/t3data2/schae/v26LooseNoExtSystMETTrigSYST/'
idir='/share/t3data2/schae/v26Loose_BTAGW_TightSkim/'
odir='/share/t3data2/schae/v26Loose_BTAGW_TightSkim_7var'+name_model+'/'
if not os.path.exists(odir):
    os.mkdir(odir)
dlist = os.listdir(idir)

# returns a compiled model
from keras.models import load_model
# identical to the previous one                          
#model_dir='/home/smau/testarea/HInv/STPostProcessing/Plotting/ANN/'
model_dir='./'
model = load_model(model_dir+'model'+name_model+'.hf')
# load the scaler
from sklearn.externals import joblib
scaler = joblib.load(model_dir+'scaler'+name_model+'.save') 

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
                #'jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]'
                vbf+=[[e.jj_mass,e.jj_deta,e.jj_dphi,e.met_tst_nolep_et,e.met_soft_tst_et,e.jet_pt[0],e.jet_pt[1]]]
                #vbf+=[[e.jj_mass,e.jj_deta,e.jj_dphi,e.met_tst_nolep_et,e.met_soft_tst_et,e.jet_pt[0],e.jet_pt[1],e.n_jet]]
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
