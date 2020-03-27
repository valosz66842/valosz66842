import requests
from bs4 import BeautifulSoup
import json
import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import pandas as pd
import os
import time
import shutil
import csv
import pymongo as pm
import datetime
from pprint import pprint

Folder_Path = r'E:\csv'  #csv目標資料夾
class MongoOperator:
    def __init__(self, host, port, db_name, default_collection): #mongo port:27017
        self.client = pm.MongoClient(host=host, port=port)        #建立資料庫連線
        self.db = self.client.get_database(db_name)        #選擇相應的資料庫名稱
        self.collection = self.db.get_collection(default_collection)        #設定預設的集合
    def insert(self, item, collection_name =None): #增加資料 目錄,檔名
        if collection_name != None:
            collection = self.db.get_collection(self.db)
            collection.insert(item)
        else:
            self.collection.insert(item)
    def find(self, expression =None, collection_name=None): #查詢 expression:條件 collection_name:檔名
        if collection_name != None:
            collection = self.db.get_collection(self.db)
            if expression == None:
                return collection.find()
            else:
                return collection.find(expression)
        else:
            if expression == None:
                return self.collection.find()
            else:
                return self.collection.find(expression)
    def get_collection(self, collection_name=None):#查詢集合內容物
        if collection_name == None:
            return self.collection
        else:
            return self.get_collection(collection_name)
today = str(datetime.date.today()).split('-')[0] + \
       str(datetime.date.today()).split('-')[1] + \
   str(datetime.date.today()).split('-')[2]

os.chdir(Folder_Path) #換工作路徑
file_list = os.listdir() #這個資料夾內所有的檔案名稱
file_csv=[]
for file in file_list: #只讀csv檔
    if '.csv' in file:
        file_csv.append(file)
db = MongoOperator('10.120.26.31', 27017, 'db{}'.format(today),'save{}'.format(today))  # IP 目錄 檔名

for i in range(len(file_csv)):  # 讀所有檔案
    with open(Folder_Path+'/{}'.format(file_csv[i]), 'r', encoding="utf-8-sig") as f:  # 讀檔案
        reader=csv.reader(f)
        fieldnames = next(reader)
        csv_reader = csv.DictReader(f,fieldnames=fieldnames)  # self._fieldnames = fieldnames   # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:#資料
            d = {}
            for k, v in row.items():#儲存
                d[k] = v
            db.insert(d)
for i in db.find():
    print(i)



