# used for ckkw and qsf

#################### Global settings
import math
import sys
import ROOT
import imp
import array
from ROOT import *
import AtlasStyle
gStyle.SetPaintTextFormat('1.3f')
gStyle.SetLineStyleString(11,"27 15")

suffix = sys.argv[1]
sherpa = imp.load_source("Sherpa_syst_"+suffix, "./python/Sherpa_syst_"+suffix+".py")

bins_mjj = ['800', '1000', '1500', '2000', '3500']
histobins = [800, 1000, 1500, 2000, 3500, 5000]
samples = ['Z_strong','W_strong']
regions = ['SR', 'CRZ', 'CRW', 'SRPhiHigh', 'CRZPhiHigh', 'CRWPhiHigh', 'SRPhiLow', 'CRZPhiLow', 'CRWPhiLow', 'SRNjet', 'CRZNjet', 'CRWNjet']
chosen_region = {'Z_strong':'SR','W_strong':'SR','Z_strong':'CRZ','W_strong':'CRW', 'Z_strong':'SRPhiHigh','W_strong':'SRPhiHigh','Z_strong':'CRZPhiHigh','W_strong':'CRWPhiHigh', 'Z_strong':'SRPhiLow','W_strong':'SRPhiLow','Z_strong':'CRZPhiLow','W_strong':'CRWPhiLow', 'Z_strong':'SRNjet','W_strong':'SRNjet','Z_strong':'CRZNjet','W_strong':'CRWNjet'}
samples_regions = ['Z_strong+SR', 'Z_strong+CRZ', 'W_strong+SR', 'W_strong+CRW', 'Z_strong+SRPhiHigh', 'Z_strong+CRZPhiHigh', 'W_strong+SRPhiHigh', 'W_strong+CRWPhiHigh', 'Z_strong+SRPhiLow', 'Z_strong+CRZPhiLow', 'W_strong+SRPhiLow', 'W_strong+CRWPhiLow', 'Z_strong+SRNjet', 'Z_strong+CRZNjet', 'W_strong+SRNjet', 'W_strong+CRWNjet']
#regions = ['SR','CRZ','CRW']
#chosen_region = {'Z_strong':'SR','W_strong':'SR','Z_strong':'CRZ','W_strong':'CRW'}
#samples_regions = ['Z_strong+SR','Z_strong+CRZ','W_strong+SR','W_strong+CRW']
#samples = ['Z_strong']
#regions = ['SR','CRZ']
#chosen_region = {'Z_strong':'SR','Z_strong':'CRZ'}
#samples_regions = ['Z_strong+SR','Z_strong+CRZ']
samples_regionsToRaw = samples_regions
samples_regionsToSmooth = samples_regions
samples_regionsToZero = samples_regions

colors = [kBlack, kRed+2, kBlue]
styles = [20,21,22,23]
####################


def getCKKWUnc(sample, region_mjj):
  ckkw15 = sherpa.evts[sample][region_mjj]['weight_ckkw15'][0]
  ckkw30 = sherpa.evts[sample][region_mjj]['weight_ckkw30'][0]
  ckkw15_var = ckkw15 - sherpa.evts[sample][region_mjj]['Nominal'][0]
  ckkw30_var = ckkw30 - sherpa.evts[sample][region_mjj]['Nominal'][0]

  ckkw = 0
  if (ckkw15!=0 and ckkw30!=0):
    ckkw = abs(ckkw15-ckkw30)/(ckkw15+ckkw30)

  return (ckkw15,ckkw30,ckkw15_var, ckkw30_var, ckkw)


def getQSFUnc(sample, region_mjj):
  qsf15 = sherpa.evts[sample][region_mjj]['weight_qsf025'][0]
  qsf30 = sherpa.evts[sample][region_mjj]['weight_qsf4'][0]
  qsf15_var = qsf15 - sherpa.evts[sample][region_mjj]['Nominal'][0]
  qsf30_var = qsf30 - sherpa.evts[sample][region_mjj]['Nominal'][0]

  qsf = 0
  if (qsf15!=0 and qsf30!=0):
    qsf = abs(qsf15-qsf30)/(qsf15+qsf30)

  return (qsf15,qsf30,qsf15_var, qsf30_var, qsf)

