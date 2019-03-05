# Setup

To set up the plotting code, run:

```
source setup.sh

rc clean
rc find_packages
rc compile
```

# place the ntuples into a line separated text file
#ls /afs/cern.ch/user/r/rzou/workspace/public/STPostProcessing/run/newmicro/microtuples/* &> input.txt
cp -rf /eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v20 /tmp/v20
ls /tmp/v20/* &> input.txt

NOTE: data is not blinded in this setup. So comment it out in the input file.

To plot run:
```
python HInvPlot/macros/plotEvent.py -i input.txt 
```

You must specify the year for 2017 and 2018 to set the right triggers and the lumi. Lumi for 2018 is 59937:
```
python HInvPlot/macros/plotEvent.py  -i v27Loose.txt  -r /tmp/v27Loose.root  --r207Ana  --year 2017 --OverlapPh  --int-lumi 44307.4
```

To add new variables, you must add them to Root/VarEvent.cxx and its header. The binning is defined in python/Vars.py. If you want to create a variable from the existing information, then you also need to fill it in Root/ReadEvent.cxx. Follow an example like mll.

Variables can then be plotted from the output file:

```
python HInvPlot/macros/drawStack.py out.root --vars ptll  --selkey pass_zcr_allmjj_ll --wait --do-pdf --save 
```

Notes:

* --draw-syst can be added if you ran over the systematics
* --selkey is the region that you are plotting. for example, pass_zcr_allmjj_ll this is the Z control region with Mjj>1 Tev and two opposite sign leptons (e or mu)
* It's recommended to copy the micro-ntuples to the tmp space instead of eos. eos has a very slow I/O.

# Documentation

## Adding Variables

To add a variable to a jet, muon, electron, tau or photon, please follow these instructions:
Copy the jet_fjvt vector to read in new jet variables:
https://gitlab.cern.ch/VBFInv/STPostProcessing/blob/master/Plotting/HInvPlot/Root/ReadEvent.cxx#L645

Create a new variable name in the name space for your new variable. For exmaple you can copy fjvt:
https://gitlab.cern.ch/VBFInv/STPostProcessing/blob/master/Plotting/HInvPlot/Root/VarEvent.cxx#L92

Draw the histogram. Again you can follow the fjvt example: 
https://gitlab.cern.ch/VBFInv/STPostProcessing/blob/master/Plotting/HInvPlot/Root/PlotEvent.cxx

add x label, etc:
https://gitlab.cern.ch/VBFInv/STPostProcessing/blob/master/Plotting/HInvPlot/macros/drawStack.py#L188

## Load Base Leptons

You can load the base leptons in place of the signal leptons by passing the option --LoadBaseLep
when running plotEvent.py. This loads the baseline leptons into the signal lepton collection.
It does not change n_mu nor n_el though, so these can still be used for the selection of not-signal
leptons using  n_basemu==0 && n_baseel==1 && n_el==0 && trigger_lep>0.

## Condor

Drawing the systematics can be time consumming, so it is possible to submit them to a condor batch
python HInvPlot/macros/submitPlotEventCondor.py -i /home/schae/testarea/HInv/source/Plotting/v26.txt

## Fake Lepton Estimate

To run the fake lepton estimate, you can pass ```--region wcranti``` to
plotEvent.py. This will produce output histograms in the WCR anti-ID regions
(with both electrons and muons).

Once you have an output file with wcranti regions, you can run the fake
lepton estimate using the following script:

```
./HInvPlot/macros/make_template_fake_leptons.py out.root -a
```

Passing the -a switch will calculate the ratio of events in the anti-ID
region which have MET significance below/above 4 sqrt(GeV) for all wcranti
electron regions. The ratio is computed by taking the data events and
subtracting off the following MC background histograms:

* W+Jets ('wqcd' and 'wewk')
* Z+Jets ('zqcd' and 'zewk')
* ttbar ('top2')
* Multiboson ('vvv')

The list of histograms used is hardcoded in the script, but most everything
else can be configured, including:

* The threshold at which the ratio is computed; it can be adjusted by passing
```-c [cutoff]``` in units of 1/10 sqrt(GeV) (so, the default is 40, not 4).

* The variable used to compute the ratio; so, it could be adjusted to use
object-based MET sigificance by passing ```-v metsig_tst```.

* Whether or not to compute the ratio separately for the ep and em bins;
this is done if the switch ```-p``` is added.

Run with ```-h``` to see the full list of options.
