import os
import numpy as np
import matplotlib.pyplot as plt
from file_task import File_work
import warnings
import pandas as pd

fw = File_work()


class Plots:
    def __init__(self, data=None, list_of_df=None, data_ind=None):
        """
        Class for build plots, scatter and other image (e.g. LaTeX image)
        :param data: pd.DataFrame which plot needed
        """
        self.list_of_df = list_of_df
        if data is not None:
            self.data = data
        elif list_of_df is not None and data_ind is not None:
            self.data = list_of_df[data_ind]
        elif data is None and list_of_df is None:
            warnings.warn('Empty data')
            self.data = data
        self.load_conf()
        self.n = 0

    def __add__(self, other):
        """
        Func for create list of pd.DataFrames from 2 independent pd.DataFrames
        :type other: pd.DataFrame
        :param other: some pd.DataFrame
        :return list_of_df: list of pd.DataFrames
        """
        try:
            self.list_of_df.append(other)
        except AttributeError:
            self.list_of_df = [self.data, other]
        return self.list_of_df

    def merge_df(self, other):
        """
                Func for concat pd.DataFrames plots for one plot
                :param other: python module Plots (pd.DataFrame)
                :return: concat python module Plots (pd.DataFrame)
                """
        if len(self.data.columns) == len(other.columns) == 1:
            if self.data.columns[0] == other.columns[0]:
                self.data.join(other.set_index(
                    other.columns[0]
                ), on=other.columns[0])
            else:
                other.columns = self.data.columns
                self.data.join(other.set_index(
                    other.columns[0]
                ), on=other.columns[0])
        elif len(self.data.columns) == len(other.columns):
            self.col_of_similar_name = np.array(self.data.columns).sort().isin(np.array(other.columns).sort())
            if self.col_of_similar_name:
                raise warnings.warn(
                    "You try merge 2 pd.DataFrames with more then two key-values. "
                    "Try create pd.Dataframe with Pandas merge and put this df on Plots class")

    def update_data(self, data):
        """
        Optimisation func. This func can delete old pd.DataFrame from
        class variables and put new data without call self.data
        :param data: new data for plot
        :return: Void
        """
        self.data = data

    def load_conf(self):
        """
        This func load config from environ to list, which used by other func
        :return:
        """
        if os.getenv('PLOT_TYPE').lower() == 'plot':
            self.dict_plot = {
                "color": os.getenv("COLOR"),
                "drawstyle": os.getenv("DRAWSTYLE"),
                "marker": os.getenv("MARKER"),
                "markersize": os.getenv("MARKERSIZE"),
                "fillstyle": os.getenv("FILLSTYLE"),
                "linewidth": os.getenv("LINEWIDTH")
            }
        elif os.getenv('PLOT_TYPE').lower() == 'hist':
            self.dict_plot = {
                "color": os.getenv("COLOR"),
                "edgecolor": os.getenv("EDGECOLOR"),
                "xerr": os.getenv("XERR"),
                "yerr": os.getenv("YERR"),
                "ecolor": os.getenv("ECOLOR"),
                "capsize": os.getenv("CAPSIZE")
            }
        elif os.getenv('PLOT_TYPE').lower() == 'scatter':
            self.dict_plot = {
                "color": os.getenv("COLOR"),
                "width": os.getenv("WIDHTS"),
                "edgecolors": os.getenv("EDGECOLORS"),
                "facecolors": os.getenv("FACECOLORS"),
                "linewidth": os.getenv("LINEWIDTH")
            }
        for i in self.dict_plot.keys():
            if self.dict_plot[i] == "None":
                self.dict_plot.update({i: None})

    # Func for feature realise
    # def lock_conf(self, conf):
    #    """
    #    Func for disable some conf from .env
    #    :param conf: list of conf
    #    """va

    def build_one_plot(self, show=True, save=True, list_of_suffix=None):
        """
        Func to create code more 'readability', simple and object-oriente.
        :return: matplotlib.pyplot for saving % showing
        """
        if list_of_suffix is None:
            list_of_suffix = []
        index = range(len(self.data))

        if os.getenv('PLOT_TYPE') == 'plot':
            plt.plot(index, self.data[self.data.columns[-1]],
                     **self.dict_plot)

        if os.getenv('PLOT_TYPE') == 'scatter':
            plt.scatter(index, np.array(self.data[self.data.columns[-1]]),
                        **self.dict_plot)

        if os.getenv('PLOT_TYPE') == 'hist':
            plt.bar(index, np.array(self.data[self.data.columns[-1]]),
                    **self.dict_plot)

        plt.xticks(index, self.data.index)
        plt.xlabel(os.getenv('XLABEL'))
        plt.ylabel(os.getenv('YLABEL'))
        plt.title(os.getenv('TITLE'))

        if save:
            try:
                plt.savefig(fw.directhion_path +
                            '\\Output\\img_{}'.format(os.getenv('XLABEL')))
                self.n += 1
            except IndexError:
                list_of_suffix = [x for x in range(10)]
                plt.savefig(fw.directhion_path +
                            '\\Output\\img\\img_{}'.format(os.getenv('XLABEL')))
                self.n += 1
        if show:
            plt.show()

    def connect_plots(self, save=True, show=True, list_of_suffix=None):
        """
        Func for append 2 or more plots to one figure and print this
        plot on one screen.
        :param list_of_df: list of pd.DataFrames
        :return: matplotlib.Figure
        """
        fig, axarr = plt.subplots(int(os.getenv("CONCAT_SHAPEX")),
                                  int(os.getenv("CONCAT_SHAPEY")))
        fig.suptitle(os.getenv('CONCAT_TITLE'))
        j = 1
        for i in self.list_of_df:
            self.data = pd.DataFrame(i)
            try:
                if divmod(int(os.getenv("CONCAT_DIM")), 2)[1] == 0:
                    plt.subplot(2, int(os.getenv("CONCAT_DIM"))/2,
                                int(os.getenv("CONCAT_DIM"))/2)
                else:
                    plt.subplot(2, int(os.getenv("CONCAT_DIM"))/2,
                                divmod(int(os.getenv("CONCAT_DIM")), 2)[0]+1)

            except ValueError:
                raise ValueError("Something wrong... If num of plots didn't equal to {}, please, fix .env file"
                                 .format(os.getenv("CONCAT_DIM")))
            self.build_one_plot(show=False, save=False)
            j += 1

        if save:
            try:
                plt.savefig(fw.directhion_path +
                            '\\Output\\img_{}'.format(list_of_suffix[self.n]))
                self.n += 1
            except IndexError:
                list_of_suffix = [x for x in range(10)]
                plt.savefig(fw.directhion_path +
                            '\\Output\\img\\img_{}'.format(list_of_suffix[self.n]))
                self.n += 1
            except TypeError:
                list_of_suffix = [x for x in range(10)]
                plt.savefig(fw.directhion_path +
                            '\\Output\\img\\img_{}'.format(list_of_suffix[self.n]))
        if show:
            plt.show()

    #    fig, axarr = plt.subplots(2, 3, sharex=True, sharey=True)  # 6 axes, returned as a 2-d array

    #    for i in range(2):
    #        for j in range(3):
    #            plt.sca(axarr[i, j])  # set the current axes instance
    #            axarr[i, j].plot(i, j, 'ro', markersize=10)  # plot
    #            axarr[i, j].set_xlabel(str(tuple([i, j])))  # set x label
    #            axarr[i, j].get_xaxis().set_ticks([])  # hidden x axis text
    #            axarr[i, j].get_yaxis().set_ticks([])  # hidden y axis text

    #            plt.show()

    # Reshape - next version
    """
    def reshaping(self):

        Func for reshaping values in most common way
        :return: tuple of plots in figure like (x, y)


        self.hypnotises_value = np.sqrt(len(self.list_of_df))
        self.checked_number = np.sqrt(len(self.list_of_df)). \
            __divmod__(1)
        if self.checked_number[1] == 0:
            self.shape = (self.hypnotises_value,
                          self.hypnotises_value)
        else:
            if (len(self.list_of_df)-int(self.hypnotises_value)).__divmod__(2)[1] == 0:
                self.shape = (int(self.hypnotises_value) + (int(self.hypnotises_value) / 2),
                              int(self.hypnotises_value) + (int(self.hypnotises_value) / 2))
            else:
                self.shape = (int(self.hypnotises_value) + (int(self.hypnotises_value) / 2)+1,
                              int(self.hypnotises_value) + int(self.hypnotises_value) / 2)
        print(self.shape)
        """
