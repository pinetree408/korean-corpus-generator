import random
import os

def random_select(output_path, filename):
    fr = open(output_path + 'short/'+ filename, 'r')
    lines = fr.readlines()

    fw = open(output_path + 'random/' + 'random_' + filename, 'w')

    rand_selected = []
    while len(rand_selected) != 50:
        randomed = random.randint(0, len(lines)-1)
        if not(randomed in rand_selected):
            rand_selected.append(randomed)

    for i in rand_selected:
        fw.write(lines[i])

    fw.close()
    fr.close()

def generator(output_path):
    if not os.path.exists(output_path + "random"):
        os.makedirs(output_path + "random")
    random_select(output_path, 'short_pure.txt')
    random_select(output_path, 'short_pure_number.txt')
    random_select(output_path, 'short_pure_punctuation.txt')
    random_select(output_path, 'short_pure_number_punctuation.txt')
