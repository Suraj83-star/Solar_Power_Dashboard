{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "2b83a829-ba09-4d62-a7dc-b453f0007f8f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 📊 Streamlit Dashboard for Solar Irradiance Forecasting\n",
    "# ----------------------------------------------\n",
    "# This dashboard shows 72-hour GHI forecast and irrigation alerts\n",
    "# Designed for mobile view, bilingual Marathi-English support\n",
    "\n",
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from datetime import datetime"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "a615fe85-9223-4479-af67-09dc11970c04",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-04-13 22:17:42.692 No runtime found, using MemoryCacheStorageManager\n",
      "2025-04-13 22:17:42.695 No runtime found, using MemoryCacheStorageManager\n"
     ]
    }
   ],
   "source": [
    "# ---- Load Forecast Data ----\n",
    "@st.cache_data\n",
    "def load_data():\n",
    "    df = pd.read_csv(\"72h_forecast_results.csv\")  # CSV from forecasting output\n",
    "    df['timestamp'] = pd.to_datetime(df['timestamp'])\n",
    "\n",
    "    # Ensure 'irrigation_alert' column exists or create it based on threshold\n",
    "    if 'irrigation_alert' not in df.columns:\n",
    "        df['irrigation_alert'] = df['forecasted_ghi'].apply(lambda x: 1 if x >= 500 else 0)\n",
    "    return df\n",
    "\n",
    "forecast_df = load_data()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "d282a86d-d2d6-4b05-b8fb-6213bb12b675",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# ---- Title and Sidebar ----\n",
    "st.set_page_config(layout=\"centered\")\n",
    "st.title(\"🌞 Smart Irrigation Dashboard – Aurangabad\")\n",
    "st.markdown(\"\"\"\n",
    "This dashboard displays the 72-hour **solar irradiance forecast** based on atmospheric data. \n",
    "Pump alerts are generated based on GHI thresholds (500 W/m²).\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "d2fa8082-80e2-45e3-8a9b-479305883fd9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# ---- Forecast Plot ----\n",
    "st.subheader(\"🔮 Forecasted GHI (W/m²)\")\n",
    "fig, ax = plt.subplots(figsize=(12, 4))\n",
    "ax.plot(forecast_df['timestamp'], forecast_df['forecasted_ghi'], label='Forecasted GHI')\n",
    "ax.axhline(500, color='red', linestyle='--', label='Pump Threshold')\n",
    "ax.set_ylabel(\"GHI (W/m²)\")\n",
    "ax.set_xlabel(\"Time\")\n",
    "ax.legend()\n",
    "ax.set_title(\"72-Hour GHI Forecast\")\n",
    "plt.xticks(rotation=45)\n",
    "st.pyplot(fig)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "a71c1796-3d81-46f3-ab49-ba0f8235603d",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# ---- Irrigation Alerts Table ----\n",
    "st.subheader(\"🚜 Irrigation Alerts\")\n",
    "alert_df = forecast_df.copy()\n",
    "alert_df['Alert'] = alert_df['irrigation_alert'].map({1: '✅ Start Pumping', 0: '❌ Do Not Pump'})\n",
    "st.dataframe(alert_df[['timestamp', 'forecasted_ghi', 'Alert']].rename(columns={\n",
    "    'timestamp': 'Time', 'forecasted_ghi': 'Predicted GHI', 'Alert': 'Pump Decision'\n",
    "}))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "6c9e610b-b7b3-4f64-a76c-df2b61c957f7",
   "metadata": {},
   "outputs": [],
   "source": [
    "# ---- Voice Alert in Marathi (Simulated) ----\n",
    "st.subheader(\"🔊 Marathi Voice Advisory (Simulated)\")\n",
    "next_alert = alert_df.iloc[0]['irrigation_alert']\n",
    "if next_alert == 1:\n",
    "    st.success(\"🚜 सूचना: पुढील १५ मिनिटांत सिंचन सुरू करा\")\n",
    "else:\n",
    "    st.warning(\"⏳ सूचना: सौर ऊर्जा अपुरी, साठवणूक वापरा\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "925a4df4-bbd0-4c43-9133-48e31d3379a1",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# ---- Download Option ----\n",
    "st.download_button(\"📥 Download Forecast CSV\", data=forecast_df.to_csv(index=False), file_name=\"forecast_72h.csv\")\n",
    "\n",
    "# ---- Footer ----\n",
    "st.markdown(\"\"\"\n",
    "---\n",
    "🔧 Developed by Suraj Shah · Powered by SARIMA GHI Forecasting · Streamlit Deployment\n",
    "\"\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": none,
   "id": "5abfade9-1c8a-4786-bc10-f70e19f1bc82",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
