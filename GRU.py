import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler


# Scale Data
def ScaleDataGRU(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler

# Prepare Sequences for Model Training
# def CreateSequences(data, seq_length):
#     X, y = [], []
#     for i in range(len(data) - seq_length):
#         X.append(data[i:i+seq_length])  # Past seq_length days as input
#         y.append(data[i+seq_length, 3])  # Predict Close price
#         X_train, y_train= np.array(X), np.array(y)
#         X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 5)
#         return X_train, y_train


def PredictNextCloseGRU(model, data, scaler, seq_length):
    """
    Predict the next closing price using the trained GRU model.

    Parameters:
    - model: Trained GRU model
    - data: Original stock dataframe (including Close prices)
    - scaler: The MinMaxScaler used for training
    - seq_length: The number of past days used for prediction

    Returns:
    - next_close_price: The predicted closing price (actual value)
    """

    # Extract last `seq_length` rows of ALL 5 features
    last_seq = data.iloc[-seq_length:].values  # Shape: (seq_length, 5)
    scaled_seq = scaler.transform(last_seq).reshape(1, seq_length, 5)  # Reshape for model input
    scaled_prediction = model.predict(scaled_seq)
    next_close_price = scaler.inverse_transform([[0, 0, 0, scaled_prediction[0, 0], 0]])[0, 3]

    return next_close_price





def CreateSequences(data, seq_length, split_ratio=0.8):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])  # Past seq_length days as input
        y.append(data[i+seq_length, 3])  # Predict Closeprice
    X, y = np.array(X), np.array(y)
    # Train-Test Split
    split_index = int(len(X) * split_ratio)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    return X_train, X_test, y_train, y_test

def GRU_Prediction(raw_data):
    scaled_data, scaler = ScaleDataGRU(raw_data)
    seq_length = 10 #How many days data to take into account for Prediction ?
    X_train, X_test, y_train, y_test = CreateSequences(scaled_data, seq_length)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 5)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 5)
    gru_model = Sequential([
        GRU(50, activation='tanh', return_sequences=True, input_shape=(seq_length, 5)), 
        GRU(50, activation='tanh'),
        Dense(1)  # Predict CLosing price
    ])
    # Compile the model
    gru_model.compile(optimizer='adam', loss='mse')
    # Train the model
    gru_model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))
    return PredictNextCloseGRU(gru_model,raw_data,scaler,seq_length)

