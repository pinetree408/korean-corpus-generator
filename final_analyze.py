# -*- coding: utf-8 -*-
"""Final analyze

This module analyze correlation between pure set and random picked pure set

"""
import random
import os

from modules import analyze
from util import correlation_calc

SET_LIST = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

def picked_generator(item):
    """Generate random picked item's set.
    Args:
        item (str): It means parent set's property.
    Returns:
        void: it generate file.
    """
    with open('./random_short_' + item + '.txt', 'r') as file_read:
        lines = file_read.readlines()

        i = 5
        while i < 101:
            random.shuffle(lines)
            picked = lines[:i]
            index = str(i)
            if i != 100:
                index = '0' + index
                if i == 5:
                    index = '0' + index
            open_dir = './output/picked/' + item + '/' + item + '_picked_' + index + '.txt'
            with open(open_dir, 'w') as file_write:
                for line in picked:
                    file_write.write(line)
            i += 5

def repeat_picked_generator():
    """Repeat picked_generator function.
    Returns:
        void: it repeat picked_generator function for each parent set.
    """
    for item in SET_LIST:
        picked_generator(item)

def corr_calc_of_picked(target, analyzer):
    """Calculate correaltion between parent set and random picked set.
    Args:
        target (str): It means parent set's property
        analyzer (object): It means analyzer's class type
    Returns:
        void: it repeat picked_generator function for each parent set.
    """
    for item in SET_LIST:
        filenames = os.listdir('./output/picked/' + item +'/')

        analyzer.analyze('./set/', './analyze/', item)

        analyzer_name = ''
        if target == 'bi':
            analyzer_name = 'bigram_'
        elif target == 'word':
            analyzer_name = 'word_'

        with open('./result/result_' + target + '_' + item + '.txt', 'w') as file_read:
            for filename in filenames:
                if not '.txt' in filename:
                    continue
                target_dir = './output/picked' + item + '/'
                analyzer.analyze(target_dir, './analyze/', filename.replace('.txt', ''))

                corr_file1 = './analyze/' + analyzer_name +'analyze_' + item  + '.txt'
                corr_file2 = './analyze/' + analyzer_name + 'analyze_' + filename
                corr = correlation_calc.entropy_calc(corr_file1, corr_file2)
                file_read.write(str(corr) + '\n')

def corr_calc_of_target(target):
    """Calculate correlation of each target
    Args:
        target (str): It means parent set's property
    Returns:
        void: it repeat picked_generator function for each parent set.
    """
    if target == 'uni':
        uni_analyzer = analyze.Unigram()
        corr_calc_of_picked(target, uni_analyzer)
    elif target == 'bi':
        bi_analyzer = analyze.Bigram()
        corr_calc_of_picked(target, bi_analyzer)
    elif target == 'word':
        word_analyzer = analyze.Word()
        corr_calc_of_picked(target, word_analyzer)

if __name__ == "__main__":
    repeat_picked_generator()
    corr_calc_of_target('word')
