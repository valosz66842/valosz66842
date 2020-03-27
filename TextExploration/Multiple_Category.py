import jieba
import pandas as pd
#使用網路上簡體的中文詞庫
from sklearn.feature_selection import chi2
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
jieba.set_dictionary(r'.\dict.txt.big_new.txt')
jieba.load_userdict(r'.\self_define_dict.txt')
df = pd.read_csv(r'./all_comment_labeled.csv',encoding='utf8')#訓練資料集
df['label']=df['label'].astype(float)
df = df[(df['label'] == 1.0) | (df['label'] == 0.0)|(df["label"]==0.5)]#分成三類
df=df[pd.notnull(df['clean_content'])]#清除空直
df['classgrop']=df['label'].factorize()[0]#分組
class_grop_id=df[['label','classgrop']].drop_duplicates().sort_values('classgrop')#最後統計數字
cut_content=[]
for i in df['clean_content']:
    cut_content.append(" ".join(list(jieba.cut(i))))#斷詞
df['cut_content']=cut_content#斷詞完後放回原檔案
Tfidf_model=TfidfVectorizer(sublinear_tf=True,min_df=3,norm='l2').fit(df.cut_content)#亞向量
features=Tfidf_model.fit_transform(df.cut_content).toarray()#稀疏矩陣
print(features.shape)#看大小
labels=df.classgrop
models=[RandomForestClassifier(n_estimators=200,max_depth=3,random_state=0),LinearSVC(),MultinomialNB(),LogisticRegression(random_state=0),]#用RandomForestClassifier,LinearSVC,MultinomialNB,LogisticRegression
CV=5#做五次
cv_df=pd.DataFrame(index=range(CV*len(models)))
entries=[]
for model in models:
    model_name=model.__class__.__name__
    accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)#對模型進行評分
    print(accuracies)
    for fold_idx,accuracy in enumerate(accuracies):
        entries.append((model_name,fold_idx,accuracy))
        cv_df=pd.DataFrame(entries,columns=['model_name','fold_idx','accuracy'])
sns.boxplot(x='model_name',y="accuracy",data=cv_df)
sns.stripplot(x='model_name',y="accuracy",data=cv_df,size=8,jitter=True,edgecolor="gray",linewidth=2)#盒鬚圖看四種模型比較
plt.show()
for model in models:#用四個模型進行多元分類
    Precise=0#計算成功次數
    Failure=0#計算失敗次數
    X_train,X_test,y_train,y_test=train_test_split(features,labels,test_size=0.33,random_state=0)
    model.fit(X_train,y_train)
    y_pred=model.predict(X_test)
    conf_mat=confusion_matrix(y_test,y_pred)
    fig,ax=plt.subplots(figsize=(10,10))
    for n,conf in enumerate(conf_mat):
        Precise+=conf[n]
        Failure+=np.sum(conf)-conf[n]
    print('準確度:',Precise/(Precise+Failure))
    print('成功次數:',Precise)
    print('失敗次數:',Failure)
    sns.heatmap(conf_mat,annot=True,fmt='d',xticklabels=class_grop_id.label.values,yticklabels=class_grop_id.label.values)#畫出分類的圖
    plt.ylabel("Actual")
    plt.xlabel('predicted')
    plt.show()