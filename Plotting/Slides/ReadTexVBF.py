import os,sys,math
import ROOT

import HInvPlot.JobOptions as config

log = config.getLog('ReadTex.py')

#-----------------------------------------
def Style():
    atlas_style_path='/Users/schae/testarea/SUSY/JetUncertainties/testingMacros/atlasstyle/'
    if not os.path.exists(atlas_style_path):
        print("Error: could not find ATLAS style macros at: " + atlas_style_path)
        sys.exit(1)
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasStyle.C'))
    ROOT.gROOT.LoadMacro(os.path.join(atlas_style_path, 'AtlasUtils.C'))
    ROOT.SetAtlasStyle()
def getSelKeyLabel(selkey):

    proc = None
    decay = 'Invis'
    if selkey != None: # and selkey.count('hww') or selkey.count('lowmet'):
        if True:
            if selkey.count('_nn'): proc = 'VBF H#rightarrow%s' %decay
            elif selkey.count('_ll'): proc = 'Z#rightarrow ll'
            elif selkey.count('_ee'): proc = 'Z#rightarrow ee'
            elif selkey.count('_eu'): proc = 'e#mu'
            elif selkey.count('_em'): proc = 'W#rightarrow e^{-}#nu'
            elif selkey.count('_uu'): proc = 'Z#rightarrow#mu#mu'
            elif selkey.count('_l'): proc = 'W#rightarrow l#nu'
            elif selkey.count('_e'): proc = 'W#rightarrow e#nu'
            elif selkey.count('_u'): proc = 'W#rightarrow#mu#nu'

        if selkey.count('LowMETQCD_'):  proc += ', Low MET QCD'        
        elif selkey.count('LowMETQCDFJVT_'):  proc += ', Low MET QCD'        
        elif selkey.count('LowMETQCDVR'):  proc += ', Low MET,2.5<#Delta#eta<3.8 QCD'        
        elif selkey.count('LowMETQCDSR'):  proc += ', Low MET QCD, N_{jet}=2'
        elif selkey.count('mjjLow200_'):  proc += ', 0.2<M_{jj}<1TeV'
        elif selkey.count('deta25_'):  proc += ', 2.5<#Delta#eta<3.8'
        elif selkey.count('njgt2_'):  proc += ',2<N_{jet}>5 SR'            
        elif selkey.count('sr_'):  proc += ', SR'
        elif selkey.count('wcr'):
            if 'anti' in selkey:
                proc += ', Anti-ID'
            else:
                proc += ', WCR'
        elif selkey.count('zcr'): proc += ', ZCR'
        if selkey.count('FJVT_'):  proc += ',f-jvt'                    
    return proc
#-------------------------------------------------------------------------
def getATLASLabels(pad, x, y, text=None, selkey=None):

    l = ROOT.TLatex(x, y, 'ATLAS')
    l.SetNDC()
    l.SetTextFont(72)
    l.SetTextSize(0.07)
    l.SetTextAlign(11)
    l.SetTextColor(ROOT.kBlack)
    l.Draw()

    delx = 0.05*pad.GetWh()/(pad.GetWw())
    labs = [l]

    if True:
        p = ROOT.TLatex(x+0.17, y, ' Internal') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.065)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.1f fb^{-1}' %(36100/1.0e3))
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.05)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        #labs += [a]

    proc = getSelKeyLabel(selkey)
    if proc != None:

        c = ROOT.TLatex(x, y-0.05, proc)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.05)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        labs += [c]

    return labs

#---------------------------------------------------------------------
#
def ReadFile(file_name):

    tex_map={}
    tex_map['cuts']={}
    tex_map['order']=[]
    f=open(file_name,'r')

    for line in f:
        if line.count('egin{tabular}'): tex_map['header']=line
        if line.count('\end{tabular}'):   tex_map['end']=line
        if line.count('Cut &') or line.count('Data'):           tex_map['titles']=line
        if line.count('NF='): continue
        # Found an interesting line
        if line.count('\\pm'):
            
            vals=line.split('&')
            cut_map=tex_map['cuts']
            cut_name=vals[0]
            tex_map['order']+=[cut_name]
            if len(cut_name.strip())==0: continue
            #print cut_name
            for i in range(0,len(vals)):
                if i==0: cut_map[cut_name]   =[]
                else:    cut_map[cut_name]+=[vals[i]]
            tex_map['cuts']=cut_map
            #if line.count('Top'): 
            #    print line
            #    print cut_map[cut_name]
        #print line
    #print tex_map

    # Done
    f.close()
    return tex_map

