"""
The process method in StringProcessor class accepts a string and performs the following operations on it-
1. Lower case conversion and Tokenization
2. Other pre-processing tasks as per the processing handler

The default pre-processing pipeline for handler is identification of common bigram phrases, stop word removal
and lemmatization.

It returns a space delimited string of tokens.
"""

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
