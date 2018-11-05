import os
import signal
import sys
import time
from importlib import import_module
from pprint import pformat
from random import random

import numpy as np
import tensorflow as tf

from deephyper.run.nas_cmdline import create_parser
from deephyper.search import util
from deephyper.search.nas.model.trainer import BasicTrainer
from deephyper.search.nas.model.trainer_gen import GenTrainer

logger = util.conf_logger('deephyper.search.nas')

def run(param_dict):
    logger.debug('Starting...')
    config = param_dict
    assert config.get('input_shape') is not None
    assert config.get('output_shape') is not None

    load_data = util.load_attr_from(config['load_data']['func'])

    config['create_structure']['func'] = util.load_attr_from(
        config['create_structure']['func'])

    config['create_cell']['func'] = util.load_attr_from(config['create_cell']['func'])

    logger.debug('[PARAM] Loading data')
    # Loading data
    (gen_train, n_train), (gen_valid, n_valid) = load_data(**config['load_data']['kwargs'])
    logger.debug('[PARAM] Data loaded')

    config['data'] = { 'gen_train': gen_train,
                       'n_train': n_train,
                       'gen_valid': gen_valid,
                       'n_valid': n_valid }

    architecture = config['arch_seq']

    # For all the Net generated by the CONTROLLER
    trainer = GenTrainer(config)

    # Run the trainer and get the rewards
    result = trainer.get_rewards(architecture)

    logger.debug(f'[REWARD/RESULT] = {result}')
    return result

if __name__ == '__main__':
    parser = create_parser()
    cmdline_args = parser.parse_args()
    param_dict = cmdline_args.config
    run(param_dict)
