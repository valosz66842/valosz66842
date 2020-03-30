from django.shortcuts import render
from django.shortcuts import render
from django import template
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse
from datetime import datetime
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
import random
from confluent_kafka import Producer
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import JsonResponse
import sys
pwd=os.path.dirname(__file__)
# sys.path.append(pwd+"../kafka_producer.py")
# import kafka_producer
# Create your views here.
# Create your views here.
# Create your views here.
Img_Size = '''
    width="1000" height="858"    
'''

def ajax_NewWordCloud_Img(request):
    User_Select_Class = request.GET.get("date")
    request.session["Last"]=User_Select_Class
    word = {}
    GraphClass = 'cloud'
    GraphData = ''
    i='1'
    # NewsWordCloud = {"NewsWordCloud": {
    #     "SelectDate": User_Select_Class,
    #     "KeyWord": None,
    #     "BarDateCount": None
    # }
    # }
    # try:
    #     ip = request.META['REMOTE_ADDR']
    # except:
    #     ip = request.META['HTTP_X_FORWARDED_FOR']
    # kafka_producer.producer(kafka_producer.Els(ip, "NewsWordCloud", NewsWordCloud["NewsWordCloud"]))

    PatternName = str(User_Select_Class)+'文字雲'
    GraphCount = '{}'.format(i)
    ValueName = 'stream{}'.format(i)
    ImgStrPath = '/static/images/{}.png'.format(User_Select_Class)
    GraphData += '''             

                                                <div class="card-header"><i class=""></i>{}</div>
                                                <div class="card-img-top" id='Statistics_{}' name='Statistics_{}'  alt="" >
                                                     '<img value='{}' src='{}' {} />'</div>
                                                <div class="card-body"><canvas id="my{}raph" width="100%" height="40%"></canvas></div>
                                        
                                        '''.format(PatternName, GraphCount, GraphCount, ValueName,
                                                   ImgStrPath,Img_Size,i)
    word[User_Select_Class] = GraphData
    print(word)
    return JsonResponse(word)


def NewWordCloud(request,JsonDictName=None):
    FilePath = pwd
    JsonPath = pwd
    os.chdir(JsonPath)  # 換工作路徑
    file_list = os.listdir(JsonPath)  # 這個資料夾內所有的檔案名稱
    JsonName = []
    global Page
    Page=1
    for i in file_list[::-1]:
        if 'json' in i:
            if 'wordcount_2020.json' not in i:
                JsonName.append(i)
    JsonPath = random.sample(JsonName, 1)[0]

    OpenJson = open(pwd+r'/{}'.format(JsonPath), 'r',encoding="utf-8-sig")
    OpenJson=json.load(OpenJson)
    JsonPath=JsonPath[:-5]
    global AjaxDict
    AjaxDict=OpenJson
    # JsonKey=random.sample((OpenJson.keys()),10)
    JsonKey = OpenJson.keys()
    JsonDict={}
    for n,i in enumerate(JsonKey):
        JsonDict[i]=OpenJson[i]
        if n==9:
            break
    ImgPath = pwd+r'/static/images'
    os.chdir(ImgPath)  # 換工作路徑
    file_list = os.listdir(ImgPath)  # 這個資料夾內所有的檔案名稱
    PngName=[]
    for i in file_list[::-1]:
        if 'png' in i:
            PngName.append(i[:-4])

    if "Last" in request.session:  # 檢查指定的session是否存在
        meowdate=request.session["Last"]
        meow="\static\images\\"+str(request.session["Last"])+".png"
    try:
        if request.GET["KeyWord"]!=("" or None) and request.GET["InputDay"]!=("" or None):
            KeyWord=request.GET["KeyWord"]
            InputDay=request.GET["InputDay"]
            df=pd.DataFrame(data=[{"KeyWord":KeyWord,"InputDay":InputDay}],columns=["KeyWord","InputDay"])
            df.to_csv(pwd+r"/static/plt/{}{}.csv".format(KeyWord,InputDay),encoding="utf-8-sig",index=0)
            GraphData = ''
            Image_Name = str(KeyWord)+str(InputDay) + '.png'  # 做出圖片檔案名稱
            Folder_Path = (pwd+r"/static/plt")  # 做為檢查是否有儲存圖片的路徑
            count = 0  # 計算時間
            # try:
            #     NewsWordCloud = {"NewsWordCloud": {
            #         "SelectDate": meowdate,
            #         "KeyWord": KeyWord,
            #         "BarDateCount": InputDay
            #     }
            #     }
            # except:
            #     NewsWordCloud = {"NewsWordCloud": {
            #         "SelectDate": None,
            #         "KeyWord": KeyWord,
            #         "BarDateCount": InputDay
            #     }
            #     }
            # try:
            #     ip = request.META['REMOTE_ADDR']
            # except:
            #     ip = request.META['HTTP_X_FORWARDED_FOR']
            # try:
            #     kafka_producer.producer(kafka_producer.Els(ip, "NewsWordCloud", NewsWordCloud["NewsWordCloud"]))
            # except:
            #     pass
            while True:  # 每秒檢查是否有圖檔
                file_list = os.listdir(Folder_Path)  # 這個資料夾內所有的檔案名稱
                file_png = []
                for i in file_list:
                    if "png" in i:
                        file_png.append(i)
                if Image_Name not in file_list:  # 是否有這個VideoID做為檔名的圖片
                    time.sleep(1)
                    count += 1  # 每秒加一次
                else:
                    Pie_Image = '/static/plt/{}'.format(Image_Name)
                    return render_to_response('NewWordCloud.html', locals())
                if count >= 20:  # 20秒都沒有做出圖片跳出迴圈 不傳圖片了
                    return render_to_response('NewWordCloud.html', locals())
    except:
        pass
    return render_to_response('NewWordCloud.html',locals())


def Json_Ajax(request):
    word = {}
    JsonDict=AjaxDict
    JsonKey=[]
    global Page
    k=Page
    for i in JsonDict.keys():
        JsonKey.append(i)
    for i in JsonKey[k*10:k*10+10]:
        word[i]=JsonDict[i]
    Page+=1
    return JsonResponse(word)

