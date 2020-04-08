// installing tensorflow & keras
sudo pip install keras
sudo pip install tensorflow
sudo pip install matplotlib

/// python 3
source /cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-centos7-gcc8-opt/setup.sh

// some basic instructions
https://keras.io/getting-started/sequential-model-guide/#multilayer-perceptron-mlp-for-multi-class-softmax-classification

// dumping a pickle file to be read in. This is OLD. Sid implemented a
faster version to write to numpy arrays
```
python dumpTree.py
```
// running a binomial classifier and to save the model
```
python MLP2.py
```

//USE this one: This is the faster code writing to numpy arrays
```
python getData.py
```

//then to train based upon this code, you need. You can change which
variables and which samples are trained in this piece of code. Might
make sense to make your own version of this code for a new analysis.
```
python trainMLP.py
```

// to add tmva variable use this script. Make sure the scaler and weights files are correctly set
```
python addMLP.py
```
// a much faster version that is setup to run with trainMLP.py and
uses numpy arrays to load the data quickly is. Make sure to check the
top lines for the input variables, input directory, and output directory
```
python addMLPFriendTree.py
```

// for the VBF+gamma analysis, additional variables are added:
```
python trainMLPgam.py
```