def getUncShape(samples, regions):
  mergedict = {}
  mergedictIncl = {}
  for sample in samples:
    mergedict[sample] = {}
    mergedictIncl[sample] = {}
    for region in regions:
      mergedictIncl[sample][region] = {}
      ckkw15_incl=0
      ckkw30_incl=0
      qsf15_incl=0
      qsf30_incl=0
      for bin_mjj in bins_mjj:
        region_mjj = region+'_'+bin_mjj
        mergedict[sample][region_mjj]={}
        source_sample = sample
        source_region_mjj = region_mjj
        nominal = sherpa.evts[source_sample][source_region_mjj]['Nominal'][0]
        if nominal == 0 or nominal<0:
          ckkw15=0
          ckkw30=0
          nominal = 1.
          ckkw=0
          qsf15=0
          qsf30=0
          qsf=0
          #print sample, region_mjj
        else:
          ckkw15,ckkw30,ckkw15_var,ckkw30_var,ckkw = getCKKWUnc(sample, region_mjj)
          qsf15,qsf30,qsf15_var,qsf30_var,qsf = getQSFUnc(sample, region_mjj)

        mergedict[sample][region_mjj]['ckkw15_RAW']=ckkw15
        mergedict[sample][region_mjj]['ckkw30_RAW']=ckkw30
        mergedict[sample][region_mjj]['ckkw15']=ckkw15_var/nominal
        mergedict[sample][region_mjj]['ckkw30']=ckkw30_var/nominal
        mergedict[sample][region_mjj]['ckkw']=ckkw

        mergedict[sample][region_mjj]['qsf15_RAW']=qsf15
        mergedict[sample][region_mjj]['qsf30_RAW']=qsf30
        mergedict[sample][region_mjj]['qsf15']=qsf15_var/nominal
        mergedict[sample][region_mjj]['qsf30']=qsf30_var/nominal
        mergedict[sample][region_mjj]['qsf']=qsf

        ckkw15_incl+=sherpa.evts[sample][region_mjj]['weight_ckkw15'][0]
        ckkw30_incl+=sherpa.evts[sample][region_mjj]['weight_ckkw30'][0]
        qsf15_incl+=sherpa.evts[sample][region_mjj]['weight_qsf025'][0]
        qsf30_incl+=sherpa.evts[sample][region_mjj]['weight_qsf4'][0]

      if (ckkw15_incl!=0 and ckkw30_incl!=0):
        mergedictIncl[sample][region]['ckkw'] = abs(ckkw15_incl-ckkw30_incl)/(ckkw15_incl+ckkw30_incl)
      if (qsf15_incl!=0 and qsf30_incl!=0):
         mergedictIncl[sample][region]['qsf'] = abs(qsf15_incl-qsf30_incl)/(qsf15_incl+qsf30_incl)

  return mergedict,mergedictIncl


def getUncShapeReduced(unc, samples, regions ):

  outunc = {}

  for sample,sampledict in unc.items():
    #print sample
    outunc[sample] = {}

    for region_mjj in sampledict.keys():
      mjj=region_mjj.split("_",1)[1];
      #print chosen_region, sample, mjj
      chosen_region_mjj = chosen_region[sample]+'_'+mjj
      outunc[sample][mjj]=sampledict[chosen_region_mjj]

  return outunc

def makeTableDict(mergedict, what='ckkw', nametable='ckkw_reduced_prelim'):

   f=open('python/{nametable}.py'.format(nametable=nametable), 'w')
   f.write('Sherpa_'+what+' = {}\n\n')

   for sample,sampledict in mergedict.items():
     f.write('Sherpa_'+what+'["{sample}"] = {{}}\n'.format(sample=sample))
     for region_mjj,regiondict in sampledict.items():
       f.write('Sherpa_'+what+'["{sample}"]["{region_mjj}"] = {{}}\n'.format(sample=sample,region_mjj=region_mjj))

       for unc,unc_value in regiondict.items():
         if what == unc:
           f.write('Sherpa_'+what+'["{sample}"]["{region_mjj}"]["{unc}"] = {unc_value}\n'.format(sample=sample,region_mjj=region_mjj, unc=unc, unc_value=round(unc_value,4)))

   f.close()

