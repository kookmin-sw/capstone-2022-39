import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

X_train, X_test, Y_train, Y_test = np.load('C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/news_data_max_337_size_37316.npy', allow_pickle=True)
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

# 모델 생성
model = Sequential()
model.add(Embedding(input_dim=37316,
                    output_dim=300,
                    input_length=337))
# 주변 값과의 연관성을 분석 하기 위해 사용
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu'))
model.add(MaxPool1D(pool_size=1))
# 뒷단에 LSTM을 다시 사용 하기 위해 return_sequences=True / 16개의 단어 모두 전달 하기 위해
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(13, activation='softmax'))
print(model.summary())

# 모델 학습
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=256, epochs=4, validation_data=(X_test, Y_test))

# 학습 과정 살펴 보기
fig, loss_ax = plt.subplots()

acc_ax = loss_ax.twinx()

loss_ax.plot(fit_hist.history['loss'], 'y', label='train loss')
loss_ax.plot(fit_hist.history['val_loss'], 'r', label='val loss')
loss_ax.set_ylim([0.0, 3.0])

acc_ax.plot(fit_hist.history['accuracy'], 'b', label='train_accuracy')
acc_ax.plot(fit_hist.history['val_accuracy'], 'g', label='val_accuracy')
acc_ax.set_ylim([0.0, 1.0])

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuray')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()

# 모델 검증 및 저장
score = model.evaluate(X_test, Y_test)
print(score[1])

# serialize model to JSON
model_json = model.to_json()
with open("C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights(f'C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/news_classification_{score[1]:.4f}.h5')
print("Saved model to disk")
