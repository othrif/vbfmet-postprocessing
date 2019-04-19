import ROOT
import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy
import os,sys

#-----------------------------------------
def Style():
    atlas_style_path='/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/'
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasUtils.C'))
    ROOT.SetAtlasStyle()
    
class function_turnon:
    def __call__(self, x, parameters):
        #0.5*(1+TMath::Erf((150-p0)/(TMath::Sqrt(2)*p1)))
        p0 = parameters[0] # shape
        p1 = parameters[1] # location of minimum
        x = x[0]
        y = 0.5*(1+ROOT.TMath.Erf((150-p0)/(ROOT.TMath.Sqrt(2)*p1)))
        return y
    
def myfunc(x, p):
    #return p[0]*np.exp(-(x/p[1])**2) + p[1]*np.exp(-(x/p[2])**2)
    return 0.5*(1+ROOT.TMath.Erf((x-p[0])/(ROOT.TMath.Sqrt(2)*p[1])))

def GetHists(f,cut_path, zcut_path, mvar):
    dpath    = cut_path+'/plotEvent_data/'+mvar
    wQCDpath = cut_path+'/plotEvent_wqcd/'+mvar
    wEWKpath = cut_path+'/plotEvent_wewk/'+mvar
    zQCDpath = zcut_path+'/plotEvent_zqcd/'+mvar
    zEWKpath = zcut_path+'/plotEvent_zewk/'+mvar

    zBkgEWKpath = cut_path+'/plotEvent_zewk/'+mvar
    zBkgQCDpath = cut_path+'/plotEvent_zqcd/'+mvar
    topBkgpath = cut_path+'/plotEvent_tall/'+mvar
    
    dplot    = f.Get(dpath).Clone()
    wQCDplot = f.Get(wQCDpath).Clone()
    wEWKplot = f.Get(wEWKpath).Clone()
    zBkgEWKplot = f.Get(zBkgEWKpath).Clone()
    zBkgQCDplot = f.Get(zBkgQCDpath).Clone()
    topBkgplot = f.Get(topBkgpath).Clone()

    bkgTot = wQCDplot.Clone()
    bkgTot.Add(wEWKplot)
    bkgTot.Add(zBkgEWKplot)
    bkgTot.Add(zBkgQCDplot)
    bkgTot.Add(topBkgplot)
    
    zQCDplot = f.Get(zQCDpath).Clone()
    zEWKplot = f.Get(zEWKpath).Clone()

    rebin=2
    plts = [dplot,wQCDplot,wEWKplot,zQCDplot,zEWKplot,bkgTot]
    if not mvar.count('nolep') or True:
        for p in plts:
            p.Rebin(rebin)
    
    return dplot,wQCDplot,wEWKplot,zQCDplot,zEWKplot,bkgTot

def DoFit(name, hist):
    ROOT.gROOT.LoadMacro("fit.C");
    func=ROOT.TF1("func", ROOT.fitf, 120.0,300.0, 2)
    func.SetParameters(110.0,30.0)
    func.SetParNames("p0", "p1")
    func.SetParLimits(0,   10.0,   200.0)
    func.SetParLimits(1, 0.0,  100.0)
    myfit = hist.Fit(func)
    func.SetLineColor(2)
    print name,func.GetParameter(0),func.GetParameter(1)
    func.SetName(name)
    return func

