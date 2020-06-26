__author__ = "Michal Szpunar"


import copy
from src.c4_5_tree import C45DecisionTree
from src.regex_gen import RegexGenerator
import pandas as pd
import numpy as np
import pickle


DF = pd.read_csv('full_path_to_file')  # PATH TO CSV FILE


def main(k, omega, R=None, file_name=None):

    # SPLITTING DATASET INTO K SETS
    assert k > 1
    df = DF.sample(frac=1)
    df_array = np.array_split(df, k)

    # FOR EVERY SMALLER DATASET CREATE A MODEL
    models = []
    for d in df_array:
        diff_df = pd.merge(df, d, how='outer', indicator='Exist')
        diff_df = diff_df.loc[diff_df['Exist'] != 'both']

        if R:
            r = copy.deepcopy(R)
        else:
            r = None
        model = C45DecisionTree(R=r, path=file_name, dataframe=diff_df, omega=omega)
        model.evaluate_accuracies(test_data=d)

        model.show_leaves_num()
        model.show_train_accuracies()
        model.show_test_accuracies()

        models.append(model)

    overall_accuracies = [(m.test_accuracies[1] + m.test_accuracies[2])/2 for m in models]
    max_acc_index = overall_accuracies.index(max(overall_accuracies))

    print('='*30)
    best_model = models[max_acc_index]
    best_model.show_train_accuracies()
    best_model.show_test_accuracies()

    # SAVE THE BEST MODEL AS PICKLE FILE
    pickle.dump(best_model,  open(f'r={len(R)}_k={k}_o={omega}.p', "wb"))


if __name__ == '__main__':
    rule_nums = [500]
    ks = [2]
    omegas = [0.1, 0.5, 1, 2, 5]
    #omegas = [0.001]
    for rn in rule_nums:

        strlen = len(DF.loc[0, 'Sequence'])
        rg = RegexGenerator(max_pos=strlen, curly_bracket_restrictions=4, max_bracket_num=3)

        # R = []
        # for i in range(rn):
        #     rule = rg.gen_regex()
        #     while not rule:
        #         rule = rg.gen_regex()
        #     R.append(rule)

        rg.gen_file(rn, file_name='temp.csv')

        for kn in ks:
            for on in omegas:
                print(f'r={rn}, k={kn}, omega={on}')
                main(file_name='temp.csv', k=kn, omega=on)

