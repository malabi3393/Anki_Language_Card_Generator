import re
import os

class str(str):
    def read():
        return repr(str)

def get_file_contents(fp):
    with open(fp, 'r') as f:
        return f.read()
    
def word(file_path):
    text = ''
    if os.path.isfile(file_path):
        text = get_file_contents(file_path)
    word_list = text.split(sep = ' ')
    word_list = [word.lower() for word in word_list]
    word_list = [re.sub(r"[\W*]", "", word) for word in word_list]
    word_set = set(word_list)
    return word_set

def line(file_path):
    with open(file_path, 'r') as f:
        line_list = f.read().splitlines()
        line_set = set(line_list)
        return line_set