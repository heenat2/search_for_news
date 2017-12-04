import math
import sys
import time
import metapy
import pytoml


class NewsRanker(metapy.index.OkapiBM25):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """

    def __init__(self):
        # You *must* call the base class constructor here!
        super(NewsRanker, self).__init__()

    def score_one(self, sd):
        print('inside score_one')
        """
        You need to override this function to return a score for a single term.
        For fields available in the score_data sd object,
        @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
        """
        print('calling super score one')
        parent_score = super(NewsRanker, self).score_one()
        print('done calling score one')
        print parent_score
