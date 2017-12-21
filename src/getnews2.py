"""
This module makes use of the data retrieval api at https://webhose.io/ to get data from the below listed sites -
    cnn.com, bbc.com, reuters.com, nbcnews.com,
    foxnews.com, washingtonpost.com, espn.com, tmz.com,
    sportingnews.com, usnews.com, wsj.com, latimes.com,
    time.com, nydailynews.com, economist.com, technewsworld.com,
    computerworld.com, newsmax.com, theatlantic.com, hollywoodreporter.com

For each news article, it stores data attributes specified in class document in json format.
"""

import webhoseio
import json
import time

class document:
    def __init__(self, uuid, url, site_full, site_categories, title, title_full, published, author, text):
        self.uuid = uuid
        self.url = url
        self.site_full = site_full
        self.site_categories = site_categories
        self.title = title
        self.title_full = title_full
        self.date_published = published
        self.author = author
        self.text = text


def main():
    webhoseio.config(token="XXXXXXXXXXXXXXXXX")   # needs to be substituted by real webhoseio token
    query_params = {
    "q": "language:english has_video:false is_first:true site_type:news site:(cnn.com OR bbc.com OR reuters.com OR nbcnews.com OR foxnews.com OR washingtonpost.com OR espn.com OR tmz.com OR sportingnews.com OR usnews.com OR wsj.com OR latimes.com OR time.com OR nydailynews.com OR economist.com OR technewsworld.com OR computerworld.com OR newsmax.com OR theatlantic.com OR hollywoodreporter.com) spam_score:0.0",
    "ts": "1510212713819",
    "sort": "crawled"
    }
    #get 1st set of articles
    output = webhoseio.query("filterWebContent", query_params)
    
    fl_counter = 1
    while fl_counter <= 1000:
        fl_name = "file" + "_" + str(fl_counter)
        opfile = open('C:/Users/Heena/News3/' + fl_name, 'w', encoding='utf-8')  #specify path to corpus folder here
        for post in output['posts']:
            uuid = post['uuid']
            url = post['url']
            site_full = post['thread']['site_full']
            site_categories = post['thread']['site_categories']
            title_full = post['thread']['title_full']
            title = post['title']
            published = post['published']
            author = post['author']
            text = post['text'] 

            doc = document(uuid, url, site_full, site_categories, title, title_full, published, author, text)
            jsondata = json.dumps(doc.__dict__, sort_keys=True)
            opfile.write(jsondata+'\n')

        opfile.close()
        time.sleep(30)
        print("fl_counter = ", fl_counter)
        output = webhoseio.get_next()
        print("next = ", output['next'])
        fl_counter+=1

main()
