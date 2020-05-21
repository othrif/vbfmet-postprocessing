import ROOT
import math
import array

path='/nfs/dust/atlas/user/othrif/vbf/myPP/run_130520_zee/theoryVariation'
#f1=ROOT.TFile.Open(path+'/'+'theoVariation_Z_strong_ckkw30.root')
#f2=ROOT.TFile.Open(path+'/'+'theoVariation_Z_strong_ckkw15.root')

f1=ROOT.TFile.Open(path+'/'+'theoVariation_Z_strong_qsf025.root')
f2=ROOT.TFile.Open(path+'/'+'theoVariation_Z_strong_qsf4.root')


hname = ['jj_mass_Incl_nominal','jj_mass_SRPhi_nominal', 'jj_mass_CRZPhi_nominal'] # 'jj_mass_CRWPhi_nominal'
hname1='jj_mass_Incl_nominal'
hname2='jj_mass_Incl_nominal'

for hn in hname:
    h1 = f1.Get(hn)
    h2 = f2.Get(hn)

    bins = [0.8, 1, 1.5, 2, 3.5, 100]
    h1N = h1.Rebin(5,"h1Rebin",array.array('d',bins))
    h2N = h2.Rebin(len(bins)-1,"h2Rebin",array.array('d',bins))

    up = []
    for i in range(0,h1N.GetNbinsX()+1):
        val = h1N.GetBinContent(i)
        err = h1N.GetBinError(i)
        up.append(val)

    dn = []
    for i in range(0,h2N.GetNbinsX()+1):
        val = h2N.GetBinContent(i)
        err = h2N.GetBinError(i)
        dn.append(val)

    print "="*50
    print hn
    print "="*50
    for i in range(len(up)):
        if (up[i]+dn[i]) != 0:
            print i, (up[i]-dn[i])/(up[i]+dn[i])
        else:
            print "skipping!"
    print "="*50