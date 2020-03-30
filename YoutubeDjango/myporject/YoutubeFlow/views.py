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
from sqlalchemy import create_engine
from confluent_kafka import Producer
from confluent_kafka import Consumer, KafkaException, KafkaError

# Create your views here.
# Create your views here.
import joblib
from django.views.decorators.csrf import csrf_exempt
import sys
pwd=os.path.dirname(__file__)
# sys.path.append(pwd+"../kafka_producer.py")
# import kafka_producer

def prediction(MainFollow,VideoAvgLike,FeatFollow,FeatAvgLike):
    loaded_RFmodel = joblib.load(pwd+r"/RF_rg_model.sav")
    loaded_LRmodel = joblib.load(pwd+r"/LR_rg_model.sav")
    loaded_DTmodel = joblib.load(pwd+r"/DT_rg_model.sav")
    loaded_KNNmodel = joblib.load(pwd+r"/KNN_rg_model.sav")

    at=[[MainFollow,VideoAvgLike,FeatFollow,FeatAvgLike]]
    Ln=loaded_LRmodel.predict(at)
    Rf=loaded_RFmodel.predict(at)
    KNN=loaded_KNNmodel.predict(at)
    DT=loaded_DTmodel.predict(at)
    return round(float(Ln),0),int(Rf),round(float(KNN),0),round(float(DT),0)
def YoutubeFlow(request):
    if 'VideoAvgLike' in request.GET and request.GET['VideoAvgLike'] != '':
        VideoAvgLike=float(request.GET["VideoAvgLike"])
        ChannelFollow =float(request.GET["ChannelFollow"])
        OneHourFlow=float(request.GET["OneHourFlow"])
        ChannelMedian=float(request.GET["ChannelMedian"])
    #     YoutubeFlow = {"YoutubeFlow":{
    #     "ChannelVideoLookMedian": ChannelMedian,
    #     "ChannelVideoLookAvg": VideoAvgLike,
    #     "ChannelFollow": ChannelFollow,
    #     "OneHourFlow": OneHourFlow
    # }
    #     }
    #     try:
    #         ip = request.META['REMOTE_ADDR']
    #     except:
    #         ip = request.META['HTTP_X_FORWARDED_FOR']
    #     try:
    #         kafka_producer.producer(kafka_producer.Els(ip,"YoutubeFlow", YoutubeFlow["YoutubeFlow"]))
    #     except:
    #         pass
        LnPredict,RfPredict,KNNPredict,DTPredict=prediction(ChannelMedian,VideoAvgLike,ChannelFollow,OneHourFlow)
        return render_to_response('YoutubeFlow.html',locals())
    else:
        return render_to_response('YoutubeFlow.html',locals())

def ajax_youtube(request):###可以直接進來這裡的嗎 還是要去 Flow那邊
    word={}
    return JsonResponse(word)
def ajax_youtube_Img(request):
    word={}
    return JsonResponse(word)