def DrawSF(can,trig,lep, mvar, fname):

    if lep=='u':
        #met_tenacious_tst_et
        mvar = mvar.replace('_tst_et','_tst_nolep_et')
    
    f = ROOT.TFile.Open(fname+'.root') 
    den_path = 'pass_metsf_metsf'+trig+'_'+lep+'_Nominal'
    num_path = 'pass_metsf_metsftrig'+trig+'J400_'+lep+'_Nominal'    
    zden_path = 'pass_metsf_metsf'+trig+'_nn_Nominal'
    znum_path = 'pass_metsf_metsftrig'+trig+'J400_nn_Nominal'    

    dnum,wQCDnum,wEWKnum,zQCDnum,zEWKnum,bkgNum = GetHists(f,num_path, znum_path, mvar)
    dden,wQCDden,wEWKden,zQCDden,zEWKden,bkgDen = GetHists(f,den_path, zden_path, mvar)

    deff = config.ComputeEff([dnum],[dden])
    wQCDeff = config.ComputeEff([wQCDnum],[wQCDden])
    wEWKeff = config.ComputeEff([wEWKnum],[wEWKden])
    #zQCDeff = config.ComputeEff([zQCDnum],[zQCDden])
    #zEWKeff = config.ComputeEff([zEWKnum],[zEWKden])
    bkgeff = config.ComputeEff([bkgNum],[bkgDen])

    wnum = wQCDnum.Clone(); wnum.Add(wEWKnum)
    wden = wQCDden.Clone(); wden.Add(wEWKden)

    znum = zQCDnum.Clone(); znum.Add(zEWKnum)
    zden = zQCDden.Clone(); zden.Add(zEWKden)
    print 'Integral: ',zden_path,znum.Integral(0,1001),zden.Integral(0,1001)
    weff = config.ComputeEff([wnum],[wden])
    zeff = config.ComputeEff([znum],[zden])    
    
    deff[0].SetLineColor(1)
    deff[0].SetMarkerColor(1)
    zeff[0].SetLineColor(3)
    zeff[0].SetMarkerColor(3)
    weff[0].SetLineColor(2)
    weff[0].SetMarkerColor(2)
    bkgeff[0].SetLineColor(4)
    bkgeff[0].SetMarkerColor(4)

    can.Clear()
    can.Draw()
    can.cd()
    deff[0].GetXaxis().SetRangeUser(100.0,300.0)
    deff[0].GetYaxis().SetRangeUser(0.7,1.15)
    deff[0].GetXaxis().SetTitle('Loose MET [GeV]')
    if mvar.count('tenacious'):
        deff[0].GetXaxis().SetTitle('Tenacious MET [GeV]')
        
    deff[0].GetYaxis().SetTitle('Trigger Eff.')    
    deff[0].Draw()
    weff[0].Draw('same')
    zeff[0].Draw('same')
    bkgeff[0].Draw('same')
    deff[0].SetDirectory(0)
    weff[0].SetDirectory(0)
    zeff[0].SetDirectory(0)
    bkgeff[0].SetDirectory(0)
    
    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);    
    leg.AddEntry(deff[0],'Data')
    leg.AddEntry(zeff[0],'Z')         
    leg.AddEntry(weff[0],'W')
    leg.AddEntry(bkgeff[0],'W+bkg')
    
    leg.Draw()
    can.Update()
    #can.WaitPrimitive()
    #raw_input('waiting...')
    can.SaveAs(den_path+'.pdf')

    SFW = deff[0].Clone()
    SFZ = deff[0].Clone()
    SFBkg = deff[0].Clone()
    SFW.SetDirectory(0)
    SFZ.SetDirectory(0)
    SFBkg.SetDirectory(0)
    
    SFW.Divide(weff[0])
    SFZ.Divide(zeff[0])
    SFBkg.Divide(bkgeff[0])
    SFW.GetXaxis().SetRangeUser(100.0,300.0)
    SFW.GetYaxis().SetRangeUser(0.7,1.15)    
    SFW.GetXaxis().SetTitle('Loose MET [GeV]')
    if mvar.count('tenacious'):
        SFW.GetXaxis().SetTitle('Tenacious MET [GeV]')    
    SFW.GetYaxis().SetTitle('Trigger SF')
    SFW.SetLineColor(1)
    SFW.SetMarkerColor(1)
    SFZ.SetLineColor(2)
    SFZ.SetMarkerColor(2)    
    SFBkg.SetLineColor(3)
    SFBkg.SetMarkerColor(3)
    SFW.Draw()
    SFZ.Draw('same')
    SFBkg.Draw('same')
    leg.Clear()
    leg.AddEntry(SFZ,'Z')
    leg.AddEntry(SFW,'W')
    leg.AddEntry(SFBkg,'W+bkg')
    leg.Draw()
    can.Update()
    #can.WaitPrimitive()
    #raw_input('waiting...')
    can.SaveAs(fname+'_'+den_path+'_SF.pdf')
    print 'Wfunc'
    Wfunc=DoFit('WSFFit'+fname+'_'+den_path,SFW)
    print 'Zfunc'    
    Zfunc=DoFit('ZSFFit'+fname+'_'+den_path,SFZ)
    print 'bkgfunc'    
    bkgfunc=DoFit('bkgSFFit'+fname+'_'+den_path,SFBkg)
    
    can.Update()
    #can.WaitPrimitive()
    f.Close()
    return [SFZ,SFW,SFBkg,deff[0],weff[0],zeff[0],bkgeff[0],Wfunc,Zfunc,bkgfunc]

