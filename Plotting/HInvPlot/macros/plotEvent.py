#!/usr/bin/env python

"""

This is an example macro for plotting events.

"""

import os
import re
import sys
import math
import time

import HInvPlot.JobOptions as config
import HInvPlot.systematics as systematics

par = config.getParser()
log = config.getLog('plotEvent.py')

(options, args) = par.parse_args()

#import PyCintex,
import ROOT
import HInvPlot.CutsDef as hstudy
import HInvPlot.Input   as hinput

#-----------------------------------------------------------------------------------------
def selectRegion(region):
    if options.region == None:
        return False
    elif region in options.region.split(','):
        return True
    return False

#-----------------------------------------------------------------------------------------
def passRegion(region):
    if options.region == None:
        return True
    elif region in options.region.split(','):
        return True
    return False

#-----------------------------------------------------------------------------------------
def prepareListPlot(selkey, alg_take=None, alg_pass=None, alg_suff='', region=None, nbin_lim=None, skip_samples=False, my_cut_key='', syst='Nominal'):
    #
    # Make alg for all events - this algorithm stores events for MakeInput
    #
    plot_algs=[]
    if not skip_samples:

        for key, samples in hstudy.fillSampleList(options=options).iteritems():
            plot_algs += [hstudy.preparePlotEvent('plotEvent%s_%s%s' %(alg_suff, key, my_cut_key),
                                                  syst_name=syst,
                                                  DetailLvl=options.DetailLvl,
                                                  Samples=samples,
                                                  PassAlg=alg_pass)]
                                                

    if options.no_plot:
        plot_algs = []
    return plot_algs

#-----------------------------------------------------------------------------------------
def prepareSeqSR(basic_cuts, alg_take=None, syst='Nominal'):

    selkey = basic_cuts.GetSelKey()
    region = 'sr'

    if basic_cuts.chan !='nn' or not passRegion(region):
        return ('', [])

    pass_alg = hstudy.preparePassEventForSR('pass_%s_%s_%s' %(region, selkey, syst), options, basic_cuts, cut=options.cut, syst=syst)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region, syst=syst)

    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def prepareSeqMETSF(basic_cuts, alg_take=None, syst='Nominal'):

    selkey = basic_cuts.GetSelKey()
    region = 'metsf'

    if not( basic_cuts.chan in ['nn','e','u']) or not passRegion(region):
        return ('', [])

    pass_alg = hstudy.preparePassEventForMETSF('pass_%s_%s_%s' %(region, selkey, syst), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region, syst=syst)
    
    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def prepareSeqGamSR(basic_cuts, alg_take=None, syst='Nominal'):

    selkey = basic_cuts.GetSelKey()
    region = 'gamsr'

    if basic_cuts.chan !='nn' or not passRegion(region):
        return ('', [])

    pass_alg = hstudy.preparePassEventForGamSR('pass_%s_%s_%s' %(region, selkey, syst), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region, syst=syst)
    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def prepareSeqGamZCR(basic_cuts, alg_take=None, syst='Nominal'):

    selkey = basic_cuts.GetSelKey()
    region = 'gamzcr'

    if (basic_cuts.chan not in ['ll','ee','uu']) or not passRegion(region):
        return ('', [])

    pass_alg = hstudy.preparePassEventForGamZCR('pass_%s_%s_%s' %(region, selkey, syst), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region, syst=syst)

    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def prepareSeqGamWCR(basic_cuts, alg_take=None, syst='Nominal'):

    selkey = basic_cuts.GetSelKey()
    region = 'gamwcr'

    if not( basic_cuts.chan in ['l','e','u']) or not passRegion(region):
        return ('', [])

    pass_alg = hstudy.preparePassEventForGamWCR('pass_%s_%s_%s' %(region, selkey, syst), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region, syst=syst)

    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def prepareSeqWCR(basic_cuts, region, alg_take=None, syst='Nominal'):

    selkey = basic_cuts.GetSelKey()
    region = 'wcr'

    do_met_signif=False
    if basic_cuts.chan in ['ep','em','e']:
        do_met_signif=True

    if basic_cuts.chan in ['ee','uu','ll','nn','eu'] or not passRegion(region):
        return ('', [])

    pass_alg = hstudy.preparePassEventForWCR('pass_%s_%s_%s' %(region, selkey, syst), options, basic_cuts, cut=options.cut, do_met_signif=do_met_signif)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region, syst=syst)

    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

