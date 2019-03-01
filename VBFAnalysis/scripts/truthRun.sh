export nevents=$1
export input=$2

export here=$PWD
cd ../build
acm compile
cd ${here}

athena VBFAnalysis/VBFTruthAlgJobOptions.py --evtMax ${nevents} --filesInput ${input} - --currentVariation Nominal - --normFile $TestArea/x86_64-slc6-gcc62-opt/data/VBFAnalysis/fout_v15.root