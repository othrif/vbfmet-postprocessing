
source setup.sh

rc clean
rc find_packages
rc compile

# place the ntuples into a line separated text file
#ls /afs/cern.ch/user/r/rzou/workspace/public/STPostProcessing/run/newmicro/microtuples/* &> input.txt
cp -rf /eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/v20 /tmp/v20
ls /tmp/v20/* &> input.txt

# NOTE: data is not blinded in this setup. So comment it out in the input file.

# to plot run:
python HInvPlot/macros/plotEvent.py -i input.txt 

To add new variables, you must add them to Root/VarEvent.cxx and its header. The binning is defined in python/Vars.py. If you want to create a variable from the existing information, then you also need to fill it in Root/ReadEvent.cxx. Follow an example like mll.

# Variables can then be plotted from the output file
python HInvPlot/macros/drawStack.py out.root --vars ptll  --selkey pass_zcr_allmjj_ll --wait --do-pdf --save 
# --draw-syst can be added if you ran over the systematics
# --selkey is the region that you are plotting. for example, pass_zcr_allmjj_ll this is the Z control region with Mjj>1 Tev and two opposite sign leptons (e or mu)

## NOTE::: recommend copying the micro-ntuples to the tmp space instead of eos. eos has a very slow I/O.

==========

To add a variable to a jet, muon, electron, tau or photon, please follow these instructions:
Copy the jet_fjvt vector to read in new jet variables:
https://gitlab.cern.ch/VBFInv/STPostProcessing/blob/master/Plotting/HInvPlot/Root/ReadEvent.cxx#L645

Create a new variable name in the name space for your new variable. For exmaple you can copy fjvt:
https://gitlab.cern.ch/VBFInv/STPostProcessing/blob/master/Plotting/HInvPlot/Root/VarEvent.cxx#L92

Draw the histogram. Again you can follow the fjvt example: 
https://gitlab.cern.ch/VBFInv/STPostProcessing/blob/master/Plotting/HInvPlot/Root/PlotEvent.cxx

add x label, etc:
https://gitlab.cern.ch/VBFInv/STPostProcessing/blob/master/Plotting/HInvPlot/macros/drawStack.py#L188
