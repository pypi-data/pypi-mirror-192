# STL
import os
import logging
import configparser
import pickle
import pathlib
import random
from dataclasses import dataclass

# 3rd party
import numpy as np
import matplotlib.pyplot as plt

# Home-made
import celfa_exceptions

########################################################################################################################
# CELFA - CNN Evaluation Library For ANNIE
# ----------------------------------------
#
# This file contains helpful globals.
########################################################################################################################

########################################################################################################################
# CONFIG:
from typing import List, Union


# config_data = configparser.ConfigParser()
# config_data.read("data_config.ini")

########################################################################################################################

# From p.e. curve histogram plots -> which PMTs have different MC / data curves
PE_CURVE_DIFFERING_PMT_INDICES_NOVEMBER_22 = [56, 58, 84, 85, 87, 88, 89, 100, 118, 120, 121, 137, 138, 139]
# In the data (MRDc.) these PMTs are not active compared to MC datasets
ACTIVE_PMT_DIFFERING_PMT_INDICES_NOVEMBER_22 = [22, 124]
