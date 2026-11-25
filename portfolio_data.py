
from decimal import Decimal

PORTFOLIOS = {

    "POR001": {
        "cash_balance": Decimal("100000"),
        "restricted_securities": ["XYZCORP"],
        "max_position_pct": Decimal("0.20"),
        "current_holdings": [
            ("AAPL", 100, Decimal("150")),
            ("TCS", 50, Decimal("310")),
            ("INFY", 20, Decimal("1500"))
        ]
    },

    "POR002": {
        "cash_balance": Decimal("50000"),
        "restricted_securities": [],
        "max_position_pct": Decimal("0.25"),
        "current_holdings": [
            ("GOOGL", 10, Decimal("2000"))
        ]
    },

    "POR003": {
        "cash_balance": Decimal("200000"),
        "restricted_securities": ["BADCO"],
        "max_position_pct": Decimal("0.30"),
        "current_holdings": [
            ("TCS", 100, Decimal("300")),
            ("INFY", 50, Decimal("1500")),
            ("RELIANCE", 30, Decimal("2400"))
        ]
    },

    "POR004": {
        "cash_balance": Decimal("100000"),
        "restricted_securities": [],
        "max_position_pct": Decimal("0.20"),
        "current_holdings": [
            ("GOOGL", 10, Decimal("2000")),
            ("AAPL", 100, Decimal("150"))
        ]
    },

    "POR005": {
        "cash_balance": Decimal("10000"),
        "restricted_securities": [],
        "max_position_pct": Decimal("0.25"),
        "current_holdings": [
            ("PENNY1", 10, Decimal("10")),
            ("AAPL", 20, Decimal("150")),
            ("TCS", 10, Decimal("250"))
        ]
    }
}
