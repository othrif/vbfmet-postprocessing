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

import collections

# Hardcoded bin/region labels.
# these can be overridden by passing -t [text] to set text on the legend.
# (Labels for the other binning scheme(s) should be added here!)
region_labels = {"wcranti_mjj2000_e": "M_{jj} #geq 2000 GeV",
                 "wcranti_mjj1500_e": "1500 #leq M_{jj} #leq 2000 GeV",
                 "wcranti_mjj1000_e": "1000 #leq M_{jj} #leq 1500 GeV",
                 "wcranti_allmjj_e": "M_{jj} #geq 800 GeV",
                 "wcranti_mjj2000_u": "M_{jj} #geq 2000 GeV",
                 "wcranti_mjj1500_u": "1500 #leq M_{jj} #leq 2000 GeV",
                 "wcranti_mjj1000_u": "1000 #leq M_{jj} #leq 1500 GeV",
                 "wcranti_allmjj_u": "M_{jj} #geq 800 GeV"}

# Hardcoded labels for electron and muon regions.
process_labels = {"e": "W #rightarrow e#nu",
                  "u": "W #rightarrow #mu#nu"}

def compute_ratio(args, tfile, region):
    histname = os.path.join(region, "plotEvent_data", args.var)

    # TODO XXX: should we make this configurable?
    # Note: vvv seems no longer available by default in output ROOT file.
    # (it was a small contribution anyway...)
    valid_mcs = ["wewk", "wqcd", "zewk", "zqcd", "tall"]

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
    try:
        binomial_error = 1/(low+high) * math.sqrt(low * (1 - low/(low+high)))
    except ValueError:
        binomial_error = 0

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

    data_hist.GetXaxis().SetTitle(args.xlabel)
    data_hist.GetYaxis().SetTitle(args.ylabel)

    label = ROOT.ATLASLabel(0.66, 0.87, "Internal")

    # Get the text to use to describe this region/bin.
    # It could be hardcoded in the global dictionary region_labels (above).
    # Or it could be passed in on the CLI.
    region_text = args.text
    if region_text == "" and args.region in region_labels.keys():
        region_text = region_labels[args.region]

    # Also look up the process (this could be the W to mu nu CR!) and get
    # a human-readable description.
    # This is fragile.
    process_char = args.region[-1]
    try:
        process = process_labels[process_char]
    except KeyError:
        process = process_labels['e']

    # Dynamically relocate the legend depending on whether or not we have
    # text describing the selection region.
    lower_bound = 0.70
    if not region_text == "":
        lower_bound -= 0.04
    legend = ROOT.TLegend(0.66, lower_bound, 0.95, 0.85)

    # TODO: make energy, configurable...
    legend.AddEntry(0, "#sqrt{s} = " + args.energy + " TeV, " + args.lumi + " fb^{-1}", "")
    legend.AddEntry(0, process + ", Anti-ID", "")
    if not region_text == "":
        legend.AddEntry(0, region_text, "")
    legend.AddEntry(0, "Ratio: %0.2f #pm %0.2f" % (ratio, ratio_bin_error), "")
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetMargin(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.035)
    legend.SetTextFont(42)
    legend.Draw()

    output_name = "anti_id_template_" + region + ".eps"
    if args.name != "":
        output_name = args.name + "_" + output_name
    canvas.SaveAs(output_name)
    if args.wait:
        raw_input()

    return ratio, ratio_bin_error

def main():
    parser = argparse.ArgumentParser(description="A script to make template plots for lepton fake estimation.")

    # Main argument.
    parser.add_argument('filename', default="output.root", help="Output file from HInvPlot to run over.")

    # Various CLI options.
    parser.add_argument('-w', '--wait', action="store_true", dest="wait", help="Wait after drawing plot.")
    parser.add_argument('-n', '--name', dest="name", default="", help="The name of the plot to create.")
    parser.add_argument('-t', '--text', dest="text", default="", help="Text to put on the legend.")
    parser.add_argument('-r', '--region', dest="region", default="wcranti_allmjj_e", help="Region from HInvPlot to look at.")
    parser.add_argument('-v', '--var', dest="var", default="met_significance", help="Variable to plot.")
    parser.add_argument('-c', '--cutoff', dest="cutoff", default=40, type=int, help="Threshold value at which to take the ratio.")
    parser.add_argument('-b', '--rebin', dest="rebin", default=10, help="Number to rebin by when drawing the template shape plot.")
    parser.add_argument('-a', '--all', dest="all", action="store_true", help="Run estimate for all regions. Ignore -r.")
    parser.add_argument('-p', '--plusminus', dest="plusminus", action="store_true", help="Run estimate for ep and em regions too.")
    parser.add_argument('-l', '--lumi', dest="lumi", default="36.2", help="Integrated lumi (fb^-1) for datasets, defaults to 2015+16 lumi.")
    parser.add_argument('-e', '--energy', dest="energy", default="13", help="Energy (TeV) for datasets, defaults to 13 TeV.")

    parser.add_argument('--xlabel', dest="xlabel", default="MET Significance [GeV^{1/2}]", help="Label for x axis.")
    parser.add_argument('--ylabel', dest="ylabel", default="Events", help="Label for y axis.")
    parser.add_argument('-y', '--year', dest="year", default=2016, type=int, help="The year, will set lumi automatically.")

    # Load arguments.
    args = parser.parse_args()

    if args.year == 2017:
        args.lumi = '44.3'
    elif args.year == 2018:
        args.lumi = '58.5'

    # Read the file we passed to the script.
    filename = os.path.abspath(args.filename)
    tfile = ROOT.TFile(filename)
    keys = tfile.GetListOfKeys()

    if not args.all:
        region = "pass_" + args.region + "_Nominal"
        compute_ratio(args, tfile, region)

    # If the 'all' flag is passed, loop through the ROOT file.
    # Run this for all wcranti regions.
    else:
        ratios = collections.OrderedDict()
        maxlen = -1
        for key in keys:
            region = key.GetName()
            if "pass_wcranti" not in region:
                continue
            if not ('e_Nominal' in region):
                if not (args.plusminus and ('em_Nominal' in region or 'ep_Nominal' in region)):
                    continue
            print("Calculating estimate for region: " + region)
            ratio, ratio_error = compute_ratio(args, tfile, region)
            ratios[region] = (ratio, ratio_error)
            print("")
            if len(region) >= maxlen:
                maxlen = len(region)

        for name, (ratio, ratio_error) in ratios.iteritems():
            # I really should use new python string formatting for this.
            message = "%-" + str(maxlen) +  "s = %f +/- %f"
            print(message % (str(name), ratio, ratio_error))

if __name__ == '__main__':
    main()
