import os
from datetime import datetime, timedelta
from keras.models import load_model
from LR import *
from LSTM import *
from SentimentAnalysis import *
from BILSTM import *
import json
from GRU import *
from Arima import * 
# Define path for cache file
CACHE_FILE = 'predicted_prices_cache.json'
Excelfile=r"D:\Project\Observations\Observation.xlsx"

# Load cache from file or return an empty dictionary if the file doesn't exist
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save cache to the file
def save_cache(cache):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)

# Check if the cached price for a stock symbol needs updating (older than 1 day)
def cache_needs_updating(cache_key):
    cache = load_cache()
    if cache_key in cache:
        # Parse the date the price was cached
        cache_date = datetime.strptime(cache[cache_key]["date"], "%Y-%m-%d")
        # Return True if more than a day has passed since the cache date
        return datetime.now() - cache_date > timedelta(days=1)
    return True  # If not cached, we need to update

# Main function for LSTM prediction with caching and daily update checks
def LSTM_Cached(symbol, historical_data, time_step=60):
    # Load the current cache
    cache = load_cache()
    
    # Define cache key based on stock symbol
    cache_key = f"{symbol}"
    
    # Check if we have a valid, up-to-date prediction in the cache
    if cache_key in cache and not cache_needs_updating(cache_key):
        print("Returning cached prediction for:", symbol)
        return cache[cache_key]["predicted_price"]
    
    # Train the model and make a new prediction if cache is outdated or missing
    lstm_model = LSTM_train(historical_data, time_step)
    predicted_price = LSTM_prediction(lstm_model, historical_data, time_step)
    predicted_price = float(predicted_price)
    # Cache the new prediction with today's date
    cache[cache_key] = {
        "predicted_price": predicted_price,
        "date": str(datetime.now().date())
    }
    save_cache(cache)
    print("New prediction generated and cached for:", symbol)
    return predicted_price
def CompanyName(symbol):
    inverse_stock_symbols = {
    "HCLTECH.NS": "HCL TECH",
    "INFY.NS": "INFOSYS",
    "TCS.NS": "TCS",
    "WIPRO.NS": "WIPRO",
    "TECHM.NS": "Tech Mahindra",
    "LTIM.NS": "LTIMindtree",
    "PERSISTENT.NS": "Persistent Systems",
    "OFSS.NS": "Oracle Financial Services",
    "POLICYBZR.NS": "Policy Bazar",
    "HEXT.NS": "Hexaware",
    "SASKEN.NS": "Sasken Tech",
    "QUICKHEAL.NS": "Quick Heal",
    "BSOFT.NS": "Birlasoft"}
    return inverse_stock_symbols[symbol]

def save_stock_prediction(symbol, lstm_prediction, lr_prediction,gru_prediction, BiLSTM_prediction,Arima_prediction,variation, file_path=Excelfile):
    """Save stock prediction values to an Excel file with a unique sheet per symbol."""
    today = datetime.now().strftime("%Y-%m-%d")
    sheet_name = CompanyName(symbol)  # Unique sheet name based on stock symbol
    
    # Check if the file exists
    if os.path.exists(file_path):
        wb = load_workbook(file_path)
        if sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
        else:
            ws = wb.create_sheet(sheet_name)
            ws.append(["Date", "LSTM Prediction", "LR Prediction", "GRU Prediction","BiLSTM_Prediction","Arima_prediction","Volatility"])  # Headers if new
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name
        ws.append(["Date", "LSTM Prediction", "LR Prediction", "GRU Prediction","BiLSTM_Prediction","Arima_prediction", "Volatility"])  # Headers if new
    
    # Check if today's date already exists in the sheet
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == today:
            print(f"Stock prediction entry for {symbol} on {today} already exists. Skipping.")
            wb.save(file_path)
            return
    ws.append([today, lstm_prediction, lr_prediction, gru_prediction,BiLSTM_prediction,Arima_prediction,variation])
    wb.save(file_path)
    print(f"Stock prediction saved to '{sheet_name}' in {file_path}")


def ModelWeight(stock_code):
    file_path = r"D:\Project\Observations\ga_weights.json"
    stock_name=CompanyName(stock_code)
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

            if stock_name in data:
                model = data[stock_name].get("Model Weights", {})
                sentiment = data[stock_name].get("Sentiment Weights", {})

                # Extract and return each value in order
                lstm = model.get("LSTM Prediction", 0.0)
                lr = model.get("LR Prediction", 0.0)
                gru = model.get("GRU Prediction", 0.0)
                bilstm = model.get("BiLSTM Prediction", 0.0)
                arima = model.get("Arima Prediction", 0.0)

                # vader = sentiment.get("VADER Score", 0.0)
                # finbert = sentiment.get("FinBERT Score", 0.0)
                # lm = sentiment.get("LM Score", 0.0)

                return lstm, lr, gru, bilstm, arima
            else:
                raise ValueError(f"Stock '{stock_name}' not found.")
    
    except FileNotFoundError:
        raise FileNotFoundError("Weights file not found.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON file.")




def Predict_StockPrice(symbol):
    historical_data=FetchHistoricalData(symbol)
    input_data=Fetch_Current_data(symbol)

    print("values:","\n"*5)
    print(input_data)
    LSTM_prediction=LSTM_Cached(symbol,historical_data['Close'],time_step=10)
    # print("LSTM_prediction: ",LSTM_prediction)

    LR_predict=LR_prediction(historical_data,input_data)
    # print("LR_prediction: ",LR_predict)

    GRU_predict=GRU_Prediction(historical_data)
    # print("GRU_prediction: ",GRU_predict)

    BiLSTM_predict=BILSTM_Prediction(historical_data)
    # print("BiLSTM_prediction: ",BiLSTM_predict)

    Arima_predict=Arima_Prediction(historical_data)
    Variation=Volatility(symbol)
    # print("Variation: ",Variation)
    Senti=SentimentScore(symbol)

    save_stock_prediction(symbol, LSTM_prediction, LR_predict,GRU_predict,BiLSTM_predict,Arima_predict, Variation)
    

    lstm, lr, gru, bilstm, arima=ModelWeight(symbol)
    Fundamental_prediction= (  (lstm*LSTM_prediction)+(lr*LR_predict)+(GRU_predict*gru)+(BiLSTM_predict*bilstm) + (arima*Arima_predict) )

    final_pred=Fundamental_prediction + (Senti*Variation)
    # print(f" {CompanyName(symbol)}'s can Close at: ",final_pred)
    return final_pred 

if __name__=="__main__":
    Predict_StockPrice("WIPRO.NS")


