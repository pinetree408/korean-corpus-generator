# -*- coding: utf-8 -*-
"""Make Short corpus from 4 parent pharse

This module generate short corpus from 4 parent pharse

"""
import re
import os

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

    def change_complete_korean(self, word):
        """chnage korean word to korean letter list
        Args:
            word (str): target word
        Return:
            len (int): length of target word's letter
        """
        additional = self.hangul.findall(word)
        additional_len = 0
        for item in additional:
            additional_len += len(item)
        words = self.hangul.sub('', word).decode('utf-8')
        result = 0
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

            result += self.sum_length(en_h_char, en_b_char, en_f_char)

        return result + additional_len

    @staticmethod
    def sum_length(en_h, en_b, en_f):
        """sum enh, enb, enf's length
        Args:
            en_h (str): enh's char
            en_b (str): enb's char
            en_f (str): enf's char
        """
        return len(en_h) + len(en_b) + len(en_f)

class Preprocess(object):
    """generate short corpus from 4 parent pharses
    Attributes:
        ke (object): korean & english object
    """
    def __init__(self):
        """Initialize preprocess class
        this method initialize all attributes of this class
        """
        self.ke_object = KE()

    def shorter(self, set_path, filename):
        """generate short pharse set from target file
        Args:
            set_path (str): target file's path
            filename (str): target file name
        """
        with open(set_path + filename, 'r') as file_read:
            with open(set_path + 'short/short_' + filename, 'w') as file_write:
                lines = file_read.readlines()
                for line in lines:
                    splited = line[:len(line)-1].split(' ')
                    splited_len = len(splited) - 1
                    for item in splited:
                        splited_len += self.ke_object.change_complete_korean(item)
                    if splited_len > 20 and splited_len < 50:
                        file_write.write(line)

    def generator(self, set_path):
        """generate short pharse set from each parent set
        Args:
            set_path (str): target file's path
        """
        if not os.path.exists(set_path + "short"):
            os.makedirs(set_path + "short")
        self.shorter(set_path, 'pure.txt')
        self.shorter(set_path, 'pure_number.txt')
        self.shorter(set_path, 'pure_number_punctuation.txt')
        self.shorter(set_path, 'pure_punctuation.txt')
