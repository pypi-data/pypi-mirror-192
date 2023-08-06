# STL
import os
import itertools
from typing import Union, List, Tuple
from pathlib import Path

# 3rd party
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.patches
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import sklearn.metrics
from sklearn.metrics import roc_auc_score, roc_curve, auc
import statsmodels.stats.proportion as sm

# Home-made
import celfa_data
import celfa_exceptions


########################################################################################################################
# CELFA - CNN Evaluation Library For ANNIE
# ----------------------------------------
# This file encapsulates the CNN-Class and its methods to load, organize, plot and to interpret the net's performance.
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

class Evaluator:
    """Load, organize, plot and interpret the trained model."""

    def __init__(self,
                 model_path: str = None,
                 model=None,
                 model_name: str = None,
                 test_data: list = None,
                 test_cat_values: list = None,
                 net_data_indices: list = None,
                 stats_data_indices: list = None,
                 cat_values_dict: dict = None,
                 data_dict: dict = None,
                 mute_tf_info: bool = True,
                 real_test_data: bool = False,
                 reshape_data: bool = False,
                 mode: str = "em",
                 data_container: Union[celfa_data.ExperimentalData, celfa_data.SimulationData] = None,
                 override_real_test_data_flag: bool = None) -> None:  # TODO: Override_real_test_data_flag..
        """
        Used for high-level evaluation and presentation of data_container, meant as an easy way to evaluate model performance.
        Requires at least model_path. The model will be loaded into self.model as a keras.model. To access plotting
        functionality, data_dict and stats_data_indices needs to be provided.
        ----------------------------------------------------------------------------------------------------------------
        An example for creating an Evaluator object, and some basic functionality:
        ev = Evaluator(model_path="PATH",
                       model_name="Example_evaluator",
                       test_data=test_data_set,
                       net_data_indices=[0, 1],
                       stats_data_indices=[2, 3],
                       cat_values_dict={"Electron": [1, 0], "Muon": [0, 1]},
                       data_dict={"Charge": 0, "Time": 1, "Energy": 2, "VisibleEnergy": 3})
        In this example. Charge and time data_container has been used for training (net_data_indices=[0,1]) and "Energy" as well
        as "VisibleEnergy" will be used by the Evaluator to plot histograms, prediction accuracy vs "Energy"
        or "VisibleEnergy" etc. data_dict defines the keys by which data_container will be accessed. For example,
        ev.plot_histogram("VisibleEnergy")
        will plot a histogram of the data_container located at position data_dict["VisibleEnergy"] = 3 of the data_container given in
        test_data.
        ----------------------------------------------------------------------------------------------------------------
        Some other basic examples:
        -----
        ev.plot_confusion_matrix(savefig=True, normalized=False, title="CM Absolute", filename="cm_xxx")
        -> This will plot the non-normalized confusion matrix with the title "CM Absolute", and saves it in the current
            directory as "cm_xxx.pdf"
        -----
        ev.plot_histogram("VisibleEnergy", category=["Muon", "Electron"], bins=100, histtype=["step", "bar"])
        -> This will plot two histograms in the same plot of VisibleEnergy for Muon and Electron events, using 100 bins
            and the style of the Muon plot being "step" (matplotlib.pyplot), and similarly, the style of the Electron
            plot being "bar".
        -----
        ev.plot_accuracy("VisibleEnergy", category="Muon")
        -> This will plot Muon VisibleEnergy vs. model prediction accuracy.
        ----------------------------------------------------------------------------------------------------------------
        :rtype: None
        :return: None
        :param mode: Specifies the mode of operation. 'em' -> e/mu classification; 'rc' -> ring counting/classification
        :param mute_tf_info: If set to true, disable printing of tf info.
        :param model_name: Name of the model
        :param test_data: Data with which the model shall be evaluated. The Evaluator expects a tuple of the shape
            (data_container, category values).
        :param stats_data_indices: Requires a list of indices which correspond to what data_container will be used to evaluate the
            model. This includes one-dimensional data_container which has not been used for training, e.g. "VisualEnergy", but not
            data_container like "Charge" or "Time". The Evaluator will access data_container when calling methods by using the keys defined
            in data_dict. See the example in the docstring.
        :param test_cat_values: Array or list of true category values of test data_container.
        :param data_dict: Dictionary which documents the structure of the data_container provided in test_data. Keys are data_container
            types like "VisibleEnergy" or "Charge" etc. Further functionality of the Evaluator Class is accessed by
            using these keywords.
        :param net_data_indices: Include a list of indices of which parts of the data_container have been used to train the net.
            For example: If training has been done using charge and time data_container, but the data_container provided is
            [charge, time, EnergyMuon], then setting 'net_data_indices = [0, 1]' will tell the Evaluator that the net
            has been only trained with charge and time data_container.
        :param net_data_indices: Same as 'net_data_indices', but for all the data_container that has not been given to train the
            net. For example: EnergyMuon -> for histograms only.
        :param cat_values_dict: A dictionary which translates category value tuples of the form (0, 1) etc. to
            human-readable identifiers such as "Electron". Default = None.
        :param model_path: full name.
        :param real_test_data: Set to true if the network is used on new, real data_container, without category values.
        :param reshape_data: Specify if data_container is to be reshaped.
        """

        if override_real_test_data_flag:
            if real_test_data is not None:
                self.real_test_data = real_test_data
            else:
                self.real_test_data = False
        else:
            if type(data_container) == celfa_data.ExperimentalData:
                self.real_test_data = True
            elif type(data_container) == celfa_data.SimulationData:
                self.real_test_data = False
            else:
                self.real_test_data = real_test_data
        if mute_tf_info:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

        # instantiation
        self.data_dict = data_dict
        self.model_path = model_path
        self.model_name = model_name
        self.__test_data_original = test_data
        self.test_category_values = test_cat_values
        self.net_data_indices = net_data_indices
        self.stats_data_indices = stats_data_indices
        self.mode = mode
        self.data_container = data_container

        if type(self.data_container) is celfa_data.SimulationData:
            self.category_values_dict = self.data_container.cat_values_dict
        else:
            self.category_values_dict = cat_values_dict

        # Instantiated for other methods.
        #
        # The creation of test_data, test_category_values needs to be rewritten / checked when celfa_data.split_data_cat
        #   is changed. Consider moving the functionality of this operation to method, for better readability and
        #   overview. __test_data_original needs to exist this way since for example stats_data depends on the original
        #   shape of test_data.
        if not self.real_test_data:
            if type(self.data_container) == celfa_data.SimulationData:
                self.test_category_values = np.array(data_container.category_values)
            else:
                self.__test_data_original, self.test_category_values = celfa_data.split_data_cat(
                    self.__test_data_original)
                self.test_category_values = np.array(self.test_category_values)

        # Fields to be filled
        self.stats_dict = {}
        self.stats_data = None
        self.unique_categories = None
        self.counts_per_category = None
        self.score = None
        self.efficiency = None
        self.accuracy = None
        self.purity = None
        self.rounded_labels = None
        self.y_prob = None
        self.y_classes = None
        self.cm = None
        self.cm_normalized = False
        self.__predicted_category_values = []
        self.__reshape_data = reshape_data

        # Model loading
        if model is None:
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            self.model = model
        self.predicted = None

        # Calculation of parameters and statistics, and preparation of data_container
        self.__create_stats_dict()
        self.__create_test_data()
        self.__create_stats_data()
        self.__calculate_y_prob()
        self.__create_predicted_category_values()
        self.__join_predicted_and_category_values_and_stats_data()
        if not self.real_test_data:
            self.__calculate_efficiency_accuracy_purity_count_categories_cm()
        else:
            # self.stats_data = [self.stats_data]
            pass

    def __create_stats_dict(self) -> None:
        """
        Initialize 'self.stats_dict' from 'self.stats_data_indices'. This translates the indices from test_data to the
        ordering of stats_data.
        """
        if self.data_container:
            i = 0
            for key in self.data_container.data_dict:
                if self.data_container.data_dict[key] in self.data_container.stats_data_indices:
                    self.stats_dict[key] = i
                    i += 1
        else:
            i = 0
            for key in self.data_dict:
                if self.data_dict[key] in self.stats_data_indices:
                    self.stats_dict[key] = i
                    i += 1

    def __create_test_data(self) -> None:
        """Initialize test_data from test_data selected by net_data_indices."""
        if type(self.data_container) == celfa_data.ExperimentalData \
                or type(self.data_container) == celfa_data.SimulationData:
            if self.data_container.input_layers:
                test_data_dict = {}
                for key in self.data_container.input_layers:
                    test_data_dict[key] = np.array([*celfa_data.select_data(self.data_container.data,
                                                                            [self.data_container.data_dict[key]])])
                    test_data_dict[key] = test_data_dict[key].reshape(self.data_container.input_layers[key])
                self.test_data = test_data_dict
            else:
                self.test_data = np.array(
                    celfa_data.select_data(self.data_container.data, self.data_container.net_data_indices))
                # TODO: Adapt for multiple data_container inputs
                self.test_data = self.test_data.reshape(-1, *self.test_data.shape[2:])

        elif self.real_test_data:
            s_data = []

            for i in range(len(self.__test_data_original)):
                temp = []
                for index in self.net_data_indices:
                    temp.append(self.__test_data_original[i][index])
                s_data.append(temp)
            if self.__reshape_data:
                self.test_data = (np.array(s_data)).reshape((-1, 10, 16, len(self.net_data_indices)))
            else:
                self.test_data = np.array(s_data)

        elif not self.real_test_data:
            self.test_data = np.array(celfa_data.select_data(self.__test_data_original, self.net_data_indices))
            if self.__reshape_data:
                self.test_data = self.test_data.reshape((-1, 10, 16, len(self.net_data_indices)))

    def __create_stats_data(self) -> None:
        """Initialize stats_data from test_data selected by stats_data_indices."""
        # if self.stats_dict is None:
        #    return

        if self.data_container is None:
            s_data = []

            for i in range(len(self.__test_data_original)):
                temp = []
                for index in self.stats_data_indices:
                    temp.append(self.__test_data_original[i][index])
                s_data.append(temp)
            self.stats_data = s_data

        elif type(self.data_container) == celfa_data.ExperimentalData \
                or type(self.data_container) == celfa_data.SimulationData:
            self.stats_data = celfa_data.select_data(self.data_container.data, self.data_container.stats_data_indices)

        else:
            self.stats_data = celfa_data.select_data(self.__test_data_original, self.stats_data_indices)

    def __create_predicted_category_values(self) -> None:
        """Create predicted category values based on network prediction of test data_container. This needs to be adapted for
        different network outputs."""
        if self.mode == "em":
            for i in range(len(self.y_prob)):
                if self.y_prob[i][0] >= 0.5:
                    self.__predicted_category_values.append(self.category_values_dict["Electron"])
                else:
                    self.__predicted_category_values.append(self.category_values_dict["Muon"])
        elif self.mode == "rc":
            for i in range(len(self.y_prob)):
                if self.y_prob[i][0] >= 0.5:
                    self.__predicted_category_values.append(self.category_values_dict["MR"])
                else:
                    self.__predicted_category_values.append(self.category_values_dict["SR"])

    def __join_predicted_and_category_values_and_stats_data(self) -> None:
        """Take predicted category values, and zip it to only the data_container."""
        # whatever you do, do not change the order of zip's. This WILL break all methods dependent on self.stats_data,
        # since the order is crucial.
        if self.real_test_data:
            if self.stats_dict is None:
                self.stats_data = list(zip([0 for _ in range(len(self.__predicted_category_values))],
                                           [0 for _ in range(len(self.__predicted_category_values))],
                                           self.y_prob,
                                           self.__predicted_category_values))
            else:
                self.stats_data = list(zip(self.stats_data,
                                           [0 for _ in range(len(self.__predicted_category_values))],
                                           self.y_prob,
                                           self.__predicted_category_values))
        else:
            if self.stats_dict is None:
                self.stats_data = list(zip([0 for _ in range(len(self.__predicted_category_values))],
                                           self.test_category_values,
                                           self.y_prob,
                                           self.__predicted_category_values))
            else:
                self.stats_data = list(zip(self.stats_data,
                                           self.test_category_values,
                                           self.y_prob,
                                           self.__predicted_category_values))

    def __calculate_y_prob(self) -> None:
        """Calculate the classification probability for each test_data entry."""
        if self.data_container:
            self.y_prob = np.array(self.model.predict(self.test_data, batch_size=100, verbose=0))
        else:
            self.y_prob = np.array(self.model.predict(self.test_data, batch_size=100, verbose=0))

    def __calculate_efficiency_accuracy_purity_count_categories_cm(self) -> None:
        """
        Count entries per category and number of unique categories. Calculate accuracy, purity and the confusion matrix.
        Private method that will be called upon construction of the Evaluator class object.
        """

        # TODO: Split this method up into smaller chunks, so it's easier to edit in the future or to adjust to other
        #   network architectures.
        _, self.counts_per_category = np.unique(self.test_category_values,
                                                return_counts=True, axis=0)

        self.unique_categories = [self.category_values_dict[key] for key in self.category_values_dict]

        self.rounded_labels = np.argmax(self.test_category_values, axis=1)
        self.y_classes = self.y_prob.argmax(axis=-1)
        self.cm = sklearn.metrics.confusion_matrix(self.rounded_labels, self.y_classes)
        self.cm_normalized = self.cm.astype('float') / self.cm.sum(axis=1)[:, np.newaxis]

        self.efficiency = self.cm[1][1] / (self.cm[1][1] + self.cm[1][0])
        self.accuracy = (self.cm[0][0] + self.cm[1][1]) / (self.cm[0][0] + self.cm[0][1] +
                                                           self.cm[1][0] + self.cm[1][1])
        self.purity = self.cm[1][1] / (self.cm[1][1] + self.cm[0][1])

    def recalc_cm_etc(self):
        self.__calculate_efficiency_accuracy_purity_count_categories_cm()

    def get_predicted(self) -> list:
        """Return self.predicted."""
        return self.predicted

    def get_predicted_category_values(self) -> list:
        """Return self.__predicted_category_values"""
        return self.__predicted_category_values

    def get_cm_entry(self, x: int, y: int, normalized=False):
        """ Get an entry of the confusion matrix. x and y define cm coordinates. """
        if normalized:
            return self.cm_normalized[x][y]
        else:
            return self.cm[x][y]

    def print_category_count(self) -> None:
        """Print category counts and the form of the unique categories."""
        print("Counts per category:\n", self.counts_per_category)
        print("Category shapes:\n", self.unique_categories)

    # Data-stuff
    def select_stats_data_by_data_name(self,
                                       data_name: str,
                                       category: str = None,
                                       data=None) -> list:
        """
        Return list of data_container from self.stats_data, given one of the categories defined when creating the Evaluator
        (self.category_values_dict). Return only data_container specified by data_name.

        :param data_name: Name of the data_container which will be selected. Requires the same identifier as defined in data_dict
            upon class instantiation.
        :param category: Which category will be selected from the data_container provided (e.g. "Electron"). If none is provided,
            all data_container (data_name) will be selected.
        :param data: Data from which will be selected.
        :return: list of the selected data_container.
        """
        temp_data_var = self.stats_data if data is None else data
        tdata = []
        if category is None:
            if self.real_test_data:
                tdata = [x[0][self.stats_dict[data_name]] for x in temp_data_var]
            else:
                tdata = [x[0][self.stats_dict[data_name]] for x in temp_data_var]
            # This simply flattens data_container
        else:
            for entry in temp_data_var:
                t = True
                # All parts of the category identifiers need to match. This is a stupidly long expression for this
                # simple function, couldn't really get it to work in a simpler way, but this works. Can definitely be
                # improved..
                for i in range(len(self.category_values_dict[category])):
                    if entry[1][i] == self.category_values_dict[category][i]:
                        continue
                    else:
                        t = False
                        break
                if t:
                    tdata.append(entry[0][self.stats_dict[data_name]])
        return tdata

    def select_stats_data_by_category(self, category: Union[str, None] = None):
        """
        Return entries of self.stats_data which fit the specified category.

        Allowing category = None allows for simpler handling in the Bundle class.
        """
        if category is None:
            return self.stats_data
        else:
            data = []
            for entry in self.stats_data:
                t = True
                # All parts of the category identifiers need to match. This is a stupidly long expression for this
                # simple function, couldn't really get it to work in a simpler way, but this works. Can definitely be
                # improved..
                for i in range(len(self.category_values_dict[category])):
                    if entry[1][i] == self.category_values_dict[category][i]:
                        continue
                    else:
                        t = False
                        break
                if t:
                    data.append(entry)
        return data

    @staticmethod
    def select_predicted_classes(data: list):
        """
        Extract the original (floating point) predictions of the model from data_container in the form of stats_data.
        """
        data = [event[2] for event in data]
        return data

    @staticmethod
    def select_predicted_category_values(data: list):
        """Extract the category value predictions of the model from data_container in the form of stats_data."""
        data = [event[3] for event in data]
        return data

    @staticmethod
    def fa_gen(fa: matplotlib.figure.Figure):
        """Generate figure and ax object as a Tuple if fa is None else return fa. Also, explicitly open provided fig."""
        if fa is None:
            fig, ax = plt.subplots(1, 1)
        else:
            fig = fa[0]
            ax = fa[1]
            # if fig
            dummy = plt.figure()
            new_manager = dummy.canvas.manager
            new_manager.canvas.figure = fig
            fig.set_canvas(new_manager.canvas)

        fa = (fig, ax)
        return fa

    @staticmethod
    def show_handler(fig, show: bool):
        if show:
            plt.show()
        else:
            plt.close(fig)

    @staticmethod
    def _set_lims(xlim=None,
                  ylim=None) -> None:
        """Set limits for plots. Saves clutter."""
        # cfig = plt.figure(fig.number) TODO
        if xlim:
            plt.xlim(xlim)
        if xlim:
            plt.ylim(ylim)

    @staticmethod
    def _set_lims_ax(ax: plt.figure,
                     xlim=None,
                     ylim=None) -> None:
        """Set limits for plots. Saves clutter."""
        if xlim:
            ax.set_xlim(xlim)
        if xlim:
            ax.set_ylim(ylim)

    def _save_fig(self,
                  fig: plt.figure = None,
                  file_format: Union[str, List[str]] = None,
                  filename: str = None) -> None:
        """
        Save a figure.

        :param file_format: Format of the saved file. Default = ["pdf", "png"]. Pass array to save in multiple formats.
        :param filename: Filename of the saved figure.
        :return: None
        """

        if file_format is None:
            file_format = ["pdf", "png"]

        filename = self.model_name if filename is None else filename

        plt.figure(fig.number)
        if type(file_format) is str:
            fig.savefig(filename, format=file_format, bbox_inches="tight")

        if type(file_format) is list:
            for ff in file_format:
                fig.savefig(filename + "." + ff, format=ff, bbox_inches="tight")

    def evaluate_model(self, verbose=False):
        """
        Score the model on provided test data_container. Use verbose = True to print stats about score.

        :param verbose: The verbosity parameter will be passed to keras.model.evaluate().
        """
        if self.score is None:
            self.score = self.model.evaluate(self.test_data, self.test_category_values, verbose=0)
        if verbose:
            print(f'Test loss: {self.score[0]} / Test accuracy: {self.score[1]}'
                  f' on  {len(self.test_category_values)} events')

    ####################################################################################################################
    # Analysis
    ####################################################################################################################

    @staticmethod
    def __create_bins_from_data(bins: Union[str, int, list, None],
                                data: list,
                                equal_counts: bool = False) -> list:
        """
        Create bins, specified by 'bins' and data_container. Behaviour is specified by the type of the bins' parameter.

        :param bins: Accepts an array-like object to specify bin cutoffs, an int for evenly spaced bins between
            the min and max value of the data_container provided, or the string "auto", for 100 evenly spaced bins.
            Omitting will default to auto.
        :param data: Data which will be used for bin bounds.
        :param equal_counts: If true, will attempt to build bins which contain the same number of events. Note that
            splitting data_container with the exact same values into multiple bins is not supported.
        :return: list of bins.
        """
        if (type(bins) == int or bins == "auto" or bins is None) and not equal_counts:
            if type(bins) == int:
                number_of_bins = bins + 1
            else:
                number_of_bins = 101
            bins = []
            step = (np.max(data) - np.min(data)) / number_of_bins
            for i in range(number_of_bins):
                bins.append(np.min(data) + i * step)

        elif type(bins) == int and equal_counts:
            number_of_bins = bins + 1
            counts_per_bin = int(np.floor(len(data) / number_of_bins))
            sorted_data = np.sort(data)
            bins = []

            for i in range(number_of_bins):
                bins.append(sorted_data[i * counts_per_bin])

        elif type(bins) == list:
            pass

        else:
            raise celfa_exceptions.ErrorParameter

        return bins

    def get_auc(self):
        """Simply return roc_auc_score."""
        return roc_auc_score(self.test_category_values, self.y_prob)

    def plot_roc(self,
                 category=None,
                 xlim=None,
                 ylim=None,
                 xlbl: str = None,
                 ylbl: str = None,
                 title: str = None,
                 savefig: bool = False,
                 filename: bool = None,
                 file_format: str = None,
                 return_data: bool = False,
                 show: bool = True,

                 fa: List = None,
                 return_fa: bool = None,

                 **kwargs
                 ) -> Union[None, List, Tuple]:
        """
        Plot the ROC-Curve.

        :param show: Show plot?
        :param category: Category for which the ROC-Curve is plotted.
        :param ylbl: Text for y-axis label.
        :param xlbl: Text for x-axis label.
        :param file_format: Format of the saved figure. Default (provided by self._save_fig()) is 'pdf'.
        :param savefig: Save figure?
        :param filename: Filename of the saved figure.
        :param xlim: Limits of the x-axis. Accepts tuple or similar.
        :param ylim: Limits of the y-axis. Accepts tuple or similar.
        :param title: Title of the plot. If none is provided, the title will be generated based on the provided
            parameters.

        :param fa: Pass matplotlib figure and ax object as a Tuple or List type to which the curve will be plotted.
            If fa == None, a new fig and ax will be created.
        :param return_fa: Returns figure and ax object as List.

        :param kwargs: Will be passed directly to plt.plot(), for valid arguments see documentation of
            matplotlib.pyplot.plot().

        :param return_data: If true, return data_container instead of plotting. The returned data_container is of the
            form [bins, percent_predicted_per_bin].
        :return: None, unless return_data is set to true. Shows plot. Returns Tuple of fig, ax if return_fa == True.
        """

        fpr, tpr, threshold, roc_auc = dict(), dict(), dict(), dict()
        for i in range(len(self.category_values_dict)):
            fpr[i], tpr[i], threshold[i] = roc_curve(self.test_category_values[:, i], self.y_prob[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        fig, ax = self.fa_gen(fa)

        if "label" in kwargs:
            label = kwargs.pop("label") + f" ({100 * self.get_auc():.2f})"
        else:
            label = f'ROC curve {self.get_auc():.3f}'

        ax.plot(fpr[np.where(self.category_values_dict[category]
                             == np.amax(self.category_values_dict[category]))[0][0]],
                tpr[np.where(self.category_values_dict[category]
                             == np.amax(self.category_values_dict[category]))[0][0]],
                label=label, **kwargs)

        ax.legend(loc="lower right", fontsize=12)

        ax.set_xlabel("Residual background fraction", fontsize=14) if xlbl is None else plt.xlabel(xlbl)
        ax.set_ylabel("PSignal efficiency", fontsize=14) if ylbl is None else plt.ylabel(ylbl)

        title = self.model_name if title is None else title
        ax.set_title(title)

        self._set_lims_ax(ax, xlim, ylim)

        self.show_handler(fig, show)

        if savefig:
            self._save_fig(fig, file_format, filename)
        if return_data:
            return [fpr[np.where(self.category_values_dict[category]
                                 == np.amax(self.category_values_dict[category]))[0][0]],
                    tpr[np.where(self.category_values_dict[category]
                                 == np.amax(self.category_values_dict[category]))[0][0]]]
        if return_fa:
            if fa is None:
                fa = (fig, ax)
            return fa

    def plot_percent_predicted(self,
                               data_name=None,
                               category=None,
                               bins: Union[str, int, list, None] = "auto",

                               title: Union[None, str] = None,
                               xlim=None,
                               ylim=None,
                               xlbl: str = None,
                               ylbl: str = None,

                               error_bars: bool = True,

                               show: bool = True,
                               return_data: bool = False,
                               savefig: bool = False,
                               file_format: str = "pdf",
                               filename: str = None,

                               fa: List = None,
                               return_fa: bool = None,

                               **kwargs) -> Union[None, List]:
        """
        Plots predicted count / total count per bin vs. data_name.

        :param error_bars: True if error bars based on Clopper-Pearson binomial alpha = 0.39 should be shown.
        :param data_name: Name of the data_container which will be plotted. Requires the same identifier as defined in data_dict
            upon class instantiation.
        :param bins: Pass 'auto', a positive int, a list of bins, or None (auto). Bins will be constructed in
            __create_bins_from_data.
        :param category: Category for which the ROC-Curve is plotted.

        :param title: Title of the plot. If none is provided, the title will be generated based on the provided
            parameters.
        :param xlim: Limits of the x-axis. Accepts tuple or similar.
        :param ylim: Limits of the y-axis. Accepts tuple or similar.
        :param xlbl: Text for x-axis label. If none is provided, the label will be generated based on the provided
            parameters.
        :param ylbl: Text for y-axis label. If none is provided, the label will be generated based on the provided
            parameters.

        :param return_data: If true, return data_container instead of plotting. The returned data_container is of the form
            [bins, percent_predicted_per_bin].
        :param savefig: Save figure?
        :param file_format: Format of the saved figure. Default (provided by self._save_fig()) is 'pdf'.
        :param filename: Filename of the saved figure.

        :param fa: Pass matplotlib figure and ax object as a Tuple or List type to which the curve will be plotted.
            If fa == None, a new fig and ax will be created.
        :param return_fa: Returns figure and ax object as List.

        :param kwargs: Will be passed directly to plt.plot(), for valid arguments see documentation of
             matplotlib.pyplot.plot().
        :return: None(shows plot), or data_container.
        """
        fig, ax = self.fa_gen(fa)
        data = self.stats_data
        selected_data = self.select_stats_data_by_data_name(data_name)
        bins = self.__create_bins_from_data(bins, selected_data)

        counts_per_bin = np.zeros(len(bins))
        true_pos_per_bin = np.zeros(len(bins))

        cat = (self.category_values_dict[category]).index(1)

        bin_location = np.digitize(selected_data, bins)
        percent_predicted_per_bin = []

        for i in range(len(selected_data)):
            counts_per_bin[bin_location[i] - 1] += 1
            if data[i][-1][cat]:
                true_pos_per_bin[bin_location[i] - 1] += 1

        for i in range(len(counts_per_bin)):
            if counts_per_bin[i] == 0:
                percent_predicted_per_bin.append(0)
            else:
                percent_predicted_per_bin.append(true_pos_per_bin[i] / counts_per_bin[i])

        if return_data:
            return [bins, percent_predicted_per_bin]
        else:
            error = np.array(
                [sm.proportion_confint(true_pos_per_bin[i], counts_per_bin[i],
                                       method="beta",
                                       alpha=0.39)
                 for i in range(len(bins))])
            error_bar_upper = error[:, 0] - percent_predicted_per_bin
            error_bar_lower = -error[:, 1] + percent_predicted_per_bin

            if category is None:
                category_lbl = "All categories"
            else:
                category_lbl = category

            if error_bars:
                _ = ax.errorbar(bins[:-1], percent_predicted_per_bin[:-1],
                                yerr=(error_bar_lower[:-1], error_bar_upper[:-1]),
                                fmt='o', markersize=5, alpha=1, elinewidth=2, capsize=9, **kwargs)
            else:
                _ = ax.scatter(bins, percent_predicted_per_bin, **kwargs)

            ax.set_xlabel(data_name) if xlbl is None else plt.xlabel(xlbl)

            if self.mode == "em":
                ax.set_ylabel("Predicted fraction Muon events per bin") if ylbl is None else ax.set_ylabel(ylbl)
            elif self.mode == "rc":
                ax.set_ylabel("Predicted fraction SR events per bin") if ylbl is None else ax.set_ylabel(ylbl)

            title = f"{self.model_name} % predicted: {data_name}, {category}" if title is None else title
            ax.set_title(title)

            self._set_lims_ax(ax, xlim, ylim)

            self.show_handler(fig, show)

            if savefig:
                self._save_fig(fig, file_format, filename)

            if return_fa:
                if fa is None:
                    fa = (fig, ax)
                return fa

            return None

    def plot_prediction_confidence(self,
                                   category=None,
                                   histtype="bar",
                                   style: str = "continuous",

                                   title: Union[None, str] = None,
                                   xlim=None,
                                   ylim=None,
                                   xlbl: str = None,
                                   ylbl: str = None,

                                   show: bool = True,
                                   return_data: bool = False,
                                   savefig: bool = False,
                                   file_format: str = "pdf",
                                   filename: str = None,
                                   **kwargs) -> Union[None, List[List]]:
        """
        Plots a histogram of prediction confidence.

        :param category: Category for which the prediction confidence is plotted.
        :param histtype: See matplotlib implementation of hist.
        :param style: Choose between continuous / split plot style. TODO

        :param title: Title of the plot. If none is provided, the title will be generated based on the provided
            parameters.
        :param xlim: Limits of the x-axis. Accepts tuple or similar.
        :param ylim: Limits of the y-axis. Accepts tuple or similar.
        :param xlbl: Text for x-axis label. If none is provided, the label will be generated based on the provided
            parameters.
        :param ylbl: Text for y-axis label. If none is provided, the label will be generated based on the provided
            parameters.

        :param return_data: If true, return data_container instead of plotting. The returned data_container is of the form
            [bins, correctly_classified_probabilities, incorrectly_classified_probabilities].
        :param savefig: Save figure?
        :param file_format: Format of the saved figure. Default (provided by self._save_fig()) is 'pdf'.
        :param filename: Filename of the saved figure.

        :param kwargs: will be passed to plt.hist().
        :return: None, or data_container. See param return_data.
        """
        if category is None:
            raise celfa_exceptions.ErrorParameter

        elif type(category) is str:
            selected_data = self.select_stats_data_by_category(category)
            selected_class_predictions = self.select_predicted_classes(selected_data)
            selected_category_value_predictions = self.select_predicted_category_values(selected_data)

            fig = plt.figure()
            bins = self.__create_bins_from_data(100, [0.0, 1.0])
            correctly_classified_probabilities, incorrectly_classified_probabilities = [], []

            for event in range(len(selected_data)):
                if style == "split":
                    # calling np.array() on both values since otherwise we are trying to compare objects of the form
                    # [1 0] and [1, 0]. (calling np.array() will change the second list into the first object)
                    if (np.array(selected_data[event][1]) == np.array(
                            selected_category_value_predictions[event])).all():
                        if category == "Electron" or category == "MR":
                            correctly_classified_probabilities.append(selected_class_predictions[event][0])
                        elif category == "Muon" or category == "SR":
                            correctly_classified_probabilities.append(selected_class_predictions[event][1])
                    else:
                        if category == "Electron" or category == "MR":
                            incorrectly_classified_probabilities.append(selected_class_predictions[event][0])
                        elif category == "Muon" or category == "SR":
                            incorrectly_classified_probabilities.append(selected_class_predictions[event][1])
                elif style == "continuous":
                    pass
                else:
                    raise celfa_exceptions.ErrorParameter

            if return_data:
                return [bins, correctly_classified_probabilities, incorrectly_classified_probabilities]
            else:
                if style == "continuous":
                    _ = plt.hist(
                        np.concatenate(
                            [correctly_classified_probabilities, incorrectly_classified_probabilities], axis=0),
                        bins=bins, histtype=histtype, label=f"{category} event")
                elif style == "split":
                    _ = plt.hist(correctly_classified_probabilities, bins=bins, histtype=histtype,
                                 label=f"True {category} event", **kwargs)
                    _ = plt.hist(incorrectly_classified_probabilities, bins=bins, histtype=histtype,
                                 label="Incorrect predictions", **kwargs)
            plt.legend(loc='best', fontsize=11)

            title = f"{self.model_name} % prediction: {category}" if title is None else title
            plt.title(title)

            if show:
                plt.show()

            if savefig:
                self._save_fig(fig, file_format, filename)

        elif type(category) is list:
            for entry in category:
                self.plot_prediction_confidence(entry, histtype, style, title, xlim, ylim, xlbl, ylbl, return_data,
                                                savefig, file_format, filename, **kwargs)
        else:
            raise celfa_exceptions.ErrorParameter

    def plot_probability_histogram(self,
                                   bins: Union[int, None] = None,
                                   category=None,
                                   style: str = "continuous",
                                   true_cat: bool = False,

                                   error_bars: bool = True,

                                   title: Union[None, str] = None,
                                   xlim=None,
                                   ylim=None,
                                   xlbl: str = None,
                                   ylbl: str = None,

                                   show: bool = True,
                                   return_data: bool = False,
                                   savefig: bool = False,
                                   file_format: str = "pdf",
                                   filename: str = None,

                                   fa: List = None,
                                   return_fa: bool = None,

                                   **kwargs) -> Union[None, List, Tuple]:
        """
        Plots y_prob % 'confidence' for an event.

        :param category: Category for which the prediction confidence is plotted.
        :param style: Choose between continuous / split plot style. TODO
        :param bins: Pass 'auto', a positive int, a list of bins, or None (auto). Bins will be constructed in
            __create_bins_from_data.

        :param title: Title of the plot. If none is provided, the title will be generated based on the provided
            parameters.
        :param xlim: Limits of the x-axis. Accepts tuple or similar.
        :param ylim: Limits of the y-axis. Accepts tuple or similar.
        :param xlbl: Text for x-axis label. If none is provided, the label will be generated based on the provided
            parameters.
        :param ylbl: Text for y-axis label. If none is provided, the label will be generated based on the provided
            parameters.

        :param return_data: If true, return data_container instead of plotting. The returned data_container is of the form
            [bins, correctly_classified_probabilities, incorrectly_classified_probabilities].
        :param savefig: Save figure?
        :param file_format: Format of the saved figure. Default (provided by self._save_fig()) is 'pdf'.
        :param filename: Filename of the saved figure.

        :param fa: Pass matplotlib figure and ax object as a Tuple or List type to which the curve will be plotted.
            If fa == None, a new fig and ax will be created.
        :param return_fa: Returns figure and ax object as List.

        :param kwargs: will be passed to plt.hist().
        :return: None, data or figure and ax object as a tuple.
        """

        fig, ax = self.fa_gen(fa)

        selected_data = self.stats_data
        selected_class_predictions = self.select_predicted_classes(selected_data)
        selected_category_value_predictions = self.select_predicted_category_values(selected_data)

        if category is None:
            selected_class_predictions = [prob[1] for prob in self.y_prob]

        bins = self.__create_bins_from_data(bins, [0.0, 1.01])

        probabilities_class = []
        probabilities_other_class = []
        if category is not None:
            for event in range(len(selected_data)):
                if true_cat:
                    if (np.array(self.category_values_dict[category]) == np.array(
                            selected_data[event][1])).all():
                        probabilities_class.append(
                            selected_class_predictions[event][np.where(
                                np.array(self.category_values_dict[category]) == 1)[0][0]])
                    else:
                        probabilities_other_class.append(1 - selected_class_predictions[event][np.where(
                            np.array(self.category_values_dict[category]) == 1)[0][0]])
                # calling np.array() on both values since otherwise we are trying to compare objects of the form
                # [1 0] and [1, 0]. (calling np.array() will change the second list into the first object)
                else:
                    if (np.array(self.category_values_dict[category]) == np.array(
                            selected_category_value_predictions[event])).all():
                        probabilities_class.append(
                            selected_class_predictions[event][np.where(
                                np.array(self.category_values_dict[category]) == 1)[0][0]])
                    else:
                        probabilities_other_class.append(
                            selected_class_predictions[event][np.where(
                                np.array(self.category_values_dict[category]) == 1)[0][0]])
        else:
            probabilities_class = selected_class_predictions

        if return_data:
            return [probabilities_class, probabilities_other_class, bins]
        else:
            cname = ""
            label = None
            if "label" in kwargs:
                label = kwargs.pop("label")
            if category is not None:
                if style == "continuous":
                    label = label if label else f"{category} predictions"

                    if error_bars:
                        __tf, __ta = plt.subplots(1, 1)
                        self.show_handler(__tf, False)
                        __xy = __ta.hist([*probabilities_other_class, *probabilities_class], bins=bins, histtype="bar")

                        # prob. density normalisation: divide by the width of bins * number of counts
                        _ = ax.errorbar(np.array(bins[:-1]) + (bins[2] - bins[1]) / 2,
                                        __xy[0] / (np.sum(__xy[0]) * (bins[2] - bins[1])),
                                        yerr=np.sqrt(__xy[0]) / (np.sum(__xy[0]) * (bins[2] - bins[1])),
                                        fmt='o', markersize=1, alpha=1, elinewidth=0.7, capsize=3, color="dimgrey")

                    _ = ax.hist([*probabilities_other_class, *probabilities_class], bins=bins,
                                label=label, **kwargs)
                else:
                    _ = ax.hist(probabilities_class, bins=bins, histtype="bar",
                                label=f"Prediction for class {category}", **kwargs)
                    _ = ax.hist(probabilities_other_class, bins=bins, histtype="bar",
                                label="Prediction for any other class", **kwargs)
            else:
                if self.mode == "rc":
                    cname = "SR"
                elif self.mode == "em":
                    cname = "Muon"
                else:
                    cname = "unknown"
                _ = ax.hist(probabilities_class, bins=bins, histtype="bar",
                            label=f"Prediction for class '{cname}'", **kwargs)
            ax.legend(loc='best', fontsize=11)

            if category is not None:
                ax.set_xlabel(f"Prediction for class {category}") if xlbl is None \
                    else plt.xlabel(xlbl)
            else:
                ax.set_xlabel(f"Prediction for class {cname}") if xlbl is None \
                    else plt.xlabel(xlbl)
            ax.set_ylabel("Count") if ylbl is None else plt.ylabel(ylbl)

            if xlim is not None:
                ax.set_xlim(xlim)
            if ylim is not None:
                ax.set_ylim(ylim)
            if title is None:
                ax.set_title(f"{self.model_name} prob. histogram for {category}")
            else:
                ax.set_title(title)

            self.show_handler(fig, show)

            if savefig:
                self._save_fig(fig, file_format, filename)

            if return_fa:
                if fa is None:
                    fa = (fig, ax)
                return fa

    def plot_confusion_matrix(self,
                              normalized: bool = True,
                              cmap: str = "Blues",

                              title: Union[None, str] = None,
                              xlbl: str = None,
                              ylbl: str = None,

                              show: bool = True,
                              savefig: bool = False,
                              file_format: str = "pdf",
                              filename: str = None,
                              ) -> None:
        """
        Plots the confusion matrix for Electron and Muon event classification.

        :param cmap: Colour map of the plot. See matplotlib.cmap
        :param normalized: Plot the confusion matrix normalized?

        :param title: Title of the confusion matrix. If none is provided, the title will be generated based on
            the provided parameters.
        :param xlbl: Text for x-axis label. If none is provided, the label will be generated based on the provided
            parameters.
        :param ylbl: Text for y-axis label. If none is provided, the label will be generated based on the provided
            parameters.

        :param savefig: Save figure?
        :param file_format: Format of the saved figure. Default (provided by self._save_fig()) is 'pdf'.
        :param filename: Filename of the saved figure.
        """
        # TODO: Use  self.category_values_dict
        if self.mode == "em":
            classes = ["Electron", "Muon"]
        elif self.mode == "rc":
            classes = ["MR", "SR"]
        else:
            raise celfa_exceptions.ErrorParameter

        local_cm = self.cm_normalized if normalized else self.cm

        fig = plt.figure()

        if cmap is not None:
            cmap = plt.get_cmap(cmap)
        else:
            if normalized:
                cmap = plt.get_cmap("Blues")
            else:
                cmap = plt.get_cmap("Purples")

        plt.imshow(local_cm, interpolation='nearest', cmap=cmap)

        if title is None:
            title = f"CM normalized - {self.model_name}" if normalized else f"CM absolute - {self.model_name}"
        plt.title(title)

        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.3f' if normalized else 'd'
        thresh = local_cm.max() / 2.
        for i, j in itertools.product(range(local_cm.shape[0]), range(local_cm.shape[1])):
            plt.text(j, i, format(local_cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if local_cm[i, j] > thresh else "black")

        plt.tight_layout()

        if xlbl is None:
            xlbl = "Predicted label"
        if ylbl is None:
            ylbl = "True label"
        plt.xlabel(xlbl)
        plt.ylabel(ylbl)

        self.show_handler(fig, show)

        if savefig:
            self._save_fig(fig, file_format, filename)

    def __plot_histogram_real(self,
                              data_name: str,
                              bins: Union[str, int, list, None] = "auto",
                              xlim=None,
                              ylim=None,
                              xlbl: str = None,
                              ylbl: str = None,
                              title: str = None,
                              histtype: Union[str, list] = "bar",
                              equal_counts: bool = False,
                              show: bool = True,
                              savefig: bool = False,
                              filename: str = None,
                              file_format: str = None,
                              **kwargs) -> None:
        """
        Plot a histogram (number of counts vs data_container).

        :param ylbl: Text for y-axis label.
        :param xlbl: Text for x-axis label.
        :param file_format: Format of the saved figure. Default (provided by self._save_fig()) is 'pdf'.
        :param savefig: Save figure?
        :param filename: Filename of the saved figure.
        :param equal_counts: If true, will attempt to build bins which contain the same number of events. Note that
            splitting data_container with the exact same values into multiple bins is not supported. Also note, that
            this only applies if type(bins) = int. See also self.__create_bins_from_data()
        :param xlim: Limits of the x-axis. Accepts tuple or similar.
        :param ylim: Limits of the y-axis. Accepts tuple or similar.
        :param data_name: Name of the data_container which will be plotted. Requires the same identifier as defined in
            data_dict upon class instantiation.
        :param bins: Accepts an array-like object to specify bin cutoffs, an int for evenly spaced bins between
            the min and max value of the data_container provided, or the string "auto", for 100 evenly spaced bins.
            Omitting will default to auto.
        :param title: Title of the plot. If none is provided, the title will be generated based on the provided
            parameters.
        :param histtype: If plotting only one category, or when plotting all categories in the same (histtype) style,
            requires a str. For valid parameters see matplotlib.pyplot.hist(). When plotting multiple categories, with
            differing histtype styles, requires a list.
        :param kwargs: Will be passed directly to plt.hist(), for valid arguments see documentation of
            matplotlib.pyplot.hist().
        :return: None. Shows plot.
        """
        fig, ax = plt.subplots(1, 1)

        data = self.select_stats_data_by_data_name(data_name)
        # data = [x[0] for x in data] # todo why? is this necessary? I can't remember!

        bins = self.__create_bins_from_data(bins, data, equal_counts=equal_counts)

        _ = ax.hist(data, bins=bins, histtype=histtype, label="All data_container", **kwargs)

        if title is None:
            ax.set_title(f"{self.model_name} - Histogram with {len(bins) - 1} bins. "
                         f"\n Plotting {data_name} for all categories.")
        else:
            ax.set_title(f"{title}")

        plt.legend(loc='best', fontsize=11)

        ax.set_xlabel(data_name) if xlbl is None else plt.xlabel(xlbl)
        ax.set_ylabel("Count") if ylbl is None else plt.ylabel(ylbl)

        self._set_lims(fig, xlim, ylim)

        if show:
            plt.show()

        if savefig:
            self._save_fig(fig, file_format, filename)

    def plot_histogram(self,
                       data_name: str,
                       bins: Union[object, None] = "auto",
                       xlim=None,
                       ylim=None,
                       xlbl: str = None,
                       ylbl: str = None,
                       category: Union[str, list, None] = None,
                       title: str = None,
                       histtype: Union[str, list] = "bar",
                       equal_counts: bool = False,
                       color: str = None,

                       show: bool = True,
                       savefig: bool = False,
                       filename: str = None,
                       file_format: str = None,

                       fa: List = None,
                       return_fa: bool = None,

                       **kwargs) -> Union[None, Tuple]:
        """
        Plot a histogram (number of counts vs data_container).

        :param ylbl: Text for y-axis label.
        :param xlbl: Text for x-axis label.
        :param file_format: Format of the saved figure. Default (provided by self._save_fig()) is 'pdf'.
        :param savefig: Save figure?
        :param filename: Filename of the saved figure.
        :param equal_counts: If true, will attempt to build bins which contain the same number of events. Note that
            splitting data_container with the exact same values into multiple bins is not supported. Also note, that
            this only applies if type(bins) = int. See also self.__create_bins_from_data()
        :param xlim: Limits of the x-axis. Accepts tuple or similar.
        :param ylim: Limits of the y-axis. Accepts tuple or similar.
        :param data_name: Name of the data_container which will be plotted. Requires the same identifier as defined in
            data_dict upon class instantiation.
        :param bins: Accepts an array-like object to specify bin cutoffs, an int for evenly spaced bins between
            the min and max value of the data_container provided, or the string "auto", for 100 evenly spaced bins.
            Omitting will default to auto.
        :param category: Which category will be selected from the data_container provided (e.g. "Electron"). If none is
            provided, all data_container will be selected. If a list of categories is provided, multiple histograms in
            the same plot will be created.
        :param title: Title of the plot. If none is provided, the title will be generated based on the provided
            parameters.
        :param histtype: If plotting only one category, or when plotting all categories in the same (histtype) style,
            requires a str. For valid parameters see matplotlib.pyplot.hist(). When plotting multiple categories, with
            differing histtype styles, requires a list.

        :param fa: Pass matplotlib figure and ax object as a Tuple or List type to which the curve will be plotted.
            If fa == None, a new fig and ax will be created.
        :param return_fa: Returns figure and ax object as List.

        :param kwargs: Will be passed directly to plt.hist(), for valid arguments see documentation of
            matplotlib.pyplot.hist().
        :return: None. Shows plot.
        """
        if type(category) is str:
            try:
                _ = self.select_stats_data_by_category(category)
            except KeyError:
                return None

        if type(category) is list:
            for c in category:
                try:
                    c = self.select_stats_data_by_category(c)
                except KeyError:
                    print(f"Warning: given category '{c}' is not a part of this Evaluator's stats_data.")
                    return None

        if self.real_test_data:
            self.__plot_histogram_real(data_name=data_name, bins=bins, xlim=xlim, ylim=ylim, xlbl=xlbl, ylbl=ylbl,
                                       title=title, histtype=histtype, equal_counts=equal_counts, show=show,
                                       savefig=savefig, filename=filename, file_format=file_format, **kwargs)
            return None

        fig, ax = self.fa_gen(fa)

        if type(category) is list:
            bins_t = bins
            for cat in range(len(category)):
                if data_name == "TrueEnergy":
                    if category[cat] == "Muon":
                        data = self.select_stats_data_by_data_name("EnergyMuon", category="Muon")
                    elif category[cat] == "Electron":
                        data = self.select_stats_data_by_data_name("EnergyElectron", category="Electron")
                    else:
                        return
                else:
                    data = self.select_stats_data_by_data_name(data_name, category=category[cat])
                if bins is None or type(bins) == int:
                    bins_t = self.__create_bins_from_data(bins, data, equal_counts=equal_counts)

                if type(histtype) is list:
                    if type(color) is list:
                        _ = ax.hist(data, bins=bins_t, histtype=histtype[cat], label=category[cat],
                                    color=color[cat], **kwargs)
                    else:
                        _ = ax.hist(data, bins=bins_t, histtype=histtype[cat], label=category[cat], **kwargs)

                else:
                    if type(color) is list:
                        _ = ax.hist(data, bins=bins_t, histtype=histtype, label=category[cat],
                                    color=color[cat], **kwargs)

                    else:
                        _ = ax.hist(data, bins=bins_t, histtype=histtype, label=category[cat], **kwargs)

            if title is None:
                ax.set_title(f"{self.model_name} - Histogram with {len(bins_t) - 1} bins. "
                             f"\n Plotting {data_name} for the categories {category}.")
            else:
                ax.set_title(f"{title}")

        else:
            data = self.select_stats_data_by_data_name(data_name, category=category)
            bins = self.__create_bins_from_data(bins, data, equal_counts=equal_counts)

            if category is None:
                category = "All categories"

            _ = ax.hist(data, bins=bins, histtype=histtype,
                        label=kwargs.pop("label") if "label" in kwargs else category, **kwargs)

            if title is None:
                ax.set_title(f"{self.model_name} - Histogram with {len(bins) - 1} bins. "
                             f"\n Plotting {data_name} for the category {category}.")
            else:
                ax.set_title(f"{title}")

        ax.legend(loc='best', fontsize=11)

        ax.set_xlabel(data_name) if xlbl is None else ax.set_xlabel(xlbl)
        ax.set_ylabel("Count") if ylbl is None else ax.set_ylabel(ylbl)

        self._set_lims_ax(ax, xlim, ylim)

        self.show_handler(fig, show)

        if savefig:
            self._save_fig(fig, file_format, filename)

        if return_fa:
            if fa is None:
                fa = (fig, ax)
            return fa

    def plot_accuracy(self,
                      data_name: str,
                      category: Union[str, list, None] = None,
                      column: Union[int, None] = None,
                      bins: Union[str, int, list, None] = "auto",
                      title: str = None,
                      xlim=None,
                      ylim=None,
                      xlbl: str = None,
                      ylbl: str = None,

                      xticks_minor=None,
                      xticks_major=None,
                      xtick_labels_minor=None,
                      xtick_labels_major=None,
                      yticks_minor=None,
                      yticks_major=None,
                      ytick_labels_minor=None,
                      ytick_labels_major=None,
                      grid: bool = False,

                      return_data: bool = False,
                      equal_counts: bool = False,
                      error_bars: bool = False,
                      color: Union[str, List[str]] = None,
                      plot_at_center_of_bins: bool = True,

                      show: bool = True,
                      savefig: bool = False,
                      filename: str = None,
                      file_format: str = None,

                      fa: List = None,
                      return_fa: bool = None,

                      **kwargs) -> object:
        """
        Plot model accuracy (accuracy vs data_container).
        ----------------------------------------------------------------------------------------------------------------
        Note:
        -----
        Data points beyond - if provided - xlim are automatically dropped; if no xlim has been provided, discounts all
        data_container points beyond the first and last bin border.
        :param grid: Show grid for major tick marks? Defaults to False.
        :param color: Pass matplotlib colors. Passing a list will use them in the same order as the categories.
        :param show: If true, show plot. Default: True.
        :param return_data: If true, returns data given in the format
            [bins, percentage_correct, (error_bar_lower, error_bar_upper)].
        :param plot_at_center_of_bins: If true, centers the data_container on centers of bins. In the process, the last
            data_container point is dropped.
        :param column: Only applies to MRD data_container. Specifies which MRD data_container column will be selected.
        :param error_bars: Includes error bars. Using Clopper-Pearson interval based on beta distribution.
        :param equal_counts: If true, will attempt to build bins which contain the same number of events. Note that
            splitting data_container with the exact same values into multiple bins is not supported. Also note, that
            this only applies if type(bins) = int. See also self.__create_bins_from_data()
        :param data_name: Name of the data_container which will be plotted. Requires the same identifier as defined in
            data_dict upon class instantiation.
        :param category: Which category will be selected from the data_container provided (e.g. "Electron"). If none is
            provided, all data_container will be selected. If a list of categories is provided, multiple histograms in
            the same plot will be created.
        :param bins: Accepts an array-like object to specify bin cutoffs, an int for evenly spaced bins between
            the min and max value of the data_container provided, or the string "auto", for 100 evenly spaced bins.
            Omitting will default to auto.
        :param title: Title of the plot. If none is provided, the title will be generated based on the provided
            parameters.
        :param xlim: Limits of the x-axis. Accepts tuple or similar.
        :param ylim: Limits of the y-axis. Accepts tuple or similar.
        :param ylbl: Text for y-axis label.
        :param xlbl: Text for x-axis label.
        :param kwargs: Will be passed directly to plt.scatter(), for valid arguments see documentation of
            matplotlib.pyplot.scatter().
        :param file_format: Format of the saved figure. Default (provided by self._save_fig()) is 'pdf'.
        :param savefig: Save figure?
        :param filename: Filename of the saved figure.

        :param fa: Pass matplotlib figure and ax object as a Tuple or List type to which the curve will be plotted.
            If fa == None, a new fig and ax will be created.
        :param return_fa: Returns figure and ax object as List.

        :return: None, or List of figure and ax object.
        """
        xticks = None
        if xticks_minor is not None:
            xticks = xticks_minor[:]
            copy_xticks_major = xticks_major[:]
            xticks.extend(copy_xticks_major)
            xticks.sort()
        # create data_container
        fig, ax = self.fa_gen(fa)

        percentage_correct = []
        correct_classifications_per_bin = []
        events_per_bin = []
        if category is None:
            data = self.stats_data
            selected_data = self.select_stats_data_by_data_name(data_name, data=data)
            if data_name == "MRD":
                selected_data = [x[column] for x in selected_data]

        elif type(category) is list:
            data_multiple, selected_data_multiple = [], []
            for i in range(len(category)):
                data_multiple.append(0), selected_data_multiple.append(0)
                data_multiple[i] = self.select_stats_data_by_category(category=category[i])
                selected_data_multiple[i] = self.select_stats_data_by_data_name(data_name, data=data_multiple[i])
                if data_name == "MRD":
                    selected_data_multiple[i] = [x[column] for x in selected_data_multiple[i]]
            selected_data = selected_data_multiple
            data = data_multiple
            ####
            bins = self.__create_bins_from_data(bins, selected_data[0], equal_counts=equal_counts)
            bin_location_multiple = []
            for i in range(len(selected_data)):
                bin_location_multiple.append(0)
                bin_location_multiple[i] = np.digitize(selected_data[i], bins)
            bin_location = bin_location_multiple

            bin_min = bins[0]
            bin_max = bins[-1]

            events_per_bin = np.zeros((len(selected_data), len(bins)))
            correct_classifications_per_bin = np.zeros((len(selected_data), len(bins)))
            for cat in range(len(category)):
                for i in range(len(selected_data[cat])):
                    # -1 is to compensate for np.digitize first bin position being 1, not 0.
                    events_per_bin[cat][bin_location[cat][i] - 1] += 1

                    # All parts of the category identifiers need to match. This is a stupidly long expression for this
                    # simple function, couldn't really get it to work in a simpler way, but this works. Can definitely
                    # be improved..
                    matching_categories = True
                    for j in range(len(self.category_values_dict[category[cat]])):
                        # the 3 corresponds to self.__predicted_category_values
                        if data[cat][i][3][j] != self.category_values_dict[category[cat]][j]:
                            matching_categories = False
                            break
                        else:
                            continue
                    if matching_categories:
                        if selected_data[cat][i] > bins[-1]:
                            continue
                        elif selected_data[cat][i] < bins[0]:
                            continue

                        correct_classifications_per_bin[cat][bin_location[cat][i] - 1] += 1
            percentage_correct = np.zeros((len(selected_data), len(bins)))
            for cat in range(len(category)):
                for i in range(len(bins)):
                    if events_per_bin[cat][i] == 0:
                        percentage_correct[cat][i] = 0
                    else:
                        percentage_correct[cat][i] = correct_classifications_per_bin[cat][i] / events_per_bin[cat][i]

        else:
            data = self.select_stats_data_by_category(category=category)
            selected_data = self.select_stats_data_by_data_name(data_name, data=data)
            if data_name == "MRD":
                selected_data = [x[column] for x in selected_data]
            bins = self.__create_bins_from_data(bins, selected_data, equal_counts=equal_counts)

            bin_min = bins[0]
            bin_max = bins[-1]

            bin_location = np.digitize(selected_data, bins)

            events_per_bin = np.zeros(len(bins))
            correct_classifications_per_bin = np.zeros(len(bins))
            for i in range(len(selected_data)):
                # -1 is to compensate for np.digitize first bin position being 1, not 0.
                events_per_bin[bin_location[i] - 1] += 1

                # All parts of the category identifiers need to match. This is a stupidly long expression for this
                # simple function, couldn't really get it to work in a simpler way, but this works. Can definitely be
                # improved..
                matching_categories = True
                for j in range(len(self.category_values_dict[category])):
                    # the 3 corresponds to self.__predicted_category_values
                    if data[i][3][j] != self.category_values_dict[category][j]:
                        matching_categories = False
                        break
                    else:
                        continue
                if matching_categories:
                    if selected_data[i] > bin_max or selected_data[i] < bin_min:
                        continue
                    correct_classifications_per_bin[bin_location[i] - 1] += 1

            percentage_correct = np.zeros(len(bins))
            for i in range(len(bins)):
                if events_per_bin[i] == 0:
                    percentage_correct[i] = 0
                else:
                    percentage_correct[i] = correct_classifications_per_bin[i] / events_per_bin[i]

        if plot_at_center_of_bins:
            bins_centered = []
            for i in range(1, len(bins)):
                bins_centered.append((bins[i - 1] + bins[i]) / 2)
            bins_centered.append(bins[-1] + ((bins[-1] - bins[-2]) / 2))
            # percentage_correct = percentage_correct[:-1]
            bins = bins_centered

        error_bar_upper, error_bar_lower = [], []
        if error_bars:
            if type(category) == list:
                total_error_bars_upper = []
                total_error_bars_lower = []
                for cat in range(len(category)):
                    error = np.array([sm.proportion_confint(correct_classifications_per_bin[cat][i],
                                                            events_per_bin[cat][i],
                                                            method="beta", alpha=0.39)
                                      for i in range(len(bins))])
                    error_bar_upper = error[:, 0] - percentage_correct[cat]
                    error_bar_lower = percentage_correct[cat] - error[:, 1]
                    total_error_bars_upper.append(error_bar_upper)
                    total_error_bars_lower.append(error_bar_lower)

                    if return_data:
                        pass
                    else:
                        if type(color) == list:
                            if xticks is not None:
                                _ = ax.errorbar(xticks, percentage_correct[cat][:-1],
                                                yerr=(error_bar_lower[:-1], error_bar_upper[:-1]), fmt='o',
                                                label=category[cat], markersize=5, alpha=1, elinewidth=2,
                                                color=color[cat],
                                                capsize=9, **kwargs)
                            else:
                                _ = ax.errorbar(bins[:-1], percentage_correct[cat][:-1],
                                                yerr=(error_bar_lower[:-1], error_bar_upper[:-1]), fmt='o',
                                                label=category[cat], markersize=5, alpha=1, elinewidth=2,
                                                color=color[cat],
                                                capsize=9, **kwargs)
                        else:
                            llbl = category[cat]
                            if "label" in kwargs:
                                llbl = kwargs.pop("label")
                            if xticks is not None:
                                _ = ax.errorbar(xticks, percentage_correct[cat][:-1],
                                                yerr=(error_bar_lower[:-1], error_bar_upper[:-1]), fmt='o',
                                                label=llbl, markersize=5, alpha=1, elinewidth=2, capsize=9,
                                                **kwargs)
                            else:
                                _ = ax.errorbar(bins[:-1], percentage_correct[cat][:-1],
                                                yerr=(error_bar_lower[:-1], error_bar_upper[:-1]), fmt='o',
                                                label=llbl, markersize=5, alpha=1, elinewidth=2, capsize=9,
                                                **kwargs)
                if return_data:
                    return [bins, percentage_correct, (total_error_bars_upper, total_error_bars_lower)]
            else:
                error = np.array(
                    [sm.proportion_confint(correct_classifications_per_bin[i][:-1], events_per_bin[i][:-1],
                                           method="beta",
                                           alpha=0.39)
                     for i in range(len(bins))])
                error_bar_upper = error[:, 0] - percentage_correct
                error_bar_lower = percentage_correct - error[:, 1]

                if category is None:
                    category_lbl = "All categories"
                else:
                    category_lbl = category
                if xticks is not None:
                    _ = ax.errorbar(xticks, percentage_correct[:-1],
                                    yerr=(error_bar_lower[:-1], error_bar_upper[:-1]),
                                    label=category_lbl,
                                    fmt='o', markersize=5, alpha=1, elinewidth=2, capsize=9, **kwargs)
                else:
                    _ = ax.errorbar(bins[:-1], percentage_correct[:-1],
                                    yerr=(error_bar_lower[:-1], error_bar_upper[:-1]),
                                    label=category_lbl,
                                    fmt='o', markersize=5, alpha=1, elinewidth=2, capsize=9, **kwargs)
        else:
            if type(category) == list:
                for cat in range(len(category)):
                    if xticks is not None:
                        _ = ax.scatter(xticks, percentage_correct[cat][:-1], alpha=1, label=category[cat], **kwargs)
                    else:
                        _ = ax.scatter(bins[:-1], percentage_correct[cat][:-1], alpha=1, label=category[cat], **kwargs)
            else:
                if category is None:
                    category_lbl = "All categories"
                elif "label" in kwargs:
                    pass
                else:
                    category_lbl = category
                if xticks is not None:
                    _ = ax.scatter(xticks, percentage_correct, alpha=1, label=category_lbl, **kwargs)
                else:
                    _ = ax.scatter(bins, percentage_correct, alpha=1, label=category_lbl, **kwargs)

        if xticks_major is not None and xticks_minor is not None and xtick_labels_minor is not None and \
                xtick_labels_major is not None:
            ax.set_xticks(ticks=xticks_minor, minor=True, labels=xtick_labels_minor)
            ax.set_xticks(ticks=xticks_major, minor=False, labels=xtick_labels_major)

            if grid:
                ax.grid(axis="x", which="major")

        if yticks_major is not None and yticks_minor is not None and ytick_labels_minor is not None and \
                ytick_labels_major is not None:
            ax.set_yticks(ticks=yticks_minor, minor=True, labels=ytick_labels_minor)
            ax.set_yticks(ticks=yticks_major, minor=False, labels=ytick_labels_major)

            if grid:
                ax.grid(axis="y", which="major")

        if title is None:
            title = f"{self.model_name} - Accuracy plot of CNN prediction for {category} {data_name}"
        ax.set_title(title)

        ax.legend(loc='best', fontsize=11)

        ax.set_xlabel(data_name) if xlbl is None else ax.set_xlabel(xlbl)
        ax.set_ylabel("Probability of correct guess") if ylbl is None else ax.set_ylabel(ylbl)

        self._set_lims_ax(ax, xlim, ylim)

        if return_data:
            return [bins, percentage_correct, (error_bar_lower, error_bar_upper)]

        self.show_handler(fig, show)

        if savefig:
            self._save_fig(fig, file_format, filename)

        if return_fa:
            if fa is None:
                fa = (fig, ax)
            return fa

    def mrd_hist(self,
                 column: int,
                 bins: Union[int, None] = None,
                 category=None,

                 title: Union[None, str] = None,
                 xlim=None,
                 ylim=None,
                 xlbl: str = None,
                 ylbl: str = None,

                 show: bool = True,
                 return_data: bool = False,
                 savefig: bool = False,
                 file_format: str = "pdf",
                 filename: str = None,

                 fa: List = None,
                 return_fa: bool = None,

                 **kwargs) -> Union[None, List]:
        """
        :param fa: Pass matplotlib figure and ax object as a Tuple or List type to which the curve will be plotted.
            If fa == None, a new fig and ax will be created.
        :param return_fa: Returns figure and ax object as List.
        TODO: DOCSTR
        """
        data = []
        if "MRD" in self.stats_dict:
            if category is None:
                data = self.select_stats_data_by_data_name("MRD")
            else:
                data = self.select_stats_data_by_category(category)
                data = self.select_stats_data_by_data_name("MRD", data=data)
        elif "MRD" in self.data_dict:
            print("Currently this functions only supports loading MRD data_container from stats data_container.")
            return None
        else:
            return None

        selected_column_data = [x[column] for x in data]

        if return_data:
            return selected_column_data

        bins = self.__create_bins_from_data(bins, selected_column_data)

        fig, ax = self.fa_gen(fa)

        _ = ax.hist(selected_column_data, bins=bins, **kwargs)

        if category is None:
            category = "all categories"
        if title is None:
            ax.set_title(f"{self.model_name} - Histogram with {len(bins) - 1} bins. "
                         f"\n Plotting MRD column {column} data_container for the category {category}.")
        else:
            ax.set_title(f"{title}")

        ax.legend(loc='best', fontsize=11)

        ax.set_xlabel(f"MRD entry {column}") if xlbl is None else ax.set_xlabel(xlbl)
        ax.set_ylabel("Count") if ylbl is None else ax.set_ylabel(ylbl)

        self._set_lims_ax(ax, xlim, ylim)

        self.show_handler(fig, show)

        if savefig:
            self._save_fig(fig, file_format, filename)

        if return_fa:
            if fa is None:
                fa = (fig, ax)
            return fa

    """
    Some quick analysis and helper methods following, that produce standard and often used plots.
    """

    def full_ana(self, path: str = None, hists=True):
        """Plot all useful analysis plots. Includes:
        - cm if applicable
        - accuracy if applicable
        - ROC if applicable
        - prediction per bin (all classes) vs. VisibleEnergy
        - probability histogram (all classes)
        - histograms for all data specified in self.data_dict() except for charge, charge_abs, time and time_abs data
        - TODO
        """

        save_dics = ["histogram", "accuracy", "roc", "probhist"]
        for dic in save_dics:
            Path(path + dic).mkdir(parents=False, exist_ok=True)

        if not self.real_test_data:
            self.plot_confusion_matrix(savefig=True,
                                       filename=path + F"{self.model_name}_cm",
                                       title=f"CM - {self.model_name}\nAccuracy: {self.accuracy*100:.2f} %")
            fig, ax = self.plot_accuracy(data_name="VisibleEnergy",
                                         category=list(self.category_values_dict.keys()),
                                         bins=[500 * i for i in range(0, 15)],
                                         return_fa=True,
                                         error_bars=True,
                                         title=f"Prediction accuracy vs. visible energy - {self.model_name}"
                                         )
            ax.grid("both")
            ax.set_xlabel("Visible energy [p.e.]")
            self._save_fig(fig, filename=path + f"accuracy/{self.model_name}_accuracy_visible_energy")

            for category in self.category_values_dict.keys():
                """
                fig, ax = self.plot_accuracy(category=category,
                                             data_name="VisibleEnergy",
                                             bins=[500 * i for i in range(0, 15)],
                                             return_fa=True,
                                             title="Accuracy vs. visible energy" \
                                                   + f"- {self.model_name}\nCategory: {category}")
                ax.grid("both")
                self._save_fig(fig, filename=path + f"accuracy/{self.model_name}_accuracy_visible_energy_{category}")
                """
                fig, ax = self.plot_roc(category=category, return_fa=True,
                                        title=f"ROC - {self.model_name} - signal: {category}",
                                        color="dimgrey")
                ax.grid("both")
                self._save_fig(fig, filename=path + f"roc/{self.model_name}_roc_{category}")

        if hists:
            for data_name in self.stats_dict.keys():
                kw_args_hists = {
                    "alpha": 0.6,
                    "return_fa": True,
                    "log": True,
                    "data_name": data_name,
                    "title": f"{self.model_name} - {data_name} histogram"
                }
                if data_name in ["charge", "charge_abs", "time", "time_abs"]:
                    continue
                if data_name in ["MRD", "mrd"]:
                    continue
                    # self.mrd_hist()  # Todo single cols + all cols together
                if data_name in ["param", "params", "PARAM"]:
                    continue
                if data_name == "VisibleEnergy":
                    fig, ax = self.plot_histogram(category=list(self.category_values_dict.keys()),
                                                  bins=[i * 200 for i in range(36)],
                                                  **kw_args_hists)
                    ax.grid("both")
                    self._save_fig(fig, filename=path + f"histogram/{self.model_name}_visible_energy")
                if data_name == "Rings":
                    fig, ax = self.plot_histogram(category=list(self.category_values_dict.keys()),
                                                  bins=np.arange(0, 12, 1),
                                                  **kw_args_hists)
                    ax.grid("both")
                    self._save_fig(fig, filename=path + f"histogram/{self.model_name}_{data_name}")
                if data_name in ["MuonNumber", "ElectronNumber", "KaonNumber"]:
                    fig, ax = self.plot_histogram(category=list(self.category_values_dict.keys()),
                                                  bins=np.arange(0, 6, 1),
                                                  **kw_args_hists)
                    ax.grid("both")
                    self._save_fig(fig, filename=path + f"histogram/{self.model_name}_{data_name}")
                if data_name in ["NeutronNumber"]:
                    fig, ax = self.plot_histogram(category=list(self.category_values_dict.keys()),
                                                  bins=np.arange(0, 10, 1),
                                                  **kw_args_hists)
                    ax.grid("both")
                    self._save_fig(fig, filename=path + f"histogram/{self.model_name}_{data_name}")
                else:
                    fig, ax = self.plot_histogram(category=list(self.category_values_dict.keys()),
                                                  bins=np.arange(0, 12, 1),
                                                  **kw_args_hists)
                    ax.grid("both")
                    self._save_fig(fig, filename=path + f"histogram/{self.model_name}_{data_name}")

        fig, ax = self.plot_probability_histogram(category=None,
                                                  return_fa=True,
                                                  log=True,
                                                  title=f"Prediction histogram - {self.model_name}")
        ax.grid("both")
        self._save_fig(fig, filename=path + f"probhist/{self.model_name}__all")

        for category in self.category_values_dict.keys():
            fig, ax = self.plot_probability_histogram(category=category,
                                                      return_fa=True,
                                                      log=True,
                                                      title="Prediction histogram -" \
                                                            + f" {self.model_name} - Category {category}")
            ax.grid("both")
            self._save_fig(fig, filename=path + f"probhist/{self.model_name}_{category}")

        return


class Bundle:
    def __init__(self, evals: List[Evaluator], real_data_indices=None):
        self.evals = evals
        self.real_data_indices = real_data_indices

    def plot_percent_predicted(self, *args, **kwargs):
        """Plots predicted count / total count per bin vs. data_name for each member of self.evals."""
        for evaluator in self.evals:
            evaluator.plot_percent_predicted(*args, **kwargs)

    def plot_prediction_accuracy(self, *args, **kwargs):
        """ Calls plot_prediction_confidence for each member of self.evals which support plot_prediction_confidence. """
        for i in range(len(self.evals)):
            if i not in self.real_data_indices:
                (self.evals[i]).plot_prediction_confidence(*args, **kwargs)
            else:
                pass

    def plot_probability_histogram(self,
                                   bins: Union[None, str, List, int] = None,
                                   log: bool = True,
                                   density: bool = False,
                                   show: bool = True,
                                   *args,
                                   **kwargs):
        """
        Plots y_prob % 'confidence' for an event. See also Evaluator.plot_probability_histogram()

        :param bins: Will be passed on to the evaluator to create bins. See Evaluator.__create_bins_from_data()
        :param log: Defines whether the histogram will be plotted in log or non log format.
        :param density: Normalizes the area under the curve to unit area.
        """
        to_plot = []
        for i in range(len(self.evals)):
            if i in self.real_data_indices:
                ret = (self.evals[i]).plot_probability_histogram(show=show, *args, **kwargs)
                if ret is not None:
                    to_plot.append([ret, i])
                else:
                    pass
            else:
                pass
        if to_plot:
            for entry in to_plot:
                print(entry[0][2])
                _ = plt.hist([*entry[0][0], *entry[0][1]], bins=entry[0][2], histtype="bar",
                             label=f"Prediction % for selected class of {self.evals[entry[1]].model_name}",
                             alpha=0.5, density=density, log=log)
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fontsize=11)

                plt.xlabel(f"Predicted probability of being of the selected class")
                plt.ylabel("Count")
            if show:
                plt.show()

    def plot_confusion_matrix(self, *args, **kwargs):
        for i in range(len(self.evals)):
            if self.real_data_indices:
                if i not in self.real_data_indices:
                    (self.evals[i]).plot_confusion_matrix(*args, **kwargs)
                else:
                    pass
            else:
                (self.evals[i]).plot_confusion_matrix(*args, **kwargs)

    def plot_histogram(self, *args, **kwargs) -> None:
        """
        Plot a histogram (number of counts vs data_container).
        """
        for evaluator in self.evals:
            evaluator.plot_histogram(*args, **kwargs)

    def plot_accuracy(self, *args, **kwargs) -> None:
        """
        Plot model accuracy (accuracy vs data_container).
        ----------------------------------------------------------------------------------------------------------------
        Note:
        -----
        Data points beyond - if provided - xlim are automatically dropped; if no xlim has been provided, discounts all
        data_container points beyond the first and last bin border.
        """
        for i in range(len(self.evals)):
            if i not in self.real_data_indices:
                (self.evals[i]).plot_accuracy(*args, **kwargs)
            else:
                pass


class DataVis(celfa_data.ExperimentalData):

    def __init__(self,
                 container: Union[celfa_data.ExperimentalData, celfa_data.SimulationData]):
        """Initializes all members of ExperimentalData or SimulationData, based on which container has been provided."""
        self.net_data_indices = container.net_data_indices
        self.stats_data_indices = container.stats_data_indices
        self.data_dict = container.data_dict
        self.data = container.data
        self.input_layers = container.input_layers

        if type(container) == celfa_data.ExperimentalData:
            pass
        elif type(container) == celfa_data.SimulationData:
            self.category_values = container.category_values
            self.cat_values_dict = container.cat_values_dict

    def save_fig(self,
                 fig: plt.figure = None,
                 file_format: Union[str, List[str]] = None,
                 filename: str = None) -> None:
        """
        Save a figure.

        :param file_format: Format of the saved file. Default = ["pdf", "png"]. Pass array to save in multiple formats.
        :param filename: Filename of the saved figure.
        :return: None
        """

        if file_format is None:
            file_format = ["pdf", "png"]

        filename = self.model_name if filename is None else filename

        plt.figure(fig.number)
        if type(file_format) is str:
            fig.savefig(filename, format=file_format, bbox_inches="tight")

        if type(file_format) is list:
            for ff in file_format:
                fig.savefig(filename + "." + ff, format=ff, bbox_inches="tight")

    def select_data(self,
                    index: int = None,
                    data_name: str = None) -> Union[None, List]:
        dcpy = []
        if index is not None:
            pass

        elif data_name is not None:
            index = self.data_dict[data_name]

        try:
            for event in self.data:
                dcpy.append(event[index])

        except IndexError:
            print("No viable index / data_name provided."
                  " Cannot access event[i][index] or event[i][data_dict['data_name']].")
            return None

        return dcpy

    def plot_2d_charge_hist(self,
                            data_name: str = "charge_abs",
                            xlim: Union[List, tuple, object] = None,
                            return_data: bool = False,
                            binmaxy: int = 10000,
                            binnumy: int = 100,
                            return_fig: bool = False) -> Union[None, np.ndarray, object]:
        """

        :param xlim: X Limits of the histogram. If both return_fig and return_data are true, returns both, data first.
        :param return_data: Returns 2d-array of histogram values.
        :param binmaxy: Bin maximum of the y-axis (VisibleEnergy).
        :param binnumy: Bin count on the y-axis.
        :param return_fig: Returns the figure object. If both return_fig and return_data are true, returns both, data
            first.
        :return:
        """
        charge_data_mrdmc = []
        charge_data_abs_mrdmc = []

        number_of_pixels_mrdmc = []

        norm_data = self.select_data(data_name="charge")
        abs_data = self.select_data(data_name="charge_abs")
        for i in range(len(self)):
            tempc = 0
            for pixel in norm_data[i]:
                if pixel != 0:
                    tempc += 1
            number_of_pixels_mrdmc.append(tempc)
            charge_data_mrdmc.append(norm_data[i])
            charge_data_abs_mrdmc.append(abs_data[i])

        charge_data_mrdmc = np.reshape(np.array(charge_data_mrdmc), (-1, 1))
        charge_data_abs_mrdmc = np.reshape(np.array(charge_data_abs_mrdmc), (-1, 1))

        numcutsalldatasets = []
        for i in range(1):
            t_charge_data_abs = np.array(self.select_data(data_name=data_name)[:])

            events_sorted_by_number_pmt = [[] for _ in range(160)]
            # for cut in [0.5,1,1.5,2,2.5,3,4,5,6,7,8,9,10,20,50,100]:
            # print(i, cut)

            for entry in t_charge_data_abs:
                tempc = 0

                for pixel in entry:
                    if pixel > 0:
                        tempc += 1

                events_sorted_by_number_pmt[tempc].append(entry)

            numcutsalldatasets.append(events_sorted_by_number_pmt)

        doublebindata = [[[] for _ in range(160)] for __ in range(3)]

        for datseti in range(len(numcutsalldatasets)):
            for datsetibynum in range(len(numcutsalldatasets[datseti])):
                for ev in numcutsalldatasets[datseti][datsetibynum]:
                    doublebindata[datseti][datsetibynum].extend([*ev])

        hists_1 = []
        bins = np.linspace(0.00000001, binmaxy, binnumy)
        for one_data in doublebindata[0][:]:
            thistdata = plt.hist(one_data, bins)
            hists_1.append(thistdata[0])

        hists_1 = np.transpose(hists_1)

        fig, ax = plt.subplots(1, 1, figsize=(7, 7), dpi=400)

        # background
        cmap = matplotlib.cm.get_cmap('jet')
        rgba = cmap(0.0)
        # ax.set_facecolor(rgba)

        # plot data
        im = ax.imshow(np.array(hists_1), origin="lower", cmap=cmap, norm=matplotlib.colors.LogNorm())

        # colorbarstuff
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='7%', pad=0.05)

        fig.colorbar(im, cax=cax, orientation='vertical')

        # ytick stuff
        labels = [item.get_text() for item in ax.get_xticklabels()]
        labels = [f"{round(i, 4)}" for i in np.arange(0, binmaxy, binmaxy / 10)]

        ax.set_yticks([round(i, 4) for i in np.arange(0, binnumy, binnumy / 10)])
        ax.set_yticklabels(labels)

        # lims
        ax.set_xlim(xlim)
        # TODO: set_ylim(ylim)

        # aesthetics
        ax.set_title("VisibleEnergy histograms vs. active PMT count; beam data")

        ax.set_ylabel("VisibleEnergy [p.e.]")
        ax.set_xlabel("Number of active PMTs")

        if return_data and not return_fig:
            return np.array(hists_1)
        if not return_data and return_fig:
            return fig
        if return_data and return_fig:
            return np.array(hists_1), fig

        plt.show()

    def plot_charge_hist(self,
                         normalized=True,
                         **kwargs):
        """
        :param normalized: If true, use normalized charge data. If false, use absolute.
        :return:
        """
        data_name = "charge" if normalized else "charge_abs"
        data = self.select_data(data_name=data_name)
        plt.hist(data, **kwargs)
