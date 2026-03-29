# 🚨 Rogue Trader Alert System

A real-time trader surveillance dashboard that monitors trading behaviour, detects anomalous patterns using rule-based logic, and generates AI-powered risk reports — inspired by the Nick Leeson scandal that bankrupted Barings Bank in 1995.

---

## 🧠 Motivation

In 1995, a single rogue trader named Nick Leeson concealed $1.3 billion in losses and single-handedly collapsed one of Britain's oldest banks. The warning signs were there — unusually large positions, consecutive loss days, hidden losses spread across accounts — but no system caught them in time.

This project builds the system that could have.

---

## 🔍 What It Does

- Monitors daily P&L and position sizes across multiple traders
- Flags anomalous behaviour using 4 surveillance rules:
  - **Position size spike** — trader takes positions far beyond their historical average
  - **Consecutive loss days** — sustained losses over the surveillance window
  - **Hidden loss detection** — losses being concealed across accounts
  - **Strategy reversal** — profitable trader suddenly becomes loss-making
- Assigns a **risk score (0–100)** to each flagged trader
- Generates a **plain-English AI risk report** using an LLM, explaining what was detected and recommending action
- Visualises cumulative P&L and daily position sizes with clear surveillance window markers

---

## 📸 Dashboard Preview

![Dashboard](screenshots/dashboard.png)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Data Processing | Pandas, NumPy |
| Simulation | Faker |
| Anomaly Detection | Rule-based engine (custom) |
| LLM Integration | Groq API (LLaMA 3.3 70B) |
| Dashboard | Streamlit |
| Visualisation | Plotly |

---

## 📁 Project Structure

```
rogue-trader-alert/
├── data/
│   └── simulator.py        # Simulates 60 days of trader P&L data
├── detection/
│   └── rules.py            # Anomaly detection rule engine
├── llm/
│   └── explainer.py        # LLM-powered risk report generation
├── app.py                  # Streamlit dashboard
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/rogue-trader-alert.git
cd rogue-trader-alert
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Groq API key
Get a free API key at [console.groq.com](https://console.groq.com) and paste it in `llm/explainer.py`:
```python
client = Groq(api_key="your_groq_api_key_here")
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

---

## 📋 Requirements

```
streamlit
pandas
numpy
plotly
faker
groq
```

---

## 💡 How the Risk Score Works

| Score | Level | Meaning |
|---|---|---|
| 70–100 | 🔴 High Risk | Immediate review required |
| 30–69 | 🟠 Medium Risk | Monitor closely |
| 0–29 | 🟢 Low Risk | Normal behaviour |

Each triggered rule contributes to the score:
- Position size spike (>3x average): +40 points
- 5+ consecutive loss days: +30 points
- Hidden losses detected: +30 points
- Strategy reversal: +20 points

---

## ⚠️ Disclaimer

This project uses entirely simulated data for demonstration purposes. It is not intended for use with real trading data and does not constitute financial or legal advice.
