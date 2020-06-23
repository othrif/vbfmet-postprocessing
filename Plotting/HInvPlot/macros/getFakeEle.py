import ROOT
import os, sys,math
#-----------------------------------------
def Style():
    atlas_style_path='/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/'
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.SetAtlasStyle()
    
def getATLASLabels(pad, x, y, text=None, selkey=None, text2=None):
    l = ROOT.TLatex(x, y, 'ATLAS')
    l.SetNDC()
    l.SetTextFont(62)
    l.SetTextSize(0.07)
    l.SetTextAlign(11)
    l.SetTextColor(ROOT.kBlack)
    l.Draw()

    delx = 0.05*pad.GetWh()/(pad.GetWw())
    labs = [l]

    if True:
        p = ROOT.TLatex(x+0.22, y, ' Internal') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.065)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %s fb^{-1}' %(139))        
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.05)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]
        
    if text != None:

        c = ROOT.TLatex(x, y-0.1, text)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.05)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        labs += [c]
    if text2 != None:
        d = ROOT.TLatex(x, y-0.16, text2)
        d.SetNDC()
        d.SetTextFont(42)
        d.SetTextSize(0.05)
        d.SetTextAlign(12)
        d.SetTextColor(ROOT.kBlack)
        labs += [d]
    return labs

def GetHist(f,bkg,region1,lowbin,highbin,var='met_tst_et'):

    datah =0.0
    errh=ROOT.Double(0.0)
    errl=ROOT.Double(0.0)    
    datah=f.Get(region1+'/plotEvent_data/'+var).Clone()
    datah.GetYaxis().SetTitle('Data - non Fake-#it{e}')

    if var=='met_tst_et':
        datah.GetXaxis().SetTitle('MET [GeV]')
    if var=='mt':
        datah.GetXaxis().SetTitle('M_{T} [GeV]')
        datah.GetYaxis().SetTitle('Data - non Fake-#mu')
    if var.count('jj_mass'):
        datah.GetXaxis().SetTitle('M_{jj} [GeV]')
    
    for i in bkg:
        try:
            h1=f.Get(region1+'/plotEvent_'+i+'/'+var)
            datah.Add(h1,-1.0)
        except:
            print region1+'/plotEvent_'+i+'/'+var

    lowv = datah.IntegralAndError(lowbin,highbin,errl)
    higv = datah.IntegralAndError(highbin+1,10001,errh)
    upbinnum = datah.GetNbinsX()
    upbin = datah.GetBinContent(upbinnum+1)
    upbinerr = datah.GetBinError(upbinnum+1)
    upbin1 = datah.GetBinContent(upbinnum)
    upbinerr1 = datah.GetBinError(upbinnum)
    datah.SetBinContent(upbinnum+1,0.0)
    datah.SetBinError(upbinnum+1,0.0)
    datah.SetBinContent(upbinnum,upbin+upbin1)
    datah.SetBinError(upbinnum,math.sqrt(upbinerr**2+upbinerr1**2))

    if var.count('jj_mass') and False:
        upbinnum=upbinnum-1
        upbin = datah.GetBinContent(upbinnum+1)
        upbinerr = datah.GetBinError(upbinnum+1)
        upbin1 = datah.GetBinContent(upbinnum)
        upbinerr1 = datah.GetBinError(upbinnum)
        datah.SetBinContent(upbinnum+1,0.0)
        datah.SetBinError(upbinnum+1,0.0)
        datah.SetBinContent(upbinnum,upbin+upbin1)
        datah.SetBinError(upbinnum,math.sqrt(upbinerr**2+upbinerr1**2))
        upbinnum=upbinnum-1
        upbin = datah.GetBinContent(upbinnum+1)
        upbinerr = datah.GetBinError(upbinnum+1)
        upbin1 = datah.GetBinContent(upbinnum)
        upbinerr1 = datah.GetBinError(upbinnum)
        datah.SetBinContent(upbinnum+1,0.0)
        datah.SetBinError(upbinnum+1,0.0)
        datah.SetBinContent(upbinnum,upbin+upbin1)
        datah.SetBinError(upbinnum,math.sqrt(upbinerr**2+upbinerr1**2))
    ratio=1.0
    ratioOpp=1.0
    print 'Upper range:',datah.GetXaxis().GetBinUpEdge(highbin)
    if higv>0.0 and lowv>0.0:
        ratio=higv/lowv
        ratioErr = ratio*math.sqrt((errl/lowv)**2+(errh/higv)**2)
        ratioOpp=lowv/higv
        ratioOppErr = ratioOpp*math.sqrt((errl/lowv)**2+(errh/higv)**2)
        print 'Ratio: %0.3f +/- %0.3f' %(ratio,ratioErr)
        print 'RatioInv: %0.3f +/- %0.3f' %(ratioOpp,ratioOppErr)
        
    return datah

