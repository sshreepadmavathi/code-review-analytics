import csv
import pytz
import sys
from datetime import datetime, timedelta
from github import Github

def fetch_prs(repo):
    pulls = []
    three_months_ago = datetime.now(pytz.utc) - timedelta(days=90)

    print("🔄 Fetching closed PRs...")
    for pr in repo.get_pulls(state="closed"):
        if pr.created_at >= three_months_ago:
            pulls.append(pr)

    print(f"✅ Total PRs fetched: {len(pulls)}")

    csv_filename = "pull_requests.csv"
    headers = ["Pull Request Size", "Time to First Review (mins)", "Pull Request Duration (mins)", "Reviewers"]
    data = []

    for pr in pulls:
        if pr.merged_at:
            pr_size = pr.additions + pr.deletions
            reviews = list(pr.get_reviews())

            first_review_time = None
            if reviews:
                first_review_time = (reviews[0].submitted_at - pr.created_at).total_seconds() / 60

            pr_duration = (pr.merged_at - pr.created_at).total_seconds() / 60
            reviewers = ", ".join({review.user.login for review in reviews if review.user})

            print(f"📌 PR: {pr.title}, Size: {pr_size}, Reviewers: {reviewers}")
            data.append([pr_size, first_review_time, pr_duration, reviewers])

    try:
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"✅ CSV file '{csv_filename}' created successfully!")
    except PermissionError:
        print("❌ Permission denied! Close the CSV file if it's open and try again.")

# ✅ Main block to make the script executable
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fetch_pr_data.py <github_token> <org/repo>")
        sys.exit(1)

    token = sys.argv[1]
    repo_name = sys.argv[2]

    g = Github(token)
    try:
        repo = g.get_repo(repo_name)
        fetch_prs(repo)
    except Exception as e:
        print(f"❌ Error accessing repo: {e}")
