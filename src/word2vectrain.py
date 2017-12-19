from gensim.models import word2vec

model_path = 'models/word_2_vec/w2vmodel'
data_path = 'resource/news/news.dat'

sentences = [line.split() for line in open(data_path)]
print('done')
model250 = word2vec.Word2Vec(sentences,min_count=5,iter=250)
print('done')
model250.save(model_path)