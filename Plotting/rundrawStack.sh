out=$1
reg=$2
var=$3

key1='pass_'
key2='_allmjj_nn_Nominal'

echo "$key1$reg$key2"
python HInvPlot/macros/drawStack.py $out --vars $var --selkey "$key1$reg$key2" --wait --do-ratio --atlas-style /export/home/asteinhe/atlasstyle/
