# -*- coding: utf-8 -*-
"""Set up the initial set (complex, 4 parent pharse sets)
This module generate complex and 4 parent pharse sets
"""

import os
from modules import corpus, shorter

def main():
    """main srcipt for generate initial set for analayzing
    """
    set_path = './set/'
    if not os.path.exists(set_path):
        os.makedirs(set_path)

    print "Start"
    print "Complex start"
    complex_set = corpus.Complex()
    complex_set.generate(set_path)
    print "Complex complete"
    print "Pre-process start"
    preprocess_first = corpus.Preprocess()
    preprocess_first.generator(set_path)
    preprocess_second = shorter.Preprocess()
    preprocess_second.generator(set_path)
    print "Pre-process complete"

if __name__ == "__main__":
    main()
