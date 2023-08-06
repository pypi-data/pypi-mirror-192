# STL
import os
import pickle
import pathlib
import random
from dataclasses import dataclass
from typing import List, Union

# 3rd party
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

# Home-made :)
import celfa_exceptions

########################################################################################################################
# CELFA - CNN Evaluation Library For ANNIE
# ----------------------------------------

# This file encapsulates utility functions to load and organize data_container.
# In the first parts of the file, basic file operations are implemented, in the latter parts building the data_container
# structures and export, as well as saving is implemented.
########################################################################################################################


def find_number_files(path: str, label: str, name: str, ending: str = "csv", guess: int = -1,
                      beam_mrd_coinc: bool = False) -> int:
    """
    This function returns the amount of files fount, specified by the following parameters in the form
    ~/name/label_#####_name.ending, where '#####' is the corresponding file number. The function will start attempting
    to load files starting with the index '0'.

    Warning: This will only find all files, as long as the highest file index is smaller than the number of all files
    in the directory.

    :param beam_mrd_coinc: TODO see load_data
    :param path: Directory name (Include forward slash at the end)
    :param label: Label of the data_container, e.g. 'electron_beamlike'
    :param name: What data_container is read in, e.g. 'charge', 'neutron number'
    :param ending: File ending, e.g. 'csv' (without dot). Default = 'csv'
    :param guess: Best guess of number of data_container files. If set to -1, attempt to find all files fitting the structure.
     Default = -1.
    :return: Returns how many files, specified by the parameters, have been found.
    """
    try:
        os.listdir(path)
    except OSError:
        return -1

    counter = guess if guess != -1 else int(len(os.listdir(path)))

    for i in range(counter):
        p = pathlib.Path(f"{path}{label}_{i}_{name}.{ending}")
        if beam_mrd_coinc:
            p = pathlib.Path(f"{path}R{i}_{label}_{name}.{ending}")
        if not p.is_file():
            counter -= 1
            continue

    return counter


def find_number_events(path: str, label: str, name: str, ending: str = "csv",
                       guess: int = -1) -> int:
    """
    Check all available files, return the amount of single events found in the files
    specified by the parameters of the form
    ~/name/label_#####_name.ending, where '#####' is the corresponding file number. Start attempting
    to load files beginning with the index '0'.

    Warning: This will only find all events in all files, as long as the highest file index is smaller than the number
    of all files in the directory.

    :param path: Directory name (Include forward slash at the end)
    :param label: Label of the data_container, e.g. 'electron_beamlike'
    :param name: What data_container is read in, e.g. 'charge', 'neutron number'
    :param ending: File ending, e.g. 'csv' (without dot). Default = 'csv'
    :param guess: Best guess of number of data_container files. If guess = -1, the function will attempt
    to load all files following the structure above. Default = -1 (will try at most #guess files)
    :return: Returns how many events (that is: entries separated by the delimiter ',' inside the loaded files) have
    been found.
    """
    event_counter = 0
    try:
        os.listdir(path)
    except OSError:
        return -1

    file_counter = guess if guess != -1 else int(len(os.listdir(path)))

    for i in range(file_counter):
        try:
            if name in ["EnergyMuon", "EnergyElectron"]:
                data = load_column(path, f"{label}_{i}_{name}.{ending}", 2)
            else:
                data = np.loadtxt(f"{path}{label}_{str(i)}_{name}.{ending}", delimiter=",")
            event_counter += len(data)
        except OSError:
            file_counter -= 1
            continue

    return event_counter


def concat_data_to_arr(arr: np.array, path: str, label: str, name: str, number_of_files: int = -1, ending: str = "csv"
                       ) -> np.array:
    """
    Takes a np array and concatenates data_container to it, loaded from a specified number of files, according to the
    following pattern:
    ~/name/label_#####_name.ending, where '#####' is the corresponding file number.

    :param arr: np array to be concatenated to, will be returned
    :param number_of_files: How many data_container files will be loaded; set to -1 if all files should be loaded. Default = -1
    :param path: Directory name (Include forward slash at the end)
    :param label: Label of the data_container, e.g. 'electron_beamlike'
    :param name: What data_container is read in, e.g. 'charge', 'neutron number'
    :param ending: File ending, e.g. 'csv' (without dot). Default = 'csv'
    :return: Returns arr, concatenated with data_container
    """

    if number_of_files == -1:
        number_of_files = find_number_files(path, label, name, ending)

    i = 0
    while number_of_files > 1:
        i += 1
        try:
            if name in ["EnergyMuon", "EnergyElectron"]:
                data = load_column(path, f"{label}_{i}_{name}.{ending}", 2)
                # TODO
            else:
                data = np.loadtxt(f"{path}{label}_{str(i)}_{name}.{ending}", delimiter=",")
            arr = np.concatenate([arr, data], axis=0)
            number_of_files -= 1
        except OSError:
            continue

    return arr


