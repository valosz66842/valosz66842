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
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import JsonResponse
# Create your views here.
# Create your views here.
# Create your views here.
from confluent_kafka import Producer
import joblib
import sys
pwd=os.path.dirname(__file__)
sys.path.append(pwd+"../kafka_producer.py")
import kafka_producer
def prediction(MainFollow,VideoAvgLike,FeatFollow,FeatAvgLike):
    loaded_model = joblib.load(pwd+r"/lnrg_model.sav")
    loaded_RFmodel = joblib.load(pwd+r"/RF_rg_model.sav")
    at=[[MainFollow,VideoAvgLike,FeatFollow,FeatAvgLike]]
    Ln=loaded_model.predict(at)
    Rf=loaded_RFmodel.predict(at)
    return int(Ln),round(float(Rf),2)
def FeatFlow(request):
    # LnFeatPredict,RfFeatPredict=prediction(546546,978978,97878,798798)
    Class_list=["娛樂類","人物與部落客","教育類","電影與動畫","遊戲類"]
    if 'VideoAvgLike' in request.GET and request.GET['VideoAvgLike'] != '':
        a=float(1.0)
        VideoAvgLike=float(request.GET["ChannelVideoFollow"])
        Channel_Follow =float(request.GET["VideoAvgLike"])
        FeatFollow=float(request.GET["FeatFollow"])
        FeatVideoAvgLike=float(request.GET["FeatVideoAvgLike"])
        # if "FeatTable" in request.session:  # 檢查指定的session是否存在
        #     meowdate = request.session["FeatTable"]
        #     meow = "\static\images\\" + str(request.session["FeatTable"]) + ".jpg"
        # FeatFlow = {"FeatFlow": {
        #       "MainFollow": VideoAvgLike,
        #       "ChannelAvgLook": Channel_Follow,
        #       "FeatFollow": FeatFollow,
        #       "FeatAvgLook": FeatVideoAvgLike,
        #       "FeatTable":None
        # }}
        # try:
        #     ip = request.META['REMOTE_ADDR']
        # except:
        #     ip = request.META['HTTP_X_FORWARDED_FOR']
        # try:
        #     kafka_producer.producer(kafka_producer.Els(ip,"FeatFlow", FeatFlow["FeatFlow"]))
        # except:
        #     pass
        LnFeatPredict,RfFeatPredict=prediction(VideoAvgLike,Channel_Follow,FeatFollow,FeatVideoAvgLike)
        return render_to_response('FeatFlow.html',locals())
    return render_to_response('FeatFlow.html', locals())
def ajax_featflow(request):
    if request.GET.get("Feat_Class")!='':
        UserClass=request.GET.get("Feat_Class")
        # FeatFlow = {"FeatFlow": {
        #       "MainFollow": None,
        #       "ChannelAvgLook": None,
        #       "FeatFollow": None,
        #       "FeatAvgLook": None,
        #       "FeatTable": UserClass
        # }}
        # try:
        #     ip = request.META['REMOTE_ADDR']
        # except:
        #     ip = request.META['HTTP_X_FORWARDED_FOR']
        # try:
        #     kafka_producer.producer(kafka_producer.Els(ip,"FeatFlow", FeatFlow["FeatFlow"]))
        # except:
        #     pass
        request.session["FeatTable"] = UserClass
        ImagePath="/static/images/{}.jpg".format(UserClass)
        Grapt=''' 
                                    <div class="card mb-4">
                                        <div class="card-header"><i class="fas fa-chart-bar mr-1"></i>{}一年內合作影片數量</div>
                                            <img class="card-img-top"   src='{}' alt="">
                                        <div class="card-body"><canvas id="myAreaChart" width="100%" height="40%"></canvas></div>
                                    </div>
                            
        '''.format(UserClass,ImagePath)
        word={}
        word[UserClass]=Grapt
        return JsonResponse(word)
