f = open('result.txt', 'r')

lines = f.readlines()

result = {}
for line in lines:
    if len(line) in result:
        updated = result[len(line)]
	del result[len(line)]
	result[len(line)] = updated + 1
    else:
        result[len(line)] = 1

print result
