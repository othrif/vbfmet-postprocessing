import ROOT
import HInvPlot.JobOptions as config
import HInvPlot.CutsDef    as hstudy
import os,sys
import array
import math

#-----------------------------------------
def Style():
    atlas_style_path='/afs/cern.ch/user/s/schae/public/atlasstyle/'
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasUtils.C'))
    ROOT.SetAtlasStyle()
    
def SetOverflow(h):

    under = h.GetBinContent(0)
    undere = h.GetBinError(0)
    under1 = h.GetBinContent(1)
    undere1 = h.GetBinError(1)
    h.SetBinContent(0,0.0)
    h.SetBinError(0,0.0)
    h.SetBinContent(1,under+under1)
    h.SetBinError(1,math.sqrt(undere**2+undere1**2))

    maxB=h.GetNbinsX()
    under = h.GetBinContent(maxB)
    undere = h.GetBinError(maxB)
    under1 = h.GetBinContent(maxB+1)
    undere1 = h.GetBinError(maxB+1)
    h.SetBinContent(maxB+1,0.0)
    h.SetBinError(maxB+1,0.0)
    h.SetBinContent(maxB,under+under1)
    h.SetBinError(maxB,math.sqrt(undere**2+undere1**2))    

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

    sampleName='H7Znn'
    tpye = 'Sig'
    #fZ = ROOT.TFile.Open('/eos/atlas/atlascerngroupdisk/penn-ww/schae/H7syst_6M/ZnunuNom/data-MiniNtuple/ZnunuNom.root')
    #fW = ROOT.TFile.Open('/eos/atlas/atlascerngroupdisk/penn-ww/schae/H7syst_6M/WmunuNom/data-MiniNtuple/WmunuNom.root')
    fZ = ROOT.TFile.Open('/eos/atlas/atlascerngroupdisk/penn-ww/schae/H7syst/H7_713_ZnunujjEW/data-MiniNtuple/363233Znn.root')
    fW = ROOT.TFile.Open('/eos/atlas/atlascerngroupdisk/penn-ww/schae/H7syst/H7_720_WmunujjEW/data-MiniNtuple/830006.root')    
    treeName1 = 'MiniNtuple'
    treeNamePow = 'MiniNtuple'
    plt=None
    #cuts = '*(jj_mass>1.0e6 && jj_dphi<1.8 && jj_deta>3.8 && met_cst_jet>120.0e3 && met_tst_nolep_et>150.0e3 && jet_pt[0]>80.0e3 && jet_pt[1]>50e3 && n_jet<5 && met_tst_et<20.0e3)'
    #cuts = '*(jj_mass>1.0e6 && jj_dphi<1.8 && jj_deta>3.8 && met_cst_jet>120.0e3 && met_tst_et>150.0e3 && jet_pt[0]>80.0e3 && jet_pt[1]>50e3 && n_jet<5 )'    
    #cuts = '*( truth_jj_mass>200e3 && boson_pt[0]>150e3 && truth_jj_deta>3.0 && truth_jj_dphi<2.5 && jet_pt[1]>40e3)'
    #cuts = '*( truth_jj_mass>200e3 && boson_pt[0]>150e3 && truth_jj_deta>3.0 && truth_jj_dphi<2.5 && jet_pt[1]>40e3)'
    #cuts = '*( truth_jj_mass>100e3  && jet_pt[1]>30e3 && truth_jj_dphi<2.5 && boson_pt[0]>90e3)'
    # Wln CR - only needed for the Wmunu
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && njets25==2 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<1.0 && truth_jj_deta>3.8 && mu_pt[0]>30e3 && abs(mu_eta[0])<2.5)'
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && njets25==2 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0  && truth_jj_dphi>1.0 && truth_jj_deta>3.8 && mu_pt[0]>30e3 && abs(mu_eta[0])<2.5)'
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && (njets25==3 || njets25==4) && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0 && truth_jj_deta>3.8 && mu_pt[0]>30e3 && abs(mu_eta[0])<2.5)'
    # Zll CR - only needed for the Zee
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && njets25==2 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0 && truth_jj_deta>3.8 && el_pt[0]>30e3 && abs(el_eta[0])<2.37 && el_pt[1]>4e3 && abs(el_eta[1])<2.37)'
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && njets25==2 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && && truth_jj_dphi<2.0  && truth_jj_dphi>1.0 && truth_jj_deta>3.8 && el_pt[0]>30e3 && abs(el_eta[0])<2.37 && el_pt[1]>4e3 && abs(el_eta[1])<2.37)'    
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && (njets25==3 || njets25==4) && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0 && truth_jj_deta>3.8 && el_pt[0]>30e3 && abs(el_eta[0])<2.37 && el_pt[1]>4e3 && abs(el_eta[1])<2.37)'
    # SR - only needed for the Znn and Wmunu
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && njets25==2 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0 && truth_jj_deta>3.8 && maxCentral_mu_pt<4.0e3)'
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && njets25==2 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0  && truth_jj_dphi>1.0 && truth_jj_deta>3.8 && maxCentral_mu_pt<4.0e3)'    
    #cuts = '*(truth_jj_mass>0.2e6 && met_nolep_et>160e3 && (njets25==3 || njets25==4) && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0 && truth_jj_deta>3.8 && maxCentral_mu_pt<4.0e3)'
    
    cuts = '*( 1)'
    #cuts = '*( njets25>1 && truth_jj_mass>0.2e6)'
    cuts2jet = '*(truth_jj_mass>0.5e6 && met_nolep_et>150e3 && njets25==2 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0 && truth_jj_deta>3.8)'
    cutsIncl = '*(truth_jj_mass>0.5e6 && met_nolep_et>150e3 && jet_pt[1]>40e3 && jet_pt[0]>60e3 && truth_jj_dphi<2.0 && truth_jj_deta>3.8)'    
    #cuts = '*(truth_jj_mass>0.2e6 && jet_pt[1]>40e3 && jet_pt[0]>60e3  && truth_jj_deta>3.0 && zboson_m>82.0e3 && zboson_m<116.0e3)' # && zboson_m>66.0e3 && zboson_m<116.0e3
    h1n = fZ.Get("NumberEvents")
    h2n = fW.Get("NumberEvents")
    runCutZ='/%s*0.63433' %(h1n.GetBinContent(2))
    runCutW='/%s*0.63433' %(h2n.GetBinContent(2))
    
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
        xaxis='Truth MET [GeV]'
    elif options.var=="met_nolep_et":
        pvar='met_nolep_et/1.0e3'
        xaxis='Truth MET (nonInt+Z-charged leptons) [GeV]'        

    tZ = fZ.Get(treeName1)
    tW = fW.Get(treeName1)
    newBinning = array.array('d',[800,1200,1500,2000,3500,5000])
    plots = []
    plotNames=['Iptruth_jj_mass','I2ptruth_jj_mass','I3ptruth_jj_mass','I4ptruth_jj_mass']
    for n1 in plotNames:
        plt=None
        if pvar.count('jj_mass'):
            #plt = ROOT.TH1F(n1,n1,10,0.0,5000.0)
            plt = ROOT.TH1F(n1,n1,len(newBinning)-1,newBinning)
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
        plots+=[plt]

    # Plotting the Z
    print tZ
    tZ.Draw(pvar+' >>'+plotNames[0],'EventWeight'+cuts2jet+runCutZ)
    plots[0].SetDirectory(fout)
    plots[0].SetMarkerSize(0.6)
    plots[0].GetYaxis().SetTitle('Jet Veto Eff.')
    plots[0].Write()
    tZ.Draw(pvar+' >>'+plotNames[1],'EventWeight'+cutsIncl+runCutZ)
    plots[1].SetDirectory(fout)
    plots[1].SetMarkerSize(0.6)
    plots[1].Write()
    # Plotting the W
    print tW
    tW.Draw(pvar+' >>'+plotNames[2],'EventWeight'+cuts2jet+runCutW)
    plots[2].SetDirectory(fout)
    plots[2].SetMarkerSize(0.6)
    plots[2].Write()
    tW.Draw(pvar+' >>'+plotNames[3],'EventWeight'+cutsIncl+runCutW)
    plots[3].SetDirectory(fout)
    plots[3].SetMarkerSize(0.6)
    plots[3].Write()

    rplots=[]
    rplots+=[plots[0].Clone()]
    rplots+=[plots[2].Clone()]
    rplots[0].SetLineColor(1)
    rplots[0].SetMarkerColor(1)
    rplots[1].SetLineColor(2)
    rplots[1].SetMarkerColor(2)
    rplots[0].Divide(rplots[0],plots[1],1.0,1.0,"B");
    rplots[1].Divide(rplots[1],plots[3],1.0,1.0,"B"); 
    #rplots[0].Divide(plots[1])
    #rplots[1].Divide(plots[3])
    
    # pads
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1.SetBottomMargin(0); # Upper and lower plot are joined
    #pad1.SetGridx();         # Vertical grid
    pad1.Draw();             # Draw the upper pad: pad1
    pad1.cd();               # pad1 becomes the current pad
    rplots[0].GetYaxis().SetRangeUser(0.65,0.9)
    rplots[0].Draw()
    rplots[1].Draw('same')
    print 'Plt1: ',plots[0].Integral()
    print 'Plt2: ',plots[1].Integral()       

    # Print the differences:
    for i in range(1,rplots[0].GetNbinsX()+1):
        diff = rplots[0].GetBinContent(i)-rplots[1].GetBinContent(i)
        # for the parton shower or powheg comparisons use the equation above. There is only nominal and parton shower        
        #  it is (up - down)/2.0 for example (MuUp - MuDw)/2.0
        #diff = (rplots[0].GetBinContent(i)-rplots[1].GetBinContent(i))/2.0
        print 'Bin range: %0.1f - %0.1f: %0.3f' %(rplots[0].GetXaxis().GetBinLowEdge(i),rplots[0].GetXaxis().GetBinUpEdge(i), diff)
    
    texts = getATLASLabels(can, 0.65, 0.88,'')
    for t in texts:
        t.Draw()

    leg = ROOT.TLegend(0.65, 0.2, 0.98, 0.5)
    leg.SetBorderSize(0)
    leg.SetFillStyle (0)
    leg.SetTextFont(42);
    leg.SetTextSize(0.04);
    leg.AddEntry(rplots[1],'EWK W#rightarrow#mu#nu')
    leg.AddEntry(rplots[0],'EWK Z#rightarrow#nu#nu')
    leg.Draw()

    can.cd();          # Go back to the main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.03, 1, 0.3);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.3);
    pad2.SetGridy(); # vertical grid
    pad2.Draw();
    pad2.cd();       # pad2 becomes the current pad

    hratio = rplots[0].Clone()
    
    hratio.GetYaxis().SetTitle('Z#rightarrow#nu#nu/W#rightarrow#mu#nu')
    hratio.GetYaxis().SetRangeUser(0.85,1.15)
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
    hratio.Divide(rplots[1])
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
        pvar_out='truthmetnolep'
    if pvar.count('pow(truth_jj_deta,2)'):
        pvar_out='centrality'
    if pvar=='jet_pt[2]/1.0e3':
        pvar_out='jet_pt2'
    can.SaveAs(sampleName+'_'+tpye+'_'+pvar_out+'.pdf')
