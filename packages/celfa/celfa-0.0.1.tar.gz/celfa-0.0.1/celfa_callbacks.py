# STL
import os
import logging
import configparser
import itertools
from typing import Union, List
import pickle

# 3rd party
import numpy as np
import tensorflow as tf
from keras.callbacks import ModelCheckpoint
from tensorflow import keras
import matplotlib.patches
import matplotlib.pyplot as plt
import sklearn.metrics
from sklearn.metrics import roc_auc_score, roc_curve, auc
import statsmodels.stats.proportion as sm

# Home-made :)
import celfa_data
import celfa_exceptions


########################################################################################################################
# CELFA - CNN Evaluation Library For ANNIE
# ----------------------------------------
# This file serves specialised callback functionality.
########################################################################################################################

########################################################################################################################
# CONFIG:
# TODO: Config
# config_eval = configparser.ConfigParser()
# config_eval.read("eval_config.ini")

########################################################################################################################
# LOGGING:
# TODO: logging
# eval_log_formatter = logging.Formatter(config_eval["LOGGER_DATA"]["format"])

# eval_log_file_handler = logging.FileHandler(config_eval["LOGGER_DATA"]["file"])
# eval_log_file_handler.setFormatter(eval_log_formatter)

# eval_logger = logging.getLogger(__name__)
# eval_logger.addHandler(eval_log_file_handler)
# eval_logger.setLevel(logging.INFO)


########################################################################################################################

class SaveBestValidationAccuracy(keras.callbacks.Callback):
    def __init__(self, filepath, n=3, call_on_val_acc_incr=None):
        self.filepath = filepath
        self.n = n
        self.best_avg_val_acc = 0
        self.epochs_since_last_best = 0
        self.val_accuracies = []
        self.ep_stats = {}

        self.call_on_val_acc_incr = call_on_val_acc_incr

    def on_epoch_end(self, epoch, logs=None):
        # Calculate the average validation accuracy of the last n epochs
        if logs is None:
            logs = {}
        self.val_accuracies.append(logs.get('val_accuracy'))

        if epoch == 0:
            avg_val_acc = sum(self.val_accuracies)
        elif epoch < self.n:
            avg_val_acc = sum(self.val_accuracies[-epoch:]) / epoch
        else:
            avg_val_acc = sum(self.val_accuracies[-self.n:]) / self.n

        # Save the model and call val_acc_incr() if the average validation accuracy has increased
        if avg_val_acc > self.best_avg_val_acc:
            print(f"\nAverage validation accuracy improved from {self.best_avg_val_acc:.4f} to {avg_val_acc:.4f}. "
                  f"Saving model.")

            self.best_avg_val_acc = avg_val_acc
            self.model.save(self.filepath)
            self.epochs_since_last_best = 0

            if self.call_on_val_acc_incr:
                self.call_on_val_acc_incr(model=self.model,
                                          epoch=epoch,
                                          val_acc=logs.get('val_accuracy')[-1],
                                          avg_val_acc=avg_val_acc)
        else:
            self.epochs_since_last_best += 1

        # Save the logs and the number of epochs since the last best validation accuracy using pickle
        self.ep_stats[epoch] = {
            'val_acc': logs['val_accuracy'],
            'avg_val_acc': avg_val_acc,
            'epochs_since_best': self.epochs_since_last_best
        }

        try:
            with open(self.filepath + '_stats.pkl', 'rb') as f:
                saved_ep_stats = pickle.load(f)
        except FileNotFoundError:
            saved_ep_stats = {}

        saved_ep_stats.update(self.ep_stats)

        with open(self.filepath + '_stats.pkl', 'wb') as f:
            pickle.dump(saved_ep_stats, f)

