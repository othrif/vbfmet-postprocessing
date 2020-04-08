import numpy as np
import os
from root_numpy import root2array, tree2array

fs_mc16a = ['/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Agam/VBFHgam125.root', 
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Agam/Wg_EWK.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Agam/Wg_strong.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Agam/Zg_EWK.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Agam/Zg_strong.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Agam/ttg.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Agam/SinglePhoton.root']

fs_mc16d = ['/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Dgam/VBFHgam125.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Dgam/Wg_EWK.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Dgam/Wg_strong.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Dgam/Zg_EWK.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Dgam/Zg_strong.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Dgam/ttg.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Dgam/SinglePhoton.root']

fs_mc16e = ['/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/VBFHgam125.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/Wg_EWK.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/Wg_strong.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/Zg_EWK.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/Zg_strong.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/ttg.root',
            '/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/SinglePhoton.root']

branches =  ['w', 'runNumber', 'n_jet']
branches += ['jj_mass', 'jj_deta', 'jj_dphi', 'met_tst_et', 'met_soft_tst_et', 'jet_pt[0]', 'jet_pt[1]']
branches += ['jet_pt[2]', 'j3_centrality[0]', 'j3_centrality[1]', 'j3_min_mj_over_mjj'] # for n_jet >= 2
branches += ['maxCentrality', 'max_mj_over_mjj']

#stuff i am adding :)
branches += ['ph_pt[0]']
branches += ['exp(-4.0/pow(jj_deta,2))*pow(ph_eta[0]-(jet_eta[0]+jet_eta[1])/2.0,2)']
branches += ['3.141592653589793-abs(abs(ph_phi[0]-met_tst_nolep_phi)-3.141592653589793)']

#selection = 'n_jet >= 2 && n_jet <= 3' && met_tst_et > 150.0e3 && (n_basemu == 0 && n_baseel == 0 && n_ph == 0) && abs(met_tst_j1_dphi) > 1.0 && abs(met_tst_j2_dphi) > 1.0'

selection = 'n_jet <= 3 && n_jet >= 2  && met_tst_et > 150.0e3 && (n_basemu == 0 && n_baseel == 0 && n_ph == 1)'

def get_arr_from_file(filepath):
    fname = os.path.basename(os.path.normpath(filepath))
    name = fname.replace('.root', '')
    tree = '{}Nominal'.format(name)

    print('Loading {}/{}'.format(filepath, tree))
    print('branches = {}'.format(branches))
    print('selection = {}'.format(selection))
    arr = root2array(filepath, tree, branches=branches, selection=selection)   
    return name, arr


for i in range(len(fs_mc16a)):
    name, arr_a = get_arr_from_file(fs_mc16a[i])
    name_d, arr_d = get_arr_from_file(fs_mc16d[i])
    name_e, arr_e = get_arr_from_file(fs_mc16e[i])

    arr = np.concatenate([arr_a, arr_d, arr_e])
    print(len(arr))
    print('Saving {}.npy'.format(name))
    np.save(name , arr_a)


"""
for f in fs_mc16d:

    fname = os.path.basename(os.path.normpath(f))
    name = fname.replace('.root', '')
    tree = '{}Nominal'.format(name)

    print('Loading {}/{}'.format(f, tree))
    print('branches = {}'.format(branches))
    print('selection = {}'.format(selection))
    arr = root2array(f, tree, branches=branches, selection=selection)

    name = name + "_d"
    print('Saving {}.npy'.format(name))
    np.save(name , arr)

for f in fs_mc16e:

    fname = os.path.basename(os.path.normpath(f))
    name = fname.replace('.root', '')
    name = name
    tree = '{}Nominal'.format(name)

    print('Loading {}/{}'.format(f, tree))
    print('branches = {}'.format(branches))
    print('selection = {}'.format(selection))
    arr = root2array(f, tree, branches=branches, selection=selection)

    name = name + "_e"
    print('Saving {}.npy'.format(name))
    np.save(name , arr)"""
