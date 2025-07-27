                #add the path of xlsx file of the stock
file_path = r"D:\Processed Output\Processed_data_INFOSYS.xlsx"
stock="INFOSYS"
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Load data
data = pd.read_excel(file_path)

# Extract actual prices, LR predictions, and LSTM predictions
actual_price = data["Actual_Close"]
lr_pred = data["LR_Pred"]
lstm_pred = data["LSTM_Pred"]

# Function to calculate metrics with multiple tolerance levels
def calculate_metrics(actual, predicted):
    metrics = {
        "R² Score": r2_score(actual, predicted),
        "MSE": mean_squared_error(actual, predicted),
        "RMSE": np.sqrt(mean_squared_error(actual, predicted)),
        "MAE": mean_absolute_error(actual, predicted),
        "Tolerance Error (±1.0%)": np.mean(np.abs(predicted - actual) / actual <= 0.01) * 100,
        "Tolerance Error (±1.5%)": np.mean(np.abs(predicted - actual) / actual <= 0.015) * 100,
        "Tolerance Error (±2.0%)": np.mean(np.abs(predicted - actual) / actual <= 0.02) * 100,
    }
    return metrics

# Calculate metrics for LR and LSTM models
lr_metrics = calculate_metrics(actual_price, lr_pred)
lstm_metrics = calculate_metrics(actual_price, lstm_pred)

# Print metrics for comparison
print("Performance Metrics Comparison:")
print("\nLinear Regression (LR):")
for key, value in lr_metrics.items():
    print(f"{key}: {value:.4f}")

print("\nLong Short-Term Memory (LSTM):")
for key, value in lstm_metrics.items():
    print(f"{key}: {value:.4f}")

# Prepare data for visualization
comparison_data = pd.DataFrame({
    "Date": data["Date"],
    "Actual Price": actual_price,
    "LR Prediction": lr_pred,
    "LSTM Prediction": lstm_pred
})

# Plot Actual vs Predicted Prices for LR and LSTM
fig = px.line(
    comparison_data,
    x="Date",
    y=["Actual Price", "LR Prediction", "LSTM Prediction"],
    labels={'value': 'Price', 'Date': 'Time'},
    title=f'Actual vs Predicted Prices: LR vs LSTM  ({stock})'
)

# Customize layout
fig.update_layout(
    legend_title_text='Models',
    xaxis_title='Time',
    yaxis_title='Price (in ₹)',
    hovermode='x unified'
)

# Show interactive plot
fig.show()
