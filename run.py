import string
import os
from string import ascii_lowercase
import linecache
from auto_complete_data import AutoCompleteData

STOP_INPUT = '#'
PRINT_GREEN = "\u001b[38;5;28m\x1B[3m"
RESET_COLOR = "\033[0m"
PRINT_ITALLIC = "\x1B[3m"

#=====================Auxiliary Functions========================

def remove_duplicate_objects_from_list(list_):
    list_.sort(key=lambda x: x.score, reverse=True)
    list2 = []
    flag = True
    for obj1 in list_:
        for obj2 in list2:
            if obj1.completed_sentence == obj2.completed_sentence and obj1.source_text == obj2.source_text:
                flag = False
                break
        if flag:
            list2.append(obj1)
    
    return list2

def build_objects(results, data_collection, files_dict, new_string):
    list_of_auto_completes = []
    for i, sentence in enumerate(results):
        line = linecache.getline(files_dict[sentence[0]], sentence[1])
        new_object = AutoCompleteData(line, files_dict[sentence[0]], sentence[1],  AutoCompleteData.get_score(new_string))
        list_of_auto_completes.append(new_object)
    return list_of_auto_completes

    
def remove_char(string, index, data_collection, files_dict):
    SCORING = [10, 8, 6, 4, 2]
    new_string = string[:index] + string[index + 1:]
    tmp = complete_word(new_string, data_collection)
    list_of_objects = build_objects(tmp, data_collection, files_dict, new_string)
    for object_ in list_of_objects:
        object_.set_score(SCORING[index] if index < len(SCORING) else SCORING[-1])
    return list_of_objects

def add_char(string, index, char, data_collection, files_dict):
    SCORING = [5, 4, 3, 2, 1]
    new_string = string[:index] + char + string[index:]
    tmp = complete_word(new_string, data_collection)
    list_of_objects = build_objects(tmp, data_collection, files_dict, new_string)
    for object_ in list_of_objects:
        object_.set_score(SCORING[index] if index < len(SCORING) else SCORING[-1])
    return list_of_objects

def replace_char(string, index, char, data_collection, files_dict):
    SCORING = [5, 4, 3, 2, 1]
    new_string = string[:index] + char + string[index + 1:]
    tmp = complete_word(new_string, data_collection)
    list_of_objects = build_objects(tmp, data_collection, files_dict, new_string)
    for object_ in list_of_objects:
        object_.set_score(SCORING[index] if index < len(SCORING) else SCORING[-1])
    return list_of_objects

def complete_word(word, data_collection):
    return data_collection[word] if word in data_collection else []

def less_match(list_of_sentences):
    list_of_sentences.sort(key=lambda x: x.completed_sentence, reverse=True)
    return min(list_of_sentences, key=lambda x: x.score)

def ignore_symbols(sentence):
    exclude = set(string.punctuation)
    sentence = ''.join(ch for ch in sentence if ch not in exclude)
    sentence = ''.join(sentence.split())
    return sentence

#=====================End Auxiliary Functions========================

def get_best_k_completions(string_to_complete, data_collection, files_dict, K):
    tmp = complete_word(string_to_complete, data_collection)
    results = build_objects(tmp, data_collection, files_dict, string_to_complete)

    # try to find similar completions to match search
    for i in range(len(string_to_complete)):
        # remove one letter to match a completion
        results += remove_char(string_to_complete, i, data_collection, files_dict)
        results = remove_duplicate_objects_from_list(results)
        
        while len(results) > K:
            results.remove(less_match(results))
        
        for ch in ascii_lowercase:
            # add one letter to match a completion
            results += add_char(string_to_complete, i, ch, data_collection, files_dict)
            results = remove_duplicate_objects_from_list(results)
            
            while len(results) > K:
                results.remove(less_match(results))

            # change one letter to match a completion
            results += replace_char(string_to_complete, i, ch, data_collection, files_dict)
            results = remove_duplicate_objects_from_list(results)
            
            while len(results) > K:
                results.remove(less_match(results))
  
    return results


def print_results(results):
    for i, item in enumerate(results, 1):
        print(f'{str(i)}.{item.completed_sentence}, ({item.source_text}, {item.offset}, {item.score} )')

def search_input(user_input, data_collection, files_dict, K):
    string_to_complete = ignore_symbols(user_input)
    
    while user_input != STOP_INPUT:
        results = get_best_k_completions(string_to_complete, data_collection, files_dict, K)
        
        if (len(results) == 0):
            print("No Results")
            run(data_collection, files_dict, K)
        print_results(results)
        
        # let user continue his search
        user_input = input(f"{PRINT_GREEN}{PRINT_ITALLIC}{string_to_complete}{RESET_COLOR}")
        string_to_complete += ignore_symbols(user_input)


def run(data_collection, files_dict, K):
    while True:
        first_input = input("Enter your text:\n")
        search_input(first_input, data_collection, files_dict, K)
