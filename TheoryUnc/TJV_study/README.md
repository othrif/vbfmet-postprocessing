# Truth Analysis to compare Z and W bosons and Jet veto efficiency #

1- Copy `W_strong.root` and `Z_strong.root` MicroNtuples from `/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v42Truth/microntuple_220420` to a local directory, call it `processed` for example

2- Make region specific trees using `python pyAnalysis/extractNtuples.py processed/*.root`

3- Make histograms  using `python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_checks.json --treename nominal --eventWeight "w" --newOutputs --name checks_`
The configuration of the histograms (additional selection, binning, name, etc.) is specified using a `json` file called `hists_config_checks.json`

4-Draw histograms comparing `file1.root` with `file2.root`:

    a- One distribution from two files by specifying `-v` option: `python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v all/Incl/boson_pt,all/Incl/boson_pt --wait`

    b- All distributions by NOT specifying the `-v` option: `python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD`

5- Jet veto efficiency study, make histograms using  `python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_NjetTJV.json --treename nominal --eventWeight "w" --newOutputs --name tjv_`

6- To evaluate the impact of the jet veto on Z and W and their ratios, run:  `root pyAnalysis/plotTJVRatio.C `

