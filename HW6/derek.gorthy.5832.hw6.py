from collections import defaultdict
import operator
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import pickle
import random

# Returns allWords, uniqueWords
def readFileIntoArrays(filename):
    words = []
    uniqueWords = []

    f = open(filename)
    for line in f:
        word = line.split("\t")[0].lower()
        if (word != "\n"):
            words.append(word)
            if (word not in uniqueWords):
                uniqueWords.append(word)

    return words, uniqueWords

def getTop(allWords, uniqueWords, topNum):
    freqDict = defaultdict()
    for word in uniqueWords:
        freqDict[word] = 0
    for word in allWords:
        freqDict[word] += 1
    tup = []
    for key in freqDict:
        tup.append((key, freqDict[key]))
    sortedTup = sorted(tup, key=lambda x: x[1], reverse=True)

    topWords = []
    for wordTup in sortedTup[:topNum]:
        topWords.append(wordTup[0])
    return topWords

# Returns normalized context vectors for top words
def getContextVectors(allWords, uniqueWords, topWords):
    contextVectors = np.zeros((len(topWords), 2*len(uniqueWords)))
    rightShift = len(uniqueWords)
    prevWordIndex = 0
    nextWordIndex = 2

    if allWords[0] in topWords:
        contextVectors[topWords.index(allWords[0])][uniqueWords.index(allWords[1])+rightShift]

    # Iterate over every word in set
    for i in range(1, len(allWords)-1):
        word = allWords[i]
        if (word in topWords):
            contextVectors[topWords.index(word)][uniqueWords.index(allWords[prevWordIndex])] += 1
            contextVectors[topWords.index(word)][uniqueWords.index(allWords[nextWordIndex])+rightShift] += 1
        prevWordIndex += 1
        nextWordIndex += 1

    if allWords[-1] in topWords:
        contextVectors[topWords.index(allWords[-1])][uniqueWords.index(allWords[-2])]

    normalizedContextVectors = normalize(contextVectors, axis = 1, norm='l1')
    return normalizedContextVectors

def pickleFile(list, file):
    with open(file, 'wb') as f:
        pickle.dump(list, f)

def getListFromPickledFile(file):
    with open(file, 'r') as f:
        return pickle.load(f)

# sklearn implementation
def kmeans(normalizedContextVectors, k):
    km = KMeans(n_clusters=k, random_state=0).fit(normalizedContextVectors)
    return km.labels_

def printClusters(kmeansLabels, topWords, k):
    clusters = []
    for i in range(0, k):
        clusters.append(str(i)+": ")
    for i in range(0, len(kmeansLabels)):
        clusters[kmeansLabels[i]] += topWords[i] + " "
    for i in range(0, k):
        print(clusters[i])



allWordsFile = 'pickledFiles/allWords.txt'
uniqueWordsFile = 'pickledFiles/uniqueWords.txt'
topWordsFile = 'pickledFiles/topWords.txt'
normalizedContextVectorsFile = 'pickledFiles/normalizedContextVectors.txt'
topWordsNum = 1000

# Generate all lists from scratch
print("Starting...")
allWords, uniqueWords = readFileIntoArrays('wsj00-18.tag')
print("Read in file(s)...")
topWords = getTop(allWords, uniqueWords, topWordsNum)
print("Found top words...")
normalizedContextVectors = getContextVectors(allWords, uniqueWords, topWords)
print("Calculated normalized vectors...")
'''
# Pickle all lists into files
pickleFile(allWords, allWordsFile)
pickleFile(uniqueWords, uniqueWordsFile)
pickleFile(topWords, topWordsFile)
pickleFile(normalizedContextVectors, normalizedContextVectorsFile)
'''
'''
# Get arrays from pickled pickledFiles
allWords = getListFromPickledFile(allWordsFile)
uniqueWords = getListFromPickledFile(uniqueWordsFile)
topWords = getListFromPickledFile(topWordsFile)
normalizedContextVectors = getListFromPickledFile(normalizedContextVectorsFile)
'''
# Get clusters from normalized vectors
k = 25 # Number of clusters
kmeansLabels = kmeans(normalizedContextVectors, k) # Using sklearn library
print("Completed k-means clustering...")

# Print out classes
printClusters(kmeansLabels, topWords, k)
