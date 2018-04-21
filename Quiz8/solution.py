from math import sqrt # You may need this function
import numpy as np
# Some made-up toy word vectors
vec = {}
vec['man'] = [1,2,3,4,5]
vec['woman'] = [6,7,8,9,10]
vec['king'] = [-5,-4,-3,-2,-1]
vec['queen'] = [0,1,2,3,4]
vec['dog'] = [-10.2,-3.2,-2.3,-4.3,3.1]
vec['cat'] = [-8.3,-3.01,-2.0,-1.3,1.1]
vec['rabbit'] = [-5.2,-2.1,-4.3,1.0,2.0]
vec['squirrel'] = [2.9,0.1,0.3,2.0,1.5]

def sim(x,y):
    return (np.dot(x,y))/(sqrt(sum([xi**2 for xi in x]))*sqrt(sum([yi**2 for yi in y])))


def find_closest(word, vec):
    max_score = 0
    target_word_vec = vec[word]
    best_word = ""
    for current_word, current_vec in vec.items():
        if word != current_word:
            current_score = sim(target_word_vec, current_vec)
            if current_score > max_score:
                max_score = current_score
                best_word = current_word
    return best_word

def analogy(a,b,c, vec):
    a_vec = np.array(vec[a])
    b_vec = np.array(vec[b])
    c_vec = np.array(vec[c])
    max_score = 0
    best_word = ""
    for current_word, current_vec in vec.items():
        if current_word not in [a,b,c]:
            current_score = sim(current_vec, b_vec - a_vec + c_vec)
            if current_score > max_score:
                max_score = current_score
                best_word = current_word

    return best_word
# Now implement three functions:
# 1. sim()
# 2. find_closest()
# 3. analogy()
#
# Run the following:
#print(sim(vec['cat'], vec['squirrel'])) #< sanity check, should be -0.7324574388673762
print(sim(vec['cat'], vec['dog']))

#print(find_closest('rabbit', vec)) # < sanity check, should be "cat"
print(find_closest('cat', vec))
print(find_closest('king', vec))

#print(analogy('man','woman','king', vec)) #< sanity check, should be "queen"
print(analogy('squirrel','rabbit','dog', vec))
