from modules import corpus, shorter, random_selecter, analyze
import os

output_path = './output/'
if not os.path.exists(output_path):
    os.makedirs(output_path)

corpus.generator(output_path)
shorter.generator(output_path)
random_selecter.generator(output_path)

analyze.generator(output_path, 1)
