import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from dlf.master_function import data_preprocessing, compute_diff
from dlf.master_function import calculate_directional_accuracy, update
from sklearn.metrics import mean_squared_error
import tensorflow as tf
import random

# Import the data
data = np.reshape(pd.read_excel('ISM_PMI.xlsx').values, (-1))
data = compute_diff(data, 1)

# Setting the hyperparameters
num_lags = 100
train_test_split = 0.80
neurons = 100
num_epochs = 10
batch_size = 200

# Creating the training and test sets
x_train, y_train, x_test, y_test = data_preprocessing(data, num_lags, train_test_split)

# Reshape the data to 3D for LSTM input
x_train = x_train.reshape((-1, num_lags, 1))
x_test = x_test.reshape((-1, num_lags, 1))

# Create the LSTM model
model = Sequential()

# Adding a first layer
model.add(LSTM(units = neurons, input_shape = (num_lags, 1)))

# Adding a second layer
model.add(Dense(neurons, activation = 'relu')) 

# Adding a third layer
model.add(Dense(neurons, activation = 'relu')) 

# Adding the output layer 
model.add(Dense(units = 1))

# Compiling the model
model.compile(loss = 'mean_squared_error', optimizer = 'adam')

def update_plot(epoch, logs):
    if epoch % 1 == 0:
        plt.cla()
        y_predicted_train = model.predict(x_train)
        plt.plot(y_train[-100:], label = 'Training data', color = 'black', linewidth = 2.5)
        plt.plot(y_predicted_train[-100:,], label = 'Predicted data', color = 'red', linewidth = 1)
        plt.title(f'Training Epoch: {epoch}')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.legend()
        plt.grid()
        plt.savefig(str(random.randint(1, 1000)))

# Create the dynamic plot
fig = plt.figure()

# Train the model using the on_epoch_end callback
class PlotCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        update_plot(epoch, logs)
        plt.pause(0.001)

plot_callback = PlotCallback()
history = model.fit(x_train, y_train, epochs = num_epochs, batch_size = batch_size, callbacks = [plot_callback])

# Predicting in the training set
y_predicted_train = model.predict(x_train)

# Predicting in the test set
y_predicted = model.predict(x_test)

# Performance evaluation
print('---')
print('Directional Accuracy Train = ', round(calculate_directional_accuracy(y_predicted_train, y_train), 2), '%')
print('Directional Accuracy Test = ', round(calculate_directional_accuracy(y_predicted, y_test), 2), '%')
print('RMSE Train = ', round(np.sqrt(mean_squared_error(y_predicted_train, y_train)), 10))
print('RMSE Test = ', round(np.sqrt(mean_squared_error(y_predicted, y_test)), 10))
print('---')

from tensorflow.keras.utils import plot_model
from IPython.display import Image

plot_model(model, to_file = 'Architecture.png', 
           show_shapes = True, 
           show_layer_names = True)
Image('Architecture.png')
