import pandas as pd
import numpy as np
import re


class Node:

    def __init__(self, parent, children, rule, label=None):
        self.parent = parent  # node
        self.children = children  # array of nodes
        self.rule = rule  # tuple
        self.leaf = (True if self.children else False)  # boolean
        if self.leaf:
            self.label = label

    def check_rule(self, record):
        index, regex = self.rule
        record = record[index:]
        match = re.search(pattern=regex, string=record)
        return match


class DecisionTree:

    def __init__(self, R, dataframe):
        self.R = R  # array of tuples
        self.nodes = np.array([Node(parent=None, children=None, rule=None)])
        self.S = dataframe.T.to_dict().values()  # list array od dicts

    @staticmethod
    def divide_set(data, node):
        positive_set = []
        negative_set = []
        for d in data:
            if node.check_rule(d['Sequence']):
                positive_set.append(d)
            else:
                negative_set.append(d)
        return positive_set, negative_set

    # TODO: finish this
    @staticmethod
    def inf_gain(data, rule):
        # calculate the frequency of class 1
        counter = 0
        for d in data:
            if data['Cut'] == 1:
                counter += 1
        f_c = counter / len(data)



    def id3(self, R, S):

        assert S is not None




