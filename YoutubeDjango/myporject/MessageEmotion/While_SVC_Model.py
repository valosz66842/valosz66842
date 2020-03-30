import jieba
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.classification import accuracy_score
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
import joblib
from opencc import OpenCC
import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import os
import time
import lxml.html
import re
import pickle
pwd=os.path.dirname(__file__)
jieba.set_dictionary(pwd+r'/dict.txt.big_new.txt')
# 加入我們從維基百科建立的自訂字典:self_define_dict.txt
jieba.load_userdict(pwd+r'/self_define_dict.txt')



FilePath=pwd
ImgPath=r'./static/images'
WordCloud_Dice = {}
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
        for name in file_csv:
# 使用網路上簡體的中文詞庫
            data_con=pd.read_csv("./{}".format(name))
            video_id=name[:-4]
# 清理為空值的 clean content，但事實上並沒有空值
            data_con = data_con[pd.notnull(data_con['clean_con'])]
            # 對留言做斷詞
            cut_content = []
            # 中文斷詞
            for i, cont in enumerate(data_con['clean_con']):
                cut_content.append(" ".join(list(jieba.cut(cont))))
            # 加入df的新欄位: 分詞後結果
            data_con['cut_content'] = cut_content
            # 將留言轉成vector
            # load tfidf_model
            tfidf_model = pickle.load(open("./tfidf1.pkl", 'rb'))
            # tfidf_model = TfidfVectorizer(sublinear_tf=True, min_df=2, norm='l2').fit(data_con.cut_content)
            # using .transform instead of fit_transform
            # ref:https://stackoverflow.com/questions/52150800/valueerror-x-has-1709-features-per-sample-expecting-2444
            features = tfidf_model.transform(data_con.cut_content).toarray()
            print(features.shape)
            # 使用已經訓練的model直接預測
            # load the model from disk
            loaded_model = joblib.load('./LinearSVC.sav')
            y_pred = loaded_model.predict(features)
            # 將模型下標的結果記下來
            data_con['model_label'] = y_pred
            out_label = ['Pos', 'Neg']
            out_count = [0, 0]
            for n in y_pred:
                if n == 0.:
                    out_count[1] += 1
                elif n == 1.:
                    out_count[0] += 1
            print(out_count)
            # 畫圓餅圖
            # ref:https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
            # ref: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.pie.html
            # color:https://matplotlib.org/3.1.0/gallery/color/named_colors.html
            # plt.pie(out_count, labels=out_label, colors= ['cyan', 'magenta'], autopct='%.0f%%',textprops={'fontsize': 14})
            plt.pie(out_count, labels=out_label, colors=['cornflowerblue', 'coral'], autopct='%.0f%%',
                    textprops={'fontsize': 14})
            plt.title('Sentiment anlysis of video comments', fontsize=16)
            fig=plt.gcf()
            fig.set_size_inches(12,8)
            fig.savefig(ImgPath+'/sentiment_pie_{}.png'.format(video_id))
            time.sleep(10)
            os.remove(ImgPath+'/sentiment_pie_{}.png'.format(video_id))
            plt.close()
    except Exception as e:
        print(e)
        pass