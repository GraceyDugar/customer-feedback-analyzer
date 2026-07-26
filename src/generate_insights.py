import pandas as pd

df = pd.read_csv("data/analyzed_feedback.csv")

# 1. Overall sentiment breakdown
sentiment_counts = df["sentiment"].value_counts()
print("=== Sentiment Breakdown ===")
print(sentiment_counts)
print()

# 2. Theme breakdown — this is the "what should we prioritize" view
theme_counts = df["theme"].value_counts()
print("=== Theme Breakdown (by volume) ===")
print(theme_counts)
print()

# 3. Cross-tab: which themes carry the most negative sentiment
# This matters more than raw volume — a theme with 10 mentions that are all
# neutral is less urgent than a theme with 5 mentions that are all negative
negative_by_theme = df[df["sentiment"].str.upper() == "NEGATIVE"]["theme"].value_counts()
print("=== Themes with Negative Sentiment (priority signal) ===")
print(negative_by_theme)
print()

# 4. Save a summary report
with open("output/insights_summary.txt", "w") as f:
    f.write("CUSTOMER FEEDBACK INSIGHTS SUMMARY\n")
    f.write("=" * 40 + "\n\n")
    f.write(f"Total feedback analyzed: {len(df)}\n\n")
    f.write("Sentiment Breakdown:\n")
    f.write(sentiment_counts.to_string() + "\n\n")
    f.write("Top Themes by Volume:\n")
    f.write(theme_counts.to_string() + "\n\n")
    f.write("Themes with Negative Sentiment (highest priority):\n")
    f.write(negative_by_theme.to_string() + "\n")

print("Saved summary to output/insights_summary.txt")

import matplotlib.pyplot as plt

comparison = pd.DataFrame({
    "total_mentions": theme_counts,
    "negative_mentions": negative_by_theme
}).fillna(0)

comparison.plot(kind="bar", figsize=(9, 5))
plt.title("Feedback Themes: Total Volume vs Negative Sentiment")
plt.ylabel("Number of mentions")
plt.xlabel("Theme")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("output/theme_chart.png")
print("Saved chart to output/theme_chart.png")