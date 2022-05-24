import pandas as pd
import numpy as np
import pickle
import re

from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# JAVA_HOME PATH 오류 관련 처리
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras.utils import to_categorical
from keras.preprocessing.text import *
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import OneHotEncoder

# dataframe print(확인용)
pd.set_option('display.unicode.east_asian_width', True)

df = pd.read_csv('C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/워크넷.csv')
print(df)
print(df.info())

# 중복값 제거
df.drop_duplicates(subset=['제목'], inplace=True)
df.reset_index(drop=True, inplace=True)
print(df['제목'].duplicated().sum())

# 결측값 제거
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

# 문자(한글, 영문)과 숫자만 남기고 특수문자 제거
df['제목'] = [re.sub('[^A-Za-z0-9가-힣]', '', str(s)) for s in df['제목']]
print(df['제목'])

# 문자(한글, 영문)과 숫자만 남기고 특수문자 제거
df['직무내용'] = [re.sub('[^A-Za-z0-9가-힣]', '', str(s)) for s in df['직무내용']]
print(df['직무내용'])

# feature, target 분리
X = df['제목'] + " " + df['직무내용']
Y = df['모집분야']

# target encoding 및 encoder 저장
# label encoding
encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
label = encoder.classes_
print(label)
print(labeled_Y)

# 나중에 다른 문장을 토큰화할때 동일한 classes_로 인코딩해야함 -> 학습시킨 encoder 저장
# pickle로 저장 / 불러오기시 원본의 데이터 타입 그대로 유지
with open('C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/category_encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)

# 데이터 형태소 분석
okt = Okt()
for i in range(len(X)):
    X[i] = okt.nouns(X[i])
print(X)

# stopword 로드
stopwords = pd.read_csv('C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/stopword.csv')
print(stopwords)


# 함수로 만들어 기존 데이터에 apply해 stopword 제거
def delete_stopwords(lst):
    words = [
        word for word in lst if word not in list(stopwords["stopword"]) and len(word) > 1
    ]
    return " ".join(words)


X = X.apply(delete_stopwords)

# 토큰화 및 저장
# stopword 제거한 뉴스 타이틀 토큰화
token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[0])

# 나중에 다른 문장을 토큰화할때 같은 단어는 같은 숫자로 매핑해야함 -> 학습시킨 Tokenizer 저장
# pickle로 저장 / 불러오기시 원본의 데이터 타입 그대로 유지
with open('C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/category_token.pickle', 'wb') as f:
    pickle.dump(token, f)

# 단어의 개수 출력 / padding한 0을 포함하기 위해 +1
wordsize = len(token.word_index) + 1  # word_index는 토큰화한 단어와 숫자 보여줌 / 0을 포함하지 않고 1부터 시작
print(wordsize)

# 문장 길이 맞춤
# 형태소가 가장 많은 문장의 단어 수
max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

# 길이가 맞게 앞쪽에 0 붙여줌
X_pad = pad_sequences(tokened_X, max)
print(X_pad[:10])

# 데이터 저장
X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.1
)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save(f'C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/news_data_max_{max}_size_{wordsize}.npy', xy)
