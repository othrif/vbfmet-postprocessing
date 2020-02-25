import ROOT

def GetNF(f,region1,lowbin,highbin, isZ=True, znf=1.0, wnf=1.0, isMJ=False):

    dataznf =0.0
    wznf = 0.0
    zznf = 0.0
    bkgznf=0.0
    multijet=0.0
    multijet_err=ROOT.Double(0.0)
    for i in ['tall']:
        try:
            bkgznf+=f.Get(region1+'/plotEvent_'+i+'/jj_dphi').Integral(lowbin,highbin)
        except:
            print region1+'/plotEvent_'+i+'/jj_dphi'
    for i in ['data']:
        try:
            dataznf+=f.Get(region1+'/plotEvent_'+i+'/jj_dphi').Integral(lowbin,highbin)
        except:
            print region1+'/plotEvent_'+i+'/jj_dphi'
    for i in ['zewk','zqcd']:
        zznf+=f.Get(region1+'/plotEvent_'+i+'/jj_dphi').Integral(lowbin,highbin)
    for i in ['wewk','wqcd']:
        wznf+=f.Get(region1+'/plotEvent_'+i+'/jj_dphi').Integral(lowbin,highbin)
    for i in ['dqcd']:
        multijet+=f.Get(region1+'/plotEvent_'+i+'/jj_dphi').IntegralAndError(lowbin,highbin,multijet_err)             

    if isMJ:
        print 'MJ error: ',multijet_err/multijet
        return max(0.0,(dataznf-bkgznf-wnf*wznf -znf*zznf)/multijet)
        
    if isZ:
        return max(0.0,(dataznf-bkgznf-wznf)/zznf)
    else:
        return max(0.0,(dataznf-bkgznf-zznf)/wznf)

inputDir='/tmp/'
year=2018
#f=ROOT.TFile.Open('/tmp/new2016_qcd_all_KT_metTrigJER.root')
#f=ROOT.TFile.Open('/tmp/new2017_qcd_all_KT.root')
f=None
f2=None
if year==2016:
    f=ROOT.TFile.Open(inputDir+'/new2016_qcd_all_KT_metTrigJER.root')
    f2=ROOT.TFile.Open(inputDir+'/new2016_qcd_all_KT_metTrigJERHT.root')
if year==2017:
    f=ROOT.TFile.Open(inputDir+'/new2017_qcd_all_KT_metTrigJER.root')
    f2=ROOT.TFile.Open(inputDir+'/new2017_qcd_all_KT_metTrigJERHT.root')
    #f=ROOT.TFile.Open(inputDir+'/new2017_qcd_all_KT.root')
    #f2=ROOT.TFile.Open(inputDir+'/new2017_qcd_all_KT.root')
if year==2018:
    f=ROOT.TFile.Open(inputDir+'/new2018_qcd_KT_metTrigJER.root')
    f2=ROOT.TFile.Open(inputDir+'/new2018_qcd_KT_metTrigJERHT.root')
if year==2019:
    f=ROOT.TFile.Open(inputDir+'/new2019_qcd_all_KT_metTrigJERnew.root')
    f2=ROOT.TFile.Open(inputDir+'/new2019_qcd_all_KT_metTrigJERHT.root')

bkg=['data','zewk','zqcd','wewk','wqcd','tall']

print ''
print 'BDT trigger weight'
print ''
print 'Low dphi'
lowbin=0
highbin=10
region1='pass_zcr_mjjLow200_uu_Nominal'
region2='pass_wcr_mjjLow200_u_Nominal'
region3='pass_sr_mjjLow200_nn_Nominal'
ZNF=GetNF(f,region1,lowbin,highbin, isZ=True)
WNF=GetNF(f,region2,lowbin,highbin, isZ=False)
print region1,ZNF
print region2,WNF
mjNF1_BDTlow=GetNF(f,region3,lowbin,highbin, True, ZNF,WNF, True)
print region3,mjNF1_BDTlow

region1='pass_zcr_LowMETQCDSRFJVT_uu_Nominal'
region2='pass_wcr_LowMETQCDSRFJVT_u_Nominal'
region3='pass_sr_LowMETQCDSRFJVT_nn_Nominal'
ZNF=GetNF(f,region1,lowbin,highbin, isZ=True)
WNF=GetNF(f,region2,lowbin,highbin, isZ=False)
print region1,ZNF
print region2,WNF
mjnf2_BDTlow=GetNF(f,region3,lowbin,highbin, True, ZNF,WNF, True)
print region3,mjnf2_BDTlow

print 'Avg: ',(mjNF1_BDTlow+mjnf2_BDTlow)/2.0
print ''

print 'High dphi'
lowbin=11
highbin=50
region1='pass_zcr_mjjLow200_uu_Nominal'
region2='pass_wcr_mjjLow200_u_Nominal'
region3='pass_sr_mjjLow200_nn_Nominal'
ZNF=GetNF(f,region1,lowbin,highbin, isZ=True)
WNF=GetNF(f,region2,lowbin,highbin, isZ=False)
print region1,ZNF
print region2,WNF
mjNF1_BDThigh=GetNF(f,region3,lowbin,highbin, True, ZNF,WNF, True)
print region3,mjNF1_BDThigh

