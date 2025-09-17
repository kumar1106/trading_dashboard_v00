# src/app.py
# Streamlit app entry point

import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_logger, retry_network
from database import was_alerted_recently, record_alert
from config import DEFAULT_THRESHOLD_ABS, DEFAULT_THRESHOLD_PCT, BASE_CURRENCY

logger = get_logger()

# Load positions CSV
@st.cache_data(ttl=3600)
def load_positions(path="positions.csv"):
    return pd.read_csv(path)

positions = load_positions()

st.title("Trading Dashboard")
st.write("Portfolio Positions:")
st.dataframe(positions)

# Example alert processing
if st.button("Check Alerts"):
    current_time = int(datetime.now().timestamp())
    for _, row in positions.iterrows():
        triggered = False
        alert_type = None
        if abs(row['P&L']) > DEFAULT_THRESHOLD_ABS:
            triggered = True
            alert_type = 'pnl_abs'
        if abs(row['P&L_Pct']) > DEFAULT_THRESHOLD_PCT:
            triggered = True
            alert_type = alert_type or 'pnl_pct'
        if triggered:
            if not was_alerted_recently(row['Symbol'], alert_type, current_time):
                st.warning(f"{row['Symbol']}: P&L {row['P&L']:.2f} ({row['P&L_Pct']:.1f}%) - Type: {alert_type.upper()}")
                record_alert(row['Symbol'], alert_type, current_time)
            else:
                st.info(f"Alert skipped for {row['Symbol']} ({alert_type.upper()})")
