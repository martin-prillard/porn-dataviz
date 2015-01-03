__author__ = 'martin'
"""
Convert a csv matrix file to json file
"""

import pandas as pd
import json
import io
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import defaultdict
import sklearn
import pylab as pl
import pandas as pd
import numpy as np

# NLTK
wnl = WordNetLemmatizer()
not_words_stops=set(stopwords.words('english'))
not_words_stops.update(set(stopwords.words('portuguese')))
not_words_stops.update(set(stopwords.words('french')))
not_words_stops.update(set(stopwords.words('german')))
not_words_stops.update(set(stopwords.words('dutch')))
not_words_stops.update(set(stopwords.words('dutch')))
not_words_stops.update(set(stopwords.words('italian')))
not_words_stops.update(set(stopwords.words('russian')))
not_words_stops.update(set(stopwords.words('swedish')))
not_words_stops.update(set(stopwords.words('danish')))

# read csv
link_xhamster_csv_path = "../../dataset/original/xhamster/link_xhamster.csv"
link_xnxx_csv_path = "../../dataset/original/xnxx/link_xnxx.csv"
# generated file
link_json_path = "../../dataset/generated/original/link_xhamster.json"

data_xhamster = pd.read_csv(link_xhamster_csv_path, sep=",",encoding="utf-8", index_col=0)
data_xnxx = pd.read_csv(link_xnxx_csv_path, sep=",",encoding="utf-8", index_col=0)

# clean data
data_xhamster = pd.DataFrame(data_xhamster.fillna(0))
data_xnxx = pd.DataFrame(data_xnxx.fillna(0))

# get the tags name
tags_xhamster = list(data_xhamster[:0])
tags_xnxx = list(data_xnxx[:0])


# get the maximum matrix value
max_value = 0
for tag_source in tags_xhamster:
    for tag_target in tags_xhamster:
        if data_xhamster[tag_source][tag_target] >= max_value:
            max_value = data_xhamster[tag_source][tag_target]

# get matrix values
strenghs = []
for tag_source in tags_xhamster:
    for tag_target in tags_xhamster:
        strengh = []
        strengh.append(tags_xhamster.index(tag_source))
        strengh.append(tags_xhamster.index(tag_target))
        value = data_xhamster[tag_source][tag_target]

        # transform - 1 value to 0
        value = (value + 1) / max_value * 200

        # gephi edges file
        #if ((tags_xhamster.index(tag_source) != tags_xhamster.index(tag_target)) and value > 0):
        #    print str(tags_xhamster.index(tag_source)) + ';' + str(tags_xhamster.index(tag_target)) + ';Undirected;' + str(value)

        strengh.append(value)
        strenghs.append(strengh)

# create the JSON file
with io.open(link_json_path, 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps({"nodes": [{'tags':tag, 'group':1} for tag in tags_xhamster],"links": [{'source':strengh[0], 'target':strengh[1], 'value':strengh[2]} for strengh in strenghs]}, ensure_ascii=False)))








#TODO test martin
"""
# test if the word is plural
def is_plural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural
# get the singular value
def get_singular(word):
    return wnl.lemmatize(word, 'n')

def clean_word(word):
    word_cases = []
    # lower case
    word = str(word).lower()
    # remove common words and tokenize
    #word = str(filter(lambda w: not w in not_words_stops,word.split())) TODO
    # remove all space
    word = ''.join(word.split())
    pattern = re.compile(r'\s+')
    word = re.sub(pattern, '', word)
    word = word.replace(' ', '')
    # singular
    if (is_plural(word)):
        word = get_singular(word)
    return word

def test_similar_words(word1, word2):
    similar = False
    # test if they are similar
    if ((str(word1) == str(word2))):
        similar = True
    return similar

# merge xhamster tags and xnxx tags
tags_merged = defaultdict(list)
for tag in tags_xhamster:
    tag_cleaned = str(clean_word(tag))
    tags_merged[str(tag_cleaned)].append(str(tag))
for tag in tags_xnxx:
    tag_cleaned = str(clean_word(tag))
    # first id for xhamster's tags
    if (len(tags_merged[str(tag_cleaned)]) == 0):
        tags_merged[str(tag_cleaned)].append(None)
    tags_merged[str(tag_cleaned)].append(str(tag))

print tags_merged


for tag_merged in '%(chinese)s' % tags_merged:
    print tags_merged

"""

"""
print "ok number : " + str(ok)
print "ko number : " + str(ko)
print tags_xhamster
print tags_xnxx

def test_similar_words(words1, words2):
    similar = False
    size_words1 = len(words1)
    size_words2 = len(words2)
    # test if they are similar
    for i in range(0, size_words1):
        for j in range(0, size_words2):
            if (str(words1[i]) == str(words2[j])):
                # case : "sex toys" with "sex toys"
                if (size_words1 == size_words2):
                    print "test1 : " + str(words1[i]) + " - " + str(words2[j])
                    similar = True
                # case : "creampie" with "cream pie"
                elif (size_words1 < size_words2 and len(words1[i]) > len(words2[j])):
                    print "test2 : " + str(words1[i]) + " - " + str(words2[j])
                    similar = True
                # case : "cream pie" with "creampie"
                elif (size_words1 > size_words2 and len(words1[i]) < len(words2[j])):
                    print "test3 : " + str(words1[i]) + " - " + str(words2[j])
                    similar = True
    if (similar == False):
        print "Fail : " + str(words1[i]) + " - " + str(words2[j])
    return similar

for tag_source in tags_xhamster:
    equal = False
    # clean tag_source
    tag_source_cleaned = clean_word(tag_source)
    for tag_target in tags_xnxx:
        if (equal == False):
            # clean tag_target
            tag_target_cleaned = clean_word(tag_target)
            equal = test_similar_words(tag_source_cleaned, tag_target_cleaned)
        else:
            break

    if (equal == False):
        tags_merged
    else:
"""