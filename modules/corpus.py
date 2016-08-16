# -*- coding: utf-8 -*-
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


def complex_result(output_path):
    path_list = search_txt()

    fw = open(output_path + complex_output, 'w')

    all_reg = re.compile('[ a-zA-Z가-힣0-9\,\(\)\?\!\'\"\.\<\>\[\]]+')

    for path in path_list:
        corpus = corpus_generator(path)
        for item in corpus:
            item = item.decode('mbcs').encode('utf-8')
            sliced = item[:len(item)-1]
            if len(all_reg.sub('', sliced)) != 0:
                continue
            fw.write((item + '\n'))
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
        fw.write(item)
    fw.close()


def divide_result(output_path):
    fr = open(output_path + complex_output, 'r')
    complex_list = fr.readlines()

    pure = []
    pure_punctuation = []
    pure_number = []
    pure_number_punctuation = []

    all_reg = re.compile('[ 가-힣0-9\,\(\)\?\!\'\"\.\<\>\[\]]+')

    pure_reg = re.compile('[^ 가-힣]+')
    number_list = [str(x) for x in range(10)]
    punctuation_list = [',', '(', ')', '?', '!', "'", '"', '.', '<', '>', '[', ']']
    for complex in complex_list:
        encoded = complex
        if len(all_reg.sub('', encoded[:len(encoded)-2])) != 0:
            continue
        reg_result = pure_reg.findall(encoded[:len(encoded)-2])
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

    make_output(output_path + 'pure/pure.txt', pure)
    make_output(output_path + 'pure/pure_number.txt', pure_number)
    make_output(output_path + 'pure/pure_number_punctuation.txt', pure_number_punctuation)
    make_output(output_path + 'pure/pure_punctuation.txt', pure_punctuation)
    fr.close()


def combine_result(output_path, filename):
    fa = open(output_path + filename, 'a')
    fr = open(output_path + 'pure/pure.txt', 'r')
    for line in fr.readlines():
        fa.write(line)
    fr.close()
    if filename == "pure/pure_number_punctuation.txt":
        frn = open(output_path + 'pure/pure_number.txt', 'r')
        for line in frn.readlines():
            fa.write(line)
        frn.close()
        frp = open(output_path + 'pure/pure_punctuation.txt', 'r')
        for line in frp.readlines():
            fa.write(line)
        frp.close()
    fa.close()

def generator(output_path):
    if not os.path.exists(output_path + "pure"):
        os.makedirs(output_path + "pure")
    complex_result(output_path)
    divide_result(output_path)
    combine_result(output_path, 'pure/pure_number.txt')
    combine_result(output_path, 'pure/pure_punctuation.txt')
    combine_result(output_path, 'pure/pure_number_punctuation.txt')
