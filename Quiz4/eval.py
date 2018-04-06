lines_tag = [line.strip() for line in open('wsj22-24.tag') if "\t" in line]
wordtags_tag = [(l.split("\t")[0],l.split("\t")[1]) for l in lines_tag]
lines_guess = [line.strip() for line in open('wsj22-24.guess') if "\t" in line]
wordtags_guess = [(l.split("\t")[0],l.split("\t")[1]) for l in lines_guess]
correct_counter = 0
for i in range(len(wordtags_guess)):
    if wordtags_guess[i][1] == wordtags_tag[i][1]:
        correct_counter += 1
print(correct_counter/len(wordtags_guess))
