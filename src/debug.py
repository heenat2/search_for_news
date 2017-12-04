import json
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from nltk import sent_tokenize, word_tokenize
from unidecode import unidecode

data_dict = {}
j = 1
for i in range(1,21):
    ipfile = open('/home/rik/Heena/News2/file_' + str(i),'r')
    for line in ipfile:
        jsondict = json.loads(line.rstrip())
        if i == 20:
            print("writing line", j , "uuid = ", jsondict["uuid"] )
            j = j + 1
        data_dict[jsondict["uuid"]] = [jsondict['date_published'],jsondict['url'],jsondict['title_full'],jsondict['text']]
    ipfile.close()

sentence_stream = []
url_list = []
count = 0
for key in data_dict.iterkeys():
    url_list.append(key)
    sentence_stream.append(word_tokenize(unidecode(data_dict[key][3].lower())))
print(len(sentence_stream))