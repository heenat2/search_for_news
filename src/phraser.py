from nltk import RegexpTokenizer
from unidecode import unidecode
import json
from gensim.models.phrases import Phraser
from gensim.models import Phrases

tokenizer = RegexpTokenizer('[A-Za-z0-9]{3,}')

text_list = []
processed_tokens_list = []


ip_file = open('/home/rik/Heena/News2/corpus.txt', 'r')
for line in ip_file:
    jsondict = json.loads(line.rstrip())
    text_list.append(jsondict['text'])

for text in text_list:
    tokens = tokenizer.tokenize(unidecode(text.lower()))
    processed_tokens_list.append(tokens)
print('done')

phrased_token_stream = []

phrases = Phrases(processed_tokens_list, min_count=2000)
phraser_obj = Phraser(phrases)
for item in processed_tokens_list:
    phrased_token_stream.append((phraser_obj[item]))
print('done')

phraser_obj.save('/home/rik/Heena/Phraser.model')
print('done')