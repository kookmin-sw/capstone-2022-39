import numpy as np
from keras.models import Sequential
from keras.layers import *

X_train, X_test, Y_train, Y_test = np.load('C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/nouns_announcement_data_max_337_size_37316.npy', allow_pickle=True)
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

# LSTM
model = Sequential()
model.add(Embedding(input_dim=37316,
                    output_dim=200,
                    input_length=337))
model.add(Conv1D(32, kernel_size=9, padding='same', activation='relu'))
model.add(MaxPool1D(pool_size=1))
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(13, activation='softmax'))
print(model.summary())

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=256, epochs=3, validation_data=(X_test, Y_test))

score = model.evaluate(X_test, Y_test)
print(score[1])

model_json = model.to_json()
with open("C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights(f'C:/Users/Admin/Documents/GitHub/capstone-2022-39/data/category_announcement_classification_{score[1]:.4f}.h5')
