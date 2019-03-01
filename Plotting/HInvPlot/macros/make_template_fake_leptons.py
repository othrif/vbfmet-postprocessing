#!/usr/bin/env python

# A script to make template plots for lepton fake estimation.
# This version is intended to run on the output ROOT files and histograms
# from HInvPlot.
# Ben Rosser <bjr@sas.upenn.edu>

import array
import math
import os
import sys

import ROOT

# Stop ROOT from hijacking sys.argv.
ROOT.PyConfig.IgnoreCommandLineOptions = True

code = ROOT.gROOT.LoadMacro("AtlasStyle.C")
code = ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()

import argparse

def main():
    parser = argparse.ArgumentParser(description="A script to make template plots for lepton fake estimation.")
    parser.add_argument('filename', default="output.root", help="Output file from HInvPlot to run over.")
    parser.add_argument('-w', '--wait', action="store_true", dest="wait", help="Wait after drawing plot.")
    parser.add_argument('-n', '--name', dest="name", default="", help="The name of the plot to create.")
    parser.add_argument('-t', '--text', dest="text", default="", help="Text to put on the legend.")
    parser.add_argument('-r', '--region', dest="region", default="wcranti_allmjj_e", help="Region from HInvPlot to look at.")
    parser.add_argument('-v', '--var', dest="var", default="met_significance", help="Variable to plot.")
    parser.add_argument('-c', '--cutoff', dest="cutoff", default=40, type=int, help="Threshold value at which to take the ratio.")
    parser.add_argument('-b', '--rebin', dest="rebin", default=10, help="Number to rebin by when drawing the template shape plot.")
    args = parser.parse_args()

    filename = os.path.abspath(args.filename)

    tfile = ROOT.TFile(filename)
    keys = tfile.GetListOfKeys()

    region = "pass_" + args.region + "_Nominal"
    histname = os.path.join(region, "plotEvent_data", args.var)

    # TODO XXX: should we make this configurable?
    valid_mcs = ["wewk", "wqcd", "zewk", "zqcd"]

    data_hist = tfile.Get(histname)
    print("Reading histogram: " + histname)

    for mcname in valid_mcs:
        newname = histname.replace("data", mcname)
        print("Reading histogram: " + newname)
        mc_hist = tfile.Get(newname)
        try:
            data_hist.Add(mc_hist, -1)
        except:
            print("Error: failed to read histograms!")
            sys.exit(1)
    print("")

    # Okay, now make a new histogram to get the uncertainty!
    two_bin_initial = ROOT.TH1F("two_bins_initial", "two_bins_initial", 2, 0, 2)
    two_bin_final = ROOT.TH1F("two_bins_final", "two_bins_final", 2, 0, 2)

    # Integrate from 0 to 4 and retrieve the integrated error.
    low_error = ROOT.Double()
    low = data_hist.IntegralAndError(0, args.cutoff, low_error)
    low_var = float(low_error)**2

    # Integrate from 4 and above (bin 5+) and retrieve the integrated error.
    high_error = ROOT.Double()
    high = data_hist.IntegralAndError(args.cutoff + 1, data_hist.GetNbinsX()+2, high_error)
    high_var = float(high_error)**2

    # Fill one histogram with the number of low (<4) and high (>4) events.
    two_bin_final.SetBinContent(1, low)
    two_bin_final.SetBinError(1, math.sqrt(low_var))
    two_bin_final.SetBinContent(2, high)
    two_bin_final.SetBinError(2, math.sqrt(high_var))

    # Fill another with the number of events *before* this cut.
    for i in range(1, 3):
        two_bin_initial.SetBinContent(i, low+high)
        two_bin_initial.SetBinError(i, math.sqrt(low_var + high_var))

    # Using a TEfficiency, compute the error from applying the cut "metsig <= 4".
    # Since these histograms are weighted, TEfficiency wants to use Bayesian
    # statistics with a uniform prior-- I think only Bayesian methods are supported here.
    efficiency = ROOT.TEfficiency(two_bin_final, two_bin_initial)
    efficiency.SetStatisticOption(ROOT.TEfficiency.kBUniform)
    efficiency.SetPosteriorMode()
    value = efficiency.GetEfficiency(1)

    # The ratio, then, is just the efficiency of this cut over (1 - efficiency).
    # (as that gives us the efficiency of the cut metsig > 4).
    ratio = value / (1-value)

    # The error on the efficiency, though, is the maximum of the low/up error.
    error = max(efficiency.GetEfficiencyErrorLow(1), efficiency.GetEfficiencyErrorUp(1))

    # ...or, we can compute the error using binomial statistics instead.
    binomial_error = 1/(low+high) * math.sqrt(low * (1 - low/(low+high)))

    # Regardless of what we do, we need to propagate the error on the efficiency
    # to the error on the ratio, which should be the same regardless.
    ratio_error = error * math.fabs(1 / (1-value)**2)
    ratio_bin_error = binomial_error * math.fabs(1 / (1-value)**2)

    print("")
    if data_hist.GetBinContent(0) != 0:
        print("Below 0 = %f +/- %f" % (data_hist.GetBinContent(0), data_hist.GetBinError(0)))

    print("Below 4 = %f +/- %f" % (low, math.sqrt(low_var)))
    print("Above 4 = %f +/- %f" % (high, math.sqrt(high_var)))
    print("Ratio (TEfficiency) = %f +/- %f" % (ratio, ratio_error))
    print("Ratio (Binomial) = %f +/- %f" % (ratio, ratio_bin_error))
    print("")

    # Now that we've made the estimate, draw the MEt significance template shape.

    # Taken from drawStack.py-- rebin so 1 bin = 1 sqrt(GeV)
    # Actually, make this configurable parameter.
    data_hist.Rebin(args.rebin)

    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    data_hist.Draw()
    canvas.Update()

    data_hist.GetXaxis().SetTitle("MET Significance [GeV^{1/2}]")
    data_hist.GetYaxis().SetTitle("Events")

    ROOT.ATLASLabel(0.65, 0.85, "Internal")

    legend = ROOT.TLegend(0.55, 0.7, 0.92, 0.85)

    legend_header = "AntiID Template Shape"
    #legend.SetHeader(legend_header, "C")
    legend.AddEntry(0, legend_header, "")
    if not args.text == "":
        legend.AddEntry(0, args.text, "")
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.Draw()

    output_name = "anti_id_template.eps"
    if args.name != "":
        output_name = args.name + "_" + output_name
    canvas.SaveAs(output_name)
    if args.wait:
        raw_input()

if __name__ == '__main__':
    main()
