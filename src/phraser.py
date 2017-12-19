'''Modify corpus_path and phraser_model_path before training the Phraser model.
This program detects commonly occurring bi-grams in the corpus and generates
and saves a Phraser object for future use.'''

from nltk import RegexpTokenizer
from unidecode import unidecode
import json
from gensim.models.phrases import Phraser
from gensim.models import Phrases

corpus_path = '/home/rik/Heena/News2/corpus.txt'
phraser_model_path = 'models/Phraser.model'

corpus = open(corpus_path,'r')
tokenizer = RegexpTokenizer('[A-Za-z]{3,}')
text_list, processed_tokens_list, phrased_token_stream = [],[], []

for line in corpus:
    jsondict = json.loads(line.rstrip())
    text_list.append(jsondict['text'])

for text in text_list:
    tokens = tokenizer.tokenize(unidecode(text.lower()))
    processed_tokens_list.append(tokens)
print('done')

phrases = Phrases(processed_tokens_list, min_count=2000)
phraser_obj = Phraser(phrases)
for item in processed_tokens_list:
    phrased_token_stream.append((phraser_obj[item]))
corpus.close()

phraser_obj.save(phraser_model_path)
print('done')