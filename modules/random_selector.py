import random
import os

def random_select(set_path, output_path, filename):
    fr = open(set_path + 'short/'+ filename, 'r')
    lines = fr.readlines()

    fw = open(output_path + 'random_' + filename, 'w')


    rand_queue = [i for i in range(len(lines))]
    rand_selected = []

    while len(rand_selected) != 400:
    	picked = random.choice(rand_queue)
	rand_selected.append(picked)
	rand_queue.remove(picked)

    for index in rand_selected:
        fw.write(lines[index])

    fw.close()
    fr.close()

def generator(set_path, output_path):
    random_select(set_path, output_path, 'short_pure.txt')
    random_select(set_path, output_path, 'short_pure_number.txt')
    random_select(set_path, output_path, 'short_pure_punctuation.txt')
    random_select(set_path, output_path, 'short_pure_number_punctuation.txt')