def getATLASLabels(pad, x, y, text=None, selkey=None):
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

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.1f fb^{-1}' %(36.1e3/1.0e3))
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
    return labs
        
def DrawList(can,plts,names,plt_name,ytitle='Trigger Eff.',trig='xe110'):
    print plts
    can.Clear();
    color=1
    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);    
    
    plts[0].GetXaxis().SetTitle('Loose MET [GeV]')
    #if mvar.count('tenacious'):
    plts[0].GetXaxis().SetTitle('Tenacious MET [GeV]')
    #plts[0].GetXaxis().SetRangeUser(0.6,1.2)
    plts[0].GetYaxis().SetTitle(ytitle)
    for p in plts:
        p.SetLineColor(color)
        p.SetMarkerColor(color)
        if color==1:
            p.Draw()
        else:
            p.Draw('same')
        leg.AddEntry(p,names[color-1])
        color+=1
        p.GetYaxis().SetRangeUser(0.6,1.2)

    leg.Draw()
    texts = getATLASLabels(can, 0.2, 0.88,trig)
    for t in texts:
        t.Draw()
    can.Update()
    can.SaveAs(plt_name+'.pdf')

###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":

    Style()
    can = ROOT.TCanvas('stack', 'stack', 500, 500)
    #f = ROOT.TFile.Open('v26metsf_v3.root')
    mvar = 'met_tst_et'
    fname='v26metsf_v5_tenac_njet2'
    fname='v26metsf_v8_tenac_nj3'
    #fname='v26metsf_v8_tenac_nj3_detjj25'
    #fname='v26metsf_v8_tenac_nj3'
    #f = ROOT.TFile.Open('v26metsf_v4_tenac.root')
    #f = ROOT.TFile.Open('v26metsf_v7_tenac_fjvt.root')
    #f = ROOT.TFile.Open('v26metsf_v7_tenac_fjvtCST120.root')
    #f = ROOT.TFile.Open('v26metsf_v6_tenac_detajj25.root')
    #f = ROOT.TFile.Open('v26metsf_v6_tenac_detajj25_njet2.root')      
    mvar = 'met_tenacious_tst_et'
    #mvar = 'met_cst_jet'
    trig='xe90'
    lep='u'
    fname='v26metsf_v8_tenac_detjj25'
    #fname='v26metsf_v8_tenac_detjj25_CST120'
    xe90_u_detajj25 = DrawSF(can,trig,lep, mvar, fname)
    trig='xe70'    
    xe70_u_detajj25 = DrawSF(can,trig,lep, mvar, fname)

    
    trig='xe110'
    mvar = 'met_tst_et'
    #fname='v26metsf_v8_tenac_detjj25_CST120'
    fname='v26metsf_v8_tenac_detjj25_loose'
    xe110_u_detajj25_metLoose = DrawSF(can,trig,lep, mvar, fname)
    fname='v26metsf_v8_tenac_detjj25_CST120'
    xe110_u_cst120_metLoose = DrawSF(can,trig,lep, mvar, fname)
    
    #[SFZ,SFW,SFBkg,deff[0],weff[0],zeff[0],bkgeff[0],Wfunc,Zfunc,bkgfunc]
    lep='e' 
    mvar = 'met_tenacious_tst_et'   
    xe110_e_nj3 = DrawSF(can,trig,lep, mvar, fname)
    lep='u'
    xe110_u_nj3 = DrawSF(can,trig,lep, mvar, fname)
    lep='e'
    fname='v26metsf_v4_tenac'
    xe110_e_tenac = DrawSF(can,trig,lep, mvar, fname)
    lep='u'
    xe110_u_tenac = DrawSF(can,trig,lep, mvar, fname)
    #fname='v26metsf_v6_tenac_detajj25'
    fname='v26metsf_v8_tenac_detjj25'
    lep='e'    
    xe110_e_detajj25 = DrawSF(can,trig,lep, mvar, fname)
    lep='u'
    #fname='v26metsf_v8_tenac_detjj25_CST120'
    print 'xe110_u_detajj25'
    xe110_u_detajj25 = DrawSF(can,trig,lep, mvar, fname)

    fname='v26metsf_v7_tenac_fjvt'
    xe110_u_fjvt = DrawSF(can,trig,lep, mvar, fname)
    #fname='v26metsf_v7_tenac_fjvtCST120'
    fname='v26metsf_v8_tenac_detjj25_CST120'
    print fname
    xe110_u_fjvtCST120 = DrawSF(can,trig,lep, mvar, fname)
    #fname='v26metsf_v7_tenac_fjvtCST120'
    fname='v26metsf_v8_tenac_detjj25_CST120'
    lep='e'
    xe110_e_fjvtCST120 = DrawSF(can,trig,lep, mvar, fname)
    #fname='v26metsf_v7_tenac_fjvt'
    fname='v26metsf_v7_tenac_fjvt'
    xe110_e_fjvt = DrawSF(can,trig,lep, mvar, fname)   
    #print xe110_e_nj3
    DrawList(can,[xe110_e_nj3[0],xe110_e_nj3[2]],['Z','W+bkg'],trig+'test',trig=trig)
    DrawList(can,[xe110_e_tenac[2],xe110_e_detajj25[2]],['e','e LooserCuts'],trig+'e_default_vs_detajj25',trig=trig)
    DrawList(can,[xe110_u_tenac[2],xe110_u_detajj25[2]],['#mu','#mu LooserCuts'],trig+'u_default_vs_detajj25',trig=trig)

    DrawList(can,[xe110_u_nj3[2],xe110_e_tenac[2],xe110_u_tenac[2]],['#mu+3j','e+2j','#mu+2j'],trig+'njet_mu3j_vs_e2j_SF',ytitle='Trigger SF',trig=trig)
    DrawList(can,[xe110_u_nj3[6],xe110_e_tenac[6],xe110_u_tenac[6]],['#mu+3j','e+2j','#mu+2j'],trig+'njet_mu3j_vs_e2j_eff',trig=trig)        

    DrawList(can,[xe110_u_tenac[2],xe110_u_detajj25[2],xe110_u_fjvt[2],xe110_u_fjvtCST120[2],xe110_u_fjvtCST120[0],xe110_e_fjvtCST120[0]],['#mu','#mu LooserCuts','fjvt','fjvt+cst120','Z in SR','Z SR lep'],trig+'u_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    DrawList(can,[xe110_e_tenac[2],xe110_e_detajj25[2],xe110_e_fjvt[2],xe110_e_fjvtCST120[2],xe110_e_fjvtCST120[0]],['e','e LooserCuts','fjvt','fjvt+cst120','Z in SR'],trig+'e_default_vs_detajj25_vs_fjvt_cst120',trig=trig)   
    DrawList(can,[xe110_u_tenac[4],xe110_u_detajj25[4],xe110_u_fjvt[4],xe110_u_fjvtCST120[4],xe110_u_fjvtCST120[4],xe110_e_fjvtCST120[5]],['#mu','#mu LooserCuts','fjvt','fjvt+cst120','Z in SR','Z SR lep'],trig+'u_eff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    DrawList(can,[xe110_e_tenac[5],xe110_e_detajj25[5],xe110_e_fjvt[5],xe110_e_fjvtCST120[5]],['#nu#nu','#nu#nu |#Delta#eta_{jj}|>2.5','fjvt','fjvt+cst120','Z in SR'],trig+'nn_Zeff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)  
    DrawList(can,[xe110_e_tenac[4],xe110_e_detajj25[4],xe110_e_fjvt[4],xe110_e_fjvtCST120[4]],['e','e |#Delta#eta_{jj}|>2.5','fjvt','fjvt+cst120','Z in SR'],trig+'e_Zeff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    
    # Wbkg Eff
    DrawList(can,[xe110_e_tenac[6],xe110_e_detajj25[6],xe110_e_fjvt[6],xe110_e_fjvtCST120[6]],['e','e |#Delta#eta_{jj}|>2.5','fjvt cuts','fjvt cuts+cst120','Z in SR'],trig+'eBkg_Weff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    DrawList(can,[xe110_u_tenac[6],xe110_u_detajj25[6],xe110_u_fjvt[6],xe110_u_fjvtCST120[6]],['#mu','#mu |#Delta#eta_{jj}|>2.5','fjvt cuts','fjvt cuts+cst120','Z in SR'],trig+'uBkg_Weff_default_vs_detajj25_vs_fjvt_cst120',trig=trig)
    # trigger SF
    DrawList(can,[xe110_e_tenac[1],xe110_e_detajj25[1],xe110_e_fjvt[1],xe110_e_fjvtCST120[1]],['e','e |#Delta#eta_{jj}|>2.5','fjvt cuts','fjvt cuts+cst120','Z in SR'],trig+'eBkg_WSF_default_vs_detajj25_vs_fjvt_cst120',ytitle='Trigger SF',trig=trig)
    DrawList(can,[xe110_u_tenac[1],xe110_u_detajj25[1],xe110_u_fjvt[1],xe110_u_fjvtCST120[1]],['#mu','#mu |#Delta#eta_{jj}|>2.5','fjvt cuts','fjvt cuts+cst120','Z in SR'],trig+'uBkg_WSF_default_vs_detajj25_vs_fjvt_cst120',ytitle='Trigger SF',trig=trig)
    # lepton comparison
    #DrawList(can,[xe110_e_detajj25[6],xe110_u_detajj25[6],xe110_e_detajj25[5]],['e','#mu','#nu#nu',],'e_default_vs_detajj25_vs_fjvt_cst120')
    DrawList(can,[xe110_e_detajj25[6],xe110_u_detajj25[6],xe110_e_detajj25[5]],['e','#mu','#nu#nu'],trig+'e_vs_mu_vs_nn_eff',trig=trig)
    DrawList(can,[xe110_e_detajj25[2],xe110_u_detajj25[2]],['e','#mu','#nu#nu'],trig+'e_vs_mu_SF',ytitle='Trigger SF',trig=trig)


    DrawList(can,[xe110_u_detajj25[2],xe110_u_detajj25_metLoose[2]],['#mu Loose','#mu Tenacious'],trig+'Tenacious_vs_Loose_SF',ytitle='Trigger SF',trig=trig)
    DrawList(can,[xe110_u_detajj25[6],xe110_u_detajj25_metLoose[6]],['#mu Loose','#mu Tenacious'],trig+'Tenacious_vs_Loose_Eff',ytitle='Trigger Eff',trig=trig)        

    DrawList(can,[xe110_u_fjvtCST120[2],xe110_u_cst120_metLoose[2]],['#mu Loose','#mu Tenacious'],'Tenacious_vs_Loose_CST_SF',ytitle='Trigger SF',trig=trig)
    DrawList(can,[xe110_u_fjvtCST120[6],xe110_u_cst120_metLoose[6]],['#mu Loose','#mu Tenacious'],'Tenacious_vs_Loose_CST_Eff',ytitle='Trigger Eff',trig=trig) 

    # Compare triggers
    DrawList(can,[xe70_u_detajj25[2],xe90_u_detajj25[2],xe110_u_detajj25[2]],['#mu xe70','#mu xe90','#mu xe110'],'xeComparison_SF', ytitle='Trigger SF',trig='xe70,90,110')
    DrawList(can,[xe70_u_detajj25[6],xe90_u_detajj25[6],xe110_u_detajj25[6]],['#mu xe70','#mu xe90','#mu xe110'],'xeComparison_Eff',ytitle='Trigger Eff',trig='xe70,90,110')        
    
