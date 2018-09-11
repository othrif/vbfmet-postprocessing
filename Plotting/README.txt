
source setup.sh

rc clean
rc find_packages
rc compile

# place the ntuples into a line separated text file
#ls /eos/user/r/rzou/v04/merged/* &> input.txt
ls /afs/cern.ch/user/r/rzou/workspace/public/STPostProcessing/run/newmicro/microtuples/* &> input.txt

# NOTE: data is not blinded in this setup. So comment it out in the input file.

# to plot run:
python HInvPlot/macros/plotEvent.py -i input.txt 

To add new variables, you must add them to Root/VarEvent.cxx and its header. The binning is defined in python/Vars.py. If you want to create a variable from the existing information, then you also need to fill it in Root/ReadEvent.cxx. Follow an example like mll.

# Variables can then be plotted from the output file
python HInvPlot/macros/drawStack.py out.root --vars ptll  --selkey pass_zcr_allmjj_ll --wait --do-pdf --save --draw-syst
