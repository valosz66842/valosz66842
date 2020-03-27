'''
以MongoBD為底，
進行資料的儲存及判斷是否重複存取
與中斷後的續傳，
因為紀錄來源為mongoDB
也可以跨設備進行續傳
並能判斷該頁面是否有目標區間內的文章，
若沒有則翻頁
加速查詢
若是因為程式錯誤導致失敗則會以line通知本人
成功也會用line通知本人
本程式可以放在liunx跑
這是VMDocker版本
'''
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
import numpy as np
from pprint import pprint
from datetime import datetime, timedelta
class MongoOperator: #Mondb連線
    def __init__(self, host, port, db_name, default_collection): #mongo port:27017
        self.client = pm.MongoClient(host=host, port=port)        #建立資料庫連線
        self.db = self.client.get_database(db_name)        #選擇相應的資料庫名稱
        self.collection = self.db[default_collection]
    def insert(self, item, collection_name =None): #增加資料 DBNAME,collection
        if collection_name != None:
            collection = self.db.get_collection(self.db)
            collection.insert(item)
        else:
            self.collection.insert(item)
    def delect_collention(self,item):#刪除collection
        self.collection.delete_many(item)
    def find(self, expression =None, collection_name=None): #查詢 expression:條件 collection_name:檔名
        if collection_name != None:
            collection = self.collection
            if expression == None:
                return collection.find()
            else:
                return collection.find(expression)
        else:
            if expression == None:
                return self.collection.find()
            else:
                return self.collection.find(expression)
def lineNotifyMessage(token, msg):#完成或失敗用line通知本人
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code
def GetDateTime(Date):
    Date=str(Date)
    date=''.join(''.join(''.join(str(Date).split("-")).split(":")).split(" "))
    return date
PTT_Hot="https://www.ptt.cc/bbs/hotboards.html"
res=requests.get(PTT_Hot)
soup=BeautifulSoup(res.text,"html.parser")
PTT=soup.select("div[class='board-name']")
Arime=[]
for PTT_Arime in PTT[:5]:#每次爬取最熱門的五個看板資料
    Arime.append(PTT_Arime.text)
# Arime=['PathofExile']
StartDate=input("請輸入爬蟲起始日期(YYYYMMDD):")
EndDate=input("請輸入爬蟲結束日期(YYYYMMDD):")
StartDate=int(StartDate)
EndDate=int(EndDate)
print(Arime)
MongoDB=MongoOperator("mongo",27017,"PttData","PttData")
url_dict={}
for item in MongoDB.find():
    url_dict[item["canonicalUrl"]]=1
MongoDBTemp=MongoOperator("mongo",27017,"PttTemp","{}To{}".format(StartDate,EndDate))
RecordArimeCount=0
for RecordCount in MongoDBTemp.find():
    RecordArimeCount=RecordCount.get("ArimeCount")
    Arime=RecordCount.get("Arime")
