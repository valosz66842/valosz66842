import pandas as pd
#該程式試著將一個擁有大量資料的csv檔根據某一個欄位值做groupby，並且將分開來的dataframe各自再存成新的csv檔
#這邊範例使用ettoday_news_manydays.csv這個檔案，將根據 "日期" 將新聞分割成各自的csv檔

#讀入新聞總檔案
data = pd.read_csv(r'C:\Users\Big data\PycharmProjects\pyAI2\FeatCount2\split\FeatCount2.csv')

#使用pandas的groupby之後轉成List，其中每個元素會是tuple，第一項是goupby的值，第二項為datarame
a = data.groupby('MainClass') #根據'date'這個欄位做groupby

for item in list(a):
    print(item[0])
    item[1].dropna(axis=1,how='any',inplace=True)
    item[1].to_csv(r'C:\Users\Big data\PycharmProjects\pyAI2\FeatCount2\split\FeatCountPeoPleClass{}.csv'.format(item[0]), encoding='utf-8-sig', index=0)

#比較簡潔的寫法請先參考就好，核心概念與上邊的範例相同
#out = [v for k, v in data.groupby('date')]
#print(out[0]['date'])