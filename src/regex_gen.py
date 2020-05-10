import math
import random


class RegexGenerator:

    _letters = ['A', 'C', 'G', 'T']

    # Here are defined some rules, that will assure correct sytnax
    # ^ - at the begining
    # $ - at the end
    # + - not first and not last
    # | - not first and not last
    # {} - only int between brackets. range: todo specify
    # [] - can have '-' indicating a range or nothing indicating set

    # Here is some notation used later while creating a list of symbols
    # f - first
    # l - last
    # nf - not first
    # nl - not last
    # nfnl - not first not last
    # w - whatever

    @staticmethod
    def gen_dict_list(symbols, position):
        return [{'string': s, 'position': position} for s in symbols]

    def __init__(self, max_pos, max_bracket_num, curly_bracket_restrictions):
        self.max_pos = max_pos
        self.max_bracket_num = max_bracket_num
        self.curly_bracket_restrictions = curly_bracket_restrictions

        f_list = RegexGenerator.gen_dict_list(symbols=['^'], position='f')
        l_list = RegexGenerator.gen_dict_list(symbols=['$'], position='l')
        nf_list = RegexGenerator.gen_dict_list(symbols=['+', '*'], position='nf')
        # nl_list = RegexGenerator.gen_dict_list(symbols=[], position='nl')
        nfnl_list = RegexGenerator.gen_dict_list(symbols=['|'], position='nfnl')
        w_list = RegexGenerator.gen_dict_list(symbols=RegexGenerator._letters.append('.'), position='w')

        self.mult_symbols = w_list + nfnl_list + nf_list
        self.unique_symbols = f_list + l_list

    def curly_brackets(self, amount=None):
        if amount is None:
            amount = random.randint(1, self.curly_bracket_restrictions)
        return {'brackets': 'curly',
                'string': f'{{{amount}}}',
                'length': amount,
                'position': 'nf'}

    def square_brackets(self):
        # range useless (?) bc it's quite a narrow set so there's no need to implement it
        length = random.randint(2, len(RegexGenerator._letters))
        letters = random.sample(RegexGenerator._letters, k=length)
        return {'brackets': 'square',
                'string': f'[{"".join(x for x in letters)}]',
                'length': 1,
                'position': 'w'}

    def gen_brackets(self, num, max_len):
        total_len = 0
        brackets = []
        for i in range(num):
            if total_len == max_len:
                break

            curly = bool(random.getrandbits(1))
            if curly:
                if max_len - total_len > self.curly_bracket_restrictions:
                    temp = self.curly_brackets()
                else:
                    temp = self.curly_brackets(amount=(max_len-total_len))
                total_len += temp['length']
                brackets.append(temp)
            else:
                brackets.append(self.square_brackets())
                total_len += 1
        return brackets, total_len

    def gen_regex(self):
        regex_len = random.randint(1, self.max_pos)

        # generating brackets
        b_num = random.randint(0, self.max_bracket_num)
        brackets, b_len = self.gen_brackets(num=b_num, max_len=regex_len)

        # pick characters at random
        characters = random.choices(self.mult_symbols, k=(regex_len - b_len))









