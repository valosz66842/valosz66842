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
import jieba
import csv
cc = OpenCC('s2t')
jieba.load_userdict('E:\YoutubeYear\SortDict.csv') #字典抓頻道名
SavePath='E:\YoutubeYear\FeatDate.csv'
FilePath=open(r'E:\YoutubeYear\Feat.csv',encoding='utf-8-sig') #feat頻道名

LenDictPath=open(r'E:\YoutubeYear\SortDict.csv',encoding='utf-8-sig')
StatisticsPath=open(r'E:\YoutubeYear\NewAllStatistics.csv',encoding='utf-8-sig')
all_title=''
job_pd=pd.DataFrame()
stopword={}
LenDict={}
Statistics_pd=pd.read_csv(r'E:\YoutubeYear\NewAllStatistics.csv')
LongSortDict_pd=pd.read_csv(r'E:\YoutubeYear\SortDict.csv')
#print(Statistics_pd)
name_list=list(LongSortDict_pd['name'])
def is_alphabet(keyword):
    return all(ord(c) < 128 and ord(c)>64 for c in keyword)
StopPath=open(r'E:\dict\wordstop.txt',encoding='utf-8-sig')
reader=csv.reader(StopPath)
for row in reader:
    try:
        stopword[row[0]]=1
    except:
        stopword['']=1
# searchpath= open('E:\YoutubeYear\StopNew.csv', 'r', encoding='utf-8-sig')
# reader=csv.reader(searchpath)
# for row in reader:
#     stopword[row[0]]=1
reader=csv.reader(LenDictPath)
for n,row in enumerate(reader):
    if n==0 :
        pass
    elif LenDict.get(len(row[0]))==None:
        LenDict[len(row[0])]=(n+1)
No_dict={}
same={}
same_path=open(r'E:\dict\same.txt')
reader=csv.reader(same_path)
for row in reader:
    for i in row:
        same[i.lower()]=row[0].lower()
print(same)
reader=csv.reader(FilePath)#抓合作的影片
stop=[]
Feat_channelID_dict={}
Feat_name_dict={}
Feat_median_dict={}
Feat_follow_dict={}
Feat_avg_dict = {}
Feat_Quartile1_dict = {}
Feat_Quartile3_dict = {}