region1='pass_zcr_LowMETQCDSRFJVT_uu_Nominal'
region2='pass_wcr_LowMETQCDSRFJVT_u_Nominal'
region3='pass_sr_LowMETQCDSRFJVT_nn_Nominal'
ZNF=GetNF(f,region1,lowbin,highbin, isZ=True)
WNF=GetNF(f,region2,lowbin,highbin, isZ=False)
print region1,ZNF
print region2,WNF
mjnf2_BDThigh=GetNF(f,region3,lowbin,highbin, True, ZNF,WNF, True)
print region3,mjnf2_BDThigh

print 'Avg: ',(mjNF1_BDThigh+mjnf2_BDThigh)/2.0

print ''
print 'HT trigger weight'
print ''
print 'Low dphi'
lowbin=0
highbin=10
region1='pass_zcr_mjjLow200_uu_Nominal'
region2='pass_wcr_mjjLow200_u_Nominal'
region3='pass_sr_mjjLow200_nn_Nominal'
ZNF=GetNF(f2,region1,lowbin,highbin, isZ=True)
WNF=GetNF(f2,region2,lowbin,highbin, isZ=False)
print region1,ZNF
print region2,WNF
mjNF1_HTlow=GetNF(f2,region3,lowbin,highbin, True, ZNF,WNF, True)
print region3,mjNF1_HTlow

region1='pass_zcr_LowMETQCDSRFJVT_uu_Nominal'
region2='pass_wcr_LowMETQCDSRFJVT_u_Nominal'
region3='pass_sr_LowMETQCDSRFJVT_nn_Nominal'
ZNF=GetNF(f2,region1,lowbin,highbin, isZ=True)
WNF=GetNF(f2,region2,lowbin,highbin, isZ=False)
print region1,ZNF
print region2,WNF
mjnf2_HTlow=GetNF(f2,region3,lowbin,highbin, True, ZNF,WNF, True)
print region3,mjnf2_HTlow

print 'Avg: ',(mjNF1_HTlow+mjnf2_HTlow)/2.0
print ''

print 'High dphi'
lowbin=11
highbin=50
region1='pass_zcr_mjjLow200_uu_Nominal'
region2='pass_wcr_mjjLow200_u_Nominal'
region3='pass_sr_mjjLow200_nn_Nominal'
ZNF=GetNF(f2,region1,lowbin,highbin, isZ=True)
WNF=GetNF(f2,region2,lowbin,highbin, isZ=False)
print region1,ZNF
print region2,WNF
mjNF1_HThigh=GetNF(f2,region3,lowbin,highbin, True, ZNF,WNF, True)
print region3,mjNF1_HThigh

region1='pass_zcr_LowMETQCDSRFJVT_uu_Nominal'
region2='pass_wcr_LowMETQCDSRFJVT_u_Nominal'
region3='pass_sr_LowMETQCDSRFJVT_nn_Nominal'
ZNF=GetNF(f2,region1,lowbin,highbin, isZ=True)
WNF=GetNF(f2,region2,lowbin,highbin, isZ=False)
print region1,ZNF
print region2,WNF
mjnf2_HThigh=GetNF(f2,region3,lowbin,highbin, True, ZNF,WNF, True)
print region3,mjnf2_HThigh

print 'Avg: ',(mjNF1_HThigh+mjnf2_HThigh)/2.0


print ''
print 'Totals:'
print ''

avg_lowdphi=sum([mjNF1_BDTlow,mjnf2_BDTlow,mjNF1_HTlow,mjnf2_HTlow])/4.0
sys_lowdphi=(max([mjNF1_BDTlow,mjnf2_BDTlow,mjNF1_HTlow,mjnf2_HTlow]) - min([mjNF1_BDTlow,mjnf2_BDTlow,mjNF1_HTlow,mjnf2_HTlow]))/2.0
avg_highdphi=sum([mjNF1_BDThigh,mjnf2_BDThigh,mjNF1_HThigh,mjnf2_HThigh])/4.0
sys_highdphi=(max([mjNF1_BDThigh,mjnf2_BDThigh,mjNF1_HThigh,mjnf2_HThigh]) - min([mjNF1_BDThigh,mjnf2_BDThigh,mjNF1_HThigh,mjnf2_HThigh]))/2.0
print 'Avg Low Dphi: ',avg_lowdphi
print 'DIFFLOW/2: ',sys_lowdphi
print 'Avg High Dphi: ',avg_highdphi
print 'DIFFhigh/2: ',sys_highdphi

print ''
print 'year: ',year
print 'Low dphi: %0.3f +/- %0.3f' %(avg_lowdphi,sys_lowdphi)
print 'High dphi: %0.3f +/- %0.3f' %(avg_highdphi,sys_highdphi)
