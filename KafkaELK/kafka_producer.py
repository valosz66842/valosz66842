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
import datetime
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

def Els(ip,key,WebDict):
    FeatFlow= {"FeatFlow":{
        "MainFollow": None,
        "ChannelAvgLook": None,
        "FeatFollow": None,
        "FeatAvgLook": None,
        "FeatTable": None
    }}
    AiTitle = {"AiTitle":{
        "MakeTitle": None,
        "MakeArticle":None
    }}
    MessageEmotion= {"MessageEmotion":{
        "VideoUrl": None
    }}
    YoutubeFlow = {"YoutubeFlow":{
        "ChannelVideoLookMedian": None,
        "ChannelVideoLookAvg": None,
        "ChannelFollow": None,
        "OneHourFlow": None
    }}
    YoutubeReport = {"YoutubeReport":{
        "ChannelClass": None,
        "Channel_Avg_Look": None
    }}
    NewsWordCloud= {"NewsWordCloud":{
        "SelectDate":None,
        "KeyWord":None,
        "BarDateCount":None
    }
    }
    if key=="NewsWordCloud":
        NewsWordCloud={"NewsWordCloud":WebDict}
    if key=="FeatFlow":
        FeatFlow = {"FeatFlow":WebDict}
    if key=="AiTitle":
        AiTitle = {"AiTitle":WebDict}
    if key=="MessageEmotion":
        MessageEmotion = {"MessageEmotion":WebDict}
    if key=="YoutubeReport":
        YoutubeReport = {"YoutubeReport":WebDict}
    if key=="YoutubeFlow":
        YoutubeFlow={"YoutubeFlow":WebDict}
    ElsDict={}
    Date = '%Y-%m-%d'
    Time='%H:%M:%S'
    ElsDict["ip"]=ip
    ElsDict["Date"]=datetime.datetime.now().strftime(Date)
    ElsDict["Time"]=datetime.datetime.now().strftime(Time)
    ElsDict.update(NewsWordCloud)
    ElsDict.update(FeatFlow)
    ElsDict.update(AiTitle)
    ElsDict.update(MessageEmotion)
    ElsDict.update(YoutubeFlow)
    ElsDict.update(YoutubeReport)
    return ElsDict
def producer(kafka_value):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_port =s.getsockname()[0]+":9092"
    s.close()
    value = json.dumps(kafka_value, ensure_ascii=False)
    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        # Kafka集群在那裡?
        'bootstrap.servers': ip_port  # <-- 置換成要連接的Kafka集群
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(props)
    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName = 'LongMoonTest'
    # produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])
    producer.produce(topicName, value=value)#傳送進去 Topic,data
    # 步驟5. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()