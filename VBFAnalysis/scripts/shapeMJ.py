import ROOT
from array import array
#f=ROOT.TFile.Open('/tmp/HFALL_feb18_nomU.root','UPDATE')
#f=ROOT.TFile.Open('/tmp/HFPlotALL_plotvar_feb27U.root','UPDATE')
f=ROOT.TFile.Open('/tmp/HFPlotALL_plotvar_mar5.root','UPDATE')

bins=11

#hmultijet_VBFjetSel_1Nom_SR1_obs_cuts
#httbar_VBFjetSel_9Nom_oneMuNegCR9_obs_jj_mass
# h.push_back(new TH1F((name+"_jj_mass").c_str(), (name+"_jj_mass;;").c_str(), 10, 0, 5000));
#      h.push_back(new TH1F((name+"_jj_dphi").c_str(), (name+"_jj_dphi;;").c_str(), 6, 0, 3.0));
#      h.push_back(new TH1F((name+"_met_et").c_str(), (name+"_met_et;;").c_str(), 10, 0, 800));
#      h.push_back(new TH1F((name+"_lepmet_et").c_str(), (name+"_lepmet_et;;").c_str(), 10, 0, 800));

# fake ele
hists=[]
newBinning = array('d',[0.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 3500.0, 4000.0, 4500.0, 5000.0 ])
for reg in ['oneEleCR','oneEleLowSigCR']:
    for ibin in range(1,bins+1):
        hcuts = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_cuts'
        hmjj = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_jj_mass'
        hdphijj = 'heleFakes_VBFjetSel_XNom_'+reg+'X_obs_jj_dphi'
        print hcuts.replace('X','%s' %ibin)
        mymj = f.Get(hcuts.replace('X','%s' %ibin))
        #mjj=ROOT.TH1F(hmjj.replace('X','%s' %ibin),hmjj.replace('X','%s' %ibin),10, 0, 5000)
        mjj=ROOT.TH1F(hmjj.replace('X','%s' %ibin),hmjj.replace('X','%s' %ibin),len(newBinning)-1, newBinning)
        
        dphijj=ROOT.TH1F(hdphijj.replace('X','%s' %ibin),hdphijj.replace('X','%s' %ibin),6, 0, 3.0)
        print mymj
        newmjjbin=3
        if ibin==1 or ibin==6:
            newmjjbin=3
            mjj.SetBinContent(newmjjbin,mymj.GetBinContent(1))
            mjj.SetBinError(newmjjbin,mymj.GetBinError(1))        
        if ibin==2 or ibin==7:
            newmjjbin=4
            mjj.SetBinContent(newmjjbin,mymj.GetBinContent(1))
            mjj.SetBinError(newmjjbin,mymj.GetBinError(1))
        if ibin==3 or ibin==8:
            newmjjbin=5
            mjj.SetBinContent(newmjjbin,mymj.GetBinContent(1))
            mjj.SetBinError(newmjjbin,mymj.GetBinError(1))
        if ibin==4 or ibin==9:
            newmjjbin=6
            mjj.SetBinContent(newmjjbin,0.5*mymj.GetBinContent(1))
            mjj.SetBinError(newmjjbin,0.5*mymj.GetBinError(1))
            mjj.SetBinContent(newmjjbin+1,0.3*mymj.GetBinContent(1))
            mjj.SetBinError(newmjjbin+1,0.2*mymj.GetBinError(1))
            mjj.SetBinContent(newmjjbin+2,0.2*mymj.GetBinContent(1))
            mjj.SetBinError(newmjjbin+2,0.2*mymj.GetBinError(1))            
        if ibin==5 or ibin==10:
            newmjjbin=9
            mjj.SetBinContent(newmjjbin,0.7*mymj.GetBinContent(1))
            mjj.SetBinError(newmjjbin,0.7*mymj.GetBinError(1))
            mjj.SetBinContent(newmjjbin+1,0.3*mymj.GetBinContent(1))
            mjj.SetBinError(newmjjbin+1,0.3*mymj.GetBinError(1))        
        if ibin==11:
            mjj.SetBinContent(3,0.38*mymj.GetBinContent(1))
            mjj.SetBinContent(4,0.25*mymj.GetBinContent(1))
            mjj.SetBinContent(5,0.18*mymj.GetBinContent(1))
            mjj.SetBinContent(6,0.12*mymj.GetBinContent(1))
            mjj.SetBinContent(7,0.04*mymj.GetBinContent(1))
            mjj.SetBinContent(8,0.02*mymj.GetBinContent(1))
            mjj.SetBinContent(9,0.01*mymj.GetBinContent(1))              
        if ibin in [1,2,3,4,5]:
            dphijj.SetBinContent(1,0.5*mymj.GetBinContent(1))
            dphijj.SetBinError(1,0.5*mymj.GetBinError(1))
            dphijj.SetBinContent(2,0.5*mymj.GetBinContent(1))
            dphijj.SetBinError(2,0.5*mymj.GetBinError(1))
        if ibin in [6,7,8,9,10]:
            dphijj.SetBinContent(3,0.5*mymj.GetBinContent(1))
            dphijj.SetBinError(3,0.5*mymj.GetBinError(1))
            dphijj.SetBinContent(4,0.5*mymj.GetBinContent(1))
            dphijj.SetBinError(4,0.5*mymj.GetBinError(1))
        if ibin ==11:
            dphijj.SetBinContent(1,0.25*mymj.GetBinContent(1))
            dphijj.SetBinError(1,0.25*mymj.GetBinError(1))
            dphijj.SetBinContent(2,0.25*mymj.GetBinContent(1))
            dphijj.SetBinError(2,0.25*mymj.GetBinError(1))        
            dphijj.SetBinContent(3,0.25*mymj.GetBinContent(1))
            dphijj.SetBinError(3,0.25*mymj.GetBinError(1))
            dphijj.SetBinContent(4,0.25*mymj.GetBinContent(1))
            dphijj.SetBinError(4,0.25*mymj.GetBinError(1))
        hists+=[mjj,dphijj]
    
