from modules import corpus, shorter, random_selecter, analyze
from util import correlation_calc
import os
import shutil

set_path = './set/'

output_path = './output/'
if not os.path.exists(output_path):
    os.makedirs(output_path)

analyze_path = './analyze/'
if not os.path.exists(analyze_path):
    os.makedirs(analyze_path)

unigram = analyze.Unigram()
bigram = analyze.Bigram()

set_list = ['pure','pure_number','pure_punctuation','pure_number_punctuation']

for item in set_list:

    unigram.analyze(set_path,analyze_path, item)
    bigram.analyze(set_path,analyze_path, item)

    for i in range(10):
        random_selecter.random_select(set_path, output_path, 'short_' + item + '.txt')
        unigram.analyze(output_path, analyze_path, 'random_short_' + item)
        bigram.analyze(output_path, analyze_path, 'random_short_' + item)
        uni_corr = correlation_calc.correlation_cal(analyze_path + "analyze_" + item + ".txt", analyze_path + "analyze_random_short_" + item + ".txt")
        bi_corr = correlation_calc.correlation_cal(analyze_path + "bigram_analyze_" + item + ".txt", analyze_path + "bigram_analyze_random_short_" + item + ".txt")
        print uni_corr, bi_corr
        shutil.copy2("./output/random_short_" + item +".txt", "./output/random_short_" + item + str(uni_corr) + str(bi_corr) +".txt")

