import csv
import os
import pytz
from github import Github
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 🔄 Load environment variables
load_dotenv()

# 🔑 Get GitHub Token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 🚨 Debugging: Check if token is loaded
if not GITHUB_TOKEN:
    raise ValueError("GitHub Token is missing! Check your .env file.")

# 📂 Repository details
REPO_NAME = "junit-team/junit5"

# 🏗️ Connect to GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# 📆 Get the date 3 months ago (Ensure it's timezone-aware)
three_months_ago = datetime.now(pytz.utc) - timedelta(days=90)

# 📌 Fetch only PRs created in the last 3 months (Using pagination)
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
        reviews = pr.get_reviews()
        if reviews.totalCount > 0:
            first_review_time = (reviews[0].submitted_at - pr.created_at).total_seconds() / 60
        else:
            first_review_time = None  # No review comments

        # ⏳ Calculate PR duration
        pr_duration = (pr.merged_at - pr.created_at).total_seconds() / 60

        # 👥 Get reviewers
        reviewers = ", ".join(set([review.user.login for review in reviews if review.user]))

        # 📌 Add data row
        data.append([pr_size, first_review_time, pr_duration, reviewers])

# ✍️ Write data to CSV
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)

print(f"✅ CSV file '{csv_filename}' created successfully!")
