import pandas as pd
import numpy as np
import random
import json
from sklearn.metrics import mean_squared_error

# Load Excel file
file_path = r"D:\Project\Observations\FinalSheet.xlsx"
xls = pd.ExcelFile(file_path)
senti_df = xls.parse("Senti Scores")
senti_df["Date"] = pd.to_datetime(senti_df["Date"])

# Columns for sentiment scores
senti_cols = ["VADER Score", "FinBERT Score", "LM Score"]

# GA hyperparameters
POP_SIZE = 30
N_GEN = 50
CROSS_RATE = 0.8
MUTATION_RATE = 0.2

# --- GA Functions ---

def normalize(weights):
    weights = np.array(weights)
    weights = np.clip(weights, 0, None)
    total = weights.sum()
    return (weights / total).tolist() if total != 0 else [1.0 / len(weights)] * len(weights)

def initialize_population(model_cols, senti_cols):
    pop = []
    for _ in range(POP_SIZE):
        model_weights = normalize([random.random() for _ in model_cols])
        senti_weights = normalize([random.random() for _ in senti_cols])
        pop.append((model_weights, senti_weights))
    return pop

def evaluate_individual(weights, model_df, senti_df):
    model_weights, senti_weights = weights
    df = model_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.merge(senti_df, on="Date", how="inner")
    model_preds = sum(w * df[col] for w, col in zip(model_weights, model_cols))
    senti_preds = sum(sw * df[col] for sw, col in zip(senti_weights, senti_cols))
    final_pred = model_preds + (senti_preds * df["Volatility"])
    return np.sqrt(mean_squared_error(df["Actual Close"], final_pred))

def crossover(parent1, parent2):
    def cx(w1, w2):
        if random.random() < CROSS_RATE:
            pt = random.randint(1, len(w1) - 1)
            return normalize(w1[:pt] + w2[pt:])
        return normalize(w1)
    return (cx(parent1[0], parent2[0]), cx(parent1[1], parent2[1]))

def mutate(weights):
    def mutate_one(w):
        if random.random() < MUTATION_RATE:
            idx = random.randint(0, len(w) - 1)
            w[idx] = random.random()
        return normalize(w)
    return (mutate_one(weights[0]), mutate_one(weights[1]))

def genetic_algorithm(model_df, senti_df, model_cols):
    population = initialize_population(model_cols, senti_cols)
    for _ in range(N_GEN):
        scores = [evaluate_individual(ind, model_df, senti_df) for ind in population]
        ranked = sorted(zip(population, scores), key=lambda x: x[1])
        population = [ind for ind, _ in ranked[:POP_SIZE // 2]]
        while len(population) < POP_SIZE:
            p1, p2 = random.sample(population[:10], 2)
            child = mutate(crossover(p1, p2))
            population.append(child)
    return min(population, key=lambda x: evaluate_individual(x, model_df, senti_df))

# --- Main Execution ---

results = {}

for sheet_name in xls.sheet_names:
    if sheet_name == "Senti Scores":
        continue

    try:
        df = xls.parse(sheet_name)
        print(f"{sheet_name} loaded successfully.")
    except Exception as e:
        print(f"ERROR in '{sheet_name}': {e}")
        continue

    df = df.dropna(subset=["Actual Close", "Volatility"])
    model_cols = [col for col in df.columns if "Prediction" in col or "Arima" in col]
    if not model_cols:
        continue

    best_model_wts, best_senti_wts = genetic_algorithm(df, senti_df, model_cols)

    results[sheet_name] = {
        "Model Weights": dict(zip(model_cols, best_model_wts)),
        "Sentiment Weights": dict(zip(senti_cols, best_senti_wts))
    }

# Save results to JSON
output_json_path = r"D:\Project\Observations\ga_weights.json"
with open(output_json_path, "w") as f:
    json.dump(results, f, indent=4)

print("\nGA weights saved to JSON.")
