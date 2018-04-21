lines = [line.strip() for line in open('wsj00-18.tag') if "\t" in line]
wordtags = [(l.split("\t")[0],l.split("\t")[1]) for l in lines]
print(wordtags[0:10])
