# -*- coding: utf-8 -*-
"""ML_LSTM_BERT (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kVSl7mB5P926rKY7y-ZJWtE6KPQkcPGJ
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
import re

from google.colab import drive
drive.mount('/content/drive')

"""# IMPORTING THE DATASET"""

data = pd.read_csv('/content/drive/MyDrive/ColabNotebooks/News.csv')

data.head()

"""# EXPLORATORY DATA ANALYSIS"""

data.shape

data.describe

data.info()

data.isna().sum()

print("Total no of unique Subject: ", len(data['subject'].unique()))

data.subject.value_counts()

data['Word_counts text']=data['text'].apply(lambda x: len(str(x.split())))
data['Word_counts title']=data['title'].apply(lambda x: len(str(x.split())))

data.head()

plt.figure(figsize=(15,10))
sns.countplot(x="Labels", data=data , palette="dark")
plt.title('Labels Vs. Count')

plt.figure(figsize=(15,10))
sns.countplot(x="subject", data=data , palette="dark")
plt.title('subject Vs. Count')

piedata = data['Labels']
plt.figure(figsize=(15,10))
piedata.value_counts().plot(kind = 'pie',autopct = '%.3f%%')
plt.title('Piechart showing distribution of targets')

plt.figure(figsize=(20,14))
sns.countplot(x="subject", data=data ,hue='Labels')

plt.figure(figsize=(20,14))
sns.countplot(y = data['subject'], order = data['subject'].value_counts().sort_values(ascending=False).iloc[0:25].index,palette='dark')
plt.title('Count Vs. Subjects')

l=[10,20,30,40,50,60,70,80,90,100]
for ele in l:
    print("{} percentile of counts is {}".format(ele,np.percentile(data['Word_counts text'],ele)))

l=[10,20,30,40,50,60,70,80,90,100]
for ele in l:
    print("{} percentile of counts is {}".format(ele,np.percentile(data['Word_counts title'],ele)))

plt.figure(figsize=(20,14))
sns.barplot(x='Labels', y='Word_counts title', data=data)
plt.title('Avg no. of words in news vs. Labels')

l=[1,2,3,4,5,6,7,8,9,10]
for ele in l:
    print("{} percentile of counts is {}".format(ele,np.percentile(data['Word_counts title'],ele)))

data.drop('subject',axis=1,inplace=True)
data.head()

data.drop('title',axis=1,inplace=True)
data.drop('date',axis=1,inplace=True)

data.head()

data.drop(['Unnamed: 0','Word_counts text','Word_counts title'],axis=1,inplace=True)

data.head()

"""#IMPORTING TEXT PROCESSING LIBRARIES"""

import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import inflect
p = inflect.engine()
!pip install contractions==0.0.18
import contractions

"""# DEFINING A PREPROCESSING FUNCTION"""

from nltk.stem import WordNetLemmatizer
def text_Preprocessing(text):
  def remove_emoji(text):
    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF"u"\U00002702-\U000027B0"u"\U000024C2-\U0001F251""]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)
  news =[contractions.fix(text) for text in text]
  news =[text.lower() for text in news]
  news =[re.sub(r'\S+@\S+','',text) for text in news]
  news =[re.sub(r'\d+','',text) for text in news]
  news =[re.sub(r'[^\w\s]','',text) for text in news]
  news =[text.strip() for text in news]
    

  stop_words=set(stopwords.words('english'))
  
  cleaned_news=[]
  for text in news:
    tokens =[word for word in word_tokenize(text) if not word in stop_words]
    cleaned_news.append(" ".join(tokens))

  lemmatizer = WordNetLemmatizer()
  lem_news=[]
  for text in news:
    lem_news.append(" ".join(list(map(lemmatizer.lemmatize , word_tokenize(text)))))
  
  return lem_news

t=data['text']
data['text'] =text_Preprocessing(t)
data.head()

"""# CONVERTING LABELS TO NUMERICAL VALUES"""

data.Labels=data.Labels.map({'True':0,'Fake':1})

data.head()

"""#SPLITTING THE DATA INTO X AND Y"""

x=data['text']
y=data['Labels']

