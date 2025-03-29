import unittest
from unittest.mock import MagicMock
import pytz
from datetime import datetime, timedelta
from fetch_pr_data import fetch_prs  # Import the function to test

class TestFetchPRs(unittest.TestCase):
    def test_fetch_prs(self):
        """Test if fetch_prs correctly processes and writes PR data to CSV."""
        # 🛠️ Mock repo and PRs
        mock_repo = MagicMock()

        # Mock PR1 (recent, within 90 days)
        mock_pr1 = MagicMock()
        mock_pr1.created_at = datetime.now(pytz.utc) - timedelta(days=10)  # Within 90 days
        mock_pr1.merged_at = mock_pr1.created_at + timedelta(days=2)
        mock_pr1.additions = 50
        mock_pr1.deletions = 20
        mock_pr1.get_reviews.return_value = [MagicMock(submitted_at=mock_pr1.created_at + timedelta(minutes=30),
                                                        user=MagicMock(login="reviewer1"))]

        # Mock PR2 (recent, within 90 days)
        mock_pr2 = MagicMock()
        mock_pr2.created_at = datetime.now(pytz.utc) - timedelta(days=20)  # Within 90 days
        mock_pr2.merged_at = mock_pr2.created_at + timedelta(days=3)
        mock_pr2.additions = 100
        mock_pr2.deletions = 40
        mock_pr2.get_reviews.return_value = [MagicMock(submitted_at=mock_pr2.created_at + timedelta(minutes=45),
                                                        user=MagicMock(login="reviewer2"))]

        # Assign mock PRs to repo
        mock_repo.get_pulls.return_value = [mock_pr1, mock_pr2]

        # Run fetch_prs
        fetch_prs(mock_repo)

        # ✅ Read and check CSV output
        with open("pull_requests.csv", "r") as file:
            content = file.readlines()

        print(f"CSV Content: {content}")  # Debugging output

        # ✅ Ensure CSV contains data (header + 2 rows)
        self.assertGreater(len(content), 1, "CSV file should have data rows!")

if __name__ == "__main__":
    unittest.main()
