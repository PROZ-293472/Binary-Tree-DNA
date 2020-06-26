__author__ = "Michal Szpunar"


import copy
from src.utils import Util


class Node:
    debug_name = 0

    def __init__(self, parent, rule=None, leaf=False, label=None, set=None):
        self.parent = parent  # node
        self.positive_child = []
        self.negative_child = []
        self.rule = rule  # tuple
        self.leaf = leaf
        self.label = label
        self.set = set
        self.debug_name = Node.debug_name
        Node.debug_name += 1

    def to_leaf(self):
        label = Util.set_to_label(self.set)
        return Node(parent=self.parent, leaf=True, label=label, set=self.set)


class Id3DecisionTree:

    def __init__(self, R, dataframe, omega):
        self.root = Node(parent=None, rule=None)
        self.nodes = [self.root]
        self.leaves = []

        self.S = dataframe.to_dict('records')  # list array of dicts
        self.R = R  # array of tuples

        self.omega = omega

        self.setup()



    def id3(self, node, rules, data):
        assert data

        #print(f'NODE: {node.debug_name}')

        if Util.entrophy(data) == 0:
            node.leaf = True
            node.label = data[0]['Cut']
            self.leaves.append(node)
            return

        if len(rules) == 0:
            label = Util.set_to_label(data)
            node.leaf = True
            node.label = label
            self.leaves.append(node)
            return

        best_rule = Util.best_rule(rules, data)
        if not best_rule:
            label = Util.set_to_label(data)
            node.leaf = True
            node.label = label
            self.leaves.append(node)
            return

        node.rule = best_rule

        positive_child, negative_child = Node(parent=node), Node(parent=node)
        node.positive_child = positive_child
        node.negative_child = negative_child

        self.nodes.append(node.positive_child)
        self.nodes.append(node.negative_child)

        node.positive_child.set, node.negative_child.set = Util.divide_set(data, rule=node.rule)

        self.id3(node=node.positive_child, rules=copy.deepcopy(rules), data=node.positive_child.set)
        self.id3(node=node.negative_child, rules=copy.deepcopy(rules), data=node.negative_child.set)

    def setup(self):
        self.id3(node=self.root, rules=self.R, data=self.S)
        #print('='*10 + ' ID3 DONE ' + '='*10)

    ### STUFF AFTER SETUP ###
    @staticmethod
    def search_leaves(node, found_leaves):
        if node.leaf:
            found_leaves.append(node)
            return

        Id3DecisionTree.search_leaves(node.positive_child, found_leaves)
        Id3DecisionTree.search_leaves(node.negative_child, found_leaves)

    @staticmethod
    def search_children(node, children):
        if node.leaf:
            return
        children.append(node.positive_child)
        children.append(node.negative_child)

        Id3DecisionTree.search_children(node.positive_child, children)
        Id3DecisionTree.search_children(node.negative_child, children)

    @staticmethod
    def feed_forward(record, node):
        if node.leaf:
            return node.label

        seq = record['Sequence']
        if Util.check_rule(seq, node.rule):
            return Id3DecisionTree.feed_forward(record, node.positive_child)
        else:
            return Id3DecisionTree.feed_forward(record, node.negative_child)

    @staticmethod
    def get_prediction(root, record):
        return Id3DecisionTree.feed_forward(record, root)

    @staticmethod
    def evaluate_accuracy(decision_tree, t_set):
        score = 0
        for t in t_set:
            pred = Id3DecisionTree.get_prediction(decision_tree.root, t)
            if pred == t['Cut']:
                score += 1
        return score / len(t_set)

    @staticmethod
    def evaluate_label_accuracy(decision_tree, t_set, label):
        num_of_examples = 0
        score = 0
        for t in t_set:
            if t['Cut'] == label:
                num_of_examples += 1
                pred = Id3DecisionTree.get_prediction(decision_tree.root, t)
                if pred == t['Cut']:
                    score += 1
        return score / num_of_examples


    @staticmethod
    def evaluate_accuracy2(node):
        score = 0
        for t in node.set:
            pred = Id3DecisionTree.get_prediction(node, t)
            if pred == t['Cut']:
                score += 1
        return score / len(node.set)

    def subtree_test_error_estimate(self, node):
        e = (1 - Id3DecisionTree.evaluate_accuracy2(node)) * len(node.set)
        leaves = []
        Id3DecisionTree.search_leaves(node, leaves)
        omg = self.omega * len(leaves)
        nt = len(node.set)
        return (e + omg) / nt



