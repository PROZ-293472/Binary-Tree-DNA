import math
import re


class Util:

    @staticmethod
    def check_rule(record, rule):
        index, regex = rule
        r = record[index:]

        match = re.search(pattern=regex, string=r)
        return match

    @staticmethod
    def set_to_label(data):
        counter = 0
        for d in data:
            if d['Cut'] == 1:
                counter += 1
        f_1 = counter / len(data)
        f_0 = 1 - f_1
        label = 1 if f_1 > f_0 else 0

        return label

    @staticmethod
    def divide_set(data, rule):
        positive_set = []
        negative_set = []

        for d in data:
            if Util.check_rule(d['Sequence'], rule):
                positive_set.append(d)
            else:
                negative_set.append(d)
        return positive_set, negative_set

    @staticmethod
    def entrophy(data):
        if not data:
            return 0
        counter = 0
        for d in data:
            if d['Cut'] == 1:
                counter += 1
        f_1 = counter / len(data)
        f_0 = 1 - f_1
        if f_0 == 0 or f_1 == 0:
            return 0

        entrophy = -1 * (f_1 * math.log(f_1) + f_0 * math.log(f_0))
        return entrophy


    @staticmethod
    def inf_gain(data, rule):
        i = Util.entrophy(data)

        sets = Util.divide_set(data, rule=rule)
        inf = 0.0
        for s in sets:
            inf += len(s) / len(data) * Util.entrophy(s)

        infgain = i - inf
        return infgain

    @staticmethod
    def best_rule(rules, data):
        best_infgain = -math.inf
        best_rule = []
        i = 0
        print('Searching for best rule...')
        for r in rules:
            print(f'Rule {i} of {len(rules)}')
            i += 1
            ig = Util.inf_gain(data, r)
            if ig == 0:
                rules.remove(r)

            if ig > best_infgain:
                best_infgain = ig
                best_rule = r
        if best_infgain == 0:
            return False
        rules.remove(best_rule)
        return best_rule