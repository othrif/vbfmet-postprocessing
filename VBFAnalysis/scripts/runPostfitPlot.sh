#!/bin/bash

#2020-02-11 amanda.lynn.steinhebel@cern.ch
#Utilize fitPlot.py script to draw pre- and post-fit plots
#
#Input: the .root file used for fitting (NOT the workspace, the original input), optionally a directory of pickle files containing postfit info (from StatsTools commandYieldTable script) - needed for postfit plot
#Output: pdf plot, .txt file of statistical syst (to be optionally used when making impact plots)
#
#Example command
# ./runPullPlots.sh inputRoot.root pickleDir/
#(required input first argument, optional pickle directory for postfit plots)


inputs=("$@")
if [ "$#" == 2 ]; then
  postfit=" --postFitPickleDir ${inputs[1]}"
else
  postfit=""
fi


echo "Running \"python fitPlot.py -i ${inputs[0]} --data --ratio --show-mc-stat-err $postfit --saveAs pdf -q\""
python fitPlot.py -i ${inputs[0]} --data --ratio --show-mc-stat-err $postfit --saveAs pdf -q

