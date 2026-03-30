import pandas as pd
import streamlit as st

st.title("Task 1 – Google Play Store Analysis")

# Load datasets
import os

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "../data/play_store_data.csv")
df = pd.read_csv(data_path)
current_dir = os.path.dirname(__file__)
reviews_path = os.path.join(current_dir, "../data/user_reviews.csv")
reviews_df = pd.read_csv(reviews_path)
df["Category"] = df["Category"].str.upper()

st.subheader("Apps Dataset Preview")
st.write(df.head())

st.subheader("Apps Dataset Columns")
st.write(df.columns)

st.subheader("Reviews Dataset Preview")
st.write(reviews_df.head())

st.subheader("Reviews Dataset Columns")
st.write(reviews_df.columns)


# Clean Installs column safely
df['Installs'] = df['Installs'].str.replace('+', '', regex=False)
df['Installs'] = df['Installs'].str.replace(',', '', regex=False)

# Convert to numeric, invalid values (like 'Free') become NaN
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

# Replace NaN with 0
df['Installs'] = df['Installs'].fillna(0).astype(int)
# Convert Rating to numeric
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

st.sidebar.header("Filters")

# Category filter
category = st.sidebar.selectbox(
    "Select Category",
    options=df['Category'].unique()
)

# Rating filter
min_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=3.5
)

filtered_apps = df[
    (df['Category'] == category) &
    (df['Rating'] >= min_rating)
]

st.subheader("Filtered Apps")
st.dataframe(filtered_apps)


st.subheader("Top 10 Apps by Installs")

top_apps = (
    filtered_apps
    .sort_values(by="Installs", ascending=False)
    .head(10)
)

st.bar_chart(top_apps.set_index("App")["Installs"])



import plotly.express as px
from datetime import datetime
import pytz

# Convert Size to MB
def convert_size(size):
    if isinstance(size, str) and 'M' in size:
        return float(size.replace('M', ''))
    elif isinstance(size, str) and 'k' in size:
        return float(size.replace('k', '')) / 1024
    return None

df['Size_MB'] = df['Size'].apply(convert_size)

# Convert Reviews to numeric
df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')

# Merge apps and reviews
merged_df = pd.merge(df, reviews_df, on='App', how='inner')

allowed_categories = [
    'GAME', 'BEAUTY', 'BUSINESS', 'COMICS',
    'COMMUNICATION', 'DATING',
    'ENTERTAINMENT', 'SOCIAL', 'EVENTS'
]

task1_df = merged_df[
    (merged_df['Rating'] > 3.5) &
    (merged_df['Reviews'] > 500) &
    (merged_df['Installs'] > 50000) &
    (merged_df['Category'].isin(allowed_categories)) &
    (~merged_df['App'].str.contains('s', case=False, na=False)) &
    (merged_df['Sentiment_Subjectivity'] > 0.5)
]

category_translation = {
    "BEAUTY": "सौंदर्य",        # Hindi
    "BUSINESS": "வணிகம்",      # Tamil
    "DATING": "Partnersuche"   # German
}

task1_df["Category_Display"] = task1_df["Category"].map(
    lambda x: category_translation.get(x, x)
)
# Time restriction (5 PM – 7 PM IST)
ist = pytz.timezone("Asia/Kolkata")
current_hour = datetime.now(ist).hour

if 17 <= current_hour < 19:
    st.subheader("Task 1: App Size vs Rating (Bubble Chart)")
   
    fig = px.scatter(
        task1_df,
        x="Size_MB",
        y="Rating",
        size="Installs",
        color="Category_Display",
        hover_name="App",
        size_max=70,
        opacity=0.75,
        color_discrete_map={
            "GAME": "pink",
            "सौंदर्य": "green",      # Hindi Beauty
            "வணிகம்": "blue",       # Tamil Business
            "Partnersuche": "purple",
            "COMICS": "brown",
            "COMMUNICATION": "orange",
            "ENTERTAINMENT": "red",
            "SOCIAL": "gray",
            "EVENTS": "cyan"
        },
        title="App Size vs Rating (Bubble Chart)"
    )
    fig.update_layout(
        xaxis_title="App Size (MB)",
        yaxis_title="Rating",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Bubble chart visible only between 5 PM and 7 PM IST")

st.subheader("User Sentiment Distribution")


sentiment_counts = reviews_df['Sentiment'].value_counts()
st.bar_chart(sentiment_counts)


