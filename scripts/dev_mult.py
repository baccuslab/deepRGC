# %load_ext autoreload
# %autoreload 1

import os
import functools
import argparse
import tensorflow as tf
K = tf.keras.backend
import tableprint as tp
import numpy as np
from deepretina import config
import deepretina
import deepretina.experiments
import deepretina.models
import deepretina.core
import deepretina.metrics
# %aimport deepretina
# %aimport deepretina.experiments
# %aimport deepretina.models
# %aimport deepretina.core
# %aimport deepretina.metrics
D = deepretina
batch_size = 1000
np.arange(0,5,1)[0:10]
val_split=0.95
config.data_dir = "/storage/baccus/"
config.data_dir = "/home/tyler/scratch/"
config.results_dir = "/storage/baccus/results/"
expts = [
    # ("15-10-07",D.experiments.CELLS["15-10-07"],"whitenoise"),
    # ("15-10-07",D.experiments.CELLS["15-10-07"],"naturalscene"),
    # ("15-11-21a",D.experiments.CELLS["15-11-21a"],"whitenoise"),
    # ("15-11-21a",D.experiments.CELLS["15-11-21a"],"naturalscene"),
    # ("15-11-21b",D.experiments.CELLS["15-11-21b"],"whitenoise"),
    # ("15-11-21b",D.experiments.CELLS["15-11-21b"],"naturalscene"),
    # ("16-01-07",D.experiments.CELLS["16-01-07"],"naturalscene"),
    # ("16-01-07",D.experiments.CELLS["16-01-07"],"whitenoise"),
    # ("16-01-08",D.experiments.CELLS["16-01-08"],"naturalscene"),
    # ("16-01-08",D.experiments.CELLS["16-01-08"],"whitenoise"),
    #
    ("17-11-10-ssb","all","naturalmovie"),
    ("17-12-09-ssb","all","naturalmovie"),
    ("17-12-09b-ssb","all","naturalmovie"),
    ("17-12-16b-ssb","all","naturalmovie")
]
run_name = "josh_naturalmovie"

data, input_shape, nsamples = D.experiments.load_multiple_expt(expts, 'train', 40, 6000)
experiment_n, experiment_ntrain = D.experiments.ntrain_by_experiment(data,val_split)

train_data = D.experiments.multiple_experiment_generator(data, "TRAIN",val_split=val_split)
valid_data = D.experiments.multiple_experiment_generator(data, "VALID",val_split=val_split)

steps_per_epoch = sum(np.ceil(experiment_ntrain/batch_size))
steps_per_valid = sum(np.ceil(experiment_n-experiment_ntrain)/batch_size)

def context(func):
    def wrapper(*args, **kwargs):
        graph = tf.Graph()
        with graph.as_default():
            with tf.Session(graph=graph) as sess:
                K.set_session(sess)
                result = func(*args, **kwargs)
        return result
    return wrapper

# %%
@context
def fit_g_cnn(train_data, input_shape, steps_per_epoch, run_name, valid_data, steps_per_valid):
    D.core.train_generator(D.models.g_cnn, train_data, input_shape, steps_per_epoch, run_name,
    valid_data, steps_per_valid, lr=1e-2, nb_epochs=250, bz=1000, loss=D.metrics.argmin_poisson,
    the_metrics=[D.metrics.matched_cc, D.metrics.matched_mse, D.metrics.matched_rmse])


@context
def fit_bn_cnn(expt, stim):
    D.core.train(D.models.bn_cnn, expt, stim, lr=1e-2, nb_epochs=250, val_split=0.05,bz=batch_size)

fit_g_cnn(train_data, input_shape, steps_per_epoch, run_name, valid_data, steps_per_valid)

# fit_bn_cnn(expt, stim)