import re
import sys
import jieba
from snownlp import SnowNLP
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

text = codecs.open(r'C:\Users\Big data\PycharmProjects\MyDjango\myporject\AiToTitle\t6.txt', 'r', 'utf-8').read()

tr4s = TextRank4Sentence()
tr4s.analyze(text=text, lower=True, source = 'all_filters')

#設定只保留中文、英文、數字（去掉韓語日語德語，也會去掉表情符號等等）
#reference: https://zhuanlan.zhihu.com/p/84625185
rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")

#print( '摘要：' )
tt = []
for i, item in enumerate(tr4s.get_key_sentences(num=3,sentence_min_len=80)):

    #print('第{}順位，利用textrank的第一次摘要: '.format(i+1))
    #print(item.index, item.weight, item.sentence)

    s = SnowNLP(item.sentence)
    #print('利用snownlp再取一次的結果: ')
    secnd_sn = s.summary(3)
    #print(secnd_sn)
    for cont in secnd_sn:
        ttt = rule.sub(' ', str(cont))
        if len(ttt.split(' ')) < 3 and len(ttt) > 12:
            tt.append(ttt)
    #print(' ')

s = SnowNLP(text)
#print('直接使用snownlp的摘要: ')
first_sn = s.summary(3)
for cont in first_sn:
    ttt = rule.sub(' ', str(cont))
    if len(ttt.split(' ')) < 3 and len(ttt) > 12:
        tt.append(ttt)
#print(first_sn)
#print(' ')

if len(tt) == 0:
    print('無適合的標題')
else:
    #print(len(tt))
    print('標題生成: ')
    print(set(tt))
