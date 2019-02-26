import os
import sys
import ROOT

def Style():
    pathToScript=os.path.realpath(__file__).strip(__file__.split("/")[-1])
    ROOT.gROOT.LoadMacro(os.path.expandvars("${SourceArea}/VBFAnalysis/python/Plotting/AtlasStyle/AtlasStyle.C"))
    ROOT.gROOT.LoadMacro(os.path.expandvars("${SourceArea}/VBFAnalysis/python/Plotting/AtlasStyle/AtlasUtils.C"))
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
                           
        if selkey.count('sr_'):  proc += ', SR'
        if selkey.count('wcr'): proc += ', WCR'
        if selkey.count('zcr'): proc += ', ZCR'

    return proc

def getATLASLabels(pad, x, y, lumi, text=None, selkey=None):
    
    l = ROOT.TLatex(x, y, 'ATLAS')
    l.SetNDC()
    l.SetTextFont(72)
    l.SetTextSize(0.055)
    l.SetTextAlign(11)    
    l.SetTextColor(ROOT.kBlack)
    l.Draw()    
    
    # delx = 0.05*pad.GetWh()/(pad.GetWw())
    labs = [l]
    
    if True:
        p = ROOT.TLatex(x+0.15, y, ' Internal') #
        p.SetNDC()
        p.SetTextFont(42)
        p.SetTextSize(0.055)
        p.SetTextAlign(11)
        p.SetTextColor(ROOT.kBlack)        
        p.Draw()
        labs += [p]

        a = ROOT.TLatex(x, y-0.04, '#sqrt{s}=13 TeV, %.1f fb^{-1}' %(lumi))
        a.SetNDC()
        a.SetTextFont(42)
        a.SetTextSize(0.04)
        a.SetTextAlign(12)
        a.SetTextColor(ROOT.kBlack)
        a.Draw()
        labs += [a]

    proc = getSelKeyLabel(selkey)
    if proc != None:
        
        c = ROOT.TLatex(x, y-0.08, proc)
        c.SetNDC()
        c.SetTextFont(42)
        c.SetTextSize(0.04)
        c.SetTextAlign(12)
        c.SetTextColor(ROOT.kBlack)
        labs += [c]
       
    return labs

