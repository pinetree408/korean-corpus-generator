import operator

with open("analyze/bigram_analyze_pure.txt", 'r') as file_read:
    total = 0
    result = {}
    for line in file_read:
        line_splited = line.split(':')
        total += int(line_splited[1])
        result[line_splited[0]] = line_splited[1]

    for key in result.keys():
        result[key] = float(result[key]) / float(total) * 100

    sorted_result = sorted(result.items(), key=operator.itemgetter(1))
    sorted_result.reverse()
    for item in sorted_result:
        print item
