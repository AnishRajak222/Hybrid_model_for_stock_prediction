import pandas as pd
import json

# Load Excel workbook and JSON weights
excel_path = r"D:\Project\Observations\FinalSheet(BasedonOld).xlsx"
json_path = r"D:\Project\Observations\ga_weights.json"
output_path = "D:\Project\Observations\Update.xlsx"

# Read the Excel file
xls = pd.read_excel(excel_path, sheet_name=None)

# Load weights from JSON
with open(json_path, 'r') as f:
    weights_data = json.load(f)

# Create a dictionary to hold updated sheets
updated_sheets = {}

# Iterate through each sheet
for sheet_name, df in xls.items():
    if sheet_name == "Senti Scores":
        updated_sheets[sheet_name] = df  # Copy as-is
        continue

    try:
        # Get the weights for the current sheet
        model_weights = weights_data[sheet_name]["Model Weights"]

        # Initialize hybrid prediction to 0
        df["Hybrid Model"] = 0

        # Add weighted predictions
        for col, weight in model_weights.items():
            if col in df.columns:
                df["Hybrid Model"] += df[col] * weight
            else:
                print(f"Warning: Column '{col}' not found in sheet '{sheet_name}'.")

        updated_sheets[sheet_name] = df

    except KeyError:
        print(f"Warning: No model weights found for sheet '{sheet_name}'. Skipping.")
        updated_sheets[sheet_name] = df  # Keep original if no weights

# Write to new Excel file
with pd.ExcelWriter(output_path) as writer:
    for sheet, data in updated_sheets.items():
        data.to_excel(writer, sheet_name=sheet, index=False)

print(f"Updated Excel file saved as '{output_path}'.")
