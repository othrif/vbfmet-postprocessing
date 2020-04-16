### General Description ###
Algorithms included: VBFAnalysisAlg, HFInputAlg, VBFTruthAlg.

In order to run the algorithms all the samples should have the name pattern: user.ANYNAME.vTAG.RUNNUMBER. Data samples should in addition has physics_Main in the name.

The list of systematics is defined in VBFAnalysis/python/systematics.py. See VBFAnalysis/scripts/submitHFInputCondor.py as an example of how to use it.

The grouping of samples is based on RUNNUMBER and "physics_Main". It is defined in VBFAnalysis/python/sample.py. See VBFAnalysis/share/VBFAnalysisAlgJobOptions.py as an example of how to use it.

VBFAnalysis/python/job_configurations package allows users to add user defined flags to athena job options. See VBFAnalysis/share/HFInputJobOptions.py as an example of how to use it.


## First time setup ##

```bash
cd $TestArea
git clone ssh://git@gitlab.cern.ch:7999/VBFInv/STPostProcessing.git source/
mkdir build;cd build
acmSetup AthAnalysis,21.2.101
acm compile
```

## Future setup ##
```bash
cd $TestArea/build
acmSetup
```

# Create the input files
Generating a map is the preferred option for listing files:
```bash
# For GRID files
python VBFAnalysis/util/writeFileMap.py 
# Copy in a text file with one input file per line. There is an input for text files from the GRID, and these can be overwritten preferring your local files.
python VBFAnalysis/util/writeFileMapLS.py 
```
Then collect the pickle file to get the total event counts for normalization:
```bash
python source/VBFAnalysis/util/getN.py -p source/VBFAnalysis/data/uchicagoFileMap_v15Loose.p -o fout_v15raw.root
```
To check the number of raw events, the RAW counts need to be saved: Add the -r 1 option.
```bash
python source/VBFAnalysis/util/getN.py -p source/VBFAnalysis/data/uchicagoFileMap_v15Loose.p -o fout_v15raw.root -r 1
```

## Run VBFAnalysisAlg ##
This generates the micro ntuples (from the MiniNtuples).
For running locally with athena:
```bash
cd run
# run locally on 10 events over a file
athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --evtMax 10 --filesInput /eos/user/r/rzou/v04/user.othrif.v04.364162.Sherpa_221_NNPDF30NNLO_Wmunu_MAXHTPTV140_280_CVetoBVeto.e5340_s3126_r9364_r9315_p3575_MiniNtuple.root/user.othrif.14790250._000001.MiniNtuple.root - --currentVariation Nominal
# run locally over a dir
athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --evtMax 10 --filesInput /eos/user/r/rzou/v04/user.othrif.v04.364106.Sherpa_221_NNPDF30NNLO_Zmumu_MAXHTPTV140_280_CVetoBVeto.e5271_s3126_r9364_r9315_p3575_MiniNtuple.root/* - --currentVariation Nominal
```
For running on condor:
```bash
# you'll want to generate a list of files, which only has to be done once. give it a comma separated list of input containers
python VBFAnalysis/util/writeFileMap.py
# there is also a setup for local files  VBFAnalysis/util/writeFileMapLS.py
# run on condor over a list of files for nominal
submitVBFAnalysisCondor.py -l /eos/user/r/rzou/v04/list -n
# run on condor over a list of files for all sys
submitVBFAnalysisCondor.py -l /eos/user/r/rzou/v04/list
# run on condor over a list of files for all sys with log files saved to a specific dir
submitVBFAnalysisCondor.py -l /eos/user/r/rzou/v04/list -d dir
# you'll need a grid proxy, which needs to have global permission. This is in the /tmp/x509*. Use the -p option. -l is for the map of the files at chicago on RUCIO
submitVBFAnalysisCondor.py -l ../source/VBFAnalysis/data/uchicagoFileMap.p -n -p /home/schae/testarea/HInv/run/x509up_u20186
```
You can change the list of systematics in VBFAnalysis/python/systematics.py.
To merge the samples, in the dir where microtuples live do:
```bash
mergeVBFAnalysisAlg.sh
```


## Run HF Input Maker ##
This generates histograms for HistFitter to read from. It reads from the microtuples produced by VBFAnalysisAlg.
     --doTMVA creates fitting plots from the variable tmva
```bash
cd run
# run locally over 10 events for nominal
athena VBFAnalysis/HFInputJobOptions.py --evtMax 10 --filesInput /eos/user/r/rzou/v04/microtuples/Z_strongNominal364100_000001.root - --currentVariation Nominal
```
For running on condor:
```bash
# run on condor over all the contributions and nominal only
submitHFInputCondor.py --mergeKTPTV --extraVars 7 --Binning 11 -d submitTest -i /home/schae/testarea/HInv/runSherpa227/v34ATight120/ -n --slc7
# run on condor over all the contributions and systematics
submitHFInputCondor.py --mergeKTPTV --extraVars 7 --Binning 11 -d submitTest -i /home/schae/testarea/HInv/runSherpa227/v34ATight120/ --slc7
```
You can change the list of systematics in VBFAnalysis/python/systematics.py and list of contributions in VBFAnalysis/python/sample.py.

## Plotting output of HF Input Maker ##
To plot all bins do (HFoutput.root is the file after merging the output of HF Input Maker). Add --unBlindSR to also show data in SRs:
```bash
fitPlot.py -i HFoutput.root --data --ratio
```
You can also print out tex tables of the yields and save them together with the plot as pdf:
```bash
fitPlot.py -i HFoutput.root --data --ratio --yieldTable --texTables -q --saveAs pdf
```
In case the HFinput was created with the --doPlot flag you can also plot the variables that were saved. Format: --plot VARIABLE,REGION,MJJBINS. REGION is for example SR,twoEleCR,oneMuPosCR,oneEleNegLowSig. Code checks if REGION is in the histname so just giving oneEle would include pos negative but also lowsig regions. MJJBINS are the bins plotted sperated by a "\_". To unblind use --unBlindSR. Example:
```bash
fitPlot.py -i HFoutput.root --plot jj_mass,SR,1_2_3 --data --ratio
```
To compare different root files you can use the --compare option instead of -i:
```bash
fitPlot.py --compare HFoutput1.root,HFoutput2.root,HFoutput3.root --data --ratio --yieldTable --texTables -q --saveAs png
```

python VBFAnalysis/scripts/sysPlotv2.py -i  /tmp/HFALL_feb17d_sysNew_smooth5.New.root  --inputUpdate /tmp/HFALL_feb17d_sysNew_smooth5.New.root       --saveAs png   --syst weird  --smooth 5 --ZeroCheck --combinePlusMinus

```bash
# run on condor over all the contributions and nominal only for photon analysis
submitHFInputCondor.py --mergeKTPTV --extraVars 7 --Binning 13 -d submitTest -i /home/schae/testarea/HInv/runSherpa227/v34ATight120/ -n --slc7 --doVBFMETGam
```