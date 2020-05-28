# Truth Analysis to compare Z and W bosons and Jet veto efficiency #

1- Copy `W_strong.root` and `Z_strong.root` MicroNtuples from `/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v42Truth/microntuple_230420` to a local directory, call it `processed` for example

You can run steps 2-4 using this script: `source plotAll.sh`, or following the step-by-step:

2- Make region specific trees using `python pyAnalysis/extractNtuples.py processed/W_strong.root processed/Z_strong.root`

3- Make histograms  using:
``` bash
#python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_checks.json --treename nominal --eventWeight "w" --newOutputs --name checks_
python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_Vdefs.json --treename nominal --eventWeight "1000*w" --newOutputs --name checks_
python pyAnalysis/makeHists.py processed/extract_* --config pyAnalysis/hists_config_NjetTJV_Vdefs.json --treename nominal --eventWeight "1000*w" --newOutputs --name tjv_
```
The configuration of the histograms (additional selection, binning, name, etc.) is specified using a `json` files:
- `hists_config_checks.json` is to draw all distributions to perform checks
- `hists_config_NjetTJV.json` draw `jj_mass` for `Njet25==2 and Njet25>=2` for jet veto efficiency study

4-Draw histograms comparing `file1.root` with `file2.root`:

a- One distribution from two files by specifying `-v` option: `python pyAnalysis/drawHists.py -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD -v /all/Incl/boson_pt,/all/Incl/boson_pt -l --wait`

b- All distributions by NOT specifying the `-v` option: `python pyAnalysis/drawHists.py  -p processed -f hists_checks_extract_Zvv_QCD,hists_checks_extract_Wlv_QCD`

c- Jet veto efficiency study done by running: `python pyAnalysis/ratioHists.py  -p processed -f hists_tjv_extract_Zvv_QCD,hists_tjv_extract_Wlv_QCD -v /all/SR25/jj_mass,/all/SRmTJV/jj_mass --wait`
