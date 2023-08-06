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

def plot_saved_stats(filepath, n, save_filepath, save_name, file_format="png"):
    # Load the saved stats data using pickle
    with open(filepath + '_stats.pkl', 'rb') as f:
        ep_stats = pickle.load(f)

    # Extract the validation accuracy, average validation accuracy, and epochs_since_best for each epoch
    val_accs = [stat['val_acc'] for stat in ep_stats.values()]
    avg_val_accs = [stat['avg_val_acc'] for stat in ep_stats.values()]
    epochs_since_bests = [stat['epochs_since_best'] for stat in ep_stats.values()]

    # Plot the validation accuracy
    plt.figure('plot_saved_stats_Validation_Accuracy')
    plt.plot(val_accs, label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.grid()

    # Plot the average validation accuracy
    plt.figure('plot_saved_stats_Average_Validation_Accuracy')
    plt.plot(avg_val_accs, label='Average Validation Accuracy (last {} epochs)'.format(n))
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.grid()

    # Plot the validation and average validation accuracy
    plt.figure('plot_saved_stats_Validation_Average_Validation_Accuracy')
    plt.plot(avg_val_accs, label='Validation,\nAverage Validation Accuracy (last {} epochs)'.format(n))
    plt.plot(val_accs, label='Validation Accuracy', alpha=0.5)
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.grid()
    plt.legend()

    # Plot the epochs_since_best
    plt.figure('plot_saved_stats_Epochs_Since_Best_Validation_Accuracy')
    plt.plot(epochs_since_bests, label='Epochs Since Best Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Epochs')
    plt.grid()

    # Highlight datapoints with epochs_since_best == 0 as red circles in the plots
    for i in range(len(epochs_since_bests)):
        if epochs_since_bests[i] == 0:
            plt.figure('plot_saved_stats_Validation_Accuracy')
            plt.legend()
            plt.plot(i, val_accs[i], 'ro', alpha=0.5, label="Savepoint" if not i else "")
            plt.figure('plot_saved_stats_Average_Validation_Accuracy')
            plt.legend()
            plt.plot(i, avg_val_accs[i], 'ro', alpha=0.5, label="Savepoint" if not i else "")
            plt.figure('plot_saved_stats_Epochs_Since_Best_Validation_Accuracy')
            plt.legend()
            plt.plot(i, epochs_since_bests[i], 'ro', alpha=0.5, label="Savepoint" if not i else "")

    plt.figure('plot_saved_stats_Validation_Accuracy').savefig(
        save_filepath + save_name + "_val_acc" + "." + file_format, format=file_format, bbox_inches="tight")
    plt.figure('plot_saved_stats_Average_Validation_Accuracy').savefig(
        save_filepath + save_name + "_av_val_acc" + "." + file_format, format=file_format, bbox_inches="tight")
    plt.figure('plot_saved_stats_Validation_Average_Validation_Accuracy').savefig(
        save_filepath + save_name + "_both_val_acc" + "." + file_format, format=file_format, bbox_inches="tight")

    plt.figure('plot_saved_stats_Epochs_Since_Best_Validation_Accuracy').savefig(
        save_filepath + save_name + "_ep_since" + "." + file_format, format=file_format, bbox_inches="tight")

    plt.show()
