#coding:utf-8
from .forms import PostForm,YoutubeForm
from django.shortcuts import render
from .models import Post
from django import template
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
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
from .models import Restaurant,Food
from django.http import JsonResponse
from django.shortcuts import render_to_response
import random
Img_Size = '''
    width="100" height="150"
'''
pwd=os.path.dirname(__file__)
ImgPath = pwd+r'/static/images'
os.chdir(ImgPath)  # 換工作路徑
file_list = os.listdir(ImgPath)  # 這個資料夾內所有的檔案名稱
PngName = []
for i in file_list[::-1]:
    PngName.append(i)
def ajax_index_Img(request):
    word={}
    i=random.sample(PngName,1)
    Greap='''<img class ="card1-img1-top1" src="\static\images\{}" alt="" {}>'''.format(i[0],Img_Size)
    word[i[0]] = Greap
    return JsonResponse(word)
def index(request):
    return render_to_response('index.html', locals())
