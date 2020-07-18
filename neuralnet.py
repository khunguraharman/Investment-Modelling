import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.utils import shuffle
import numpy as np
import pickle

companies = pickle.load(open("save.p", "rb"))

for ticker in companies:
    features = pd.read_pickle(ticker + '_features.pkl')  # load financial data
    labels = pd.read_pickle(ticker + 'avgprices.pkl')
    train_labels = np.array(labels.iloc[1:])
    train_samples = np.array(features.iloc[1:])
    train_labels, train_samples = shuffle(train_labels, train_samples)
    scaler = StandardScaler()
    scaled_train_samples = scaler.fit_transform(train_samples.reshape(-1, 1))
    #model = Sequential([Dense(units=)])