#------------------------
def ExtractVals(word,scale=1.0):
    val=0.0; err=0.0
    if word.count('\pm'):
        try:
            val,err=word.split('$\\pm$')
            val=scale*float(val.strip('\\\\ \n').strip())
            err=scale*float(err.strip('\\\\ \n').strip())
        except:

            try: 
                word=word[word.find('$'):word.rfind('$')]
                word=word.strip('$')
                val,err=word.split('\\pm')
                val=scale*float(val.strip())
                if err.count('_'):
                    err=err[err.rfind('}')-5:err.rfind('}')-1]
                err=scale*float(err.strip())
            except:
                print 'could  not decipher: ',word
                val=0.0; err=0.0
                                
    else: # for data
        try:
            word=word.rstrip('\\')
            val=scale*float(word.strip().strip('$').strip())
            err=math.sqrt(val)
        except:
            print 'could  not decipher 2: ',word
    
    return val,err
#------------------------
def PrintRatio(map1,map2,scale2=1.0, addInstead=False):
    ratio_map={}
    cuts1=map1['cuts']
    cuts2=map2['cuts']

    print map1['cuts']
    if map1['titles']!=map2['titles']: 
        print 'Titles do not match'
        print '1: ', map1['titles']
        print '2: ', map2['titles']
        sys.exit(0)
    all_cuts_ratio_list=[]; all_cut_names=[]
    #for cut_name,cut_vals1 in cuts1.iteritems():
    for cut_name in map1['order']:
        cut_vals1=cuts1[cut_name]
        if cut_name not in cuts2:
            print '-------------------------------------'
            print 'ERROR could not find cutname: ',cut_name
            print '-------------------------------------'
            continue
        cut_vals2=cuts2[cut_name]
        #print 'cutName:',cut_name,' ',cut_vals1
        if len(cut_vals1)!=len(cut_vals2): 
            print '-------------------------------------'
            print 'ERROR length not the same: ',cut_name
            print '-------------------------------------'
            continue

        ratio_list=[]
        data=0.0
        mc=0.0; mc_err=0.0
        for i in range(0,len(cut_vals1)):

            if i==(len(cut_vals1)-3):
                val1,err1=ExtractVals(cut_vals1[i])
                val2,err2=ExtractVals(cut_vals2[i], scale2)
                mc=val1+val2
                mc_err=math.sqrt(err1**2+err2**2)
            elif i==(len(cut_vals1)-2):
                val1,err1=ExtractVals(cut_vals1[i])
                val2,err2=ExtractVals(cut_vals2[i], scale2)
                data=val1+val2
            else:
                val1,err1=ExtractVals(cut_vals1[i], 1.0)
                val2,err2=ExtractVals(cut_vals2[i], 1.0)

            if addInstead:
                #
                # Addining two tables together
                #
                if i!=(len(cut_vals1)-1):

                    ratio=val1+val2
                    err=math.sqrt(err1*err1+err2*err2)
                else:

                    ratio=0.0
                    if mc!=0.0: ratio=data/mc
                    if mc!=0.0 and data!=0.0: 
                        err=ratio*math.sqrt((mc_err/mc)**2+1.0/data)
                    print 'ratio!!!',ratio
                ratio_list+=[[ratio,err]]
            else:
                #
                # Computing the ratio of two tables
                #
                ratio=0.0
                if val2!=0.0:
                    ratio=val1/val2
                else:
                    print 'ERROR - value 2: ',val2
        
                err='nan'
                if val1!=0.0 and val2!=0.0:
                    e1=err1/val1; e2=err2/val2
                    err=ratio*math.sqrt(e1*e1+e2*e2)
                ratio_list+=[[ratio,err]]

        # Saving
        all_cut_names+=[cut_name]
        all_cuts_ratio_list+=[ratio_list]

    return all_cuts_ratio_list,all_cut_names

