from django.shortcuts import render
from django.shortcuts import render
from django import template
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import os
import time
import lxml.html
import re
import urllib.parse
import pandas as pd
import numpy as np
import csv
import jieba
import pymysql
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import JsonResponse
# Create your views here.
# Create your views here.
# Create your views here.
import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import os
import time
import lxml.html
import pandas as pd
from opencc import OpenCC
from confluent_kafka import Producer
import sys
import pickle
import joblib
from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
pwd=os.path.dirname(__file__)
# sys.path.append(pwd+"../kafka_producer.py")
# import kafka_producer
# from . import NEWS_WORDCLOUD_BY
# 留言的目標url 是看網路文章得來的，從開發者人員工具中看不到這些網址
# reference: http://www.bithub00.com/2019/07/25/Youtube%E7%88%AC%E8%99%AB/
# reference: https://github.com/egbertbouman/youtube-comment-downloader
CsvPath=pwd
FilePath=pwd
ImagePath=pwd+r'/static/images'
def ajax_MessageEmotion(request):
    word={}
    ImgStrPath='''  
                                        <div class="col-xl-6">
                                            <div class="card mb-4">
                                                <div class="card-header"><i class="fas fa-chart-cloud mr-1"></i>爬蟲準備中</div>
                                                <div class="card-img-top" id='Statistics_TOW' name='Statistics_TWO'  alt="">
                                                     '<img value='adfsdfas' src='/static/images/VKSPIDER.gif'  width="1021" height="900" /></div>
                                                <div class="card-body"><canvas id="myAraph" width="100%" height="40%"></canvas></div>
                                            </div>
                                        </div>
                                        '''

    word['VideoUrl']=ImgStrPath
    return JsonResponse(word)
    # return render_to_response('MessageEmotion.html',locals())
def youtube_get_comment_fin(url):
    MessageCount=0
    video_id=url.split('watch?v=')[1].split('&')[0]
    # 設定要抓幾留言便停止
    comment_limit = 200
    session = requests.Session()
    session.headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    # Get Youtube page with initial comments
    first_page_comment_url = 'https://www.youtube.com/all_comments?v=' + video_id
    # 先進入 https://www.youtube.com/all_comments?v=video_id (進入該頁面的目的是拿到session_token)
    response = session.get(first_page_comment_url)
    html = response.text
    # ===找到session_token
    target = 'XSRF_TOKEN'
    start = html.find(target) + len(target) + len('\': \"')  # str.find('target',start index)可找出對應的足碼
    end = html.find('"', start)
    session_token = html[start:end]
    # 設定函式去request
    def ajax_request(session, url, params, data):
        response = session.post(url, params=params, data=data)
        response_dict = json.loads(response.text)
        return response_dict.get('page_token', None), response_dict['html_content']
    # 開始進入留言區
    count = 0
    data_con = pd.DataFrame(columns=['video_id', 'viewer', 'comment', 'time', 'clean_con'])
    # 設定只保留中文、英文、數字（去掉韓語日語德語，也會去掉表情符號等等）
    # reference: https://zhuanlan.zhihu.com/p/84625185
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    ###設定簡體轉繁體方法
    cc = OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese
    # 進入留言區第一頁時要帶的資料比較不同 data / params (order_menu : True)
    data = {'video_id': video_id, 'session_token': session_token}
    params = {'action_load_comments': 1, 'order_by_time': True, 'filter': video_id, 'order_menu': True}
    # 先設定page_token為真使while作動; 待會跑到最後一頁時，page_token 為空值，因此while停止
    page_token = True
    # 每一頁留言(仿留言往下滑)
    while page_token:
        response_2 = ajax_request(session, 'https://www.youtube.com/comment_ajax', params, data)
        # 留言區的第二頁之後的帶的資料 data / params
        data = {'video_id': video_id, 'session_token': session_token}
        params = {'action_load_comments': 1, 'order_by_time': True, 'filter': video_id}
        # response_2[0] 為 page_token
        # response_2[1] 為 回傳訊息的留言內容區
        page_token = response_2[0]
        data['page_token'] = page_token
        res = BeautifulSoup(response_2[1], 'html.parser')
        # 使用標籤取出每一頁的留言
        coent = res.select('div.comment-text-content')  # 留言
        user_name = res.select('a.user-name')  # 留言者
        coent_time = res.select('span.time')  # 留言時間
        # 開始記錄留言進dataframe (data_con)
        for i in range(len(coent_time)):
            content = cc.convert(''.join(coent[i].text.strip().split('\n')))
            # 整理出乾淨的留言
            clean_data = rule.sub(' ', str(content))
            if len(rule.sub('', str(clean_data))) < 1:
                clean_content = 'NAN'
            else:
                clean_content = clean_data.strip(' ')
            # 加入pa.dataframe時順便將簡體轉成繁體
            data_con = data_con.append(
                {'video_id': video_id, 'viewer': cc.convert(user_name[i].text.strip()), 'comment': content,
                 'time': coent_time[i].text.strip(), 'clean_con': clean_content}, ignore_index=True)
            # 計算幾篇留言
            count += 1
            if count > comment_limit:
                page_token = None
                break
        print('page_token: {}'.format(page_token))
    data_con.to_csv(CsvPath+'\{}.csv'.format(video_id), index=0, encoding='utf-8-sig')

