from sklearn.metrics import *
from sklearn.linear_model import LinearRegression
from PreProcess import * 



def LR_Train(historical_data):
    print("LR_training...")

    X,Y=DataPrepare_LR(historical_data)
    x_train_transformed = scaler_x.fit_transform(X)
    y_train_transformed = scaler_y.fit_transform(Y)
    # Training the Linear Regression model
    lr = LinearRegression()
    lr.fit(x_train_transformed, y_train_transformed)
    # print("Predicted Close Price by LR:", predicted_close)
    # print("LR Trained!!")
    return lr

def LR_prediction(historical_data,input_data):
    lr=LR_Train(historical_data)
    # print("Input data at LR:", input_data)
    scaled_prediction = lr.predict( scaler_x.transform(input_data))
    predicted_close = scaler_y.inverse_transform(scaled_prediction)
    return predicted_close[0,0]





















