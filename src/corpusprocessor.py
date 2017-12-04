from nltk import RegexpTokenizer
from unidecode import unidecode
from processor import ProcessingHandler
import json
tokenizer = RegexpTokenizer('[A-Za-z0-9]{3,}')


class CorpusProcessor:
    def __init__(self,dir_path = '/home/rik/Heena/News2',processing_handler = ProcessingHandler):
        self.dir_path = dir_path
        self.processing_handler = processing_handler

    def get_corpus_list(self):
        print('In get_corpus_list')
        text_list, url_list, title_list = [],[],[]
        ip_file = open(self.dir_path + '/corpus.txt', 'r')
        for line in ip_file:
            jsondict = json.loads(line.rstrip())
            # corpus_dict[jsondict["url"]] = [jsondict['date_published'], jsondict['uuid'], jsondict['title_full'],
            #                               jsondict['text']]
            text_list.append(jsondict['text'])
            url_list.append(jsondict['url'])
            title_list.append(jsondict['title'])
        ip_file.close()
        return text_list, url_list, title_list

    def preprocess(self,text_list):
        print('In corpusprocessor.preprocess')
        path = '/home/rik/Heena/news/news.dat'
        processed_tokens_list = []
        op_file = open(path, 'w')
        for text in text_list:
            tokens = tokenizer.tokenize(unidecode(text.lower()))
            processed_tokens = self.processing_handler().process(tokens)
            processed_tokens_list.append(processed_tokens)
            op_file.writelines(' '.join(processed_tokens) + '\n')
        op_file.close()
        print('news.dat created')
        return processed_tokens_list
