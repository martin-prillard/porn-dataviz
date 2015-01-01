__author__ = 'martin'
"""
Wordcount on user's comments
"""

import pandas as pd
from gensim import corpora
from nltk.corpus import stopwords
import string

# NLTK
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
comments_tab0_path = "../../dataset/generated/youporn/video-comments-and-usernames-clean.000.csv"
comments_tab1_path = "../../dataset/generated/youporn/video-comments-and-usernames-clean.001.csv"
comments_dict_path = "../../dataset/generated/youporn/video-comments_wordcount.txt"

data0 = pd.read_csv(comments_tab0_path, sep="|")
data1 = pd.read_csv(comments_tab1_path, sep="|")
# clean data
data0 = pd.DataFrame(data0.fillna(0))
data1 = pd.DataFrame(data1.fillna(0))

# get comments
comments = []

# add the cleaned comment to the corpus
def add_comment(comments, data):
    for line in data['commenttext']:
        # utf-8
        line = str(line).decode('iso-8859-1').encode('utf-8')
        # convert in lower case
        line = line.lower()
        # remove punctuation
        trans_table = string.maketrans( string.punctuation, " "*len(string.punctuation))
        line = line.translate(trans_table)
        # remove numbers
        line = ''.join([i for i in line if not i.isdigit()])
        # remove blak space
        line = " ".join(line.split())
        # remove common words and tokenize
        line = filter(lambda w: not w in not_words_stops,line.split())
        # add line cleaned
        comments.append(line)
    return comments

comments = add_comment(comments, data0)
comments = add_comment(comments, data1)


dictionary = corpora.Dictionary(comments)
# display wordcount sort by word frequency
dictionary.save_as_text(comments_dict_path, sort_by_word=False)
