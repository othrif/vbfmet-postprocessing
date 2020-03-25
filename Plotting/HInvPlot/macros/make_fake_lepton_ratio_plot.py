#!/usr/bin/env python

# Arguments are always nice!
import argparse

# We need sorted dictionaries.
import collections

# Mathematics.
import math

# Use this as a crutch.
import uncertainties
from uncertainties import ufloat

import ROOT

# Stop ROOT from hijacking sys.argv.
ROOT.PyConfig.IgnoreCommandLineOptions = True

# Python 2/3 compat!
import six

ROOT.gROOT.LoadMacro("AtlasStyle.C")
ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()
#ROOT.gStyle.SetErrorX(0.1)

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen]

mjj_bin_labels = {0: "All",
                  1: "#it{N}_{jets} #geq 3",
                  800.0: "#it{m}_{jj} 0.8-1 TeV",
                  1000.0: "#it{m}_{jj} 1-1.5 TeV",
                  1500.0: "#it{m}_{jj} 1.5-2 TeV",
                  2000.0: "#it{m}_{jj} 2-3.5 TeV",
                  3500.0: "#it{m}_{jj} > 3.5 TeV"}

dphi_bin_labels = {1.0: "0 < #Delta #phi_{jj} < 1",
                   2.0: "1 < #Delta #phi_{jj} < 2",}

leppt_bin_labels = {"low": "p_{T}(e) < 150 GeV",
                    "high": "p_{T}(e) > 150 GeV"}

yaxis_labels = {"ratio": "#it{R_{S}}",
                "invratio": "Inverse Ratio, E_{T}^{miss} sig. = 4 GeV^{1/2}",
                "low": "Events, E_{T}^{miss} sig. < 4 GeV^{1/2}",
                "high": "Events, E_{T}^{miss} sig. > 4 GeV^{1/2}"}

# Different markers for each series.
markers = [ROOT.kFullTriangleDown, ROOT.kFullTriangleUp, ROOT.kFullDiamond]

def calculate_ratio(low, high, binomial=False, invert=False):
    low_n = low.n
    low_err = low.s
    high_n = high.n
    high_err = high.s

    uratio = low / high

    n = low_n + high_n
    ratio = low_n / high_n
    ratio_error = uratio.s

    if binomial:
        binom_error = 1/n * math.sqrt(math.fabs(low_n * (1 - low_n/n)))
        ratio_error = binom_error * math.fabs(1 / (1-low_n/n)**2)

    # Ignore binomial option from now on.
    if invert:
        ratio = high_n / low_n
        ratio_error = (high / low).s

    return ratio, ratio_error

