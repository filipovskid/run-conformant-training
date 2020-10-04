import numpy as np
import pandas as pd
# import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.callbacks import LambdaCallback
# import matplotlib.pyplot as plt


def drboson_callback(drboson, logs, step):
    drboson.log({
        'val_loss': float(logs['val_loss']),
        'val_accuracy': float(logs['val_accuracy']),
        'loss': float(logs['loss']),
        'accuracy': float(logs['accuracy'])
    }, step=step)


def train_example(drboson, data_dir):
    dataset = pd.read_csv(data_dir.joinpath('train.csv'))
    X = dataset.iloc[:, :20].values
    y = dataset.iloc[:, 20:21].values

    sc = StandardScaler()
    X = sc.fit_transform(X)

    ohe = OneHotEncoder()
    y = ohe.fit_transform(y).toarray()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    model = Sequential()
    model.add(Dense(16, input_dim=20, activation='relu'))
    model.add(Dense(12, activation='relu'))
    model.add(Dense(4, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # history = model.fit(X_train, y_train, epochs=100, batch_size=64)

    y_pred = model.predict(X_test)

    pred = list()
    for i in range(len(y_pred)):
        pred.append(np.argmax(y_pred[i]))

    test = list()
    for i in range(len(y_test)):
        test.append(np.argmax(y_test[i]))

    a = accuracy_score(pred, test)
    print('Accuracy is:', a*100)

    logging_callback = LambdaCallback(
        on_epoch_end=lambda epoch, logs: drboson_callback(drboson, logs=logs, step=epoch)
        # on_batch_end=lambda batch, logs: print('batch', batch, 'logs', logs)
    )

    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=64,
                        callbacks=[logging_callback])
