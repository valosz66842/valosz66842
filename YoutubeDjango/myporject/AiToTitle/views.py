from django.shortcuts import render
from django.shortcuts import render
from django import template
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse
from datetime import datetime

from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import JsonResponse
from confluent_kafka import Producer
import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import os
import time
import lxml.html
import re
import urllib.parse
import pandas as pd
import numpy as np
import csv
import jieba
import pymysql
import re
import sys
import jieba
from snownlp import SnowNLP
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
# Create your views here.
# Create your views here.
# Create your views here.
import pandas as pd
import socket
import torch
import torch.nn.functional as F
import os
import argparse
from tqdm import trange
from transformers import GPT2LMHeadModel
from opencc import OpenCC
import sys
pwd=os.path.dirname(__file__)
sys.path.append(pwd+"../kafka_producer.py")
import kafka_producer

def summary_candidate_fin(text):
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
    word={}
    first_sn = s.summary(3)
    for cont in first_sn:
        ttt = rule.sub(' ', str(cont))
        if len(ttt.split(' ')) < 3 and len(ttt) > 12:
            if word.get(ttt)==None:
                word[ttt]=1
                tt.append(ttt)
    #print(first_sn)
    #print(' ')

    if len(tt) == 0:
        print('無適合的標題')
        tt.append("無適合的標題")
        return tt
    return tt
def ajax_AiToTitle_Img(request):
    word={}
    ImgStrPath = '''  
                            <div class="card mb-4">
                                <div class="card-header" ><i class="fas fa-chart-cloud mr-1"></i>腳本生成中</div>
                                        <div >
                                        <img class="adfsdfas" id='Statistics_One' name='Statistics_One'  src='/static/images/VKTitle.gif' alt="" width="1100" height="1100">
                                        </div>
                                <div class="card-body"><canvas id="myAreaChart" width="100%" height="40"></canvas></div>
                            </div>

                                        '''
    word['VideoUrl'] = ImgStrPath
    return JsonResponse(word)
def AjaxTitle(request):
    word={}

    ImgStrPath = '''

                            <div class="card mb-4">
                                <div class="card-header" ><i class="fas fa-chart-cloud mr-1"></i>標題生成中</div>
                                        <div >
                                        <img class="adfsdfas" id='Statistics_One' name='Statistics_One'  src='/static/images/AiTitle.gif' alt="" width="1100" height="1100">
                                        </div>
                                <div class="card-body"><canvas id="myAreaChart" width="100%" height="40"></canvas></div>
                            </div>

                                        '''

    word['VideoUrl']=ImgStrPath
    return JsonResponse(word)
def AiToTitle(request):
    if "Article" in request.GET:
        Article=request.GET["Article"]
        df=pd.DataFrame(data=[{"Article":Article}],columns=["Article"])
        try:
            ip = request.META['REMOTE_ADDR']
        except:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        # AiTitle = {"AiTitle": {
        #     "MakeTitle": None,
        #     "MakeArticle": Article
        # }}
        JoinIp="".join(ip.split("."))
        df.to_csv(pwd+r"/{}.csv".format(JoinIp),encoding="utf-8-sig",index=0)
        txt_Name = '{}.txt'.format(JoinIp)
        count=0
        Folder_Path=pwd
        while True:  # 每秒檢查是否有TXT
            file_list = os.listdir(Folder_Path)  # 這個資料夾內所有的檔案名稱
            txt_list = []
            for i in file_list:
                if '.txt' in i:
                    txt_list.append(i)
            if (txt_Name not in txt_list):  # 是否有這個VideoID做為檔名的圖片
                time.sleep(1)
                count += 1  # 每秒加一次
            else:
                OpenTxt = open(pwd+r"/{}.txt".format(JoinIp), "r",encoding="utf-8-sig")
                MakeArticle = OpenTxt.readlines()[0]
                return render_to_response('AiToTitle.html', locals())
            if count >= 600:  # 600秒都沒有做出圖片跳出迴圈 不傳圖片了
                return render_to_response('AiToTitle.html', locals())
        return render_to_response('AiToTitle.html', locals())
    elif "UserArticle" in request.GET:
        Article=request.GET["UserArticle"]
    #     AiTitle = {"AiTitle": {
    #     "MakeTitle": Article,
    #     "MakeArticle":None
    # }}
    #     try:
    #         ip = request.META['REMOTE_ADDR']
    #     except:
    #         ip = request.META['HTTP_X_FORWARDED_FOR']
    #     try:
    #         kafka_producer.producer(kafka_producer.Els(ip, "AiTitle", AiTitle["AiTitle"]))
    #     except:
    #         pass
        Title_list=summary_candidate_fin(Article)
        return render_to_response('AiToTitle.html',locals())
    return render_to_response('AiToTitle.html', locals())





