# tests/test_dashboard.py
# Unit tests for trading dashboard

import unittest
import time
from database import record_alert, was_alerted_recently, init_alert_history
from config import ALERT_DEDUPE_WINDOW

class TestAlerts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_alert_history()

    def test_alert_deduplication(self):
        ts = int(time.time())
        record_alert("TEST1", "pnl_abs", ts)
        self.assertTrue(was_alerted_recently("TEST1", "pnl_abs", ts+10))
        self.assertFalse(was_alerted_recently("TEST1", "pnl_abs", ts+ALERT_DEDUPE_WINDOW+1))

if __name__ == "__main__":
    unittest.main(verbosity=2)
