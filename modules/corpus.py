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
from multiprocessing import Process, Queue
from konlpy.tag import Kkma

class Complex(object):
    """Generate complex corpus from cdtree file
    Attributes:
        complex_output (str): file name of generated complex corpus
    """

    complex_output = "/complex/complex"

    @staticmethod
    def corpus_generator(path):
        """generate plain text from cdtree file
        Args:
            path (str): target file's name and path
        Returns:
            yield (str): plain text
        """
        with open(path, 'r') as file_read:
            for line in file_read:
                line = line.strip()
		if len(line) > 0 and line[0] != '\n' and line[0] != '[' and line[0] != '{' and line[0] != '}' and line[0] != '|' and line[0] != '=' and line[0] != '*' and line[0] != ':' and line[0] != '#':
                    yield line
                #if "] ;" in line:
                #    yield line.split(';')[1].split('\n')[0].strip()

    @staticmethod
    def search():
        """generate path list
        Returns:
            yield (str): target path
        """
        #dirname = '../'
	dirname = '../wiki/'
        filenames = os.listdir(dirname)

        for filename in filenames:
            #if '.cdtree' in filename:
            if '.txt' in filename:
                yield dirname+filename

    @staticmethod
    def whatisthis(string):
        try:
            string.decode('utf-8')
            return "utf8"
        except UnicodeError:
            return "not"

    def generate_per_file(self, file_name, path_list, all_reg):
        kkma = Kkma()
        with open(file_name, 'w') as file_write:
            for path in path_list:
                print path + "-start"
                for item in self.corpus_generator(path):
                    '''
                    item = item.decode('mbcs').encode('utf-8')
                    sliced = item[:len(item)-1]
                    subed = all_reg.sub('', sliced)
                    if len(subed) != 0:
                        continue
                    file_write.write((item + '\n'))
                    '''
                    for sub_item in kkma.sentences(item.decode('utf-8')):
                        sliced = sub_item[:len(sub_item)-1]
                        subed = all_reg.sub('', sliced.encode('utf-8'))
                        if len(subed) != 0:
                            continue
                        if '.' in sub_item:
                            if self.whatisthis(sub_item) == "not":
                                file_write.write(sub_item.encode('utf-8') + '\n')
                            else:
                                file_write.write(sub_item + '\n')
                print path + "-end"

    def generate(self, set_path):
        """generate complex corpus
        Args:
            set_path (str): output dir path
        """
        #with open(set_path + self.complex_output, 'w') as file_write:

        all_reg = re.compile(r"[ 가-힣0-9\,\?\!\'\"\.]+")
        #for path in self.search():
            #print path
            #self.generate_per_file(path, kkma, file_write)
        #for path in self.search():
        #    print path
        #    self.generate_per_file([path], all_reg, file_write)
        path_list = list(self.search())
        processes = []
	for i in range(4):
            file_name = set_path + self.complex_output + '-' + str(i) + ".txt"
            processes.append(Process(target=self.generate_per_file, args=(file_name, path_list[(i*23):(i*23)+23], all_reg)))
            processes[-1].start()
        for p in processes:
            p.join()

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
            pure = []
            pure_punctuation = []
            pure_number = []
            pure_number_punctuation = []

            pure_reg = re.compile(r"[^ 가-힣]+")
            number_list = [str(x) for x in range(10)]
            punctuation_list = [',', '?', '!', "'", '"', '.', '<', '>', '[', ']']
            for complex_item in file_read:
                reg_result = pure_reg.findall(complex_item[:-2])
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
