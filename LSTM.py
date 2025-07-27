import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import numpy as np
from PreProcess import *


def LSTM_train(historical_data,time_step = 60):
    print("LSTM_training...")
    scaled_data = scaler_for_LSTM.fit_transform(np.array(historical_data).reshape(-1, 1))
    X_train, y_train = DataPrepare_LSTM(scaled_data, time_step)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=60, batch_size=24, verbose=1)
    print("LSTM_training Completed!!\n")
    return model

                                            #scaler_for_LSTM  variable in PreProcess
def LSTM_prediction(model, historical_data, time_step=60):
    scaler=scaler_for_LSTM
    scaled_data = scaler.fit_transform(np.array(historical_data).reshape(-1, 1))
    last_data = scaled_data[-time_step:]
    last_data = last_data.reshape(1, time_step, 1)  # Reshape to match model input shape
    # Predict tomorrow's price
    predicted_price_scaled = model.predict(last_data)
    # Inverse transform to get the actual price
    predicted_price = scaler.inverse_transform(predicted_price_scaled)

    return predicted_price[0, 0]



if __name__ =="__main__":
    data=FetchHistoricalData("WIPRO.NS")['Adj Close']
    m=LSTM_train(data)
    print(LSTM_prediction(m,data,60))

