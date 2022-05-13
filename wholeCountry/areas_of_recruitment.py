import pickle
import re
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
from keras.models import model_from_json
import pandas as pd

category = ['건설·채굴',
            '경영·사무',
            '기계·금속',
            '농립·어업',
            '보건·의료',
            '사회복지',
            '서비스직',
            '연구·공학기술',
            '영업·판매·운송',
            '예술·엔터테인먼트',
            '전자·정보통신',
            '제조업',
            '화학·섬유·식품가공']

# 정수 인코딩을 위한 토큰 가져오기
with open(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\news_token.pickle', 'rb') as f:
    train_tokenizer = pickle.load(f)

# load json and create model
json_file = open(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\news_classification_0.7214.h5')
# print("Loaded model from disk")
stopwords = pd.read_csv(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\stopword.csv')
# print(stopwords)


def areas_of_recruitment(title):
    title = re.sub('[^A-Za-z0-9가-힣]', '', title)
    # print(title)

    okt = Okt()
    okt_title = okt.morphs(title)
    # okt_title_ex = okt.nouns(title)
    # print(okt_title_ex)
    # print(okt_title)

    result = []
    if len(okt_title) > 1:
        if okt_title not in list(stopwords['stopword']):
            result.append(okt_title)
    # okt_title = ''.join(map(str, result))
    # print(okt_title)

    tokened_Title = train_tokenizer.texts_to_sequences(okt_title)
    # print(tokened_Title)

    X_pad = pad_sequences(tokened_Title, 24)
    # print(X_pad)

    pred_test = model.predict(X_pad)
    single_pred_test = pred_test.argmax(axis=1)
    idx = np.max(single_pred_test)
    # print(idx)
    # print(category[idx])

    return category[idx]