x.head()

y.head()

"""# USING TF-IDF FOR VECTORIZATION OF TEXT DATA"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20)
tfidf = TfidfVectorizer(max_features=6000, analyzer='word', ngram_range=(1,1), stop_words='english',use_idf=True)
train = tfidf.fit_transform(x).toarray()

matrix1 = pd.DataFrame(train, columns=tfidf.get_feature_names())
matrix1

from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=0)
text_tsne = tsne.fit_transform(matrix1)
tsne_1 = np.vstack((text_tsne.T, y)).T
tsne_df = pd.DataFrame(data=tsne_1, columns=('Dim_1', 'Dim_2', 'Labels'))
tsne_df.head()

sns.FacetGrid(tsne_df, hue='Labels', size=6).map(plt.scatter, 'Dim_1', 'Dim_2').add_legend()
plt.show()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=4000, analyzer='word', ngram_range=(2,2), stop_words='english',use_idf=True)
train = tfidf.fit_transform(x).toarray()

matrix2 = pd.DataFrame(train,columns=tfidf.get_feature_names())
matrix2

from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=0)
text_tsne = tsne.fit_transform(matrix2)
tsne_1 = np.vstack((text_tsne.T, y)).T
tsne_df = pd.DataFrame(data=tsne_1, columns=('Dim_1', 'Dim_2', 'Labels'))
tsne_df.head()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=2000, analyzer='word', ngram_range=(3,3), stop_words='english',use_idf=True)
train = tfidf.fit_transform(x).toarray()

matrix3 = pd.DataFrame(train,columns=tfidf.get_feature_names())
matrix3

from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=0)
text_tsne = tsne.fit_transform(matrix3)
tsne_1 = np.vstack((text_tsne.T, y)).T
tsne_df = pd.DataFrame(data=tsne_1, columns=('Dim_1', 'Dim_2', 'Labels'))
tsne_df.head()

"""# SPLITTING THE DATA INTO TRAIN AND TEST SET"""

X_train, X_test, y_train, y_test = train_test_split(matrix1, y,stratify=y,test_size=0.25)

"""# CLASSICAL MACHINE LEARNING MODELS

**KNN**
"""

from sklearn.metrics import accuracy_score,f1_score,classification_report,confusion_matrix
from sklearn.neighbors import KNeighborsClassifier

k_cfl=KNeighborsClassifier(n_neighbors=1)
k_cfl.fit(X_train,y_train)
prediction=k_cfl.predict(X_test)
CM = confusion_matrix(y_test,prediction)
CR = classification_report(y_test,prediction)

print('The accuracy using K-NN is : {}'.format(accuracy_score(y_test,prediction)))
print('The F1-Score using K-NN is : {}'.format(f1_score(y_test,prediction, average='micro')))
print(CM)
print('The confusion matrix using K-NN is :')
CM_df = pd.DataFrame(CM,index = ['0','1'], columns = ['0','1'])
plt.figure(figsize=(20,14))
sns.heatmap(CM_df, annot=True, cmap="OrRd")
plt.title('Confusion Matrix')
plt.ylabel('Actal Values')
plt.xlabel('Predicted Values')
plt.show()

print('The classification report using K-NN is :')
print(CR)

"""**LOGISTIC REGRESSION**"""

from sklearn.linear_model import LogisticRegression

logisticR=LogisticRegression(penalty='l2',C=100,class_weight='balanced')
logisticR.fit(X_train,y_train)
prediction=logisticR.predict(X_test)
CM = confusion_matrix(y_test,prediction)
CR = classification_report(y_test,prediction)
print('The accuracy using LR is : {}'.format(accuracy_score(y_test,prediction)))
print('The F1-Score using LR is : {}'.format(f1_score(y_test,prediction, average='micro')))
print('The confusion matrix using LR for is :')
print(CM)
CM_df = pd.DataFrame(CM,index = ['0','1'], columns = ['0','1'])
plt.figure(figsize=(20,14))
sns.heatmap(CM_df, annot=True, cmap="OrRd")
plt.title('Confusion Matrix')
plt.ylabel('Actal Values')
plt.xlabel('Predicted Values')
plt.show()