inputDir='PostConf/'
year=2019
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
    f=ROOT.TFile.Open(inputDir+'/v37ALLAnti_wdphimetgam.root')
    f2=ROOT.TFile.Open(inputDir+'/v37ALLAnti_nodphimetgam.root')

bkg=['zgam','wgam','wgamewk','zgamewk','tall','efakeph','jfakeph']


Style()
can = ROOT.TCanvas('stack', 'stack', 800, 500)
print ''
print 'Electron Fakes'
print ''
lowbin=0
highbin=8 # up to 80 GeV
#mvar='mt'
lep='e'
mvar='met_tst_et'
mvar='jj_mass_variableBinGam'
region1='pass_gamwcr_allmjj_'+lep+'_Nominal'
FakesTemplatewDPHI=GetHist(f, bkg,region1,lowbin,highbin,var=mvar)
FakesTemplatenoDPHI=GetHist(f2,bkg,region1,lowbin,highbin,var=mvar)

FakesTemplatewDPHI.SetLineColor(1)
FakesTemplatewDPHI.SetMarkerColor(1)
FakesTemplatenoDPHI.SetLineColor(2)
FakesTemplatenoDPHI.SetMarkerColor(2)
FakesTemplatenoDPHI.Draw()
FakesTemplatewDPHI.Draw('same')
leg = ROOT.TLegend(0.65, 0.5, 0.98, 0.8)
leg.SetBorderSize(0)
leg.SetFillStyle (0)
leg.SetTextFont(42);
leg.SetTextSize(0.04);  
leg.AddEntry(FakesTemplatewDPHI,'with #Delta#phi(MET,#gamma) cut')
leg.AddEntry(FakesTemplatenoDPHI,'no #Delta#phi(MET,#gamma) cut')
leg.Draw()

texts = getATLASLabels(can, 0.2, 0.88,'Electron Anti-ID')
if region1.count('_u_'):
    texts = getATLASLabels(can, 0.2, 0.88,'Muon Anti-ID')
for t in texts:
    t.Draw()
can.Update()
can.WaitPrimitive()

# add regions
region2='pass_gamwcr_antiELowMET_'+lep+'_Nominal'
LowMETFakesTemplatewDPHI=GetHist(f, bkg,region2,lowbin,highbin,var=mvar)
LowMETFakesTemplatenoDPHI=GetHist(f2,bkg,region2,lowbin,highbin,var=mvar)
region3='pass_gamwcr_antiEHighMET_'+lep+'_Nominal'
HighMETFakesTemplatewDPHI=GetHist(f, bkg,region3,lowbin,highbin,var=mvar)
HighMETFakesTemplatenoDPHI=GetHist(f2,bkg,region3,lowbin,highbin,var=mvar)


can.Clear()
HighMETFakesTemplatewDPHI.Divide(LowMETFakesTemplatewDPHI)
HighMETFakesTemplatenoDPHI.Divide(LowMETFakesTemplatenoDPHI)

HighMETFakesTemplatewDPHI.GetYaxis().SetTitle('Pass MET / Fail MET')
HighMETFakesTemplatewDPHI.SetLineColor(1)
HighMETFakesTemplatewDPHI.SetMarkerColor(1)
HighMETFakesTemplatenoDPHI.SetLineColor(2)
HighMETFakesTemplatenoDPHI.SetMarkerColor(2)
HighMETFakesTemplatewDPHI.Draw()
HighMETFakesTemplatenoDPHI.Draw('same')
for i in range(1,HighMETFakesTemplatewDPHI.GetNbinsX()+1):
    print 'Ratio wdphi %s: %0.3f +/- %0.3f ' %(HighMETFakesTemplatewDPHI.GetXaxis().GetBinLowEdge(i),HighMETFakesTemplatewDPHI.GetBinContent(i),HighMETFakesTemplatewDPHI.GetBinError(i))
for i in range(1,HighMETFakesTemplatenoDPHI.GetNbinsX()+1):
    print 'Ratio no dphi %s: %0.3f +/- %0.3f ' %(HighMETFakesTemplatenoDPHI.GetXaxis().GetBinLowEdge(i),HighMETFakesTemplatenoDPHI.GetBinContent(i),HighMETFakesTemplatenoDPHI.GetBinError(i))
leg.Draw()
for t in texts:
    t.Draw()
can.Update()
can.WaitPrimitive()
