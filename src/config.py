# src/config.py
# Configuration settings for the trading dashboard

# Logging settings
LOG_MAX_BYTES = 1048576  # 1MB per log file
LOG_BACKUP_COUNT = 5     # Keep 5 old logs

# Alert de-duplication window (seconds)
ALERT_DEDUPE_WINDOW = 3600  # 1 hour

# Default alert thresholds
DEFAULT_THRESHOLD_ABS = 100.0   # Absolute P&L
DEFAULT_THRESHOLD_PCT = 5.0     # P&L percentage

# Portfolio database
PORTFOLIO_DB = "portfolio.db"

# FX base currency
BASE_CURRENCY = "USD"
