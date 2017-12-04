from nltk import RegexpTokenizer
from processor import ProcessingHandler
tokenizer = RegexpTokenizer('[A-Za-z0-9]{3,}')

class StringProcessor:
    def __init__(self):
        pass

    def process(self,query):
        string_tokens = tokenizer.tokenize(string.lower())
        processed_tokens = ProcessingHandler().process(string_tokens)
        processed_string = ' '.join(processed_tokens)
        return processed_string