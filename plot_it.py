import json
import pandas as pd
import matplotlib.pyplot as plt

# Load anomalies from JSON
with open("anomalies.json") as f:
    anomalies = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(anomalies)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Define threshold lines
LEVEL_1 = 24 * 60    # 1440 minutes
LEVEL_2 = 72 * 60    # 4320 minutes

# Split by breach level
level1 = df[df["breach_level"] == 1]
level2 = df[df["breach_level"] == 2]

# Plot
plt.figure(figsize=(12, 6))
plt.scatter(level1["timestamp"], level1["max_lag_minutes"], color="orange", label="Level 1 Breach (24h)")
plt.scatter(level2["timestamp"], level2["max_lag_minutes"], color="red", label="Level 2 Breach (72h)")

# Add threshold lines
plt.axhline(LEVEL_1, linestyle="--", color="orange", label="Level 1 Threshold (24h)")
plt.axhline(LEVEL_2, linestyle="--", color="red", label="Level 2 Threshold (72h)")

# Labeling
plt.title("SLO Breaches Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Max Lag (minutes)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

