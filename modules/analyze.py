# -*- coding: utf-8 -*-
"""Analyzer of pharse sets

This module analyze pharse sets with 3 different point

- Unigram
- Bigram
- Word

"""

import re
import copy
from konlpy.tag import Hannanum

# option 0 : default analyze
# option 1 : bigram analyze
# option 2 : all analye


class KE(object):
    """korean & english regular expersion analyze class
    Attributes:
        en_h (str): Header of korean
        en_b (dict): Body of korean
        en_f (dict): Footer of korean
        reg_h (str): regular expression of korean Header
        reg_b (str): regular expression of korean Body
        reg_f (str): regular expression of korean footer
    """

    en_h = "rRseEfaqQtTdwWczxvg"
    en_b_list = [
        'k', 'o', 'i', 'O', 'j',
        'p', 'u', 'P', 'h', 'hk',
        'ho', 'hl', 'y', 'n', 'nj',
        'np', 'nl', 'b', 'm', 'ml',
        'l'
    ]
    en_f_list = [
        '', 'r', 'R', 'rt', 's',
        'sw', 'sg', 'e', 'f', 'fr',
        'fa', 'fq', 'ft', 'fx', 'fv',
        'fg', 'a', 'q', 'qt', 't',
        'T', 'd', 'w', 'c', 'z',
        'x', 'v', 'g'
    ]

    reg_h = "[rRseEfaqQtTdwWczxvg]"
    reg_b = "hk|ho|hl|nj|np|nl|ml|k|o|i|O|j|p|u|P|h|y|n|b|m|l"
    reg_f = "rt|sw|sg|fr|fa|fq|ft|fx|fv|fg|qt|r|R|s|e|f|a|q|t|T|d|w|c|z|x|v|g|"

    def __init__(self):
        """Initialize KE class
        this method initialize all attributes of this class
        """
        reg_h_block = "("+self.reg_h+")"
        reg_b_block = "("+self.reg_b+")"
        reg_f_item_first = "("+self.reg_f+")"
        reg_f_item_second = "(?=("+self.reg_h+")("+self.reg_b+"))|("+self.reg_f+")"
        reg_f_block = "(" + reg_f_item_first + reg_f_item_second + ")"
        self.regex = reg_h_block + reg_b_block + reg_f_block
        self.hangul = re.compile('[^가-힣]+')

    def change_complete_korean(self, word, option):
        """chnage korean word to korean letter list
        Args:
            word (str): target word
        Return:
            len (int): length of target word's letter
        """
        if option == 3:
            word = word.encode('utf-8')
        try:
            words = self.hangul.sub('', word).decode('utf-8')
        except UnicodeDecodeError as e:
            print word
            words = self.hangul.sub('', word)[:-2].decode('utf-8')

        result = []
        for word in words:
            char_code = ord(word)
            if char_code < 44032 or char_code > 55203:
                break
            char_code = char_code - 44032
            en_h_code = char_code / 588
            en_bf_code = char_code % 588
            en_b_code = en_bf_code / 28
            en_f_code = en_bf_code % 28
            en_h_char = self.en_h[en_h_code]
            en_b_char = self.en_b_list[en_b_code]
            en_f_char = self.en_f_list[en_f_code]

            if option == 2:
                result.append(self.bigram_unit(en_h_char, en_b_char, en_f_char))
            elif option == 1:
                result.append(en_h_char)
                result.append(en_b_char)
                if en_f_code != 0:
                    result.append(en_f_char)
            elif option == 3:
                result.append(self.word_unit(en_h_char, en_b_char, en_f_char))

        return result

    @staticmethod
    def bigram_unit(en_h_char, en_b_char, en_f_char):
        """generate unit word for bigram analyze
        Args:
            en_h_char (str): korean letter header
            en_b_char (str): korean letter body
            en_f_char (str): korean letter footer
        Return
            parsed_word (list): unit word
        """
        parsed_word = []
        parsed_word.append(en_h_char)
        parsed_word.append(en_b_char)
        if en_f_char != '':
            parsed_word.append(en_f_char)
        return parsed_word

    @staticmethod
    def word_unit(en_h_char, en_b_char, en_f_char):
        """generate unit word for word analyze
        Args:
            en_h_char (str): korean letter header
            en_b_char (str): korean letter body
            en_f_char (str): korean letter footer
        Return
            parsed_word (str): unit word
        """
        parsed_word = ""
        parsed_word += en_h_char
        parsed_word += en_b_char
        parsed_word += en_f_char
        return parsed_word

class Unigram(object):
    """Analyze pharse set by unigram
    Attributes:
        compare_set (dict): for correlation calculation
        ke (object): for korean analying
        set (list): 4 parent sets
    """

    def __init__(self):
        """Initialize unigram class
        this method initialize all attributes of this class
        """
        self.compare_set = []
        self.ke_object = KE()
        self.set = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

    def analyze(self, analyze_path, output_path, filename):
        """Analyze pharse set from target filename by unigram
        Args:
            analyze_path (str): target input file's path
            output_path (str): output file's path
            filename (str): target filename
        """
        input_file = filename + '.txt'
        output_file = 'analyze_' + filename + '.txt'

        with open(analyze_path + input_file, 'r') as file_read:
            result = []
            for line in file_read:
                for word in line.split(' '):
                    for item in self.ke_object.change_complete_korean(word, 1):
                        result.append(item)
                        if filename in self.set:
                            if not item in self.compare_set:
                                self.compare_set.append(item)
                             

            #self.copy_set_file(filename, result)
            final = self.update_dict(result)

            if not filename in self.set:
                for key in self.compare_set:
                    if not key in final.keys():
                        final[key] = 0

            with open(output_path + output_file, 'w') as file_write:
                for key, value in final.iteritems():
                    file_write.write(str(key) + ' : ' + str(value) + '\n')

    def copy_set_file(self, filename, result):
        """Copy parent set file from filename for compare set
        Args:
            filename (str): target filename
            result (list): target result
        """
        if filename in self.set:
            self.compare_set = copy.deepcopy(result)

    @staticmethod
    def update_dict(result):
        """generate dict for correlation calc as analyze result
        Args:
            result (list): target result
        Return:
            final (dict): calculated dict
        """
        final = {}
        for item in result:
            if item in final.keys():
                updated = final[item]
                del final[item]
                final[item] = updated + 1
            else:
                final[item] = 1
        return final

