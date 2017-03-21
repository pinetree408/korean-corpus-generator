import operator

type_list = ['', 'bigram_', 'word_']
SET_LIST = ['pure', 'pure_number', 'pure_punctuation', 'pure_number_punctuation']

for typ in type_list:
    print typ
    for item in SET_LIST:
        print item
        with open("analyze/"+typ+"analyze_" + item +".txt", 'r') as parent, \
            open("analyze/"+typ+"analyze_random_short_"+ item +".txt") as child:
            parent_total = 0
            child_total = 0

            for line in parent:
                line_splited = line.split(':')
                if int(line_splited[1]) != 0:
                    parent_total += 1
            for line in child:
                line_splited = line.split(':')
                if int(line_splited[1]) != 0:
                    child_total += 1
            print parent_total, child_total
