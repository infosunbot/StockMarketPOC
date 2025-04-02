from collections import defaultdict, deque
from datetime import datetime

stocks = {
    "TEA": {"type": "Common", "last_dividend": 0, "fixed_dividend": None, "par_value": 100},
    "POP": {"type": "Common", "last_dividend": 8, "fixed_dividend": None, "par_value": 100},
    "ALE": {"type": "Common", "last_dividend": 23, "fixed_dividend": None, "par_value": 60},
    "GIN": {"type": "Preferred", "last_dividend": 8, "fixed_dividend": 0.02, "par_value": 100},
    "JOE": {"type": "Common", "last_dividend": 13, "fixed_dividend": None, "par_value": 250}
}

# Group trades by stock symbol using deque for fast time-window slicing
# On real world scenario it would be a DB optimisation, like indexing 
trades_by_symbol = defaultdict(deque)