for ibin in range(1,bins+1):
    print 'hmultijet_VBFjetSel_XNom_SRX_obs_cuts'.replace('X','%s' %ibin)
    mymj = f.Get('hmultijet_VBFjetSel_XNom_SRX_obs_cuts'.replace('X','%s' %ibin))
    #mjj=ROOT.TH1F('hmultijet_VBFjetSel_XNom_SRX_obs_jj_mass'.replace('X','%s' %ibin),'hmultijet_VBFjetSel_XNom_SRX_obs_jj_mass'.replace('X','%s' %ibin),10, 0, 5000)
    #newBinning = array.array('d',[0.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 3500.0, 4000.0, 4500.0, 5000.0 ])
    mjj=ROOT.TH1F('hmultijet_VBFjetSel_XNom_SRX_obs_jj_mass'.replace('X','%s' %ibin),'hmultijet_VBFjetSel_XNom_SRX_obs_jj_mass'.replace('X','%s' %ibin),len(newBinning)-1, newBinning)    
    dphijj=ROOT.TH1F('hmultijet_VBFjetSel_XNom_SRX_obs_jj_dphi'.replace('X','%s' %ibin),'hmultijet_VBFjetSel_XNom_SRX_obs_jj_dphi'.replace('X','%s' %ibin),6, 0, 3.0)
    print mymj
    newmjjbin=3
    if ibin==1 or ibin==6:
        newmjjbin=3
        mjj.SetBinContent(newmjjbin,mymj.GetBinContent(1))
        mjj.SetBinError(newmjjbin,mymj.GetBinError(1))        
    if ibin==2 or ibin==7:
        newmjjbin=4
        mjj.SetBinContent(newmjjbin,mymj.GetBinContent(1))
        mjj.SetBinError(newmjjbin,mymj.GetBinError(1))
    if ibin==3 or ibin==8:
        newmjjbin=5
        mjj.SetBinContent(newmjjbin,mymj.GetBinContent(1))
        mjj.SetBinError(newmjjbin,mymj.GetBinError(1))
    if ibin==4 or ibin==9:
        newmjjbin=6
        mjj.SetBinContent(newmjjbin,0.6*mymj.GetBinContent(1))
        mjj.SetBinError(newmjjbin,0.6*mymj.GetBinError(1))
        mjj.SetBinContent(newmjjbin+1,0.3*mymj.GetBinContent(1))
        mjj.SetBinError(newmjjbin+1,0.3*mymj.GetBinError(1))
        mjj.SetBinContent(newmjjbin+2,0.1*mymj.GetBinContent(1))
        mjj.SetBinError(newmjjbin+2,0.1*mymj.GetBinError(1))        
    if ibin==5 or ibin==10:
        newmjjbin=9
        mjj.SetBinContent(newmjjbin,0.7*mymj.GetBinContent(1))
        mjj.SetBinError(newmjjbin,0.7*mymj.GetBinError(1))
        mjj.SetBinContent(newmjjbin+1,0.3*mymj.GetBinContent(1))
        mjj.SetBinError(newmjjbin+1,0.3*mymj.GetBinError(1))        
    if ibin==11:
        mjj.SetBinContent(3,0.38*mymj.GetBinContent(1))
        mjj.SetBinContent(4,0.25*mymj.GetBinContent(1))
        mjj.SetBinContent(5,0.18*mymj.GetBinContent(1))
        mjj.SetBinContent(6,0.13*mymj.GetBinContent(1))
        mjj.SetBinContent(7,0.05*mymj.GetBinContent(1))
        mjj.SetBinContent(8,0.01*mymj.GetBinContent(1))        


    if ibin in [1,2,3,4,5]:
        dphijj.SetBinContent(1,0.5*mymj.GetBinContent(1))
        dphijj.SetBinError(1,0.5*mymj.GetBinError(1))
        dphijj.SetBinContent(2,0.5*mymj.GetBinContent(1))
        dphijj.SetBinError(2,0.5*mymj.GetBinError(1))
    if ibin in [6,7,8,9,10]:
        dphijj.SetBinContent(3,0.5*mymj.GetBinContent(1))
        dphijj.SetBinError(3,0.5*mymj.GetBinError(1))
        dphijj.SetBinContent(4,0.5*mymj.GetBinContent(1))
        dphijj.SetBinError(4,0.5*mymj.GetBinError(1))
    if ibin ==11:
        dphijj.SetBinContent(1,0.25*mymj.GetBinContent(1))
        dphijj.SetBinError(1,0.25*mymj.GetBinError(1))
        dphijj.SetBinContent(2,0.25*mymj.GetBinContent(1))
        dphijj.SetBinError(2,0.25*mymj.GetBinError(1))        
        dphijj.SetBinContent(3,0.25*mymj.GetBinContent(1))
        dphijj.SetBinError(3,0.25*mymj.GetBinError(1))
        dphijj.SetBinContent(4,0.25*mymj.GetBinContent(1))
        dphijj.SetBinError(4,0.25*mymj.GetBinError(1))          

    print 'dphi: ',dphijj.Integral()
    print mjj.Integral()
    hists+=[mjj,dphijj]


for h in hists:
    f.cd()
    h.SetDirectory(f)
    h.Write()

f.Close()