def makePlots(unc, NPs,NPRawLow,NPRawHigh, samples, regions):
  # plot the uncertainty vs mjj bins for each sample in each region do this for a given NP
  histo_saver = []

  for sample_region in samples_regions:
      sample,region = sample_region.split('+')
      print '***************************************'
      print 'Working on ', sample, 'region', region
      print '***************************************'

      name = '%s' % (sample_region)
      c = TCanvas(name, name, 600, 600)

      legend = TLegend(0.40,0.70,0.70,0.9,'')

      bins = array.array('d', histobins)
      bins_n = len(histobins)-1

      for j,NP in enumerate(NPs):
        namehisto = '{sample}_{region}_{np}'.format(sample=sample, region=region, np=NP)
        histo = TH1F(namehisto, namehisto, bins_n, bins)
        lowestSyst  = 9999
        highestSyst = -9999
        sys.stdout.write(str(sample))
        sys.stdout.write(' = ')
        sys.stdout.write('{')

        sys.stdout.write('\'')
        sys.stdout.write(str([region])[2 :-2: ])
        sys.stdout.write('\'')
        sys.stdout.write(': {')

        for i,bin_mjj in enumerate(bins_mjj):  # this is the binning of the fit,
          sys.stdout.write('"')
          sys.stdout.write(str(bin_mjj))
          sys.stdout.write('": ')
          if (str(sample)+'+'+str([region])[2 :-2: ] in samples_regionsToRaw):
            sys.stdout.write(str(unc[sample][region+'_'+bin_mjj][NP]))
            if lowestSyst > unc[sample][region+'_'+bin_mjj][NP]:
              lowestSyst = unc[sample][region+'_'+bin_mjj][NP]
            if highestSyst < unc[sample][region+'_'+bin_mjj][NP]:
              highestSyst = unc[sample][region+'_'+bin_mjj][NP]
          elif (str(sample)+'+'+str([region])[2 :-2: ] in samples_regionsToSmooth):
            totalRawLow=0
            totalRawHigh=0
            for i2,bin_mjj2 in enumerate(bins_mjj):  # this is the binning of the fit,
              totalRawLow += float(unc[sample][region+'_'+bin_mjj2]['ckkw15_RAW'])
              totalRawHigh+= float(unc[sample][region+'_'+bin_mjj2]['ckkw30_RAW'])
            smoothed = abs(totalRawLow-totalRawHigh)/(totalRawLow+totalRawHigh)
            sys.stdout.write(str(smoothed))
            lowestSyst = smoothed
            highestSyst = smoothed
          elif (str(sample)+'+'+str([region])[2 :-2: ] in samples_regionsToZero):
            sys.stdout.write('0')
            lowestSyst = 0
            highestSyst = 0
          if (i+1) != len(bins_mjj):
            sys.stdout.write(', ')

          histo.SetBinContent(i+1, unc[sample][region+'_'+bin_mjj][NP])

#          histo.Fit("pol1")
          histo.SetLineWidth(2)
          histo.SetLineColor(colors[j])
          histo.SetMarkerColor(colors[j])
          histo.SetMarkerStyle(styles[j])
          histo.SetTitle('{sample} {region}'.format(sample=sample, region=region))

          histo.GetXaxis().SetTitle('M_{jj} [GeV]')
          histo.GetXaxis().SetNdivisions(505, True)
          histo.GetYaxis().SetTitle('Relative uncertainty')
          histo.GetYaxis().SetRangeUser(0.0, 0.1)
        if j==0:
          print '}'
          histo.Draw('PhistL')
        else:
          histo.Draw('PhistsameL')
        legend.AddEntry(histo.GetName(),histo.GetName(), 'LP')
        histo_saver.append(histo)
        print '(Min-Highest)%',lowestSyst*100,'-',highestSyst*100
      histo_saver.append(legend)
      legend.Draw('same')
      c.SetGridy()
      c.SaveAs('systPlots/'+NP+'_'+sample+'_'+region+'_'+suffix+'.pdf')

