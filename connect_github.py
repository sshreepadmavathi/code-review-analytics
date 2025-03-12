from github import Github

# 🔑 Use your GitHub Personal Access Token here
GITHUB_TOKEN = "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"

# 🏗️ Connect to GitHub
g = Github(GITHUB_TOKEN)

# 🧑 Get my GitHub username
user = g.get_user()
print(f"✅ Successfully connected! Logged in as: {user.login}")

