# Setup

To set up the plotting code, run:

```
source setup.sh

rc clean
rc find_packages
rc compile
```

Then, copy the ntuples from eos to a local directory, and put
a list of their names into a newline separated text file. For instance,
to copy the v20 ntuples:

```
cp -rf /eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v20 /tmp/v20
ls /tmp/v20/* &> input.txt
```

NOTE: data is not blinded in this setup. So comment it out in the input file.

To plot, run:

```
python HInvPlot/macros/plotEvent.py -i input.txt 
```

You must specify the year for 2017 and 2018 to set the right triggers and the lumi. Lumi for 2018 is 58450.1:
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


==========

Options for SFs:
nohup python HInvPlot/macros/plotEvent.py  -i v34ALooseMETPassThru.txt   -r v34ALooseMETPassThru_ktmerge.root     --mergeKTPTV -a metsf &> /tmp/logMETSFAKT &
nohup python HInvPlot/macros/plotEvent.py  -i v34ALooseMETPassThru.txt   -r v34ALooseMETPassThru_noktmerge.root      -a metsf &> /tmp/logMETSFAnoKT &

nohup python HInvPlot/macros/plotEvent.py  -i v34DLooseMETPassThru.txt   -r v34DLooseMETPassThru_ktmerge.root  --year 2017   --mergeKTPTV -a metsf &> /tmp/logMETSFDKT &
nohup python HInvPlot/macros/plotEvent.py  -i v34DLooseMETPassThru.txt   -r v34DLooseMETPassThru_noktmerge.root   --year 2017    -a metsf &> /tmp/logMETSFDnoKT &

nohup python HInvPlot/macros/plotEvent.py  -i v34ELooseMETPassThru.txt   -r v34ELooseMETPassThru_ktmerge.root --year 2018    --mergeKTPTV -a metsf &> /tmp/logMETSFEKT &
nohup python HInvPlot/macros/plotEvent.py  -i v34ELooseMETPassThru.txt   -r v34ELooseMETPassThru_noktmerge.root  --year 2018    -a metsf &> /tmp/logMETSFEnoKT &

nohup python HInvPlot/macros/plotEvent.py  -i /tmp/v34ELooseMETPassThru.txt   -r /tmp/v34ELooseMETPassThru_ktmerge.root --year 2018    --mergeKTPTV -a metsf &> /tmp/logMETSFEKT &
nohup python HInvPlot/macros/plotEvent.py  -i /tmp/v34ELooseMETPassThru.txt   -r /tmp/v34ELooseMETPassThru_noktmerge.root  --year 2018    -a metsf &> /tmp/logMETSFEnoKT &

nohup python HInvPlot/macros/plotEvent.py  -i /tmp/v34ELooseMETPassThru.txt   -r /tmp/v34ELooseMETPassThru_njcut_ktmerge.root --year 2018   --metsf-cuts 2  --mergeKTPTV -a metsf &> /tmp/logMETSFEKT_njcut &
nohup python HInvPlot/macros/plotEvent.py  -i /tmp/v34ELooseMETPassThru.txt   -r /tmp/v34ELooseMETPassThru_njcut_noktmerge.root  --year 2018   --metsf-cuts 2  -a metsf &> /tmp/logMETSFEnoKT_njcut &
nohup python HInvPlot/macros/plotEvent.py  -i /tmp/v34ELooseMETPassThru.txt   -r /tmp/v34ELooseMETPassThru_3j_ktmerge.root --year 2018  --metsf-cuts 1  --mergeKTPTV -a metsf &> /tmp/logMETSFEKT_3j &
nohup python HInvPlot/macros/plotEvent.py  -i
/tmp/v34ELooseMETPassThru.txt   -r
/tmp/v34ELooseMETPassThru_3j_noktmerge.root  --year 2018
--metsf-cuts 1   -a metsf &> /tmp/logMETSFEnoKT_3j &

> python HInvPlot/macros/TrigSF.py --wait --year 2018 --input /tmp/v34ELooseMETPassThru_ktmerge.root


==========

nohup python HInvPlot/macros/plotEvent.py  -i v34ALooseSYSTJan7.txt
-r /tmp/mca20156.root   --chan nn,e,u,l,ee,uu,ll  --DetailLvl 10
--mergeKTPTV  &> /tmp/test & tail -f /tmp/test

python HInvPlot/macros/submitPlotEventCondor.py -i
/home/schae/testarea/HInv/source/Plotting/v34ELooseSYSTJan7.txt
--extraCommand=" --chan nn,e,u,l,ee,uu,ll --DetailLvl 10 --mergeKTPTV
--year 2018 " -d v34PlotsEJan7

python HInvPlot/macros/submitPlotEventCondor.py -i
/home/schae/testarea/HInv/source/Plotting/v34DLooseSYSTJan7.txt
--extraCommand=" --chan nn,e,u,l,ee,uu,ll --DetailLvl 10 --mergeKTPTV
--year 2017 " -d v34PlotsDJan7

python HInvPlot/macros/submitPlotEventCondor.py -i /home/schae/testarea/HInv/source/Plotting/v34ALooseSYSTJan7.txt --extraCommand=" --chan nn,e,u,l,ee,uu,ll --DetailLvl 10 --mergeKTPTV " -d v34PlotsAJan7

python HInvPlot/macros/drawStack.py out_all_v37febALL.root --vars
averageIntPerXing,centrality,j3Pt,jetEta0,jetEta1,jj_deta,jj_dphi,jj_mass,jj_mass_variableBin,met_cst_jet,met_soft_tst_et,met_tst_nolep_et,metsig_tst,min_mj3_over_mjj,n_jet,met_tst_et
--do-ratio --save --do-pdf --do-eps --outdir /tmp/ZCR/ --year 2019
--int-lumi=139e3 --draw-syst --selkey pass_zcr_allmjj_uu_Nominal
>&/tmp/a1u.log

========

example on lxplus:
```
ssh -Y lxplus770.cern.ch
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase # use your path
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'
setupATLAS
mkdir /tmp/try
cd /tmp/try
git clone ssh://git@gitlab.cern.ch:7999/VBFInv/STPostProcessing.git source/
mkdir build;cd build
acmSetup AthAnalysis,21.2.101
acm compile
cd ..
cd source/Plotting
source setup.sh
rc find_packages
rc clean
rc find_packages
rc compile
ls /eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/*root &> /tmp/v37Egam.txt
python HInvPlot/macros/plotEvent.py -i /tmp/v37Egam.txt -r /tmp/v37e.root --year 2018 --OverlapPh &>/tmp/eph.log & tail -f /tmp/eph.log
```

=======
if you have trouble with acm, then use these instructions
```
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase # use your path
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'
setupATLAS
mkdir /tmp/try2
cd /tmp/try2
git clone https://gitlab.cern.ch/VBFInv/STPostProcessing.git source/
mkdir build;cd build
asetup AthAnalysis,21.2.114,here
cmake ../source/
cd ..
cmake --build build/
cd source/Plotting
source setup.sh
rc find_packages
rc clean
rc compile
ls /eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v37Egam/*root &> /tmp/v37Egam.txt
python HInvPlot/macros/plotEvent.py -i /tmp/v37Egam.txt -r
/tmp/v37e.root --year 2018 --OverlapPh &>/tmp/eph2.log & tail -f /tmp/eph2.log

python HInvPlot/macros/drawStack.py  /tmp/v37e.root     --vars jj_mass_variableBin      --do-ratio     --year 2019  --int-lumi=139e3   --selkey pass_gamwcr_allmjj_l_Nominal --ph-ana  --wait --hscale 1
```
