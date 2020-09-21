import os
import string
from string import ascii_lowercase
import linecache

def all_substrings(sentence):
    sentence_without_spaces = ''.join(sentence.split())
    res = [sentence_without_spaces[i: j] for i in range(len(sentence_without_spaces))
           for j in range(i + 1, len(sentence_without_spaces) + 1)]
    
    return list(set(res))


def add_text_to_data(file_lines, file_number, data_collection):
    for line_number, line in enumerate(file_lines, 1):
        substrings_of_line = all_substrings(line)
        for substr in substrings_of_line:
            if substr.lower() in data_collection:
                if len(data_collection[substr.lower()]) < 5:
                    data_collection[substr.lower()].append([file_number, line_number])
            else:
               data_collection[substr.lower()] = [[file_number, line_number]]
             
    
def open_file(root, file):
    if file.endswith('.txt'):
        open_file = open(os.path.join(root, file), encoding="utf8")
        
        return open_file.read().split('\n')


def init_data_collection(path):
    print("Loading the files and preparing the system...")
    data_collection = {}
    files_dict = {}
    for (root, dirs, files) in os.walk(path):
        for file_number, file in enumerate(files):
            
            # for each file read data
            file_lines = open_file(root, file)
            
            # add every path to the files dict
            files_dict[file_number] = os.path.join(root, file)
            
            # Inserting the text into the data base
            add_text_to_data(file_lines, file_number, data_collection)
    
    print("The system is ready.")
    
    return data_collection, files_dict