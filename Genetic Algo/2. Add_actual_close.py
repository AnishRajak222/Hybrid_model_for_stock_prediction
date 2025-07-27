import pandas as pd
import os
import json
from datetime import datetime, timedelta

def update_actual_close_values(verbose=True):
    companies = {
        "HCLTECH.NS": "HCL TECH", "INFY.NS": "INFOSYS", "TCS.NS": "TCS", "WIPRO.NS": "WIPRO", 
        "TECHM.NS": "Tech Mahindra", "LTIM.NS": "LTIMindtree", 
        "PERSISTENT.NS": "Persistent Systems", "OFSS.NS": "Oracle Financial Services", 
        "POLICYBZR.NS": "Policy Bazar", "SASKEN.NS": "Sasken Tech", 
        "QUICKHEAL.NS": "Quick Heal", "BSOFT.NS": "Birlasoft"
    }

    # Paths
    input_file = r"D:\Project\Observations\Observation.xlsx"
    output_file = r"D:\Project\Observations\FinalSheet.xlsx"
    cache_dir = r"D:\Project\Genetic Algo\Cache"
    metadata_file = os.path.join(cache_dir, "metadata.json")

    # Check last update and delete old FinalSheet.xlsx if >30 days old
    if os.path.exists(output_file):
        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                meta = json.load(f)
            last_run = datetime.strptime(meta.get("last_updated", "1970-01-01"), "%Y-%m-%d")
            if datetime.today() - last_run > timedelta(days=30):
                if verbose:
                    print("FinalSheet.xlsx is over a month old. Deleting for fresh generation.")
                os.remove(output_file)
        else:
            os.remove(output_file)

    if verbose:
        print(f"Reading input Excel: {input_file}")
    xls = pd.ExcelFile(input_file)

    # Load sentiment sheet (no modification needed)
    senti_scores = pd.read_excel(xls, sheet_name="Senti Scores")
    senti_scores["Date"] = pd.to_datetime(senti_scores["Date"], errors='coerce', format='mixed', dayfirst=True)

    with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
        senti_scores.to_excel(writer, sheet_name="Senti Scores", index=False)

        for ticker, sheet_name in companies.items():
            if verbose:
                print(f"Processing: {sheet_name} ({ticker})")
            try:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df["Parsed Date"] = pd.to_datetime(df["Date"], errors='coerce', format='mixed', dayfirst=True)
                df = df[df["Parsed Date"].notna()]
                df["Date"] = df["Parsed Date"]
                df.drop(columns=["Parsed Date"], inplace=True)

                cache_file = os.path.join(cache_dir, f"{ticker}_history.csv")
                if not os.path.exists(cache_file):
                    if verbose:
                        print(f"Cache not found for {ticker}")
                    df["Actual Close"] = None
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    continue

                hist = pd.read_csv(cache_file, parse_dates=["Date"], dayfirst=True)
                hist["Date"] = pd.to_datetime(hist["Date"], errors='coerce', format='mixed', dayfirst=True)
                hist = hist[hist["Date"].notna()]
                hist.set_index("Date", inplace=True)
                hist["MapDate"] = hist.index.date
                hist_dict = dict(zip(hist["MapDate"], hist["Close"]))

                df["Actual Close"] = df["Date"].dt.date.map(hist_dict)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            except Exception as e:
                print(f"Error processing {sheet_name}: {e}")

    # Save/update metadata
    with open(metadata_file, "w") as f:
        json.dump({"last_updated": datetime.today().strftime("%Y-%m-%d")}, f)

    if verbose:
        print("\nActual Close values updated successfully.")

if __name__ == "__main__":
    update_actual_close_values()
