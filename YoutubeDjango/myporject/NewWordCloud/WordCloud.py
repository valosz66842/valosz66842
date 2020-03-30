#coding=utf-8
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from confluent_kafka import Producer
from bs4 import BeautifulSoup
from confluent_kafka import Consumer, KafkaException, KafkaError
import requests
import json
from opencc import OpenCC
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
import jieba
import pymysql
from random import randint

#使用網路上簡體的中文詞庫: https://raw.githubusercontent.com/fxsjy/jieba/master/extra_dict/dict.txt.big
#記得將簡體的中文詞庫轉成繁體(可以使用opencc套件轉成繁體)，轉完的檔案為dict.txt.big_new.txt
jieba.set_dictionary('dict.txt.big_new.txt')
#再加入我們從維基百科建立的自訂字典:self_define_dict.txt，可以將專有名詞成功斷開-->蔡英文、韓國瑜
#這個自定義字典存檔時記得使用utf-8的編碼存檔
jieba.load_userdict('self_define_dict.txt')
#讀入stopwords.txt並做成 stopwords 字典
stopwords = {}
with open('test_dict_stop.txt', 'r', encoding='UTF-8') as file:
    for st_word in file.readlines():
        st_word = st_word.strip() #data.strip()為去除前後空白
        stopwords[st_word] = 1
#'''
#讀入已合併的新聞檔案: totalnews_{date}.csv
#讀入新聞總檔案
FilePath=r'C:\Users\Big data\PycharmProjects\MyDjango\myporject\NewWordCloud\14\For_All_News\data_for_merge'
ImgPath=r'.\static\images'
WordCloud_Dice = {}
def is_alphabet(keyword):
    return all(ord(c) < 128 for c in keyword)

#### 要搜尋的新聞日期 (20200121(含)之後才有完整資料) ####
Folder_Path = FilePath  #csv目標資料夾
os.chdir(Folder_Path)  # 換工作路徑
file_list = os.listdir(Folder_Path)  # 這個資料夾內所有的檔案名稱
file_csv = []
for file in file_list:  # 只讀csv檔
    if '.csv' in file:
        file_csv.append(file)