def load_data(path: str,
              label: str,
              name: str,
              number_of_files: int = -1,
              ending: str = "csv",
              beam_mrd_coinc: bool = False,
              file_index_edges: List[int] = None,
              verbose: bool = False
              ) -> np.array:
    """
    Similar to concat_data_to_arr, the difference being that an array will be constructed.
    Load data_container to a np array, loaded from a specified number of files, according to the
    following pattern:
    ~/name/label_#####_name.ending, where '#####' is the corresponding file number.

    :param verbose: TODO
    :param file_index_edges: Pass list or tuple of 2 ints to specify max and min file index for loading.
    :param beam_mrd_coinc: TODO
    :param number_of_files: How many data_container files will be loaded; set to -1 if all files should be loaded. Default = -1
    :param path: Directory name (Include forward slash at the end)
    :param label: Label of the data_container, e.g. 'electron_beamlike'
    :param name: What data_container is read in, e.g. 'charge', 'neutron number'
    :param ending: File ending, e.g. 'csv' (without dot). Default = 'csv'
    :return: Returns arr, concatenated with data_container
    """
    arr = []
    if number_of_files == -1:
        number_of_files = find_number_files(path, label, name, ending)
    else:
        number_of_files = number_of_files
    if file_index_edges is not None:
        number_of_files = file_index_edges[1]
        i = file_index_edges[0]
    else:
        i = 0

    break_condition = 1 if file_index_edges is None else file_index_edges[0]

    while number_of_files > break_condition:
        i += 1
        number_of_files -= 1
        try:
            data = []
            if beam_mrd_coinc:
                if name in ["EnergyMuon", "EnergyElectron"]:
                    data = load_column(path, f"R{i}_{label}_{name}.{ending}", 2)
                elif name in ["VisibleEnergy", "Rings", "NeutronNumber"]:
                    data = load_column(path, f"R{i}_{label}_{name}.{ending}", 0)
                elif name in ["MRD"]:
                    data = np.loadtxt(f"{path}R{i}_{label}_{name}.{ending}", delimiter=",")
                    if data.shape == (6,):
                        # explicitly adding the extra dimension using np.array([]) is done to ensure the data is
                        # reshaped into the shape (1, 160) in case of having only a single entry
                        data = np.array([data])
                    np.reshape(data, (-1, 6))
                else:
                    data = np.loadtxt(f"{path}R{i}_{label}_{name}.{ending}", delimiter=",")
                    if data.shape == (160,):
                        # explicitly adding the extra dimension using np.array([]) is done to ensure the data is
                        # reshaped into the shape (1, 160) in case of having only a single entry
                        data = np.array([data])
                    np.reshape(data, (-1, 160))
                try:
                    arr = np.concatenate([arr, data], axis=0) if len(arr) > 0 else data
                except ValueError:
                    # Usually due to a .csv file only containing 1 event
                    if data.shape == (0,):
                        pass
                    else:
                        raise celfa_exceptions.ErrorMismatch
                        pass

            else:
                if name in ["EnergyMuon", "EnergyElectron"]:
                    data = load_column(path, f"{label}_{i}_{name}.{ending}", 2)
                elif name in ["VisibleEnergy", "Rings", "NeutronNumber"]:
                    data = load_column(path, f"{label}_{i}_{name}.{ending}", 0)
                elif name in ["MRD"]:
                    data = np.loadtxt(f"{path}{label}_{i}_{name}.{ending}", delimiter=",")
                    if data.shape == (6,):
                        # explicitly adding the extra dimension using np.array([]) is done to ensure the data is
                        # reshaped into the shape (1, 160) in case of having only a single entry
                        data = np.array([data])
                    np.reshape(data, (-1, 6))
                elif name in ["MuonNumber"]:
                    data1 = load_column(path, f"{label}_{i}_{'EnergyMuon'}.{ending}", 0)
                    data2 = load_column(path, f"{label}_{i}_{'EnergyMuon'}.{ending}", 1)
                    data = np.array(data1) + np.array(data2)
                elif name in ["ElectronNumber"]:
                    data1 = load_column(path, f"{label}_{i}_{'EnergyElectron'}.{ending}", 0)
                    data2 = load_column(path, f"{label}_{i}_{'EnergyElectron'}.{ending}", 1)
                    data = np.array(data1) + np.array(data2)
                elif name in ["PionNumber"]:
                    data1 = load_column(path, f"{label}_{i}_{'EnergyPion'}.{ending}", 0)
                    data2 = load_column(path, f"{label}_{i}_{'EnergyPion'}.{ending}", 1)
                    data3 = load_column(path, f"{label}_{i}_{'EnergyPion'}.{ending}", 2)
                    data = np.array(data1) + np.array(data2) + np.array(data3)
                elif name in ["KaonNumber"]:
                    data1 = load_column(path, f"{label}_{i}_{'EnergyKaon'}.{ending}", 0)
                    data2 = load_column(path, f"{label}_{i}_{'EnergyKaon'}.{ending}", 1)
                    data = np.array(data1) + np.array(data2)
                elif name in ["time"]:
                    data = np.loadtxt(f"{path}{label}_{i}_{name}.{ending}", delimiter=",")
                    data_cpy = []
                    for element in range(len(data)):
                        if sum(data[element]) == 0:
                            data_cpy.append(np.zeros(160 * 1))
                        else:
                            temp_flip = [(0 if not k else 1 - k) for k in data[element]]
                            data_cpy.append(temp_flip)
                    np.reshape(data_cpy, (-1, 160))
                else:
                    data = np.loadtxt(f"{path}{label}_{i}_{name}.{ending}", delimiter=",")
                    if data.shape == (160,):
                        # explicitly adding the extra dimension using np.array([]) is done to ensure the data is
                        # reshaped into the shape (1, 160) in case of having only a single entry
                        data = np.array([data])
                    np.reshape(data, (-1, 160))
                try:
                    arr = np.concatenate([arr, data], axis=0) if len(arr) > 0 else data
                except ValueError:
                    # Usually due to a .csv file only containing 1 event
                    raise celfa_exceptions.ErrorMismatch
                    pass

        except OSError:
            if beam_mrd_coinc:
                if verbose:
                    print(f"Call to load_data_to_arr (name,{label}_{i}_{name}.{ending}): file not found")
            else:
                if verbose:
                    print(f"Call to load_data_to_arr ({path}{label}_{i}_{name}.{ending}): file not found")
            continue

    return arr


