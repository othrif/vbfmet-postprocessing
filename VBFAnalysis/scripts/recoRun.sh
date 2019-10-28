export nevents=$1
export input=$2
cd ../build
acm compile
cd ../run

athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --evtMax ${nevents} --filesInput ${input} - --currentVariation Nominal - --normFile $TestArea/x86_64-slc6-gcc62-opt/data/VBFAnalysis/fout_v26Loose.root