out=$1
reg=$2
var=$3

key1='pass_'
key2='_Nominal'

python HInvPlot/macros/drawStack.py $out --vars $var --selkey "$key1$reg$key2" --wait --do-ratio --atlas-style /afs/cern.ch/work/a/asteinhe/atlasstyle/ --blind