def load_time_data(path: str, label: str, number_of_files: int = -1, ending="csv") -> np.array:
    """
    TODO: add file index edges (see load_data)
    Similar to concat_time_data, the difference being that an array will be constructed.
    Special util function to load in time data_container files, specified by the pattern
    ~/name/label_#####_name.ending, where '#####' is the corresponding file number. The optional parameter
    'number_of_files' specifies how many files should be loaded, leave empty for all possible files in the directory.
    Invert order of high time values <-> low time values, by inverting the interval [0,1] to [1,0] (range of data_container).
    Also check for sum of elements of charge data_container of an event to be 0, if so, append empty arr.

    Take in an array, to which the loaded time data_container will be appended. Compare "concat_data_to_arr".

    :param ending: File ending. Default = "csv"
    :param path: Directory name (Include forward slash at the end)
    :param label: Label of the data_container, e.g. 'electron_beamlike'
    :param number_of_files: How many data_container files will be loaded; set to -1 if all files should be loaded. Default = -1
    :return: time_val, with loaded time data_container appended to it. (time)
    """
    arr = np.zeros((0, 160))

    if number_of_files == -1:
        number_of_files = find_number_files(path, label, "charge")

    i = 0
    while number_of_files > 1:
        # 'mismatch_flag' monitors which of the 2 files (time, charge) could not be loaded - if only one
        # of the files could not be loaded (mismatch in data_container files), it will raise a critical error.
        mismatch_flag = 0
        i += 1
        try:
            training_data_list_t = np.loadtxt(f"{path}{label}_{i}_time.{ending}", delimiter=",")
        except OSError:
            print(f"Call to concat_time_data ({path}{label}_{i}_time.{ending}): "
                  f"file not found")
            mismatch_flag += 1
            continue
        try:
            training_data_list_c = np.loadtxt(f"{path}{label}_{i}_charge.{ending}", delimiter=",")
        except OSError:
            mismatch_flag += 1
            print(f"Call to concat_time_data ({path}{label}_{i}_charge.{ending}): file not found")
            continue

        if mismatch_flag > 1:
            print(f"Call to concat_time_data ({path}{label}_{i}): data_container mismatch error!")
            raise celfa_exceptions.ErrorMismatch

        loaded_from_csv = []
        for element in range(len(training_data_list_t)):
            if sum(training_data_list_c[element]) == 0:
                loaded_from_csv.append(np.zeros(160 * 1))
            else:
                # TODO: this
                temp_flip = [(0 if not k else 1 - k) for k in training_data_list_t[element]]
                loaded_from_csv.append(temp_flip)

        loaded_from_csv = np.array(loaded_from_csv)
        # TODO: check if np.array is a better solution for ragged data_container shapes
        arr = [*arr, *loaded_from_csv]
        number_of_files -= 1

    print(f"Call to concat_time_data ({path}{label}): executed successfully")
    return arr


