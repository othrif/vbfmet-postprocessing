// installing tensorflow & keras
sudo pip install keras
sudo pip install tensorflow
sudo pip install matplotlib

/// python 3
source /cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-centos7-gcc8-opt/setup.sh

// some basic instructions
https://keras.io/getting-started/sequential-model-guide/#multilayer-perceptron-mlp-for-multi-class-softmax-classification

// dumping a pickle file to be read in
python dumpTree.py

// running a binomial classifier and to save the model
python MLP2.py

// to add tmva variable use this script. Make sure the scaler and weights files are correctly set
python addMLP.py