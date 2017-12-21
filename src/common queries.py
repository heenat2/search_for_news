"""
This module creates a file (resource/testdata.txt) of sample queries. It extracts these from the corpus, mining
the data from the titles of the news articles. The file contains a random list of noun phrases and the queries
provided in it have not been proved to work better than other test queries.
"""

from textblob import TextBlob
import json
import gensim

title_list = []

ip_file = open('/home/rik/Heena/News2/corpus.txt', 'r')
for line in ip_file:
    jsondict = json.loads(line.rstrip())
    title_list.append(TextBlob(jsondict['title']).noun_phrases)

new_title_list = []
for title in title_list:
    new_title_list.append([token for token in title if len(token) > 4])

dict = gensim.corpora.Dictionary(new_title_list)
print(dict)

# filter tokens with very high and low frequencies
high_freq_words = []
from six import iteritems
high_freq_words = [tokenid for tokenid, docfreq in iteritems(dict.dfs) if docfreq > 500]

low_freq_words = []
from six import iteritems
low_freq_words = [tokenid for tokenid, docfreq in iteritems(dict.dfs) if docfreq < 10]
dict.filter_tokens(low_freq_words + high_freq_words)
dict.compactify()

from unidecode import unidecode
opfile = open('resource/testdata.txt','w')
for id, token in dict.iteritems():
    if "\'" not in token:
        opfile.write(unidecode(token)+'\n')