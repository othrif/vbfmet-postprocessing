import yaml      
import neuralNet
import sys

with open(sys.argv[1]) as ymlfile:
    cfg = yaml.load(ymlfile)
    mlp = neuralNet.MLP(cfg)
    
mlp.preprocess_data()
mlp.train_model()
mlp.make_plots()
mlp.feature_importance()
