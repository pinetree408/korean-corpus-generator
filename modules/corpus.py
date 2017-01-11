# -*- coding: utf-8 -*-
"""Corpus

This module generate complex corpus and preprocess 4 parent pharse set
- Pure : just consists of korean
- Pure-number : Pure + (korean + number) set
- Pure-punctuation : Pure + (korean + punctuation) set
- Pure-number-punctuation : Pure + (korean + number)
                                 + (korean + punctuation)
                                 + (korean + number + punctuation)

"""

import re
import os


class Complex(object):
    """Generate complex corpus from cdtree file
    Attributes:
        complex_output (str): file name of generated complex corpus
    """

    complex_output = "complex.txt"

    @staticmethod
    def corpus_generator(path):
        """generate plain text from cdtree file
        Args:
            path (str): target file's name and path
        Returns:
            result (list): plain text corpus
        """
        with open(path, 'r') as file_read:
            lines = file_read.readlines()

            result = []
            for line in lines:
                if "] ;" in line:
                    final = line.split(';')[1].split('\n')[0].strip()
                    result.append(final)

        return result

    @staticmethod
    def search():
        """generate path list
        Returns:
            result (list): target path list
        """
        dirname = '../'
        filenames = os.listdir(dirname)

        result = []
        for filename in filenames:
            if '.cdtree' in filename:
                txtfile = dirname+filename
                result.append(txtfile)
        return result


    def generate(self, set_path):
        """generate complex corpus
        Args:
            set_path (str): output dir path
        """
        path_list = self.search()

        with open(set_path + self.complex_output, 'w') as file_write:

            all_reg = re.compile(r"[ 가-힣0-9\,\?\!\'\"\.\<\>\[\]]+")

            for path in path_list:
                corpus = self.corpus_generator(path)
                for item in corpus:
                    item = item.decode('mbcs').encode('utf-8')
                    sliced = item[:len(item)-1]
                    subed = all_reg.sub('', sliced)
                    if len(subed) != 0:
                        continue
                    file_write.write((item + '\n'))

class Preprocess(object):
    """Generate 4 parent pharse set from complex
    Attributes:
        complex_output (str): file name of generated complex corpus
    """

    complex_output = 'complex.txt'

    @staticmethod
    def check_list(list1, list2):
        """check whether list1's item is in list2's item or not
        Args:
            list1 (list): first target list
            list2 (list): second target list
        Return:
            boolean: if list1's item is in list2's item,
                         it return True, if not it return False
        """
        for item1 in list1:
            for item2 in list2:
                if item1 in item2:
                    return True

        return False

    @staticmethod
    def make_output(filename, input_list):
        """make input_list to txt file with filename
        Args:
            filename (str): output file's name
            input_list (list): target list
        """
        with open(filename, 'w') as file_write:
            for item in input_list:
                file_write.write(item)

    def generator(self, set_path):
        """generate 4 parent pharse set from complex
        Args:
            set_path (str): output dir path
        """
        with open(set_path + self.complex_output, 'r') as file_read:
            complex_list = file_read.readlines()

            pure = []
            pure_punctuation = []
            pure_number = []
            pure_number_punctuation = []

            pure_reg = re.compile(r"[^ 가-힣]+")
            number_list = [str(x) for x in range(10)]
            punctuation_list = [',', '?', '!', "'", '"', '.', '<', '>', '[', ']']
            for complex_item in complex_list:
                reg_result = pure_reg.findall(complex_item[:len(complex)-2])
                if len(reg_result) == 0:
                    pure.append(complex_item)
                    pure_number.append(complex_item)
                    pure_punctuation.append(complex_item)
                    pure_number_punctuation.append(complex_item)
                else:
                    if (self.check_list(number_list, reg_result) and
                            self.check_list(punctuation_list, reg_result)):
                        pure_number_punctuation.append(complex_item)
                    else:
                        if self.check_list(number_list, reg_result):
                            pure_number.append(complex_item)
                            pure_number_punctuation.append(complex_item)
                        else:
                            pure_punctuation.append(complex_item)
                            pure_number_punctuation.append(complex_item)

            self.make_output(set_path + "pure.txt", pure)
            self.make_output(set_path + "pure_number.txt", pure_number)
            self.make_output(set_path + "pure_number_punctuation.txt", pure_number_punctuation)
            self.make_output(set_path + "pure_punctuation.txt", pure_punctuation)
