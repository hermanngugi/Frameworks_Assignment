import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv", low_memory=False)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

# App title
st.title("CORD-19 Data Explorer")
st.write("A simple exploration of COVID-19 research papers (CORD-19 metadata)")

# Sidebar filters
year_range = st.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Publications over time
st.subheader("Publications Over Time")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
year_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
top_journals.plot(kind="bar", ax=ax)
ax.set_xlabel("Journal")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Word cloud
st.subheader("Word Cloud of Titles")
text = " ".join(str(title) for title in filtered['title'].dropna())
if text:
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.write("No titles available for this selection.")

# Show data sample
st.subheader("Sample Data")
st.dataframe(filtered.head(20))
