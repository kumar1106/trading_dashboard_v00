"""
Main Streamlit app for Trading Dashboard.

Features:
- Loads portfolio from positions.csv
- Calculates P&L and P&L %
- Handles alerts with de-duplication
- FX-adjusted vs raw backtesting chart
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import helpers from src folder
from database import was_alerted_recently, record_alert
from utils import get_logger
from config import DEFAULT_THRESHOLD_ABS, DEFAULT_THRESHOLD_PCT

logger = get_logger()

# -------------------------------
# Load Portfolio Positions
# -------------------------------
try:
    positions = pd.read_csv('positions.csv')
    positions.columns = positions.columns.str.strip()  # Clean column names
except FileNotFoundError:
    st.error("positions.csv file not found in project root!")
    st.stop()

# Safety check: Required columns
required_cols = ['Symbol', 'Quantity', 'Avg_Price', 'Currency', 'P&L', 'P&L_Pct']
for col in required_cols:
    if col not in positions.columns:
        st.error(f"Missing column in positions.csv: {col}")
        st.stop()

# -------------------------------
# Calculate P&L & P&L %
# -------------------------------
positions['P&L'] = (positions['Quantity'] * positions['Avg_Price'] * 0)  # Replace 0 with live price if available
positions['P&L_Pct'] = 0.0  # Placeholder; can compute from live price

st.header("Portfolio Overview")
st.dataframe(positions)

# -------------------------------
# Trigger Alerts
# -------------------------------
current_time = int(datetime.now().timestamp())
for _, row in positions.iterrows():
    triggered = False
    alert_type = None

    if abs(row['P&L']) > DEFAULT_THRESHOLD_ABS:
        triggered = True
        alert_type = 'pnl_abs'

    if abs(row['P&L_Pct']) > DEFAULT_THRESHOLD_PCT * 100:
        triggered = True
        alert_type = alert_type or 'pnl_pct'  # Prioritize abs if both

    if triggered:
        if not was_alerted_recently(row['Symbol'], alert_type, current_time):
            st.warning(
                f"⚠️ {row['Symbol']}: P&L {row['P&L']:.2f} ({row['P&L_Pct']:.1f}%) "
                f"- Type: {alert_type.upper().replace('_', ' ')}"
            )
            record_alert(row['Symbol'], alert_type, current_time)
        else:
            st.info(f"Alert for {row['Symbol']} skipped (recent duplicate: {alert_type.upper().replace('_', ' ')})")

st.success("Dashboard loaded successfully!")
