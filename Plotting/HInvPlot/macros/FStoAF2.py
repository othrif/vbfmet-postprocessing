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

def DrawSF(can,trig,lep, mvar, fname,year=2018):

    deff[0].SetLineColor(1)
    deff[0].SetMarkerColor(1)
    zeff[0].SetLineColor(3)
    zeff[0].SetMarkerColor(3)
    weff[0].SetLineColor(2)
    weff[0].SetMarkerColor(2)
    bkgeff[0].SetLineColor(4)
    bkgeff[0].SetMarkerColor(4)

    trig_err = DrawError(trig, bkgeff[0]);
    
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
    can.WaitPrimitive()
    #raw_input('waiting...')
    can.SaveAs(den_path+'_Znn.pdf')

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
    
    can.Update()
    can.WaitPrimitive()
    f.Close()
    return [SFZ,SFW,SFBkg,deff[0],weff[0],zeff[0],bkgeff[0],Wfunc,Zfunc,bkgfunc,trig_err]

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
        p = ROOT.TLatex(x+0.14, y, ' Internal') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.065)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.1f fb^{-1}' %(139e3/1.0e3))
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
        
def DrawList(can,plts,names,plt_name,ytitle='Trigger Eff.',trig='xe110',input_err=None):
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
            if input_err:
                input_err.SetLineColor(ROOT.kMagenta)
                input_err.SetMarkerColor(ROOT.kMagenta)
                input_err.SetFillColor(ROOT.kMagenta)
                input_err.SetFillStyle(3003)
                input_err.Draw('same e5')
                p.Draw('same')                
        else:
            p.Draw('same')
        leg.AddEntry(p,names[color-1])
        color+=1
        p.GetYaxis().SetRangeUser(0.6,1.2)
    if input_err:
        leg.AddEntry(input_err,'Fit+Err')
    leg.Draw()
    texts = getATLASLabels(can, 0.2, 0.88,trig)
    for t in texts:
        t.Draw()
    can.Update()
    can.SaveAs(plt_name+'_Znn.pdf')

