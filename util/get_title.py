import os

def corpus_generator(path):
    fr = open(path, 'r')
    lines = fr.readlines()

    result = []
    for line in lines:
        if 'filename' in line:
	    result.append(line)
	elif 'title' in line:
	    result.append(line)
	elif 'author' in line:
	    result.append(line)
	elif 'date' in line:
	    result.append(line)
    fr.close()
    return result

def search_txt():
    dirname = '../'
    filenames = os.listdir(dirname)

    result = []
    for filename in filenames:
        if '.cdtree' in filename:
            txtfile = dirname+filename
            result.append(txtfile)
    return result

def complex_result():
    path_list = search_txt()

    fw = open('title.txt', 'w')

    for path in path_list:
        corpus = corpus_generator(path)
	title = ""
        for item in corpus:
            item = item.decode('mbcs').encode('utf-8')
	    parsed = item.split('>')
	    content = parsed[1].split('<')
	    title += "|" + content[0]

        fw.write((title + '\n'))

    fw.close()

complex_result()
