from modules import corpus, shorter, random_selecter, analyze
from util import correlation_calc
import os
import shutil

set_path = './set/'
if not os.path.exists(set_path):
    os.makedirs(set_path)

print "Start"
print "Complex start"
complex = corpus.Complex()
complex.generate(set_path)
print "Complex complete"
print "Pre-process start"
preprocess_first = corpus.Preprocess()
preprocess_first.generator(set_path)
preprocess_second = shorter.Preprocess()
preprocess_second.generator(set_path)
print "Pre-process complete"
