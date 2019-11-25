out=$1
reg=$2
var=$3
lumi=$4

key1='pass_'
key2='_Nominal'

python HInvPlot/macros/drawStack.py $out --vars $var --selkey "$key1$reg$key2"  --do-ratio --atlas-style /export/home/asteinhe/atlasstyle/ --do-pdf --show-mc-stat-err --int-lumi $lumi --save
