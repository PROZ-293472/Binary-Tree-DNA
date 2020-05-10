import math
import random


class RegexGenerator:
    _letters = ['A', 'C', 'G', 'T']
    _mult_symbols = ['.', '*', '+', '|']
    _unique_symbols = ['$', '^']

    # Here are defined some rules, that will assure correct sytnax
    # ^ - at the begining
    # $ - at the end
    # | - not first and not last
    # {} - only int between brackets. range: todo specify
    # [] - can have '-' indicating a range or nothing indicating set

    def __init__(self, max_pos, curly_bracket_restrictions):
        self.max_pos = max_pos
        self.curly_bracket_restrictions = curly_bracket_restrictions

    def curly_brackets(self):
        amount = random.randint(1, self.curly_bracket_restrictions)
        return {'brackets':'curly',
                'string':f'{{{amount}}}',
                'length': amount}

    def square_brackets(self):
        # range useless (?) bc it's quite a narrow set so there's no need to implement it
        length = random.randint(2, len(RegexGenerator._letters))
        letters = random.sample(RegexGenerator._letters, k=length)
        return {'brackets': 'square',
                'string': f'[{"".join(x for x in letters)}]',
                'length': 1}

    def gen_brackets(self, num):
        brackets = []
        for i in range(num):
            curly = bool(random.getrandbits(1))
            if curly:
                brackets.append(self.curly_brackets())
            else:
                brackets.append(self.square_brackets())
        return brackets


    def gen_regex(self):
        # regex len (assuming that brackets are not in entity)
        length = random.randint(1, self.max_pos-1)
        # num of brackets


        # pick characters at random
        elements = random.choices(RegexGenerator._letters + RegexGenerator._mult_symbols, k=length)

        # GENERATING BRACKETS
        # pick a random number of bracket pairs
        bracket_num = random.randint(1, math.floor(self))







