from nltk import RegexpTokenizer
from processor import ProcessingHandler

tokenizer = RegexpTokenizer('[A-Za-z0-9]{3,}')


class StringProcessor:
    def __init__(self):
        self.__processing_handler__ = ProcessingHandler()

    def process(self, ip_string):
        string_tokens = tokenizer.tokenize(ip_string.lower())
        processed_tokens = self.__processing_handler__.process(string_tokens)
        processed_string = ' '.join(processed_tokens)
        return processed_string
