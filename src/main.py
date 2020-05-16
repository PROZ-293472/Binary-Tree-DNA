from src.regex_gen import RegexGenerator

rg = RegexGenerator(max_pos=30, curly_bracket_restrictions=4, max_bracket_num=3)
brackets = rg.gen_brackets(num=10, max_len=20)
print(brackets)
print('----------------')
rg.gen_regex()

