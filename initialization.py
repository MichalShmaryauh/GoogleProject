import os
from trie import Trie

"""This class Store Data so that every word in every file is a key \n
in singelton words_dict and every key have a trie of the all the next word in every file \n
in addation we have a anothe words_trie that keep all the key in dictionary \n
 (becauth if the user enter prefix of any word) """


class StoreData:
    __instance = None
    words_dict = {}
    words_trie = Trie()

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __str__(self):
        return "words_dict={}".format(self.words_dict)


"""This function get a dictionary and return a list of all the sub files """


def get_list_of_files(dirName):
    list_of_file = os.listdir(dirName)
    all_files = list()
    for entry in list_of_file:
        full_path = os.path.join(dirName, entry)
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)

    return all_files


"""This function add words to dictionary """


def add_words_to_dictionary(line, num_line, file):
    dict = StoreData()
    words_array = line.replace('\n', '').split()
    for index in range(len(words_array)):
        if index == len(words_array) - 1:
            new_word = ''
        else:
            new_word = words_array[index + 1]
        if not dict.words_dict.get(words_array[index]):
            dict.words_dict[words_array[index]] = Trie()
        dict.words_trie.insert(words_array[index], (num_line, file))
        dict.words_dict[words_array[index]].insert(new_word, (num_line, file))


"""This function open file """


def open_file(dir_name):
    files_list = get_list_of_files(dir_name)
    try:
        for file in files_list:
            print(f' file {file} is loading...')
            line_index = 0
            with open(str(file), 'r', encoding='utf8') as f:
                for line in f:
                    line_index += 1
                    add_words_to_dictionary(line, line_index, file)
    except OSError:
        print("Oops! That was no valid file. Try again...")
        return
