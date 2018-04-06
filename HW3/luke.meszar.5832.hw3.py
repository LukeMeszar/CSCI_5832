#CSCI 5832 Homework 3
#Luke Meszar
#Run with python 3

import numpy as np
def parse_text():
    lines  = [line.strip() for line in open('wsj00-18.tag')]
    wordtags = [(lines[0].split("\t")[0],'<s>')]
    for i in range(len(lines)-1):
        line = lines[i]
        if "\t" in line:
            wordtags.append((line.split("\t")[0],line.split("\t")[1]))
        else:
            #keep track of where sentences end and add beginning and end markers
            wordtags.append( (lines[i-1].split("\t")[0],'</s>') )
            wordtags.append( (lines[i+1].split("\t")[0],'<s>') )
    sentences = []
    wordtags.append( (lines[-2].split("\t")[0],'</s>'))
    tags = [x[1] for x in wordtags]
    return wordtags, tags

def compute_tag_MLE(tags):
    single_tag_counts = {}
    tag_pair_counts = {}
    tag_probabilities = {}
    #get counts for all single tags and tag pairs
    for i in range(len(tags)-1):
        first_tag, second_tag = tags[i], tags[i+1]
        tag_pair = first_tag + "|" + second_tag
        if first_tag in single_tag_counts:
            single_tag_counts[first_tag] += 1
        else:
            single_tag_counts[first_tag] = 1
        if tag_pair in tag_pair_counts:
            tag_pair_counts[tag_pair] += 1
        else:
            tag_pair_counts[tag_pair] = 1
    #account for last tag
    if tags[-1] in single_tag_counts:
        single_tag_counts[tags[-1]] += 1
    else:
        single_tag_counts[tags[-1]] = 1
    #compute tag pair probability without smoothing
    for tag_pair in tag_pair_counts:
        tag_probabilities[tag_pair] = tag_pair_counts[tag_pair]/single_tag_counts[tag_pair.split("|")[0]]
    tag_list = list(single_tag_counts)
    #make sure </s> is at the end of the list for convienence
    tag_list.remove("</s>")
    tag_list.append("</s>")
    return tag_probabilities, tag_list

def compute_word_tag_MLE(wordtags):
    tag_counts = {}
    word_tag_counts = {}
    word_tag_probabilities = {}
    #get counts for each tag and wordtag pair
    for wordtag in wordtags:
        tag = wordtag[1]
        if wordtag in word_tag_counts:
            word_tag_counts[wordtag] += 1
        else:
            word_tag_counts[wordtag] = 1
        if tag in tag_counts:
            tag_counts[tag] += 1
        else:
            tag_counts[tag] = 1
    #compute wordtag probabilities without smoothing
    for wordtag in word_tag_counts:
        word_tag_probabilities[wordtag] = word_tag_counts[wordtag]/tag_counts[wordtag[1]]
    return word_tag_probabilities

def viterbi(sentence, transition_probs, emission_probs, tag_list):
    num_tags = len(tag_list)
    viterbi_array = np.zeros((num_tags,len(sentence)+2))
    viterbi_array[0,0] = 1 #set start position probability
    backpointer = np.zeros((num_tags,len(sentence)+2))
    sentence_length = len(sentence)
    #initialization step
    for state in range(1,num_tags-1):
        viterbi_array[state][1] = transition_probs.get("<s>|" + tag_list[state],0)*emission_probs.get((sentence[0],tag_list[state]),0)
        backpointer[state][1] = 0
    #dynamic programming part
    for time in range(2, sentence_length+1):
        for state in range(1,num_tags-1):
            max_prob = 0
            max_prob_index = 0
            #get max probability
            for tag_index in range(1,len(tag_list)):
                current_prob = viterbi_array[tag_index,time-1]*\
                transition_probs.get(tag_list[tag_index]+"|"+tag_list[state],0)\
                *emission_probs.get((sentence[time-1],tag_list[state]),0)
                if current_prob > max_prob:
                    max_prob = current_prob
                    max_prob_index = tag_index
            viterbi_array[state][time] = max_prob
            backpointer[state][time] = max_prob_index
    max_prob = 0
    max_prob_index = 0
    #termination step
    for state in range(1,num_tags-1):
        current_prob = viterbi_array[state][sentence_length]*transition_probs.get(tag_list[state] + "|</s>",0)
        if current_prob > max_prob:
            max_prob = current_prob
            max_prob_index = state
    viterbi_array[num_tags-1][sentence_length+1] = max_prob
    backpointer[num_tags-1][sentence_length+1] = max_prob_index
    pointer = int(backpointer[num_tags-1][sentence_length+1])
    #have to subtract 1 from pointer since the max index was found with an
    #off by one error
    path = [pointer-1]
    #travel backwords through an array
    for time in reversed(range(sentence_length+1)):
        pointer = int(backpointer[pointer][time])
        path.append(pointer-1)
    #turn path around so it is read from left to right
    path.reverse()
    #remove first two elements that correspond to the start of sentence tags
    path = path[2:]
    #convert tag indexes into tag names
    predicted_tags = list(map(lambda x: tag_list[x+1],path))
    return predicted_tags
if __name__ == '__main__':
    wordtags, tags = parse_text()
    tag_MLE, tag_list = compute_tag_MLE(tags)
    word_tag_MLE = compute_word_tag_MLE(wordtags)
    print(viterbi(['This','is','a','sentence','.'], tag_MLE, word_tag_MLE,tag_list))
    print(viterbi(['This','might','produce','a','result','if','the','system','works','well','.'], tag_MLE, word_tag_MLE,tag_list))
    print(viterbi(['Can','a','can','can','a','can','?'], tag_MLE, word_tag_MLE,tag_list))
    print(viterbi(['Can','a','can','move','a','can','?'], tag_MLE, word_tag_MLE,tag_list))
    print(viterbi(['Can','you','walk','the','walk','and','talk','the','talk','?'], tag_MLE, word_tag_MLE,tag_list))
