import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import pandas as pd
import os
import time
import shutil
import csv
from pprint import pprint
import pymongo as pm
import datetime
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

###把目標資料夾所有json傳進mongo
JsonFile_Path = r'E:\json'  # 保存路徑
os.chdir(JsonFile_Path) #換工作路徑
file_list = os.listdir() #這個資料夾內所有的檔案名稱
file_json=[]
for file in file_list: #只讀json檔
    if '.json' in file:
        file_json.append(file)

for i in range(0, len(file_json)):  # 讀所有檔案
    with open('E:/json/%s'%(file_json[i]), 'r', encoding="utf-8-sig") as f:  # 讀檔案
        result_data=json.load(f) ##成功
        db = MongoOperator('10.120.26.31',27017,'te','%s'%(file_json[i]))
        db.insert(result_data)

    for item in db.find():
        print(item)