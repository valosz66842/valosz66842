import pandas as pd
import jieba
import matplotlib.pyplot as plt
from random import randint
import datetime
import time
import os
import json
import seaborn as sns
import matplotlib
from matplotlib.font_manager import FontProperties
pwd=os.path.dirname(__file__)
def plot_keyword_djagram(Keyword,Day):
    with open(pwd+r'./wordcount_2020.json' , 'r', encoding='utf-8') as reader:
        data = json.loads(reader.read())
    #print(data)
    #print(len(data))
    keyword = Keyword
    #畫過去幾天
    daylimit = Day
    date_list = []
    wd_count = []
    ar_count = [] #article count
    for item in data:
        date_list.append(item['filedate'][4::])
        ar_count.append(item['data_length'])
        if item.get(keyword) == None:
            wd_count.append(0)
        else:
            wd_count.append(item.get(keyword))
    print(date_list)
    print(wd_count)
    #=== 處理word_count的normalize
    Max = max(ar_count)
    for i in range(len(wd_count)):
        wd_count[i] = int(wd_count[i]*Max/ar_count[i])
    # print('max ar: ', Max)
    # print('ar_count: ', ar_count)
    # print('改善後: ',wd_count)
    # print(' ========================= ')
    #设置输出的图片大小
    figsize = 11,9
    figure, ax = plt.subplots(figsize=figsize)
    #plt.plot(date_list[-1*daylimit::], wd_count[-1*daylimit::],linewidth=2)
    xlabe = date_list[-1*daylimit::]
    plt.bar(date_list[-1*daylimit::],wd_count[-1*daylimit::]);
    #設定x-axis
    ax.xaxis.set_tick_params(labelsize=14) #x-label size
    if daylimit >= 45:
        plt.xticks(xlabe[::4]) #x-label的區間
    elif daylimit >= 30:
        plt.xticks(xlabe[::3]) #x-label的區間
    elif daylimit >= 12:
        plt.xticks(xlabe[::2])
    plt.xlabel("Time(date in 2020)", fontsize=16, fontweight='bold')
    plt.ylabel("Discussion level", fontsize=16, fontweight='bold')
    #設定中文文字
    font = FontProperties(fname=r"msjh.ttc", size=20)
    plt.title('keyword: {}'.format(keyword), fontproperties=font)
    plt.savefig(pwd+r'/static/plt/{}{}.png'.format(keyword,InputDay))
    time.sleep(3)
    os.remove(pwd+r"/static/plt/{}{}.csv".format(keyword,
                                                                                                             InputDay))
    os.remove(pwd+r"/static/plt/{}{}.png".format(keyword,
                                                                                                             InputDay))

pwd=os.path.dirname(__file__)

FilePath=pwd+r'/static/plt'

def is_alphabet(keyword):
    return all(ord(c) < 128 for c in keyword)
while True:
#### 要搜尋的新聞日期 (20200121(含)之後才有完整資料) ####
    Folder_Path = FilePath  #csv目標資料夾
    os.chdir(Folder_Path)  # 換工作路徑
    file_list = os.listdir(Folder_Path)  # 這個資料夾內所有的檔案名稱
    file_csv = []
    for file in file_list:  # 只讀csv檔
        if '.csv' in file:
            file_csv.append(file)
    try:
        if len(file_csv) !=0:
            for name in file_csv:
                CsvPand=pd.read_csv(pwd+r"/static/plt/{}".format(name))
                KeyWord=CsvPand['KeyWord'][0]
                InputDay=CsvPand['InputDay'][0]
                plot_keyword_djagram(KeyWord,InputDay)
    except:
        pass
