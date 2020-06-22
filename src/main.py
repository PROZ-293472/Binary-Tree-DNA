from src.regex_gen import RegexGenerator
from src.algorithm import DecisionTree
import pandas as pd

df = pd.read_csv('C:\\Users\\Lenovo\\Desktop\\Studia\\UM\\PROJEKT\\DecisionTreeDNA\\data\\spliceATrainKIS.csv')
strlen = len(df.loc[0, 'Sequence'])
rg = RegexGenerator(max_pos=strlen, curly_bracket_restrictions=4, max_bracket_num=3)
R = []
for i in range(60):
    regex = rg.gen_regex()
    while not regex:
        regex = rg.gen_regex()
    R.append(regex)

model = DecisionTree(R=R, dataframe=df)




