import csv
import os
import pytz
from github import Github, Auth
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 🔄 Load environment variables
load_dotenv()

# 🔑 Get GitHub Token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 🚨 Ensure the GitHub token is available
if not GITHUB_TOKEN:
    raise ValueError("GitHub Token is missing! Check your .env file.")

# 📂 Repository details
REPO_NAME = "junit-team/junit5"

# 🏗️ Authenticate using the latest method
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)
repo = g.get_repo(REPO_NAME)

# 📆 Get the date 3 months ago (timezone-aware)
three_months_ago = datetime.now(pytz.utc) - timedelta(days=90)

def fetch_prs():
    """Fetch PR data and save it to a CSV file."""
    pulls = []
    for pr in repo.get_pulls(state="closed"):
        if pr.created_at >= three_months_ago:
            pulls.append(pr)

    # 📄 CSV file name
    csv_filename = "pull_requests.csv"

    # 📝 Define headers
    headers = ["Pull Request Size", "Time to First Review (mins)", "Pull Request Duration (mins)", "Reviewers"]

    # 📊 Store data here
    data = []

    for pr in pulls:
        if pr.merged_at:  # Only include merged PRs
            pr_size = pr.additions + pr.deletions  # PR Size = Added + Deleted lines
            
            # ⏳ Calculate time to first review
            reviews = list(pr.get_reviews())  # Convert to list to access elements
            if reviews:
                first_review_time = (reviews[0].submitted_at - pr.created_at).total_seconds() / 60
            else:
                first_review_time = None  # No review comments

            # ⏳ Calculate PR duration
            pr_duration = (pr.merged_at - pr.created_at).total_seconds() / 60

            # 👥 Get unique reviewers
            reviewers = ", ".join({review.user.login for review in reviews if review.user})

            # 📌 Add data row
            data.append([pr_size, first_review_time, pr_duration, reviewers])

    # ✍️ Write data to CSV
    try:
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"✅ CSV file '{csv_filename}' created successfully!")
    except PermissionError:
        print("❌ Permission denied! Close the CSV file if it's open and try again.")

# ✅ Run function if script is executed directly
if __name__ == "__main__":
    fetch_prs()
