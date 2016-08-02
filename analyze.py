# -*- coding: utf-8 -*-
import re
import copy
import codecs


class Generator:

    enH = "rRseEfaqQtTdwWczxvg"
    enB_list = [
        'k', 'o', 'i', 'O', 'j',
        'p', 'u', 'P', 'h', 'hk',
        'ho', 'hl', 'y', 'n', 'nj',
        'np', 'nl', 'b', 'm', 'ml',
        'l'
    ]
    enF_list = [
        '', 'r', 'R', 'rt', 's',
        'sw', 'sg', 'e', 'f', 'fr',
        'fa', 'fq', 'ft', 'fx', 'fv',
        'fg', 'a', 'q', 'qt', 't',
        'T', 'd', 'w', 'c', 'z',
        'x', 'v', 'g'
    ]

    regH = "[rRseEfaqQtTdwWczxvg]"
    regB = "hk|ho|hl|nj|np|nl|ml|k|o|i|O|j|p|u|P|h|y|n|b|m|l"
    regF = "rt|sw|sg|fr|fa|fq|ft|fx|fv|fg|qt|r|R|s|e|f|a|q|t|T|d|w|c|z|x|v|g|"

    def __init__(self):
        enB_dict = {}
        for i in range(len(self.enB_list)):
            enB_dict[self.enB_list[i]] = i
        enF_dict = {}
        for i in range(len(self.enF_list)):
            enF_dict[self.enF_list[i]] = i
        self.enB = enB_dict
        self.enF = enF_dict
        regH_block = "("+self.regH+")"
        regB_block = "("+self.regB+")"
        regF_item_first = "("+self.regF+")"
        regF_item_second = "(?=("+self.regH+")("+self.regB+"))|("+self.regF+")"
        regF_block = "(" + regF_item_first + regF_item_second + ")"
        self.regex = regH_block + regB_block + regF_block

    def change_complete_korean(self, word):

        hangul = re.compile('[^가-힣]+')
        word = hangul.sub('', word).decode('utf-8')
        result = []
        for i in range(len(word)):
            char_code = ord(word[i])
            if char_code < 44032 or char_code > 55203:
                break
            char_code = char_code - 44032
            enH_code = char_code / 588
            enBF_code = char_code % 588
            enB_code = enBF_code / 28
            enF_code = enBF_code % 28
            enH_char = self.enH[enH_code]
            enB_char = self.enB_list[enB_code]
            enF_char = self.enF_list[enF_code]

            parsed_word = []
            parsed_word.append(enH_char)
            parsed_word.append(enB_char)
            if enF_code != 0:
                parsed_word.append(enF_char)
            result.append(parsed_word)

        return result

def analyze(filename):

    input_file = filename + '.txt'
    output_file = 'analyze_' + filename + '.txt'

    generator = Generator()

    fr = open(input_file, 'r')

    lines = fr.readlines()

    result = []
    for line in lines:
        words = line.split(' ')
        for word in words:
            for item in generator.change_complete_korean(word):
                result.append(item)

    final = {}
    for item in result:
        if item in final.keys():
            updated = final[item]
            del final[item]
            final[item] = updated + 1
        else:
            final[item] = 1

    fw = open(output_file, 'w')
    for key in final.keys():
        fw.write(str(key) + ' : ' + str(final[key]) + '\n')
    fw.close()
    fr.close()

compare_set = {}

def bigram_analyze(filename):
    global compare_set

    input_file = filename + '.txt'
    output_file = 'bigram_analyze_' + filename + '.txt'

    generator = Generator()

    fr = open(input_file, 'r')

    lines = fr.readlines()

    bigram = []
    for line in lines:
        words = line.split(' ')
        for word in words:
            changed = generator.change_complete_korean(word)
            for i in range(len(changed)):
                items = changed[i]
                for j in range(len(items)):
                    if len(items) - 1 == j:
                        continue
		    else:
                        bigram.append(items[j] + '-' + items[j+1])
                if len(changed) -1 == i:
                    continue
	        else:
                    bigram.append(items[len(items)-1] + '-' + changed[i+1][0])

    if filename == 'complex':
	compare_set = copy.deepcopy(bigram)

    final = {}
    for item in bigram:
        if item in final.keys():
            updated = final[item]
            del final[item]
            final[item] = updated + 1
        else:
            final[item] = 1

    if filename != 'complex':
        for key in compare_set:
            if not(key in final.keys()):
	        final[key] = 0

    fw = open(output_file, 'w')
    for key in final.keys():
        fw.write(str(key) + ' : ' + str(final[key]) + '\n')
    fw.close()
    fr.close()

'''
analyze('complex')
analyze('pure')
analyze('pure_number')
analyze('pure_number_punctuation')
analyze('pure_punctuation')
analyze('short_pure')
analyze('short_pure_number')
analyze('short_pure_number_punctuation')
analyze('short_pure_punctuation')
analyze('random_short_pure')
analyze('random_short_pure_number')
analyze('random_short_pure_punctuation')
analyze('random_short_pure_number_punctuation')
'''
bigram_analyze('complex')
bigram_analyze('pure')
bigram_analyze('pure_number')
bigram_analyze('pure_number_punctuation')
bigram_analyze('pure_punctuation')
bigram_analyze('short_pure')
bigram_analyze('short_pure_number')
bigram_analyze('short_pure_number_punctuation')
bigram_analyze('short_pure_punctuation')
bigram_analyze('random_short_pure')
bigram_analyze('random_short_pure_number')
bigram_analyze('random_short_pure_punctuation')
bigram_analyze('random_short_pure_number_punctuation')