for q,row in enumerate(reader):
    channel_name=['']
    row[1]=row[1].lower()
    if len(row[1].split('ft'))>2:
        all_title = row[1].split('ft')[-1].split('｜')[0].split('|')[0].split(')')[0].split('。')[0]
    elif 'feat' in row[1]:
        all_title = row[1].split('feat')[-1].split('｜')[0].split('|')[0].split(')')[0].split('。')[0]
    elif 'ft' in row[1]:
        all_title = row[1].split('ft')[1].split('｜')[0].split('|')[0].split(')')[0].split('。')[0]

    s_list = jieba.cut(all_title, cut_all=False)
    jieba_title=' '.join(s_list)
    jieba_title=jieba_title.split(' ')
    #print('p:',p)
    for title in jieba_title:
        if stopword.get(title)!=None or len(title)<2: #不在停用詞裡面 而且長度不是1
            pass
        elif is_alphabet(channel_name[-1]) == True and is_alphabet(title) == True: #連續是英文的詞
            channel_name[-1] = channel_name[-1]+title
        else:
            channel_name.append(title.lower())#不在停用字的詞
    new_channel_name=[]
    for name in channel_name: #查詢是否在7100個頻道名單內 可以的話存入準備搜尋
        if same.get(name) != None:
            name = same[name]
        try:
            for i in name_list[LenDict[len(name)]:]:
                if name in str(i) :
                    new_channel_name.append(name.lower())
                    break
        except Exception as e:
            if str(e) =='0':
                pass
            else:
                print(e,end='')

    #print('可以使用',new_channel_name)
    # === go to page1
    url = "https://www.youtube.com/results?"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
               "content-type": "application/x-www-form-urlencoded"}
    para = {"search_query": "TEST123", "sp": "EgIQAg%253D%253D"}
    count=0
    Feat_channel=[]
    Feat_name=[]
    Feat_median=[]
    Feat_follow=[]
    Feat_avg=[]
    Feat_Quartile1=[]
    Feat_Quartile3=[]
    Feat_dict={}
    if len(new_channel_name) <1:
        pass
    else:
        print('\n',new_channel_name,'-------------'+row[1])
        for n, name in enumerate(new_channel_name):  # 一個關鍵字搜尋頻道
            if same.get(name)!=None:
                name=same[name]
            if No_dict.get(name)==None:
                try:#搜尋不到結果
                    if Feat_channelID_dict.get(name)==None: #假如這個詞沒搜尋過
                        for i in range(10):
                            try:#請求錯誤
                                para["search_query"] = name
                                html = requests.get(url, headers=headers, params=para)
                                response = BeautifulSoup(html.text, 'html.parser')
                                a = response.select('script')  # 目標json在window["ytInitialData"]在當中，在a的倒數第3個
                                data_str = str(a[-3].text)  # window["ytInitialData"] = {"responseContext":{... 的字串檔
                                data_str = '{' + data_str.split('= {')[1].split('window["ytInitialPlayerResponse"]')[0].strip(' ').strip('\n').strip(';')
                                data_dict = json.loads(data_str)
                                break
                            except:
                                time.sleep(2)
                                pass
                        channel_id = re.findall(r"channelId\': \'(.*?)\'", str(data_dict))[0]
                        for i in range(5):
                            try:
                                set_a = data_dict['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][i]['itemSectionRenderer']['contents']
                                try:
                                    try:
                                        channel_feat_name = set_a[0]['channelRenderer']['title']['simpleText'].lower()
                                        break
                                    except:
                                        channel_feat_name = set_a[0]['videoRenderer']['longBylineText']['runs'][0]['text'].lower()
                                        break
                                except:
                                    channel_feat_name = set_a[1]['channelRenderer']['title']['simpleText'].lower()
                                    break
                            except:
                                pass
                        c = Statistics_pd.loc[
                            Statistics_pd['channel_id'] == row[0], ['channel_id', 'Channel_name', 'count',
                                                                    'watch_all_count', 'median', 'avg', 'Quartile1',
                                                                    'Quartile3', 'Follow']]  # 取原頻道名稱
                        # print(c)
                        # print(row[0])
                        MainName = (list(c['Channel_name']))[0]
                        MainMedian = (list(c['median']))[0]
                        MainFollow = (list(c['Follow']))[0]
                        MainAvg=(list(c['avg']))[0]
                        MainWatch_all=(list(c['watch_all_count']))[0]
                        Main_Quartile1 = (list(c['Quartile1']))[0]
                        Main_Quartile3 = (list(c['Quartile3']))[0]
                        b = Statistics_pd.loc[
                            Statistics_pd['channel_id'] == channel_id, ['channel_id', 'Channel_name', 'count',
                                                                        'watch_all_count', 'median', 'avg', 'Quartile1',
                                                                        'Quartile3', 'Follow']]
                        median = (list(b['median']))[0]
                        follow = (list(b['Follow']))[0]
                        avg=(list(b['avg']))[0]
                        Quartile1=(list(b['Quartile1']))[0]
                        Quartile3=(list(b['Quartile3']))[0]
                        Feat_dict[row[0]] = 1
                        Feat_channelID_dict[name] = channel_id
                        Feat_name_dict[name] = channel_feat_name.lower()
                        Feat_median_dict[name] = median
                        Feat_follow_dict[name] = follow
                        Feat_avg_dict[name] = avg
                        Feat_Quartile1_dict[name] = Quartile1
                        Feat_Quartile3_dict[name] = Quartile3
                        if Feat_dict.get(channel_id) == None:
                            count += 1
                            Feat_dict[channel_id] = 1
                            Feat_name.append(cc.convert(channel_feat_name))  # 儲存合作的頻道名稱
                            Feat_channel.append(channel_id)  # 儲存合作的頻道ID
                            Feat_median.append(median)  # 儲存合作的中位數
                            Feat_follow.append(follow)  # 儲存合作的追隨數
                            Feat_avg.append(avg)
                            Feat_Quartile1.append(Quartile1)
                            Feat_Quartile3.append(Quartile3)
                            print(name, channel_id, end=' ')
                    #print('\n存入  ' + '查詢使用:' + name + ' ' + channel_name + ' ' + channel_id)
                    else: #這個詞有搜尋過
                        c = Statistics_pd.loc[Statistics_pd['channel_id'] == row[0], ['channel_id', 'Channel_name', 'count','watch_all_count', 'median', 'avg','Quartile1', 'Quartile3', 'Follow']]#取原頻道名稱
                        #print(c)
                        #print(row[0])
                        channel_id=Feat_channelID_dict[name]
                        channel_feat_name=Feat_name_dict[name]
                        Feat_dict[row[0]] = 1
                        median=Feat_median_dict[name]
                        follow=Feat_follow_dict[name]
                        avg=Feat_avg_dict[name]
                        Quartile1=Feat_Quartile1_dict[name]
                        Quartile3=Feat_Quartile3_dict[name]
                        MainName = (list(c['Channel_name']))[0]
                        MainMedian = (list(c['median']))[0]
                        MainFollow = (list(c['Follow']))[0]
                        MainAvg=str((list(c['avg']))[0])
                        MainWatch_all=(list(c['watch_all_count']))[0]
                        Main_Quartile1 = (list(c['Quartile1']))[0]
                        Main_Quartile3 = (list(c['Quartile3']))[0]
                        if Feat_dict.get(channel_id)==None:
                            count += 1
                            Feat_dict[channel_id]=1
                            Feat_name.append(cc.convert(channel_feat_name))#儲存合作的頻道名稱
                            Feat_channel.append(channel_id)#儲存合作的頻道ID
                            Feat_median.append(median)#儲存合作的中位數
                            Feat_follow.append(follow)#儲存合作的追隨數
                            Feat_avg.append(avg)
                            Feat_Quartile1.append(Quartile1)
                            Feat_Quartile3.append(Quartile3)
                            print(name,channel_id,end=' ')
                except Exception as e:
                    No_dict[name]=1
                    stop.append(name)
                    print('')
                    print(e)
                    pass
                #print(type(b))
                #print(b.iloc[[0,2]])
                #print(Statistics_pd.loc[Statistics_pd['channel_id']==channel_id,['median']])
        if(len(Feat_channel) <1) or count ==0:#沒合作對象不用做
            pass
        else:
            print(row[0],count)
            df = pd.DataFrame(
                data=[{'MainID': row[0],
                       'MainName':MainName,
                       'MainVideoTitle': row[1],
                       'MainVideoID': row[2],
                       'MainMedian': MainMedian,
                       'MainFollow': MainFollow,
                       'MainLookCount': row[3],
                       'MainAvg':MainAvg,
                       'MainWatch_all':MainWatch_all,
                       'Main_Quartile1' :Main_Quartile1,
                       'Main_Quartile3' :Main_Quartile3,
                       'FeatCount': count}],
                columns=['MainID', 'MainName','MainVideoTitle', 'MainVideoID','MainMedian','MainFollow','MainLookCount','MainAvg','MainWatch_all','Main_Quartile1','Main_Quartile3','FeatCount'])
            for i in range(len(Feat_channel)):#新增欄位到右邊
                df['Feat_channel{}'.format(i+1)]=Feat_channel[i]
                df['Feat_name{}'.format(i+1)]=Feat_name[i]
                df['Feat_median{}'.format(i+1)]=Feat_median[i]
                df['Feat_follow{}'.format(i+1)]=Feat_follow[i]
                df['Feat_avg{}'.format(i+1)]=Feat_avg[i]
                df['Feat_Quartile1{}'.format(i + 1)] = Feat_Quartile1[i]
                df['Feat_Quartile3{}'.format(i + 1)] = Feat_Quartile3[i]
                #print(Feat_channel[i],Feat_name[i],Feat_median[i],end='')
            job_pd=job_pd.append(df,sort=False)
    if q%2==0:
        searchpath = open('E:\YoutubeYear\StopNew.csv', 'a', encoding='utf-8-sig')
        #print('寫入')
        for i in stop:
            searchpath.write(i)
            searchpath.write('\n')
            stop=[]
job_pd=job_pd.sort_values(by='FeatCount')
job_pd.to_csv(SavePath,index=0,header=True,encoding='utf-8-sig')

#使用pandas的groupby之後轉成List，其中每個元素會是tuple，第一項是goupby的值，第二項為datarame
a = job_pd.groupby('FeatCount') #根據'date'這個欄位做groupby

for item in list(a):
    print(item[0])
    item[1].dropna(axis=1,how='any',inplace=True)
    item[1].to_csv('./FeatCountPeoPle{}.csv'.format(item[0]), encoding='utf-8-sig', index=0)




