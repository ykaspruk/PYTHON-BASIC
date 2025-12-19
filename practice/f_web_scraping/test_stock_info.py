"""
Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""
import unittest
from unittest.mock import MagicMock, patch
from stock_info import get_most_active_tickers, scrape_stock_all_tabs, render_table


class TestStockInfo(unittest.TestCase):

    def test_get_most_active_tickers_structure(self):
        """Integration test: Verify we get a list of tuples from the live site."""
        tickers = get_most_active_tickers()
        self.assertIsInstance(tickers, list)
        if tickers:
            self.assertIsInstance(tickers[0], tuple)
            self.assertEqual(len(tickers[0]), 2)

    @patch('selenium.webdriver.Chrome')
    def test_scrape_stock_all_tabs_mock(self, mock_driver):
        """Unit test: Verify the data structure returned by the scraper."""
        driver_instance = mock_driver.return_value

        mock_address = MagicMock()
        mock_address.find_elements.return_value = [MagicMock(text="Line 1"), MagicMock(text="USA")]

        mock_stats = MagicMock(text="Full Time Employees: 10,000")
        mock_emp_val = MagicMock(text="10,000")
        mock_stats.find_element.return_value = mock_emp_val

        driver_instance.find_element.side_effect = [mock_address, mock_stats]
        driver_instance.find_elements.return_value = []

        result = scrape_stock_all_tabs(driver_instance, "AAPL", "Apple Inc.")

        self.assertEqual(result["Code"], "AAPL")
        self.assertEqual(result["Country"], "USA")
        self.assertEqual(result["Employees"], "10,000")

    def test_parse_logic_in_report(self):
        """Test the logic used for sorting without running the whole scraper."""
        test_results = [
            {"Name": "A", "CEO Year Born": "1990", "52-Week Change": "10.0%"},
            {"Name": "B", "CEO Year Born": "1980", "52-Week Change": "50.0%"},
            {"Name": "C", "CEO Year Born": "2000", "52-Week Change": "5.0%"}
        ]

        # Test Youngest CEO logic (Highest year)
        youngest = sorted([r for r in test_results if r["CEO Year Born"].isdigit()],
                          key=lambda x: int(x["CEO Year Born"]), reverse=True)
        self.assertEqual(youngest[0]["Name"], "C")  # Year 2000 is youngest

        # Test 52-Week Change parsing
        def parse_pct(s):
            return float(s.replace('%', ''))

        best_gainer = max(test_results, key=lambda x: parse_pct(x["52-Week Change"]))
        self.assertEqual(best_gainer["Name"], "B")  # 50.0% is highest


if __name__ == "__main__":
    unittest.main()