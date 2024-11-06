from collections import defaultdict
import os
import string
import argparse

from ascii_graph import Pyasciigraph
from ascii_graph import colors

import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable

parser = argparse.ArgumentParser()
parser.add_argument('filenames', nargs='*', help='The file to read')
parser.add_argument('--limit', '-l', type=int, default=10, help='Limit the number of words in histogram')
parser.add_argument('--min-word-len', '-m', type=int, default=0, help='Minimum word length')
parser.add_argument('--ex-words', '-e', nargs='+', default=[], help='Exclude words')
parser.add_argument('--ex-char-series', '-c', nargs='+', default=[], help='Exclude character series in words')
parser.add_argument('--in-char-series', '-i', nargs='+', default=[], help='Include character series in words')
parser.add_argument('--directory', '-d', help='Directory to process')
args = parser.parse_args()

def count_words_in_file(file_path):
    word_count = defaultdict(int)
    
    with open(file_path, 'r') as file:
        translation = str.maketrans('', '', string.punctuation)
        for line in file:
            # Remove punctuation
            line = line.translate(translation)
            words = line.split()
            for word in words:
                word_count[word.lower()] += 1
                
    return word_count

def filter_word_count(word_count, min_word_len, ex_words, ex_char_series, in_char_series):
    filtered_word_count = defaultdict(int)
    
    for word, count in word_count.items():
        if len(word) < min_word_len:
            continue
        if word in ex_words:
            continue
        if any(series in word for series in ex_char_series):
            continue
        if not all(series in word for series in in_char_series):
            continue
        filtered_word_count[word] = count
        
    return filtered_word_count

def print_histogram(title, word_count, limit):
    word_count = list(sorted(word_count.items(), key=lambda x: x[1], reverse=True))[:limit]
    col_arr = [
        colors.BCya,
        colors.IYel,
    ]
    word_count = [(wc[0], wc[1], col_arr[i%len(col_arr)]) for i, wc in enumerate(word_count)]
    graph = Pyasciigraph()
    for line in graph.graph(title, word_count):
        print(line)

def get_text_files_from_directory(directory):
    files = []
    
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            files.append(os.path.join(directory, file))
            
    return files

if args.directory:
    files = get_text_files_from_directory(args.directory)
    for file in files:
        word_count = count_words_in_file(file)
        filtered_word_count = filter_word_count(word_count, args.min_word_len, args.ex_words, args.ex_char_series, args.in_char_series)
        print_histogram('Word count: ' + file, filtered_word_count, args.limit)

for file in args.filenames:
    word_count = count_words_in_file(file)
    filtered_word_count = filter_word_count(word_count, args.min_word_len, args.ex_words, args.ex_char_series, args.in_char_series)
    print_histogram('Word count: ' + file, filtered_word_count, args.limit)
