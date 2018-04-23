from collections import defaultdict
from collections import OrderedDict
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

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
    right_shift = len(unique_words)
    combined_vectors = np.zeros((len(top_words),2*len(unique_words)))
    print("creating vectors")
    for i in range(len(words)):
        current_word = words[i]
        left_word = words[i-1]
        right_word = words[(i+1) % len(words)]
        if current_word in top_words:
            if i % 10000 == 0:
                print(i)
            combined_vectors[top_words.index(current_word)][unique_words.index(left_word)] += 1
            combined_vectors[top_words.index(current_word)][unique_words.index(right_word)+right_shift] += 1
    return combined_vectors

def normalize_and_fit(vectors, k):
    print("normalizing")
    normalized_vectors = normalize(np.array(vectors), axis=1, norm='l1')
    print("kmeans")
    kmeans = KMeans(n_clusters=k, random_state=0).fit(normalized_vectors)
    return kmeans.labels_

def print_labels(labels, top_words, k):
    clusters = []
    for i in range(0, k):
        clusters.append("Cluster" + str(i)+": ")
    for i in range(0, len(labels)):
        clusters[labels[i]] += top_words[i] + " "
    for i in range(0, k):
        print(clusters[i])

if __name__ == '__main__':
    k=25
    words, unique_words = parse_text()
    top_words = get_top_1000(words)
    vectors = create_left_right_vecs(words, unique_words, top_words)
    labels = normalize_and_fit(vectors,k)
    print_labels(labels, top_words, k)
