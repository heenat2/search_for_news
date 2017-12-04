import json
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from nltk import sent_tokenize, word_tokenize

data_dict = {}
for i in range(1,51):
    ipfile = open('/home/rik/Heena/News2/file_' + str(i),'r')
    for line in ipfile:
        jsondict = json.loads(line.rstrip())
        data_dict[jsondict["uuid"]] = [jsondict['date_published'],jsondict['url'],jsondict['title_full'],jsondict['text']]
    ipfile.close()

data_tokens = {}
#sentence_stream = []
bow_list = []
url_list = []
for key in data_dict.iterkeys():
    #data_tokens[key] = sent_tokenize(data_dict[key][3].lower())
    #data_tokens[key] = [word_tokenize(line) for line in data_tokens[key]]
    bow = [word_tokenize(data_dict[key][3])]
    bow_list.append(bow)
    url_list.append(key)
    #for sent in data_tokens[key]:
        #sentence_stream.append(sent)

#print('value1 ',data_tokens['3985b917f62f40b70a6f4932957cfead4ce3229d'])
#print('value2 ',data_tokens['ee6aad01ba60173da527b062dfa70565e9cffba7'])
#print('value3 ',data_tokens['3b7e2d0ee3f42fed5b1a8f9ff575649e68536bf7'])
#print(sentence_stream[0],sentence_stream[1],sentence_stream[2])

phrases = Phrases(sentence_stream)
bigram = Phraser(phrases)
