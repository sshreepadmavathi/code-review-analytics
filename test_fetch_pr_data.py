import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime
import pytz
from fetch_pr_data import fetch_prs

class TestFetchPRs(unittest.TestCase):
    @patch("fetch_pr_data.repo.get_pulls")  # ✅ Mock `repo.get_pulls`
    def test_fetch_prs(self, mock_get_pulls):
        """Test if PR data is fetched and written correctly to CSV"""

        # ✅ Create Mock Pull Request Objects
        mock_pr1 = MagicMock()
        mock_pr1.created_at = datetime(2024, 1, 10, 12, 0, 0, tzinfo=pytz.utc)
        mock_pr1.merged_at = datetime(2024, 1, 12, 14, 30, 0, tzinfo=pytz.utc)
        mock_pr1.additions = 50
        mock_pr1.deletions = 20
        mock_pr1.get_reviews.return_value = [
            MagicMock(submitted_at=datetime(2024, 1, 11, 10, 0, 0, tzinfo=pytz.utc), user=MagicMock(login="reviewer1"))
        ]

        mock_pr2 = MagicMock()
        mock_pr2.created_at = datetime(2024, 1, 15, 9, 0, 0, tzinfo=pytz.utc)
        mock_pr2.merged_at = datetime(2024, 1, 17, 18, 45, 0, tzinfo=pytz.utc)
        mock_pr2.additions = 100
        mock_pr2.deletions = 40
        mock_pr2.get_reviews.return_value = [
            MagicMock(submitted_at=datetime(2024, 1, 16, 14, 0, 0, tzinfo=pytz.utc), user=MagicMock(login="reviewer2"))
        ]

        # ✅ Mock `get_pulls` to return mock PRs
        mock_get_pulls.return_value = [mock_pr1, mock_pr2]

        # ✅ Run `fetch_prs()` with mock repo
        fetch_prs(repo_instance=MagicMock(get_pulls=lambda state: [mock_pr1, mock_pr2]))  

        # ✅ Check if CSV file was created
        self.assertTrue(os.path.exists("pull_requests.csv"))

        # ✅ Verify CSV Content
        with open("pull_requests.csv", "r") as file:
            content = file.readlines()
            print("CSV Content:", content)  
            self.assertGreater(len(content), 1, "CSV file should have data rows!")

if __name__ == "__main__":
    unittest.main()
