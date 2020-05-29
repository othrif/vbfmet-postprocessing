import ROOT
import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy
import os,sys

#-----------------------------------------
def Style():
    atlas_style_path='../VBFAnalysis/python/Plotting/AtlasStyle/'
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

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.0f fb^{-1}' %(139e3/1.0e3))
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

    from optparse  import OptionParser
    p = OptionParser()

    p.add_option( '--ipath1',     type='string',      default='/tmp/363233.root',                 dest='ipath1',      help='Input path 1')
    p.add_option( '--ipath2',     type='string',      default='/tmp/308095.root',        dest='ipath2',      help='Input path 2')
    p.add_option( '--var',      type='string',      default='jj_mass',                 dest='var',       help='jj_mass,jet_pt2,njets,njets25,jj_dphi,jj_deta,bosonpt')

    (options, args) = p.parse_args()
    
    Style()
    fout = ROOT.TFile.Open('myplt_Znn.root','RECREATE')
    can = ROOT.TCanvas('stack', 'stack', 800, 500)

    sampleName='H7ZnnRatio'
    tpye = 'Sig'
    fVBFFilt = ROOT.TFile.Open('/tmp/308095.root')
    fIncl = ROOT.TFile.Open('/tmp/363233Znn.root')
    fZmm = ROOT.TFile.Open('/tmp/830007Zmm.root')
    #fZmmSh = ROOT.TFile.Open('/tmp/308093New.root')    
    fZmmSh = ROOT.TFile.Open('/tmp/3080923.root')    
    treeName1 = 'MiniNtuple'
    treeNamePow = 'MiniNtuple'
    plt=None
    vbfplt=None
    implt=None
    #cuts = '*(jj_mass>1.0e6 && jj_dphi<1.8 && jj_deta>3.8 && met_cst_jet>120.0e3 && met_tst_nolep_et>150.0e3 && jet_pt[0]>80.0e3 && jet_pt[1]>50e3 && n_jet<5 && met_tst_et<20.0e3)'
    #cuts = '*(jj_mass>1.0e6 && jj_dphi<1.8 && jj_deta>3.8 && met_cst_jet>120.0e3 && met_tst_et>150.0e3 && jet_pt[0]>80.0e3 && jet_pt[1]>50e3 && n_jet<5 )'    
    #cuts = '*( truth_jj_mass>200e3 && boson_pt[0]>150e3 && truth_jj_deta>3.0 && truth_jj_dphi<2.5 && jet_pt[1]>40e3)'
    #cuts = '*( truth_jj_mass>200e3 && boson_pt[0]>150e3 && truth_jj_deta>3.0 && truth_jj_dphi<2.5 && jet_pt[1]>40e3)'
    #cuts = '*( truth_jj_mass>100e3  && jet_pt[1]>30e3 && truth_jj_dphi<2.5 && boson_pt[0]>90e3)'
    cuts = '*( 1)'
    #cuts = '*( njets25>1 && truth_jj_mass>0.2e6)'
    cuts = '*(truth_jj_mass>0.5e6 && met_nolep_et>110e3 && njets25==2 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0 && truth_jj_deta>3.8 && zboson_m>66.0e3 && zboson_m<116.0e3)'
    #cuts = '*(truth_jj_mass>0.2e6 && jet_pt[1]>40e3 && jet_pt[0]>60e3  && truth_jj_deta>3.0 && zboson_m>82.0e3 && zboson_m<116.0e3)' # && zboson_m>66.0e3 && zboson_m<116.0e3
    h1n = fIncl.Get("NumberEvents")
    h2n = fVBFFilt.Get("NumberEvents")
    h3n = fZmm.Get("NumberEvents")
    h4n = fZmmSh.Get("NumberEvents")
    runCutH7='/%s*3.4831' %(h1n.GetBinContent(2))
    runCutSh='/%s*2.9385' %(h2n.GetBinContent(2))
    runCutZmm='/%s*0.62' %(h3n.GetBinContent(2))
    runCutZmmSh='/%s*0.63197' %(h4n.GetBinContent(2))
    
    pvar='truth_jj_mass/1.0e3'
    xaxis='Truth m_{jj} [GeV]'
    if options.var=="centrality":
        pvar='exp(-4.0/pow(truth_jj_deta,2)) * pow(jet_eta[2] - (jet_eta[0]+jet_eta[1])/2.0,2)'
        xaxis='Third jet centrality'
    elif options.var=="jet_pt2":
        pvar='jet_pt[2]/1.0e3'
        xaxis='Third Jet p_{T} [GeV]'
    elif options.var=="njets":        
        pvar='njets'
        xaxis='Truth N_{jets}'
    elif options.var=="njets25":        
        pvar='njets25'
        xaxis='Truth N_{jets,25}'
    elif options.var=="jj_dphi":  
        pvar='truth_jj_dphi'
        xaxis='Truth #Delta#phi_{jj}'
    elif options.var=="jj_deta": 
        pvar='truth_jj_deta'
        xaxis='Truth #Delta#eta_{jj}'
    #pvar='jet_phi[0]-jet_phi[1]'
    #xaxis='Truth #Delta#phi_{jj}'
    elif options.var=="bosonpt": 
        pvar='boson_pt[0]/1.0e3'
        xaxis='boson p_{T} [GeV]'
    elif options.var=="bosonm":
        pvar='boson_m[0]/1.0e3'
        xaxis='boson mass [GeV]'
    elif options.var=="zboson_m":
        pvar='zboson_m/1.0e3'
        xaxis='boson mass [GeV]'
    elif options.var=="zboson_eta":
        pvar='zboson_eta'
        xaxis='boson #eta'        
    elif options.var=="zboson_pt":
        pvar='zboson_pt/1.0e3'
        xaxis='boson p_{T} [GeV]'
    elif options.var=="met_et":
        pvar='met_et/1.0e3'
    elif options.var=="met_nolep_et":
        pvar='met_nolep_et/1.0e3'
        xaxis='Truth MET [GeV]'
    elif options.var=="met_nolep_et":
        pvar='met_nolep_et/1.0e3'
        xaxis='Truth MET (nonInt+Z-charged leptons) [GeV]'        
    #pvar='jj_dphi'
    #xaxis='#Delta#phi_{jj}'
    #pvar='met_truth_et/1.0e3'
    #xaxis='Truth MET [GeV]'    
    #pvar='met_tst_nolep_et/1.0e3'
    #xaxis='MET(nolep) [GeV]'    
    #pvar='sqrt((truth_mu_pt[0]*sin(truth_mu_phi[0])+truth_mu_pt[1]*sin(truth_mu_phi[1]))*(truth_mu_pt[0]*sin(truth_mu_phi[0])+truth_mu_pt[1]*sin(truth_mu_phi[1])) + (truth_mu_pt[0]*cos(truth_mu_phi[0])+truth_mu_pt[1]*cos(truth_mu_phi[1]))*(truth_mu_pt[0]*cos(truth_mu_phi[0])+truth_mu_pt[1]*cos(truth_mu_phi[1])) )' 
    #pvar='truth_jet_phi[0]-truth_jet_phi[1]'
    #xaxis='Truth Z p_{T} [GeV]'
    tIncl = fIncl.Get(treeName1)
    n1 = 'Iptruth_jj_mass'
    if pvar.count('jj_mass'):
        plt = ROOT.TH1F(n1,n1,10,0.0,5000.0)
    elif pvar.count('pow(truth_jj_deta,2)'):
        plt = ROOT.TH1F(n1,n1,25,0.0,5.0)
    elif pvar=='jet_phi[0]-jet_phi[1]' or pvar=='zboson_eta':
        plt = ROOT.TH1F(n1,n1,50,-7.0,7.0)
    elif pvar.count('njets'):
        plt = ROOT.TH1F(n1,n1,10,-0.5,9.5)
    elif pvar.count('jj_dphi') or pvar.count('truth_jet_phi[0]-truth_jet_phi[1]'):
        plt = ROOT.TH1F(n1,n1,10,0.0,3.0)
    elif pvar.count('jj_deta'):
        plt = ROOT.TH1F(n1,n1,30,0.0,10.0)
    elif pvar=='truth_jet_phi[0]-truth_jet_phi[1]':
        plt = ROOT.TH1F(n1,n1,50,-7.0,7.0)
    elif pvar=='jet_pt[2]/1.0e3':
        plt = ROOT.TH1F(n1,n1,50,0.0,500.0)
    else:
        plt = ROOT.TH1F(n1,n1,25,0.0,500.0)
    plt.GetYaxis().SetTitle('Arb. Normalisation')
    plt.GetXaxis().SetTitle(xaxis)
    print tIncl
    tIncl.Draw(pvar+' >>'+n1,'EventWeight'+cuts+runCutH7)
    plt.SetDirectory(fout)
    plt.SetMarkerSize(0.6)
    plt.Write()
    #cuts = '*(truth_jj_mass>0.2e6 && jet_pt[1]>40e3 && jet_pt[0]>60e3  && truth_jj_deta>3.0)'
    tVBFFilt = fVBFFilt.Get(treeNamePow)
    n2='vbfptruth_jj_mass'
    if pvar.count('jj_mass'):
        vbfplt = ROOT.TH1F(n2,n2,10,0.0,5000.0)
    elif pvar.count('pow(truth_jj_deta,2)'):
        vbfplt = ROOT.TH1F(n2,n2,25,0.0,5.0)        
    elif pvar=='jet_phi[0]-jet_phi[1]' or pvar=='zboson_eta':
        vbfplt = ROOT.TH1F(n2,n2,50,-7.0,7.0)
    elif pvar.count('njets'):
        vbfplt = ROOT.TH1F(n2,n2,10,-0.5,9.5)
    elif pvar.count('jj_dphi') or pvar.count('jet_phi[0]-jet_phi[1]'):
        vbfplt = ROOT.TH1F(n2,n2,10,0.0,3.0)
    elif pvar.count('jj_deta'):
        vbfplt = ROOT.TH1F(n2,n2,30,0.0,10.0)
    elif pvar=='truth_jet_phi[0]-truth_jet_phi[1]':
        vbfplt = ROOT.TH1F(n2,n2,50,-7.0,7.0)
    elif pvar=='jet_pt[2]/1.0e3':
        vbfplt = ROOT.TH1F(n2,n2,50,0.0,500.0)
    else:
        vbfplt = ROOT.TH1F(n2,n2,25,0.0,500.0)
    vbfplt.GetYaxis().SetTitle('Events')
    vbfplt.GetXaxis().SetTitle(xaxis)
    tVBFFilt.Draw(pvar+' >>'+n2,'EventWeight'+cuts+runCutSh)
    vbfplt.SetLineColor(2)
    vbfplt.SetMarkerColor(2)
    vbfplt.SetMarkerSize(0.6)
    vbfplt.SetDirectory(fout)
    vbfplt.Write()

    tZmm = fZmm.Get(treeNamePow)
    n3='zmmptruth_jj_mass'
    if pvar.count('jj_mass'):
        zmmplt = ROOT.TH1F(n3,n3,10,0.0,5000.0)
    elif pvar.count('pow(truth_jj_deta,2)'):
        zmmplt = ROOT.TH1F(n3,n3,25,0.0,5.0)        
    elif pvar=='jet_phi[0]-jet_phi[1]' or pvar=='zboson_eta':
        zmmplt = ROOT.TH1F(n3,n3,50,-7.0,7.0)
    elif pvar.count('njets'):
        zmmplt = ROOT.TH1F(n3,n3,10,-0.5,9.5)
    elif pvar.count('jj_dphi') or pvar.count('jet_phi[0]-jet_phi[1]'):
        zmmplt = ROOT.TH1F(n3,n3,10,0.0,3.0)
    elif pvar.count('jj_deta'):
        zmmplt = ROOT.TH1F(n3,n3,30,0.0,10.0)
    elif pvar=='truth_jet_phi[0]-truth_jet_phi[1]':
        zmmplt = ROOT.TH1F(n3,n3,50,-7.0,7.0)
    elif pvar=='jet_pt[2]/1.0e3':
        zmmplt = ROOT.TH1F(n3,n3,50,0.0,500.0)
    else:
        zmmplt = ROOT.TH1F(n3,n3,25,0.0,500.0)
    zmmplt.GetYaxis().SetTitle('Events')
    zmmplt.GetXaxis().SetTitle(xaxis)
    tZmm.Draw(pvar+' >>'+n3,'EventWeight'+cuts+runCutZmm)
    zmmplt.SetLineColor(3)
    zmmplt.SetMarkerColor(3)
    zmmplt.SetMarkerSize(0.6)
    zmmplt.SetDirectory(fout)
    zmmplt.Write()

    tZmmSh = fZmmSh.Get(treeNamePow)
    n4='zmmptruth_jj_mass'
    if pvar.count('jj_mass'):
        zmmshplt = ROOT.TH1F(n4,n4,10,0.0,5000.0)
    elif pvar.count('pow(truth_jj_deta,2)'):
        zmmshplt = ROOT.TH1F(n4,n4,25,0.0,5.0)        
    elif pvar=='jet_phi[0]-jet_phi[1]' or pvar=='zboson_eta':
        zmmshplt = ROOT.TH1F(n4,n4,50,-7.0,7.0)
    elif pvar.count('njets'):
        zmmshplt = ROOT.TH1F(n4,n4,10,-0.5,9.5)
    elif pvar.count('jj_dphi') or pvar.count('jet_phi[0]-jet_phi[1]'):
        zmmshplt = ROOT.TH1F(n4,n4,10,0.0,3.0)
    elif pvar.count('jj_deta'):
        zmmshplt = ROOT.TH1F(n4,n4,30,0.0,10.0)
    elif pvar=='truth_jet_phi[0]-truth_jet_phi[1]':
        zmmshplt = ROOT.TH1F(n4,n4,50,-7.0,7.0)
    elif pvar=='jet_pt[2]/1.0e3':
        zmmshplt = ROOT.TH1F(n4,n4,50,0.0,500.0)
    else:
        zmmshplt = ROOT.TH1F(n4,n4,25,0.0,500.0)
    zmmshplt.GetYaxis().SetTitle('Events')
    zmmshplt.GetXaxis().SetTitle(xaxis)
    tZmmSh.Draw(pvar+' >>'+n4,'EventWeight'+cuts+runCutZmmSh)
    zmmshplt.SetLineColor(4)
    zmmshplt.SetMarkerColor(4)
    zmmshplt.SetMarkerSize(0.6)
    zmmshplt.SetDirectory(fout)
    zmmshplt.Write()

    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    #pad1.SetGridx();         # Vertical grid
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad
    
    #plt.Draw()
    #vbfplt.Draw('same')
    #zmmplt.Draw('same')
    #zmmshplt.Draw('same')
    #plt.Draw('same')
    #implt.Draw('same')
    print 'Plt1: ',plt.Integral()
    print 'Plt2: ',vbfplt.Integral()
    print 'Plt3: ',zmmplt.Integral()
    print 'Plt4: ',zmmshplt.Integral()

    # Dividing
    plt.GetYaxis().SetRangeUser(0.1,10.0)
    if pvar.count('met'):
        plt.Rebin(2)
        zmmplt.Rebin(2)
        zmmshplt.Rebin(2)
        vbfplt.Rebin(2)
    plt.Divide(zmmplt)
    vbfplt.Divide(zmmshplt)
    
    plt.Draw()
    vbfplt.Draw('same')

    texts = getATLASLabels(can, 0.65, 0.88,'')
    for t in texts:
        t.Draw()

    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);
    leg.AddEntry(plt,'H7 Z#rightarrow#nu#nu/Z#rightarrow#mu#mu')
    leg.AddEntry(vbfplt,'Sherpa Z#rightarrow#nu#nu/Z#rightarrow#mu#mu')
    leg.Draw()

    can.cd();          # Go back to the main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.03, 1, 0.3);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.3);
    pad2.SetGridy(); # vertical grid
    pad2.Draw();
    pad2.cd();       # pad2 becomes the current pad

    hratio = vbfplt.Clone()
    
    hratio.GetYaxis().SetTitle('Sherpa/H7')
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
    hratio.Divide(plt)
    hratio.Draw()

    for i in range(1,hratio.GetNbinsX()+1):
        print hratio.GetBinContent(i)
    if pvar.count('jj_mass'):
        hratio.Fit('pol1',"","",500.0,5000.0)
    elif pvar.count('pow(truth_jj_deta,2)'):
        hratio.Fit('pol1',"","",0.0,5.0)        
    elif pvar.count('jj_dphi'):
        hratio.Fit('pol1',"","",0.3,3.2)
    elif pvar.count('jj_deta'):
        hratio.Fit('pol1',"","",2.5,6.5)
    elif pvar.count('boson_pt'):
        hratio.Fit('pol1',"","",90.0,500.0)
    elif pvar.count('boson_m'):
        hratio.Fit('pol1',"","",90.0,500.0)
    elif pvar.count('met'):
        hratio.Fit('pol1',"","",90.0,500.0)
    elif pvar.count('jet_pt'):
        hratio.Fit('pol1',"","",10.0,300.0)
    elif pvar.count('njets'):
        hratio.Fit('pol1',"","",0.0,9.0)
    can.Update()
    can.WaitPrimitive()
    pvar_out=pvar
    if len(pvar.split('/'))>1:
        pvar_out=pvar.split('/')[0]
    if pvar=='boson_pt[0]/1.0e3':
        pvar_out='boson_pt'
    if pvar=='zboson_pt/1.0e3':
        pvar_out='zboson_pt'
    if pvar=='zboson_m/1.0e3':
        pvar_out='zboson_m'
    if pvar=='boson_m[0]/1.0e3':
        pvar_out='boson_m'
    if pvar=='met_et/1.0e3':
        pvar_out='truthmet'
    if pvar=='met_nolep_et/1.0e3':
        pvar_out='truthmet'
    if pvar=='met_nolep_et/1.0e3':
        pvar_out='truthmetnolep'
    if pvar.count('pow(truth_jj_deta,2)'):
        pvar_out='centrality'
    if pvar=='jet_pt[2]/1.0e3':
        pvar_out='jet_pt2'
    can.SaveAs(sampleName+'_'+tpye+'_'+pvar_out+'.pdf')
