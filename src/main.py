from src.regex_gen import RegexGenerator

rg = RegexGenerator(max_pos=10, curly_bracket_restrictions=4)
brackets = rg.gen_brackets(5)
print(brackets)