def concat_time_data(arr: np.array, path: str, label: str, number_of_files: int = -1) -> np.array:
    """
    Special util function to load in time data_container files, specified by the pattern
    ~/name/label_#####_name.ending, where '#####' is the corresponding file number. The optional parameter
    'number_of_files' specifies how many files should be loaded, leave empty for all possible files in the directory.
    Invert order of high time values <-> low time values, by inverting the interval [0,1] to [1,0] (range of data_container).
    Also check for sum of elements of charge data_container of an event to be 0, if so, append empty arr.

    Will take in an array, to which the loaded time data_container will be appended. Compare "concat_data_to_arr".

    :param path: Directory name (Include forward slash at the end)
    :param label: Label of the data_container, e.g. 'electron_beamlike'
    :param arr: np array to which the time data_container will be concatenated.
    :param number_of_files: How many data_container files will be loaded; set to -1 if all files should be loaded. Default = -1
    :return: time_val, with loaded time data_container appended to it. (time)
    """
    if number_of_files == -1:
        number_of_files = find_number_files(path, label, "charge")

    i = 0
    while number_of_files > 1:
        # 'mismatch_flag' monitors which of the 2 files (time, charge) could not be loaded - if only one
        # of the files could not be loaded (mismatch in data_container files), it will raise a critical error.
        mismatch_flag = 0
        i += 1
        try:
            training_data_list_t = np.loadtxt(f"{path}{label}_{str(i)}_time.csv", delimiter=",")
        except OSError:
            print(f"Call to concat_time_data ({path}{label}_{str(i)}_time.csv): file not found")
            mismatch_flag += 1
            continue
        try:
            training_data_list_c = np.loadtxt(f"{path}{label}_{str(i)}_charge.csv", delimiter=",")
        except OSError:
            mismatch_flag += 1
            print(f"Call to concat_time_data ({path}{label}_{str(i)}_charge.csv): file not found")
            continue

        if mismatch_flag > 1:
            print(f"Call to concat_time_data ({path}{label}_{str(i)}): data_container mismatch error!")
            raise celfa_exceptions.ErrorMismatch

        loaded_from_csv = []
        for element in range(len(training_data_list_t)):
            if sum(training_data_list_c[element]) == 0:
                loaded_from_csv.append(np.zeros(160 * 1))
            else:
                # TODO: this
                temp_flip = [(0 if not k else 1 - k) for k in training_data_list_t[element]]
                loaded_from_csv.append(temp_flip)

        loaded_from_csv = np.array(loaded_from_csv)
        arr = np.concatenate([arr, loaded_from_csv], axis=0)
        number_of_files -= 1

    return arr


def zip_data(data_sets: list) -> list:
    """
    Zip multiple data_container sets at once, return the zipped data_container sets.

    Note: This is a free, single standing function since it relies on the behaviour of zip(). Specifically, the property
    that only as many elements as the length of the shortest list will be zipped together, is used. This allows for
    easy test-implementation, and using the code in an older version of python, or if the behaviour of zip() is changed,
    it is easier to debug, since only this singular function will break.

    :param data_sets: List of data_container (in the form of arrays)
    :return: np.array of zipped data_sets
    """
    return list(zip(*data_sets))


