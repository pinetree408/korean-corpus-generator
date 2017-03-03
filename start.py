# -*- coding: utf-8 -*-
"""Generate 10 random picked pharse set

This module generate 10 random picked pharse sets from random_selector module

"""
import os
import shutil

from modules import analyze, random_selector
from util import correlation_calc

if __name__ == "__main__":
    SET_PATH = "./set/"
    OUTPUT_PATH = "./output/"
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    ANALYZE_PATH = "./analyze/"
    if not os.path.exists(ANALYZE_PATH):
        os.makedirs(ANALYZE_PATH)

    UNIGRAM = analyze.Unigram()
    BIGRAM = analyze.Bigram()
    WORD = analyze.Word()

    #SET_LIST = ["pure", "pure_number", "pure_punctuation", "pure_number_punctuation"]
    SET_LIST = ["pure_number_punctuation"]

    for item in SET_LIST:

        print "start-" + item
        print "start-unigram"
        UNIGRAM.analyze(SET_PATH, ANALYZE_PATH, item)
        print "start-bigram"
        BIGRAM.analyze(SET_PATH, ANALYZE_PATH, item)
        print "start-morpheme"
        WORD.analyze(SET_PATH, ANALYZE_PATH, item)

        print "start random generate"
        for i in range(10):
            random_selector.random_select(SET_PATH, OUTPUT_PATH, 'short_'+item+'.txt')

            random_short_target = 'random_short_' + item #mackenzie_
            UNIGRAM.analyze(OUTPUT_PATH, ANALYZE_PATH, random_short_target)
            BIGRAM.analyze(OUTPUT_PATH, ANALYZE_PATH, random_short_target)
            WORD.analyze(OUTPUT_PATH, ANALYZE_PATH, random_short_target)

            uni_analyze_path = ANALYZE_PATH + "analyze_"
            bi_analyze_path = ANALYZE_PATH + "bigram_analyze_"
            word_analyze_path = ANALYZE_PATH + "word_analyze_"

            uni_corr = correlation_calc.correlation_cal(uni_analyze_path+item,
                                                        uni_analyze_path+random_short_target)
            bi_corr = correlation_calc.correlation_cal(bi_analyze_path+item,
                                                       bi_analyze_path+random_short_target)
            word_corr = correlation_calc.correlation_cal(word_analyze_path+item,
                                                         word_analyze_path+random_short_target)

            final_name = "_"+str(uni_corr)+"_"+str(bi_corr)+"_"+str(word_corr)
            print final_name
            copied = "./output/random_short_"+item
            shutil.copy2(copied+".txt", copied+final_name+".txt")
