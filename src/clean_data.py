import pandas as pd

df = pd.read_csv("data/raw/feedback_raw.csv")
print("Rows before cleaning:", len(df))

# 1. Drop exact duplicate rows
df = df.drop_duplicates(subset="text")

# 2. Drop rows with missing/empty text
df = df.dropna(subset=["text"])
df = df[df["text"].str.strip() != ""]

# 3. Trim whitespace on all text columns
df["text"] = df["text"].str.strip()
df["author"] = df["author"].str.strip()

# 4. Standardize the date column to a real datetime type
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# 5. Add a word count column — useful later to filter out low-signal feedback like "great!"
df["word_count"] = df["text"].str.split().str.len()

print("Rows after cleaning:", len(df))
print(df.head())

# Save cleaned version
df.to_csv("data/cleaned_feedback.csv", index=False)
print("Saved to data/cleaned_feedback.csv")