for file_name in file_csv:
    data = pd.read_csv(r'C:\Users\Big data\PycharmProjects\MyDjango\myporject\NewWordCloud\14\For_All_News\data_for_merge\{}'.format(file_name))
    #一邊讀入一邊做jieba斷詞，將斷詞完的做停用字的處理，最後將斷詞存入
    wd_dict = {}
    #新聞總檔案
        #有些中文字python預設為unicode無法編譯，例如游錫堃的堃，使用encoding ='utf-8-sig'
    for j, content in enumerate(data['content']):
        #這個是將udn的內容中有該段文字給替換成空白
        content=str(content)
        content = content.replace('''domready(function() {if ( !countDownStatus ) getCountdown();if ( !highChartsStatus ) getHighcharts();});domready(function() {var channelId = 2;var actArea = "poll_at_story_0_v773";var actCode = "v773";var actTemplate = "bar2";var elemDiv = document.createElement('div');elemDiv.id = actArea;elemDiv.className ='vote_body area';var scr = document.getElementById(actArea+'_script');scr.parentNode.insertBefore(elemDiv, scr);$.getScript('/funcap/actIndex.jsp?actCode=' + actCode + '&channelId=' + channelId , function() {actTemplate = eval('objAct_' + actCode + '.d1.actTemplate');$.ajaxSetup({ cache: true });$.getScript('/func/js/' + actTemplate + '_min.js?2019122401', function() {$.ajaxSetup({ cache: false });piepkg();loadTemplateJs(actTemplate);eval(actTemplate + 'view("' + '#' + actArea + '");')})});});''', '')
        content = content.strip('').strip('\n').strip('') #去除文章前後的空白與斷行
        seg_con_list = jieba.cut(content)
        # 拿stopwords來清理jieba處理完的字串
        for wd in seg_con_list:
            wd = wd.strip('')
            if is_alphabet(wd) != True:
                if stopwords.get(wd) == None and len(wd) > 1:
                    if wd_dict.get(wd) == None: #開始計算字詞的數量，未出現的單字存入字典
                        wd_dict[wd] = 1
                    else: #開始計算字詞的數量，出現過的單字字典數加1
                        wd_dict[wd] += 1
            # 每篇文章做完再進到下一行
    VideoID = file_name[:-4]
    print("影片ID:{}".format(VideoID))
    #=== deal with similarity_dict ===
    fw = open(r'C:\Users\Big data\PycharmProjects\MyDjango\myporject\NewWordCloud\similarity_dict.txt', 'r', encoding='utf-8-sig')
    sy_list=[]
    while True:
        line = fw.readline()
        b = line.strip('\n').strip(' ')
        a = b.split(',')
        sy_list.append(a)
        if not line:
            break
    fw.close()
    sy_list.pop() #將最後一個空串列丟出
    ncount=0
    for n, syn in enumerate(sy_list):
        for i in range(len(syn)):
            ncount += wd_dict.get(syn[i],0)
            if wd_dict.get(syn[i]) != None:
                del wd_dict[syn[i]]
        wd_dict[syn[0]] = ncount
        ncount = 0
    sort_dict=wd_dict
    print(sort_dict)
    sort_dict=sorted(sort_dict.items(), key=lambda d: d[1], reverse=True)
    print(sort_dict)
    print(type(sort_dict))
    print(len(sort_dict))
    print(type(sort_dict[0]))
    Json_Dict={}
    json_key=''
    json_value=''
    for i in range(30):
        sort_dict[i]=str(sort_dict[i])
        json_key=sort_dict[i].split('\',')[0]
        json_key=json_key[2:]
        json_value=sort_dict[i].split('\', ')[1]
        json_value=json_value[:-1]
        Json_Dict[json_key]=json_value
        if (i+1)%10==0:

            Json_Dict[json_key] = json_value

    with open(r"C:\Users\Big data\PycharmProjects\MyDjango\myporject\NewWordCloud\14\{}.json".format(VideoID),'w',encoding='utf-8-sig') as f:
        json.dump(Json_Dict, f,ensure_ascii=False)

    #del wd_dict['不拘']
    # ===== 生成文字雲 ======
    def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
        h = randint(0, 240)
        #s = int(100.0 * 255.0 / 255.0)
        s = randint(70,100)
        l = int(100.0 * float(randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)
    ###http://csscoke.com/2015/01/01/rgb-hsl-hex/ HSL調色###
    #font設定成微軟正黑體，這邊我是直接抓我windows中的字體檔案，將該檔案放在程式的同一個工作目錄下即可
    font = r'C:\Users\Big data\PycharmProjects\MyDjango\myporject\NewWordCloud/NotoSansCJKtc-Black.otf'
    # wordcloud = WordCloud(background_color='white',font_path=font,scale=5)
    wordcloud = WordCloud(background_color='white',font_path=font,max_font_size =50,min_font_size=10,scale=10,max_words=500)
    #文字雲使用頻率，輸入值為字詞數的字典 (wd_dict)
    my_wordcloud =wordcloud.generate_from_frequencies(frequencies=wd_dict)
    #畫出文字雲
    my_wordcloud.recolor(color_func = random_color_func)
    plt.axis("off")
    # plt.imshow(my_wordcloud)
    # fig = plt.gcf()
    # fig.set_size_inches(20, 10)
    # fig.savefig(ImgPath + '\{}.png'.format(VideoID))
    # time.sleep(10)
    #====== 保存圖片 ======
    #新聞總檔案
    wordcloud.to_file(r'C:\Users\Big data\PycharmProjects\MyDjango\myporject\NewWordCloud\14\{}.png'.format(VideoID))
    plt.imshow(my_wordcloud)
