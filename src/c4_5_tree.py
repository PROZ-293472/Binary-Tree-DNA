import copy
from src.id3_tree import Id3DecisionTree
from src.utils import Util


class C45DecisionTree:
    def __init__(self, R, dataframe, omega):
        self.tree = Id3DecisionTree(R=R, dataframe=dataframe, omega=omega)
        self.c4_5()
        self.train_accuracies = None
        self.test_accuracies = None

    def trim(self, node):
        # print(f'NODE: {node.debug_name}')
        if not node.parent:
            return
        if node not in self.tree.nodes:
            pass
        if not node.leaf:
            leaf = node.to_leaf()
            e0 = self.tree.subtree_test_error_estimate(node)
            e1 = self.tree.subtree_test_error_estimate(leaf)

            if e0 >= e1:
                print('CUT!')
                # search for children
                children = []
                Id3DecisionTree.search_children(node, children)
                for c in children:
                    self.tree.nodes.remove(c)
                    if c.leaf:
                        self.tree.leaves.remove(c)

                node.leaf = True
                node.label = leaf.label
                self.tree.leaves.append(node)
        self.trim(node.parent)

    def c4_5(self):
        i = 0
        for leaf in self.tree.leaves:
            print(f'c4.5 progress: LEAF {i} OUT OF {len(self.tree.leaves)}')
            self.trim(leaf)
            i += 1

    def evaluate(self, data):
        acc = self.tree.evaluate_accuracy(self.tree, data)
        acc1 = Id3DecisionTree.evaluate_label_accuracy(self.tree, data, label=1)
        acc0 = Id3DecisionTree.evaluate_label_accuracy(self.tree, data, label=0)

        return acc, acc1, acc0

    def evaluate_accuracies(self, test_data):
        self.train_accuracies = self.evaluate(self.tree.S)
        self.test_accuracies = self.evaluate(test_data.to_dict('records'))

    def show_test_accuracies(self):
        print(f'TOTAL TEST ACCURACY: {self.test_accuracies[0]}')
        print(f'TEST ACCURACY OF ONES: {self.test_accuracies[1]}')
        print(f'TEST ACCURACY OF ZEROS: {self.test_accuracies[2]}')

    def show_train_accuracies(self):
        print(f'TOTAL TRAIN ACCURACY: {self.train_accuracies[0]}')
        print(f'TRAIN ACCURACY OF ONES: {self.train_accuracies[1]}')
        print(f'TRAIN ACCURACY OF ZEROS: {self.train_accuracies[2]}')

    def show_leaves_num(self):
        one_counter = 0
        for n in self.tree.leaves:
            if n.label == 1:
                one_counter += 1
        zero_counter = len(self.tree.leaves) - one_counter
        print(f'NUM OF "0" LEAVES: {zero_counter}')
        print(f'NUM OF "1" LEAVES: {one_counter}')