###########################################################################
# Main function for command line execuation
#
if __name__ == "__main__":

    Style()
    fout = ROOT.TFile.Open('myplt_W.root','RECREATE')
    can = ROOT.TCanvas('stack', 'stack', 800, 500)

    sampleName='VBFH300'
    #tpye = 'Wen'
    #sampleName='Z_EWK'
    tpye = 'Znn'
    fIncl = ROOT.TFile.Open('/tmp/'+sampleName+'Nominal313137.root')
    fVBFFilt = ROOT.TFile.Open('/tmp/'+sampleName+'Nominal313137FS.root')    
    #fIncl = ROOT.TFile.Open('/tmp/'+sampleName+'All.root')
    #fVBFFilt = ROOT.TFile.Open('/tmp/'+sampleName+'PowAll.root')    
    treeName1 = sampleName+'Nominal'
    treeNamePow = sampleName+'Nominal'
    plt=None
    vbfplt=None
    implt=None
    #cuts = '*(jj_mass>1.0e6 && jj_dphi<1.8 && jj_deta>3.8 && met_cst_jet>120.0e3 && met_tst_nolep_et>150.0e3 && jet_pt[0]>80.0e3 && jet_pt[1]>50e3 && n_jet<5 && met_tst_et<20.0e3)'
    #cuts = '*(jj_mass>1.0e6 && jj_dphi<1.8 && jj_deta>3.8 && met_cst_jet>120.0e3 && met_tst_et>150.0e3 && jet_pt[0]>80.0e3 && jet_pt[1]>50e3 && n_jet<5 )'    
    cuts = '*(jj_mass>0.2e6 && met_tst_nolep_et>150e3 && jj_mass>250e3)'
    cuts = '*(jj_mass>0.2e6 && met_tst_nolep_et>100e3 && jj_mass>250e3)'
    #cuts = '*(jj_mass>0.2e6 && met_truth_et>150e3)'
    runCutH7='*(1)' #Wenu 363237, zee=363234, znn=363233
    runCutSh='*(1)' #Wenu 308096, zee=308092, znn=308095
    if tpye=='Zee':
        runCutH7='*(1)' #Wenu 363237, zee=363234, znn=363233
        runCutSh='*(1)' #Wenu 308096, zee=308092, znn=308095
    if tpye=='Znn':
        runCutH7='*(1)' #Wenu 363237, zee=363234, znn=363233
        runCutSh='*(1)' #Wenu 308096, zee=308092, znn=308095                
    pvar='jj_mass/1.0e3'
    xaxis='m_{jj} [GeV]'
    pvar='jet_pt[0]/1.0e3'
    xaxis='Lead Jet p_{T} [GeV]'    
    pvar='jet_pt[1]/1.0e3'
    xaxis='subLead Jet p_{T} [GeV]'
    pvar='jet_pt[2]/1.0e3'
    xaxis='3rd Jet p_{T} [GeV]'
    #pvar='jet_eta[0]'
    #xaxis='Lead Jet #eta'    
    #pvar='jet_eta[1]'
    #xaxis='subLead Jet #eta'    
    pvar='jet_eta[2]'
    xaxis='3rd Jet #eta'    
    #pvar='truth_jj_dphi'
    #xaxis='Truth #Delta#phi_{jj}'
    #pvar='jj_dphi'
    #xaxis='#Delta#phi_{jj}'
    #pvar='met_truth_et/1.0e3'
    #xaxis='Truth MET [GeV]'    
    #pvar='met_tst_nolep_et/1.0e3'
    #xaxis='MET(nolep) [GeV]'    
    #pvar='n_jet'
    #xaxis='n_{jet}'
    #pvar='n_jet_truth'
    #xaxis='Truth n_{jet}'        
    #pvar='sqrt((truth_mu_pt[0]*sin(truth_mu_phi[0])+truth_mu_pt[1]*sin(truth_mu_phi[1]))*(truth_mu_pt[0]*sin(truth_mu_phi[0])+truth_mu_pt[1]*sin(truth_mu_phi[1])) + (truth_mu_pt[0]*cos(truth_mu_phi[0])+truth_mu_pt[1]*cos(truth_mu_phi[1]))*(truth_mu_pt[0]*cos(truth_mu_phi[0])+truth_mu_pt[1]*cos(truth_mu_phi[1])) )' 
    #pvar='truth_jet_phi[0]-truth_jet_phi[1]'
    #xaxis='Truth Z p_{T} [GeV]'
    tIncl = fIncl.Get(treeName1)
    n1 = 'Ipjj_mass'
    if pvar.count('jj_mass'):
        plt = ROOT.TH1F(n1,n1,20,0.0,5000.0)
    elif pvar.count('jj_dphi'):
        plt = ROOT.TH1F(n1,n1,30,0.0,3.0)
    elif pvar=='truth_jet_phi[0]-truth_jet_phi[1]':
        plt = ROOT.TH1F(n1,n1,50,-7.0,7.0)
    elif pvar.count('n_jet'):
        plt = ROOT.TH1F(n1,n1,10,-0.5,9.5)
    elif pvar.count('_eta'):
        plt = ROOT.TH1F(n1,n1,30,-4.5,4.5)
    else:
        plt = ROOT.TH1F(n1,n1,50,0.0,500.0)
    plt.GetYaxis().SetTitle('Events')
    plt.GetXaxis().SetTitle(xaxis)
    print tIncl
    tIncl.Draw(pvar+' >>'+n1,'w*36000.0'+cuts+runCutSh)
    plt.SetDirectory(fout)
    plt.SetMarkerSize(0.6)
    plt.Write()

    tVBFFilt = fVBFFilt.Get(treeNamePow)
    n2='vbfpjj_mass'
    if pvar.count('jj_mass'):
        vbfplt = ROOT.TH1F(n2,n2,20,0.0,5000.0)
    elif pvar=='truth_jet_phi[0]-truth_jet_phi[1]':
        vbfplt = ROOT.TH1F(n2,n2,50,-7.0,7.0)
    elif pvar.count('jj_dphi'):
        vbfplt = ROOT.TH1F(n2,n2,30,0.0,3.0)
    elif pvar=='truth_jet_phi[0]-truth_jet_phi[1]':
        vbfplt = ROOT.TH1F(n2,n2,50,-7.0,7.0)
    elif pvar.count('n_jet'):
        vbfplt = ROOT.TH1F(n2,n2,10,-0.5,9.5)
    elif pvar.count('_eta'):
        vbfplt = ROOT.TH1F(n2,n2,30,-4.5,4.5)        
    else:
        vbfplt = ROOT.TH1F(n2,n2,50,0.0,500.0)
    vbfplt.GetYaxis().SetTitle('Events')
    vbfplt.GetXaxis().SetTitle(xaxis)
    tVBFFilt.Draw(pvar+' >>'+n2,'w*36000.0'+cuts+runCutH7)
    vbfplt.SetLineColor(2)
    vbfplt.SetMarkerColor(2)
    vbfplt.SetMarkerSize(0.6)
    vbfplt.SetDirectory(fout)
    vbfplt.Write()

    #imMERGETree = fInclForMerge.Get(treeName)
    #n3='inclmergedtruth_jj_mass'
    #if pvar.count('jj_mass'): 
    #    implt = ROOT.TH1F(n3,n3,100,0.0,5000.0)
    #elif pvar=='truth_jet_phi[0]-truth_jet_phi[1]':
    #    implt = ROOT.TH1F(n3,n3,50,-7.0,7.0)           
    #else:
    #    implt = ROOT.TH1F(n3,n3,50,0.0,500.0)
    #implt.GetYaxis().SetTitle('Events')
    #implt.GetXaxis().SetTitle(xaxis)
    #imMERGETree.Draw(pvar+'/1.0e3 >>'+n3,'w*36000.0'+cuts)
    #implt.SetLineColor(3)
    #implt.SetMarkerColor(3)
    #implt.SetMarkerSize(0.6)
    #implt.SetDirectory(fout)
    #implt.Write()

    # Now Draw

    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    #pad1.SetGridx();         # Vertical grid
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad
    
    plt.Draw()
    #vbfplt.Scale(1.10)
    vbfplt.Draw('same')
    #implt.Draw('same')

    #sumed = vbfplt.Clone()
    #sumed.Add(implt)
    #sumed.SetLineColor(4)
    #sumed.SetMarkerColor(4)    
    #sumed.Draw('same')

    #e=ROOT.Double(0.0)
    #tot=sumed.IntegralAndError(0,10001,e)
    #print 'Merged: ',tot,'+/-',e
    #tot=plt.IntegralAndError(0,10001,e)
    #print 'Incl: ',tot,'+/-',e
    #tot=vbfplt.IntegralAndError(0,10001,e)
    #print 'Filtered only: ',tot,'+/-',e
    #tot=implt.IntegralAndError(0,10001,e)
    #print 'Incl to be merged: ',tot,'+/-',e        
    
    texts = getATLASLabels(can, 0.2, 0.88,'')
    for t in texts:
        t.Draw()

    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);
    leg.AddEntry(plt,'AF2 VBFH300')
    leg.AddEntry(vbfplt,'FullSim')
    #leg.AddEntry(implt,'Incl for Merging')
    #leg.AddEntry(sumed,'Merged')
    leg.Draw()

    can.cd();          # Go back to the main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.03, 1, 0.3);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.3);
    pad2.SetGridy(); # vertical grid
    pad2.Draw();
    pad2.cd();       # pad2 becomes the current pad

    hratio = vbfplt.Clone()
    hratio.Divide(plt)
    hratio.GetYaxis().SetTitle('FS/AF2')
    hratio.GetYaxis().SetRangeUser(0.5,1.5)       
    hratio.GetYaxis().SetNdivisions(505);
    hratio.GetYaxis().SetTitleSize(20);
    hratio.GetYaxis().SetTitleFont(43);
    hratio.GetYaxis().SetTitleOffset(1.55);
    hratio.GetYaxis().SetLabelFont(43); 
    hratio.GetYaxis().SetLabelSize(15);
    hratio.GetXaxis().SetTitleSize(20);
    hratio.GetXaxis().SetTitleFont(43);
    hratio.GetXaxis().SetTitleOffset(3.);
    hratio.GetXaxis().SetLabelFont(43); # Absolute font size in pixel (precision 3)
    hratio.GetXaxis().SetLabelSize(15);
    hratio.Draw()
    hratio.Fit('pol1')
    can.Update()
    can.WaitPrimitive()
    if pvar=='jet_pt[0]/1.0e3':
        pvar='j0pt'
    if pvar=='jet_pt[1]/1.0e3':
        pvar='j1pt'
    if pvar=='jet_pt[2]/1.0e3':
        pvar='j2pt'
    if pvar=='jet_eta[0]':
        pvar='j0eta'
    if pvar=='jet_eta[1]':
        pvar='j1eta'
    if pvar=='jet_eta[2]':
        pvar='j2eta'
    pvar_out=pvar
    if len(pvar.split('/'))>1:
        pvar_out=pvar.split('/')[0]
    can.SaveAs(sampleName+'_'+tpye+'_'+pvar_out+'.pdf')
