from search import Search

search = Search()
results = search.get_results_for_query("donald trump", 10)
for res in results:
    print res.get_title()
    print res.get_url()
    get_topics()



