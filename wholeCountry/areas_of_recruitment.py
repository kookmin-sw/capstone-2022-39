import pickle
import re
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
from keras.models import model_from_json
import pandas as pd


# LabelEncoder 로드
with open(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\category_encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
category = encoder.classes_
# print(category)

# 정수 인코딩을 위한 토큰 가져오기
with open(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\category_token.pickle', 'rb') as f:
    train_tokenizer = pickle.load(f)

# 모델 로드
json_file = open(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

model.load_weights(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\category_classification_0.7607.h5')

stopwords = pd.read_csv(r'C:\Users\Admin\Documents\GitHub\capstone-2022-39\data\stopword.csv')


def areas_of_recruitment(title):
    title = re.sub('[^A-Za-z0-9가-힣]', '', title)
    # print(title)

    okt = Okt()
    okt_title = okt.morphs(title)

    result = []
    if len(okt_title) > 1:
        if okt_title not in list(stopwords['stopword']):
            result.append(okt_title)

    tokened_Title = train_tokenizer.texts_to_sequences(okt_title)
    # print(tokened_Title)

    X_pad = pad_sequences(tokened_Title, 337)
    # print(X_pad)

    pred_test = model.predict(X_pad)
    single_pred_test = pred_test.argmax(axis=1)
    idx = np.max(single_pred_test)

    return category[idx]
