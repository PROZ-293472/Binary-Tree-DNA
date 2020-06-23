from src.c4_5_tree import C45DecisionTree
from src.regex_gen import RegexGenerator
from src.id3_tree import Id3DecisionTree
import pandas as pd
import numpy as np

df = pd.read_csv('C:\\Users\\Lenovo\\Desktop\\Studia\\UM\\PROJEKT\\DecisionTreeDNA\\data\\spliceDTrainKIS.csv')

# GENERATING A SET OF RULES
rule_num = 300
strlen = len(df.loc[0, 'Sequence'])
rg = RegexGenerator(max_pos=strlen, curly_bracket_restrictions=4, max_bracket_num=3)
R = []
for i in range(rule_num):
    rule = rg.gen_regex()
    while not rule:
        rule = rg.gen_regex()
    R.append(rule)
print(R)

# SPLITTING DATASET INTO K SETS
k = 10
df = df.sample(frac=1)
df_array = np.array_split(df, k)

models = []
for d in df_array:
    diff_df = pd.merge(df, d, how='outer', indicator='Exist')
    diff_df = diff_df.loc[diff_df['Exist'] != 'both']

    model = C45DecisionTree(R=R, dataframe=diff_df, omega=0.001)
    model.evaluate_accuracies(test_data=d)

    model.show_leaves_num()
    model.show_train_accuracies()
    model.show_test_accuracies()

    models.append(model)







