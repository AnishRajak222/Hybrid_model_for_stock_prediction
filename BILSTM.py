import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping


def BI_LSTM_Prepare(df, sequence_length=6):
    
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Add previous day's close price
    df['Close_prev'] = df['Close'].shift(1)
    df.dropna(inplace=True)

    X = df[['Open', 'High', 'Low', 'Close_prev', 'Volume']].values
    y = df['Close'].values.reshape(-1, 1)

    # Generate sequences
    X_seq, y_seq = [], []
    for i in range(sequence_length, len(X)):
        X_seq.append(X[i-sequence_length:i+1])
        y_seq.append(y[i])

    return np.array(X_seq), np.array(y_seq)


def normalize_data(X, y):
    """
    Normalizes the input and target data using MinMaxScaler.

    Args:
    - X (np.array): Input features.
    - y (np.array): Target values.

    Returns:
    - X_normalized (np.array): Normalized features.
    - y_normalized (np.array): Normalized target values.
    - scaler_x, scaler_y: Scalers for inverse transformation.
    """
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_normalized = scaler_x.fit_transform(X.reshape(-1, X.shape[2])).reshape(X.shape)
    y_normalized = scaler_y.fit_transform(y)

    return X_normalized, y_normalized, scaler_x, scaler_y


def build_model(input_shape):
    """
    Builds and compiles the Bi-LSTM model.

    Args:
    - input_shape (tuple): Shape of the input data.

    Returns:
    - model (tf.keras.Model): Compiled Bi-LSTM model.
    """
    model = Sequential([
        Bidirectional(LSTM(50, return_sequences=True), input_shape=input_shape),
        Dropout(0.2),
        Bidirectional(LSTM(50, return_sequences=False)),
        Dropout(0.2),
        Dense(25, activation="relu"),
        Dense(1)
    ])

    model.compile(optimizer=Adam(learning_rate=0.001), loss="mean_squared_error")
    return model


def train_model(model, X_train, y_train, X_test, y_test, epochs=65, batch_size=10):
    """
    Trains the Bi-LSTM model with early stopping.

    Args:
    - model: Compiled Bi-LSTM model.
    - X_train, y_train: Training data.
    - X_test, y_test: Test data.
    - epochs (int): Number of training epochs.
    - batch_size (int): Batch size.

    Returns:
    - history: Model training history.
    """
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping]
    )

    return history


def predict_and_evaluate(model, X_test, y_test, scaler_y):
    """
    Makes predictions and evaluates the model.

    Args:
    - model: Trained Bi-LSTM model.
    - X_test: Test features.
    - y_test: Test target values.
    - scaler_y: Scaler for inverse transformation.

    Returns:
    - y_pred: Predicted values (inverse transformed).
    - y_test: Actual values (inverse transformed).
    """
    y_pred = model.predict(X_test)
    y_pred = scaler_y.inverse_transform(y_pred)
    y_test = scaler_y.inverse_transform(y_test)

    return float(y_pred[0][0]), float(y_test[0][0])


# ------------------- Main Execution -------------------

def BILSTM_Prediction(historical_data):
    # Parameters

    epochs =  65
    batch_size = 10
    
    
    # prepare data
    X, y = BI_LSTM_Prepare(historical_data )

    # Normalize data
    X, y, scaler_x, scaler_y = normalize_data(X, y)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/len(X), shuffle=False)

    # Build and train the model
    model = build_model((X.shape[1], X.shape[2]))
    train_model(model, X_train, y_train, X_test, y_test, epochs, batch_size)

    # Make predictions
    y_pred, y_test = predict_and_evaluate(model, X_test, y_test, scaler_y)

    # Print predictions
    # print("\nPredicted Prices:")
    # print(y_pred)

    # print("\nActual Prices:")
    # print(y_test)]
    return y_pred


if __name__ == '__main__':
    symbol="WIPRO.NS"
    BILSTM_Prediction(FetchHistoricalData(symbol))
