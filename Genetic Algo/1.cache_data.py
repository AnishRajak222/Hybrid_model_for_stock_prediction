import os
import yfinance as yf
from datetime import datetime, timedelta
import time
import json

# Setup
cache_dir = r"D:\Project\Genetic Algo\Cache"
os.makedirs(cache_dir, exist_ok=True)
log_file = os.path.join(cache_dir, "cache_log.json")

# Tickers
companies = {
    "HCLTECH.NS": "HCL TECH", "INFY.NS": "INFOSYS", "TCS.NS": "TCS", "WIPRO.NS": "WIPRO",
    "TECHM.NS": "Tech Mahindra", "LTIM.NS": "LTIMindtree", "PERSISTENT.NS": "Persistent Systems",
    "OFSS.NS": "Oracle Financial Services", "POLICYBZR.NS": "Policy Bazar",
    "SASKEN.NS": "Sasken Tech", "QUICKHEAL.NS": "Quick Heal", "BSOFT.NS": "Birlasoft"
}

# Load or initialize cache log
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        cache_log = json.load(f)
else:
    cache_log = {}

last_updated_str = cache_log.get("last_updated")
refresh_needed = True

# Check if last run was more than 30 days ago
if last_updated_str:
    try:
        last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d")
        if datetime.today() - last_updated < timedelta(days=30):
            refresh_needed = False
            print("Cache is still fresh (within 30 days). Skipping download.\n")
        else:
            print("Cache is older than 30 days. Refreshing...\n")
    except Exception as e:
        print(f"Failed to parse last updated date: {e}")
else:
    print("No previous cache log found. Proceeding with download.\n")

# If cache is old, delete all files
if refresh_needed:
    for file in os.listdir(cache_dir):
        if file.endswith(".csv"):
            os.remove(os.path.join(cache_dir, file))
    print("Old cache deleted.\n")

# Download data if needed
if refresh_needed:
    for ticker in companies:
        print(f"Downloading: {ticker}")
        cache_file = os.path.join(cache_dir, f"{ticker}_history.csv")

        try:
            data = yf.download(
                ticker,
                start=(datetime.today().replace(year=datetime.today().year - 5)).strftime('%Y-%m-%d'),
                end=datetime.today().strftime('%Y-%m-%d')
            )

            if data.empty:
                print(f"No data for {ticker}. Possibly rate-limited.")
                continue

            data = data[["Close"]]
            data.reset_index(inplace=True)
            data.to_csv(cache_file, index=False)
            print(f"Cached to {cache_file}")
            time.sleep(2)

        except Exception as e:
            print(f"Error downloading {ticker}: {e}")

    # Save update timestamp
    cache_log["last_updated"] = datetime.today().strftime("%Y-%m-%d")
    with open(log_file, "w") as f:
        json.dump(cache_log, f)

    print("\nCaching completed and log updated.")
else:
    print("Using existing cached data.")