def make_graph(data, xlabel, legend_label, legend_header, bin_labels, filename, args, min_ratio, max_ratio):
    canvas_name, _, _ = filename.partition(".")
    canvas = ROOT.TCanvas(canvas_name, canvas_name, 800, 600)
    outer_count = 0

    hists = collections.OrderedDict()

    ROOT.gStyle.SetPalette(eval(args.style))

    data["Combined"] = collections.OrderedDict()

    if args.invert:
        min_ratio = -0.3
        max_ratio = 1.25

    # At every iteration make a new histogram.
    for name, dataset in six.iteritems(data):
        hist_name = "hist_" + canvas_name + "_" + str(name)
        hist = ROOT.TH1F(hist_name, hist_name, len(dataset), 0, len(dataset))
        count = 1

        # Now loop through the actual dataset.
        for bin_name, (low, high) in six.iteritems(dataset):
            hist.GetXaxis().SetBinLabel(count, bin_labels[bin_name])

            # Compute ratio. Or not!
            if args.var == "low":
                ratio = low.n
                ratio_error = low.s
            elif args.var == "high":
                ratio = high.n
                ratio_error = high.s
            else:
                ratio, ratio_error = calculate_ratio(low, high, binomial=args.binomial, invert=args.invert)

            hist.SetBinContent(count, ratio)
            hist.SetBinError(count, ratio_error)

            if name != "Combined":
                if bin_name not in data["Combined"]:
                    data["Combined"][bin_name] = (low, high)
                else:
                    cur_low, cur_high = data["Combined"][bin_name]
                    data["Combined"][bin_name] = (low + cur_low, high + cur_high)

            if name == "Combined":
                print("Ratio (%s) = %f /- %f" % (str(bin_name), ratio, ratio_error))

            count += 1

            if not args.invert:
                max_ratio = math.ceil(max(max_ratio, ratio))

            if not args.invert:
                min_ratio = math.floor(min(min_ratio, ratio))

        # this is, uh, a hack.
        for _, oldhist in six.iteritems(hists):
            oldhist.GetYaxis().SetRangeUser(min_ratio, max_ratio*1.05)

        canvas.cd()
        draw_opts = "pe0 plc pmc"
        if outer_count != 0:
            draw_opts += " same"

        hist.Draw(draw_opts)

        # Set the marker.
        # For the combined: use the circle, make it a bit bigger.
        # Otherwise: use a different marker for each set.
        if name == "Combined":
            hist.SetMarkerSize(1.5)
        elif outer_count < len(markers):
            hist.SetMarkerStyle(markers[outer_count])
            if markers[outer_count] == ROOT.kFullDiamond:
                hist.SetMarkerSize(1.3)

        varname = args.var
        if not args.invert:
            varname = "inv" + varname

        offset = 0.05*hist.GetBinWidth(1)*outer_count
        hist.GetXaxis().SetLimits(-2+offset, 2+offset)
        hist.GetXaxis().SetNdivisions(len(dataset), 0, 0, False)
        hist.GetXaxis().SetTitle(xlabel)
        hist.GetYaxis().SetTitle(yaxis_labels[varname])
        hist.GetXaxis().SetLabelSize(0.048)

        hist.GetYaxis().SetRangeUser(min_ratio, max_ratio)

        outer_count += 1

        canvas.Update()
        hists[name] = hist

    xcoord = 0.70

    xcoord2 = 0.90
    if args.invert and len(dataset) > 3:
        xcoord2 -= 0.50
        xcoord -= 0.50

    legend = ROOT.TLegend(xcoord - 0.01, 0.78 - .05*len(hists), xcoord2, 0.87)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    # I _really_ don't understand ROOT font sizes!
    legend.SetTextSize(0.04)
    legend.SetTextFont(42)
    legend.SetHeader(legend_header)

    label_coord = xcoord - 0.01
    if not args.invert:
        label_coord -= 0.04
    label = ROOT.ATLASLabel(label_coord, 0.88, "Internal")

    for name, hist in six.iteritems(hists):
        if name == "Combined":
            legend.AddEntry(hist, "Combined")
        elif type(name) == str and "ep" in name:
            legend.AddEntry(hist, "W #rightarrow e^{+} #nu")
        elif type(name) == str and "em" in name:
            legend.AddEntry(hist, "W #rightarrow e^{-} #nu")
        elif type(name) == str and "low" in name:
            legend.AddEntry(hist, "p_{T}(e) < 150 GeV")
        elif type(name) == str and "high" in name:
            legend.AddEntry(hist, "p_{T}(e) > 150 Gev")
        else:
            legend_name = str(int(name))
            if legend_name == '2016':
                legend_name = '2015+2016'
            legend.AddEntry(hist, legend_label + legend_name)

    legend.Draw()

    canvas.Update()
    if args.wait:
        six.moves.input()
    canvas.SaveAs(filename)
    canvas.SaveAs(filename.replace("eps", "C"))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="CSV file to parse.")
    parser.add_argument('-w', '--wait', action="store_true", dest="wait",help="Wait after making plots.")
    parser.add_argument('-s', '--style', default="ROOT.kDarkRainBow", dest="style", help="ROOT style to use for plotting.")
    parser.add_argument('-y', '--year', default=None, dest="year", type=int, help="Only look at a specific year.")
    parser.add_argument('-b', '--binomial', dest="binomial", action="store_true", help="Use binomial errors to calculate ratio.")
    parser.add_argument('-v', '--var', dest="var", default="ratio", help="Variable to plot.")
    parser.add_argument('-z', '--zero', dest="zero", action="store_true", help="Round negative fluctuations to zero.")
    parser.add_argument('--plusminus', dest="plusminus", action="store_true", help="Use plus/minus, look at channel.")
    parser.add_argument('--leppt', dest="leppt", action="store_true", help="Look for lepton pt binning.")
    parser.add_argument('-i', '--invert', dest="invert", action="store_true", help="Invert ratios when making plot.")
    args = parser.parse_args()

    # Make a ttree from the fake lepton CSV file.
    tree = ROOT.TTree("tree", "tree")
    tree.ReadFile(args.filename)

    dphi_eliminated = collections.OrderedDict()
    mjj_eliminated = collections.OrderedDict()
    year_eliminated = collections.OrderedDict()
    year_eliminated_mjj = collections.OrderedDict()

    epm_mjj = collections.OrderedDict()

    leppt_mjj = collections.OrderedDict()
    leppt_mjj_inverse = collections.OrderedDict()

    zero = ufloat(0, 0)

    # Given how few entries there are, this sort of iteration is fine.
    for event in tree:
        # Skip "allmjj" and "njets >= 2" for now.
        if "allmjj" not in tree.region: # and "njgt2" not in tree.region:
            low = ufloat(tree.low, tree.lowerr)
            high = ufloat(tree.high, tree.higherr)

            if args.zero:
                low = max(zero, low)
                high = max(zero, high)

            # Eliminate delta phi. Create dictionary binned in year[mjj].
            if tree.year not in dphi_eliminated:
                dphi_eliminated[tree.year] = collections.OrderedDict()
            if tree.mjj not in dphi_eliminated[tree.year]:
                dphi_eliminated[tree.year][tree.mjj] = (low, high)
            else:
                cur_low, cur_high = dphi_eliminated[tree.year][tree.mjj]
                dphi_eliminated[tree.year][tree.mjj] = (low + cur_low, high + cur_high)

            # Eliminate mjj. Create dictionary binned in year[dphi].
            if tree.year not in mjj_eliminated:
                mjj_eliminated[tree.year] = collections.OrderedDict()
            if tree.dphijj not in mjj_eliminated[tree.year]:
                mjj_eliminated[tree.year][tree.dphijj] = (low, high)
            else:
                cur_low, cur_high = mjj_eliminated[tree.year][tree.dphijj]
                mjj_eliminated[tree.year][tree.dphijj] = (low + cur_low, high + cur_high)

            # optional: only look at a specific year in these plots.
            if args.year != None and args.year != tree.year:
                continue

            # Eliminate year. Create dictionary binned in dphi[mjj] and mjj[dphi].
            if tree.dphijj not in year_eliminated:
                year_eliminated[tree.dphijj] = collections.OrderedDict()
            if tree.mjj not in year_eliminated_mjj:
                year_eliminated_mjj[tree.mjj] = collections.OrderedDict()

            if tree.mjj not in year_eliminated[tree.dphijj]:
                year_eliminated[tree.dphijj][tree.mjj] = (low, high)
            else:
                cur_low, cur_high = year_eliminated[tree.dphijj][tree.mjj]
                year_eliminated[tree.dphijj][tree.mjj] = (low + cur_low, high + cur_high)

            if tree.dphijj not in year_eliminated_mjj[tree.mjj]:
                year_eliminated_mjj[tree.mjj][tree.dphijj] = (low, high)
            else:
                cur_low, cur_high = year_eliminated_mjj[tree.mjj][tree.dphijj]
                year_eliminated_mjj[tree.mjj][tree.dphijj] = (low + cur_low, high + cur_high)

            # Parse channel.
            if args.plusminus and not ord(tree.channel[1]) == 0:
                if tree.channel not in epm_mjj:
                    epm_mjj[tree.channel] = collections.OrderedDict()
                if tree.mjj not in epm_mjj[tree.channel]:
                    epm_mjj[tree.channel][tree.mjj] = (low, high)
                else:
                    cur_low, cur_high = epm_mjj[tree.channel][tree.mjj]
                    epm_mjj[tree.channel][tree.mjj] = (low + cur_low, high + cur_high)

            # Parse "leppt".
            if args.leppt and "leppt" in tree.region:
                leppt_cut = "low"
                if "high" in tree.region:
                    leppt_cut = "high"
                if leppt_cut not in leppt_mjj:
                    leppt_mjj[leppt_cut] = collections.OrderedDict()
                if tree.mjj not in leppt_mjj[leppt_cut]:
                    leppt_mjj[leppt_cut][tree.mjj] = (low, high)
                else:
                    cur_low, cur_high = leppt_mjj[leppt_cut][tree.mjj]
                    leppt_mjj[leppt_cut][tree.mjj] = (low + cur_low, high + cur_high)

                if tree.mjj not in leppt_mjj_inverse:
                    leppt_mjj_inverse[tree.mjj] = collections.OrderedDict()
                if leppt_cut not in leppt_mjj_inverse[tree.mjj]:
                    leppt_mjj_inverse[tree.mjj][leppt_cut] = (low, high)
                else:
                    cur_low, cur_high = leppt_mjj_inverse[tree.mjj][leppt_cut]
                    leppt_mjj_inverse[tree.mjj][leppt_cut] = (low + cur_low, high + cur_high)

    year_label = "All Years"
    year_name = "year_eliminated.eps"
    if args.year != None:
        year_label = str(args.year) + " Only"
        year_name = "year_" + str(args.year) + ".eps"

    # Now make plots, with each variable eliminated!
    if args.plusminus:
        make_graph(epm_mjj, "Bins", "Charge: ", "36.1 fb^{-1}", mjj_bin_labels, args.var + "_epm.eps", args, -5, 30)
    if args.leppt:
        make_graph(leppt_mjj, "#it{m}_{jj} Bin [GeV]", "Lepton p_{T}", "36.1 fb^{-1}", mjj_bin_labels, args.var + "_leppt.eps", args, -5, 30)
        make_graph(leppt_mjj_inverse, "Lepton p_{T} Bin [GeV]", "m_{jj} Bin: ", "36.1 fb^{-1}", leppt_bin_labels, args.var + "_leppt_inverse.eps", args, -5, 30)
    else:
        make_graph(dphi_eliminated, "Bins", "Year: ", "0 < #Delta #it{#phi}_{jj} < 2", mjj_bin_labels, args.var + "_" + "fake_electron_mjj_dependence.eps", args, -5, 30)
        make_graph(mjj_eliminated, "#Delta #phi_{jj} Bin", "Year: ", "All m_{jj} Bins", dphi_bin_labels, args.var + "_" + "mjj_eliminated.eps", args, -5, 30)
        make_graph(year_eliminated, "#it{m}_{jj} Bin [GeV]", "#Delta #phi_{jj} Bin ", year_label, mjj_bin_labels, args.var + "_" + "dphi_" + year_name, args, -5, 30)
        make_graph(year_eliminated_mjj, "#Delta #phi_{jj} Bin", "m_{jj} Bin: ", year_label, dphi_bin_labels, args.var + "_" + "mjj_" + year_name, args, -5, 30)

if __name__ == '__main__':
    main()
