# 📊 Streamlit Dashboard for Solar Irradiance Forecasting
# ----------------------------------------------
# This dashboard shows 72-hour GHI forecast and irrigation alerts
# Designed for mobile view, bilingual Marathi-English support

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---- Load Forecast Data ----
@st.cache_data
def load_data():
    df = pd.read_csv("72h_forecast_results.csv")  # CSV from forecasting output
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Ensure 'irrigation_alert' column exists or create it based on threshold
    if 'irrigation_alert' not in df.columns:
        df['irrigation_alert'] = df['forecasted_ghi'].apply(lambda x: 1 if x >= 500 else 0)
    return df

forecast_df = load_data()

# ---- Title and Sidebar ----
st.set_page_config(layout="centered")
st.title("🌞 Smart Irrigation Dashboard – Aurangabad")
st.markdown("""
This dashboard displays the 72-hour **solar irradiance forecast** based on atmospheric data. 
Pump alerts are generated based on GHI thresholds (500 W/m²).
""")

# ---- Forecast Plot ----
st.subheader("🔮 Forecasted GHI (W/m²)")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(forecast_df['timestamp'], forecast_df['forecasted_ghi'], label='Forecasted GHI')
ax.axhline(500, color='red', linestyle='--', label='Pump Threshold')
ax.set_ylabel("GHI (W/m²)")
ax.set_xlabel("Time")
ax.legend()
ax.set_title("72-Hour GHI Forecast")
plt.xticks(rotation=45)
st.pyplot(fig)

# ---- Irrigation Alerts Table ----
st.subheader("🚜 Irrigation Alerts")
alert_df = forecast_df.copy()
alert_df['Alert'] = alert_df['irrigation_alert'].map({1: '✅ Start Pumping', 0: '❌ Do Not Pump'})
st.dataframe(alert_df[['timestamp', 'forecasted_ghi', 'Alert']].rename(columns={
    'timestamp': 'Time', 'forecasted_ghi': 'Predicted GHI', 'Alert': 'Pump Decision'
}))

# ---- Voice Alert in Marathi (Simulated) ----
st.subheader("🔊 Marathi Voice Advisory (Simulated)")
next_alert = alert_df.iloc[0]['irrigation_alert']
if next_alert == 1:
    st.success("🚜 सूचना: पुढील १५ मिनिटांत सिंचन सुरू करा")
else:
    st.warning("⏳ सूचना: सौर ऊर्जा अपुरी, साठवणूक वापरा")

# ---- Download Option ----
st.download_button("📥 Download Forecast CSV", data=forecast_df.to_csv(index=False), file_name="forecast_72h.csv")

# ---- Footer ----
st.markdown("""
---
🔧 Developed by Suraj Shah · Powered by SARIMA GHI Forecasting · Streamlit Deployment
""")
