import copy
from src.id3_tree import Id3DecisionTree
from src.utils import Util


class C45DecisionTree:
    def __init__(self, R, dataframe, omega):
        self.tree = Id3DecisionTree(R=R, dataframe=dataframe, omega=omega)
        self.c4_5()

    def trim(self, node):
        if not node.parent:
            return
        if not node.leaf:
            replica = copy.deepcopy(self.tree)
            label = Util.set_to_label(node.set)
            node.leaf = True
            node.label = label
            self.tree.leaves.append(node)

            e0 = Id3DecisionTree.test_error_estimate(replica)
            e1 = Id3DecisionTree.test_error_estimate(self.tree)

            if e0 < e1:
                self.tree = replica
            del replica

        self.trim(node.parent)

    def c4_5(self):
        for leaf in self.tree.leaves:
            self.tree = self.trim(leaf)

    def show_accuracies(self):
        one_counter = 0
        for n in self.tree.leaves:
            if n.label == 1:
                one_counter += 1
        zero_counter = len(self.tree.leaves) - one_counter
        print(f'NUM OF "0" LEAVES: {zero_counter}')
        print(f'NUM OF "1" LEAVES: {one_counter}')

        acc = self.tree.train_accuracy
        print(f'TOTAL ACCURACY: {acc}')
        acc1 = Id3DecisionTree.evaluate_label_accuracy(self.tree, self.tree.S, label=1)
        print(f'ACCURACY OF ONES: {acc1}')
        acc0 = Id3DecisionTree.evaluate_label_accuracy(self.tree, self.tree.S, label=0)
        print(f'ACCURACY OF ZEROS: {acc0}')













