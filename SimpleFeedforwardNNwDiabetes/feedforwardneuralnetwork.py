# -*- coding: utf-8 -*-
"""FeedforwardNeuralNetwork.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ztralj31JEoK-m6Ic1_9Us13XdnM1OZB
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler

import tensorflow as tf

df = pd.read_csv("/content/drive/MyDrive/ML Dataset/diabetes.csv");

df.head()

df.columns

for i in  range(len(df.columns[:-1])):
  label = df.columns[i]
  plt.hist(df[df['Outcome'] == 1][label], color='red', label= 'Diabetes', alpha=0.7, density= True, bins=15)
  plt.hist(df[df['Outcome'] == 0][label], color='yellow', label= 'No Diabetes', alpha=0.7, density= True, bins=15)
  plt.title(label)
  plt.ylabel('N')
  plt.xlabel(label)
  plt.legend()
  plt.show()

X = df[df.columns[:-1]].values

y= df[df.columns[-1]].values

X_train, X_temp, y_train, y_temp = train_test_split(X,y, test_size=0.4, random_state=0)
X_valid, X_test, y_valid, y_test = train_test_split(X_temp,y_temp, test_size=0.5, random_state=0)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001),
              loss = tf.keras.losses.BinaryCrossentropy(),
              metrics = ['accuracy'])

#lets test the model without any training.
model.evaluate(X_train, y_train)

#lets test again with the validation data.
model.evaluate(X_valid, y_valid)

model.fit(X_train, y_train, batch_size = 16, epochs = 24, validation_data=(X_valid,y_valid))

model.evaluate(X_test, y_test)

#the accuracy of our model is just 63%, which is pretty low, we want to improve it
#one possible reason for such low accuracy is that our X data is very varied or not normalized
#what this means, is that while columns like INSULIN has values ranging from 100 - 900, we
#also have columns like DIABETES_PEDIGREE_FN whose values are in range from 0-2.5, 

#this actually is hard for our model to train upon, so we can solve this problem by using normalization
#we will use StandardScaler for normalization.

#we will use normalize the X matrix.

scaler = StandardScaler()
X = scaler.fit_transform(X)
data = np.hstack((X, np.reshape(y, (-1, 1))))
transformed_df = pd.DataFrame(data, columns = df.columns)

for i in  range(len(transformed_df.columns[:-1])):
  label = transformed_df.columns[i]
  plt.hist(transformed_df[transformed_df['Outcome'] == 1][label], color='pink', label= 'Diabetes', alpha=0.7, density= True, bins=15)
  plt.hist(transformed_df[transformed_df['Outcome'] == 0][label], color='green', label= 'No Diabetes', alpha=0.7, density= True, bins=15)
  plt.title(label)
  plt.ylabel('N')
  plt.xlabel(label)
  plt.legend()
  plt.show()

#okay now that our data is normalized, we can tackle another issue with our data
#that is the total no. of people with diabetes is almost half of the 
#total no. of people without diabetes., we can confirm that using the following
len(transformed_df[transformed_df["Outcome"] == 1]), len(transformed_df[transformed_df["Outcome"] == 0])

# we want both the numbers to be closer, so there is equal chance of a sample
#being either 1 or 0.
#we can do that with RandomOversampler
over = RandomOverSampler()
X,y = over.fit_resample(X,y)
data = np.hstack((X, np.reshape(y, (-1, 1))))
transformed_df = pd.DataFrame(data, columns = df.columns)

len(transformed_df[transformed_df["Outcome"] == 1]), len(transformed_df[transformed_df["Outcome"] == 0])

#now lets create the model again, and observe the accuracy

X_train, X_temp, y_train, y_temp = train_test_split(X,y, test_size=0.4, random_state=0)
X_valid, X_test, y_valid, y_test = train_test_split(X_temp,y_temp, test_size=0.5, random_state=0)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001),
              loss = tf.keras.losses.BinaryCrossentropy(),
              metrics = ['accuracy'])

model.fit(X_train, y_train, batch_size = 16, epochs = 24, validation_data=(X_valid,y_valid))

model.evaluate(X_train, y_train)

model.evaluate(X_valid, y_valid)

model.evaluate(X_test, y_test)

