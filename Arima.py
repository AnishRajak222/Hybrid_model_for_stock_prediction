#pip install numpy==1.23.5 scipy==1.9.3 pmdarima==2.0.3
from pmdarima import auto_arima


def Prepare_Arima(hist_data):
    hist_data = hist_data[:-1]  # Exclude today's data
    if hist_data.empty:
        raise ValueError("No data found for the given stock symbol and date range.")
    return hist_data[['Close']]


def train_arima_model(close_prices):
    """Finds optimal ARIMA parameters and fits the model."""
    optimal_model = auto_arima(
        close_prices,
        seasonal=False,
        stepwise=True,
        suppress_warnings=True,
        test='adf',
        max_p=7,
        max_q=7,
        d=None,
        max_d=2,
        start_p=0,
        start_q=0,
        information_criterion='aic',
        trace=True
    )

    p, d, q = optimal_model.order
    print(f"Optimal ARIMA parameters: p={p}, d={d}, q={q}")

    # Fit the final ARIMA model with optimal parameters
    model = auto_arima(
        close_prices,
        order=(p, d, q),
        seasonal=False,
        stepwise=True,
        suppress_warnings=True
    )

    return model, (p, d, q)


def predict_future(model, num_days: int):
    """Predicts future stock prices for the specified number of days."""
    #future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, num_days + 1)]
    forecast = model.predict(n_periods=num_days)

    return float(forecast)







def Arima_Prediction(Historical_data):


    # prepare stock data
    close_prices= Prepare_Arima(Historical_data)
    # Train ARIMA model
    model, params = train_arima_model(close_prices)
    num_days=1 #Kitne din ka prediction chahiye ?
    # Predict future prices
    forecast = predict_future(model, num_days)

    # print("\n--- Prediction Results ---")
    # print(f"Forecasted prices: {forecast}")
    return forecast


# if __name__ == '__main__':
#     # Example usage
# # import yfinance as yf
# # import pandas as pd
# # import numpy as np
# # from datetime import datetime, timedelta


# # def FetchHistoricalData(symbol):  # Ex: WIPRO.NS
# #     start_date=today = datetime.today().strftime('%Y-%m-%d')

# #     #Calculate date 5 years ago from today
# #     end_date=five_years_ago = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
# #     #Fetch stock data from 5 years ago to today
# #     stock_data = yf.download(symbol, start=five_years_ago, end=today)
# #     return stock_data 
    # Arima_Prediction(FetchHistoricalData("WIPRO.NS"))
    
