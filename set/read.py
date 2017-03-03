# -*- coding: utf-8 -*-
import re
with open("complex.txt", 'r') as file_read:
    lines = file_read.readlines()
    for line in lines[:100]:
        if '《' in line:
            all_reg = re.compile(r"[ 0-9\,\?\!\'\"\.가-힣]+")
            subed = all_reg.sub('', line)
            print subed
            print line
