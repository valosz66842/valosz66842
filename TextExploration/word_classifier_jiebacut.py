import jieba
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import chi2
import pandas as pd
import numpy as np
#使用網路上簡體的中文詞庫
jieba.set_dictionary(r'./dict.txt.big_new.txt')
#加入我們從維基百科建立的自訂字典:self_define_dict.txt
jieba.load_userdict(r'./self_define_dict.txt')


df = pd.read_csv('./mearge_t2.csv',encoding='ANSI')

#清理為空值的 clean content，但事實上並沒有空值
df = df[pd.notnull(df['clean_content'])]

#轉換型別
df['label'] = df['label'].astype(float)

#挑選正負向的留言，和中性的留言(0.5)
df = df[(df['label'] == 1.0) | (df['label'] == 0.0) | (df['label'] == 0.5)]

#利用label這欄做成幾個類別
df['category_id'] = df['label'].factorize()[0]
#print(df[df['category_id'] == 0])

#利用['label', 'category_id']這兩欄作為依據，除去重複值做成類別的對照組?
category_id_df = df[['label', 'category_id']].drop_duplicates().sort_values('category_id')
#print(category_id_df)

#將category_id_df的對應做成字典的對照組合，將label做成key值，去對應category_id
#category_id_df.values是將dframe轉成矩陣
category_to_id = dict(category_id_df.values)
print('category_to_id: ',category_to_id)

#將category_id_df的對應做成字典的對照組合，將category_id做成key值，去對應label
id_to_category = dict(category_id_df[['category_id', 'label']].values)
print('id_to_category: ', id_to_category)

cut_content = []
#中文斷詞
for i, cont in enumerate(df['clean_content']):
    cut_content.append(" ".join(list(jieba.cut(cont))))

#加入df的新欄位: 分詞後結果
df['cut_content'] = cut_content
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_model = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2').fit(df.cut_content)

#查看每個詞的對應編號
print(tfidf_model.vocabulary_)

#注意:使用斷詞後，使用 ngram_range=(1, 2)會出錯，這個代表可以使用1個字詞或是2個字詞作連結的參數，也許是組合過多當機?
#tfidf_model = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2', ngram_range=(1, 2)).fit(df.cut_content)

features = tfidf_model.fit_transform(df.cut_content).toarray()
features.shape
labels = df.category_id


N = 2

for Product, category_id in sorted(category_to_id.items()):
    features_chi2 = chi2(features, labels == category_id)
    indices = np.argsort(features_chi2[0])

    feature_names = np.array(tfidf_model.get_feature_names())[indices]

    unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
    bigrams = [v for v in feature_names if len(v.split(' ')) == 2]

    print("# '{}':".format(Product))
    print(" . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
    print(" . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))

models = [ RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0), LinearSVC(), MultinomialNB(), LogisticRegression(random_state=0), ]
CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
    model_name = model.__class__.__name__
    #做cross validation (cv=5)，做成5折
    accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
    print(accuracies)
    for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name, fold_idx, accuracy))
        cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df, size=8, jitter=True, edgecolor="gray", linewidth=2)
plt.show()
cv_df.groupby('model_name').accuracy.mean()


model = LinearSVC()

X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


conf_mat = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(10,10))

sns.heatmap(conf_mat, annot=True, fmt='d', xticklabels=category_id_df.label.values, yticklabels=category_id_df.label.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()