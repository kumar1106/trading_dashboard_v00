# src/scheduler.py
# Scheduler to run periodic analysis and alerts

from datetime import datetime
from src.config import DEFAULT_THRESHOLD_ABS, DEFAULT_THRESHOLD_PCT
from src.database import record_alert, was_alerted_recently
from src.utils import get_logger
# from src.app import send_alert  # Import dynamically to avoid circular

logger = get_logger()

def run_analysis(positions, send_alert):
    """
    Run analysis for positions.
    positions: DataFrame with Symbol, P&L, P&L_Pct
    send_alert: function to call for alerting
    """
    current_time = int(datetime.now().timestamp())
    for _, row in positions.iterrows():
        triggered = False
        alert_type = None
        if abs(row['P&L']) > DEFAULT_THRESHOLD_ABS:
            triggered = True
            alert_type = 'pnl_abs'
        if abs(row['P&L_Pct']) > DEFAULT_THRESHOLD_PCT and alert_type is None:
            triggered = True
            alert_type = 'pnl_pct'
        if triggered:
            if not was_alerted_recently(row['Symbol'], alert_type, current_time):
                send_alert(row['Symbol'], row['P&L'], row['P&L_Pct'],
                           {'abs': DEFAULT_THRESHOLD_ABS, 'pct': DEFAULT_THRESHOLD_PCT})
                record_alert(row['Symbol'], alert_type, current_time)
