from __future__ import print_function

import os
import sys
import time
import numpy as np
import redis
import pickle

from itertools import chain

from genomic_neuralnet.common.base_compare import try_predictor
from genomic_neuralnet.util.ec2_util import get_master_dns

from celery import Celery
import celery.app.control as ctrl 
name = 'parallel_predictors'
_host = get_master_dns(public=True)
backend = 'redis://{}/0'.format(_host)
broker = 'redis://{}/0'.format(_host)
app = Celery(name, backend=backend, broker=broker)
celery_try_predictor = app.task(try_predictor)

os.environ['BROKER_TRANSPORT_OPTIONS'] = "{'visibility_timeout': 900}"

_cache_dir = os.path.expanduser('~/work_cache')
if not os.path.isdir(_cache_dir):
    os.makedirs(_cache_dir)

def disk_cache(result, id_num):
    file_path = os.path.join(_cache_dir, '{}_out.pkl'.format(id_num))
    with open(file_path, 'wb') as f: 
        pickle.dump(result, f)

def load_and_clear_cache(id_nums):
    for id_num in id_nums:
        file_path = os.path.join(_cache_dir, '{}_out.pkl'.format(id_num))
        os.unlink(file_path)

def get_num_workers():
    num_workers = 0
    for instance, stats in ctrl.Control(app).inspect().stats().iteritems():
        num_workers += stats['pool']['max-concurrency']
    return num_workers

def get_queue_length():
    conn = redis.StrictRedis(_host)
    return conn.llen('parallel_predictors')

def main():
    # Start the worker.
    app.worker_main(['--loglevel=DEBUG']) 

if __name__ == '__main__':
    main()
