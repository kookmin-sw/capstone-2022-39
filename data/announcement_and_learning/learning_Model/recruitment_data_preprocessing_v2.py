import pandas as pd
import numpy as np
import pickle
import re

from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from keras.preprocessing.text import *
from keras.preprocessing.sequence import pad_sequences

# dataframe print
pd.set_option('display.unicode.east_asian_width', True)

df = pd.read_csv('C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/워크넷.csv', index_col=0).reset_index()
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
df['제목'] = [re.sub('[^A-Za-z0-9가-힣]', '', s) for s in df['제목']]
print(df['제목'])

# 문자(한글, 영문)과 숫자만 남기고 특수문자 제거
df['직무내용'] = [re.sub('[^A-Za-z0-9가-힣]', '', s) for s in df['직무내용']]
print(df['직무내용'])

X = df['제목'] + " " + df['직무내용']
Y = df[['모집분야']]

encoder = OneHotEncoder(sparse=False)
onehot_Y = encoder.fit_transform(Y)
label = encoder.categories_
print(label)
print(onehot_Y)

# 나중에 다른 문장을 토큰화할때 동일한 classes_로 인코딩해야함 -> 학습시킨 encoder 저장
# pickle로 저장 / 불러오기시 원본의 데이터 타입 그대로 유지
with open('/data/category_onehot_encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

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

# stopword 제거한 뉴스 타이틀 토큰화
token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[0])

# 단어의 개수 출력 / padding한 0을 포함하기 위해 +1
wordsize = len(token.word_index) + 1  # word_index는 토큰화한 단어와 숫자 보여줌 / 0을 포함하지 않고 1부터 시작
print(wordsize)

with open('/data/category_token.pickle', 'wb') as f:
    pickle.dump(token, f)

# 형태소가 가장 많은 문장의 단어 수
max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

# 길이가 맞게 앞쪽에 0 붙여줌
X_pad = pad_sequences(tokened_X, max)
print(X_pad[:10])

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size = 0.1
)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save(f'C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/nouns_announcement_data_max_{max}_size_{wordsize}.npy', xy)