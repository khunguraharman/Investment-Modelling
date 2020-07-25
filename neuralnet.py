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
neurons = [8, 16, 32, 64]
dropouts = [0.2, 0.3, 0.4, 0.5]
features = pd.read_pickle(ticker + '_features.pkl')  # load financial data
#features = features.drop(['grossProfit', 'operatingIncome', 'commonStockIssued', 'commonStockRepurchased',
                          #'dividendsPaid'], axis=1)
features = features.drop(['Quick Ratio', 'Cash Ratio', 'debt_equity', 'commonStockIssued', 'commonStockRepurchased',
                           'dividendsPaid'], axis=1)

labels = pd.read_pickle(ticker + 'avgprices.pkl')
labels = np.array(labels.iloc[1:])
samples = np.array(features.iloc[1:])
scaler = StandardScaler()
scaled_samples = scaler.fit_transform(samples)
train_samples, test_samples, train_labels, test_labels = train_test_split(samples, labels, test_size=0.1,
                                                                          random_state=42)
for neuron in neurons:
    for rate in dropouts:
        print(neuron)
        print(rate)
        model = Sequential([Dropout(rate, input_shape=(8,)),
                            Dense(units=neuron, activation='relu'),
                            Dense(units=4, activation='linear'),
                            ])
        model.compile(optimizer=Adam(learning_rate=0.00000001), loss='MeanSquaredError', metrics=['accuracy'])
        model.fit(x=scaled_train_samples, y=train_labels, batch_size=10, epochs=7, shuffle=True, verbose=2)

