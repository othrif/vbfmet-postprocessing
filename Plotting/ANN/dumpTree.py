import ROOT
import pickle



example_dict={}

z_strong=[]
vbf=[]

files = ['/Users/schae/testarea/HInvNov/source/Plotting/v26Loose/Z_strong.root',
         '/Users/schae/testarea/HInvNov/source/Plotting/v26Loose/VBFH125.root',    ]

signalList=[]
fin = ROOT.TFile.Open('/Users/schae/testarea/HInvNov/source/Plotting/v26Loose/Z_strong.root')
tree = fin.Get('Z_strongNominal')
fin1 = ROOT.TFile.Open('/Users/schae/testarea/HInvNov/source/Plotting/v26Loose/VBFH125.root')
tree1 = fin1.Get('VBFH125Nominal')

for e in tree1:
    if e.n_jet!=2 and e.met_tst_et>150.0e3 and e.n_basemu==0 and e.n_baseel==0 and e.n_ph==0:
        vbf+=[[e.w,e.jj_mass/1.0e3,e.jj_deta,e.met_tst_et/1.0e3,e.jj_dphi]]
for e in tree:
    if e.n_jet!=2 and e.met_tst_et>150.0e3 and e.n_basemu==0 and e.n_baseel==0 and e.n_ph==0:
        z_strong+=[[e.w,e.jj_mass/1.0e3,e.jj_deta,e.met_tst_et/1.0e3,e.jj_dphi]]


example_dict['z_strong'] = z_strong
example_dict['vbf'] = vbf
pickle_out = open("dict.pickle","wb")
pickle.dump(example_dict, pickle_out)
pickle_out.close()
