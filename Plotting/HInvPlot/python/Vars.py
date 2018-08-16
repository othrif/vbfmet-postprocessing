# these are variables to be read in. Note that vectors are read in through ReadEvent
myvars = [    ['jj_deta', '50', '0.0', '10.0'],
              ['jj_dphi', '32', '0.0', '3.2'],
              ['jj_mass', '50', '0.0', '5000.0'],
              ['trigger_met', '2', '-0.5', '1.5'],              
              ['trigger_lep', '2', '-0.5', '1.5'],              
              ['passJetCleanTight', '2', '-0.5', '1.5'],              
              ['met_tst_et', '100', '0.0', '500.0'],
              #['met_tst_phi', '32', '-3.2', '3.2'],              
              ['met_tst_nolep_et', '100', '0.0', '500.0'],      
              ['n_jet', '10', '-0.5', '9.5'],      
              ['n_el', '4', '-0.5', '3.5'],      
              ['n_mu', '4', '-0.5', '3.5'],
              ['met_tst_j1_dphi', '32', '0.0', '3.2'],              
              ['met_tst_j2_dphi', '32', '0.0', '3.2'],              
              ['met_tst_nolep_j1_dphi', '32', '0.0', '3.2'],              
              ['met_tst_nolep_j2_dphi', '32', '0.0', '3.2'],
              ]
# these are variables not stored, but that we want to plot
myplots = [
              ['jetPt0', '500', '0.0', '500.0'],              
              ['jetPt1', '500', '0.0', '500.0'],              
              ['etaj0TimesEtaj1', '200', '-100.0', '100.0'],              
              ['chanFlavor', '10', '-0.5', '9.5'],
              ['lepPt0', '500', '0.0', '500.0'],                            
              ['lepPt1', '500', '0.0', '500.0'],
              ['mll',  '200', '0.0', '200.0'],
              ['ptll', '100', '0.0', '500.0'],
              ['mt',   '200', '0.0', '200.0'],
              ['lepCh0', '3', '-1.5', '1.5'],
              ['lepCh1', '3', '-1.5', '1.5'],
              ['j0timing', '100', '-50.0', '50.0'], 
              ['j1timing', '100', '-50.0', '50.0'],              
    ]
mev_vars = ['jj_mass',
            'met_tst_et',
            'met_tst_nolep_et',
                ]
def GetVarStr(entry=0):
    varstr = []
    for i in myvars:
        varstr  +=[i[entry]]
    return varstr

def GetPltStr(entry=0):
    varstr = []
    allvars = []
    allvars += myplots
    allvars += myvars
    for i in allvars:
        varstr  +=[i[entry]]
    return varstr
