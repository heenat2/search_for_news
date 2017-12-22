_Browse Based News Search Engine exploiting Semantic Relationships between Terms_

_Overview -_ 
The aim of this project is to create a search engine for current news that also provides recommendations / suggestions for browsing based on the 
the search results that were retrieved for the user's query. This is accomplished by mining the main topics from the highly ranked search results. 
These topics are displayed for user selection and further exploration of news. Each topic has a drop down with a list of 10 terms most similar
to it. Even these are available for selection by the user and will be added to the search query when selected.

**CORPUS** - A static corpus comprising of ~95000 news articles was used for this exercise. The articles were obtained by calling the webhose.io api.
The domain of the sites was restricted to only news websites. The trial version of this api only allows 1000 calls per month. Hence the data was 
gathered in two batches, once in October and next in November 2017.
Source code is available in getnews2.py and remove_duplicates.py.

**INDEX** - metapy library was used to create an inverted index. nltk and gensim were used for data pre-processing tasks of tokenization, 
stop-word removal, lemmatization and phrase identification. 
Source code is available in createIndex.py, corpusprocessor.py, phraser.py and processor.py.

**RANKING** - The retrieved documents are ranked as per BM25 ranking function. metapy has been used for search and ranking. Documents are assigned an 
additional weight if the query terms appear in the title of the document. This weight is added to the BM25 score. Terms appearing in the query if 
present in the document text are highlighted with a different color. However the highlight logic has limitations and does not cover all lexical forms
of the term.
Source code is available in search.py

**TOPIC MINING** - An LDA model was trained on the corpus using python library gensim. The topic terms displayed after a successful search are 
inferred from the top 10 documents. Both topic and term probabilities are taken into account to arrive at the top set of terms. An effort has been 
made to check that the most probable terms in a topic as predicted by LDA are not the most common in the corpus too. This was achieved using the 
relavance formula as specified in paper 'LDAvis: A method for visualizing and interpreting topics', https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf.
Source code is available in Ldamodel.py, lda_infer_topics2.py and sort_relevance.py

**TERMS SIMILAR TO TOPICS** - Gensim word2vec model was trained on the corpus to extract most similar terms.
Source code is available in word2vectrain.py. Similar word prediction is done in app.py.

_Installation_ - can be accomplished using method 1 or 2. Method 1 is recommended for running the application easily.

1. The application has been containerized using docker. Docker can be installed from https://docs.docker.com/engine/installation/.
Once docker is installed, the below two commands should be run from any terminal to launch it - 

docker pull heenat2/semantic_search:latest

docker run -it --rm -p 5000:5000 heenat2/semantic_search:latest 

This gives the message '* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)'.
User can directly click the url on mac or navigate to 'localhost:5000' on windows.

2. The application can also be launched by running app.py (using Python 2.7 interpreter) but this requires a copy of the corpus, the models and 
index to be placed in the 'src' folder as shown below -
src/idx
src/models
src/resource

Other prerequisite python libraries to be installed for this method are listed in file requirements.txt. If using anaconda, only the modules listed 
below are required to be installed -
a. markupsafe
b. gensim
c. metapy
d. unidecode
e. flask
f. wtforms
g. nltk