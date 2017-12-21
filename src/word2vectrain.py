"""
This module takes as input preprocessed corpus data, trains a Word2Vec model on it and writes it to file
File paths need to be considered before running this.
"""

from gensim.models import word2vec

model_path = 'models/word_2_vec/w2vmodel'
data_path = 'resource/news/news.dat'

sentences = [line.split() for line in open(data_path)]
model250 = word2vec.Word2Vec(sentences, min_count=5, iter=250)
model250.save(model_path)