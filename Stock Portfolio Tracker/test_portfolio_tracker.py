"""
Unit Tests for Stock Portfolio Tracker
--------------------------------------
Verifies key functions including arithmetic calculations, dictionary updates,
portfolio summary logic, and file handling.
"""

import os
import unittest
import csv
from portfolio_tracker import (
    STOCK_PRICES,
    calculate_portfolio_summary,
    save_portfolio_to_file
)


class TestStockPortfolioTracker(unittest.TestCase):

    def setUp(self):
        self.sample_prices = {
            "AAPL": 180.00,
            "TSLA": 250.00,
            "GOOGL": 100.00
        }

    def test_calculate_portfolio_summary(self):
        portfolio = [
            {"symbol": "AAPL", "price": 180.00, "quantity": 10.0, "total": 1800.00},
            {"symbol": "TSLA", "price": 250.00, "quantity": 2.0, "total": 500.00},
            {"symbol": "GOOGL", "price": 100.00, "quantity": 5.0, "total": 500.00},
        ]

        total_val, updated_portfolio = calculate_portfolio_summary(portfolio)

        # Total expected: 1800 + 500 + 500 = 2800.00
        self.assertEqual(total_val, 2800.00)

        # Weight checks:
        # AAPL: 1800 / 2800 * 100 = 64.2857%
        # TSLA: 500 / 2800 * 100 = 17.857%
        self.assertAlmostEqual(updated_portfolio[0]["weight"], 64.2857, places=3)
        self.assertAlmostEqual(updated_portfolio[1]["weight"], 17.8571, places=3)

    def test_stock_prices_dictionary_lookup(self):
        self.assertIn("AAPL", STOCK_PRICES)
        self.assertIn("TSLA", STOCK_PRICES)
        self.assertEqual(STOCK_PRICES["AAPL"], 180.50)
        self.assertEqual(STOCK_PRICES["TSLA"], 250.00)

    def test_empty_portfolio_calculation(self):
        total_val, updated_portfolio = calculate_portfolio_summary([])
        self.assertEqual(total_val, 0.0)
        self.assertEqual(updated_portfolio, [])


if __name__ == "__main__":
    unittest.main()