def construct_data_array(data_names, path: str, label: str, number_of_files: int = -1,
                         ending: str = "csv", load_from_config=False,
                         file_index_edges: List[int] = None, beam_mrd_coinc: bool = False) -> np.array:
    """
    Return zipped data_container sets in the order specified by data_names. Use "time" to load time, using the special
    load_time_data function. The order in which the data_container sets will be zipped is the order of the entries in data_names.

    The file name is given by ~/name/label_#####_name.ending, where '#####' is the corresponding file number.

    Note: Also automatically appends the appropriate data_container identifier (1, 0) for electron, (0, 1) for muon.
    :param file_index_edges: Pass list or tuple of 2 ints to specify max and min file index for loading.
    :param beam_mrd_coinc: TODO
    :param ending: File ending, e.g. 'csv' (without dot). Default = 'csv'
    :param data_names: List of file names which will be loaded, e.g. 'charge', 'neutron_number', 'time'.
    :param path: Directory name (Include slash at the end)
    :param label: Label of the data_container, e.g. 'electron_beamlike'
    :param number_of_files: How many data_container files will be loaded; set to -1 if all files should be loaded. Default = -1
    :param load_from_config: TODO: specify from which config file will be loaded, and support loading from config file
    this should essentially replace data_names. This will allow for having multiple configs ready, and training
    a plethora of models in one go with different data_container configs.
    Default = False.
    :return: After loading, return all data_container sets zipped together, using zip(). Length of the data_container sets will be cut to
    that of the shortest data_container set.
    """
    loaded_data = []
    for name in data_names:
        if name in ["time", "time_abs"]:
            loaded_data.append(load_data(path, label, name, number_of_files=number_of_files,
                                         ending=ending, beam_mrd_coinc=beam_mrd_coinc,
                                         file_index_edges=file_index_edges))
        else:
            loaded_data.append(load_data(path, label, name, number_of_files=number_of_files,
                                         ending=ending, beam_mrd_coinc=beam_mrd_coinc,
                                         file_index_edges=file_index_edges))

        # Should be unnecessary since zip_data() ensures that each list is the same length, but gives peace of mind
        length = len(loaded_data[0])
        if not all(len(d) == length for d in loaded_data):
            print("Call to construct_data_array: Mismatch in data_container length!")
            raise celfa_exceptions.ErrorMismatch

    return zip_data(loaded_data)


def concat_min_array(*darrs: list) -> list:
    """
    Join and return multiple arrays such that as many entries of each array are joined together as the shortest array
    contains. This is useful if an unknown number of events from different categories are loaded into different arrays,
    but each category is wanted to contain the same amount of events after being concatenated.

    >>> concat_min_array([1, 2, 3, 4, 5], [1, 1, 1], [0, 1, 3, 4])
    [[1, 2, 3], [1, 1, 1], [0, 1, 3]]

    :param darrs: Arbitrary number of arrays
    :return: Return multiple arrays such that as many entries of each array are joined together as the shortest array
    contains
    """
    min_l = len(darrs[0])
    for d in darrs:
        if len(d) < min_l:
            min_l = len(d)
    return [d[:min_l] for d in darrs]


def build_category_values(categories: list, num: int) -> list:
    """
    Return a list of category values specified in categories. Appends in order given when calling the function. num
    specifies how many data_container points are in each category. Assumes every category is the same length!

    :param categories: Specifier for category values; e.g. (1, 0) for electron, (0, 1) for muon -> [(1,0), (0,1)].
    :param num: How many identifiers for each category.
    :return: List of all category values appended to each other; ordering is specified by ordering of the parameter
    categories.
    """
    category_values = []
    for category in categories:
        [category_values.append(category) for __ in range(num)]

    return category_values


def load_column(path: str, filename: str, col: int, delimiter: str = ",", fill_empty: bool = True,
                fill_value: float = 0.0) -> List:
    """Return the n-th column of a csv-like file."""
    data = []
    with open(f"{path}{filename}", "r") as f:
        for line in f:
            # to avoid empty values in data_container
            if not (line.split(delimiter))[col] or (line.split(delimiter))[col] == "\n" and fill_empty:
                val = float(fill_value)
            else:
                val = float((line.split(delimiter))[col])
            data.append(val)
        return data


def save_data(path: str, filename: str, data: object, ending: str = "pickle"):
    """Dump data_container into file using pickle."""
    try:
        pickle_out = open(f"{path}{filename}.{ending}", "wb")
    except OSError:
        print(f"save_data: Could not open file {path}{filename}.{ending}")
        return
    pickle.dump(data, pickle_out, protocol=4)
    pickle_out.close()


def load_and_create_train_val_test_sets(data, category_values, percentages=None):
    """
    Shuffle and create train, validation and test data_container sets. The relative size can be defined by using the 'percentages'
    parameter. The returned arrays will be of the form (data_container, category_values) where data_container is of the form
    (data1, data2, data3) etc.
    """
    if percentages is None:
        percentages = [0.7, 0.15, 0.15]

    arr = list(zip(data, category_values))
    random.shuffle(arr)

    length = len(data)

    train = arr[:int(percentages[0] * length)]
    validation = arr[int(percentages[0] * length):int(percentages[0] * length) + int(percentages[1] * length)]
    test = arr[int(percentages[0] * length) + int(percentages[1] * length):
               int(percentages[0] * length) + int(percentages[1] * length) + int(percentages[2] * length)]
    return train, validation, test


