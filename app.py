import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from data.simulator import simulate_traders
from detection.rules import detect_anomalies
from llm.explainer import explain_alert

st.set_page_config(page_title="Rogue Trader Alert System", layout="wide", page_icon="🚨")

st.title("🚨 Rogue Trader Alert System")
st.caption("Real-time surveillance dashboard for detecting anomalous trader behaviour")

# --- CACHING THE DATA TO PREVENT RE-RUN BUGS ---
@st.cache_data
def load_data():
    return simulate_traders()

@st.cache_data
def load_alerts(dataframe):
    return detect_anomalies(dataframe)

# Load data using the cached functions
df, traders = load_data()
all_profiles = load_alerts(df)

# Filter out who is flagged and who is clean
alerts = [p for p in all_profiles if p["risk_score"] > 0]
clean_traders = [p for p in all_profiles if p["risk_score"] == 0]
# -----------------------------------------------

# Sidebar - Controls
st.sidebar.header("Controls")
if st.sidebar.button("🔄 Generate New Traders"):
    st.cache_data.clear() # Empties the vault
    st.rerun() # Forces the app to restart and make new data

st.sidebar.divider()

# Sidebar - Trader Selection
st.sidebar.header("Select Trader")
selected_trader = st.sidebar.selectbox("Trader", df["trader"].unique())

# Top metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Traders Monitored", len(traders))
col2.metric("Traders Flagged", len(alerts))
col3.metric("Clean Traders", len(clean_traders))

st.divider()

# Alert cards
st.subheader("🔴 Active Alerts")
if alerts:
    for alert in alerts:
        color = "red" if alert["risk_score"] >= 70 else "orange"
        with st.expander(f"⚠️ {alert['trader']} — Risk Score: {alert['risk_score']}/100"):
            st.markdown(f"**Risk Score:** :{'red' if alert['risk_score'] >= 70 else 'orange'}[{alert['risk_score']}/100]")
            st.markdown("**Anomalies Detected:**")
            for r in alert["reasons"]:
                st.markdown(f"- {r}")
            
            if st.button(f"Generate AI Risk Report for {alert['trader']}", key=alert["trader"]):
                with st.spinner("Analyzing..."):
                    explanation = explain_alert(alert)
                    st.info(explanation)
else:
    st.success("No alerts detected.")

st.divider()

# Trader deep dive
st.subheader(f"📊 Trader Deep Dive — {selected_trader}")

# Find the specific profile for the selected trader
selected_profile = next(p for p in all_profiles if p["trader"] == selected_trader)

# Display their current score
score_color = "red" if selected_profile["risk_score"] >= 70 else "orange" if selected_profile["risk_score"] > 0 else "green"
st.markdown(f"**Current Risk Score:** :{score_color}[{selected_profile['risk_score']}/100]")

trader_df = df[df["trader"] == selected_trader]

col1, col2 = st.columns(2)

with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=trader_df["day"], y=trader_df["cumulative_pnl"],
        mode="lines", name="Cumulative P&L",
        line=dict(color="green" if trader_df["cumulative_pnl"].iloc[-1] > 0 else "red", width=2)
    ))
    fig1.add_vline(x=50, line_dash="dash", line_color="gray", annotation_text="Surveillance Window")
    fig1.update_layout(title="Cumulative P&L Over Time", xaxis_title="Day", yaxis_title="P&L ($)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=trader_df["day"], y=trader_df["position_size"],
        name="Position Size",
        marker_color=["red" if d > 50 else "steelblue" for d in trader_df["day"]]
    ))
    fig2.add_vline(x=50, line_dash="dash", line_color="gray", annotation_text="Surveillance Window")
    fig2.update_layout(title="Daily Position Size", xaxis_title="Day", yaxis_title="Position Size ($)")
    st.plotly_chart(fig2, use_container_width=True)