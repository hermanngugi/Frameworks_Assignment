"""
CORD-19 Research Data Analysis
-------------------------------
Loads, cleans, and explores COVID-19 research papers metadata.
Generates simple visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load dataset
print("Loading dataset...")
df = pd.read_csv("metadata.csv", low_memory=False)

# Inspect first few rows
print("First 5 rows:")
print(df.head())

# Data info
print("\nData Info:")
print(df.info())

# Missing values
print("\nMissing values:")
print(df.isnull().sum().head(15))

# Clean data
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['abstract_word_count'] = df['abstract'].astype(str).apply(lambda x: len(x.split()) if x != 'nan' else 0)

# Basic analysis
year_counts = df['year'].value_counts().sort_index()
top_journals = df['journal'].value_counts().head(10)

print("\nPublications per year:")
print(year_counts)

print("\nTop Journals:")
print(top_journals)

# === Visualizations ===
sns.set(style="whitegrid")

# Publications over time
plt.figure(figsize=(10, 5))
year_counts.plot(kind="bar")
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.tight_layout()
plt.show()

# Top journals
plt.figure(figsize=(10, 5))
top_journals.plot(kind="bar")
plt.title("Top 10 Journals")
plt.xlabel("Journal")
plt.ylabel("Number of Papers")
plt.tight_layout()
plt.show()

# Word cloud for titles
text = " ".join(str(title) for title in df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
plt.show()
