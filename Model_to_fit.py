"""
This script contains 3 type of binary regression. In this model we build model with 2 hypothesis:
    H0: client didn't have insurance case on condition of [num_of_factors] ();
    H1: client did have insurance case on condition of [num_of_factors].
For fit this model we have all needed data:
    1) Aprior probability;
    2) Factors from some client (sex, card cash flow, active insurance etc.)
For estimate posterior probability of some factor we have 2 algorithm:
    1) MCMC (Monte-Carlo Markov Chain);
    2) Grid methods.

"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from file_task import *
from IPython.display import SVG
import IPython.display

# from Logit_model import *
# from Probit_model import *
# from Cloglog_model import *

fw = File_work()


class SVG_view(object):
    def __init__(self, svg):
        self.svg = svg

    def _repr_pretty_(self):
        import os
        os.system(
            r"start file:///C:/Users/19354877/Desktop/Pycharm/Card_insurance_modeling/Data_storage/network.svg"
        )

    def __repr__(self):
        return str(self.svg)


class CSV_view(object):
    def __init__(self, links):
        self.links = links

    def _repr_pretty(self, file):
        import os
        for i in self.links:
            os.system(
                r"{}".format(i)
            )

    def __repr__(self):
        return str(self.links)


class BN_creator:

    def __init__(self, df_basic):
        """
        Class for build needed models.
        :param df_basic: pd.DataFrame with real data from DB
        :type Model_type: Models_creator.Model_type
        :type df_basic: pd.DataFrame()
        """
        self.df_prior = []
        self.df_basic = df_basic
        self.params = self.df_basic.columns


        self.n = 0

    @staticmethod
    def join_loop(lst):
        concat_lst = []
        for i in lst:
            concat_lst += i
        return concat_lst

    def prior_distribution(self, save=True, partitioned=True, length_to_part=10):
        """
        Func for create prior distribution of random sample.
        :return: list or prior distribution
        """
        self.df_basic['Q'] = np.ones([len(self.df_basic), 1])
        for i in self.params:
            self.count = self.df_basic.groupby(i).count()
            self.count[i] = self.count['Q'] / len(self.df_basic)
            print(self.count[self.count.columns[0]])
            if len(self.count) > length_to_part and partitioned:
                self.ind = []
                self.sum_arr = []
                self.interval = np.linspace(0, self.count.index[-1], 10).astype(int)
                for ii in range(len(self.interval) - 1):
                    self.ind.append('{}-{}'.format(self.interval[ii], self.interval[ii + 1]))
                    self.sum_arr.append(
                        self.count.loc[(self.count.index < self.interval[ii + 1]) &
                                       (self.count.index >= self.interval[ii])][i].sum())
                if self.count.index[-1] != self.interval[ii + 1]:
                    self.ind.append('else')
                    self.sum_arr.append(self.count.loc[self.count.index >= self.interval[ii + 1]][i].sum())
                self.df_prior.append(pd.DataFrame(self.sum_arr, index=self.ind, columns=[i]))
            else:
                self.df_prior.append(pd.DataFrame(self.count[i], index=self.count.index))
        if save:
            for i in self.df_prior:
                i.to_csv(fw.directhion_path+r'\Output\prior_distribution\{}.csv'.format(i.index.name))
        return self.df_prior

    def posterior_probab_df(self):
        """
        Func for build DF of
        :return:
        """
        # for i in self.df_prior:
        # self.df_basic.groupby(list(self.params)).count()

    def build_relationship_schema(self, save=True, show=True, show_svg = False, list_of_suffix=None, weight=True):
        """
        This func build Bayesian network which wil be estimated by MCMC and grid.
        Node and edge of graph can be updated on .env file
        :param show: bool, if True - graph wil be shown
        :param save: bool, if True - graph will be saved on %PATH%\\Output\\img\\graph.png
        :param weight: bool, write param of edge probability
        :return dict: Bayesian network with relation
        """
        g = nx.Graph()
        self.lst_nodes = [i.columns[0] for i in self.df_prior]
        g.add_nodes_from(self.lst_nodes)
        g.add_edges_from([(i, os.getenv("ESTIMATED_VAR")) for
                          i in self.lst_nodes if i != os.getenv("ESTIMATED_VAR")])
        nx.draw(g, with_labels=True, font_weight='bold')
        if save:
            try:
                plt.savefig(fw.directhion_path +
                            '\\Output\\img_{}'.format(list_of_suffix[self.n]))
                self.n += 1
            except TypeError:
                list_of_suffix = [x for x in range(10)]
                plt.savefig(fw.directhion_path +
                            '\\Output\\img\\img_{}'.format(list_of_suffix[self.n]))
                self.n += 1
            except FileNotFoundError:
                (fw.directhion_path)

        elif show:
            plt.show()

        elif show_svg:
            SVG_view(SVG('Data_storage/network.svg'))._repr_pretty_()
        # edges = list(self.df_basic.columns)
        # for i in edges:
        #    g.add_edge(tuple(i))
        # nx.draw_spectral(g)
