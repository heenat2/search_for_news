"""
Uses metapy to create inverted index on corpus.txt to enable search for queries.
"""

from corpusprocessor import CorpusProcessor
import metapy
import pytoml

text_list, url_list, title_list = [], [], []
config_path = 'resource/news-config.toml'

cp = CorpusProcessor(dir_path='/home/rik/Heena/News2')
text_list, url_list, title_list = cp.get_corpus_list()
cp.preprocess(text_list)

idx = metapy.index.make_inverted_index(config_path)
print('inverted index created')
print('unique terms in corpus: {0}',idx.unique_terms())
print('total corpus terms: {0}',idx.total_corpus_terms())