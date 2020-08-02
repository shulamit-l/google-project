import os
import string
from string import ascii_lowercase
import linecache


class AutoCompleteData:
    def __init__(self, completed_sentence, source_text, offset, score=0):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score


def prGreen(skk): print("\033[92m {}\033[00m".format(skk), end='')


def all_substrings(sentence):
    sentence_without_spaces = ''.join(sentence.split())
    res = [sentence_without_spaces[i: j] for i in range(len(sentence_without_spaces))
           for j in range(i + 1, len(sentence_without_spaces) + 1)]
    return list(set(res))


def get_score(word):
    return len(word) * 2


def compare_score(new_sentence, all_sentences):
    if new_sentence.score < min(sentence.score for sentence in all_sentences):
        return all_sentences
    for i in range(5):
        if all_sentences[i].score < new_sentence.score:
            all_sentences[i] = new_sentence
        if all_sentences[i].score == new_sentence.score:
            newlist = [all_sentences[i].completed_sentence, new_sentence.completed_sentence]
            newlist.sort()
            all_sentences[i] = newlist[0]
    return all_sentences


dict = {}


def insert_test_to_dict(file_list, index):
    for line in range(len(file_list)):
        sentence_list = [index, line + 1]
        list_of_substr = all_substrings(file_list[line])
        for substr in list_of_substr:
            if substr.lower() in dict:
                if len(dict[substr.lower()]) < 5:
                    dict[substr.lower()].append(sentence_list)
            else:
                new_list = [sentence_list]
                dict[substr.lower()] = new_list


def open_file(root, file):
    if file.endswith('.txt'):
        open_file = open(os.path.join(root, file), encoding="utf8")
        return open_file.read().split('\n')


dict_of_files = {}


def init(path):
    print("Loading the files and preparing the system...")
    index = 0
    for (root, dirs, files) in os.walk(path):
        for file in files:
            text_in_file = open_file(root, file)
            """Inserting the text into the data base"""
            dict_of_files[index] = os.path.join(root, file)
            insert_test_to_dict(text_in_file, index)
            index += 1
    print("The system is ready.")


def update_score_after_add_or_remove(index, position, string):
    score = get_score(string)
    if index >= 4:
        score -= 2
    else:
        score -= (5 - index) * 2

    dict_of_score[position] = score


def update_score_after_replace(index, position, string):
    score = get_score(string)
    if index >= 4:
        score -= 1
    else:
        score -= (5 - index)

    dict_of_score[position] = score


def add_or_remove_char(string, index, list):
    new_string = string[:index] + string[index + 1:]
    if new_string in dict:
        for i in dict[new_string]:
            if i not in list:
                list.append(i)
                update_score_after_add_or_remove(index, len(list)-1, string)
                return list
    else:
        for ch in ascii_lowercase:
            new_string = string[:index] + ch + string[index:]
            if new_string in dict:
                for i in dict[new_string]:
                    if i not in list:
                        list.append(i)
                        update_score_after_add_or_remove(index, len(list)-1, string)
                        return list
    return list


def replace_char(string, index, list):
    for ch in ascii_lowercase:
        new_string = string[:index] + ch + string[index + 1:]
        if new_string in dict:
            for i in dict[new_string]:
                if i not in list:
                    list.append(i)
                    update_score_after_replace(index, len(list)-1, string)
                    return list
    return list


dict_of_score = {}


def get_best_k_completions(string):
    list1 = []
    if string.lower() in dict:
        for i, sentence in enumerate(dict[string.lower()]):
            list1.append(sentence)
            dict_of_score[i] = get_score(string)

    if len(list1) != 5:
        if len(string) > 4:
            for i in range(len(string)):
                list1 = replace_char(string, i + 4, list1)
                if len(list1) == 5:
                    break
            for i in range(len(string)):
                if len(list1) == 5:
                    break
                list1 = add_or_remove_char(string, i + 4, list1)
        if len(string) > 4:
            index = 4
        else:
            index = len(string) - 1
        for i in range(index, 1, -1):
            list1 = replace_char(string, i, list1)
            if len(list1) == 5:
                break
        list1 = add_or_remove_char(string,3, list1)
        if len(list1) != 5:
            list1 = replace_char(string, 0, list1)
        if len(list1) != 5:
            for i in range(2, 0, -1):
                list1 = add_or_remove_char(string, 3, list1)
                if len(list1) == 5:
                    break

    if len(list1) == 0:
        print("No matching results")
        run()
    else:
        list_of_sentence = []
        for i, sentence in enumerate(list1):
            line = linecache.getline(dict_of_files[sentence[0]], sentence[1])

            new_object = AutoCompleteData(line, dict_of_files[sentence[0]], sentence[1], dict_of_score[i])
            list_of_sentence.append(new_object)
        return list_of_sentence


def ignore_symbols(sentence):
    exclude = set(string.punctuation)
    sentence = ''.join(ch for ch in sentence if ch not in exclude)
    sentence = ''.join(sentence.split())
    return sentence


def search_input(user_input):
    user_sentence = ignore_symbols(user_input)
    while user_input != '#':
        results = get_best_k_completions(user_sentence)
        print_results(results, user_sentence)
        print("\u001b[38;5;28m ",user_sentence)
        user_input = input()
        user_sentence += ignore_symbols(user_input)


def print_results(results, user_sentence):
    num_of_suggestion = 1
    for i in results:
        print(f'{str(num_of_suggestion)}.{i.completed_sentence}, ({i.source_text}, {i.offset}, {i.score} )')
        num_of_suggestion += 1


def run():
    while True:
        first_input = input("Enter your text:\n")
        search_input(first_input)


def main():
    """Init the data base with the files sources"""
    init('my')
    """Run the search system"""
    run()


if __name__ == "__main__":
    main()