print('The classification report using LR is :')
print(CR)

"""**RANDOM FOREST CLASSIFIER**"""

from sklearn.ensemble import RandomForestClassifier

r_cfl=RandomForestClassifier(n_estimators=1000,random_state=42,n_jobs=-1)
r_cfl.fit(X_train,y_train)
prediction=r_cfl.predict(X_test)
CM = confusion_matrix(y_test,prediction)
CR = classification_report(y_test,prediction)
print('The accuracy using RF is : {}'.format(accuracy_score(y_test,prediction)))
print('The F1-Score using RF is : {}'.format(f1_score(y_test,prediction, average='micro')))
print('The confusion matrix using RF is :')
print(CM)

CM_df = pd.DataFrame(CM,index = ['0','1'], columns = ['0','1'])
plt.figure(figsize=(20,14))
sns.heatmap(CM_df, annot=True, cmap="OrRd")
plt.title('Confusion Matrix')
plt.ylabel('Actal Values')
plt.xlabel('Predicted Values')
plt.show()

print('The classification report using RF is :')
print(CR)

"""**XGBOOST CLASSIFIER**"""

from xgboost import XGBClassifier

x_cfl=XGBClassifier(n_estimators=500,nthread=-1)
x_cfl.fit(X_train,y_train)
prediction=x_cfl.predict(X_test)
CM = confusion_matrix(y_test,prediction)
CR = classification_report(y_test,prediction)
print('The accuracy using XgBoost is : {}'.format(accuracy_score(y_test,prediction)))
print('The F1-Score using XgBoost is : {}'.format(f1_score(y_test,prediction, average='micro')))
print('The confusion matrix using XgBoost is :')
print(CM)

CM_df = pd.DataFrame(CM,index = ['0','1'], columns = ['0','1'])
plt.figure(figsize=(20,14))
sns.heatmap(CM_df, annot=True, cmap="OrRd")
plt.title('Confusion Matrix')
plt.ylabel('Actal Values')
plt.xlabel('Predicted Values')
plt.show()

print('The classification report using XgBoost is :')
print(CR)

"""# SUMMARY OF ML MODELS"""

from prettytable import PrettyTable
tb = PrettyTable()
tb.field_names= (" Vectorizer ", " Model ", " Best Hyperparameter "," Accuracy ",)
tb.add_row([" Tfidf", "KNN" , "K=1" , 80.95 ])
tb.add_row([" Tfidf", "Logistic Regression" , "C=100" , 99.38 ])
tb.add_row([" Tfidf", "Random Forest" , "Estimators=1000" , 99.78 ])
tb.add_row([" Tfidf", "XGBoost" , "Estimators=500" , 99.75 ])

print(tb.get_string(titles = "Observations"))

"""# BERT EMBEDDINGS"""

!pip install tensorflow_hub
!pip install bert-for-tf2
!pip install sentencepiece
!pip install tf-hub-nightly
import tensorflow as tf
import tensorflow_hub as hub
print("TF version: ", tf.__version__)
print("Hub version: ", hub.__version__)

def bert_encode(texts, tokenizer, max_len=512):
    all_tokens = []
    all_masks = []
    all_segments = []
    
    for text in texts:
        text = tokenizer.tokenize(text)
            
        text = text[:max_len-2]
        input_sequence = ["[CLS]"] + text + ["[SEP]"]
        pad_len = max_len - len(input_sequence)
        
        tokens = tokenizer.convert_tokens_to_ids(input_sequence)
        tokens += [0] * pad_len
        pad_masks = [1] * len(input_sequence) + [0] * pad_len
        segment_ids = [0] * max_len
        
        all_tokens.append(tokens)
        all_masks.append(pad_masks)
        all_segments.append(segment_ids)
    
    return np.array(all_tokens), np.array(all_masks), np.array(all_segments)

import tensorflow_hub as hub
module_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/1"
bert_layer = hub.KerasLayer(module_url, trainable=True)

!wget --quiet https://raw.githubusercontent.com/tensorflow/models/master/official/nlp/bert/tokenization.py
!pip install bert-for-tf2
import numpy as np
import tensorflow_hub as hub
from bert import bert_tokenization


vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = bert_tokenization.FullTokenizer(vocab_file, do_lower_case)

X_tr = bert_encode(X_train['text'].values, tokenizer, max_len=150)
X_te = bert_encode(X_test['text'].values, tokenizer, max_len=150)

pool_embeddings_tr=X_tr[0]
pool_embeddings_te=X_te[0]

"""# USING XGBCLASSIFIER ON BERT EMBEDDINGS"""

from xgboost import XGBClassifier
x_cfl=XGBClassifier(n_estimators=500,nthread=-1)
x_cfl.fit(pool_embeddings_tr,y_train)
prediction=x_cfl.predict(pool_embeddings_te)

# Commented out IPython magic to ensure Python compatibility.
from sklearn.metrics import accuracy_score,f1_score,classification_report,confusion_matrix
CM = confusion_matrix(y_test,prediction)
CR = classification_report(y_test,prediction)
print('The accuracy using Xgboost is : {}'.format(accuracy_score(y_test,prediction)))
print('The confusion matrix using Xgboost is :')
print(CM)
# %matplotlib inline
CM_df = pd.DataFrame(CM,index = ['0','1'], columns = ['0','1'])
plt.figure(figsize=(20,14))
sns.heatmap(CM_df, annot=True, cmap="OrRd")
plt.title('Confusion Matrix')
plt.ylabel('Actal Values')
plt.xlabel('Predicted Values')
plt.show()

from prettytable import PrettyTable
tb = PrettyTable()
tb.field_names= (" Vectorizer ", " Model "," Accuracy ")
tb.add_row([" BERT Embeddings", "LSTM"  , 99.37 ])

print(tb.get_string(titles = "Observations"))

"""#LSTM"""

y=data['Labels']
x=data['text']

y=pd.DataFrame(y)
x=pd.DataFrame(x)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

def normalize(data):
    normalized = []
    for i in data:
        i = i.lower()
        # get rid of urls
        i = re.sub('https?://\S+|www\.\S+', '', i)
        # get rid of non words and extra spaces
        i = re.sub('\\W', ' ', i)
        i = re.sub('\n', '', i)
        i = re.sub(' +', ' ', i)
        i = re.sub('^ ', '', i)
        i = re.sub(' $', '', i)
        normalized.append(i)
    return normalized

X_train = normalize(list(X_train['text'].values))
X_test = normalize(list(X_test['text'].values))

vocab_size = 10000
embedding_dim = 64
max_length = 256
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'

## tokenizer = Tokenizer(num_words=max_vocab)
from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(X_train)

import tensorflow as tf
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

X_train = tf.keras.preprocessing.sequence.pad_sequences(X_train, padding=padding_type, truncating=trunc_type, maxlen=max_length)
X_test = tf.keras.preprocessing.sequence.pad_sequences(X_test, padding=padding_type, truncating=trunc_type, maxlen=max_length)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(embedding_dim,  return_sequences=True)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(16)),
    tf.keras.layers.Dense(embedding_dim, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])

model.summary()

from tensorflow.keras.utils import plot_model
plot_model(model)

early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=5,validation_split=0.3, batch_size=64, shuffle=True, callbacks=[early_stop])

history_dict = history.history

acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']
epochs = history.epoch

plt.figure(figsize=(20,14))
plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss', size=15)
plt.xlabel('Epochs', size=15)
plt.ylabel('Loss', size=15)
plt.legend(prop={'size': 15})
plt.show()

model.evaluate(X_test, y_test)

from prettytable import PrettyTable
tb = PrettyTable()
tb.field_names= ( " Model "," Accuracy ")
tb.add_row([ "LSTM"  ,  99.85])

print(tb.get_string(titles = "Observations"))

"""#OBSERVATIONS

1. Out of all the ML models Random Forest and Logistic regression performed pretty well and had a good Accuracy.
2. Using Bidirectional LSTM we got improvement in our accuracy compared to that of ML models.
3. Using BERT embeddings and then XgBoost Classifier gave good accuracy but was not better than Random Forest and LSTM.
"""