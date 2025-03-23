import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 📂 Load the CSV file
csv_filename = "pull_requests.csv"

try:
    df = pd.read_csv(csv_filename)
    print("✅ CSV file loaded successfully!")
except FileNotFoundError:
    print("❌ Error: CSV file not found! Run `fetch_pr_data.py` first.")
    exit()

# 🧐 Inspect the data
print("📊 First few rows of the dataset:")
print(df.head())

# 🛠️ Handle missing values (replace None with 0)
df.fillna(0, inplace=True)

# 🔍 Check basic statistics
print("\n📊 Data Summary:")
print(df.describe())

# 🔄 Convert columns to numeric (if needed)
df["Pull Request Size"] = pd.to_numeric(df["Pull Request Size"], errors="coerce")
df["Time to First Review (mins)"] = pd.to_numeric(df["Time to First Review (mins)"], errors="coerce")
df["Pull Request Duration (mins)"] = pd.to_numeric(df["Pull Request Duration (mins)"], errors="coerce")

# 📈 Plot PR Size vs. Review Time
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="Pull Request Size", y="Time to First Review (mins)")
plt.title("PR Size vs. Time to First Review")
plt.xlabel("Pull Request Size (Lines Changed)")
plt.ylabel("Time to First Review (Minutes)")
plt.grid(True)
plt.show()

# 📈 Plot PR Size vs. PR Duration
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="Pull Request Size", y="Pull Request Duration (mins)")
plt.title("PR Size vs. PR Duration")
plt.xlabel("Pull Request Size (Lines Changed)")
plt.ylabel("PR Duration (Minutes)")
plt.grid(True)
plt.show()

# 🔍 Compute correlations
correlation_matrix = df[["Pull Request Size", "Time to First Review (mins)", "Pull Request Duration (mins)"]].corr()
print("\n🔗 Correlation Matrix:")
print(correlation_matrix)

# 🔥 Heatmap for Correlations
plt.figure(figsize=(6, 4))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap")
plt.show()
