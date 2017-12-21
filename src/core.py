"""
Defines class SearchResult.
Instantiated in search.py.
"""

class SearchResult(object):

    def __init__(self, url, title, text):
        """
        :param url: URL of the retrieved document
        :type url: str
        :param title: Title of the retrieved document
        :type title: str
        :param text: Body of the retrieved document
        :type text: str
        """
        self.__url__ = url
        self.__title__ = title
        self.__text__ = text

    def get_url(self):
        return self.__url__

    def get_title(self):
        return self.__title__

    def get_text(self):
        return self.__text__