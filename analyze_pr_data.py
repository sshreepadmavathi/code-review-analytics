import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 📂 Load CSV file
df = pd.read_csv("pull_requests.csv")

# 🔍 Remove rows with missing values
df.dropna(inplace=True)

# 📊 Scatter plot: PR Size vs. Time to First Review
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["Pull Request Size"], y=df["Time to First Review (mins)"])
plt.title("PR Size vs. Time to First Review")
plt.xlabel("Pull Request Size (Lines Changed)")
plt.ylabel("Time to First Review (mins)")
plt.show()

# 📈 Correlation Matrix
correlation = df.corr()
print("📊 Correlation Matrix:\n", correlation)

# 🔥 Heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(correlation, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
