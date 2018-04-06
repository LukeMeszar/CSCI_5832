from sklearn.feature_extraction import DictVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.svm import LinearSVC

def readconll(file):
    #Professor Mulden's code
    lines = [line.strip() for line in open(file)]
    lines.pop(0)
    lines.pop(0)
    while lines[-1] == '':  # Remove trailing empty lines
        lines.pop()
    s = [x.split('_') for x in '_'.join(lines).split('__')]  # Quick split corpus into sentences
    return [[y.split() for y in x] for x in s]

def create_features(sentences):
    feature_vector = []
    #loop through ever sentence/word and create a feature dict for each word
    for sentence in sentences:
        featurized_first_word = featurize_word(sentence[0])
        feature_vector.append(featurized_first_word)
        for word_index in range(1,len(sentence)):
            current_word = sentence[word_index]
            prev_word = sentence[word_index-1]
            featurized_word = featurize_word(current_word, prev_word)
            feature_vector.append(featurized_word)
    return feature_vector

def transform_features(training_features,testing_features):
    #need to use same vectorizer object for both training and testing
    #to get same number of features
    vectorizer = DictVectorizer(sparse=True)
    return vectorizer.fit_transform(training_features), \
    vectorizer.transform(testing_features)



def get_labels(sentences):
    #creates y data
    label_vector = []
    for sentence in sentences:
        for word in sentence:
            #get Named Entity Tag NET
            NET = word[3]
            label_vector.append(NET)
    return label_vector

def featurize_word(word_vec,prev_word_vec=None):
    feature_dict = {}
    word, POS = word_vec[0], word_vec[1]
    feature_dict = {}
    #current word feature
    feature_dict['word='+word] = 1
    #current word POS feature
    feature_dict['POS='+POS] = 1
    #get features for suffixes for last 4 letters if the length is sufficient
    for suff_len in range(1,5):
        if len(word) >= suff_len:
            suff = word[-suff_len:]
            feature_dict['suff'+str(suff_len)+'='+suff] = 1
        else:
            feature_dict['suff'+str(suff_len)+'= '] = 1

    if prev_word_vec != None:
        prev_word, prev_POS = prev_word_vec[0], prev_word_vec[1]
        #features based on prev word and POS
        feature_dict['prev_word='+prev_word] = 1
        feature_dict['prev_POS='+prev_POS] = 1
        #check if capitalized
        if word[0].isupper():
            feature_dict['init_caps_in_sentence=TRUE'] = 1
        else:
            feature_dict['init_caps_in_sentence=FALSE'] = 1
        #check if prev word is capitalized
        if prev_word[0].isupper():
            feature_dict['prev_word_init_caps_in_sentence=TRUE'] = 1
        else:
            feature_dict['prev_word_init_caps_in_sentence=FALSE'] = 1

    else:
        #set unique features for start of sentence words
        feature_dict['prev_word=<s>'] = 1
        feature_dict['prev_POS=#'] = 1
        #captilization for first word doesn't really matter
        feature_dict['init_caps_first_word='+word] = 1
    return feature_dict


def svm(x_train,y_train, x_test, y_test, testing_sentences):
    #train model
    clf = LinearSVC()
    clf.fit(x_train,y_train)
    flattened_sentence = [item for sublist in testing_sentences for item in sublist]
    #get a prediction for each word in the test set
    for index, x in enumerate(x_test):
        prediction = clf.predict(x)
        flattened_sentence[index].append(prediction[0])
    return flattened_sentence

def write_predictions_to_file(predictions, test_set_flag):
    #add back header line
    header = ['-DOCSTART- -X- O O O', ' ']
    string_item_list = []
    for item in predictions:
        new_string = ""
        for part in item:
            new_string += part+" "
        #remove trailing whitespace
        new_string[:-1]
        string_item_list.append(new_string)
    full_file = header + string_item_list
    thefile = open('eng.guess'+test_set_flag, 'w')
    for item in full_file:
        thefile.write("%s\n" % item)

if __name__ == '__main__':
    training_setences = readconll('eng.train')
    testing_sentences = readconll('eng.testa')
    train_feat = create_features(training_setences)
    y_train = get_labels(training_setences)
    test_feat = create_features(testing_sentences)
    x_train, x_test = transform_features(train_feat, test_feat)
    y_test  = get_labels(testing_sentences)
    predictions = svm(x_train, y_train, x_test, y_test, testing_sentences)
    write_predictions_to_file(predictions,'a')