#-----------------------------------------------------
def PrintRatioTeX(file_name='outname.table',map1={},ratio_list=[],cut_names=[],bin_num=-1,skipColumns=[]):

    f=open(file_name,'w')
    f.write('\\resizebox{\\textwidth}{!} { \n')
    f.write(map1['header'])
    f.write(map1['titles'])
    f.write('\\hline \\hline \n')

    #Loop over cuts
    i=0
    data=0.0;
    mc=0.0; mc_err=0.0;
    for row in ratio_list:
        cut_name=cut_names[i]
        f.write(cut_name+' &')
        #ratios=row
        u=0
        for r in row:
            if bin_num>0 and u!=bin_num: 
                u+=1
                continue
            elif u in skipColumns:
                u+=1
                continue
            else: u+=1

            #if u==(len(row)):
            #    r[0]=r[0]/2.0
            #    r[1]=r[1]/2.0

            if u==(len(row)-1):
                print 'data %5.0f' %r[0]
                try:
                    f.write(' & %5.0f' %(r[0])) # This is data
                except:
                    f.write(' & nan $\\pm$ nan ')
            else:
                try:
                    f.write(' & %5.2f $\\pm$ %5.2f ' %(r[0],r[1]))
                except:
                    f.write(' & nan $\\pm$ nan ')
        f.write(' \\\\ \n')
        i+=1
    f.write(map1['end'])
    f.write('} \n')
    f.close()

#-----------------------------------------------------    
def PrintTeX(map1, file_name):
    
    f=open(file_name,'w')
    he = "\\resizebox{\\textwidth}{!} { \n ";
    f.write(he);
    header = '\\begin{tabular}{l||llllllllllll|l||l} \n ' #map1['header']
    f.write(header);
    titles = map1['titles'].rstrip().rstrip('\n').rstrip().rstrip('\\');
    titles = titles + ' & Data/MC \\\\ \n'
    f.write(titles)
    f.write('\\hline \\hline \n')

    #Loop over cuts
    i=0
    cuts1=map1['cuts']
    for cut_name in map1['order']:
        cut_vals1=cuts1[cut_name]
        f.write(cut_name+' &')
        u=0
        for row in cut_vals1:
            if u==len(cut_vals1)-1:
                f.write(row)
            else:
                f.write(row+' &')
            u+=1     
        f.write(' \\\\ \n')
        i+=1
    f.write(map1['end'])
    f.write('} \n')
    f.close()
    
#-----------------------------------------------------
def GetHeader(title='2012 Low $P_T$ For VBF Study', isVBFGroup=False):
    #
    # Gets the title of the a latex presentation
    #

    line='\\documentclass[hyperref={colorlinks=true}]{beamer}\n'
    line+='\\usepackage{amssymb}\n'
    line+='\\usepackage{beamerthemeshadow}\n'
    line+='\\usepackage{beamerthemesplit} \n'
    line+='\\usepackage{hyperref}\n'
    line+='\\setbeamertemplate{footline}{\\hspace*{.5cm}\scriptsize{\n'
    line+='\\hspace*{50pt} \\hfill\\insertframenumber\\hspace*{.5cm}}} \n'
    line+='\\setbeamersize{text margin left=.2cm,text margin right=.2cm} \n'
    line+='\\begin{document}\n'

    line+='\\title{%s} \n' %title
    line+='\\author{Doug Schaefer \\href{mailto:schae@cern.ch}{schae@cern.ch} \\and Rui Zou \\and Mark Oreglia \\and Young-Kee Kim \\and Amanda Steinhebel} \n'
    if isVBFGroup:
        #line+='\\and \n'
        #line+='Rui Zou \\and Mark Oreglia \\and Young-Kee Kim} \n'
        #line+='\\institute[Chicago]\n'
        #line+='{\\textit{\\Large University of Illinios} $\\newline$\n'
        line+='\\textit{\\Large University of Chicago} $\\newline$\n'
        #line+='\\textit{\\Large Duke University} $\\newline$\n'
        #line+='\\textit{\\Large Ludwig Maximilian University of Munich}}\n'
    else:
        line+='\\institute{Department of Physics, University of Chicago, University of Oregon} \n \n'

    # Other headers
    line+='\\date{\\today} \n'

    line+='\\frame{\\titlepage}\n \n'
    return line

