from modules import analyze
from util import correlation_calc
import random
import os

def picked_generator(item):
    fr = open('./random_short_' + item + '.txt','r')
    lines = fr.readlines()

    i = 5
    while (i < 101):
        random.shuffle(lines)
        picked = lines[:i]
        index = str(i)
        if i != 100:
            index = '0' + index
            if i == 5:
                index = '0' + index
        fw = open('./output/picked/' + item + '/' + item + '_picked_' + index + '.txt', 'w')
        for j in range(len(picked)):
            fw.write(picked[j])
        fw.close()
        i += 5
    fr.close()

set_list = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

for item in set_list:
    picked_generator(item)

target = 'word'

for item in set_list:
    filenames = os.listdir('./output/picked/' + item +'/')

    analyzer = analyze.Unigram() # default
    if target == 'bi':
        analyzer = analyze.Bigram()
    elif target == 'word':
        analyzer = analyze.Word()

    analyzer.analyze('./set/', './analyze/', item)

    analyzer_name = ''
    if target == 'bi':
        analyzer_name = 'bigram_'
    elif target == 'word':
        analyzer_name = 'word_'

    fr = open('./result/result_' + target + '_' + item + '.txt', 'w')
    for filename in filenames:
        if not('.txt' in filename):
            continue
        analyzer.analyze('./output/picked/' + item + '/', './analyze/', filename.replace('.txt', ''))
        corr = correlation_calc.entropy_calc('./analyze/' + analyzer_name +'analyze_' + item  + '.txt', './analyze/' + analyzer_name + 'analyze_' + filename)
        #print corr
        fr.write(str(corr) + '\n')
    fr.close()