def prepareSeqWCRAntiID(basic_cuts, region, alg_take=None, syst='Nominal'):

    selkey = basic_cuts.GetSelKey()
    region = 'wcranti'

    # The anti-ID region should always be e *or* mu; we don't want an
    # inclusive lepton region.
    if basic_cuts.chan in ['ee','uu','ll','nn','eu', 'l'] or not passRegion(region):
        return ('', [])

    pass_alg = hstudy.preparePassEventForWCRAntiID('pass_%s_%s_%s' %(region, selkey, syst), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot(selkey, alg_take, region=region, syst=syst)
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def prepareSeqZCR(basic_cuts, region, alg_take=None, syst='Nominal'):

    selkey = basic_cuts.GetSelKey()
    region = 'zcr'
    if basic_cuts.chan in ['ep','em','um','up','l','e','u','nn'] or not passRegion(region):
        return ('', [])

    pass_alg = hstudy.preparePassEventForZCR('pass_%s_%s_%s' %(region, selkey, syst), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region, syst=syst)

    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def main():

    if len(args) < 1 and options.input==None and options.files==None :
        log.error('Must pass at least one one input command argument or give an -i input.txt')
        sys.exit(1)

    config.loadLibs(ROOT)

    #-----------------------------------------------------------------------------------------
    # automatically set the lumi for the 2017 and 2018
    if options.year==2018 and options.int_lumi==36100.0:
        options.int_lumi=59937.2
    if options.year==2017 and options.int_lumi==36100.0:
        options.int_lumi=44307.4
        
    #-----------------------------------------------------------------------------------------
    # Prepare run numbers for requested samples and find input files
    #
    all_files = hinput.getInputSimlFiles(options.input,options.files)
    all_runs  = hinput.prepareBkgRuns(options.sample,options=options)

    #----------------------------------------------------------------------------------------
    # Create and configure main algorithm which reads input files and runs event loop
    #
    read_alg = hinput.ReadEvent('readEvent', options, all_files, all_runs, options.syst)

    #-----------------------------------------------------------------------------------------
    # Prepare selection keys
    #
    anas    = ['allmjj','mjj1000','mjj1500','mjj2000']
    if options.analysis!='all':
        anas = [options.analysis]
    if options.analysis.count('RedChan'):
        anas    = ['allmjj']#,'mjj1000','mjj1500','mjj2000']
    if options.analysis=='metsf':
        anas = ['metsf','metsfxe70','metsfxe90','metsfxe110','metsftrigxe70','metsftrigxe90','metsftrigxe70J400','metsftrigxe110','metsftrigxe110J400','metsftrigxe90J400',
                'metsfVBFTopo','metsfxe110XE70','metsfxe110XE65',
                'metsfxe90','metsfxe100','metsfxe110L155','metsfxe100L150',
                'metsfVBFTopotrigOR','metsfxe110XE70trig','metsfxe110XE65trig',
                'metsfxe90trig','metsfxe100trig','metsfxe110L155trig','metsfxe100L150trig',]
    if options.analysis.count('allmjjdphijj'):
        anas = ['allmjj','mjj1000dphijj1','mjj1500dphijj1','mjj2000dphijj1','mjj1000dphijj2','mjj1500dphijj2','mjj2000dphijj2']
    if options.analysis.count('allmjjdphijjnj'):
        anas = ['allmjj','mjj1000dphijj1nj2','mjj1500dphijj1nj2','mjj2000dphijj1nj2','mjj1000dphijj2nj2','mjj1500dphijj2nj2','mjj2000dphijj2nj2','njgt2']
    chans   = ['nn','ep','em','up','um','ee','uu','ll','l','e','u','eu']        
    if options.analysis=='qcd':
        anas = ['allmjj','mjjLow200','njgt2','deta25','LowMETQCDSR','LowMETQCDVR','LowMETQCD','LowMETQCDSRFJVT','LowMETQCDVRFJVT','LowMETQCDFJVT']
        chans   = ['nn']
    if options.analysis.count('RedChan'):
        chans   = ['nn','ee','uu','ll','l','e','u']
    if options.chan != None:
        chans = options.chan.split(',')

    try:
        tmp_signs=options.lep_sign.split(','); signs=[]
        for sign in tmp_signs:
            if not sign in ['0','1']: raise NameError('Unknown Lepton sign: %s...needs to be 0 0,1 or 1' %options.lep_sign)
            signs+=[int(sign)]
    except: raise NameError('Unknown Lepton sign: %s...needs to be 0 0,1 or 1' %options.lep_sign)

    writeStyle='RECREATE'
    syst_list=[options.syst]
    if options.syst=="All" or options.syst=='JES' or options.syst=='JER' or options.syst=='ANTISF':
        syst_class = systematics.systematics(options.syst) #All
        syst_list = syst_class.getsystematicsList()
    weight_syst_class = systematics.systematics('WeightSyst')
    weight_syst = weight_syst_class.getsystematicsList()

    timeStart = time.time()

    print 'Running These systematics'
    for syst in syst_list:
        print syst

    for syst in syst_list:
        print 'SYST: ',syst
        read_alg.ClearAlgs();
        if syst in weight_syst and (syst=='xeSFTrigWeight__1up' or syst=='xeSFTrigWeight__1down'):
            read_alg.SetSystName("Nominal")
            read_alg.SetWeightSystName("Nominal")
        elif syst in weight_syst:
            read_alg.SetSystName("Nominal")
            read_alg.SetWeightSystName(syst)
        else:
            read_alg.SetSystName(syst)
            read_alg.SetWeightSystName("Nominal")
        #-----------------------------------------------------------------------------------------
        # Common algorithms for computing additional event properties and event pre-selection
        #
        plot_alg = hstudy.preparePlotEvent('plotEvent',syst_name=syst,DetailLvl=options.DetailLvl)
        read_alg.AddCommonAlg(plot_alg)

        #-----------------------------------------------------------------------------------------
        # Cutflow algorithm list
        #
        input_cut = []

        for sign in signs: # 0=opposite sign, 1=same sign
            for a in anas:
                for c in chans:
                    basic_cuts = hstudy.BasicCuts(Analysis=a, Chan=c, SameSign=sign)
                    #
                    # MET trigger SF
                    #
                    if a.count('metsf'):
                        (name_metsf,  alg_metsf)  = prepareSeqMETSF(basic_cuts, alg_take=input_cut, syst=syst)
                        read_alg.AddNormalAlg(name_metsf,  alg_metsf)
                    else:
                        #
                        # SR Cut based regions and algorithms
                        #
                        (name_sr,  alg_sr)  = prepareSeqSR (basic_cuts, alg_take=input_cut, syst=syst)
                        read_alg.AddNormalAlg(name_sr,  alg_sr)
                        
                        #
                        # SR Cut based regions and algorithms with photon
                        #
                        if a=='allmjj':
                            (name_sr_gam,  alg_sr_gam)  = prepareSeqGamSR (basic_cuts, alg_take=input_cut, syst=syst)
                            read_alg.AddNormalAlg(name_sr_gam,  alg_sr_gam)
                            (name_zcr_gam,  alg_zcr_gam)  = prepareSeqGamZCR (basic_cuts, alg_take=input_cut, syst=syst)
                            read_alg.AddNormalAlg(name_zcr_gam,  alg_zcr_gam)
                            (name_wcr_gam,  alg_wcr_gam)  = prepareSeqGamWCR (basic_cuts, alg_take=input_cut, syst=syst)
                            read_alg.AddNormalAlg(name_wcr_gam,  alg_wcr_gam)
                        
                        #
                        # ZCR Cut based regions and algorithms
                        #
                        (name_zcr,  alg_zcr)  = prepareSeqZCR (basic_cuts, a, alg_take=input_cut, syst=syst)
                        read_alg.AddNormalAlg(name_zcr,  alg_zcr)
                        
                        #
                        # WCR Cut based regions and algorithms
                        #
                        (name_wcr,  alg_wcr)  = prepareSeqWCR (basic_cuts, a, alg_take=input_cut, syst=syst)
                        read_alg.AddNormalAlg(name_wcr,  alg_wcr)
                        
                        (name_wcranti, alg_wcranti) = prepareSeqWCRAntiID(basic_cuts, a, alg_take=input_cut, syst=syst)
                        read_alg.AddNormalAlg(name_wcranti, alg_wcranti)

        read_alg.RunConfForAlgs()

        #-----------------------------------------------------------------------------------------
        # Read selected input files and process events (real work is done here...)
        #
        for ifile in all_files:
            print 'File: ',ifile
            read_alg.ReadFile(ifile)

        #-----------------------------------------------------------------------------------------
        # Save histograms from algorithms
        #
        read_alg.Save(options.rfile, writeStyle=writeStyle)
        writeStyle='UPDATE'

    #-----------------------------------------------------------------------------------------
    # Save histograms for limit setting
    #  ---- currently not configured.....
    #if options.lfile and options.syst != None:
    #    print '--------------------------------------------------------------------'
    #    log.info('Make limit inputs for: syst=%s' %options.syst)
    #    if options.tfile:
    #        tfile = ROOT.TFile(options.tfile, 'RECREATE')
    #    else:
    #        tfile = None
    #
    #    log.info('Write limit files...')
    #
    #    if tfile:
    #        tfile.Write()
    #        del tfile

    log.info('All is done - total job time: %.1fs' %(time.time()-timeStart))

#-----------------------------------------------------------------------------------------
# Main function for command line execuation
#
if __name__ == '__main__':
    main()