def makeVariationPlots(samples, regions, variations, var_label):
  # plot the uncertainty vs mjj bins for each sample in each region do this for a given NP
  histo_saver = []

  for sample_region in samples_regions:
      sample,region = sample_region.split('+')
      print '***************************************'
      print 'Working on ', sample, 'region', region
      print '***************************************'
      name = '%s' % (sample_region)
      c = TCanvas(name, name, 600, 600)

      legend = TLegend(0.40,0.70,0.70,0.88,'')


      bins = array.array('d', histobins)
      bins_n = len(histobins)-1


      for j,NP in enumerate(variations):
        namehisto = '{sample}_{region}_{np}'.format(sample=sample, region=region, np=NP)
        print "namehisto: ", namehisto
        histo = TH1F(namehisto, namehisto, bins_n, bins)

        for i,bin_mjj in enumerate(bins_mjj):  # this is the binning of the fit,

          histo.SetBinContent(i+1, sherpa.evts[sample][region+'_'+bin_mjj][NP][0])
          histo.SetBinError(i+1, sherpa.evts[sample][region+'_'+bin_mjj][NP][1])

          #histo.Fit("pol1","same")
          histo.SetLineWidth(2)
          histo.SetLineColor(colors[j])
          histo.SetMarkerColor(colors[j])
          histo.SetMarkerStyle(styles[j])
          histo.SetTitle('{sample} {region}'.format(sample=sample, region=region))

          histo.GetXaxis().SetTitle('M_{jj} (GeV)')
          histo.GetXaxis().SetNdivisions(505, True)
          histo.GetYaxis().SetTitle('Events in 1/fb')

        if j==0:
          histo.Draw('PEhistL') # what uncertainty in each bin?
        else:
          histo.Draw('PEhistsameL')
        legend.AddEntry(histo.GetName(),NP, 'LP') #'m{} M{} g{} s{}'.format(im,iM,ig,isplit)
        histo_saver.append(histo)

      histo_saver.append(legend)
      legend.Draw('same')

      c.SetGridy()
      c.SetLogy()
      #c.SetLogx()
      c.SaveAs('variations/'+NP+'_'+sample+'_'+region+'_'+suffix+'_'+var_label+'.pdf')




def makePrintOut(unc, NPs, samples, regions):

    ### print out to see
    for sample in samples:
        for np in NPs:
          shape = []
          for bin_mjj in bins_mjj:
            region_mjj = bin_mjj
            shape.append(unc[sample][region_mjj][np])
            shape_strings = list(map(lambda x: '{:.1f}'.format(x*100), shape))
          #print sample, np, ' & '.join(shape_strings)

if __name__ == "__main__":

    print "starting to process...."
    unc,unc_incl = getUncShape(samples, regions)
    unc_reduced = getUncShapeReduced(unc, samples, regions)
    # ckkw
    makeTableDict(unc_reduced, what='ckkw',  nametable='ckkw_reduced_prelim')
    makePlots(unc, ['ckkw'], ['ckkw15_RAW'],['ckkw30_RAW'], samples, regions)
    makeVariationPlots(samples, regions, ['Nominal', 'weight_ckkw15', 'weight_ckkw30'],'ckkw')
    # qsf
    makeTableDict(unc_reduced, what='qsf',  nametable='qsf_reduced_prelim')
    makePlots(unc, ['qsf'], ['qsf15_RAW'],['qsf30_RAW'], samples, regions)
    makeVariationPlots(samples, regions, ['Nominal', 'weight_qsf025', 'weight_qsf4'],'qsf')

    for j,region in enumerate(['SR','CRW','CRZ']):
      for jj,updn in enumerate(['up','down']):
        print region+updn
        for i,NP in enumerate(['qsf','ckkw']):
          for l,sample in enumerate(['Z_strong','W_strong']):
            if sample == 'Z_strong' and region == 'CRW' or sample == 'W_strong' and region == 'CRZ':
              continue
            print NP+"_"+sample,
            for k,binn in enumerate(['PhiLow','PhiHigh']):
              for m,bin_mjj in enumerate(bins_mjj):
                if updn == 'up':
                  sys.stdout.write(str(round(1+unc[sample][region+binn+'_'+bin_mjj][NP],4))+",",)
                elif updn == 'down':
                  sys.stdout.write(str(round(1-unc[sample][region+binn+'_'+bin_mjj][NP],4))+",",)
            if updn == 'up':
              print round(1+unc_incl[sample][region][NP],4)
            elif updn == 'down':
              print round(1-unc_incl[sample][region][NP],4)
           # print ""

    for j,region in enumerate(['SR','CRW','CRZ']):
      for jj,updn in enumerate(['up','down']):
        print region+updn
        for l,sample in enumerate(['Z_strong','W_strong']):
          if sample == 'Z_strong' and region == 'CRW' or sample == 'W_strong' and region == 'CRZ':
            continue
          for k,binn in enumerate(['PhiLow','PhiHigh']):
            for i,NP in enumerate(['qsf','ckkw']):
              for m,bin_mjj in enumerate(bins_mjj):
                if updn == 'up':
                  sys.stdout.write(str(round(1+unc[sample][region+binn+'_'+bin_mjj][NP],4))+",",)
                elif updn == 'down':
                  sys.stdout.write(str(round(1-unc[sample][region+binn+'_'+bin_mjj][NP],4))+",",)
            if updn == 'up':
              print round(1+unc_incl[sample][region][NP],4)
            elif updn == 'down':
              print round(1-unc_incl[sample][region][NP],4)
           # print ""
outFile = TFile("test.root", "recreate")
