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
def prepareListPlot(selkey, alg_take=None, alg_pass=None, alg_suff='', region=None, nbin_lim=None, skip_samples=False, my_cut_key=''):
    #
    # Make alg for all events - this algorithm stores events for MakeInput
    #
    #plot_var = [] #options.var]
    #print 'alg_suff',alg_suff
    #plot_alg = hstudy.preparePlotEvent('plotEvent%s' %alg_suff,
    #                                   Vars=plot_var,
    #                                   SelKey=selkey,
    #                                   Region=region,
    #                                   PassAlg=alg_pass,
    #                                   NBinLim=nbin_lim)
    #
    #if type(alg_take) == type([]):
    #    alg_take += [plot_alg]

    #
    # Make plot algorithm for MC samples
    #
    #plot_algs = [plot_alg]
    plot_algs=[]
    if not skip_samples:

        for key, samples in hstudy.fillSampleList(options=options).iteritems():
            plot_algs += [hstudy.preparePlotEvent('plotEvent%s_%s%s' %(alg_suff, key, my_cut_key),
                                                  Samples=samples,
                                                  PassAlg=alg_pass)]
        
    return plot_algs

#-----------------------------------------------------------------------------------------
def prepareSeqSR(basic_cuts, alg_take=None):

    selkey = basic_cuts.GetSelKey()
    region = 'sr'

    if basic_cuts.chan !='nn' or not passRegion(region):
        return ('', [])
    
    pass_alg = hstudy.preparePassEventForSR('pass_%s_%s' %(region, selkey), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region)

    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def prepareSeqWCR(basic_cuts, region, alg_take=None):

    selkey = basic_cuts.GetSelKey()
    region = 'wcr'
    
    if basic_cuts.chan in ['ee','uu','ll','nn'] or not passRegion(region):
        return ('', [])
    
    pass_alg = hstudy.preparePassEventForWCR('pass_%s_%s' %(region, selkey), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region)

    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)

#-----------------------------------------------------------------------------------------
def prepareSeqZCR(basic_cuts, region, alg_take=None):

    selkey = basic_cuts.GetSelKey()
    region = 'zcr'
    if basic_cuts.chan in ['ep','em','um','up','l','e','u','nn'] or not passRegion(region):
        return ('', [])
    
    pass_alg = hstudy.preparePassEventForZCR('pass_%s_%s' %(region, selkey), options, basic_cuts, cut=options.cut)
    plot_alg = prepareListPlot              (selkey, alg_take, region=region)

    # return normal plotting
    return (pass_alg.GetName(), [pass_alg] + plot_alg)
                
#-----------------------------------------------------------------------------------------
def main():

    if len(args) < 1 and options.input==None and options.files==None :
        log.error('Must pass at least one one input command argument or give an -i input.txt')
        sys.exit(1)

    config.loadLibs(ROOT)     

    #-----------------------------------------------------------------------------------------
    # Prepare run numbers for requested samples and find input files
    #
    all_files = hinput.getInputSimlFiles(options.input,options.files)
    all_runs  = hinput.prepareBkgRuns(options.sample,options=options)

    #----------------------------------------------------------------------------------------
    # Create and configure main algorithm which reads input files and runs event loop
    #
    read_alg = hinput.ReadEvent('readEvent', options, all_files, all_runs)

    #-----------------------------------------------------------------------------------------
    # Prepare selection keys
    #
    anas    = ['allmjj']
    chans   = ['nn','ep','em','up','um','ee','uu','ll','l','e','u']

    if options.chan != None:
        chans = options.chan.split(',')

    #-----------------------------------------------------------------------------------------
    # Common algorithms for computing additional event properties and event pre-selection
    #     
    # Currently using mc name because tatsuya does not store the mc channel number
    #
    plot_alg = hstudy.preparePlotEvent('plotEvent')        
    read_alg.AddCommonAlg(plot_alg)    

    #-----------------------------------------------------------------------------------------
    # Cutflow algorithm list
    #
    input_cut = []

    try:
        tmp_signs=options.lep_sign.split(','); signs=[]
        for sign in tmp_signs: 
            if not sign in ['0','1']: raise NameError('Unknown Lepton sign: %s...needs to be 0 0,1 or 1' %options.lep_sign)
            signs+=[int(sign)]
    except: raise NameError('Unknown Lepton sign: %s...needs to be 0 0,1 or 1' %options.lep_sign)
        
    for sign in signs: # 0=opposite sign, 1=same sign
        for a in anas:            
            for c in chans:
                basic_cuts = hstudy.BasicCuts(Analysis=a, Chan=c, SameSign=sign)
                    
                #
                # SR Cut based regions and algorithms
                #
                (name_sr,  alg_sr)  = prepareSeqSR (basic_cuts, alg_take=input_cut)
                read_alg.AddNormalAlg(name_sr,  alg_sr)

                #
                # ZCR Cut based regions and algorithms
                #
                (name_zcr,  alg_zcr)  = prepareSeqZCR (basic_cuts, a, alg_take=input_cut)
                read_alg.AddNormalAlg(name_zcr,  alg_zcr)

                #
                # WCR Cut based regions and algorithms
                #
                (name_wcr,  alg_wcr)  = prepareSeqWCR (basic_cuts, a, alg_take=input_cut)
                read_alg.AddNormalAlg(name_wcr,  alg_wcr)                  

    read_alg.RunConfForAlgs()

    #-----------------------------------------------------------------------------------------
    # Read selected input files and process events (real work is done here...)
    # 
    timeStart = time.time()

    for ifile in all_files:
        print 'File: ',ifile
        read_alg.ReadFile(ifile)
    
    #-----------------------------------------------------------------------------------------
    # Save histograms from algorithms
    #
    read_alg.Save(options.rfile)

    #-----------------------------------------------------------------------------------------
    # Save histograms for limit setting
    #  ---- currently not configured.....
    if options.lfile and options.syst != None: 
        print '--------------------------------------------------------------------'
        log.info('Make limit inputs for: syst=%s' %options.syst)
        if options.tfile:
            tfile = ROOT.TFile(options.tfile, 'RECREATE')
        else:
            tfile = None
            
        log.info('Write limit files...')

        if tfile:
            tfile.Write()
            del tfile

    log.info('All is done - total job time: %.1fs' %(time.time()-timeStart))

#-----------------------------------------------------------------------------------------
# Main function for command line execuation
#
if __name__ == '__main__':
    main()
    
