import re
import os
from functools import reduce

class str(str):
    def read():
        return repr(str)

    
def word(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        word_list = [text.split() for text in lines]
        word_list = list(reduce(lambda x,y: x + y, word_list, [] ))
        word_list = [word.lower() for word in word_list]
        word_list = [re.sub(r"^\W+|\W+$", "", word) for word in word_list]
        word_list = [word for word in word_list if word != '']
        
        word_set = set(word_list)
        if word_set == set():
            raise ValueError("This document is empty")
        return word_set

def line(file_path):
    with open(file_path, 'r') as f:
        line_list = f.read().splitlines()
        line_set = set(line_list)
        line_set = set([line for line in line_set if any(c.isalpha() for c in line)])
        # for line in line_set:
            # if line.endswith('\\n'):
            #     line = line[:-2]

        return line_set

def other(file_path, sep):
    with open(file_path, 'r') as f:
        para = f.read()
        word_list = para.split(sep = sep)
        word_list = [text.replace('\n', '') for text in word_list]
        word_list = [text.strip() for text in word_list]
        word_set = set(word_list)
        return  word_set




def perform_split(fp, sep):
    match sep:
        case '\n':
            return line(fp)
        case ' ':
            return word(fp)
        case _:
            return other(fp, sep) 