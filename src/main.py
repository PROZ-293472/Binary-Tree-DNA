from src.regex_gen import RegexGenerator
from src.algorithm import DecisionTree
import pandas as pd

df = pd.read_csv('C:\\Users\\Lenovo\\Desktop\\Studia\\UM\\PROJEKT\\DecisionTreeDNA\\data\\spliceATrainKIS.csv')
strlen = len(df.loc[0, 'Sequence'])
rg = RegexGenerator(max_pos=strlen, curly_bracket_restrictions=4, max_bracket_num=3)
R = []
for i in range(400):
    regex = rg.gen_regex()
    while not regex:
        regex = rg.gen_regex()
    R.append(regex)
print(R)
model = DecisionTree(R=R, dataframe=df, omega=0.5)


one_counter = 0
for n in model.leaves:
    if n.label == 1:
        one_counter += 1
zero_counter = len(model.leaves) - one_counter
print(f'NUM OF "0" LEAVES: {zero_counter}')
print(f'NUM OF "1" LEAVES: {one_counter}')

acc = model.evaluate_accuracy(model.S)
print(f'TOTAL ACCURACY: {acc}')
acc1 = model.evaluate_label_accuracy(model.S, label=1)
print(f'ACCURACY OF ONES: {acc1}')
acc0 = model.evaluate_label_accuracy(model.S, label=0)
print(f'ACCURACY OF ZEROS: {acc0}')



