from __future__ import print_function
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
from keras.utils.np_utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

traindata = pd.read_csv('data/training_data_combined_ihr_30_spo2_60.csv', header=None)
testdata = pd.read_csv('data/test_data_combined_ihr_30_spo2_60.csv', header=None)


X = traindata.iloc[:,1:91]
Y = traindata.iloc[:,0]
C = testdata.iloc[:,0]
T = testdata.iloc[:,1:91]

scaler = Normalizer().fit(X)
trainX = scaler.transform(X)
# summarize transformed data
np.set_printoptions(precision=3)
#print(trainX[0:5,:])

scaler = Normalizer().fit(T)
testT = scaler.transform(T)
# summarize transformed data
np.set_printoptions(precision=3)
#print(testT[0:5,:])


y_train = np.array(Y)
y_test = np.array(C)


# reshape input to be [samples, time steps, features]
X_train = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
X_test = np.reshape(testT, (testT.shape[0], 1, testT.shape[1]))


batch_size = 16

# 1. define the network
def create_model():
  print("called")
  model = Sequential()
  model.add(LSTM(32,input_dim=90,return_sequences=True))  # try using a GRU instead, for fun
  model.add(Dropout(0.1))
  model.add(LSTM(32, return_sequences=False))  # try using a GRU instead, for fun
  model.add(Dropout(0.1))
  model.add(Dense(1))
  model.add(Activation('sigmoid'))
  model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
  return model

seed = 7
np.random.seed(seed)


model = KerasClassifier(build_fn=create_model, nb_epoch=100, batch_size=10, verbose=0)
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
results = cross_val_score(model, X_train, y_train, cv=kfold)
print(results.mean())
'''
# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
checkpointer = callbacks.ModelCheckpoint(filepath="logs/lstm5/checkpoint-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='val_acc', mode='max')
csv_logger = CSVLogger('logs/lstm5/training_set_iranalysis.csv',separator=',', append=False)
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=5000, validation_split=0.33,callbacks=[checkpointer,csv_logger])
model.save("logs/lstm5/lstm1layer_model.hdf5")
'''










