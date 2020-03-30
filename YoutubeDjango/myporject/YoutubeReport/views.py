import os
import os
import requests
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render_to_response
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

from confluent_kafka import Producer, Consumer
import socket
# Create your views here.
# Create your views here.
import sys
pwd=os.path.dirname(__file__)
# sys.path.append(pwd+"../kafka_producer.py")
# import kafka_producer
# sys.path.append(pwd+"../UserMongoDB.py")
# import UserMongoDB
Img_Size = '''
    width="900" height="600"
'''


def UserClassPandas():
    FilePath=pwd+r'/流量分類.csv'
    ClassPd=pd.read_csv(FilePath)
    return ClassPd
def EnglishToChinese(string):
    if string=='教育類':
        return 'Education'
    if string=='娛樂類':
        return 'Entertainment'
    if string=='遊戲類':
        return 'Game'
    else:
        return 'Movie'
def Get_Avg_Look(string):
    if string=='20萬以上':
        return 'TOP1'
    if string=='5萬至20萬':
        return 'TOP2'
    if string=='2萬至5萬':
        return 'TOP3'
    if string=='2萬以下':
        return 'TOP4'

def ajax_YoutubeReport_Img(request):
    if request.GET.get("channel_class")!='':
        User_Select_Class=request.GET.get("channel_class") #取得分類
        # YoutubeReport = {"YoutubeReport": {
        #     "ChannelClass": User_Select_Class,
        #     "Channel_Avg_Look": None
        # }}
        # try:
        #     ip = request.META['REMOTE_ADDR']
        # except:
        #     ip = request.META['HTTP_X_FORWARDED_FOR']
        # try:
        #     kafka_producer.producer(kafka_producer.Els(ip,"YoutubeReport", YoutubeReport["YoutubeReport"]))
        # except:
        #     pass
        category = EnglishToChinese(User_Select_Class)
        word={}
        GraphData=''
        ImgPathFile = pwd+r'/static/images/cat_image/{}'.format(category)
        os.chdir(ImgPathFile)  # 換工作路徑
        file_list = os.listdir(ImgPathFile)  # 這個資料夾內所有的檔案名稱
        PngName = []
        for i in file_list:
            if 'png' in i:
                PngName.append(i)

        for n,name in enumerate(PngName):
            category_name=["影片發佈時間點分析","影片發佈流量高峰期",'主要發片時間點與流量高峰期相對關係','影片發佈流量高峰期']
            if 'hist' in name:
                GraphClass='bar'
            elif 'line' in name:
                GraphClass='area'
            ImgClass=EnglishToChinese(User_Select_Class)
            GraphCount='{}'.format(i)
            ValueName='stream{}'.format(i)
            ImgStrPath = '/static/images/cat_image/{}/{}'.format(category,name)
            GraphData+= '''             <div class="col-xl-6">
                                            <div class="card mb-4">
                                                <div class="card-header"><i class="fas fa-chart-{} mr-1"></i>{}</div>
                                                <div class="card-img-top" id='Statistics_{}' name='Statistics_{}'  alt="">
                                                     '<img value='{}' src='{}'  {}/>'</div>
                                                <div class="card-body"><canvas id="my{}raph" width="100%" height="40"></canvas></div>
                                            </div>
                                        </div>
                                        '''.format(GraphClass, User_Select_Class+category_name[n], GraphCount, GraphCount,name[:-4], ImgStrPath,Img_Size,name[:-4])
        DataPd=UserClassPandas()
        Channel_Avg_Look_Pandas=DataPd['均觀看數']
        GraphData+='''
                    
                                <div class="card bg-warning text-white mb-4">
                                    <div class="card-body">請選擇此分類區間</div>
                                    <div class="card-footer d-flex align-items-center justify-content-between">
                                        <form  method="get" enctype="multipart/form-data" class="OptionWordCloud">
                                             <select id="Channel_Avg_Look" name="Channel_Avg_Look" method="get" style="width:300px;">
                                                    <option></option>'''
        for Channel_Avg_Look_Interval in  Channel_Avg_Look_Pandas:
            GraphData +='''                        <option  id="{}" name="{}" type="text">{}</option>
                                                    '''.format(Channel_Avg_Look_Interval,Channel_Avg_Look_Interval,User_Select_Class+Channel_Avg_Look_Interval)

        GraphData +='''
                                             </select>
                                        </form>
                                        <div class="small text-white"><i class="AsNoClass"></i></div>
                                    </div>
                                </div>

                        '''
        GraphData +='''</div>
                    <div class="row" id="UserClassSelectGreap">
                     <script language="JavaScript2">
                         $("#Channel_Avg_Look").change(function()
                            {
                              $.ajax
                              (
                                  {
                                      url: 'ajax/ajax_Two_YoutubeReport_Img/',
                                      data:{"Channel_Avg_Look":$(this).val()},
                                      type: 'GET',
                                      dataType: 'json',
                                      success: function (data)
                                      {
                                        var content='';
                                        $.each
                                        (
                                            data,function(key,value)
                                            {
                                                {
                                                  content+='<div name='+key+' class="row"> '+value+' </div>'
                                                }
                                            }
                                        );
                                         $('#UserClassSelectGreap').html(content)
                                      },
                                  }
                              );
                            }
                        );
                        </script>'''

        word[User_Select_Class]=GraphData
        return JsonResponse(word)
