# -*- coding: utf-8 -*-
import re
import os


class Complex():

    complex_output = 'complex.txt'

    def corpus_generator(self, path):
        fr = open(path, 'r')
        lines = fr.readlines()

        result = []
        for line in lines:
            if '] ;' in line:
                final = line.split(';')[1].split('\n')[0].strip()
                result.append(final)

        fr.close()
        return result

    def search(self):
        dirname = '../'
        filenames = os.listdir(dirname)

        result = []
        for filename in filenames:
            if '.cdtree' in filename:
                txtfile = dirname+filename
                result.append(txtfile)
        return result


    def generate(self, set_path):
        path_list = self.search()

        fw = open(set_path + self.complex_output, 'w')

        all_reg = re.compile('[ 가-힣0-9\,\?\!\'\"\.\<\>\[\]]+')

        for path in path_list:
            corpus = self.corpus_generator(path)
            for item in corpus:
                item = item.decode('mbcs').encode('utf-8')
                sliced = item[:len(item)-1]
		subed = all_reg.sub('', sliced)
                if len(subed) != 0:
                    continue
                fw.write((item + '\n'))
        fw.close()

class Preprocess():

    complex_output = 'complex.txt'

    def check_list(self, list1, list2):
        for item1 in list1:
            for item2 in list2:
                if item1 in item2:
                    return True

        return False


    def make_output(self, filename, input_list):
        fw = open(filename, 'w')
        for item in input_list:
           fw.write(item)
        fw.close()


    def generator(self, set_path):
        fr = open(set_path + self.complex_output, 'r')
        complex_list = fr.readlines()

        pure = []
        pure_punctuation = []
        pure_number = []
        pure_number_punctuation = []

        pure_reg = re.compile('[^ 가-힣]+')
        number_list = [str(x) for x in range(10)]
        punctuation_list = [',', '?', '!', "'", '"', '.', '<', '>', '[', ']']
        for complex in complex_list:
        
	    reg_result = pure_reg.findall(complex[:len(complex)-2])
            if len(reg_result) == 0:
                pure.append(complex)
	        pure_number.append(complex)
	        pure_punctuation.append(complex)
	        pure_number_punctuation.append(complex)
            else:
                if self.check_list(number_list, reg_result) and self.check_list(punctuation_list, reg_result):
                    pure_number_punctuation.append(complex)
                else:
                    if self.check_list(number_list, reg_result):
                        pure_number.append(complex)
		        pure_number_punctuation.append(complex)
                    else:
                        pure_punctuation.append(complex)
		        pure_number_punctuation.append(complex)

        self.make_output(set_path + 'pure.txt', pure)
        self.make_output(set_path + 'pure_number.txt', pure_number)
        self.make_output(set_path + 'pure_number_punctuation.txt', pure_number_punctuation)
        self.make_output(set_path + 'pure_punctuation.txt', pure_punctuation)
        fr.close()
