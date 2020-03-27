import sys
from snownlp import SnowNLP
import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import os
import time
import lxml.html
import re
import urllib.parse
from opencc import OpenCC
import pandas as pd
import numpy as np
import csv
cc = OpenCC('s2t')
from snownlp import sentiment

sort_pd=pd.read_csv('E:\YoutubeYear\新增資料夾\SortList.csv')
sort_list=list(sort_pd['name'])
dict_list=[]
temp=1
len_max=1
i=1
def is_alphabet(keyword):
    return all(ord(c) < 128 for c in keyword)
for n,i in enumerate(sort_list):
    if len(str(i).split(' '))>1:
        if len(i)<12:
            for j in range(len(str(i).split(' '))):
                if (len(str(i).split(' ')[j])>len_max):
                    len_max=len(str(i).split(' ')[j])
                    temp=j
            dict_list.append(str(i).split(' ')[temp])
        else:
            dict_list.append(str(i))
    else:
        dict_list.append(str(i))
dici_str=[]
for n,i in enumerate(dict_list):
    if len(i)==1:
        pass
    elif is_alphabet(i) and len(i)<=3:
        pass
    else:
        dici_str.append(i)
i=0
dici_str.sort(key = lambda i:len(str(i)),reverse=False)
print(dici_str)
word={}
for i in dici_str:
    with open('E:\YoutubeYear\LongMoonEEEESortDict.csv','a',encoding='utf-8-sig') as f:
        if word.get(str(i)) == None:
            word[str(i)]=1
            f.write(str(i))
            f.write('\n')




# def read_and_analysis(input_file, output_file):
#   f = open(input_file)
#   fw = open(output_file, "w")
#   while True:
#     line = f.readline()
#     if not line:
#       break
#     lines = line.strip().split("\t")
#     if len(lines) < 2:
#       continue
#
#     s = SnowNLP(lines[1].decode('utf-8'))
#     # s.words 查询分词结果
#     seg_words = ""
#     for x in s.words:
#       seg_words += "_"
#       seg_words += x
#     # s.sentiments 查询最终的情感分析的得分
#     fw.write(lines[0] + "\t" + lines[1] + "\t" + seg_words.encode('utf-8') + "\t" + str(s.sentiments) + "\n")
#   fw.close()
#   f.close()
#
# if __name__ == "__main__":
#   input_file = sys.argv[1]
#   output_file = sys.argv[2]
#   read_and_analysis(input_file, output_file)
