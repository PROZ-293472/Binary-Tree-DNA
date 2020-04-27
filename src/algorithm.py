import pandas as pd
import numpy as np
import re
import math


class Util:

    @staticmethod
    def check_rule(record, rule):
        index, regex = rule
        record = record[index:]
        match = re.search(pattern=regex, string=record)
        return match



class Node:

    def __init__(self, parent, rule, leaf=False, label=None):
        self.parent = parent  # node
        self.children = []  # array of nodes
        self.rule = rule  # tuple
        self.leaf = leaf
        self.label = label


class DecisionTree:

    def __init__(self, R, dataframe):
        self.R = R  # array of tuples
        self.nodes = np.array([Node(parent=None, children=None, rule=None)])
        self.S = dataframe.T.to_dict().values()  # list array of dicts

    @staticmethod
    def divide_set(data, node=None, rule=None):
        assert node is not None or rule is not None
        positive_set = []
        negative_set = []

        if node:
            r = node.rule
        if rule:
            r = rule

        for d in data:
            if Util.check_rule(d['Sequence'], r):
                positive_set.append(d)
            else:
                negative_set.append(d)
        return positive_set, negative_set

    @staticmethod
    def entrophy(data):
        counter = 0
        for d in data:
            if d['Cut'] == 1:
                counter += 1
        f_1 = counter / len(data)
        f_0 = 1 - f_1

        entrophy = -1 * (f_1 * math.log(f_1) + f_0 * math.log(f_0))
        return entrophy

    @staticmethod
    def inf_gain(data, rule):
        i = DecisionTree.entrophy(data)

        sets = DecisionTree.divide_set(data, rule=rule)
        inf = 0.0
        for s in sets:
            inf += len(s)/len(data) * DecisionTree.entrophy(s)

        infgain = i - inf
        return infgain

    @staticmethod
    def id3(root, rules, data):
        assert data is not None

        if DecisionTree.entrophy(data) == 0:
            root.children.append(Node(parent=root, rule=None, leaf=True, label=data[0]['Cut']))
            return

        if len(rules) == 0:
            counter = 0
            for d in data:
                if d['Cut'] == 1:
                    counter += 1
            f_1 = counter / len(data)
            f_0 = 1 - f_1
            label = f_1 if f_1 > f_0 else f_0
            root.children.append(Node(parent=root, rule=None, leaf=True, label=label))
            return

        best_infgain = -math.inf
        best_rule = []
        for r in rules:
            ig = DecisionTree.inf_gain(data, r)
            if ig > best_infgain:
                best_infgain = ig
                best_rule = r
        rules.remove(best_rule)

        n = Node(parent=root, rule=best_rule)
        root.children.append(n)

        sets = DecisionTree.divide_set(data, node=n)

        for s in sets:
            DecisionTree.id3(root=n, rules=rules, data=s)






