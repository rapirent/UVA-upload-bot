# encoding=utf8
import sys
import os
from gensim import corpora, models, similarities
from six import iteritems

dictionary = corpora.Dictionary.load('lyrics.dict')
corpus = corpora.MmCorpus('lyrics.mm')

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=28)

doc = sys.argv[1]
vec_bow = dictionary.doc2bow(doc.lower().split())
print(vec_bow)
vec_lsi = lsi[vec_bow]

print(vec_bow)
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus], num_features=100)
index.save('lyrics.index')

sims = index[vec_lsi]

sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims[:5])

lyrics = [];
fp = open("data/lyrics_word_net.dataset")
for i, line in enumerate(fp):
    lyrics.append(line)
fp.close()

url = [];
fp = open("data/lyrics_url.dataset")
for i, line in enumerate(fp):
    url.append(line)
fp.close()

for lyric in sims[:5]:
    print("\n相似歌詞：",  lyrics[lyric[0]])
    print("相似度：",  lyric[1])
    print("試聽連結：",  url[lyric[0]])
