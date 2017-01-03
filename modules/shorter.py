# -*- coding: utf-8 -*-
import re
import copy
import codecs
import os

class KE():

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
        additional = hangul.findall(word)
        additional_len = 0
        for item in additional:
            additional_len += len(item)
        word = hangul.sub('', word).decode('utf-8')
        result = 0
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

            result += len(enH_char)
            result += len(enB_char)
            result += len(enF_char)

        return result + additional_len

class Preprocess():

    def __init__(self):
        self.ke = KE()

    def shorter(self, set_path, filename):
  
        fr = open(set_path + filename, 'r')
        fw = open(set_path + 'short/short_' + filename, 'w')
        lines = fr.readlines()
        for line in lines:
            splited = line[:len(line)-1].split(' ')
            splited_len = len(splited) - 1
            for item in splited:
                splited_len += self.ke.change_complete_korean(item)
            if splited_len > 20 and splited_len < 50:
                fw.write(line)
        fw.close()
        fr.close()

    def generator(self, set_path):
        if not os.path.exists(set_path + "short"):
            os.makedirs(set_path + "short")
        self.shorter(set_path, 'pure.txt')
        self.shorter(set_path, 'pure_number.txt')
        self.shorter(set_path, 'pure_number_punctuation.txt')
        self.shorter(set_path, 'pure_punctuation.txt')
