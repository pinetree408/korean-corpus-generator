import random


def random_select(filename):
    fr = open(filename, 'r')
    lines = fr.readlines()

    fw = open('random_' + filename, 'w')

    rand_selected = []
    while len(rand_selected) != 50:
        randomed = random.randint(0, len(lines)-1)
        if not(randomed in rand_selected):
            rand_selected.append(randomed)

    for i in rand_selected:
        fw.write(lines[i])

    fw.close()
    fr.close()

random_select('short_pure.txt')
random_select('short_pure_number.txt')
random_select('short_pure_punctuation.txt')
random_select('short_pure_number_punctuation.txt')
