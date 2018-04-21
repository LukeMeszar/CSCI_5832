from collections import defaultdict
from collections import OrderedDict
import numpy as np

def parse_text():
    lines = [line.strip() for line in open('wsj00-18.tag') if "\t" in line]

    words = [l.split("\t")[0].lower() for l in lines]
    punctuation = [".", ",", ";", "\"", "'"]
    words_without_punc = []
    for word in words:
        if word not in punctuation:
            words_without_punc.append(word)
    unique_words = list(set(words_without_punc))
    return words_without_punc, unique_words
def get_top_1000(words):
    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1
    ordered_word_count = OrderedDict(sorted(word_count.items(), key=lambda t: -t[1]))
    top_tuple = list(ordered_word_count.items())[0:1000]
    return [x[0] for x in top_tuple]

def create_left_right_vecs(words, unique_words, top_words):
    left_vec  = [ [0]*len(unique_words) ]*len(top_words)
    right_vec = [ [0]*len(unique_words) ]*len(top_words)
    for i in range(len(words)):
        current_word = words[i]
        if current_word in top_words:
            left_word = words[i-1]
            right_word = words[i+1 % len(words)]
            left_vec[top_words.index(current_word)][unique_words.index(left_word)] += 1
            right_vec[top_words.index(current_word)][unique_words.index(right_word)] += 1
    return left_vec, right_vec


if __name__ == '__main__':
    words, unique_words = parse_text()
    top_words = get_top_1000(words)
    left_vec, right_vec = create_left_right_vecs(words, unique_words, top_words)
    for row in left_vec:
        for entry in row:
            if entry != 0:
                print(entry)
