import numpy as np

def classify(f, w):
    classscores = {c:(f.dot(w[c])) for c in range(len(w))}
    return max(classscores, key = classscores.get)

f = np.array([[1,0,1,0,1],[1,1,0,0,0],[1,0,0,1,1],[1,0,1,1,1]]) # 4 examples
classes = np.array([0,1,1,0]) # which belong to these classes
traindata = zip(classes, f)   # zip them up for easier looping
w = np.zeros((2,5))           # initialize two weight vectors of length 5

### Your code here
### 1. Loop over each example until you do a complete run through all examples without error
### 2. Classify the example
### 3. If correct, do nothing
### 4. If incorrect  subtract featurevector from incorrect class vector
###                       add featurevector to   correct   class vector
### (print out number of errors made during each iteration to see that the classifier improves)
perfect = False
iteration = 1
while not perfect:
    num_correct = 0
    for i in range(4):
        x,y = f[i], classes[i]
        yprime = classify(x,w)
        if y != yprime:
            w[yprime] = w[yprime] - x
            w[y] = w[y] + x
        else:
            num_correct += 1
    print("iteration", iteration, "num_correct", num_correct)
    iteration += 1
    if num_correct == 4:
        perfect = True


print(classify(f[0],w))
print(classify(f[1],w))
print(classify(f[2],w))
print(classify(f[3],w))

print(w[0])
print(w[1])
