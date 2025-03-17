import csv
import os
from github import Github
from datetime import datetime, timedelta
from dotenv import load_dotenv  # Import dotenv

# 🔄 Load environment variables from .env file
load_dotenv()

# 🔑 Get GitHub Token from .env file
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 📂 Repository details (change this to your repo)
REPO_NAME = "junit-team/junit5"

# 🏗️ Connect to GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# 📆 Get the date 3 months ago
three_months_ago = datetime.now() - timedelta(days=90)

# 📌 Fetch all merged pull requests from the last 3 months
pulls = [pr for pr in repo.get_pulls(state="closed") if pr.created_at >= three_months_ago]

# 📄 CSV file name (Overwrites Existing File)
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

# ✍️ Write data to CSV (Overwrites old file)
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Add column headers
    writer.writerows(data)  # Add data rows

print(f"✅ CSV file '{csv_filename}' created successfully!")
