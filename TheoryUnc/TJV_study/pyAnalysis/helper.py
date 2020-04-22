import math
import ROOT

class HistEntry:
    def __init__(self, hist, hname):
        self.hname    = hname
        self.hist     = hist.Clone()
        self.file     = file
    def merge_bins(self):
        self.hist.SetBinContent(1,self.hist.GetBinContent(0)+self.hist.GetBinContent(1))
        self.hist.SetBinError(1,math.sqrt(self.hist.GetBinError(0)**2+self.hist.GetBinError(1)**2))
        self.hist.SetBinContent(0,0)
        self.hist.SetBinError(0,0)
        last_bin=self.hist.GetNbinsX()
        #print 'last_bin: ',last_bin,' ',self.hist.GetNbinsX()
        my_err = ROOT.Double(0)
        my_last_bin_val = self.hist.IntegralAndError(last_bin,self.hist.GetNbinsX()+5, my_err)
        self.hist.SetBinContent(last_bin,my_last_bin_val)
        self.hist.SetBinError(last_bin,my_err)
        for mbin in range(last_bin+1,self.hist.GetNbinsX()+2):
            self.hist.SetBinContent(mbin,0.0)
            self.hist.SetBinError(mbin,0.0)
        return self.hist
