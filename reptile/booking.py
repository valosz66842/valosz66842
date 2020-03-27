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
from opencc import OpenCC #pip install opencc-python-reimplemented
cc = OpenCC('s2t')
header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
url='https://www.booking.com/searchresults.zh-tw.html?aid=309654&label=accommodations-chinese-zh-xt-K_EAatmaWx4okpP32qUC8gS52083193612%3Apl%3Ata%3Ap1%3Ap22%2C623%2C000%3Aac%3Aap%3Aneg%3Afi%3Atiaud-146342138230%3Akwd-267761191%3Alp21102%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YcsZ-Id2vkzIfTmYhvC5HOg&sid=8b471e8ae57b78709803f5f5c0912586&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.zh-tw.html%3Faid%3D309654%3Blabel%3Daccommodations-chinese-zh-xt-K_EAatmaWx4okpP32qUC8gS52083193612%253Apl%253Ata%253Ap1%253Ap22%252C623%252C000%253Aac%253Aap%253Aneg%253Afi%253Atiaud-146342138230%253Akwd-267761191%253Alp21102%253Ali%253Adec%253Adm%253Appccp%253DUmFuZG9tSVYkc2RlIyh9YcsZ-Id2vkzIfTmYhvC5HOg%3Bsid%3D8b471e8ae57b78709803f5f5c0912586%3Bsb_price_type%3Dtotal%26%3B&sr_autoscroll=1&ss=%E5%8F%B0%E5%8C%97&is_ski_area=0&checkin_year=2020&checkin_month=3&checkin_monthday=1&checkout_year=2020&checkout_month=3&checkout_monthday=2&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1'
res=requests.get(url)
soup=BeautifulSoup(res.text,'html.parser')
article_each=soup.select('a[class="hotel_name_link url"]')
page=soup.select('div[class="sr_header--title"]')[0].text.split(' ')
page_count=int(page[1])
for page in range(25,page_count,25):
    for article in article_each: #第一頁
        title=str.strip(article.select('span[class="sr-hotel__name"]')[0].text)
        print(cc.convert(title))
        article=article['href']
        article_url='https://www.booking.com'
        for i in article:
            if i == '\n':
                pass
            else:
                article_url+=i
        print(article_url)
        article_res=requests.get(article_url,headers=header)
        article_soup=BeautifulSoup(article_res.text,'html.parser')
        article_Features=article_soup.select('div[class="room-info"]')
        print(p)
        #article_json=json.loads((article_soup('script')[4]).text)['address']['streetAddress']
        #print(article_Features)
        for i,n in enumerate(article_Features):
            print(n('a')[0].text)
        # counter_str=article_soup.select('div[id="property_description_content"]')
        # counter=''
        # for n in counter_str:
        #     n=n('p')
        #     for main in n:
        #         counter+=main.text
        # print(cc.convert(counter))
        #print(cc.convert(article_json))
    url='https://www.booking.com/searchresults.zh-tw.html?aid=309654&label=accommodations-chinese-zh-xt-K_EAatmaWx4okpP32qUC8gS52083193612%3Apl%3Ata%3Ap1%3Ap22%2C623%2C000%3Aac%3Aap%3Aneg%3Afi%3Atiaud-146342138230%3Akwd-267761191%3Alp21102%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YcsZ-Id2vkzIfTmYhvC5HOg&sid=8b471e8ae57b78709803f5f5c0912586&tmpl=searchresults&checkin_month=3&checkin_monthday=1&checkin_year=2020&checkout_month=3&checkout_monthday=2&checkout_year=2020&class_interval=1&dest_id=-2637882&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=index&src_elem=sb&srpvid=77ae70b02ce7010a&ss=%E5%8F%B0%E5%8C%97&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    article_each = soup.select('a[class="hotel_name_link url"]')
