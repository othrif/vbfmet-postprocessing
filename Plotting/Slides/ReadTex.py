import os,sys,math

import HInvPlot.JobOptions as config

log = config.getLog('ReadTex.py')
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
    line+='\\author{Doug Schaefer \\href{mailto:schae@cern.ch}{schae@cern.ch} \\and Rui Zou \\and Mark Oreglia \\and Young-Kee Kim} \n'
    if isVBFGroup:
        #line+='\\and \n'
        #line+='Rui Zou \\and Mark Oreglia \\and Young-Kee Kim} \n'
        #line+='\\institute[Chicago]\n'
        #line+='{\\textit{\\Large University of Illinios} $\\newline$\n'
        line+='\\textit{\\Large University of Chicago} $\\newline$\n'
        #line+='\\textit{\\Large Duke University} $\\newline$\n'
        #line+='\\textit{\\Large Ludwig Maximilian University of Munich}}\n'
    else:
        line+='\\institute{Department of Physics, University of Chicago} \n \n'

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
            
if __name__ == "__main__":

    f=open('vbf_qcd_validation.tex','w')
    f.write(GetHeader('Validation of QCD ntuples'))
    dir1='../QCDVRLoose/'
    samples = [['pass_sr_mjjLow200_nn_','pass_sr_deta25_nn_'],['pass_sr_LowMETQCD_nn_','pass_sr_LowMETQCDFJVT_nn_'],
                   ['pass_sr_LowMETQCDVR_nn_','pass_sr_LowMETQCDVRFJVT_nn_'],
                   ['pass_sr_LowMETQCDSR_nn_','pass_sr_LowMETQCDSRFJVT_nn_'],                   
                   ]

    filelist = ['Nominal_jj_mass_Nominal.pdf','Nominal_jj_deta_Nominal.pdf',
                    'Nominal_jj_dphi_Nominal.pdf','Nominal_met_tenacious_tst_et_Nominal.pdf',
                    'Nominal_met_soft_tst_et_Nominal.pdf','Nominal_j0fjvt_Nominal.pdf',
                    'Nominal_j1fjvt_Nominal.pdf','Nominal_jetPt0_Nominal.pdf','Nominal_jetPt1_Nominal.pdf','Nominal_n_jet_Nominal.pdf']
    titles = ['Jet Invariant Mass', 'Jet rapidity separation', 'Jet $\\phi$ Separation','MET','MET soft', 'Lead Jet fjvt','SubLead Jet fjvt','Leading Jet $p_{T}$','SubLeading Jet $p_{T}$','Number of Jets']
    for s in samples:
        i=0        
        for fi in filelist:
            xtitle=''
            ytitle=''
            titleR='LowMET'
            if s[0].count('LowMETQCDSR'):
                titleR='LowMET2j'
            if s[0].count('LowMETQCDVR'):
                titleR='LowDEtajj'
            if s[1].count('FJVT'):
                xtitle+='No FJVT'
                ytitle+='With FJVT'
            if s[0].count('mjjLow200'):
                #xtitle='Low $M_{jj}<1000$ GeV'
                #ytitle='$2.5<\\Delta\\eta_{jj}<3.8$'
                xtitle='LowMjj'
                ytitle='DEta25'
                titleR='QCD Validation'
            f.write(Get2Chart(names=[dir1+s[0]+fi,dir1+s[1]+fi], title=titleR+' '+titles[i],xtitle=xtitle,ytitle=ytitle))                
            i+=1
    f.write(GetEnd())
    f.close()
        
    #f=open('vbf_dphiBug.tex','w')
    #f.write(GetHeader('Validation of MET DPhi Bug ntuples'))
    #
    #dir1='../Baseline2018/'
    #dir2='../Baseline201516/'
    #dir1='../Baseline2016BugFix/'
    #samples = [['pass_wcr_allmjj_e_','pass_wcr_allmjj_u_'],['pass_zcr_allmjj_ee_','pass_zcr_allmjj_uu_'],
    #               ['pass_sr_allmjj_nn_']
    #               ]
    #    #jj_mass,jj_dphi,met_tst_et,met_tst_nolep_et,jj_deta,met_significance,met_tst_et,lepPt0 
    #filelist = ['Nominal_jj_mass_Nominal.pdf','Nominal_jj_deta_Nominal.pdf',
    #                'Nominal_jj_dphi_Nominal.pdf','Nominal_met_tst_et_Nominal.pdf',
    #                'Nominal_met_tst_nolep_et_Nominal.pdf','Nominal_met_significance_Nominal.pdf',
    #                'Nominal_lepPt0_Nominal.pdf']
    #titles = ['Jet Invariant Mass', 'Jet rapidity separation', 'Jet $\\phi$ Separation','MET','MET no leptons', 'MET Significance','Leading lepton $p_{T}$']
    #for s in samples:
    #    i=0        
    #    for fi in filelist:
    #        if len(s)==2:
    #            f.write(Get4Chart(names=[dir2+s[0]+fi,dir2+s[1]+fi,dir1+s[0]+fi,dir1+s[1]+fi], title=titles[i],xtitle='2015 and 2016',ytitle='Bug Fix'))
    #        elif len(s)==1:
    #            f.write(Get2Chart(names=[dir2+s[0]+fi,dir1+s[0]+fi], title='SR '+titles[i],xtitle='2015 and 2016',ytitle='Bug Fix'))                
    #        i+=1
    #f.write(GetEnd())
    #f.close()

    
    #ls = os.listdir('/Users/schaefer/PENN_physics/testarea/AtlasMuonFakes/CAFAna/HWWMVACode/VBFStudies/noMETCut/WWCR/wwcr_1jet/mtw40')

    #for i in ls:
    #    if not i.count('.table'):
    #        continue;
    #    map1=ReadFile('/Users/schaefer/PENN_physics/testarea/AtlasMuonFakes/CAFAna/HWWMVACode/VBFStudies/noMETCut/WWCR/wwcr_1jet/mtw40/'+i)
    #    AddQCD(map1,i);
    #    #sys.exit(0)
    ##Adding two tables together!!
    ##AddTwoTables('vbf_publ_mm.table','vbf_publ_ee.table')
    ##AddTwoTables('sr_eemm_cr.table','sr_emme_cr.table')
    #
    ## Generate a table comparing 2011 to 2012
    ##map1=ReadFile('ALL_FullSim_blind.table')
    ##map2=ReadFile('ALL_FullSim_blind_2012.table')
    #if False:
    #    map1=ReadFile('ALL_FullSim_unblind.table')
    #    map2=ReadFile('SR_2012_unblind.table')
    #
    #    all_cuts_ratio_list,all_cut_names=PrintRatio(map1,map2,scale2=0.35292307692307695)
    ##all_cuts_ratio_list,all_cut_names=PrintRatio(map1,map2,scale2=1.0)
    ##print 'name: ',all_cut_names
    ##print 'name: ',all_cuts_ratio_list
    #    PrintRatioTeX('SR_top_syst_unblind.table',map1,all_cuts_ratio_list,all_cut_names)

    #print map1
    #print map2
    #TopSyst
    #map1=ReadFile('ReAnalysis/VBF_blind_cutflow_Jan16/SR_eemm_blind_SF.table')
    #map2=ReadFile('ReAnalysis/VBF_blind_cutflow_Jan16/SR_sherattbar_mergedSF.table')

    #map1=ReadFile('ReAnalysis/VBF_blind_cutflow_Jan16/SR_merged_blind_OF.table')
    if False:
        map2=ReadFile('ReAnalysis/VBF_blind_cutflow_Jan16/SR_mcatnlo_mergedOF.table')
        map1=ReadFile('ReAnalysis/VBF_blind_cutflow_Jan16/SR_sherpattbar_mergedOF.table')
        
    #map2=ReadFile('ReAnalysis/VBF_blind_cutflow_Jan16/SR_mcantlo_mergedSF.table')
    #map1=ReadFile('ReAnalysis/VBF_blind_cutflow_Jan16/SR_sherattbar_mergedSF.table')
        all_cuts_ratio_list,all_cut_names=PrintRatio(map1,map2,scale2=1.0)
        PrintRatioTeX('SR_top_syst_unblind.table',map1,all_cuts_ratio_list,all_cut_names, bin_num=4)
    if False:

        map2=ReadFile('ReAnalysis/wjet/ptre_0j.table')
        map1=ReadFile('ReAnalysis/wjet/ptno_0j.table')
        
        all_cuts_ratio_list,all_cut_names=PrintRatio(map1,map2,scale2=1.0)
        PrintRatioTeX('Ratio_0j_sig_2011.table',map1,all_cuts_ratio_list,all_cut_names, bin_num=11)

    if False:
        line=GetHeader(title='Low Pt')
        cuts=['bveto_cut','pttot_cut','dyjj_cut','mll_cut'] #,'mll_cut','mt_cut']
        
        base='os_v2_17_lopt_abcd/'
        chans=['ee','uu','ll','ll']
        chans=['ee','uu','ORDEReu','ORDERue']
        pvars=["mll","mt","lep0Pt","lep0Phi","lep0Eta","lep1Pt","lep1Phi","lep1Eta","met","met_rel","dyjj","mjj","mtl0met","mtl1met","dphill","drlj","pttot","ptll","cen_jet_leadpt"]
        regs=['hwwcut']
        #regs=['zabcdD']#,'zabcdB','zabcdC','zabcdD']
        #pass_hwwcut_lopt_2j_uu_pttot_Nominal
        for pvar in pvars:
            for cut in cuts:
                base_names=[]
                for reg in regs:
                    for chan in chans: 
                        base_names+=[base+cut+'/'+'pass_'+reg+'_lopt_2j_'+chan+'_'+pvar+'_Nominal.pdf']

                    line+=Get4Chart(names=base_names, title=pvar+' '+reg+' Cut: '+cut[:-4])

        line+=GetEnd()
        f=open('out.tex','w')
        f.write(line)
        f.close()
