from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
from keras.layers import Flatten
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import pickle

companies = pickle.load(open("save.p", "rb"))

for ticker in companies:
    features = pd.read_pickle(ticker + '_features.pkl')  # load financial data
    labels = pd.read_pickle(ticker + '_mrktcaps.pkl')
    train_labels = np.array(labels.iloc[1:])
    train_samples = np.array(features.iloc[1:])
    print(train_labels)
    print(train_samples)
