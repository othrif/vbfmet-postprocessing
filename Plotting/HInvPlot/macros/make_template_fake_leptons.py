#!/usr/bin/env python

# A script to make template plots for lepton fake estimation.
# This version is intended to run on the output ROOT files and histograms
# from HInvPlot.
# Ben Rosser <bjr@sas.upenn.edu>

import array
import collections
import csv
import math
import os
import string
import sys

import ROOT

# Stop ROOT from hijacking sys.argv.
ROOT.PyConfig.IgnoreCommandLineOptions = True

code = ROOT.gROOT.LoadMacro("AtlasStyle.C")
code = ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()

import argparse

# The uncertainties package provides for error propagation.
# needs to be installed by hand: "pip install --user uncertainties"
# after setting up a release.
import uncertainties

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

tex_region_labels = {
    "allmjj": "M_{jj} > \unit[800]{GeV}",
    "mjj800dphijj1nj2": r"800 < m_{jj} < \unit[1000]{GeV}, \Delta \phi_{jj} < 1",
    "mjj1000dphijj1nj2": r"1000 < m_{jj} < \unit[1500]{GeV}, \Delta \phi_{jj} < 1",
    "mjj1500dphijj1nj2": r"1500 < m_{jj} < \unit[2000]{GeV}, \Delta \phi_{jj} < 1",
    "mjj2000dphijj1nj2": r"2000 < m_{jj} < \unit[3500]{GeV}, \Delta \phi_{jj} < 1",
    "mjj3500dphijj1nj2": r"m_{jj} > \unit[3500]{GeV}, \Delta \phi_{jj} > 1",
    "mjj800dphijj2nj2": r"800 < m_{jj} < \unit[1000]{GeV}, \Delta \phi_{jj} > 1",
    "mjj1000dphijj2nj2": r"1000 < m_{jj} < \unit[1500]{GeV}, \Delta \phi_{jj} > 1",
    "mjj1500dphijj2nj2": r"1500 < m_{jj} < \unit[2000]{GeV}, \Delta \phi_{jj} > 1",
    "mjj2000dphijj2nj2": r"2000 < m_{jj} < \unit[3500]{GeV}, \Delta \phi_{jj} > 1",
    "mjj3500dphijj2nj2": r"m_{jj} > \unit[3500]{GeV}, \Delta \phi_{jj} > 1",
    "njgt2": r"N_\text{jets} > 2"
                    }

# Hardcoded labels for electron and muon regions.
process_labels = {"e": "W #rightarrow e#nu",
                  "ep": "W #rightarrow e^{+}#nu",
                  "em": "W #rightarrow e^{-}#nu",
                  "u": "W #rightarrow #mu#nu"}

