from bs4 import BeautifulSoup
import random
import time
import pandas as pd
import json
import requests
import datetime
import re
import os

ltn_dict = r'./newsdata'  #存至此目錄
if not os.path.exists(ltn_dict): #若目錄不存在則新增一個
    os.mkdir(ltn_dict)
dflist=pd.DataFrame()
today = datetime.date.today() ; today = str(today)
def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code
yesterday = str(getYesterday())
#print(str(''.join(yesterday.split('-'))))
#一次爬取五個網站類型相同新聞分類
part_list = ['politics','society','life','world',"novelty"]
# def save(title,date,time,content,'Link','flog'):
try:
    for topic in part_list:
        page = 1
        url = 'https://news.ltn.com.tw/ajax/breakingnews/%s/'%(topic) + str(page) #一次爬五個版
        print(url)
        request_session = requests.session()
        respond = request_session.get(url=url)
        js = json.loads(respond.text) #將json格式轉成python_json格式
        all =js['data'] #取出data底下的內容
        n = 1
        for i in all:
            try:
                print("第", n, "篇")
                title = i['title'];print("標題:",title)
                url = i['url'];print("網址:",url)
                flag = i['type_cn'];print("flag",flag)
                each_res = requests.get(url)  ; each_soup = BeautifulSoup(each_res.text) ; each_html = each_soup.findAll("div", {'class': "whitecon"})
                str_ = ''
                n += 1
                for page in each_html:
                    page = page('p')
                    for news_all in page:
                        str_ += news_all.text.split('不用抽')[0]
                date_time = each_soup.select("span[class='time']")[0].text
                date = date_time.split()[0]
                if date == yesterday:
                    date = date.replace('-', '') ; print(date)
                else :
                    continue
                time = date_time.split()[1].split(':')[0] + date_time.split()[1].split(':')[1] ; print(time)
            except:
                pass
            df = pd.DataFrame(  # 用pandas轉成dataframe
                data=[{
                    'title': title,
                    'date': date,
                    'time': str(time),
                    'content': str_,
                    'link': url,
                    'flag':flag
                }],
                columns=['title','date','time','content','link','flag']
            )
            dflist = dflist.append(df, ignore_index=True)  # 將檔案存檔

        for page_test in range(2,27) : #json頁數,因第一頁和其他頁json格式不一樣
            url = "https://news.ltn.com.tw/ajax/breakingnews/%s/%s"%( topic , page_test)
            res = requests.get(url)
            soup = BeautifulSoup(res.text,'html.parser')
            json_string = str(soup)
            js = json.loads(json_string)
            i = 20
            j = 500 #第二頁最多到39 ,共500篇
            while(i < j):
                try:
                    url_main = js['data'][str(i)]['url']
                    res = requests.get(url_main)
                    soup = BeautifulSoup(res.text,'html.parser')
                    str_ = ''
                    print( "第" , i+1 , "篇")
                    print("flag", js['data'][str(i)]['type_cn'])
                    print( "標題:" + js['data'][str(i)]['title'])
                    print("網址:" + js['data'][str(i)]['url'])
                    news = soup.select("div[class='text boxTitle boxText']")
                    for page in news:
                        page = page('p')
                        for news_all in page:
                            str_ += news_all.text.split('不用抽')[0]
                    date_time = soup.select("span[class='time']")[0].text
                    date = date_time.split()[0]
                    if date == yesterday:
                        date = date.replace('-', '')
                        print(date)
                        time = date_time.split()[1].split(':')[0] + date_time.split()[1].split(':')[1]
                        print(time)
                        df = pd.DataFrame(
                            data = [{   # 用pandas轉成dataframe
                                'title':js['data'][str(i)]['title'],
                                'date':date,
                                'time': str(time),
                                'content': str_,
                                'link':js['data'][str(i)]['url'],
                                'flag':js['data'][str(i)]['type_cn']
                            }],
                            columns = ['title','date','time','content','link','flag']
                        )
                        dflist = dflist.append(df,ignore_index=True) #將檔案存檔
                        i += 1
                    elif date == today: #當日期為今日還是要 i+=1,因是用ajax爬蟲,需換頁
                        i += 1
                        pass
                    else:  #昨日後都不要
                        break
                    if (i % 20 == 0):  # 20篇一個json
                        page_test += 1
                        url = "https://news.ltn.com.tw/ajax/breakingnews/%s/%s" % (topic, page_test)
                        res = requests.get(url)
                        soup = BeautifulSoup(res.text, 'html.parser')
                        json_string = str(soup)
                        js = json.loads(json_string)
                except:
                    break
    dflist.to_csv(ltn_dict + '/ltn_%s.csv'%(str(''.join(yesterday.split('-')))),encoding='utf-8-sig', index=0)
    message ='LTN_news: {} 的新聞已經由例行公事完成'.format(yesterday)
    # 帶入權杖，這串token是當時在line網站上建立line notify時會跑出來的金鑰，官方說法是權杖
    token = 'p8jxzXyw8xl2NOuPjSi8s5NOP0qFTPXDQ2idzOSZZK8'
    # 使用前面訂好的函式發送出訊息
    #lineNotifyMessage(token, message)
except Exception as e:
    message = 'LTN_news: Expection occurs! message: {}'.format(e)
    # 帶入權杖，這串token是當時在line網站上建立line notify時會跑出來的金鑰，官方說法是權杖
    token = 'p8jxzXyw8xl2NOuPjSi8s5NOP0qFTPXDQ2idzOSZZK8'
    # 發生exception時送出該訊息
    #lineNotifyMessage(token, message)

