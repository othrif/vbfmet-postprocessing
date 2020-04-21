import numpy as np
import os
from root_numpy import root2array, tree2array

fs = ['/share/t3data2/schae/v26LooseJ400/VBFH125.root',
      '/share/t3data2/schae/v26LooseJ400/Z_strong.root',
      '/share/t3data2/schae/v26LooseJ400/W_strong.root',
      '/share/t3data2/schae/v26LooseJ400/Z_EWK.root',
      '/share/t3data2/schae/v26LooseJ400/ttbar.root']

fs=['/share/t3data2/schae/PileupStudies/Mar7gam/mc16e/v37Egam/VBFHgam125.root']
branches =  ['w', 'runNumber', 'n_jet']
branches += ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
branches += ['jet_pt[2]', 'j3_centrality[0]', 'j3_centrality[1]', 'j3_min_mj_over_mjj'] # for n_jet >= 2

#branches += ['maxCentrality', 'max_mj_over_mjj','ph_pt[0]','ph_eta[0]']
#branches += ['exp(-4.0/pow(jj_deta,2))*pow(ph_eta[0]-(jet_eta[0]+jet_eta[1])/2.0,2)']
#branches += ['3.141592653589793-abs(abs(ph_phi[0]-met_tst_nolep_phi)-3.141592653589793)']
branches += ['maxCentrality', 'max_mj_over_mjj']
#selection = 'n_jet >= 2 && n_jet <= 3 && met_tst_et > 150.0e3 && (n_basemu == 0 && n_baseel == 0 && n_ph == 0) && abs(met_tst_j1_dphi) > 1.0 && abs(met_tst_j2_dphi) > 1.0'
#selection = 'n_jet >= 2 && n_jet <= 3 && met_tst_et > 150.0e3 && (n_basemu == 0 && n_baseel == 0 && n_ph == 1)'

#selection = 'n_jet >= 2 && n_jet <= 3 && met_tst_et > 150.0e3 && (n_basemu == 0 && n_baseel == 0 && n_ph == 1)'# && abs(met_tst_j1_dphi) > 1.0 && abs(met_tst_j2_dphi) > 1.0'
selection = 'n_jet >= 2 && n_jet <= 3 && met_tst_et > 120.0e3 && (n_basemu == 0 && n_baseel == 0 && n_ph == 0)'# && abs(met_tst_j1_dphi) > 1.0 && abs(met_tst_j2_dphi) > 1.0'


for f in fs:
    fname = os.path.basename(os.path.normpath(f))
    name = fname.replace('.root', '')
    tree = '{}Nominal'.format(name)

    print('Loading {}/{}'.format(f, tree))
    print('branches = {}'.format(branches))
    print('selection = {}'.format(selection))
    arr = root2array(f, tree, branches=branches, selection=selection)

    print('Saving {}.npy'.format(name))
    np.save(name , arr)
