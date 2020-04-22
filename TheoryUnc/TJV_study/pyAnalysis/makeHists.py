import json
import ROOT
import os
from array import array
import argparse

from helper import HistEntry

parser = argparse.ArgumentParser(description='Author: O. Rifki')
parser.add_argument('files', type=str, nargs='+', metavar='<file.root>', help='ROOT files containing the jigsaw information. Histograms will be drawn and saved in the file.')
parser.add_argument('--config', required=True, type=str, dest='config', metavar='<file.json>', help='json file containing configurations for making histograms')
parser.add_argument('--out_tdirectory', required=False, type=str, dest='outdir', metavar='', help='TDirectory to store all generated histograms', default='all')
parser.add_argument('--treename', required=False, type=str, dest='treename', metavar='', help='Tree containing the ntuple information', default='oTree')
parser.add_argument('--eventWeight', required=False, type=str, dest='eventWeightBranch', metavar='', help='Event Weight Branch name', default='weight')
parser.add_argument('--newOutputs', action='store_true', default=False, help='create new output files for histograms')
parser.add_argument('--name', required=False, type=str, dest='name', metavar='', help='Suffix to add to histogram name', default='')


# parse the arguments, throw errors if missing any
args = parser.parse_args()

config = json.load(file(args.config))

for f in args.files:
  print "opening {0}".format(f)
  if args.newOutputs:
    in_file = ROOT.TFile.Open(f, "READ")
    out_file = ROOT.TFile.Open(os.path.join(os.path.dirname(f), "hists_{1:s}{0:s}".format(os.path.basename(f),args.name)), "RECREATE")
    tree = in_file.Get(args.treename)
  else:
    out_file = ROOT.TFile.Open(f, "UPDATE")
    tree = out_file.Get(args.treename)
  # create tdirectory and cd into it
  print "\tmaking tdirectory {0}".format(args.outdir)

  # for each thing to draw, we want to apply a selection on them too
  for cut in config['cuts']:
    innerDir = os.path.join(args.outdir, cut['name'])
    #print "{0}={1}+{2}".format(innerDir, args.outdir, cut['name'])
    try: out_file.rmdir(innerDir)
    except: pass
    try: out_file.rm(innerDir)
    except: pass
    try: out_file.mkdir(innerDir)
    except: pass
    try: out_file.cd(innerDir)
    except: pass
    # get list of things to draw
    for toDraw in config['draw']:
      histName = toDraw['name']
      histDimension = len(toDraw['draw'].split(':'))
      if "nbins" in toDraw:
        print "\tmaking {4}D histogram {0}\n\t{1} bins from {2} to {3}".format(toDraw['name'], toDraw['nbins'], toDraw['min'], toDraw['max'], histDimension)
        if histDimension == 1:
          h = ROOT.TH1F(histName,histName,toDraw['nbins'], toDraw['min'], toDraw['max'])
        else:
          raise ValueError('Not handling higher dim for now {0}'.format(toDraw))
      elif "edges" in toDraw:
        print "\tmaking {1}D histogram with bin edges: {0}".format(toDraw['edges'], histDimension)
        if histDimension == 1:
          h = ROOT.TH1F(histName,histName,len(toDraw['edges'])-1,array('d',toDraw['edges']))
        else:
          raise ValueError('Not handling higher dim for now {0}'.format(toDraw))
      else:
        print "ERROR: problem configuring the binning of the histograms..."
        exit()

      # things look ok, so we draw to the histogram
      print "\t\tdrawing {0}\n\t\twith cut ({1})*({2})".format(toDraw['draw'], args.eventWeightBranch, cut['name'])

      tree.Draw(toDraw['draw'] + ' >> ' + histName, '({0:s})*({1:s})'.format(args.eventWeightBranch, cut['cut']) )
      samename=h.GetName()
      hnew = HistEntry(h, histName)
      hnew=hnew.merge_bins() # merge upper overflow bin
      hnew.SetName(samename)
      # write to file
      print "\t\twriting to file"
      hnew.Write()

  out_file.Close()
