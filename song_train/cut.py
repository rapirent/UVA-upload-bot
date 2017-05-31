#_*_ encoding: utf-8 _*_
#encoding=utf-8
#from codecs_to_hex import to_hex
import jieba
import sys
import codecs

jieba.set_dictionary('data/dict.txt.big')

output = codecs.open('data/lyrics_cut.dataset', 'w', 'utf-8')

with open('data/lyrics.dataset', 'rb') as song:
    for line in song:
        words = jieba.cut(line)
        output.write(u" ".join(words))
        print(line)

output.close()