def split_data_cat(data):
    s_data, s_cat = [], []
    for entry in data:
        s_data.append(entry[0])
        s_cat.append(entry[1])
    return s_data, s_cat


def select_data(data, indices):
    s_data = []

    for entry in data:
        temp = []
        for index in indices:
            temp.append(entry[index])
        s_data.append(temp)
    return s_data


def reshape_data_entry(data, index, shape):
    """Select a data_container type from data_container and reshape using np.reshape()"""
    selected_data = np.array(select_data(data, [index])).reshape(shape)
    new_shaped_data = []

    if index == 0:
        all_except_first_data = select_data(data, [r for r in range(index + 1, len(data[0]))])
        for i in range(0, len(selected_data)):
            j = [selected_data[i], *(all_except_first_data[i])]
            new_shaped_data.append(j)

    elif index == (len(data[0]) - 1):
        all_except_last_data = select_data(data, [r for r in range(0, len(data[0]) - 1)])
        for i in range(0, len(selected_data)):
            j = [*(all_except_last_data[i]), selected_data[i]]
            new_shaped_data.append(j)

    else:
        all_up_to_index_data = select_data(data, [r for r in range(0, index)])
        all_after_index_data = select_data(data, [r for r in range(index + 1, len(data[0]))])
        for i in range(0, len(selected_data)):
            j = [*(all_up_to_index_data[i]), selected_data[i], *(all_after_index_data[i])]
            new_shaped_data.append(j)

    return new_shaped_data


# data_container set stuff
def dataset_stats(data_names: List[str],
                  path: str = None,
                  label: str = None,
                  number_of_files: int = -1,
                  file_index_edges: List[int] = None,
                  beam_mrd_coinc: bool = False,
                  data=None):
    """TODO DOCSTR"""
    if path is not None and label is not None:
        data = construct_data_array(data_names, path, label, number_of_files=number_of_files,
                                    file_index_edges=file_index_edges, beam_mrd_coinc=beam_mrd_coinc)
    else:
        data = data

    total_events = len(data)
    print("Total # of events: ", total_events)

    for entry in data_names:
        if entry == "charge":
            # charge stats
            charge_data = [x[data_names.index(entry)] for x in data]
            charge_null_sum = 0
            for c in charge_data:
                if np.sum(c) == 0:
                    charge_null_sum += 1
            print("Events with 0 charge sum: ", charge_null_sum)

        if entry == "VisibleEnergy":
            # vis energy stats
            vis_energy_data = [x[data_names.index(entry)] for x in data]
            vis_energy_average = np.average(vis_energy_data)
            vis_energy_median = np.median(vis_energy_data)

            print("Vis energy average: ", vis_energy_average)
            print("Vis energy median: ", vis_energy_median)

        elif entry == "Rings":
            # ring stats
            ring_data = [x[data_names.index(entry)] for x in data]
            ring_average = np.average(ring_data)
            ring_median = np.median(ring_data)

            print("Ring count average: ", ring_average)
            print("Ring count median: ", ring_median)

            sr_count, mr_count, null_r_count, negative_r_count = 0, 0, 0, 0
            sr_events, mr_events = [], []
            for event in data:
                if event[data_names.index(entry)] > 1:
                    mr_count += 1
                    mr_events.append(event)
                elif event[data_names.index(entry)] == 1:
                    sr_count += 1
                    sr_events.append(event)
                elif event[data_names.index(entry)] == 0:
                    null_r_count += 1
                elif event[data_names.index(entry)] < 0:
                    negative_r_count += 1

            print("SR events: ", sr_count)

            if "VisibleEnergy" in data_names:
                print("Average SR visible energy: ",
                      np.average([x[data_names.index("VisibleEnergy")] for x in sr_events]))
                print("Median SR visible energy: ",
                      np.median([x[data_names.index("VisibleEnergy")] for x in sr_events]))
            print("MR events: ", mr_count)

            if "VisibleEnergy" in data_names:
                print("Average MR visible energy: ",
                      np.average([x[data_names.index("VisibleEnergy")] for x in mr_events]))
                print("Median MR visible energy: ",
                      np.median([x[data_names.index("VisibleEnergy")] for x in mr_events]))
            print("Null ring events: ", null_r_count)
            print("Negative ring events: ", negative_r_count)

        elif entry == "EnergyElectron":
            # electron stats
            electron_energy_data = [x[data_names.index(entry)] for x in data]
            to_be_removed = np.array([0])
            cleaned_electron_energy_data = np.setdiff1d(electron_energy_data, to_be_removed)

            electron_energy_cleaned_average = np.average(cleaned_electron_energy_data)
            electron_energy_cleaned_median = np.median(cleaned_electron_energy_data)

            print("Number of electron events: ", len(cleaned_electron_energy_data))
            print("Electron energy average (cleaned, no '0' entries): ", electron_energy_cleaned_average)
            print("Electron energy median (cleaned, no '0' entries): ", electron_energy_cleaned_median)

        elif entry == "EnergyMuon":
            # muon stats
            muon_energy_data = [x[data_names.index(entry)] for x in data]
            to_be_removed = np.array([0])
            cleaned_muon_energy_data = np.setdiff1d(muon_energy_data, to_be_removed)

            muon_energy_cleaned_average = np.average(cleaned_muon_energy_data)
            muon_energy_cleaned_median = np.median(cleaned_muon_energy_data)

            print("Number of muon events: ", len(cleaned_muon_energy_data))
            print("Muon energy average (cleaned, no '0' entries): ", muon_energy_cleaned_average)
            print("Muon energy median (cleaned, no '0' entries): ", muon_energy_cleaned_median)

        elif entry == "NeutronNumber":
            # muon stats
            neutron_data = [x[data_names.index(entry)] for x in data]

            neutron_count_average = np.average(neutron_data)
            neutron_count_median = np.median(neutron_data)

            print("Average neutron count: ", neutron_count_average)
            print("Median neutron count: ", neutron_count_median)


