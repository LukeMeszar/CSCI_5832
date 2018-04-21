# Jack Dinkel
# NLP HW6
# NOTE: This is meant to be run with Python3

from collections import defaultdict
from collections import OrderedDict
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans


num_words = 1000
training_size = float("inf")
k = 25

word_dict   = defaultdict(int)
train_words = []

iters = 0
for line in open('wsj00-18.tag'):
    word = line.strip().split("\t")[0].lower()
    word_dict[word] += 1
    train_words.append(word)
    iters += 1
    if iters >= training_size:
        break

print("train words", len(train_words))

unique_train_words = list(OrderedDict.fromkeys(train_words))
top_words = [ key for key, value in sorted(word_dict.items(), key=(lambda t:-t[1])) ][:num_words]
print("unique_words", len(unique_train_words))

left_vectors  = [ [0]*len(unique_train_words) ]*num_words
right_vectors = [ [0]*len(unique_train_words) ]*num_words
print(len(left_vectors), len(left_vectors[0]))

print("building vectors")

for itr in range(len(train_words)):
    word  = train_words[itr]
    left  = train_words[itr-1]
    right = train_words[(itr+1) % len(unique_train_words)]

    # We only care if the word is in the top 1000
    if word in top_words:
        left_vectors[top_words.index(word)][unique_train_words.index(left)] += 1
        #print()
        #print(unique_train_words.index(left))
        #print(unique_train_words.index(right))
        #print(unique_train_words.index(right)+len(unique_train_words))
        right_vectors[top_words.index(word)][unique_train_words.index(right)] += 1

print(left_vectors)
print(right_vectors)

print("concatenating vectors")
vectors = []
for itr in range(len(left_vectors)):
    vectors.append(left_vectors[itr] + right_vectors[itr])

print("normalizing vectors")
# Normalize vectors
normalized_vectors = normalize(np.array(vectors), axis=1, norm='l1')
print("normalized_vectors", normalized_vectors.shape)

print("kmeans")
# Cluster using k-means
kmeans = KMeans(n_clusters=k, random_state=0).fit(normalized_vectors)
print(kmeans.labels_)

#kmeans = KMeans(n_clusters = 2, random_state=0).fit([[0,0],[1,1],[100,100],[100,101]])
#print(kmeans.labels_)
