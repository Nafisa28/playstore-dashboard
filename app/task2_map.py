import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import pytz

st.title("Task 2 – Global Installs Choropleth Map")


# Load dataset
apps_df = pd.read_csv("../data/play_store_data.csv")

st.subheader("Dataset Preview")
st.write(apps_df.head())


# Clean Installs column
apps_df['Installs'] = apps_df['Installs'].str.replace('+', '', regex=False)
apps_df['Installs'] = apps_df['Installs'].str.replace(',', '', regex=False)
apps_df['Installs'] = pd.to_numeric(apps_df['Installs'], errors='coerce')
apps_df['Installs'] = apps_df['Installs'].fillna(0).astype(int)


# Remove categories starting with A, C, G, S
filtered_df = apps_df[
    ~apps_df['Category'].str.startswith(('A', 'C', 'G', 'S'), na=False)
]

st.subheader("After Removing A/C/G/S Categories")
st.write(filtered_df[['App','Category','Installs']].head())


# Total installs per category
category_installs = (
    filtered_df
    .groupby('Category')['Installs']
    .sum()
    .reset_index()
)

st.subheader("Total Installs by Category")
st.dataframe(category_installs)


# Top 5 categories by installs
top5_categories = category_installs.sort_values(
    by='Installs', ascending=False
).head(5)

st.subheader("Top 5 Categories")
st.dataframe(top5_categories)

# Prepare choropleth data (one category per country)
countries = ["India", "United States", "Brazil", "Germany", "Australia"]

map_df = top5_categories.head(5).copy()
map_df = map_df.reset_index(drop=True)

map_df["Country"] = countries

st.subheader("Map Data Preview")
st.dataframe(map_df)

import plotly.express as px
from datetime import datetime
import pytz

# Time restriction (6 PM – 8 PM IST)
ist = pytz.timezone("Asia/Kolkata")
current_hour = datetime.now(ist).hour


# Highlight categories with installs > 1M
map_df['Highlight'] = map_df['Installs'].apply(
    lambda x: "Above 1M Installs" if x > 1_000_000 else "Normal"
)

st.subheader("Highlighted Categories")
st.dataframe(map_df)

if 18 <= current_hour <= 20:

    st.subheader("Task 2: Global Installs Choropleth Map")

    fig = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    hover_data=["Category","Installs"],
    color="Highlight",
    projection="natural earth",
    color_discrete_map={
        "Above 1M Installs": "red",
        "Normal": "lightblue"
    },
    title="Global Installs by Top 5 Categories"
)

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Choropleth map visible only between 6 PM and 8 PM IST")
