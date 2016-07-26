fr = open('complex.txt', 'r')

lines = fr.readlines()

result = {}
for line in lines:
    if len(line) in result:
        updated = result[len(line)]
	del result[len(line)]
	result[len(line)] = updated + 1
    else:
        result[len(line)] = 1

fw = open('analyze.txt', 'w')
for key in result.keys():
    fw.write(str(key) + ' : ' + str(result[key]) + '\n')
fw.close()

fr.close()
