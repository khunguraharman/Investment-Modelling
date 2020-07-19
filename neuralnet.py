import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import MeanSquaredError
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.utils import shuffle
import numpy as np
import pickle

companies = pickle.load(open("save.p", "rb"))

for ticker in companies:
    features = pd.read_pickle(ticker + '_features.pkl')  # load financial data
    #features = features.drop(['grossProfit', 'operatingIncome', 'commonStockIssued', 'commonStockRepurchased',
                              #'dividendsPaid'], axis=1)
    features = features.drop(['Quick Ratio', 'Cash Ratio', 'debt_equity', 'commonStockIssued', 'commonStockRepurchased',
                               'dividendsPaid'], axis=1)
    labels = pd.read_pickle(ticker + 'avgprices.pkl')
    train_labels = np.array(labels.iloc[1:])
    train_samples = np.array(features.iloc[1:])
    train_labels, train_samples = shuffle(train_labels, train_samples)
    scaler = StandardScaler()
    scaled_train_samples = scaler.fit_transform(train_samples)
    model = Sequential([Dense(units=8, input_shape=(8,), activation='relu'),
                        Dense(units=4, activation='linear'),
                        ])
    model.compile(optimizer=Adam(learning_rate=0.00000001), loss='MeanSquaredError', metrics=['accuracy'])
    model.fit(x=scaled_train_samples, y=train_labels, batch_size=7, epochs=10, shuffle=True, verbose=2)

