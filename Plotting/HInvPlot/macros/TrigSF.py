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
    for p in plts:
        p.Rebin(rebin)
    
    return dplot,wQCDplot,wEWKplot,zQCDplot,zEWKplot,bkgTot

###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":

    Style()    
    #f = ROOT.TFile.Open('v26metsf_v3.root')
    mvar = 'met_tst_et'
    f = ROOT.TFile.Open('v26metsf_v4_tenac.root')
    mvar = 'met_tenacious_tst_et'
    trig='xe110'
    lep='u'
    den_path = 'pass_metsf_metsf'+trig+'_'+lep+'_Nominal'
    num_path = 'pass_metsf_metsftrig'+trig+'J400_'+lep+'_Nominal'    
    zden_path = 'pass_metsf_metsf'+trig+'_nn_Nominal'
    znum_path = 'pass_metsf_metsftrig'+trig+'J400_nn_Nominal'    

    dnum,wQCDnum,wEWKnum,zQCDnum,zEWKnum,bkgNum = GetHists(f,num_path, znum_path, mvar)
    dden,wQCDden,wEWKden,zQCDden,zEWKden,bkgDen = GetHists(f,den_path, zden_path, mvar)

    deff = config.ComputeEff([dnum],[dden])
    wQCDeff = config.ComputeEff([wQCDnum],[wQCDden])
    wEWKeff = config.ComputeEff([wEWKnum],[wEWKden])
    zQCDeff = config.ComputeEff([zQCDnum],[zQCDden])
    zEWKeff = config.ComputeEff([zEWKnum],[zEWKden])
    bkgeff = config.ComputeEff([bkgNum],[bkgDen])

    wnum = wQCDnum.Clone(); wnum.Add(wEWKnum)
    wden = wQCDden.Clone(); wden.Add(wEWKden)

    znum = zQCDnum.Clone(); znum.Add(zEWKnum)
    zden = zQCDden.Clone(); zden.Add(zEWKden)

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

    can = ROOT.TCanvas('stack', 'stack', 500, 500)
    can.Draw()
    can.cd()
    deff[0].GetXaxis().SetTitle('MET [GeV]')
    deff[0].GetYaxis().SetTitle('Trigger Eff.')    
    deff[0].Draw()
    weff[0].Draw('same')
    zeff[0].Draw('same')
    bkgeff[0].Draw('same')
    
    leg = ROOT.TLegend(0.51, 0.62, 0.93, 0.89)
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
    can.WaitPrimitive()
    raw_input('waiting...')
    can.SaveAs(den_path+'.pdf')

    SFW = deff[0].Clone()
    SFZ = deff[0].Clone()
    SFBkg = deff[0].Clone()
    SFW.Divide(weff[0])
    SFZ.Divide(zeff[0])
    SFBkg.Divide(bkgeff[0])
    SFW.GetXaxis().SetTitle('MET [GeV]')
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
    can.WaitPrimitive()
    raw_input('waiting...')
    can.SaveAs(den_path+'_SF.pdf')
