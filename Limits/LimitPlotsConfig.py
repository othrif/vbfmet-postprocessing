
import os
import re
import sys

#-----------------------------------------------------------------------------
def getLog(name, level = 'INFO'):

    import logging
    import sys
    
    f = logging.Formatter("Py:%(name)s: %(levelname)s - %(message)s")
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(f)
    
    log = logging.getLogger(name)
    log.addHandler(h)

    if level == 'DEBUG':   log.setLevel(logging.DEBUG)
    if level == 'INFO':    log.setLevel(logging.INFO)
    if level == 'WARNING': log.setLevel(logging.WARNING)    
    if level == 'ERROR':   log.setLevel(logging.ERROR)

    return log

#-----------------------------------------------------------------------------
def setATLASDefaults(ROOT, options = None):

    ROOT.gStyle.SetFillColor(10)           
    ROOT.gStyle.SetFrameFillColor(10)      
    ROOT.gStyle.SetCanvasColor(10)         
    ROOT.gStyle.SetPadColor(10)            
    ROOT.gStyle.SetTitleFillColor(0)       
    ROOT.gStyle.SetStatColor(10)   
    
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetFrameBorderMode(0) 
    ROOT.gStyle.SetPadBorderMode(0)   
    ROOT.gStyle.SetDrawBorder(0)      
    ROOT.gStyle.SetTitleBorderSize(0)
    
    ROOT.gStyle.SetFuncWidth(2)
    ROOT.gStyle.SetHistLineWidth(2)
    ROOT.gStyle.SetFuncColor(2)
    
    ROOT.gStyle.SetPadTopMargin(0.08)
    ROOT.gStyle.SetPadBottomMargin(0.16)
    ROOT.gStyle.SetPadLeftMargin(0.16)
    ROOT.gStyle.SetPadRightMargin(0.12)

    ROOT.gROOT.SetStyle("Plain");
  
    # set axis ticks on top and right
    ROOT.gStyle.SetPadTickX(1)         
    ROOT.gStyle.SetPadTickY(1)         
  
    # Set the background color to white
    ROOT.gStyle.SetFillColor(10)           
    ROOT.gStyle.SetFrameFillColor(10)      
    ROOT.gStyle.SetCanvasColor(10)         
    ROOT.gStyle.SetPadColor(10)            
    ROOT.gStyle.SetTitleFillColor(0)       
    ROOT.gStyle.SetStatColor(10)           
  
  
    # Turn off all borders
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetFrameBorderMode(0) 
    ROOT.gStyle.SetPadBorderMode(0)   
    ROOT.gStyle.SetDrawBorder(0)      
    ROOT.gStyle.SetTitleBorderSize(0) 
  
    # Set the size of the default canvas
    ROOT.gStyle.SetCanvasDefH(400)          
    ROOT.gStyle.SetCanvasDefW(650)          
    #gStyle->SetCanvasDefX(10)
    #gStyle->SetCanvasDefY(10)   
  
    # Set fonts
    font = 42
    ROOT.gStyle.SetLabelFont(font,"xyz")
    ROOT.gStyle.SetStatFont(font)       
    ROOT.gStyle.SetTitleFont(font)      
    ROOT.gStyle.SetTitleFont(font,"xyz")
    ROOT.gStyle.SetTextFont(font)       
    ROOT.gStyle.SetTitleX(0.3)        
    ROOT.gStyle.SetTitleW(0.4)        
  
   # Set Line Widths
   #gStyle->SetFrameLineWidth(0)
    ROOT.gStyle.SetFuncWidth(2)
    ROOT.gStyle.SetHistLineWidth(2)
    ROOT.gStyle.SetFuncColor(2)
  
   # Set margins
    ROOT.gStyle.SetPadTopMargin(0.08)
    ROOT.gStyle.SetPadBottomMargin(0.16)
    ROOT.gStyle.SetPadLeftMargin(0.16)
    ROOT.gStyle.SetPadRightMargin(0.12)
  
   # Set tick marks and turn off grids
    ROOT.gStyle.SetNdivisions(505,"xyz")
  
   # Set Data/Stat/... and other options
    ROOT.gStyle.SetOptDate(0)
    ROOT.gStyle.SetDateX(0.1)
    ROOT.gStyle.SetDateY(0.1)
   #gStyle->SetOptFile(0)
    ROOT.gStyle.SetOptStat(1110)
    ROOT.gStyle.SetOptFit(111)
    ROOT.gStyle.SetStatFormat("6.3f")
    ROOT.gStyle.SetFitFormat("6.3f")
   #gStyle->SetStatTextColor(1)
   #gStyle->SetStatColor(1)
   #gStyle->SetOptFit(1)
   #gStyle->SetStatH(0.20)
   #gStyle->SetStatStyle(0)
   #gStyle->SetStatW(0.30)
   #gStyle -SetStatLineColor(0)
    ROOT.gStyle.SetStatX(0.919)
    ROOT.gStyle.SetStatY(0.919)
    ROOT.gStyle.SetOptTitle(0)
   #gStyle->SetStatStyle(0000)    # transparent mode of Stats PaveLabel
    ROOT.gStyle.SetStatBorderSize(0)
  
   # Adjust size and placement of axis labels
    ROOT.gStyle.SetLabelSize(0.065,"xyz")
   #gStyle -> SetLabelOffset(0.005,"xyz")
   #gStyle -> SetTitleY(.98)
    ROOT.gStyle.SetTitleOffset(1.0,"xz")
    ROOT.gStyle.SetTitleOffset(1.15,"y")
    ROOT.gStyle.SetTitleSize(0.065, "xyz")
    ROOT.gStyle.SetLabelSize(0.065, "xyz")
    ROOT.gStyle.SetTextAlign(22)
    ROOT.gStyle.SetTextSize(0.12)
  
    # Set paper size for life in the US
    ROOT.gStyle.SetPaperSize(ROOT.TStyle.kA4)
  
   # Set color pallete
    ROOT.gStyle.SetPalette(1)
  
   #gStyle -> SetOptFit(0)
    ROOT.gStyle.SetOptStat("reimo")
   #gStyle -> SetStatStyle(0)	
    ROOT.gStyle.SetHistMinimumZero(True)
   
    ROOT.gROOT.ForceStyle()
