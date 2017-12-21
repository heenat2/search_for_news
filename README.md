Browse Based News Search Engine exploiting Semantic Relationships between Terms

Overview: This project aims to enhance news search experience for a user by mining the main topics from the highly ranked search results. 
These topics are displayed for user selection and further exploration of news. Each topic has a drop down with a list of 10 terms most similar
to it. Even these are available for selection and will be added to the search query when selected.

CORPUS - A static corpus comprising of ~95000 news articles was used for this exercise. The articles were obtained by calling the webhose.io api.
The domain of the sites was restricted to only news websites. 
Source code is available in getnews2.py and remove_duplicates.py.

INDEX - metapy library was used to create an inverted index. nltk and gensim were used for data pre-processing tasks of tokenization, 
stop-word removal, lemmatization and phrase identification. 
Source code is available in createIndex.py, corpusprocessor.py, phraser.py and processor.py.

RANKING - The retrieved documents are ranked as per BM25 ranking function. metapy has been used for search and ranking. Documents are assigned an 
additional weight if the query terms appear in the title of the document. This weight is added to the BM25 score. Terms appearing in the query if 
present in the document text are highlighted with a different color. However the highlight logic has limitations and does not cover all forms of 
the term.
Source code is available in search.py

TOPIC MINING - An LDA model was trained on the corpus using python library gensim. The topic terms displayed after a successful search are inferred 
from the top 10 documents. Both topic and term probabilities are taken into account to arrive at the top set of terms. An effort has been made to 
check that the most probable terms in a topic as predicted by LDA are not also very common in the corpus. This was achieved using the relavance 
formula as specified in paper 'LDAvis: A method for visualizing and interpreting topics' at 
https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf.
Source code is available in Ldamodel.py, lda_infer_topics2.py and sort_relevance.py

TERMS SIMILAR TO TOPICS - Gensim word2vec model was trained on the corpus to extract most similar terms.
Source code is available in word2vectrain.py. Similar word prediction is done in app.py.


