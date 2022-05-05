import pandas as pd
import numpy as np
import pickle
import re

from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras.utils import to_categorical
from keras.preprocessing.text import *
from keras.preprocessing.sequence import pad_sequences


# dataframe print(확인용)
pd.set_option('display.unicode.east_asian_width', True)


df = pd.read_csv('C:/Python/공고수집/중요/워크넷(공고-제목,모집분야).csv')
print(df)
print(df.info())

# 중복값 제거
df.drop_duplicates(subset=['제목'], inplace=True)
df.reset_index(drop=True, inplace=True)
print(df['제목'].duplicated().sum())

# 문자(한글, 영문)과 숫자만 남기고 특수문자 제거
df['제목'] = [re.sub('[^A-Za-z0-9가-힣]', '', s) for s in df['제목']]
print(df['제목'])

# feature, target 분리
X = df['제목']
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
with open('C:/Python/category_encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

# one-hot encoding
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)

# 형태소 분석
# 첫 뉴스 타이틀 형태소 분석
okt = Okt()
print(type(X))
okt_X = okt.morphs(X[0])
print(X[0])
print(okt_X)

# 데이터 형태소 분석
for i in range(len(X)):
    X[i] = okt.morphs(X[i])
print(X)

# stopword 로드
stopwords = pd.read_csv('C:/Python/stopword.csv')
print(stopwords)

# for문으로 stopword 제거
for i in range(len(X)):
    result = []
    for j in range(len(X[i])):
        if len(X[i][j]) > 1:
            if X[i][j] not in list(stopwords['stopword']):
                result.append(X[i][j])
    X[i] = ' '.join(result)
print(X)

# 토큰화 및 저장
# stopword 제거한 뉴스 타이틀 토큰화
token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[0])

# 나중에 다른 문장을 토큰화할때 같은 단어는 같은 숫자로 매핑해야함 -> 학습시킨 Tokenizer 저장
# pickle로 저장 / 불러오기시 원본의 데이터 타입 그대로 유지
with open('C:/Python/news_token.pickle', 'wb') as f:
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
