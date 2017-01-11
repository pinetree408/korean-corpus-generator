import collections
import math


def correlation(A, B): 
    n = len(A)
    Asum, Bsum = sum(A), sum(B)
    return (
        (n * sum(a * b for a, b in zip(A, B)) - Asum * Bsum)
        / math.sqrt(n*sum(a**2 for a in A) - Asum**2)
        / math.sqrt(n*sum(b**2 for b in B) - Bsum**2)
    )   

def correlation_cal(file1, file2):
    f1r = open(file1+".txt", 'r')
    f2r = open(file2+".txt", 'r')

    f1lines = f1r.readlines()
    f2lines = f2r.readlines()

    f1correl = {}
    for line in f1lines:
        temp = line.split(':')
        f1correl[temp[0].strip()] = temp[1].strip()
    od1 = collections.OrderedDict(sorted(f1correl.items()))

    f2correl = {}
    for line in f2lines:
        temp = line.split(':')
        f2correl[temp[0].strip()] = temp[1].strip()
    od2 = collections.OrderedDict(sorted(f2correl.items()))


    f1value = []
    for k, v in od1.iteritems():
        f1value.append(int(v))

    f2value = []
    for k, v in od2.iteritems():
        f2value.append(int(v))

    corr = correlation(f1value, f2value)

    f1r.close()
    f2r.close()
    return corr

def entropy_calc(file1, file2):
    f1r = open(file1+".txt", 'r')
    f2r = open(file2+".txt", 'r')

    f1lines = f1r.readlines()
    f2lines = f2r.readlines()

    f1correl = {}
    for line in f1lines:
        temp = line.split(':')
        f1correl[temp[0].strip()] = temp[1].strip()
    od1 = collections.OrderedDict(sorted(f1correl.items()))

    f2correl = {}
    for line in f2lines:
        temp = line.split(':')
        f2correl[temp[0].strip()] = temp[1].strip()
    od2 = collections.OrderedDict(sorted(f2correl.items()))


    f1value = []
    for k, v in od1.iteritems():
        f1value.append(float(v))

    f2value = []
    for k, v in od2.iteritems():
        f2value.append(float(v))

    p_sum = sum(f2value)
    q_sum = sum(f1value)
    entropy = 0.0
    for i in range(len(f1value)):
	p = (f2value[i]/p_sum)
	q = (f1value[i]/q_sum)
        print p, q
	if q == 0.0 or p == 0.0:
            continue
        log_unit = math.log((p/q), 2)
        unit = p*log_unit
	entropy += unit
    
    f1r.close()
    f2r.close()
    return entropy
	
#print correlation_cal("../output/word_analyze_pure.txt", "../output/word_analyze_random_short_pure_0.992831169761.txt")
