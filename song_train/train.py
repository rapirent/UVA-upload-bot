#_*_ encoding: utf-8 _*_


from gensim import corpora, models, similarities
from six import iteritems
from collections import defaultdict
import os
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


with open('data/stop_words.txt') as stop_words:
    stop_word_content = stop_words.readlines()
stop_word_content = [word.strip() for word in stop_word_content]
stop_word_content = " ".join(stop_word_content)

dictionary = corpora.Dictionary(document.split() for document in open('data/lyrics_word_net.dataset'))
stoplist = set(stop_word_content.split())
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
            if stopword in dictionary.token2id]
dictionary.filter_tokens(stop_ids)
dictionary.compactify()
dictionary.save('lyrics.dict')

texts = [[word for word in document.split() if word not in stoplist]
         for document in open('data/lyrics_word_net.dataset')]

frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
#過濾frequency只優一的
texts = [[token for token in text if frequency[token] > 1]
         for text in texts]

#doc2vec
corpus = [dictionary.doc2bow(text) for text in texts]
#輸出結果
corpora.MmCorpus.serialize('lyrics.mm', corpus)


##載入剛剛做的

if (os.path.exists("lyrics.dict")):
    dictionary = corpora.Dictionary.load('lyrics.dict')
    corpus = corpora.MmCorpus('lyrics.mm')
else:
    print('沒有lyrics.dict')

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=28)
corpus_lsi = lsi[corpus_tfidf]
#輸出
lsi.save('lyrics.lsi')
#載入LSI模組
#lsi = models.LsiModel.load('lyrics.lsi')

dictionary = corpora.Dictionary.load('lyrics.dict')
corpus = corpora.MmCorpus('lyrics.mm')

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=28)
print('debug 0')
print(lsi.show_topics(-1, num_words=10))
print('debug 1')
print(lsi.show_topic(1, topn=1))
print('debug 2')
print(lsi.show_topic(2, topn=1))
print('debug 3')
print(lsi.show_topic(3, topn=1))
print('debug 4')
print(lsi.show_topic(4, topn=1))
print('debug 5')
print(lsi.show_topic(5, topn=1))
print('debug 6')
print(lsi.show_topic(6, topn=1))
print('debug 7')
print(lsi.show_topic(7, topn=1))
print('debug 8')
print(lsi.show_topic(8, topn=1))
print('debug 9')
print(lsi.show_topic(9, topn=1))
print('debug 10')
print(lsi.show_topic(10, topn=20))
print('debug 11')
print(lsi.show_topic(11, topn=20))
print('debug 12')
print(lsi.show_topic(12, topn=20))
print('debug 13')
print(lsi.show_topic(13, topn=20))
print('debug 14')
print(lsi.show_topic(14, topn=20))
print('debug 15')
print(lsi.show_topic(15, topn=20))
print('debug 16')
print(lsi.show_topic(16, topn=20))
print('debug 17')
print(lsi.show_topic(17, topn=20))
print('debug 18')
print(lsi.show_topic(18, topn=20))
print('debug 19')
print(lsi.show_topic(19, topn=20))
print('debug 20')
print(lsi.show_topic(20, topn=20))
print('debug 21')
print(lsi.show_topic(21, topn=20))
print('debug 22')
print(lsi.show_topic(22, topn=20))
print('debug 23')
print(lsi.show_topic(23, topn=20))
print('debug 24')
print(lsi.show_topic(24, topn=20))
print('debug 25')
print(lsi.show_topic(25, topn=20))
print('debug 26')
print(lsi.show_topic(26, topn=20))
print('debug 27')
print(lsi.show_topic(27, topn=20))
print('debug')

