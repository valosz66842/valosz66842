import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble.forest import RandomForestRegressor
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn import preprocessing, linear_model
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVR
import os
Folder_Path = r'C:\Users\Big data\PycharmProjects\pyAI2\1Featdata'  #要拼接的所有文件
os.chdir(Folder_Path) #換工作路徑
file_list = os.listdir() #這個資料夾內所有的檔案名稱
file_csv=[]
for file in file_list: #只讀csv檔
    if '.csv' in file:
        file_csv.append(file)
print(file_csv)
#重複合作對象的組合，其影片的觀看數以澃中位數取代了，存成1_goupby_mainlookcount_median.csv
VideoPandas = pd.read_csv(r'C:\Users\Big data\PycharmProjects\pyAI2\1_goupby_mainlookcount_meanafsd.csv')
print('原始資料數',len(VideoPandas))
x=VideoPandas[['MainFollow','MainMedian','MainAvg','MainLookCount','Feat_median1','Feat_follow1','Feat_avg1']]
xAvg=x[['MainFollow','MainAvg','Feat_follow1','Feat_avg1']]
xMedian=x[['MainFollow','MainMedian','Feat_follow1','Feat_median1']]
y=x['MainLookCount']
sns.distplot(x['MainFollow']/1000, bins=20,kde=False)
def make_Data_type(df):  # 抓出資料的型態
  columns = df.columns.tolist()
  word={}
  for item in columns:
   if 'int' in str(df.dtypes[item]):
    word[str(item)]='mean'
   elif 'float' in str(df.dtypes[item]):
    word[str(item)]='mean'
  return word
VideoPandas = pd.read_csv(r'C:\Users\Big data\PycharmProjects\pyAI2\1_goupby_mainlookcount_meanafsd.csv')
data=VideoPandas.groupby(['MainID','Feat_channel1'],as_index=False).agg(make_Data_type(VideoPandas))
x=data[['MainFollow','MainMedian','MainAvg','MainLookCount','Feat_median1','Feat_follow1','Feat_avg1']]
xAvg=data[['MainFollow','MainAvg','Feat_follow1','Feat_avg1']]
xMedian=data[['MainFollow','MainMedian','Feat_follow1','Feat_median1']]
print('合併後資料數',len(x))
y=x['MainLookCount']
L_list=[]
RF_list=[]
models=[LinearRegression(),RandomForestRegressor(n_estimators=200, max_features='auto', oob_score=True)]
data=data[data["Feat_follow1"]<3200000] #因為台灣最高的Youtube人數只有318萬 這群人
print("刪除誤抓的資料後資料數",len(data))
x=data[['MainFollow','MainMedian','MainAvg','MainLookCount','Feat_median1','Feat_follow1','Feat_avg1']]
xAvg=data[['MainFollow','MainAvg','Feat_follow1','Feat_avg1']]
xMedian=data[['MainFollow','MainMedian','Feat_follow1','Feat_median1']]
y=x['MainLookCount']
L_list=[]
RF_list=[]
models=[LinearRegression(),RandomForestRegressor(n_estimators=200, max_features='auto', oob_score=True)]
print('--------------del outline-----------')
data = data[(data['MainAvg'] >= data['Feat_avg1']/20)]
data=data[['MainMedian', 'MainFollow', 'MainLookCount', 'MainAvg', 'Main_Quartile1', 'Main_Quartile3', 'Feat_median1', 'Feat_follow1', 'Feat_avg1', 'Feat_Quartile11', 'Feat_Quartile31']]
DataColums=data.columns.tolist()
data = preprocessing.scale(data)
data = pd.DataFrame(data,columns=['MainMedian', 'MainFollow', 'MainLookCount', 'MainAvg', 'Main_Quartile1', 'Main_Quartile3', 'Feat_median1', 'Feat_follow1', 'Feat_avg1', 'Feat_Quartile11', 'Feat_Quartile31'])
for Colums in DataColums:
    data=data[np.abs(data[str(Colums)]) < 3]
print("標準化之後的資料數",len(data))
x=data[['MainFollow','MainMedian','MainAvg','MainLookCount','Feat_median1','Feat_follow1','Feat_avg1']]
xAvg=data[['MainFollow','MainAvg','Feat_follow1','Feat_avg1']]
xMedian=data[['MainFollow','MainMedian','Feat_follow1','Feat_median1']]
y=x['MainLookCount']
L_list=[]
RF_list=[]
models=[LinearRegression(),RandomForestRegressor(n_estimators=200, max_features='auto', oob_score=True)]
print('----------------平均數------------------')
for i in range(10):
    for n,model in enumerate(models):
        x_train,x_test,y_train,y_test=train_test_split(xAvg,y,test_size=0.2,random_state=i)
        model.fit(x_train,y_train)
        predict=model.predict(x_test)
        if n==0:
            L_list.append((metrics.r2_score(y_test,predict)))
        if n==1:
            RF_list.append((metrics.r2_score(y_test,predict)))
print('R^2 of linear reg: {}, \nmean: {}'.format(L_list, (np.mean(L_list))))
print('R^2 of RF reg: {}, \nmean: {}'.format(RF_list, (np.mean(RF_list))))
plt.scatter(y_test, predict)
plt.xlabel("test set value")
plt.ylabel("predicted value")
plt.show()
# a=data.clumns.tolist()
# print(a)