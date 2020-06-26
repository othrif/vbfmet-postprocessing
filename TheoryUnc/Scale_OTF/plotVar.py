# python plotVar.py conf new test
#
import os
import sys
import ROOT
import numpy as np

max_def = 30
min_def = -1
pstyle={'up':['', ROOT.kRed, 1],'down':['SAME', ROOT.kRed, 7]};
xaxis = np.array(range(1,22))

def Style():
    ROOT.gROOT.LoadMacro('/afs/desy.de/user/o/othrif/atlasrootstyle/AtlasStyle.C')
    ROOT.gROOT.LoadMacro('/afs/desy.de/user/o/othrif/atlasrootstyle/AtlasUtils.C')
    ROOT.SetAtlasStyle()


def readFile(filename):
    var = {}
    with open(filename) as file:
        postfix = 'NONE'
        for line in file:
            if "up" in line or "down" in line:
                postfix = line.rstrip()
            if "renofact_Z_strong" in line or "renofact_W_strong" in line:
                l = line.rstrip().split()
                var[l[0]+"_"+postfix] = np.array([float(x) for x in l[1].split(',')])
    return var

def plotHist(can,histo1,histo2):
    histo1.GetXaxis().SetLabelOffset(0.01);
    histo1.SetTitle("");
    histo1.GetYaxis().SetTitle("Transfer Factor Uncertainty (%)");
    histo1.GetXaxis().SetTitle("Analysis bins");
    histo1.SetMinimum(min_def);
    histo1.SetMaximum(max_def);
    histo1.GetXaxis().SetNdivisions(21)
    histo1.SetLineColor(pstyle['up'][1]+1)
    histo1.SetMarkerColor(pstyle['up'][1]+1)
    histo1.SetLineStyle(pstyle['up'][2])
    histo2.SetLineColor(pstyle['down'][1]+1)
    histo2.SetMarkerColor(pstyle['down'][1]+1)
    histo2.SetLineStyle(pstyle['down'][2])
    histo1.Draw("HIST")
    histo2.Draw("HIST SAME E")
    legend=ROOT.TLegend(0.48,0.69,0.85,0.94);
    legend.SetHeader(proc+"+jets " + " reno./fact. ");
    legend.SetTextFont(62);
    legend.SetTextSize(0.04);
    legend.SetBorderSize(0);
    legend.AddEntry(histo1, "Up variation","l");
    legend.AddEntry(histo2, "Down variation","l");
    legend.Draw();
    can.Update()
    can.SaveAs(outPath+proc+'_env_tf.pdf')
    can.WaitPrimitive()

def plot2Hist(can,histo1,histo2,histo3,histo4):
    histo1.GetXaxis().SetLabelOffset(0.01);
    histo1.SetTitle("");
    histo1.GetYaxis().SetTitle("Transfer Factor Uncertainty (%)");
    histo1.GetXaxis().SetTitle("Analysis bins");
    histo1.SetMinimum(min_def);
    histo1.SetMaximum(max_def);
    histo1.GetXaxis().SetNdivisions(21)

    histo1.SetLineColor(ROOT.kRed+1)
    histo1.SetMarkerColor(ROOT.kRed+1)

    histo2.SetLineColor(ROOT.kRed+1)
    histo2.SetMarkerColor(ROOT.kRed+1)
    histo2.SetLineStyle(7)

    histo3.SetLineColor(ROOT.kBlue+1)
    histo3.SetMarkerColor(ROOT.kBlue+1)

    histo4.SetLineColor(ROOT.kBlue+1)
    histo4.SetMarkerColor(ROOT.kBlue+1)
    histo4.SetLineStyle(7)

    histo1.Draw("HIST")
    histo2.Draw("HIST SAME")
    histo3.Draw("HIST SAME E")
    histo4.Draw("HIST SAME E")

    legend=ROOT.TLegend(0.48,0.69,0.85,0.94);
    legend.SetHeader(proc+"+jets " + " reno./fact. ");
    legend.SetTextFont(62);
    legend.SetTextSize(0.04);
    legend.SetBorderSize(0);
    legend.AddEntry(histo1, "CONF: Up variation","l");
    legend.AddEntry(histo2, "CONF: Down variation","l");
    legend.AddEntry(histo3, "NEW: Up variation","l");
    legend.AddEntry(histo4, "NEW: Down variation","l");
    legend.Draw();
    can.Update()
    can.SaveAs(outPath+proc+'_env_tf.pdf')
    can.WaitPrimitive()

def getHist(var, nbins, doStat=False):
    histo = {}
    for sys in 'up', 'down':
        print 'renofact '+proc+' '+sys
        suf_stat=''
        if doStat:
            suf_stat='STAT'
        vbf_bins = abs(100*(1-var['renofact_'+proc+'_strong_SR'+sys]/var['renofact_'+proc+'_strong_CR'+proc+sys])).round(decimals=2)
        vbf_bins_stat = abs(np.sqrt(np.power(var['renofact_'+proc+'_strong_SR'+sys+suf_stat],2)+np.power(var['renofact_'+proc+'_strong_CR'+proc+sys+suf_stat],2))).round(decimals=2)
        histo[sys] = ROOT.TH1F(proc+sys+str(nbins), proc+sys, 21, 0.5,21.5)
        for i in xaxis:
            if i < 12:
                print i, vbf_bins[i-1]
                histo[sys].SetBinContent(i, vbf_bins[i-1])
                if doStat:
                    histo[sys].SetBinError(i,  vbf_bins_stat[i-1])
                else:
                    histo[sys].SetBinError(i,  0)
            else:
                if nbins > 11:
                    print i, vbf_bins[i-1]
                    histo[sys].SetBinContent(i, vbf_bins[i-1])
                    if doStat:
                        histo[sys].SetBinError(i,  vbf_bins_stat[i-1])
                    else:
                        histo[sys].SetBinError(i,  0)
                else:
                    histo[sys].SetBinContent(i, -5)
                    if doStat:
                        histo[sys].SetBinError(i,  vbf_bins_stat[i-1])
                    else:
                        histo[sys].SetBinError(i,  0)
    return histo['up'], histo['down']

Style()

filename1=sys.argv[1]
filename2=sys.argv[2]
output = sys.argv[3]

outPath = "./output/TF/"+output+"/"

if not os.path.exists(outPath):
    os.makedirs(outPath)


var1 = readFile(filename1)
var2 = readFile(filename2)


for proc in 'Z','W':
    can=ROOT.TCanvas()
    h1_up,h1_down=getHist(var1,11) # CONF
    h2_up,h2_down=getHist(var2,21 ) # NEW ,doStat=True
    #plotHist(can,h1_up,h1_down)
    plot2Hist(can,h1_up,h1_down,h2_up,h2_down)







