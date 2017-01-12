# -*- coding: utf-8 -*-
"""Random select

This module generate random picked 400 pharse set

"""
import random

def random_select(set_path, output_path, filename):
    """Select random picked 400 pharse set from target filename
    Args:
        set_path (str): target input file's path
        output_path (str): output file's path
        filename (str): target filename
    """
    with open(set_path + 'short/'+ filename, 'r') as file_read:
        lines = file_read.readlines()

        with open(output_path + 'random_' + filename, 'w') as file_write:

            rand_queue = [i for i in range(len(lines))]
            rand_selected = []

            while len(rand_selected) != 400:
                picked = random.choice(rand_queue)
                rand_selected.append(picked)
                rand_queue.remove(picked)

            for index in rand_selected:
                file_write.write(lines[index])

def generator(set_path, output_path):
    """generate random picked 400 pharse set from each 4 parent pharse set
    Args:
        set_path (str): target input file's path
        output_path (str): output file's path
    """
    random_select(set_path, output_path, 'short_pure.txt')
    random_select(set_path, output_path, 'short_pure_number.txt')
    random_select(set_path, output_path, 'short_pure_punctuation.txt')
    random_select(set_path, output_path, 'short_pure_number_punctuation.txt')
