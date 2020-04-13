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

#    if basic_cuts.chan !='nn' or not passRegion(region):
#        return ('', [])

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
def main():

    if len(args) < 1 and options.input==None and options.files==None :
        log.error('Must pass at least one one input command argument or give an -i input.txt')
        sys.exit(1)

    config.loadLibs(ROOT)

    #-----------------------------------------------------------------------------------------
    # automatically set the lumi for the 2017 and 2018
    if options.year==2018 and options.int_lumi==36207.66:
        options.int_lumi=58450.1
    if options.year==2017 and options.int_lumi==36207.66:
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
    anas    = ['all']
    chans   = ['ee','uu','ll','eu']

    try:
        tmp_signs=options.lep_sign.split(','); signs=[]
        for sign in tmp_signs:
            if not sign in ['0','1']: raise NameError('Unknown Lepton sign: %s...needs to be 0 0,1 or 1' %options.lep_sign)
            signs+=[int(sign)]
    except: raise NameError('Unknown Lepton sign: %s...needs to be 0 0,1 or 1' %options.lep_sign)


    writeStyle='RECREATE'
    syst_list=[options.syst]
    if options.syst=="All" or options.syst=='JES' or options.syst=='JER' or options.syst=='ANTISF' or options.syst=='SigTheory':
        syst_class = systematics.systematics(options.syst) #All
        syst_list = syst_class.getsystematicsList()
    weight_syst_class = systematics.systematics('WeightSyst')
    weight_syst = weight_syst_class.getsystematicsList()

    timeStart = time.time()

    print 'Running the following systematics:'
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
                    basic_cuts = hstudy.BasicCuts(Analysis=a, Chan=c, options=options, SameSign=sign)
                    #
                    # SR Cut based regions and algorithms
                    #
                    (name_sr,  alg_sr)  = prepareSeqSR (basic_cuts, alg_take=input_cut, syst=syst)
                    read_alg.AddNormalAlg(name_sr,  alg_sr)


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

