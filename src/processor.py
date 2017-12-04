import os
from gensim.models.phrases import Phraser
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode

phraser_path = '/home/rik/Heena/Phraser.model'
stoppath = '/home/rik/Heena/lemur-stopwords.txt'
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
        print('In StopWordProcessor.process')
        newtokenlist = [token for token in tokenlist if token not in stopset]
        return newtokenlist


class BigramPhraser(AbstractProcessor):
    def process(self, tokenlist):
        print('In BigramPhraser.process')
        return model[tokenlist]


class Stemmer(AbstractProcessor):
    def process(self, tokenlist):
        print('In Stemmer.process')
        newtokenlist = [stemmer.stem(token) for token in tokenlist]
        return newtokenlist


class Lemmatizer(AbstractProcessor):
    def process(self, tokenlist):
        print('In Lemmatizer.process')
        newtokenlist = [unidecode(wordnet_lemmatizer.lemmatize(token)) for token in tokenlist]
        return newtokenlist


class ProcessingHandler:
    def __init__(self, pipeline=[BigramPhraser(), StopWordProcessor(), Lemmatizer()]):
        self.pipeline = pipeline

    def process(self, doc):
        print('In ProcessingHandler.process')
        newdoc = doc
        for processor in self.pipeline:
            newdoc = processor.process(newdoc)
        return newdoc
