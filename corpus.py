#-*- coding: utf-8 -*-
import re
import os


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


path_list = search_txt()

fw = open('result.txt', 'w')

for path in path_list:
    corpus = corpus_generator(path)
    for item in corpus:
        fw.write(item + '\n')
fw.close()


