import copy

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

    def __init__(self, parent, rule=None, leaf=False, label=None):
        self.parent = parent  # node
        self.positive_child = []
        self.negative_child = []
        self.rule = rule  # tuple
        self.leaf = leaf
        self.label = label


class DecisionTree:

    i = 0
    def __init__(self, R, dataframe):
        self.R = R  # array of tuples
        self.root = Node(parent=None, rule=None)
        self.S = dataframe.to_dict('records')  # list array of dicts
        self.setup()

    @staticmethod
    def divide_set(data, rule):
        positive_set = []
        negative_set = []

        for d in data:
            if Util.check_rule(d['Sequence'], rule):
                positive_set.append(d)
            else:
                negative_set.append(d)
        return positive_set, negative_set

    @staticmethod
    def entrophy(data):
        if not data:
            return 0
        counter = 0
        for d in data:
            if d['Cut'] == 1:
                counter += 1
        f_1 = counter / len(data)
        f_0 = 1 - f_1
        if f_0 == 0 or f_1 == 0:
            return 0

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
    def best_rule(rules, data):
        best_infgain = -math.inf
        best_rule = []
        for r in rules:
            ig = DecisionTree.inf_gain(data, r)
            if ig == 0:
                rules.remove(r)

            if ig > best_infgain:
                best_infgain = ig
                best_rule = r
        if best_infgain == 0:
            return False
        rules.remove(best_rule)
        return best_rule

    @staticmethod
    def set_to_label(data):
        counter = 0
        for d in data:
            if d['Cut'] == 1:
                counter += 1
        f_1 = counter / len(data)
        f_0 = 1 - f_1
        label = f_1 if f_1 > f_0 else f_0

        return label

    @staticmethod
    def id3(node, rules, data):
        assert data

        DecisionTree.i += 1
        print(DecisionTree.i)

        if DecisionTree.entrophy(data) == 0:
            node.leaf = True
            node.label = data[0]['Cut']
            return

        if len(rules) == 0:
            label = DecisionTree.set_to_label(data)
            node.leaf = True
            node.label = label
            return

        best_rule = DecisionTree.best_rule(rules, data)
        if not best_rule:
            label = DecisionTree.set_to_label(data)
            node.leaf = True
            node.label = label
            return

        node.rule = best_rule

        positive_child, negative_child = Node(parent=node), Node(parent=node)
        node.positive_child = positive_child
        node.negative_child = negative_child

        positive_set, negative_set = DecisionTree.divide_set(data, rule=node.rule)

        DecisionTree.id3(node=node.positive_child, rules=copy.deepcopy(rules), data=positive_set)
        DecisionTree.id3(node=node.negative_child, rules=copy.deepcopy(rules), data=negative_set)

    def setup(self):
        DecisionTree.id3(node=self.root, rules=self.R, data=self.S)









