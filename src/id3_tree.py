import copy

from src.utils import Util


class Node:
    debug_name = 0
    def __init__(self, parent, rule=None, leaf=False, label=None):
        self.parent = parent  # node
        self.positive_child = []
        self.negative_child = []
        self.rule = rule  # tuple
        self.leaf = leaf
        self.label = label
        self.set = []
        self.debug_name = Node.debug_name
        Node.debug_name += 1


class Id3DecisionTree:
    i = 0

    def __init__(self, R, dataframe, omega):
        self.root = Node(parent=None, rule=None)
        self.nodes = [self.root]
        self.leaves = []

        self.S = dataframe.to_dict('records')  # list array of dicts
        self.R = R  # array of tuples
        self.train_accuracy = None

        self.omega = omega

        self.setup()



    def id3(self, node, rules, data):
        assert data

        Id3DecisionTree.i += 1
        print(Id3DecisionTree.i)

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
        self.train_accuracy = Id3DecisionTree.evaluate_accuracy(self, self.S)

    ### STUFF AFTER SETUP ###

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
    def test_error_estimate(decision_tree):
        e = (1 - decision_tree.train_accuracy) * len(decision_tree.S)
        omg = decision_tree.omega * len(decision_tree.leaves)
        nt = len(decision_tree.S)
        return (e + omg) / nt
