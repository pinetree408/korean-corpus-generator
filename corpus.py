#-*- coding: utf-8 -*-
import re
import os

complex_output = 'complex.txt'


def corpus_generator(path):
    fr = open(path, 'r')
    lines = fr.readlines()

    result = []
    for line in lines:
        if ';' in line:
            final = line.split(';')[1].split('\n')[0].strip()
            result.append(final)
    fr.close()
    return result


def search_txt():
    dirname = '../'
    filenames = os.listdir(dirname)

    result = []
    for filename in filenames:
        if '.cdtree' in filename:
            txtfile = dirname+filename
            result.append(txtfile)
    return result

def complex_result():
    path_list = search_txt()

    fw = open(complex_output, 'w')

    for path in path_list:
        corpus = corpus_generator(path)
        for item in corpus:
            fw.write(item[:len(item)-1] + '\n')
    fw.close()

def check_list(list1, list2):
    for item1 in list1:
        for item2 in list2:
            if item1 in item2:
	        return True

    return False

def make_output(filename, input_list):
    fw = open(filename, 'w')
    for item in input_list:
        fw.write(item.decode('mbcs').encode('utf-8'))
    fw.close()



def divide_result():
    fr = open(complex_output, 'r')
    complex_list = fr.readlines()

    pure = []
    pure_punctuation = []
    pure_number = []
    pure_number_punctuation = []

    all_reg = re.compile('[ 가-힣0-9\,\(\)\?\!\'\"\.\<\>\[\]]+')

    pure_reg = re.compile('[^ 가-힣]+')
    number_list = [str(x) for x in range(10)]
    punctuation_list = [',','(',')','?','!',"'",'"','.','<','>','[',']']
    for complex in complex_list:
        encoded = complex.decode('mbcs').encode('utf-8')
        if len(all_reg.sub('', encoded[:len(encoded)-1])) != 0:
            continue
        reg_result = pure_reg.findall(encoded[:len(encoded)-1])
        if len(reg_result) == 0:
            pure.append(complex)
	else:
            if check_list(number_list, reg_result) and check_list(punctuation_list, reg_result):
                pure_number_punctuation.append(complex)
            else:
                if check_list(number_list, reg_result):
                    pure_number.append(complex)
                else:
                    pure_punctuation.append(complex)
    
    make_output('pure.txt', pure)
    make_output('pure_number.txt', pure_number)
    make_output('pure_number_punctuation.txt', pure_number_punctuation)
    make_output('pure_punctuation.txt', pure_punctuation)

complex_result()
divide_result()
