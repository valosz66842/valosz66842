#coding=utf-8
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


#### 資料夾名稱 ####
folder_name = 'history'
#### 要搜尋的新聞日期 (20200121(含)之後才有完整資料) ####
date = '20200131'
#### 讀取所有新聞合併的dataframe ####
df = pd.read_csv(r'C:\Users\Big data\PycharmProjects\pyAI2\all_news_similarity_files.csv')


# ===============================================================================
# ===============================================================================
# 將指定日期的所有新聞標題及內文合併成一個string===================================
s = ''
for i in range(len(df)):
    if str(df['date'][i]) == date:  # 歷史新聞符合指定日期時才加進str
        s = s + str(df['title'][i]) + '\n' + str(df['content'][i]) + '\n'
#print(s)


# 停用字字典(將停用字放在一個list裡面)==============================================
stopword_path = r'./stopwords_v2.txt'
stopword_list = []
with open (stopword_path, 'r', encoding = 'utf-8', errors='ignore') as f:
    for eachline in f.readlines():
        eachline = eachline.strip()  # 去除前後空白
        stopword_list.append(eachline.replace('\n', ''))
#print(stopword_list)


# 加入自定義字典 & 繁中字典=========================================================
jieba.load_userdict('self_define_dict.txt')  ### 自定義字典一定要放在繁中字典的code下面!!!!!
jieba.set_dictionary('dict.txt.big_new.txt')


# JIEBA斷詞=========================================================================
str_cut = jieba.cut(s)
str_cut_with_space = " ".join(str_cut)  #### string形式
#print(str_cut_with_space)

str_cut_list = str_cut_with_space.split(" ")  #### list形式
#print(str_cut_list)


# 分詞後的結果變成字典做字數統計========================================================
word_count = {}
for word in str_cut_list:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1
#print(word_count)


# 將字典轉為TUPLE，且存為list========================================================
# (長度大於１、且不在停用字字典裡、且不包含"\r\n")====================================
word_list = [(k, word_count[k]) for k in word_count if len(k) > 1 and k not in stopword_list and k != "\r\n"]


# 用每個元素的第2個元素排序(由大至小)==================================================
word_list.sort(key = lambda x : x[1], reverse = True)
print("日期：{} 關鍵字出現頻率排序 : ".format(date))
print(word_list)


# 轉為字典格式(做文字雲頻率用)=========================================================
word_dict = dict(word_list)
#print(word_dict)


# ================================WORDCLOUD===========================================
# 生成文字雲 (中文字體需要另外下載才能顯示https://www.google.com/get/noto/#serif-hant)
# ====================================================================================
font = r'C:\Users\Big data\PycharmProjects\pyAI2\NotoSansCJKtc-Black.otf'  # 字體路徑
cloud = WordCloud(font_path = font,
                  background_color = "black",       # 底色
                  max_words = 2000,                 # 詞數量
                  stopwords = set(stopword_list))   # 停用字

# 產生文字雲(使用出現頻率)
word_cloud = cloud.generate_from_frequencies(frequencies=word_dict)

# 輸出圖片
plt.axis('off')
plt.imshow(word_cloud)
plt.savefig('WordColud.png')
plt.show()


# 文字雲圖檔存檔=========================================================================
#cloud.to_file("./WordCloud_{}.jpg".format(date))
# ======================================================================================
