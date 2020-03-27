import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import request
import os
import time
import lxml.html
import datetime
import csv
from opencc import OpenCC
cc = OpenCC('s2t')
Folder_Path = r'C:\Users\Big data\PycharmProjects\pyAI2\FeatCount2\split\新增資料夾'  #要拼接的所有文件
os.chdir(Folder_Path) #換工作路徑
file_list = os.listdir() #這個資料夾內所有的檔案名稱
file_csv=[]
for file in file_list: #只讀csv檔
    if '.csv' in file:
        file_csv.append(file)
js_list=pd.DataFrame() #創一個表格
for i in range(len(file_csv)): #讀所有檔案
    OpenCsvPath= open(Folder_Path+'/{}'.format(file_csv[i]),'r',encoding='utf-8-sig')
    csv_pd = pd.read_csv(OpenCsvPath)
    js_list=js_list.append(csv_pd)

js_list.to_csv(Folder_Path+'\Channel6.csv', encoding="utf-8-sig", index=False, header=True, mode='w')#合併輸出