@dataclass
class ExperimentalData:
    """Wrapper for loaded experimental data_container.

    data_container is a list of lists, which contain the different data_container types.
    data_dict is of the form {"charge": 1, "MRD": 2}, and contains information about retrieval of data_container.
    stats_data_indices uses the same mapping defined in data_dict, and indicates which of the data_container is loaded only for
        statistical purposes (the model has not been trained which this data_container), e.g. "VisibleEnergy", "Rings"
    net_data_indices: see stats_data_indices. The difference being, that these indices define the data_container with which the
        model has been trained. E.g. "charge" and "MRD"
    input_layers: dictionary which describes the model's input layers. The keys are the name of data_container / input layer,
        the values correspond to the input shapes.
        This describes which data_container is loaded; data_container also needs to have same name as described in data_dict.
         Compare evaluating a functional model:
            fun.evaluate({"mrd": data_mrd, "charge": data_charge}, y)
        The input layers of the model also need to carry the same name / identifier as the keys.
        Example:
            input_layers = {"MRD": (-1, 1, 6), "charge": (-1, 10, 16, 1)}
    """
    net_data_indices: List[int]
    stats_data_indices: List[int]
    data_dict: dict
    data: List[np.array]
    input_layers: dict

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        """Returns an iterator over the data in the ExperimentalData object."""
        return iter(self.data)

    def __contains__(self, item):
        """Returns True if the item is in the data list, False otherwise."""
        return item in self.data

    def __getitem__(self, index):
        """Returns the data at the specified index in the data list."""
        return self.data[index]

    def relu_cut(self,
                 index: int = None,
                 data_name: str = None,
                 offset: float = 0):
        """
        Defines ReLU(x) on every event, for the datapoint specified by index. Offset will act like ReLU(x-offset).
        """
        if index is not None:
            pass
        elif data_name is not None:
            index = self.data_dict[data_name]

        try:
            for e in range(len(self)):
                for d in range(len(self.data[e][index])):
                    if self.data[e][index][d] > offset:
                        continue
                    else:
                        self.data[e][index][d] = 0

        except IndexError:
            print("No viable index / data_name provided."
                  " Cannot access data[i][index] or data[i][data_dict['data_name']].")

    def calculate_norm_charge_map(self,
                                  norm_charge_map_index: int,
                                  abs_charge_map_index: int):
        """
        Calculates the normalized charge map. Needs index of where the normalized charge map will be saved to, and
        where the absolute charge map can be found in data.
        """
        new_data = []

        for e in range(len(self)):
            if max(self.data[e][abs_charge_map_index]) == 0:
                continue

            temp_data = self.data[e][abs_charge_map_index] / max(self.data[e][abs_charge_map_index])

            for d in range(len(self.data[e][norm_charge_map_index])):
                self.data[e][norm_charge_map_index][d] = temp_data[d]

            new_data.append(self.data[e])

        self.data = new_data

    def sum_chargemap(self, norm=False):
        """Sum all charge maps and return the summed entries. Choose either the normalised or absolute charge map."""
        summed_chargemap = np.zeros(shape=160)
        index = self.data_dict["charge"] if norm else self.data_dict["charge_abs"]

        for i in range(len(self)):
            for j in range(160):
                summed_chargemap[j] += self.data[i][index][j]

        return summed_chargemap

    def create_active_int_array(self):
        """Return numpy int array with a '1' entry equaling to 'active' PMTs, '0' to inactive."""
        summed_chargemap = self.sum_chargemap(norm=False)
        active_map = np.zeros(160)

        for i in range(160):
            active_map[i] = 1 if bool(summed_chargemap[i]) else 0

        return active_map

    def plot_active_pmts(self, return_fa=False):
        """Plot a map of active PMTs. Also print and return a list of inactive PMTs. If the figure and ax are to be
           returned, inactive PMTs and fig, ax are returned as a list: [inactive PMTs, (fig, ax)]."""
        summed_chargemap = self.sum_chargemap(norm=False)
        active_map = self.create_active_int_array()

        inactive_list = np.where(active_map == 0)
        print(f"Inactive PMTs: {inactive_list}")

        fig, ax = plt.subplots(1, 1)
        ax.imshow(active_map.reshape((10, 16)), origin="lower")

        if return_fa:
            return [inactive_list, (fig, ax)]
        else:
            return inactive_list

    def check_active_chargemap_equal(self, other):
        """Return true if active chargemap is equal of this object and the supplied other. If false also print differing
           PMT indices."""
        different = []
        equal = True
        self_active = self.create_active_int_array()
        other_active = other.create_active_int_array()

        for i in range(160):
            if self_active[i] != other_active[i]:
                different.append(i)
                equal = False

        print(f"The provided data containers don't match in terms of active PMTs in these positions: {different}")
        return equal

    def blackout_pmts(self, indices: List):
        """Blackout all pmts specified by the indices provided. Set all entries of the positions specified by indices
            for every event to 0 in normalised and absolute maps."""
        for j in range(160):
            for i in range(len(self)):
                if j in indices:
                    self.data[i][self.data_dict["charge"]][j] = 0
                    self.data[i][self.data_dict["charge_abs"]][j] = 0

        self.calculate_norm_charge_map(norm_charge_map_index=self.data_dict["charge"],
                                       abs_charge_map_index=self.data_dict["charge_abs"])

    def plot_saliency_map(self, model, index, save=False, filename=None, return_map=False):
        # TODO: Docstr
        # Get the charge data for the specified datapoint
        charge_data = self.data[index][self.data_dict["charge"]]

        # Generate the saliency map
        saliency_map = keras.backend.gradients(model.output, model.input)[0]
        saliency_map = saliency_map[0].numpy()

        # Reshape the saliency map to a 2D array
        saliency_map = np.reshape(saliency_map, (10, 16))

        # Plot the saliency map
        plt.imshow(saliency_map, cmap="jet", origin="lower")
        plt.colorbar()
        plt.title("Saliency Map")

        if save:
            # Save the plot as a PNG and PDF
            if filename is None:
                filename = "saliency_map"
            plt.savefig(f"{filename}.png", dpi=300)
            plt.savefig(f"{filename}.pdf")

        elif return_map:
            return saliency_map

        if return_map:
            plt.show()


@dataclass
class SimulationData(ExperimentalData):
    """Wrapper for loaded simulation data_container, inherits from ExperimentalData

    category_values is just a list of category values corresponding to the loaded data_container.
    """
    category_values: List
    cat_values_dict: dict

    def calculate_norm_charge_map(self,
                                  norm_charge_map_index: int,
                                  abs_charge_map_index: int):
        """
        Calculates the normalized charge map. Needs index of where the normalized charge map will be saved to, and
        where the absolute charge map can be found in data.
        """
        new_data = []
        new_catvals = []

        for e in range(len(self)):
            if max(self.data[e][abs_charge_map_index]) == 0:
                continue

            temp_data = self.data[e][abs_charge_map_index] / max(self.data[e][abs_charge_map_index])

            for d in range(len(self.data[e][norm_charge_map_index])):
                self.data[e][norm_charge_map_index][d] = temp_data[d]

            new_data.append(self.data[e])
            new_catvals.append(self.category_values[e])

        self.data = new_data
        self.category_values = new_catvals