#--------------------------------------------------------
def GetGenericChart(message, title='Check Modelling'):
    #
    # Makes a page with four histograms
    #
    line='\\frame{\\frametitle{%s}\n' %(title)
    line+=message+'\n'
    line+='}\n'
    return line

#--------------------------------------------------------
def Get6Chart(names=[], title='Check Modelling'):
    #
    # Makes a page with four histograms
    #
    if len(names)!=6: 
        print 'ERROR - different than 6 histograms'
        return ''
    line='\\frame{\\frametitle{%s}\n' %(title)
    line+='\\begin{columns}\n'
    line+='\\begin{column}{4cm}\n'
    line+='\\includegraphics[angle=0.0, width=0.9\\textwidth]{%s}\n' %(names[0])
    line+='$\\newline$\n'
    line+='\\includegraphics[angle=0.0, width=0.9\\textwidth]{%s}\n' %(names[1])
    line+='\\end{column}\n'
    line+='\\begin{column}{4cm} \n'
    line+='\\includegraphics[angle=0.0, width=0.9\\textwidth]{%s}\n' %(names[2])
    line+='$\\newline$\n'
    line+='\\includegraphics[angle=0.0, width=0.9\\textwidth]{%s}\n' %(names[3])
    line+='\\end{column}\n'
    line+='\\begin{column}{4cm} \n'
    line+='\\includegraphics[angle=0.0, width=0.9\\textwidth]{%s}\n' %(names[4])
    line+='$\\newline$\n'
    line+='\\includegraphics[angle=0.0, width=0.9\\textwidth]{%s}\n' %(names[5])
    line+='\\end{column}\n'
    line+='\\end{columns}\n'
    line+='}\n'

    return line

#--------------------------------------------------------
def Get4Chart(names=[], title='Check Modelling',xtitle='',ytitle=''):
    #
    # Makes a page with four histograms
    #
    if len(names)!=4: 
        print 'ERROR - different than 4 histograms'
        return ''
    line='\\frame{\\frametitle{%s}\n' %(title)
    line+='\\begin{columns}\n'
    line+='\\begin{column}{6cm}\n'
    line+='%s $\\newline$ \n' %(xtitle)
    line+='\\includegraphics[angle=0.0, width=0.7\\textwidth]{%s}\n' %(names[0])
    line+='$\\newline$\n'
    line+='\\includegraphics[angle=0.0, width=0.7\\textwidth]{%s}\n' %(names[1])
    line+='\\end{column}\n'
    line+='\\vline\n'
    line+='\\begin{column}{6cm} \n'
    line+='%s $\\newline$ \n' %(ytitle)    
    line+='\\includegraphics[angle=0.0, width=0.7\\textwidth]{%s}\n' %(names[2])
    line+='$\\newline$\n'
    line+='\\includegraphics[angle=0.0, width=0.7\\textwidth]{%s}\n' %(names[3])
    line+='\\end{column}\n'
    line+='\\end{columns}\n'
    line+='}\n'

    return line

#--------------------------------------------------------
def Get3Chart(names=[], title='Check Modelling',xtitle='',ytitle=''):
    #
    # Makes a page with four histograms
    #
    if len(names)!=3: 
        print 'ERROR - different than 3 histograms'
        return ''
    line='\\frame{\\frametitle{%s}\n' %(title)
    line+='\\begin{columns}\n'
    line+='\\begin{column}{6cm}\n'
    line+='%s $\\newline$ \n' %(xtitle)
    line+='\\includegraphics[angle=0.0, width=0.7\\textwidth]{%s}\n' %(names[0])
    #line+='$\\newline$\n'
    #line+='\\includegraphics[angle=0.0, width=0.7\\textwidth]{%s}\n' %(names[1])
    line+='\\end{column}\n'
    line+='\\vline\n'
    line+='\\begin{column}{6cm} \n'
    line+='%s $\\newline$ \n' %(ytitle)    
    line+='\\includegraphics[angle=0.0, width=0.7\\textwidth]{%s}\n' %(names[1])
    line+='$\\newline$\n'
    line+='\\includegraphics[angle=0.0, width=0.7\\textwidth]{%s}\n' %(names[2])
    line+='\\end{column}\n'
    line+='\\end{columns}\n'
    line+='}\n'

    return line

