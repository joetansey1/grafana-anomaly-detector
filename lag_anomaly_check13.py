import pandas as pd
import json
import re
import numpy as np

# === CONFIG ===
csv_file = "MfrOsSuite4.csv"
chunk_size = 48  # e.g., 4h @ 5min intervals
anomaly_threshold_multiplier = 1.25

# === PARSE LAG UTILITY ===
def parse_lag(value):
    try:
        if pd.isna(value):
            return 0.0
        value = str(value).strip().lower()
        value = value.replace(",", "")
        value = re.sub(r"(?<=\d)(?=[a-zA-Z])", " ", value)

        match = re.match(r"([\d\.]+)\s*(\w+)", value)
        if not match:
            return 0.0
        num, unit = match.groups()
        num = float(num)

        if "min" in unit:
            return num
        elif "hour" in unit or unit.startswith("h"):
            return num * 60
        elif "day" in unit or unit.startswith("d"):
            return num * 60 * 24
        elif "week" in unit or unit.startswith("w"):
            return num * 60 * 24 * 7
        elif unit == "s" or "sec" in unit:
            return num / 60
        else:
            return num
    except:
        return 0.0

# === LOAD & CLEAN ===
df = pd.read_csv(csv_file, skiprows=1)
df.columns = [c.strip() for c in df.columns]
time_col = df.columns[0]
# Identify time column without accidentally dropping "Time"
time_col = df.columns[0]
if time_col != "Time":
    df["Time"] = pd.to_datetime(df[time_col], errors="coerce")
    df = df.drop(columns=[time_col])
else:
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

print(f"🧠 Loaded {len(df)} rows. Parsing lag values...")

# Parse lag values
lag_df = df.drop(columns=["Time"]).applymap(parse_lag)
lag_df["Time"] = df["Time"]

# === GLOBAL THRESHOLD CALC ===
all_maxes = lag_df.drop(columns=["Time"]).max(axis=1)
global_p95 = all_maxes.quantile(0.95)
threshold = global_p95 * anomaly_threshold_multiplier

# === DETECTION ===
all_anomalies = []

# Define breach level thresholds
LEVEL_1_THRESHOLD = 24 * 60    # 1440 minutes
LEVEL_2_THRESHOLD = 72 * 60    # 4320 minutes

for start in range(0, len(lag_df), chunk_size):
    chunk = lag_df.iloc[start:start + chunk_size].copy()
    if chunk.empty:
        continue

    metrics = chunk.drop(columns=["Time"])
    chunk["max_lag"] = metrics.max(axis=1)
    chunk["max_lag_column"] = metrics.idxmax(axis=1)

    # Identify anomalies
    for _, row in chunk.iterrows():
        lag = float(row["max_lag"])

    # Always evaluate breach level
    if lag > LEVEL_2_THRESHOLD:
        breach_level = 2
    elif lag > LEVEL_1_THRESHOLD:
        breach_level = 1
    else:
        breach_level = 0

    if breach_level > 0:
        all_anomalies.append({
            "timestamp": row["Time"].isoformat(),
            "max_lag_minutes": lag,
            "source": row["max_lag_column"],
            "breach_level": breach_level
        })

# === OUTPUT ===

print(f"\n📈 Top 20 lag values (minutes):")
lag_values = lag_df.drop(columns=["Time"])
top_lags = lag_values.max(axis=1).sort_values(ascending=False).head(20)
print(top_lags)

# Filter only SLO-breaching anomalies
breach_anomalies = [a for a in all_anomalies if a["breach_level"] > 0]

if breach_anomalies:
    with open("anomalies.json", "w") as f:
        json.dump(breach_anomalies, f, indent=2)

    print(f"\n🚨 Top breach-level anomalies:")
    for a in sorted(breach_anomalies, key=lambda x: x["max_lag_minutes"], reverse=True)[:5]:
        print(a)

    print(f"\n✅ Total SLO breaches found: {len(breach_anomalies)}. Saved to anomalies.json")
else:
    print(f"\n✅ No SLO breaches found.")

