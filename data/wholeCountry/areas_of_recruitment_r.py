import pandas as pd
import numpy as np
import re
from keras.models import *
from keras.preprocessing.sequence import pad_sequences
import pickle
from konlpy.tag import Okt

# 모델 로드
json_file = open(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\category_announcement_classification_0.7645.h5')


# Tokenizer 로드
with open(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\category_token.pickle', 'rb') as f:
    token = pickle.load(f)

# LabelEncoder 로드
with open(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\category_onehot_encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
category = encoder.categories_[0]
# print(category)

# stopword 로드
stopwords = pd.read_csv(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\stopword.csv')
# print(stopwords)


def delete_stopwords(lst):
    words = []
    if lst not in list(stopwords['stopword']) and len(lst) > 1:
        words.append(lst)
    return ' '.join(words)


def areas_of_recruitment(title):
    title = re.sub('[^A-Za-z0-9가-힣]', '', title)

    okt = Okt()
    okt_title = okt.nouns(title)

    # okt_title = okt_title.apply(delete_stopwords)

    result = []
    if len(okt_title) > 1:
        if okt_title not in list(stopwords['stopword']):
            result.append(okt_title)

    tokened_Title = token.texts_to_sequences(okt_title)

    # 길이가 맞게 앞쪽에 0 붙여줌
    X_pad = pad_sequences(tokened_Title, 337)
    # print(X_pad[:10])

    predict = model.predict(X_pad)

    return category[np.argmax(predict[0])]
