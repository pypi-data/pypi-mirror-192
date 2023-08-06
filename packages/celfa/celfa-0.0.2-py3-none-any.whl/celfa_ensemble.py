# STL
import os
import logging
import configparser
import itertools
from typing import Union, List

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

# Home-made
import celfa_data
import celfa_exceptions


########################################################################################################################
# CELFA - CNN Evaluation Library For ANNIE
# ----------------------------------------
# This file simplifies the task of training ensembles.
########################################################################################################################

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

def build_av_ens(models: list, input_layers: list, model_input: dict):
    """Build a simple averaging ensemble, from already trained models.

    :param models: loaded models
    :param input_layers: a list of tf.keras.layers.Input()
    :param model_input: dictionary corresponding to the models input(s). Keys: names of the input layers, values:
        tf.keras.layers.Input()
    """

    prepared_models = []
    for model in models:
        prepared_models.append(model(model_input))

    ensemble_output = tf.keras.layers.Average()(prepared_models)
    ensemble = tf.keras.Model(inputs=input_layers, outputs=ensemble_output)

    return ensemble


def train_ens(untrained_model_path: str, trained_filepath: str, count: int,
              train_data, train_cat_vals,
              validation_data, validation_cat_vals,
              batch_size: int = 100, epochs: int = 30,
              input_layers: list = None, model_input: dict = None):
    """Supply untrained model. will train specified amount of models."""
    trained_models = []
    for i in range(0, count):
        untrained = tf.keras.models.load_model(untrained_model_path)
        checkpoint = ModelCheckpoint(f"{trained_filepath}_{i}.model",
                                     monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')

        history = untrained.fit(
            train_data, train_cat_vals,
            validation_data=(validation_data, validation_cat_vals),
            batch_size=batch_size,
            shuffle=True,
            callbacks=[
                checkpoint,
            ],
            epochs=epochs)

        print(history.history.keys())
        # summarize history for accuracy
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        print(f"####################################################### \n \n"
              f"     Finished epochs ; finished training model # {i} \n \n "
              f"#######################################################")
        trained_models.append(untrained)

    if input_layers and model_input:
        return build_av_ens(trained_models, input_layers, model_input)
    else:
        return trained_models
