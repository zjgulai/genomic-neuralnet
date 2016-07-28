from __future__ import print_function

from genomic_neuralnet.config import JOBLIB_BACKEND
from genomic_neuralnet.methods import get_lr_prediction 
from genomic_neuralnet.analyses import run_optimization

def main():
    params = {} 
    run_optimization(get_lr_prediction, params, 'optimal_en.shelf', 'OLS')

if __name__ == '__main__':
    main()
