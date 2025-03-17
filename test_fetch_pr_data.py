import unittest
from fetch_pr_data import fetch_prs
import os

class TestFetchPRs(unittest.TestCase):
    def test_fetch_prs(self):
        """Test if CSV file is created successfully"""
        fetch_prs()
        self.assertTrue(os.path.exists("pull_requests.csv"))

if __name__ == "__main__":
    unittest.main()

