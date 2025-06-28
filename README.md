# grafana-anomaly-detector
LLM-Powered SLO Anomaly Detector
This repo implements a hybrid anomaly detection pipeline for time-series lag data using both statistical thresholds and LLM-based contextual classification (via Mistral, LLaMA, or similar local models).

Built for observability and platform engineering teams, it helps identify and explain ingestion or processing delays in telemetry pipelines with meaningful, ML-informed labels.

Features

🧹 Parses human-readable time formats (e.g., 2.4h, 3d, 45m) from CSV exports

🔍 Detects anomalies based on configurable lag thresholds (e.g., 24h, 72h SLOs)

🤖 ML classification with LLMs:

Prompts Mistral/LLaMA models with lag context, table name, and history

Outputs semantic anomaly descriptions or labels (e.g., "critical data loss", "pipeline backfill")

📈 Visualizes lag breaches over time

💾 Exports structured JSON reports for dashboards or alerting

Example Use Case

Export pipeline delay data from Snowflake, Graphite, or Prometheus

Run lag_anomaly_check13.py to detect breach events

Classify breaches with your local LLM (optional integration stub)

Use plot_it.py to visualize timeline with threshold lines

Publish structured anomaly logs to your internal dashboard or Grafana annotation layer

Output Format (anomalies.json)

[
  {
    "timestamp": "2025-06-01T23:00:00",
    "max_lag_minutes": 75297.6,
    "source": "n6-primary-...",
    "breach_level": 2,
    "llm_classification": "historical ETL gaps - likely backfill outage"
  },
  ...
]

Setup

pip install -r requirements.txt

You will also need:

Python 3.9+

matplotlib, pandas, openai, or your local LLM client (e.g., ollama, llama-cpp)

Credits

Designed by a weary TME who got tired of squinting at wall-to-wall time series and decided to fight back with a language model.

MIT License. Pull requests welcome.
