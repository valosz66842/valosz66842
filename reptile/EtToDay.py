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
import sys
from opencc import OpenCC
def save(title, date, content, link):
    df = pd.DataFrame(
        data=[{
            'title': title,
            'date': date,
            'content': content,
            'link': link,
        }],
        columns=['title', 'date', 'content', 'link'])
    return df
url='https://www.ettoday.net/news/news-list-2020-3-1-0.htm'
html=requests.get(url)
soup=BeautifulSoup(html.text,'html.parser')
each_article=soup.select("div[class='part_list_2']")[0].findAll("a")
EtToDay_Pandas=pd.DataFrame()
word_dict={}
page=0
tFile='20200229.xml'
for j in range(1,5000):
    for article in each_article:
        title=article.text
        print(article.text)
        # print('https://www.ettoday.net/'+article['href'])
        link='https://www.ettoday.net/'+article['href']
        article_html=requests.get(link)
        article_soup=BeautifulSoup(article_html.text,'html.parser')
        content=''
        article_content=article_soup.select("div[class='story']")
        for Pcontent in article_content:
            Pcontent=Pcontent('p')
            for i in Pcontent:
                content+=i.text
        try:
            article_date=article_soup.select("time[class='date']")[0].text.strip().split(' ')[0]
        except:
            article_date = article_soup.select("time[class='news-time']")[0].text.strip().split(' ')[0]
        date=article_date[:4]+article_date[5:7]+article_date[8:10]
        df=pd.DataFrame()
        print(date)
        if word_dict.get(title)==None:
            df=save(title,date,content,link)
            EtToDay_Pandas=EtToDay_Pandas.append(df)
            word_dict[title]=1
    page+=1
    para = {'offset': page,
            'tPage': '3',
            'tFile':tFile,
            'tOt':'0',
            'tSi':'100',
            'tAr':'0'}

    # 'itct': 'CDIQybcCIhMIx5HpptOR5wIVxZnCCh0mTAlx'} #"search_query": "博恩夜夜"代表關鍵字是博恩夜夜 。"sp":"EgIQAQ%3D%3D" 代表此搜尋只找出影片
    html = requests.post('https://www.ettoday.net/show_roll.php', data=para)
    each_article = BeautifulSoup(html.text, 'html.parser').findAll("a")
    if page%50==0:
        EtToDay_Pandas.to_csv('E:\EtToDay\EtToDay{}.csv'.format(page),index=0,encoding="utf-8-sig")
        EtToDay_Pandas=pd.DataFrame()
    EtToDayDate=date[:4]+'-'+date[5]+'-'+str(int(date[6:]))
    if len(each_article)==0:
        url = 'https://www.ettoday.net/news/news-list-{}-0.htm'.format(EtToDayDate)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        each_article = soup.select("div[class='part_list_2']")[0].findAll("a")
        tFile=date+'.xml'