StartCount=len(Arime)-RecordArimeCount
try:
    for ArimeCount,Eeptile_Arime in enumerate(Arime[StartCount::-1]):
        RecordArticle=0
        url = "https://www.ptt.cc/bbs/{}/index.html".format(Eeptile_Arime)
        for TempData in MongoDBTemp.find():
            url=TempData.get("url")
            RecordArticle=TempData.get("count")
        cookies = {"over18": "1"}

        res = requests.get(url, cookies=cookies)
        soup = BeautifulSoup(res.text, 'html.parser')
        article_each = soup.select("div[class='title']")
        PttPage = soup.select("a[class='btn wide']")[1]['href'].split('index')[1].split('.html')[0]  # 每一個板的頁數
        DateAll=soup.select("div[class='date']")
        ExternalDate=[]
        for Date in DateAll:#從外面判斷是否符合日期的文章
            if len(Date.text.replace("/","").strip())==3:
                Date=Date.text.replace("/","").strip()
                ExternalDate.append(int(Date))
            else:
                ExternalDate.append(int(Date.text.replace("/","").strip()))
        overdate=int(str(StartDate)[4:])#使用者輸入的開始日期
        StartYear=str(StartDate)[:4]#紀錄目標的年份
        ArmieYearBlo=True
        ExtMax=max(ExternalDate)#這頁最大的日期
        EndBol = True
        OnePageBol = True
        TempArticleCount=RecordArticle  #計算之前每次執行到的位置
        RecordArticle=len(article_each)-RecordArticle #計算文章開始位置
        while(EndBol==True):
            if ((overdate >= ExtMax  or OnePageBol ==True) and (ArmieYearBlo==True)):
                for count,article in enumerate(article_each[RecordArticle::(-1)]):
                    try:
                        MongoDBDict={}
                        canonicalUrl="https://www.ptt.cc/"+article("a")[0]["href"]#文章網址
                        if url_dict.get(canonicalUrl)==None:
                            MongoDBTemp.insert({"url": url, "canonicalUrl": canonicalUrl,"count":count+1+TempArticleCount,"ArimeCount":ArimeCount+1,"Arime":Arime})
                            title=article("a")[0].text#文章標題
                            print(title)
                            article_res=requests.get(canonicalUrl,cookies=cookies)
                            article_soup=BeautifulSoup(article_res.text,"html.parser")
                            authorId=article_soup.select("span[class='article-meta-value']")[0].text.split(" ")[0]#作者ID
                            authorName=(article_soup.select("span[class='article-meta-value']")[0].text.split(" (")[1])[:-1]#作者暱稱
                            article_date=article_soup.select("span[class='article-meta-value']")[3].text#文章原始時間
                            purlishedTime=datetime.strptime(article_date, '%a %b %d %H:%M:%S %Y')#格式化發文日期
                            purlishedTime=GetDateTime(purlishedTime)
                            ArticleDate=int(purlishedTime[:8])#文章的發布日期
                            ArticleYear = purlishedTime[:4]
                            print("ArticleDate:",ArticleDate)
                            # print("StartDate",StartDate)
                            # print("EndDate",EndDate)
                            if ArticleDate <= StartDate and ArticleDate>=EndDate:#開始的日期及結束日期
                                ISOTIMEFORMAT = '%Y%m%d%H%M%S'#定義格式
                                createdTime=datetime.now().strftime(ISOTIMEFORMAT)#寫入資料庫日期
                                updateTime=datetime.now().strftime(ISOTIMEFORMAT)#最新日期
                                content=article_soup.select("div[id='main-content']")[0].text.split(article_date)[1].split("--")[0].strip() #內文
                                commentId =''
                                commentContent =''
                                commentTime=''
                                try:
                                    PushTime = "".join("".join(
                                        (article_soup.select("span[class='push-ipdatetime']")[0].text).strip().split(
                                            "/")).split(":"))
                                    commentIdAll = article_soup.select("span[class='f3 hl push-userid']")
                                    for PushCount in range(len(commentIdAll)):#記錄所有推文
                                        commentId=commentId+(article_soup.select("span[class='f3 hl push-userid']")[PushCount].text)+'\n'#紀錄推文ID
                                        commentContent=commentContent+(article_soup.select("span[class='f3 push-content']")[PushCount].text)+'\n' #紀錄推文內容
                                        commentTime=commentTime+"".join(PushTime.split(" "))+'\n'
                                except:#這篇文章沒有任何推文
                                    commentId="沒有推文"
                                    commentContent="沒有推文"
                                    commentTime="沒有推文"
                                    print("沒有推文")
                                #題目要求的資料
                                MongoDBDict["authorId"]=authorId
                                MongoDBDict["authorName"]=authorName
                                MongoDBDict["title"]=title
                                MongoDBDict["purlishedTime"]=purlishedTime
                                MongoDBDict["content"]=content
                                MongoDBDict["canonicalUrl"]=canonicalUrl
                                MongoDBDict["createdTime"]=createdTime
                                MongoDBDict["updateTime"]=updateTime
                                MongoDBDict["commentId"]=commentId
                                MongoDBDict["commentContent"]=commentContent
                                MongoDBDict["commentTime"]=commentTime
                                MongoDB.insert(MongoDBDict)
                                print(MongoDBDict)
                            else:
                                ArmieYearBlo=False
                            MongoDBTemp.delect_collention({})
                        else:
                            print("這篇存過了")
                    except Exception as e:
                        print(e)
                        pass
                if OnePageBol == False:
                    if EndDate > ArticleDate:
                        EndBol = False  #
                url = "https://www.ptt.cc/bbs/{}/index{}.html".format(Eeptile_Arime, PttPage)
                print(url)
                cookies = {"over18": "1"}
                res = requests.get(url, cookies=cookies)
                soup = BeautifulSoup(res.text, 'html.parser')
                article_each = soup.select("div[class='title']")
                PttPage = soup.select("a[class='btn wide']")[1]['href'].split('index')[1].split('.html')[0]  # 每一個板的頁數
                OnePageBol = False#紀錄是否第一頁
            elif(OnePageBol ==False):#目標日期不在這頁則持續翻頁 且非第一頁有置頂文
                url = "https://www.ptt.cc/bbs/{}/index{}.html".format(Eeptile_Arime, PttPage)
                print(url)
                cookies = {"over18": "1"}
                res = requests.get(url, cookies=cookies)
                soup = BeautifulSoup(res.text, 'html.parser')
                article_each = soup.select("div[class='title']")
                PttPage = soup.select("a[class='btn wide']")[1]['href'].split('index')[1].split('.html')[0]  # 每一個板的頁數
                DateAll = soup.select("div[class='date']")
                ExternalDate=[]
                for Date in DateAll:  # 從外面判斷是否符合日期的文章
                    if len(Date.text.replace("/", "").strip()) == 3:
                        Date =Date.text.replace("/", "").strip()
                        ExternalDate.append(int(Date))
                    else:
                        ExternalDate.append(int(Date.text.replace("/", "").strip()))
                ExtMax = max(ExternalDate)
                ExtMin = min(ExternalDate)
                # print("ExtMax:",ExtMax)
                # print("EexMin:",ExtMin)
                if ExtMin*5<ExtMax:#這頁是跨年份的頁面
                    ArmieYearBlo = True
                else:
                    article_date = article_soup.select("span[class='article-meta-value']")[3].text  # 文章原始時間
                    purlishedTime = datetime.strptime(article_date, '%a %b %d %H:%M:%S %Y')  # 格式化發文日期
                    purlishedTime = GetDateTime(purlishedTime)
                    article_Year=purlishedTime[:4]
                    if article_Year==StartYear:
                        ArmieYearBlo = True
                print(ExternalDate)
                print(url)
                print(ExtMax)
    message = '電獺少女專案PTT的文章已經由python爬蟲完成'
    # 帶入權杖，這串token是當時在line網站上建立line notify時會跑出來的金鑰，官方說法是權杖
    token = 'UfofIRYlkm581H8lZzR2pRWYIVuf7DhaJgJZHZkE1hX'
    # 使用前面訂好的函式發送出訊息
    lineNotifyMessage(token, message)
except Exception as e:
    message = '電獺少女專案PTT的文章失敗，錯誤訊息為:{}'.format(e)
    # 帶入權杖，這串token是當時在line網站上建立line notify時會跑出來的金鑰，官方說法是權杖
    token = 'UfofIRYlkm581H8lZzR2pRWYIVuf7DhaJgJZHZkE1hX'
    # 使用前面訂好的函式發送出訊息
    lineNotifyMessage(token, message)
