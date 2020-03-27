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
FeatPath='E:\YoutubeYear'
FeatName=''
os.chdir(FeatPath) #換工作路徑
file_list = os.listdir() #這個資料夾內所有的檔案名稱
def save(channel_id,video_title,video_id,view_count,publish_time): #此頻道所有影片
    df=pd.DataFrame(
        data=[{'channel_id': channel_id,
               'video_title': cc.convert(video_title),
               'video_id': video_id,
               'view_count': view_count,
               'publish_time': publish_time}],
        columns=['channel_id','video_title','video_id','view_count','publish_time']
    )
    return df
Joblist=pd.DataFrame()
for i in range(len(file_list)): #讀所有檔案
    with open(FeatPath+'/{}'.format(file_list[i]),'r',encoding='utf-8-sig') as f:
        reader=csv.reader(f)
        for row in reader:
            if 'feat' in row[1] or 'ft' in row[1]:
                if 'Minecraft' not in row[1]:
                    df=save(row[0],row[1],row[2],row[3],row[4])
                    Joblist=Joblist.append(df,ignore_index=True)
Joblist.to_csv(FeatPath+'/{}Feat.csv'.format(FeatName),index=0,encoding='utf-8-sig')


