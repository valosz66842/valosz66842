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
import jieba
import pymysql
# 開啟資料庫連線
Folder_Path = r'C:\Users\Big data\PycharmProjects\pyAI2\FeatData'  #csv目標資料夾
class MySqlOperator:
    def __init__(self,host,user,password):
        self.conn = pymysql.Connect(host,user,password)
        self.cursor = self.conn.cursor()  # 設置光標
    def make_table_sql(self, df):  # 抓出資料的型態
        columns = df.columns.tolist()
        make_table = []
        for item in columns:
            if 'int' in str(df.dtypes[item]):
                char = item + ' INT'
            elif 'float' in str(df.dtypes[item]):
                char = item + ' float'
            elif 'object' in str(df.dtypes[item]):
                char = item + ' VARCHAR(255)'
            elif 'datetime' in str(df.dtypes[item]):
                char = item + ' DATETIME'
            make_table.append(char)
        return ','.join(make_table)
    def mysqlconnect(self,dbname,table_name):
        self.dbname=dbname
        self.table_name=table_name
    def csvtomysql(self,df):
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(self.dbname))#若沒有目錄創建一個
        self.conn.select_db(self.dbname)  # 連線的名字
        values = df.values.tolist()
        strs = ''
        for i in df.columns.tolist():
            strs += i
            strs += ','
        strs = strs[:-1]
        s = ','.join(['%s' for i in range(len(df.columns))])
        string = self.make_table_sql(df)
        try:
            self.cursor.execute('CREATE TABLE {} ({})'.format(self.table_name,string))#創造表格
        except:
            pass
        sqlStuff = ('INSERT INTO {} ({}) VALUES ({})'.format(self.table_name,strs, s))#塞資料
        self.cursor.executemany(sqlStuff, values)
    def findAll(self):
        sql = "select * from {}.{}".format(self.dbname,self.table_name)
        self.cursor.execute(sql)  # 執行sql語句
        return self.cursor.fetchall()
    def find(self,string):
        sql = "select {} from {}.{}".format(string,self.dbname, self.table_name)
        self.cursor.execute(sql)  # 執行sql語句
        return self.cursor.fetchall()
    def groupfind(self,string,group):
        sql = "select {} from {}.{} group by {}".format(string,self.dbname, self.table_name,group)
        self.cursor.execute(sql)  # 執行sql語句
        return self.cursor.fetchall()
os.chdir(Folder_Path)  # 換工作路徑
file_list = os.listdir(Folder_Path)  # 這個資料夾內所有的檔案名稱
file_csv = []
for file in file_list:  # 只讀csv檔
    if '.csv' in file:
        file_csv.append(file)
db=MySqlOperator('127.0.0.1','root','670wutr5') #連線 user身分 密碼
print(file_csv)
conn = db.conn
cursor=db.cursor

for i in range(len(file_csv)):
    name = file_csv[i][:-4]
    df=pd.read_csv(r'C:\Users\Big data\PycharmProjects\pyAI2\FeatData/{}'.format(file_csv[i])) #讀的檔案
    db.mysqlconnect("SQL","{}".format(name))#目錄名稱 表格名稱 如果沒有都會創建一個
    db.csvtomysql(df) #要塞進去的資料
    db.conn.commit()#執行
    data = db.findAll()  # 查詢目錄下的表格
    for j in data:
        print(j)

# data=db.findAll()#查詢目錄下的表格
# data=db.find('count(*)')



