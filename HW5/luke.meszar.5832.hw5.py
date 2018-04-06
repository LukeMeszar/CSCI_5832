import numpy as np
import itertools

grammar = {
    ('S','NP','VP'):0.9,
    ('S','VP'):0.1,
    ('VP','V','NP'):0.5,
    ('VP','V'):0.1,
    ('VP','V','@VP_V'):0.3,
    ('VP','V','PP'):0.1,
    ('@VP_V','NP','PP'):1.0,
    ('NP','NP','NP'):0.1,
    ('NP','NP','PP'):0.2,
    ('NP','N'):0.7,
    ('PP','P','NP'):1.0,
    ('N','people'):0.5,
    ('N','fish'):0.2,
    ('N','tanks'):0.2,
    ('N','rods'):0.1,
    ('V','people'):0.1,
    ('V','fish'):0.6,
    ('V','tanks'):0.3,
    ('P','with'):1.0
}
def get_nonterms(grammar):
    nonterms = []
    for rule in grammar:
        if rule[0] not in nonterms:
            nonterms.append(rule[0])
    return nonterms

def CKY(words, grammar, nonterms):
    num_words = len(words)
    score = np.zeros((num_words+1,num_words+1,len(nonterms)))
    for index in range(num_words):
        for A in nonterms:
            rule = (A, words[index])
            if rule in grammar:
                score[index,index+1,nonterms.index(A)] = grammar.get(rule,0)
        added = True
        while added:
            added = False
            for element in itertools.product(nonterms,nonterms):
                A,B = element[0], element[1]
                A_index,B_index = nonterms.index(A), nonterms.index(B)
                rule = (A,B)
                if score[index,index+1,B_index] > 0 and rule in grammar:
                    prob = grammar.get(rule,0)*score[index, index+1, B_index]
                    if (prob >  score[index, index+1, A_index]):
                         score[index, index+1, A_index] = prob
                         added = True
    # print(score)
    for span in range(2, num_words+1):
        for begin in range(0,num_words-span+1):
            end = begin + span
            for split in range(begin+1,end):
                for element in itertools.product(nonterms, nonterms,nonterms):
                    A,B,C = element[0], element[1], element[2]
                    A_index,B_index,C_index = nonterms.index(A), \
                    nonterms.index(B), nonterms.index(C)
                    prob = score[begin, split, B_index]*score[split,end, C_index]\
                    *grammar.get((A,B,C), 0)
                    if prob > score[begin,end,A_index]:
                        score[begin,end,A_index] = prob

                added = True
                while added:
                    added = False
                    for element in itertools.product(nonterms,nonterms):
                        A,B = element[0], element[1]
                        A_index,B_index = nonterms.index(A), nonterms.index(B)
                        prob = grammar.get((A,B), 0)*score[begin,end,B_index]
                        if prob > score[begin,end,A_index]:
                            score[begin,end,A_index] = prob
                            added = True
    return (score[0,num_words,nonterms.index('S')])



if __name__ == '__main__':
    nonterms = get_nonterms(grammar)
    print(CKY(['fish','people','fish','tanks'], grammar, nonterms))
    print(CKY(['people','with','fish','rods','fish','people'], grammar, nonterms))
    print(CKY(['fish','with','fish','fish'], grammar, nonterms))
    print(CKY(['fish','with','tanks','people','fish'], grammar, nonterms))
    print(CKY(['fish','people','with','tanks','fish','people','with','tanks'], grammar, nonterms))
    print(CKY(['fish','fish','fish','fish','fish'], grammar, nonterms))
    print(CKY(['rods','rods','rods','rods'], grammar, nonterms))
