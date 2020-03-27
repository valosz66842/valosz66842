#coding=utf-8
import jieba
from gensim import corpora, models, similarities
import pandas as pd
import pickle


# 停用字字典(將停用字放在一個list裡面)============================================================
stopword_path = r'./stopwords_v2.txt'
stopword_list = []
with open (stopword_path, 'r', encoding = 'utf-8') as f:
    for eachline in f.readlines():
        eachline = eachline.strip()  # 去除前後空白
        stopword_list.append(eachline.replace('\n', ''))
# 加入自定義字典 & 繁中字典======================================================================
jieba.set_dictionary('dict.txt.big_new.txt')
jieba.load_userdict('self_define_dict.txt')  ### 自定義字典一定要放在繁中字典的code下面!!!!!
################################################################################################
##################### 將 ettoday 舊 新 聞 斷 詞 完 後 先 存 成 LIST##############################
################################################################################################
# # 讀取ettoday舊新聞合併的dataframe=====================================================================
# df = pd.read_csv('C:/Users/vicky/PycharmProjects/vk/youtube_project/ettoday_random_news/all_ettoday_random_news.csv')
#
# # 將dataframe有出現的日期變成一個list(照順序排)========================================================
# date_list = sorted(list(df.drop_duplicates(subset='date', keep='first',inplace=False)['date']))  # 去除日期重複值
# date_list= [str(d) for d in date_list]  # int轉str
#
# # 將ettoday舊新聞,依日期一天存成一個元素在一個list======================================================
# ettoday_doc = []
# for d in date_list:
#     s = ''
#     for i in range(len(df)):
#         if str(df['date'][i]) == d:  # 歷史新聞符合指定日期時才加進str
#             s = s + str(df['title'][i]) + '\n' + str(df['content'][i]) + '\n'
#     ettoday_doc.append(s)
#
# # 將ettoday_doc=[]內容做斷詞、只取長度大於１、且不在停用字字典裡、且不包含"\r\n"=====================
# # (變二維矩陣)
# ettoday_doc_cut = []
# for doc in ettoday_doc:
#     doc_list = [word for word in jieba.cut(doc) if len(word) > 1 and word not in stopword_list and word != "\r\n"]
#     ettoday_doc_cut.append(doc_list)
#
# # 將ettoday_doc_cut這個LIST存成pickle檔案==========================================================
# pickle_out = open("ettoday_old_list.pickle","wb")
# pickle.dump(ettoday_doc_cut, pickle_out)
# pickle_out.close()
###################################################################################################
###################################################################################################
# 將斷好詞的ettoday舊新聞LIST讀回(保留原始LIST型態)==================================================
pickle_in = open("ettoday_old_list.pickle","rb")
ettoday_doc_cut = pickle.load(pickle_in)
#====================================================================================================
# 讀取所有""其他要被比較的""新聞檔案===================================================================
df_others = pd.read_csv('C:/Users/vicky/PycharmProjects/vk/youtube_project/auto_crawl/NEWS/news_similarity_files/all_news_similarity_files.csv')
# 將有出現的日期變成一個list(照順序排)=================================================================
date_list = sorted(list(df_others.drop_duplicates(subset='date', keep='first',inplace=False)['date']))  # 去除日期重複值
date_list= [str(d) for d in date_list]  # int轉str
# 依日期一天存成一個元素在一個list=====================================================================
others_doc = []
for d in date_list:
    s = ''
    for i in range(len(df_others)):
        if str(df_others['date'][i]) == d:  # 歷史新聞符合指定日期時才加進str
            s = s + str(df_others['title'][i]) + '\n' + str(df_others['content'][i]) + '\n'
    others_doc.append(s)
# 將others_doc=[]內容做斷詞、只取長度大於１、且不在停用字字典裡、且不包含"\r\n"=====================
# (變二維矩陣)
others_doc_cut = []
for doc in others_doc:
    doc_list = [word for word in jieba.cut(doc) if len(word) > 1 and word not in stopword_list and word != "\r\n"]
    others_doc_cut.append(doc_list)
# 將ettoday舊新聞和其他要被比較的新聞合成一個list====================================================
all_doc_cut = ettoday_doc_cut + others_doc_cut
# 基準日期讀取、斷詞================================================================================
df_base = pd.read_csv('C:/Users/vicky/PycharmProjects/vk/youtube_project/auto_crawl/NEWS/base_date/all_base_date.csv')
s_base = ''
for i in range(len(df_base)):
    s_base = s_base + str(df_base['title'][i]) + '\n' + str(df_base['content'][i]) + '\n'
print("基準日期: ", df_base['date'][1])
# 將s_base內容做斷詞、只取長度大於１、且不在停用字字典裡、且不包含"\r\n"===============================
# (變二維矩陣)
s_base_cut = [word for word in jieba.cut(s_base) if len(word) > 1 and word not in stopword_list and word != "\r\n"]
# ==============================================================================================
# 製作語料庫 ====================================================================================
# ==============================================================================================
# 用dictionary方法生成字典(其他文檔)
# corpora是用來表示每篇文檔的詞數, corpora是一種約定的表達方式,是一個二維矩陣
dictionary = corpora.Dictionary(all_doc_cut)
# 用數字對所有詞進行編號
dictionary.keys()
# 使用doc2bow製作語料庫(其他文檔)
# (語料庫是一組向量，向量中的元素是一個二元組(編號,次數）,對應分詞後的文檔中的每一個詞)
corpus = [dictionary.doc2bow(doc) for doc in all_doc_cut]
# 基準文檔也轉換為二元祖向量
doc_test_vec = dictionary.doc2bow(s_base_cut)
# 相似度分析 (使用TF-IDF模型對語料庫建模)(其他文檔)
tfidf = models.TfidfModel(corpus)
# 獲取基準文檔中，每個詞的TF-IDF值
tfidf_test_doc = tfidf[doc_test_vec]
#print(tfidf_test_doc)
# 對每個目標文檔(其他文檔)，分析與基準文檔的相似度
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
sim = index[tfidf_test_doc]
print("基準文檔({})和其他文檔的相似度：".format(df_base['date'][1]), sim)


# 用相似度排序
# news_acc_list = sorted(enumerate(sim), key=lambda item: -item[1])  #　sim是一個list,只有兩個值,第一個才是相似度的值
# print(news_acc_list)