#--------------------------------------------------------
def Get2Chart(names=[], title='Check Modelling',xtitle='',ytitle=''):
    #
    # Makes a page with four histograms
    #
    if len(names)!=2: 
        print 'ERROR - different than 2 histograms'
        return ''
    line='\\frame{\\frametitle{%s}\n' %(title)
    line+='\\begin{columns}\n'
    line+='\\begin{column}{6cm}\n'
    line+='%s $\\newline$ \n' %(xtitle)
    line+='\\includegraphics[angle=0.0, width=0.98\\textwidth]{%s}\n' %(names[0])
    line+='\\end{column}\n'
    line+='\\vline\n'
    line+='\\begin{column}{6cm} \n'
    line+='%s $\\newline$ \n' %(ytitle)    
    line+='\\includegraphics[angle=0.0, width=0.98\\textwidth]{%s}\n' %(names[1])
    line+='\\end{column}\n'
    line+='\\end{columns}\n'
    line+='}\n'

    return line

#--------------------------------------------------------
def GetList(ls=[],title='Check Modelling'):
    #
    # Makes a page with itemized list
    #
    line='\\frame{\\frametitle{%s}\n' %(title)
    line+='\\begin{itemize}\n'
    for l in ls:
        line+='\\item %s\n' %l
    line+='\\end{itemize}\n'
    line+='}\n'

    return line

#--------------------------------------------------------
def GetVRTable(title='Check Modelling'):
    #
    # Makes a page with itemized list
    #
    line='\\frame{\\frametitle{%s}\n' %(title)
    line+='\\begin{table}\n'
    #line+='\\begin{table}\n'    
    line+='\\end{table}\n'
    line+='}\n'

    return line

#--------------------------------------------------------
def GetEnd():
    
    return '\\end{document}\n'

#--------------------------------------------------------
def GetNFAndError(data,tot_bkg,tot_bkg_err, z_tot, z_err, returnFloat=False):

    nf=1.0
    z_err_rel=0.0
    other_bkg=(tot_bkg-z_tot)
    other_bkg_err = math.sqrt(tot_bkg_err*tot_bkg_err-z_err*z_err)
    if z_tot!=0.0:
        z_err_rel=(z_err/z_tot)
        nf=(data-other_bkg)/z_tot
    else: print 'ERROR - z total is 0!!! could not compute NF'

    nf_err=0.0
    nf_err_sq=0.0
    if (data-other_bkg)!=0.0: nf_err_sq = (data+other_bkg_err**2)/(data-other_bkg)/(data-other_bkg)
    else: print 'WARNING not error calculated because NF is 0!'

    nf_err= nf*math.sqrt(nf_err_sq+z_err_rel**2)

    if returnFloat: return nf,nf_err

    return 'NF=%5.3f +/- %5.3f' %(nf,nf_err)

#-----------------------------------
def AddTwoTables(n1, n2):

    map1=ReadFile(n1)
    map2=ReadFile(n2)

    all_cuts_ratio_list,all_cut_names=PrintRatio(map1,map2,scale2=1.0, addInstead=True)
    #print 'name: ',all_cut_names
    #print 'name: ',all_cuts_ratio_list
    #PrintRatioTeX('output.table', map1, all_cuts_ratio_list, all_cut_names, skipColumns=[6])
    PrintRatioTeX('output2.table', map1, all_cuts_ratio_list, all_cut_names)

#-----------------------------------
def AddQCD(map1, n='out.table'):
    cuts1=map1['cuts']
    for cut_name in map1['order']:
        cut_vals1=cuts1[cut_name]

        data=0.0
        mc=0.0; mc_err=0.0
        print cut_vals1
        for i in range(0,len(cut_vals1)):

            if i==(len(cut_vals1)-4): # QCD
                val1,err1=ExtractVals(cut_vals1[i])
            elif i==(len(cut_vals1)-3): # wjet
                val2,err2=ExtractVals(cut_vals1[i])
            elif i==(len(cut_vals1)-2): # total BKG
                val4,err4=ExtractVals(cut_vals1[i])                
            else: #
                val3,err3=ExtractVals(cut_vals1[i])


        wjet = val2 - 2.*val1
        wjet_err = math.sqrt(err1*err1+2.0*err2*err2)
        cut_vals1[len(cut_vals1)-3] = ' %0.1f $\\pm$ %0.1f ' %(wjet, wjet_err)

        bkg = val4 - 2.*val1
        bkg_err = math.sqrt(err4*err4+2.0*err2*err2)
        cut_vals1[len(cut_vals1)-2] = ' %0.1f $\\pm$ %0.1f ' %(bkg, bkg_err)
        cut_vals1[len(cut_vals1)-1] = ' %0.0f $\\pm$ %0.1f ' %(val3, err3)        

        mcr=0.0
        mcr_err=0.0
        if val3!=0.0 and bkg!=0.0:
            mcr = val3/bkg
            mcr_err = mcr*math.sqrt(err3/val3*err3/val3+bkg_err/bkg*bkg_err/bkg)
        cut_vals1+= [' %0.2f $\\pm$ %0.2f ' %(mcr, mcr_err)]

        print cut_vals1
            
    PrintTeX(map1,n)

