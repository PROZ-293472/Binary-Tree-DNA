import copy
import random


class RegexGenerator:

    _letters = ['A', 'C', 'G', 'T']
    _forbidden = [('++', '+'), ('**', '*'), ('+*', '+'), ('*+', '*'),
                  ('*{', '{'), ('}*', '}'), ('+{', '{'), ('}+', '}'),
                  ('^*', '^'), ('^+', '^')]

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
    def gen_dict_list(symbols, position, presort_pos):
        return [{'string': s, 'position': position, 'presort_pos': presort_pos} for s in symbols]

    @staticmethod
    def list_to_string(dict_list):
        s = ''
        for d in dict_list:
            s += d['string']
        return s

    def __init__(self, max_pos, max_bracket_num, curly_bracket_restrictions):
        self.max_pos = max_pos
        self.max_bracket_num = max_bracket_num
        self.curly_bracket_restrictions = curly_bracket_restrictions

        f_list = RegexGenerator.gen_dict_list(symbols=['^'], position='f', presort_pos=0)
        l_list = RegexGenerator.gen_dict_list(symbols=['$'], position='l', presort_pos=0)
        nf_list = RegexGenerator.gen_dict_list(symbols=['+', '*'], position='nf', presort_pos=0)
        # nfnl_list = RegexGenerator.gen_dict_list(symbols=['|'], position='nfnl', presort_pos=1)
        w_list = RegexGenerator.gen_dict_list(symbols=RegexGenerator._letters + ['.'], position='w', presort_pos=0)

        self.mult_symbols = w_list + nf_list  # + nfnl_list
        self.unique_symbols = f_list + l_list

    def curly_brackets(self, amount=None):
        if amount is None:
            amount = random.randint(1, self.curly_bracket_restrictions)
        return {'brackets': 'curly',
                'string': f'{{{amount}}}',
                'length': amount,
                'position': 'nf',
                'presort_pos': 0}

    def square_brackets(self):
        # range useless (?) bc it's quite a narrow set so there's no need to implement it
        length = random.randint(2, len(RegexGenerator._letters))
        letters = random.sample(RegexGenerator._letters, k=length)
        return {'brackets': 'square',
                'string': f'[{"".join(x for x in letters)}]',
                'length': 1,
                'position': 'w',
                'presort_pos': 0}

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

    def sort(self, dict_list):
        # pre-sort (for nfnl records)
        dict_list = sorted(dict_list, key=lambda k: k['presort_pos'])
        max_index = 0
        min_index = self.max_pos

        new_list = copy.deepcopy(dict_list)

        # in this one giant abomination we replace str keys with numeric in order to sort a list
        for i in range(len(dict_list)):
            d = dict_list[i]
            if d['position'] == 'f':  # always first
                new_list[i]['position'] = 0
            elif d['position'] == 'l':  # always last
                new_list[i]['position'] = self.max_pos
            elif d['position'] == 'nf' or d['position'] == 'w':  # wherever between first and last
                new_list[i]['position'] = random.randint(1, self.max_pos-1)
            elif d['position'] == 'nfnl':  # must not be first or last
                new_list[i]['position'] = random.randint(min_index+1, max_index-1)

            if new_list[i]['position'] > max_index:
                max_index = new_list[i]['position']
            if new_list[i]['position'] < min_index:
                min_index = new_list[i]['position']

        return sorted(new_list, key=lambda k: k['position'])

    @staticmethod
    def repair(text):
        forbidden_sequences = [r[0] for r in RegexGenerator._forbidden]
        repairs = [r[1] for r in RegexGenerator._forbidden]
        while any(elem in text for elem in forbidden_sequences):
            for i in range(len(forbidden_sequences)):
                if forbidden_sequences[i] in text:
                    text = text.replace(forbidden_sequences[i], repairs[i])
        return text


    # main func
    def gen_regex(self):
        regex_len = random.randint(1, self.max_pos)

        # generating brackets
        b_num = random.randint(0, self.max_bracket_num)
        brackets, b_len = self.gen_brackets(num=b_num, max_len=regex_len-1)

        # pick characters at random
        characters = random.choices(self.mult_symbols, k=(regex_len - b_len))

        has_unique = bool(random.random() > 0.7)
        if has_unique:
            unique_num = 1
            temp = random.sample(self.unique_symbols, unique_num)
            characters += temp

        phrase_raw = brackets + characters
        phrase_raw = [copy.deepcopy(i) for i in phrase_raw]

        phrase_raw = self.sort(phrase_raw)
        phrase = RegexGenerator.list_to_string(phrase_raw)
        phrase = RegexGenerator.repair(phrase)
        if '}{' in phrase or '^{' in phrase:
            return False
        if phrase[0] == '+' or phrase[0] == '*' or phrase[0] == '{':
            return False

        index = random.randint(1, self.max_pos - (regex_len-1))

        print((index, phrase))
        return index, phrase







