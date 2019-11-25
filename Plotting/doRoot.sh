#declare -a sampleArray=("_allmjj_" "_mjjLow200_" "_mjjLowNjetFJVT_" "_njgt_")
declare -a sampleArray=("_allmjj" "_mjjLow200" "_mjjLowNjetFJVT" "_njgt")
#declare -a treeArray=("_allmjj_" "_mjjLow200_" "_mjjLowNjetFJVT_" "_njgt_")
count=-1
declare -a selkeyArray=()

#path1='puDown.root'
#path1='puUp.root'
#path1='hadd.root'

sr='pass_sr'
sr1='_nn_'
wcr='pass_wcr'
wcr1='_l_'
wcr2='_u_'
wcr3='_e_'


syst='PRW_DATASF__1down'


for i in "${sampleArray[@]}"; do
	((count++))
	syst='Nominal'
	path='output34/LoosePF18OTM_NoPUCorr/out34'
	path1='.root'
	selkeyArray+=($sr${sampleArray[$count]}$sr1$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr1$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr2$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr3$syst)
	for j in "${selkeyArray[@]}"; do
		python HInvPlot/macros/drawStack.py "$path$i$path1" --vars averageIntPerXing --selkey ${j} --do-root --atlas-style /export/home/asteinhe/atlasstyle/ --show-mc-stat-err --int-lumi 59937  --save
	done
	selkeyArray=()

	syst='PRW_DATASF__1up'
	path='output34/LoosePF18OTM_NoPUCorr_puSyst/out34'
	path1='_puUp.root'
	selkeyArray+=($sr${sampleArray[$count]}$sr1$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr1$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr2$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr3$syst)
	for j in "${selkeyArray[@]}"; do
		python HInvPlot/macros/drawStack.py "$path$i$path1" --vars averageIntPerXing --selkey ${j} --do-root --atlas-style /export/home/asteinhe/atlasstyle/ --show-mc-stat-err --int-lumi 59937 --save
	done
	selkeyArray=()

	syst='PRW_DATASF__1down'
	path1='_puDown.root'
	selkeyArray+=($sr${sampleArray[$count]}$sr1$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr1$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr2$syst)
	selkeyArray+=($wcr${sampleArray[$count]}$wcr3$syst)
	for j in "${selkeyArray[@]}"; do
		python HInvPlot/macros/drawStack.py "$path$i$path1" --vars averageIntPerXing --selkey ${j} --do-root --atlas-style /export/home/asteinhe/atlasstyle/ --show-mc-stat-err --int-lumi 59937 --save
	done
	selkeyArray=()
done
rm *.png
