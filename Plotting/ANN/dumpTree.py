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
print 'Nentries: ',tree.GetEntries(),tree1.GetEntries()
for e in tree1:
    if e.n_jet==2 and e.met_tst_et>150.0e3 and ((e.n_basemu==0 and e.n_baseel==0 and e.n_ph==0)) and abs(e.met_tst_j1_dphi)>1.0 and abs(e.met_tst_j2_dphi)>1.0:
        #print e.met_tst_et
        vbf+=[[e.w,e.jj_mass/1.0e3,e.jj_deta,e.met_tst_et/1.0e3,e.jj_dphi,e.jet_pt[0]/1.0e3,e.jet_pt[1]/1.0e3,e.met_soft_tst_et/1.0e3]]
for e in tree:
    if e.n_jet==2 and e.met_tst_et>150.0e3 and ((e.n_basemu==0 and e.n_baseel==0 and e.n_ph==0)) and abs(e.met_tst_j1_dphi)>1.0 and abs(e.met_tst_j2_dphi)>1.0:
        z_strong+=[[e.w,e.jj_mass/1.0e3,e.jj_deta,e.met_tst_et/1.0e3,e.jj_dphi,e.jet_pt[0]/1.0e3,e.jet_pt[1]/1.0e3,e.met_soft_tst_et/1.0e3]]


print 'nvbf: ',len(vbf)
example_dict['z_strong'] = z_strong
example_dict['vbf'] = vbf
pickle_out = open("dict7a.pickle","wb")
pickle.dump(example_dict, pickle_out)
pickle_out.close()