def youtube_videoinfo_json_test1(url):
    for i in range(10):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

            # get web response
            html = requests.get(url, headers=headers)
            response = BeautifulSoup(html.text, 'html.parser')

            a = response.select('script')  # 目標json在window["ytInitialData"]在當中，在a的倒數第3個
            data_str = str(a[-3].text)  # window["ytInitialData"] = {"responseContext":{... 的字串檔
            # 處理成完整的json格是再做json.loads
            data_str = '{' + data_str.split('= {')[1].split('}};\n')[0] + '}}'
            data_dict = json.loads(data_str)
        except:
            time.sleep(2)
            pass
    # print(data_dict)
    # ===開始取資料
    # 該影片相關資訊
    set_a = data_dict['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
        'videoPrimaryInfoRenderer']
    # 該影片的頻道相關資訊
    set_b = data_dict['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']
    video_title = set_a['title']['runs'][0]['text']
    video_view_count = set_a['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
    video_post_date = set_a['dateText']['simpleText']
    video_like_count = set_a['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['simpleText']
    video_dislike_count = set_a['videoActions']['menuRenderer']['topLevelButtons'][1]['toggleButtonRenderer']['defaultText']['simpleText']
    channel_of_video = set_b['title']['runs'][0]['text']
    channel_id_of_video = set_b['title']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId']
    video_title=''.join(video_title.split(' '))
    VideoStatistics=[]
    VideoStatistics.append('影片標題:'+video_title)
    VideoStatistics.append('\n'+video_view_count)
    VideoStatistics.append('發佈日期:'+video_post_date)
    VideoStatistics.append('按讚數:'+video_like_count)
    VideoStatistics.append('倒讚數:'+video_dislike_count)
    VideoStatistics.append('頻道名稱:'+channel_of_video)
    VideoStatistics.append('頻道ID:'+channel_id_of_video)
    return VideoStatistics

def MessageEmotion(request):
    if 'UserGetVideoUrl' in request.GET and request.GET['UserGetVideoUrl'] != '':
        VideoUrl=request.GET["UserGetVideoUrl"]
        youtube_get_comment_fin(VideoUrl)#把網址丟進爬蟲程式
        HtmlCodeList=youtube_videoinfo_json_test1(VideoUrl) #把程式丟進爬蟲抓影片標題 發佈日期 等等資訊
        # MessageEmotion = {"MessageEmotion": {
        #     "VideoUrl": VideoUrl,
        # }}
        # try:
        #     ip = request.META['REMOTE_ADDR']
        # except:
        #     ip = request.META['HTTP_X_FORWARDED_FOR']
        # try:
        #     kafka_producer.producer(kafka_producer.Els(ip,"MessageEmotion", MessageEmotion["MessageEmotion"]))
        # except:
        #     pass
        video_id = VideoUrl.split('watch?v=')[1].split('&')[0] #取得Video ID
        Video_Name=str(video_id)+'.png' #做出圖片檔案名稱
        Folder_Path=ImagePath #做為檢查是否有儲存圖片的路徑
        count=0#計算時間
        Pie_Name='sentiment_pie_{}.png'.format(video_id)
        while True:#每秒檢查是否有圖檔
            file_list = os.listdir(Folder_Path)  # 這個資料夾內所有的檔案名稱
            if (Video_Name not in file_list) or (Pie_Name not in file_list):#是否有這個VideoID做為檔名的圖片
                time.sleep(1)
                count+=1#每秒加一次
            else:
                Video_Image = '/static/images/{}.png'.format(video_id)
                Pie_Image='/static/images/{}'.format(Pie_Name)
                return render_to_response('MessageEmotion.html',locals())
            if count>=20:#20秒都沒有做出圖片跳出迴圈 不傳圖片了
                return render_to_response('MessageEmotion.html', locals())
    else:
        return render_to_response('MessageEmotion.html', locals())