def ajax_Two_YoutubeReport_Img(request):
    if request.GET.get("Channel_Avg_Look")!='':
        User_Select_Class = request.GET.get("Channel_Avg_Look")
        if "電影與動畫" in User_Select_Class:
            category_ch = User_Select_Class[:5]
            category=EnglishToChinese(User_Select_Class[:5])
            TOP_Count=Get_Avg_Look(User_Select_Class[5:])
        else:
            category_ch=User_Select_Class[:3]
            category=EnglishToChinese(User_Select_Class[:3])
            TOP_Count=Get_Avg_Look(User_Select_Class[3:])

        word = {}
        ImgPath=pwd+r"/static/images/cat_image/{}/{}_{}".format(category,category,TOP_Count)
        os.chdir(ImgPath)  # 換工作路徑
        file_list = os.listdir(ImgPath)  # 這個資料夾內所有的檔案名稱
        PngName = []
        for i in file_list:
            if 'png' in i:
                PngName.append(i)
        GraphData = ''
        # YoutubeReport = {"YoutubeReport": {
        #     "ChannelClass": category_ch,
        #     "Channel_Avg_Look": User_Select_Class
        # }}
        # try:
        #     ip = request.META['REMOTE_ADDR']
        # except:
        #     ip = request.META['HTTP_X_FORWARDED_FOR']
        # try:
        #     UserMongoDB.SaveMongoDB(UserMongoDB.Els(ip,"YoutubeReport", YoutubeReport["YoutubeReport"]))
        # except:
        #     pass
        for n,name in enumerate(PngName):
            name = str(name)
            if 'hist' in name:
                GraphClass = 'bar'
            elif 'line' in name:
                GraphClass = 'area'
            category_name = ["影片發佈時間點分析", "影片發佈流量高峰期", '主要發片時間點與流量高峰期相對關係', '影片發佈流量高峰期']
            ImgClass = EnglishToChinese(User_Select_Class)
            GraphCount = '{}'.format(i)
            ValueName = 'stream{}'.format(i)
            ImgStrPath = '/static/images/cat_image/{}/{}_{}/{}'.format(category,category,TOP_Count,name)
            GraphData += '''             <div class="col-xl-6">
                                                    <div class="card mb-4">
                                                        <div class="card-header"><i class="fas fa-chart-{} mr-1"></i>{}</div>
                                                        <div class="card-img-top" id='Statistics_{}' name='Statistics_{}'  alt="">
                                                             '<img value='{}' src='{}' {} />'</div>
                                                        <div class="card-body"><canvas id="my{}raph" width="100%" height="40"></canvas></div>
                                                    </div>
                                                </div>
                                                '''.format(GraphClass, User_Select_Class+category_name[n], GraphCount, GraphCount, ValueName,
                                                           ImgStrPath,Img_Size,i)
        word[User_Select_Class] = GraphData
        print(word)
        return JsonResponse(word)
def YoutubeReport(request):
    DataPd=UserClassPandas() #取得建呈提供的欄位
    Channel_Class_Pandas=DataPd['類別']#用在網頁上下拉式選單
    Channel_Class_Pandas.dropna(axis=0, how='any', inplace=True)#刪除下拉式選單的空值
    return render_to_response('YoutubeReport.html',locals())#只要有這行就可以讀取html檔顯示網頁
# Create your views here.
