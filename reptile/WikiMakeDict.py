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
from opencc import OpenCC #pip install opencc-python-reimplemented
cc = OpenCC('s2t')
def save(title):
    df = pd.DataFrame(
        data=[{
            'title': title,
        }],
        columns=['title'])
    return df
# with open('E:/csv/ds.txt', "r") as f:    #開啟檔案
#     data = f.read()
# print(data)
# dic=data.split(' ')
# print(dic)
joblist=pd.DataFrame()
break_true=False
t=False
# for i in range(len(dic)):
#     df=save(dic[i])
#     jslist=jslist.append(df,ignore_index=True)
# jslist.to_csv('E:/csv/dict.csv',encoding="utf-8-sig")
count=0
passcount=0
word_count={}
with open(r'E:\dict\暫時用不到\歷史資料\2.0\dict4.txt','r',encoding="utf-8-sig") as f:
    reader=csv.reader(f) #讀檔案內容
    for row in reader:
        try:
            break_true = False
            url='https://zh.wikipedia.org/wiki/%s'%(row[0])
            res=requests.get(url)
            soup=BeautifulSoup(res.text,'html.parser')
            list=soup.select('div[class="mw-parser-output"]')
            for dicts in list: #抓詞
                dicts=dicts('p')
                for s in dicts:
                    s=s('a')
                    for i in range(len(s)):#每一個詞
                        t = False
                        count+=1
                        if '尋找「' in s[i].text:
                            break_true = True#紀錄是否為空
                            print('這個頁面是空的')
                            break
                        if ('[' in s[i].text or s[i].text.isdigit()==True) or len(s[i].text)>15: #只有數字略過或是長度>15掠過
                            pass
                        else:
                            print(count,cc.convert(s[i].text))
                            if ( word_count.get(cc.convert(s[i].text) )) == None:  # 沒存過存進去
                                df = save(cc.convert(s[i].text))  # 儲存每一個詞
                                print(cc.convert(s[i].text) + '存入')
                                joblist = joblist.append(df, ignore_index=True)
                                word_count[cc.convert(s[i].text)] = 1
                            else:
                                print('存過',cc.convert(s[i].text))
                if break_true == True:#若空找下一個詞
                    break
        except:
            print('----')
            if (passcount>3):
                break
            passcount+= 1
            pass
joblist.to_csv('E:/dict/dicts.csv',encoding="utf-8-sig",index=0,header=False)