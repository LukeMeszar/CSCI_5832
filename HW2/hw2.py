from math import log
from math import inf
#constants
delta = 1
size_of_vocabulary = 32

def calculate_probs(filename):
    letter_array = []
    with open(filename) as fileobj:
        for line in fileobj:
            for ch in line:
                if ch != "\n":
                    letter_array.append(ch)
    count_list_bigram = {}
    count_list_unigram = {}
    alphabet = []
    #get a count for all bigrams we see in the text and unigrams in the text
    #create alphabet for particular language
    for i in range(len(letter_array)-1):
        first_letter, second_letter = letter_array[i], letter_array[i+1]
        bigram = first_letter + second_letter
        if first_letter not in alphabet:
            alphabet.append(first_letter)
        if first_letter in count_list_unigram:
            count_list_unigram[first_letter] += 1
        else:
            count_list_unigram[first_letter] = 1
        if bigram in count_list_bigram:
            count_list_bigram[bigram] += 1
        else:
            count_list_bigram[bigram] = 1
    #add count for last letter in text due to off by one error
    if letter_array[-1] in count_list_unigram:
        count_list_unigram[letter_array[-1]] += 1
    else:
        count_list_unigram[letter_array[-1]] = 1
    #create pseudocounts for all possible bigrams given an alphabet that were
    #not seen in the text
    for letter1 in alphabet:
        for letter2 in alphabet:
            bigram = letter1+letter2
            if bigram not in count_list_bigram:
                #note we dont need the count(li-1 li) term since we know it will
                #be 0
                count_list_bigram[bigram] = \
                delta/(count_list_unigram[letter1]+delta*size_of_vocabulary)


    bigram_probs = {}
    #calculate the log prob p(li|li-1, class) for each bigram
    for bigram in count_list_bigram:
        bigram_probs[bigram] = log((count_list_bigram[bigram] + delta)/(\
        count_list_unigram[bigram[0]]+delta*size_of_vocabulary))
    return bigram_probs

def classify(text_input, probs):
    classifications = {}
    for language in probs:
        current_probs = probs[language]
        log_prob_classification = 0
        for i in range(len(text_input)-1):
            first_letter, second_letter = text_input[i], text_input[i+1]
            bigram = first_letter + second_letter
            #sets 0 if bigram can't be in a language since it contains a letter
            #not in the language
            log_prob_classification += current_probs.get(bigram,0)
        classifications[language] = log_prob_classification
    max_score = -inf
    best_language = ""
    #find most probable language
    for language, prob in classifications.items():
        if prob > max_score:
            max_score = prob
            best_language = language
    return best_language, classifications

if __name__ == '__main__':
    de_probs  = calculate_probs("de")
    en_probs = calculate_probs("en")
    nl_probs = calculate_probs("nl")
    sv_probs = calculate_probs("sv")
    all_probs = {"de": de_probs, "en": en_probs, "nl": nl_probs, "sv": sv_probs}
    text_input_en = "this is a very short text"
    text_input_de = "dies ist ein sehr kurzer text"
    text_input_nl = "dit is een zeer korte tekst"
    text_input_sv = "detta är en mycket kort text"
    print(classify(text_input_en, all_probs))
    print(classify(text_input_de, all_probs))
    print(classify(text_input_nl, all_probs))
    print(classify(text_input_sv, all_probs))
