"""Defines processors used by corpusprocessor pipeline
Variable paths are phraser_path and stopwords list path"""

import os
from gensim.models.phrases import Phraser
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode

phraser_path = 'models/Phraser.model'
stoppath = 'resource/stopwords.txt'
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer('english')
model = Phraser.load(phraser_path)

stopfile = open(stoppath, 'r')
stopset = set()
for line in stopfile:
    stopset.add(line.rstrip())
stopfile.close()


class AbstractProcessor:
    def __init__(self):
        pass

    def process(self, tokenlist):
        pass


class StopWordProcessor(AbstractProcessor):
    def process(self, tokenlist):
        '''
        :param tokenlist: tokenized document
        :type tokenlist: list
        :return: tokenized document after removing stop words
        :rtype: list
        '''
        newtokenlist = [token for token in tokenlist if token not in stopset]
        return newtokenlist


class BigramPhraser(AbstractProcessor):
    def process(self, tokenlist):
        '''
        :param tokenlist: tokenized document
        :type tokenlist: list
        :return: tokenized document with tokens forming frequent bigram phrases joined by underscore
        :rtype: list
        '''
        return model[tokenlist]


class Stemmer(AbstractProcessor):
    def process(self, tokenlist):
        '''
        :param tokenlist: tokenized document
        :type tokenlist: list
        :return: list of stemmed tokens of a document
        :rtype: list
        '''
        newtokenlist = [stemmer.stem(token) for token in tokenlist]
        return newtokenlist


class Lemmatizer(AbstractProcessor):
    def process(self, tokenlist):
        '''
        :param tokenlist: tokenized document
        :type tokenlist: list
        :return: list of lemmatized tokens of a document
        :rtype: list
        '''
        newtokenlist = [unidecode(wordnet_lemmatizer.lemmatize(token)) for token in tokenlist]
        return newtokenlist


class ProcessingHandler:
    def __init__(self, pipeline=[BigramPhraser(), StopWordProcessor(), Lemmatizer()]):
        '''
        :param pipeline: Sequence of nlp operations to be performed for each document
        :type pipeline: list
        '''
        self.pipeline = pipeline

    def process(self, doc):
        '''
        :param doc: list of tokens forming a document
        :type doc: list
        :return: pre-processed list of document tokens as per ProcessingHandler pipeline
        :rtype: list
        '''
        newdoc = doc
        for processor in self.pipeline:
            newdoc = processor.process(newdoc)
        return newdoc