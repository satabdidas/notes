# index_git_notes_01.py
'''Creates simple index of .md file-names and headers within those files, in a
Git repository.'''

import os
import hashlib
import re
import pprint
import json
import nltk

top_dir_path = os.path.join('', 'notes')
list_of_dirs = []
list_of_files = []
list_of_lines = []
hash_start_ptrn = re.compile('^#+')
hash_all_ptrn = re.compile('^#+$')
hash_end_prtn = re.compile('#+$')
equals_all_ptrn = re.compile('^=+$')
hyphens_all_ptrn = re.compile('^-+$')
word_dividers_ptrn = re.compile('''-|/''')
# Do not strip back-ticks until word has been accepted.
to_be_stripped = re.compile(''''|"|,''')
not_unwanted_words = [
        'set-up', 'key-bindings', 'OS_X'
        ]
unwanted_words = [
        'be', 'go',
        ]

treebank_to_wordnet_dict = {
        'J': nltk.wordnet.wordnet.ADJ, 
        'R' : nltk.wordnet.wordnet.ADV, 
        'N' : nltk.wordnet.wordnet.NOUN, 
        'V' : nltk.wordnet.wordnet.VERB,
        }

def generate_headword(word, treebank_POS, wnl_obj):
    if treebank_POS[0] not in treebank_to_wordnet_dict:
        return ''
    else:
        return wnl_obj.lemmatize(word,
                treebank_to_wordnet_dict[treebank_POS[0]])

def add_f_to_list(top_dir_path = top_dir_path):
    for f in os.listdir(top_dir_path):
        if f[0] == '.':
            continue
        the_path = os.path.join(top_dir_path, f)
        if os.path.isdir(the_path):
            list_of_dirs.append(the_path)
            add_f_to_list(the_path)
        else:
            list_of_files.append(the_path)
    return list_of_files, list_of_dirs

def make_dirname_into_string(dirname):
    dirname = os.path.split(dirname)[-1]
    if dirname in not_unwanted_words:
        return dirname
    return dirname.replace('_', ' ').strip()

def make_filename_into_string(filename):
    filename = os.path.split(filename)[-1]
    filename_parts = filename.split('.')
    filename, extension = filename_parts[0], filename_parts[-1]
    if not extension:
        return
    filename = filename.replace('_', ' ').strip()
    return filename
    return filename.replace('_', ' ').strip()

def list_all_words(the_string, wnl_obj):
    the_string = the_string.lower()
    the_string = the_string.replace('"', '').replace('.', '')
    tokenized_words = nltk.word_tokenize(the_string)
    words_to_divide = []
    words_not_to_divide = []
    words_to_report = []
    tagged_words = nltk.pos_tag(tokenized_words)
    for word, treebank_POS in tagged_words:
        if (word[0] == '`' == word[-1]) or (word in not_unwanted_words):
            word = word.replace('`', '')
            words_not_to_divide.append(word)
        else:
            words_to_divide.append((word, treebank_POS))
    # delete unwanted words
    for word, treebank_POS in words_to_divide:
        word = generate_headword(word, treebank_POS, wnl_obj)
        if (not word) or (word in unwanted_words):
            continue
        word = re.sub(to_be_stripped, '', word)
        if re.search(word_dividers_ptrn, word):
            words_to_report.extend(re.split(word_dividers_ptrn, word))
        else:
            words_to_report.append(word)
    for word in words_not_to_divide:
        words_to_report.append(word)
    return words_to_report

def list_lines(path):
    with open(path) as f:
        return f.read().split('\n')

def find_headers(list_of_lines):
    header_lines = []
    # distinguish setext (underlined) and atx (#s at line-start) formats
    for line, next_line in zip(list_of_lines, list_of_lines[1:]):
        # First find atx headers
        # Lines that have no other content than # are ignored in MD but must 
        # be eliminated here.
        if (re.search(hash_start_ptrn, line) and not 
                re.search(hash_all_ptrn, line)):
            # Strip any initial or final hashes
            line = re.sub(hash_start_ptrn, '', line)
            line = re.sub(hash_end_prtn, '', line)
            header_lines.append(line.strip())
        # Next find setext headers
        elif (re.search(equals_all_ptrn, next_line) or 
                re.search(hyphens_all_ptrn, next_line)):
            header_lines.append(line)
    return header_lines

def add_string_to_dict(dictionary, the_string, the_file):
    dictionary[the_string.__hash__()] = (the_string, the_file)
    return dictionary

def main():
    index_entries = []
    string_and_path_lookup = {}
    tuple_storage = {}
    list_of_files, list_of_dirs = add_f_to_list()
    wnl_obj = nltk.stem.WordNetLemmatizer()
    # First create hash-based dictionary of string-path tuples; then index the
    # words in the strings of that dictionary. The purpose of the dictionary is
    # to thin the main redundancies - filenames that reappear in one of the
    # headers within them.
    for the_dir in list_of_dirs:
        # Process directory name
        the_string = make_dirname_into_string(the_dir)
        dir_tuple = ('dir', the_dir, the_string)
        tuple_storage[dir_tuple.__hash__()] = dir_tuple
        string_and_path_lookup = add_string_to_dict(
                string_and_path_lookup, the_string, the_dir)
        words = list_all_words(the_string, wnl_obj)
        # Index words and path
        for word in words:
            index_entries.append((word, dir_tuple.__hash__()))
    for the_file in list_of_files:
        # Process file name
        the_string = make_filename_into_string(the_file)
        if the_string:
            file_tuple = ('file', the_file, the_string)
            tuple_storage[file_tuple.__hash__()] = file_tuple
            string_and_path_lookup = add_string_to_dict(
                    string_and_path_lookup, the_string, the_file)
            words = list_all_words(the_string, wnl_obj)
            # index words and path
            for word in words:
                index_entries.append((word, file_tuple.__hash__()))
        # Process headers
        header_lines = find_headers(list_lines(the_file))
        for line in header_lines:
            string_and_path_lookup = add_string_to_dict(
                    string_and_path_lookup, line, the_file)
            header_tuple = ('header', the_file, line)
            tuple_storage[header_tuple.__hash__()] = header_tuple
            words = list_all_words(line, wnl_obj)
            # index words and path and line
            for word in words:
                index_entries.append((word, header_tuple.__hash__()))
    index_entries = list(set(index_entries))
    index_entries.sort()
    for word, the_hash in index_entries:
        print '\n', word, tuple_storage[the_hash]
#    pprint.pprint(index_entries)
    pprint.pprint(string_and_path_lookup)
