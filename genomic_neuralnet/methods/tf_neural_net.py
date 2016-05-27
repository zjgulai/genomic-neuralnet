import numpy as np

from genomic_neuralnet.util import NeuralnetConfig
from genomic_neuralnet.methods.generic_tf_net import get_net_prediction

def get_tfnet_pred( train_data, train_truth, test_data, test_truth
                     , hidden=(5,), weight_decay=0.0): 
    net_config = NeuralnetConfig()
    net_config.hidden_layers = hidden
    net_config.learning_rate = 0.1
    net_config.continue_epochs=2500
    net_config.max_epochs=10000
    net_config.batch_splits = 5

    return get_net_prediction( train_data, train_truth, test_data, test_truth
                             , net_config=net_config, weight_decay=weight_decay)
