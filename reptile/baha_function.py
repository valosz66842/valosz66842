from bs4 import BeautifulSoup
import random
import time
import pandas as pd

import requests
import re
from lxml import etree
import json
# 下面的部分我全部做成一個function 目前你還需要做的就是修改一下我們上次開會寫的baha.py做成一個function去產生 下面這個urllist
# 當然下面還有一些要寫的地方，你看一下註解，對你來講肯定不難啦
# 你先這樣寫寫看，如果有問題再丟line給我，如果可以的話  不要把運行錯誤的部分刪掉，這樣我比較知道你原本想要怎麼寫

# import requests
# from bs4 import BeautifulSoup
# import re
# from lxml import etree
def save(count, title,date, content,Link):
    df = pd.DataFrame(
        data=[{
            'count': time,
            'title': title,
            'date': date,
            'content': content,
            'Link': Link,
        }],
        columns=['ID', 'title', 'date', 'content','留言'])
    return df
page=2
url = 'https://forum.gamer.com.tw/B.php?page={}&bsn=60559'.format(page)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
each_article=soup.select("div[class='b-list__tile']")
Joblist=pd.DataFrame()
count=1
while(True):
    print(page)
    for article in each_article:
        try:
            snB=[]
            reply_all=''
            Link='https://forum.gamer.com.tw/'+article('p')[0]['href']
            title=article('p')[0].text
            print(Link)
            print(title)
            article_res=requests.get(Link)
            article_res.encoding=('utf-8') #編碼
            article_soup=BeautifulSoup(article_res.text,'html.parser')
            article_time=article_soup.select("div[class='c-post__header__info']")[0]('a')[0]['data-mtime']
            article_date=article_time.split(' ')[0]
            print(article_date)
            content=article_soup.select("div[class='c-article__content']")#抓內文的標籤
            article_content=content[0].text#內文
            reply = []#儲存留言
            for article_main in content:
                if article_main==article_content:#抓留言跟內文同樣不抓 剛抓過了
                    pass
                else:
                    reply.append(article_main.text)#儲存留言
            json_all=article_soup.select("div[class='old-reply']")
            for json_No in json_all:#抓json留言
                string = str(str(json_No.a['onclick']).split(',')[1])
                string = (string[:-2]).strip()
                snB.append(string)
            for i in range(len(snB)):
                json_Link='https://forum.gamer.com.tw/ajax/moreCommend.php?bsn=60559&snB={}&returnHtml=1'.format(snB[i])
                json_res = requests.get(json_Link)
                js = (json.loads(str(json_res.text)))['html']
                for js_soup in js:
                    js_soup=BeautifulSoup(js_soup,'html.parser')
                    reply_each=js_soup.select("article[class='reply-content__article c-article']")
                    reply.append(reply_each[0].text)#抓完json留言
            for i in range(len(reply)):#儲存json留言
                reply_all+=reply[i]
            print(reply_all)
            df=save(count,title,article_date,article_content,reply_all) #儲存到表格
            count+=1#計算爬的文章數
        except Exception as e:
            print(e)
            break
    page += 1
    url= 'https://forum.gamer.com.tw/B.php?page={}&bsn=60559'.format(page) #翻頁
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    each_article = soup.select("div[class='b-list__tile']")
