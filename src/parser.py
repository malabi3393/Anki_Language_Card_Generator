import re
import os
from functools import reduce

class str(str):
    def read():
        return repr(str)

    
def open_file(fp, sep):
    with open(fp, 'r') as f: return f.read()

#THIS IS NOW TEXT RENAME IT AS SUCH
def word(lines):
    word_list = lines.split()
    word_list = [word.lower() for word in word_list]
    word_list = [re.sub(r"^\W+|\W+$", "", word) for word in word_list]
    word_list = [word for word in word_list if word != '']
    
    word_set = set(word_list)
    if word_set == set():
        raise ValueError("This document is empty")
    return word_set

def line(line_list):
    line_list = line_list.split('\n')
    line_set = set(line_list)
    line_set = set([line for line in line_set if any(c.isalpha() for c in line)])
    # for line in line_set:
        # if line.endswith('\\n'):
        #     line = line[:-2]

    return line_set

def sentence(para):
    sentences = para.split('.')
    def further_split(sep, sen):
        new_split = [i.split(sep) for i in sen]
        return list(reduce(lambda x, y: x + y, new_split, []))
    sentences = further_split('!', sentences)
    sentences = further_split('?', sentences)
    sentences = [s for s in sentences if s != '']
    sentences = [s.strip() for s in sentences if s != '']
    return sentences

def other(para, sep):
    word_list = para.split(sep = sep)
    word_list = [text.replace('\n', '') for text in word_list]
    word_list = [text.strip() for text in word_list]
    word_set = set(word_list)
    return  word_set




def perform_split(fp, sep = ' ', filepath = True):
    if filepath:
        fp = open_file(fp, sep)
    match sep:
        case '\n':
            return line(fp)
        case ' ':
            return word(fp)
        case '.':
            return sentence(fp)
        case _:
            return other(fp, sep) 