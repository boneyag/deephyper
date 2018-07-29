'''
 * @Author: romain.egele, dipendra.jha
 * @Date: 2018-06-21 15:31:30
'''

from collections import OrderedDict
from deephyper.model.arch import StateSpace

class Problem:
    def __init__(self):
        space = OrderedDict()
        space['num_outputs'] = 36
        space['regression'] = False

        # ARCH
        space['max_layers'] = 8
        space['layer_type'] = 'conv1D'
        state_space = StateSpace()
        state_space.add_state('filter_size', [size for size in range(3, 10, 2)])
        state_space.add_state('pool_size', [size for size in range(1, 6)])
        state_space.add_state('stride_size', [s for s in range(1, 4)])
        state_space.add_state('drop_out', [])
        state_space.add_state('num_filters', [2 ** i for i in range(5, 10)])
        state_space.add_state('skip_conn', [])
        space['state_space'] = state_space

        # ITER
        space['max_episodes'] = 500 # iter on controller

        # HyperParameters
        space['hyperparameters'] = {'batch_size': 64,
                                    'eval_batch_size': 64,#needs to be same as batch size
                                    'activation': 'relu',
                                    'learning_rate': 0.0001,
                                    'optimizer': 'adam',
                                    'num_epochs': 10,
                                    'loss_metric': 'softmax_cross_entropy',
                                    'test_metric': 'accuracy'
                                }
        self.space = space


if __name__ == '__main__':
    instance = Problem()
