# grafana-anomaly-detector
LLM-Powered SLO Anomaly Detector


This repo contains a lightweight pipeline that detects and visualizes SLO breaches in time-series lag metrics using a hybrid approach:

- 📊 **Local metrics analysis** via pandas/Numpy (e.g., max lag, breach levels)
- 🧠 **LLM-assisted anomaly classification** via **Mistral** or **LLaMA** (e.g., contextual severity, deduplication, filtering)

It’s designed to flag large-scale ingestion or replication lag spikes across distributed systems, tag them with breach levels (e.g., >24h or >72h), and augment or filter them via local LLMs before publishing.

## Contents

- `lag_anomaly_check13.py`: Parses CSV lag data, assigns breach levels, queries a local Mistral/LLaMA server for anomaly scoring, and outputs structured results to `anomalies.json`.
- `plot_it.py`: Simple matplotlib visualization of all breach-level anomalies.
- `requirements.txt`: Optional, for local setup.

## Requirements

- Python 3.9+
- A locally running LLaMA or Mistral instance with a compatible API (e.g., `http://localhost:11434` for Ollama or `vLLM`).
- Input CSV with time-indexed lag data.

## Coming Soon

- Integration with  dashboards
- Grafana export and time bucket overlays
- Root-cause LLM summaries of upstream system behavior
