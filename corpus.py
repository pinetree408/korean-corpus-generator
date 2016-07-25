#-*- coding: utf-8 -*-
import re
import os


def corpus_generator(path):
    hangul = re.compile('[^ 가-힣]+')
    fr = open(path, 'r')
    lines = fr.readlines()

    result = []
    result.append(path)
    for line in lines:
        if line.strip() == '':
            continue
        sentence = line.strip().split('\n')[0]
        if sentence[len(sentence)-1] == '.':
            sentence_list = sentence.split('.')
            for check in sentence_list:
                if check.strip() == '':
                    continue
                initial = check.strip().decode('mbcs').encode('utf-8')
                corpus = hangul.findall(initial)
                if len(corpus) == 0:
                    result.append(initial)

    fr.close()
    return result


def search_txt():
    dirname = '../'
    filenames = os.listdir(dirname)

    result = []
    for filename in filenames:
        if not('.py' in filename):
            subfiles = os.listdir(dirname+filename+'/')
            for subfile in subfiles:
                if '.txt' in subfile:
                    txtfile = dirname+filename+'/'+subfile
                    result.append(txtfile)
                elif not('.py' in subfile):
                    finalfiles = os.listdir(dirname+filename+'/'+subfile+'/')
                    for finalfile in finalfiles:
                        if '.txt' in finalfile:
                            txtfile = dirname+filename+'/'+subfile+'/'+finalfile
                            result.append(txtfile)
    return result


path_list = search_txt()

fw = open('result.txt', 'w')

for path in path_list:
    corpus = corpus_generator(path)
    for item in corpus:
        fw.write(item + '\n')
fw.close()


