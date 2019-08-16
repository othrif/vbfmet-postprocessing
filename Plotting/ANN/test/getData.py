import numpy as np
import os
from root_numpy import root2array, tree2array

## 2016 (or was it 2015...?)
#fs = ['/share/t3data2/schae/v26LooseJ400/VBFH125.root',
#      '/share/t3data2/schae/v26LooseJ400/Z_strong.root',
#      '/share/t3data2/schae/v26LooseJ400/W_strong.root',
#      '/share/t3data2/schae/v26LooseJ400/Z_EWK.root',
#      '/share/t3data2/schae/v26LooseJ400/ttbar.root']

## 2016 with Q/G
#fs = ['/share/t3data2/schae/v26Loose_QG/VBFH125.root',
#      '/share/t3data2/schae/v26Loose_QG/Z_strong.root',
#      '/share/t3data2/schae/v26Loose_QG/W_strong.root',
#      '/share/t3data2/schae/v26Loose_QG/Z_EWK.root',
#      '/share/t3data2/schae/v26Loose_QG/ttbar.root']

## 2018
#fs = ['/share/t3data2/schae/v28LooseNominalFixXS/VBFH125.root',
#      '/share/t3data2/schae/v28LooseNominalFixXS/Z_strong.root',
#      '/share/t3data2/schae/v28LooseNominalFixXS/W_strong.root',
#      '/share/t3data2/schae/v28LooseNominalFixXS/Z_EWK.root',
#      '/share/t3data2/schae/v28LooseNominalFixXS/ttbar.root']

## 2016 with more stats
#fs = ['/share/t3data2/schae/v26LooseJ400/VBFH125.root',
#      '/share/t3data2/schae/v31_mergedLOMGWZ/Z_strongNominal.root']
#      '/share/t3data2/schae/v31_mergedLOMGWZ/W_strongNominal.root',
#      '/share/t3data2/schae/v26LooseJ400/Z_EWK.root',
#      '/share/t3data2/schae/v26LooseJ400/ttbar.root']

## filtered only
#fs = ['/share/t3data2/schae/v26LooseJ400/VBFH125.root',
#      '/share/t3data2/schae/v31_mergedLOMGWZ/Z_strongNominalFiltOnly.root']

## inclusive only
#fs = ['/share/t3data2/schae/v26LooseJ400/VBFH125.root',
#      '/share/t3data2/schae/v31_mergedLOMGWZ/Z_strongNominalIncl.root']

## more QG
#fs = ['/share/t3data2/schae/v26LooseQGVars/VBFH125.root',
#      '/share/t3data2/schae/v26LooseQGVars/Z_strong.root',
#      '/share/t3data2/schae/v26LooseQGVars/W_strong.root',
#      '/share/t3data2/schae/v26LooseQGVars/Z_EWK.root',
#      '/share/t3data2/schae/v26LooseQGVars/ttbar.root']

# v26 + v28
fs = ['/share/t3data2/schae/v26LooseQGVars/VBFH125.root',
      '/share/t3data2/schae/v26LooseQGVars/Z_strong.root',
      '/share/t3data2/schae/v26LooseQGVars/W_strong.root',
      '/share/t3data2/schae/v26LooseQGVars/Z_EWK.root',
      '/share/t3data2/schae/v26LooseQGVars/ttbar.root',
      '/share/t3data2/schae/v28LooseNominalFixXS/VBFH125.root',
      '/share/t3data2/schae/v28LooseNominalFixXS/Z_strong.root',
      '/share/t3data2/schae/v28LooseNominalFixXS/W_strong.root',
      '/share/t3data2/schae/v28LooseNominalFixXS/Z_EWK.root',
      '/share/t3data2/schae/v28LooseNominalFixXS/ttbar.root']

branches =  ['w', 'runNumber', 'n_jet']
branches += ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
branches += ['jet_eta[0]', 'jet_eta[1]', 'jet_phi[0]', 'jet_phi[1]']
branches += ['jet_pt[2]', 'j3_centrality[0]', 'j3_centrality[1]', 'j3_min_mj_over_mjj'] # for n_jet >= 2
branches += ['maxCentrality', 'max_mj_over_mjj']
branches += ['met_tenacious_tst_et', 'met_tight_tst_et', 'met_cst_jet']
#branches += ['jet_TrackWidth[0]', 'jet_TrackWidth[1]', 'jet_NTracks[0]', 'jet_NTracks[1]']

selection = 'n_jet >= 2 && n_jet <= 4 && met_tst_et > 150.0e3 && (n_basemu == 0 && n_baseel == 0 && n_ph == 0) && abs(met_tst_j1_dphi) > 1.0 && abs(met_tst_j2_dphi) > 1.0 && jj_mass > 500e3'

print('branches = {}'.format(branches))
print('selection = {}'.format(selection))

for f in fs:
    #fname = os.path.basename(os.path.normpath(f))
    fname = f.split('/')[-1]
    fdir = f.split('/')[-2]
    name = fname.replace('.root', '')
    if 'Nominal' in name:
        name = name.replace('Nominal', '')
    if 'Incl' in name:
        name = name.replace('Incl', '')
    if 'FiltOnly' in name:
        name = name.replace('FiltOnly', '')
    tree = '{}Nominal'.format(name)

    print('Loading {}/{}'.format(f, tree))
    arr = root2array(f, tree, branches=branches, selection=selection)

    print('Saving {}.npy'.format(name))
    np.save('{}_{}'.format(fdir, name), arr)
