import webhoseio
import json
import time

#class definition for document object
class document:
    def __init__(self,uuid,url,site_full,site_categories,title,title_full,published,author,text):
        self.uuid = uuid
        self.url = url
        self.site_full = site
        self.site_categories = site_categories
        self.title = title
        self.title_full = title_full
        self.date_published = published
        self.author = author
        self.text = text

#function to create 
def main():
    webhoseio.config(token="ee20e5f2-4fee-45f5-97f3-b24e15aec607")
    query_params = {
    "q": "language:english site_type:news site:(cnn.com OR bbc.com OR foxnews.com OR usatoday.com) has_video:false",
    "ts": "1506060752159",
    "sort": "crawled"
    }
    output = webhoseio.query("filterWebContent", query_params)
    flname = "file" + "1"
    opfile = open('/home/rik/file1','w')

    uuid = output['posts'][0]['uuid']
    url =  output['posts'][0]['url']
    site_full = output['posts'][0]['thread']['site_full']
    site_categories = output['posts'][0]['thread']['site_categories']
    title_full = output['posts'][0]['thread']['title_full']
    title = output['posts'][0]['title']
    published = output['posts'][0]['published']
    author = output['posts'][0]['author']
    text = output['posts'][0]['text'] 

    doc = document(uuid,url,site_full,site_categories,title,title_full, published, author,text)

    jsondata = json.dumps(doc.__dict__,sort_keys=True)
    opfile.write(jsondata)

main()