def parse_cut(cutstring):
    mjj_cut = ''
    dphi_cut = ''
    njet_cut = 'gt2'

    if 'mjj' in cutstring:
        cutstring = cutstring[cutstring.find("mjj") + len("mjj"):]
        if len(cutstring) != 0:
            while cutstring[0] in string.digits:
                mjj_cut += cutstring[0]
                cutstring = cutstring[1:]

    if 'dphijj' in cutstring:
        cutstring = cutstring[cutstring.find("dphijj") + len("dphijj"):]
        if len(cutstring) != 0:
            while cutstring[0] in string.digits:
                dphi_cut += cutstring[0]
                cutstring = cutstring[1:]

    # this one is a bit more hardcoded.
    if 'nj' in cutstring:
        njet_cut = cutstring[cutstring.find("nj") + len("nj"):]

    if mjj_cut == '':
        mjj_cut = '800'
    if dphi_cut == '':
        dphi_cut = '2'

    return mjj_cut, dphi_cut, njet_cut

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

    if args.avg:
        mean = data_hist.GetMean()
        mean_error = data_hist.GetMeanError()
        print("Average value in bin " + str(region) +  " = " + str(mean) + " +/- " + str(mean_error))

    # Integrate from 0 to 4 and retrieve the integrated error.
    low_error = ROOT.Double()
    low = data_hist.IntegralAndError(0, args.cutoff, low_error)

    # Integrate from 4 and above (bin 5+) and retrieve the integrated error.
    high_error = ROOT.Double()
    high = data_hist.IntegralAndError(args.cutoff + 1, data_hist.GetNbinsX()+2, high_error)

    ulow = uncertainties.ufloat(low, low_error)
    uhigh = uncertainties.ufloat(high, high_error)

    try:
        ratio = (ulow / uhigh).n
        ratio_error = (ulow / uhigh).s
    except:
        ratio = 0.0
        ratio_error = 0.0

    if args.invert:
        try:
            ratio = (uhigh / ulow).n
            ratio_error = (uhigh / ulow).s
        except:
            ratio = 0.0
            ratio_error = 0.0

    print("")
    if data_hist.GetBinContent(0) != 0:
        print("Below 0 = %f +/- %f" % (data_hist.GetBinContent(0), data_hist.GetBinError(0)))

    print("Below 4 = %f +/- %f" % (low, low_error))
    print("Above 4 = %f +/- %f" % (high, high_error))
    print("Ratio = %f +/- %f" % (ratio, ratio_error))
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
    process_char = args.region.split("_")[-1]
    try:
        process = process_labels[process_char]
    except KeyError:
        process = process_labels['e']

    # Dynamically relocate the legend depending on whether or not we have    # text describing the selection region.
    lower_bound = 0.70
    if not region_text == "":
        lower_bound -= 0.04
    legend = ROOT.TLegend(0.66, lower_bound, 0.95, 0.85)

    # TODO: make energy, configurable...
    legend.AddEntry(0, "#sqrt{s} = " + args.energy + " TeV, " + args.lumi + " fb^{-1}", "")
    legend.AddEntry(0, process + ", Anti-ID", "")
    if not region_text == "":
        legend.AddEntry(0, region_text, "")
    legend.AddEntry(0, "Ratio: %0.2f #pm %0.2f" % (ratio, ratio_error), "")
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

    # This is a bit of a mess.
    return ratio, ratio_error, low, low_error, high, high_error

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
    parser.add_argument('-c', '--cutoff', dest="cutoff", default=4, type=int, help="Threshold value at which to take the ratio.")
    parser.add_argument('-b', '--rebin', dest="rebin", default=1, type=int, help="Number to rebin by when drawing the template shape plot.")
    parser.add_argument('-a', '--all', dest="all", action="store_true", help="Run estimate for all regions. Ignore -r.")
    parser.add_argument('-p', '--plusminus', dest="plusminus", action="store_true", help="Run estimate for ep and em regions too.")
    parser.add_argument('-l', '--lumi', dest="lumi", default="36.2", help="Integrated lumi (fb^-1) for datasets, defaults to 2015+16 lumi.")
    parser.add_argument('-e', '--energy', dest="energy", default="13", help="Energy (TeV) for datasets, defaults to 13 TeV.")

    parser.add_argument('--xlabel', dest="xlabel", default="MET Significance [GeV^{1/2}]", help="Label for x axis.")
    parser.add_argument('--ylabel', dest="ylabel", default="Events", help="Label for y axis.")
    parser.add_argument('-y', '--year', dest="year", default=2016, type=int, help="The year, will set lumi automatically.")

    parser.add_argument('-o', '--output', dest="output", default="fake_leptons.csv", help="CSV file containing output fake lepton info.")

    parser.add_argument('--avg', action="store_true", dest="avg", help="Only print average values after subtracting MC; do nothing else.")
    parser.add_argument('-i', '--invert', action="store_true", dest="invert", help="Invert the ratio to be high/low instead of low/high.")

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
        lows = collections.OrderedDict()
        highs = collections.OrderedDict()
        maxlen = -1
        for key in keys:
            region = key.GetName()
            if "pass_wcranti" not in region:
                continue
            if not ('e_Nominal' in region):
                if not (args.plusminus and ('em_Nominal' in region or 'ep_Nominal' in region)):
                    continue
            print("Calculating estimate for region: " + region)

            # This is kind of ugly.
            args.region = region[len("pass_"):-len("_Nominal")]

            ratio, ratio_error, low, low_error, high, high_error = compute_ratio(args, tfile, region)
            lows[region] = (low, low_error)
            highs[region] = (high, high_error)
            ratios[region] = (ratio, ratio_error)

            print("")
            if len(region) >= maxlen:
                maxlen = len(region)

        for name, (ratio, ratio_error) in ratios.iteritems():
            # I really should use new python string formatting for this.
            if ratio == -1:
                message = "%-" + str(maxlen) +  "s = 0 (Error)"
                print(message % str(name))
            else:
                message = "%-" + str(maxlen) +  "s = %f +/- %f"
                print(message % (str(name), ratio, ratio_error))

        # Write out CSV record.
        csvname = args.output.replace(".csv", "_" + str(args.year) + ".csv")
        with open(csvname, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            # So ROOT can parse this later.
            writer.writerow(["region/C","channel/C","mjj/F","dphijj/F","njets/C","year/F","low","lowerr","high","higherr","ratio","ratioerr"])

            # Print tex output too.
            print("")
            print("Bin & Events $ < \unit[4]{\sqrt{GeV}} $ & Events $ > \unit[4]{\sqrt{GeV}} $ & Ratio \\\\ ")
            print("\hline")
            for name, (ratio, ratio_error) in ratios.iteritems():
                low, low_error = lows[name]
                high, high_error = highs[name]
                # TODO: Replace name with tex-friendly string.
                try:
                    split_name = name.split('_')
                    region = split_name[2]
                    channel = split_name[3]
                    message = "$ " + tex_region_labels[region]
                    if 'p' in channel:
                        message += ", " + channel[0] + "^+"
                    elif 'm' in channel:
                        message += ", " + channel[0] + "^-"
                    message += " $ "
                except KeyError:
                    message = name.replace("_", "\\_")
                message += " & $ \\num{" + str(low) + "} \pm \\num{" + str(low_error) + "} $ &"
                message += " $ \\num{" + str(high) + "} \pm \\num{" + str(high_error) + "} $ & "
                if ratio != -1:
                    message += "$ \\num{" + str(ratio) + "} \pm \\num{" + str(ratio_error) + "} $ "
                message += "  \\\\ "
                print(message)

                # Write to CSV.
                mjj_cut, dphi_cut, njet_cut = parse_cut(region)
                writer.writerow([region, channel, mjj_cut, dphi_cut, njet_cut, args.year, low, low_error, high, high_error, ratio, ratio_error])

if __name__ == '__main__':
    main()
