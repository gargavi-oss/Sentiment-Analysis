import pandas as pd


df = pd.read_csv("training.1600000.processed.noemoticon.csv", encoding='latin-1', header=None)


df = df[[0, 5]]
df.columns = ["label", "text"]

# Map label 4 (positive) → 1, keep 0 as negative
df["label"] = df["label"].replace(4, 1)

# Remove neutral tweets (label=2) if they exist
df = df[df["label"] != 2]

# 🔹 Reduce dataset size for faster training
# Choose your size (e.g. 10000, 50000, 100000)
df = df.sample(n=20000, random_state=42).reset_index(drop=True)

# Shuffle dataset again just in case
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save smaller dataset
df.to_csv("twitter_data_small.csv", index=False)

print(f"✅ twitter_data_small.csv created with {len(df)} samples (columns: text, label)")
