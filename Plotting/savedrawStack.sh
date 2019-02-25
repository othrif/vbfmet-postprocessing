out=$1
reg=$2
chan=$3
var=$4

key1='pass_'
key2='_allmjj_'
key3='_Nominal'

python HInvPlot/macros/drawStack.py $out --vars $var --selkey "$key1$reg$key2$chan$key3" --do-ratio --atlas-style /export/home/asteinhe/atlasstyle/ --blind --do-eps --save