def MakeRatio(indir1, indir2, plot_name,can):
    print plot_name
    print indir1+plot_name
    f1 = ROOT.TFile.Open(indir1+plot_name.replace('pdf','root'))
    f2 = ROOT.TFile.Open(indir2+plot_name.replace('pdf','root'))
    can.SetGridy(True);
    data_name=''
    bkg_name=''
    for i in f1.GetListOfKeys():
        plt_name= i.GetName()
        if plt_name.count('data_'):
            data_name=plt_name
            continue
        if plt_name.count('totbkg_'):
            bkg_name=plt_name
            continue
    dpltv1 = f1.Get(data_name)
    dpltv2 = f2.Get(data_name)
    bpltv1 = f1.Get(bkg_name)
    bpltv2 = f2.Get(bkg_name)

    exp_ratio = dpltv1.Clone()
    exp_ratio_one = dpltv1.Clone()
    rpltv1 = dpltv1.Clone()
    rpltv2 = dpltv2.Clone()
    rpltv1.Divide(bpltv1)
    rpltv2.Divide(bpltv2)
    
    leg = ROOT.TLegend(0.18,0.18,0.6,0.35)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    
    can.Clear();
    ROOT.gStyle.SetErrorX(0.5)
    dpltv1.Divide(dpltv2)
    bpltv1.Divide(bpltv2)
    rpltv1.Divide(rpltv2)
    dpltv1.GetYaxis().SetTitle('15+16 / 18')
    dpltv1.GetYaxis().SetRangeUser(0.0,2.0)    
    #dpltv1.GetYaxis().SetTitle('15+16 / 18')    
    dpltv1.SetLineColor(1)
    dpltv1.SetMarkerColor(1)
    bpltv1.SetMarkerStyle(21)
    rpltv1.SetMarkerStyle(22)
    bpltv1.SetLineColor(2)
    bpltv1.SetMarkerColor(2)
    rpltv1.SetLineColor(3)
    rpltv1.SetMarkerColor(3)
    dpltv1.SetStats(0)
    bpltv1.SetStats(0)
    rpltv1.SetStats(0)
    dpltv1.GetXaxis().SetTitle(bpltv1.GetXaxis().GetTitle())
    blind=False
    if not plot_name.count('pass_sr_allmjj_nn_'):
        dpltv1.Draw('e')
        bpltv1.Draw('same e')
        rpltv1.Draw('same e')
    else:
        blind=True
        #dpltv1.Draw('axis e')
        #can.GetPad(0).SetGridy(True);
        bpltv1.GetYaxis().SetTitle(dpltv1.GetYaxis().GetTitle())
        bpltv1.GetXaxis().SetTitle(dpltv1.GetXaxis().GetTitle())
        bpltv1.GetYaxis().SetRangeUser(0.0,2.0)
        bpltv1.Draw('e')

    eff = 36100.0/59937.0
    #eff = 36100.0/44307.4
    for i in range(0,exp_ratio.GetNbinsX()+1):
        exp_ratio.SetBinError(i,0.02*eff)
        exp_ratio_one.SetBinError(i,0.02*eff)        
        if dpltv1.GetBinContent(i)>0.0:
            exp_ratio.SetBinContent(i,eff)
            exp_ratio_one.SetBinContent(i,1.0)
        else:
            exp_ratio.SetBinContent(i,0.0)
            exp_ratio_one.SetBinContent(i,0.0)            
    lin = ROOT.TLine(0.0, eff, dpltv1.GetXaxis().GetBinUpEdge(dpltv1.GetNbinsX()-1), eff)
    lin.SetLineWidth(2)
    lin.SetLineStyle(1)
    lin.SetLineColor(5)
    #lin.SetMarkerSize(0)
    #lin.SetMarkerColor(5)
    lin.Draw()
    dkval = dpltv1.KolmogorovTest(exp_ratio, '')
    for i in range(0,exp_ratio.GetNbinsX()+1):
        if bpltv1.GetBinContent(i)>0.0:
            exp_ratio.SetBinContent(i,eff)
        else:
            exp_ratio.SetBinContent(i,0.0)
    
    bkval = bpltv1.KolmogorovTest(exp_ratio, '')
    rkval = rpltv1.KolmogorovTest(exp_ratio_one, '')
    if blind:
        rkval=-1
        dkval=-1        
    leg.AddEntry(dpltv1,'Data Ratio, KS: %.2f' %dkval)
    leg.AddEntry(bpltv1,'Bkg Ratio, KS: %.2f' %bkval)
    leg.AddEntry(rpltv1,'Data/Bkg Ratio, KS: %.2f' %rkval)
    a=leg.AddEntry(lin,'Ratio of Int. Lumi')
    a.SetMarkerSize(0)
    a.SetMarkerColor(5)
    leg.Draw()

    # atlas labeling

    texts = getATLASLabels(can, 0.2, 0.88, selkey=plot_name)
    for text in texts:
        text.Draw()
    
    can.Update()
    #can.WaitPrimitive()
    na = indir1+plot_name.replace('.pdf','_ratio.pdf')
    can.SaveAs(na)
    return na
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    #config.setPlotDefaults(ROOT)
    Style()
    can = ROOT.TCanvas('stack', 'stack', 700, 500)
    can.Draw()
    can.cd()
    
    f=open('vbf_2018_NoJetCut_ratios.tex','w')
    f.write(GetHeader('Ratios of 2018'))
    dir1='/tmp/v26LooseJ400Nominal_NoJetCut/'
    #dir2='/tmp/v28bLooseNominal/'    
    dir2='/tmp/v28bLooseNominal_NoJetCut/'    

    #,'Nominal_met_tenacious_tst_et_Nominal.pdf',]
    filelist = ['Nominal_jj_mass_Nominal.pdf','Nominal_jj_deta_Nominal.pdf',
                    'Nominal_jj_dphi_Nominal.pdf','Nominal_met_tst_et_Nominal.pdf','Nominal_met_soft_tst_et_Nominal.pdf','Nominal_j0fjvt_Nominal.pdf','Nominal_j1fjvt_Nominal.pdf','Nominal_jetPt0_Nominal.pdf','Nominal_jetPt1_Nominal.pdf','Nominal_n_jet_Nominal.pdf',
                    'Nominal_lepPt0_Nominal.pdf','Nominal_lepPt1_Nominal.pdf']
    titles = ['Jet Invariant Mass', 'Jet rapidity separation', 'Jet $\\phi$ Separation','MET','MET soft', 'Lead Jet fjvt','SubLead Jet fjvt','Leading Jet $p_{T}$','SubLeading Jet $p_{T}$','Number of Jets','Leading Lepton $p_{T}$','subLeading Lepton $p_{T}$']
    samples = ['pass_wcr_allmjj_e_','pass_wcr_allmjj_u_','pass_zcr_allmjj_ee_','pass_zcr_allmjj_uu_','pass_sr_allmjj_nn_']
    titles = ['Jet Invariant Mass', 'Jet rapidity separation', 'Jet $\\phi$ Separation','MET', 'MET soft', 'Lead Jet fjvt','SubLead Jet fjvt','Leading lepton $p_{T}$','SubLeading Jet $p_{T}$','Number of Jets','Leading Lepton $p_{T}$','subLeading Lepton $p_{T}$']#'MET Tenacious',
    for s in samples:
        i=0        
        for fi in filelist:
            n = MakeRatio(dir1,dir2,s+fi, can)
            f.write(Get3Chart(names=[dir1+s+fi,dir2+s+fi,n], title=titles[i],xtitle='2015 and 2016',ytitle='2018'))
            i+=1
    f.write(GetEnd())
    f.close()
