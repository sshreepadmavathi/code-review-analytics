import csv
import pytz
from datetime import datetime, timedelta

def fetch_prs(repo):
    """Fetch PR data from a given repository and save it to a CSV file."""
    pulls = []
    three_months_ago = datetime.now(pytz.utc) - timedelta(days=90)

    print("🔄 Fetching closed PRs...")  # Debugging
    for pr in repo.get_pulls(state="closed"):
        if pr.created_at >= three_months_ago:
            pulls.append(pr)

    print(f"✅ Total PRs fetched: {len(pulls)}")  # Debugging

    # CSV File
    csv_filename = "pull_requests.csv"
    headers = ["Pull Request Size", "Time to First Review (mins)", "Pull Request Duration (mins)", "Reviewers"]
    data = []

    for pr in pulls:
        if pr.merged_at:
            pr_size = pr.additions + pr.deletions  # PR Size
            reviews = list(pr.get_reviews())  # Convert to list

            first_review_time = None
            if reviews:
                first_review_time = (reviews[0].submitted_at - pr.created_at).total_seconds() / 60

            pr_duration = (pr.merged_at - pr.created_at).total_seconds() / 60
            reviewers = ", ".join({review.user.login for review in reviews if review.user})

            # 🔍 Debugging output
            print(f"📌 PR Created: {pr.created_at}, Merged: {pr.merged_at}, Size: {pr_size}, Reviewers: {reviewers}")

            data.append([pr_size, first_review_time, pr_duration, reviewers])

    # Write to CSV
    try:
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"✅ CSV file '{csv_filename}' created successfully!")
    except PermissionError:
        print("❌ Permission denied! Close the CSV file if it's open and try again.")
