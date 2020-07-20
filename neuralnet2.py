import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import MeanSquaredError
from keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

companies = pickle.load(open("save.p", "rb"))
ticker = companies[0]

dropouts = [0.2, 0.3, 0.4, 0.5]
features = pd.read_pickle(ticker + '_features.pkl')  # load financial data
#features = features.drop(['grossProfit', 'operatingIncome', 'commonStockIssued', 'commonStockRepurchased',
                          #'dividendsPaid'], axis=1)
features = features.drop(['grossProfit', 'Current Ratio', 'Quick Ratio', 'Cash Ratio', 'debt_equity',
                           'Volume', 'netIncome'], axis=1)
labels = pd.read_pickle(ticker + '_mrktcaps.pkl')
labels = labels.drop(['date'], axis=1)
labels = np.array(labels.iloc[1:])
samples = np.array(features.iloc[1:])

train_samples, test_samples, train_labels, test_labels = train_test_split(samples, labels, test_size=0.1,
                                                                          random_state=42)
scaler = StandardScaler()
train_samples = scaler.fit_transform(train_samples)
test_samples = scaler.fit_transform(test_samples)


for rate in dropouts:
    print(rate)
    model = Sequential([Dense(units=8, input_shape=(7,), activation='relu'),
                        Dropout(rate),
                        Dense(units=4, activation='linear'),
                        ])
    model.compile(optimizer=Adam(learning_rate=0.00000001), loss='MeanSquaredError', metrics=['accuracy'])
    model.fit(x=train_samples, y=train_labels, batch_size=6, epochs=11, validation_data=(test_samples, test_labels),
              verbose=2)

