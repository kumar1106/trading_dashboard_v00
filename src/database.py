# src/database.py
# SQLite database handling: alert history

import sqlite3
from config import PORTFOLIO_DB, ALERT_DEDUPE_WINDOW
from utils import get_logger

logger = get_logger()

def init_alert_history() -> None:
    """
    Initialize alert history table with composite key: (symbol, alert_type)
    """
    conn = sqlite3.connect(PORTFOLIO_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS alert_history
                 (symbol TEXT, alert_type TEXT, timestamp INTEGER,
                  PRIMARY KEY (symbol, alert_type))''')
    conn.commit()
    conn.close()
    logger.info("Alert history table initialized.")

def record_alert(symbol: str, alert_type: str, timestamp: int) -> None:
    """
    Record alert for a symbol and type.
    """
    conn = sqlite3.connect(PORTFOLIO_DB)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO alert_history VALUES (?, ?, ?)",
              (symbol, alert_type, timestamp))
    conn.commit()
    conn.close()
    logger.info(f"Recorded {alert_type} alert for {symbol} at {timestamp}.")

def was_alerted_recently(symbol: str, alert_type: str, current_time: int) -> bool:
    """
    Check if an alert was sent within ALERT_DEDUPE_WINDOW.
    """
    conn = sqlite3.connect(PORTFOLIO_DB)
    c = conn.cursor()
    c.execute("SELECT timestamp FROM alert_history WHERE symbol=? AND alert_type=?",
              (symbol, alert_type))
    result = c.fetchone()
    conn.close()
    if result:
        last_time = result[0]
        if current_time - last_time < ALERT_DEDUPE_WINDOW:
            logger.info(f"Skipped duplicate {alert_type} alert for {symbol}.")
            return True
    return False
