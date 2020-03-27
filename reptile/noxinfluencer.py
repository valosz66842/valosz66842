import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from urllib import request, parse
import os
import time
import lxml.html
import datetime
import csv
import re
from opencc import OpenCC
page=1
kind=['entertainment','gaming','film+%26+animation','education','people+%26+blogs']
cc = OpenCC('s2t')
def save(name,class_,fans,like,channel_id):
    df = pd.DataFrame(
        data=[{
            'name': name,
            'class_': class_,
            'fans': fans,
            'like': like,
            'channel_id':channel_id
        }],
        columns=['name','class_','fans','like','channel_id'])
    return df
def save_True(str,kind):
    if str=='娛樂類' and kind=='entertainment':
        return True
    elif str=='教育類' and kind=='education':
        return True
    elif str=='電影與動畫' and kind=='film+%26+animation':
        return True
    elif str=='遊戲類' and kind=='gaming':
        return True
    elif str=='人物與部落客' and kind=='people+%26+blogs':
        return True
    else:
        return False
def fans_count(string):
    if '萬' in string:
        i=float(string.split('萬')[0])*10000
        return i
    else:
        return float(string)
name_all=[]
class_all=[]
fans_all=[]
like_all=[]
Joblist=pd.DataFrame()
#
page=1
count = 0
i=0
url = 'https://tw.noxinfluencer.com/youtube-channel-rank/_influencer-rank?country=tw&category={}&rankSize=1000&type=0&interval=weekly&pageNum={}'.format(kind[0], page)
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
for n, kind_start in enumerate(kind):
    i=0
    count=0
    page=1
    url = 'https://tw.noxinfluencer.com/youtube-channel-rank/_influencer-rank?country=tw&category={}&rankSize=1000&type=0&interval=weekly&pageNum={}'.format(kind_start, page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    while(count<150):
        try:
            name=(soup.select("td[class='profile']")[i].text).strip()
            class_=(soup.select("td[class='text category']")[i].text).strip()
            fans=((soup.select("td[class='text followerNum with-num']")[i].text).strip()).split(' ')[0]
            like=((soup.select("td[class='text avgView with-num']")[i].text).strip()).split(' ')[0]
            channel_id = soup.select("td[class='profile']")[i]('a')[0]['href'].split('/')[-1]
            fans=fans_count(fans)
            like=fans_count(like)
            i+=1
            if i ==50:
                page+=1
                i=0
                url = 'https://tw.noxinfluencer.com/youtube-channel-rank/_influencer-rank?country=tw&category={}&rankSize=1000&type=0&interval=weekly&pageNum={}'.format(kind_start, page)
                res = requests.get(url)
                soup = BeautifulSoup(res.text, 'html.parser')
            if save_True(class_,kind_start)==True:
                df=save(cc.convert(name),class_,fans,like,channel_id)
                Joblist=Joblist.append(df,ignore_index=True)
                count+=1
        except:
            break
Joblist.to_csv("E:Youtube/150AimeYoutube.csv",encoding='utf-8-sig',index=False,header=True)
Joblist=pd.DataFrame()