class Bigram(object):
    """Analyze pharse set by bigram
    Attributes:
        compare_set (dict): for correlation calculation
        ke (object): for korean analying
        set (list): 4 parent sets
    """

    def __init__(self):
        """Initialize unigram class
        this method initialize all attributes of this class
        """
        self.compare_set = []
        self.ke_object = KE()
        self.set = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

    def analyze(self, analyze_path, output_path, filename):
        """Analyze pharse set from target filename by bigram
        Args:
            analyze_path (str): target input file's path
            output_path (str): output file's path
            filename (str): target filename
        """
        with open(analyze_path + filename + '.txt', 'r') as file_read:
            bigram = []
            for line in file_read:
                for word in line.split(' '):
                    changed = self.ke_object.change_complete_korean(word, 2)
                    for i, items in enumerate(changed):
                        for j, item in enumerate(items):
                            if len(items) - 1 == j:
                                continue
                            else:
                                bigram_item = item + '-' + items[j+1]
                                bigram.append(bigram_item)
                                if filename in self.set:
                                    if not bigram_item in self.compare_set:
                                        self.compare_set.append(bigram_item)
                        if len(changed) - 1 == i:
                            continue
                        else:
                            bigram_item = items[len(items)-1] + '-' + changed[i+1][0]
                            bigram.append(bigram_item)
                            if filename in self.set:
                                if not bigram_item in self.compare_set:
                                    self.compare_set.append(bigram_item)

            #self.copy_set_file(filename, bigram)
            final = self.update_dict(bigram)

            if not filename in self.set:
                for key in self.compare_set:
                    if not key in final.keys():
                        final[key] = 0

            self.write_output(output_path, 'bigram_analyze_' + filename + '.txt', final)

    def copy_set_file(self, filename, result):
        """Copy parent set file from filename for compare set
        Args:
            filename (str): target filename
            result (list): target result
        """
        if filename in self.set:
            self.compare_set = copy.deepcopy(result)

    @staticmethod
    def update_dict(result):
        """generate dict for correlation calc as analyze result
        Args:
            result (list): target result
        Return:
            final (dict): calculated dict
        """
        final = {}
        for item in result:
            if item in final.keys():
                updated = final[item]
                del final[item]
                final[item] = updated + 1
            else:
                final[item] = 1
        return final

    @staticmethod
    def write_output(output_path, output_file, final):
        """write output file with updated frequency
        Args:
            output_path (str): output file's path
            output_file (str): output file's name
            final (dict): final frequency dict
        """
        with open(output_path + output_file, 'w') as file_write:
            for key, value in final.iteritems():
                file_write.write(str(key) + ' : ' + str(value) + '\n')

class Word(object):
    """Analyze pharse set by word
    Attributes:
        compare_set (dict): for correlation calculation
        hannanum (object): for morphere analyzing
        ke (object): for korean analying
        set (list): 4 parent sets
    """
    def __init__(self):
        """Initialize unigram class
        this method initialize all attributes of this class
        """
        self.compare_set = []
        self.hannanum = Hannanum()
        self.ke_object = KE()
        self.set = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

    def analyze(self, analyze_path, output_path, filename):
        """Analyze pharse set from target filename by word
        Args:
            analyze_path (str): target input file's path
            output_path (str): output file's path
            filename (str): target filename
        """
        input_file = filename + '.txt'
        output_file = 'word_analyze_' + filename + '.txt'

        with open(analyze_path + input_file, 'r') as file_read:
            word_list = []
            for line in file_read:
                if len(line.strip()) == 0:
                    continue
                #self.hannanum.morphs(line.decode('utf-8'))
                #for word in line.decode('utf-8').split(' '):
                try:
                    morphs_list = self.hannanum.morphs(line.decode('utf-8'))
                except UnicodeDecodeError as e:
                    morphs_list = self.hannanum.morphs(line.encode('utf-8'))

                for word in morphs_list:
                    changed = self.ke_object.change_complete_korean(word, 3)
                    word_item = "".join(changed)
                    word_list.append(word_item)
                    if filename in self.set:
                        if not word_item in self.compare_set:
                            self.compare_set.append(word_item)

            #self.copy_set_file(filename, word_list)
            final = self.update_dict(word_list)

            if not filename in self.set:
                for key in self.compare_set:
                    if not key in final.keys():
                        final[key] = 0

            with open(output_path + output_file, 'w') as file_write:
                for key, value in final.iteritems():
                    file_write.write(str(key) + ' : ' + str(value) + '\n')

    def copy_set_file(self, filename, result):
        """Copy parent set file from filename for compare set
        Args:
            filename (str): target filename
            result (list): target result
        """
        if filename in self.set:
            self.compare_set = copy.deepcopy(result)

    @staticmethod
    def update_dict(result):
        """generate dict for correlation calc as analyze result
        Args:
            result (list): target result
        Return:
            final (dict): calculated dict
        """
        final = {}
        for item in result:
            if item in final.keys():
                updated = final[item]
                del final[item]
                final[item] = updated + 1
            else:
                final[item] = 1
        return final
