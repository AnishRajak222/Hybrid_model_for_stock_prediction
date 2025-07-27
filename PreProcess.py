import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler




def FetchHistoricalData(symbol):  # Ex: WIPRO.NS
    start_date=today = datetime.today().strftime('%Y-%m-%d')

    #Calculate date 5 years ago from today
    end_date=five_years_ago = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    #Fetch stock data from 5 years ago to today
    stock_data = yf.download(symbol, start=five_years_ago, end=today)
    return stock_data 



# Extract the latest data tuple (Open, High, Low)
def Fetch_Current_data(symbol):
    stock_data = yf.download(symbol, period='1d', interval='1m')
    # print(stock_data.head())
    return stock_data[['Open', 'High', 'Low','Volume']].iloc[-2].values.reshape(1, -1)



def DataPrepare_LR(stock_data): # Prepare Data for Linear regression
    X = pd.DataFrame()
    X[['Open', 'High', 'Low','Volume']] = stock_data[['Open', 'High', 'Low','Volume']]

    Y = pd.DataFrame()
    Y['Close'] = stock_data['Close']
    return X,Y




# Give data as stock_data['Close'] while calling
def DataPrepare_LSTM(data, time_step=60):      # Prepare Data for LSTM
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)



def Scaling_X_Y():
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    return scaler_x, scaler_y




# Calculate variation and ensure it's a float
def Volatility(symbol):
    """
    Calculate the max variation (high - low) over the past 1 month
    stock_data: DataFrame containing at least 'High' and 'Low' columns
    """
    recent_data = yf.download(symbol, period='5d', interval='1m')
    # print(recent_data)
    max_high = recent_data['High'].max()
    min_low = recent_data['Low'].min()
    # print("\n")
    # print(max_high)
    # print("\n")
    # print(min_low)
    volatility = max_high - min_low
    
    return float(volatility)



# variation = Volatility(symbol)
scaler_x, scaler_y=Scaling_X_Y()
scaler_for_LSTM = MinMaxScaler(feature_range=(0, 1))

if __name__ == '__main__':
    pass
    print(Fetch_Current_data("TCS.NS"))
    # print(Fetch_Current_data("HCLTECH.NS"))
    # print(Fetch_Current_data("WIPRO.NS"))
    # print(Fetch_Current_data("INFY.NS"))

    # print(FetchHistoricalData("TCS.NS"))
    # print(FetchHistoricalData("HCLTECH.NS"))
    # print(FetchHistoricalData("WIPRO.NS"))
    # print(FetchHistoricalData("INFY.NS"))

    # Volatility("TCS.NS")
    # Volatility("INFY.NS")
    # Volatility("HCLTECH.NS")
    # Volatility("WIPRO.NS") 

