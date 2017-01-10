# -*- coding: utf-8 -*-
import re
import copy
import codecs
from konlpy.tag import Hannanum

# option 0 : default analyze
# option 1 : bigram analyze
# option 2 : all analye


class KE(object):

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

    def change_complete_korean(self, word, option):

        hangul = re.compile('[^가-힣]+')
        if option == 3:
            word = word.encode('utf-8')
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

            if option == 2:
                parsed_word = []
                parsed_word.append(enH_char)
                parsed_word.append(enB_char)
                if enF_code != 0:
                    parsed_word.append(enF_char)
                result.append(parsed_word)
            elif option == 1:
                result.append(enH_char)
                result.append(enB_char)
                if enF_code != 0:
                    result.append(enF_char)
	    elif option == 3:
                parsed_word = ""
                parsed_word += enH_char
                parsed_word += enB_char
                if enF_code != 0:
                    parsed_word += enF_char
                result.append(parsed_word)

        return result

class Unigram(object):

    def __init__(self):
        self.compare_set = {}
	self.ke = KE()
	self.set = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

    def analyze(self, analyze_path, output_path, filename):

        input_file = filename + '.txt'

        output_file = 'analyze_' + filename + '.txt'

        fr = open(analyze_path + input_file, 'r')

        lines = fr.readlines()

        result = []
        for line in lines:
            words = line.split(' ')
            for word in words:
                for item in self.ke.change_complete_korean(word, 1):
                    result.append(item)

        if filename in self.set:
            self.compare_set = copy.deepcopy(result)

        final = {}
        for item in result:
            if item in final.keys():
                updated = final[item]
                del final[item]
                final[item] = updated + 1
            else:
                final[item] = 1

        if not (filename in self.set):
            for key in self.compare_set:
                if not(key in final.keys()):
                    final[key] = 0

        fw = open(output_path + output_file, 'w')
        for key in final.keys():
            fw.write(str(key) + ' : ' + str(final[key]) + '\n')
        fw.close()
        fr.close()


class Bigram(object):

    def __init__(self):
        self.compare_set = {}
	self.ke = KE()
	self.set = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

    def analyze(self, analyze_path, output_path, filename):

        input_file = filename + '.txt'

        output_file = 'bigram_analyze_' + filename + '.txt'

        fr = open(analyze_path + input_file, 'r')

        lines = fr.readlines()

        bigram = []
        for line in lines:
            words = line.split(' ')
            for word in words:
                changed = self.ke.change_complete_korean(word, 2)
                for i in range(len(changed)):
                    items = changed[i]
                    for j in range(len(items)):
                        if len(items) - 1 == j:
                            continue
                        else:
                            bigram.append(items[j] + '-' + items[j+1])
                    if len(changed) - 1 == i:
                        continue
                    else:
                        bigram.append(items[len(items)-1] + '-' + changed[i+1][0])

        if filename in self.set:
            self.compare_set = copy.deepcopy(bigram)

        final = {}
        for item in bigram:
            if item in final.keys():
                updated = final[item]
                del final[item]
                final[item] = updated + 1
            else:
                final[item] = 1

        if not (filename in self.set):
            for key in self.compare_set:
                if not(key in final.keys()):
                    final[key] = 0

        fw = open(output_path + output_file, 'w')
        for key in final.keys():
            fw.write(str(key) + ' : ' + str(final[key]) + '\n')
        fw.close()
        fr.close()

class Word(object):

    def __init__(self):
        self.compare_word_set = {}
	self.hannanum = Hannanum()
	self.ke = KE()
	self.set = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

    def analyze(self, analyze_path, output_path, filename):

        input_file = filename + '.txt'

        output_file = 'word_analyze_' + filename + '.txt'

        fr = open(analyze_path + input_file, 'r')

        lines = fr.readlines()

        word_list = []
        for line in lines:
	    if len(line.strip()) == 0:
                continue
            #words = self.hannanum.morphs(line.decode('utf-8'))
            words = line.decode('utf-8').split(' ')
            for word in words:
                changed = self.ke.change_complete_korean(word, 3)
	        word_list.append("".join(changed))

        if filename in self.set:
            self.compare_word_set = copy.deepcopy(word_list)

        final = {}
        for item in word_list:
            if item in final.keys():
                updated = final[item]
                del final[item]
                final[item] = updated + 1
            else:
                final[item] = 1

        if not (filename in self.set):
            for key in self.compare_word_set:
                if not(key in final.keys()):
                    final[key] = 0

        fw = open(output_path + output_file, 'w')
        for key in final.keys():
            fw.write(str(key) + ' : ' + str(final[key]) + '\n')
        fw.close()
        fr.close()
