"""
Processes corpus and writes processed content to news.dat
Input file name = corpus.txt. Default directory path for corpus.txt is set to '/home/rik/Heena/News2'.
Processed file name = news.dat
Is called from createIndex.py
"""

from nltk import RegexpTokenizer
from unidecode import unidecode
from processor import ProcessingHandler
import json
tokenizer = RegexpTokenizer('[A-Za-z]{3,}')
path = 'resource/news/news.dat'

class CorpusProcessor:

    def __init__(self, dir_path='resource', processing_handler=ProcessingHandler):
        """
        :param dir_path: path to folder containing corpus
        :type dir_path: str
        :param processing_handler: handler for sequence of operations to be performed for data preprocessing
        :type processing_handler: ProcessingHandler
        """
        self.dir_path = dir_path
        self.processing_handler = processing_handler

    def get_corpus_list(self):
        """
        :return: News article title, url and body for each article in the corpus
        :rtype: List of strings for each body/text, url and title
        """
        print('Getting corpus...')
        text_list, url_list, title_list = [],[],[]
        ip_file = open(self.dir_path + '/corpus.txt', 'r')
        for line in ip_file:
            jsondict = json.loads(line.rstrip())
            text_list.append(jsondict['text'])
            url_list.append(jsondict['url'])
            title_list.append(jsondict['title'])
        ip_file.close()
        return text_list, url_list, title_list

    def preprocess(self,text_list):
        """
        :param text_list: List of tokens
        :type text_list: List of str
        :return: List of pre-processed tokens as per processing handler
        :rtype: List of str

        Also creates news.dat, required for index creation
        """
        print('Started preprocessing...')
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