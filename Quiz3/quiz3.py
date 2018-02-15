lines = [line.strip() for line in open('wsj00-18.tag') if "\t" in line]
#print(lines[0:10])
wordtags = [(l.split("\t")[0],l.split("\t")[1]) for l in lines]
#print(wordtags[0:10])
#sanity check
tokens = [x[0] for x in wordtags]
#print(tokens[0:10])
#print(len(set(tokens)))
counter = 0
for word in tokens:
    if word == "the":
        counter += 1
#print(counter)
tags = [x[1] for x in wordtags]
#print(len(set(tags)))
#question 1 and qusetion 2
unique_tokens = set(list(tokens))
# tokens_to_tag = {}
# for token,tag in wordtags:
#     if token in tokens_to_tag:
#         tag_array = tokens_to_tag.get(token)
#         if tag not in tag_array:
#             tag_array.append(tag)
#         tokens_to_tag[token] = tag_array
#     else:
#         tokens_to_tag[token] = [tag]
# one_tag_counter = 0
# two_tag_counter = 0
# for key, value in tokens_to_tag.items():
#     if len(value) == 1:
#         one_tag_counter += 1
#     if len(value) == 2:
#         two_tag_counter += 1
# print("question 1", one_tag_counter)
# print("question 2", two_tag_counter)
#question 3
# the_token_tags = {}
# for token, tag in wordtags:
#     if token == "the":
#         if tag in the_token_tags:
#             the_token_tags[tag] += 1
#         else:
#             the_token_tags[tag] = 1
# most_common_the_tag = ""
# value_of_common_the_tag = 0
# for key, value in the_token_tags.items():
#     if key != "DT":
#         if value > value_of_common_the_tag:
#             value_of_common_the_tag = value
#             most_common_the_tag = key
# print("question 3", most_common_the_tag, value_of_common_the_tag)
#question 4
# this_tags = []
# for token, tag in wordtags:
#     if token == "this":
#         if tag not in this_tags:
#             this_tags.append(tag)
# print("question 4", len(this_tags))
#question 5
dt_nn_counter = 0
for i in range(len(wordtags)-1):
    current_tag,next_tag = wordtags[i][1], wordtags[i+1][1]
    if current_tag == "DT" and next_tag == "NN":
        dt_nn_counter += 1

print("question 5", dt_nn_counter)
