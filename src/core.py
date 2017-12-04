

class Response(object):

    def __init__(self, browse_dict, results):
        self.__browse_dict__ = browse_dict
        self.__results__ = results

    def get_browse_dict(self):
        return self.__browse_dict__

    def get_results(self):
        return self.__results__


class SearchResult(object):

    def __init__(self, url, title):
        self.__url__ = url
        self.__title__ = title

    def get_url(self):
        return self.__url__

    def get_title(self):
        return self.__title__


