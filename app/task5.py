import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
import pytz

# Load dataset
df = pd.read_csv("../data/play_store_data.csv")

# Task Title
st.title("Task 5: Average Rating vs Total Reviews for Top 10 App Categories")

# Show original dataset
st.subheader("Original Dataset")
st.dataframe(df)

# -----------------------------
# Data Cleaning
# -----------------------------

# Convert Rating column
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Convert Reviews column
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

# Clean Installs column
df['Installs'] = df['Installs'].str.replace('+', '', regex=False)
df['Installs'] = df['Installs'].str.replace(',', '', regex=False)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

# Clean Size column
df['Size'] = df['Size'].str.replace('M', '', regex=False)
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')

# Convert Last Updated column
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Extract update month
df['Update_Month'] = df['Last Updated'].dt.month

# -----------------------------
# Apply Filters
# -----------------------------

filtered_df = df[
    (df['Rating'] >= 4.0) &
    (df['Size'] >= 10) &
    (df['Update_Month'] == 1)
]

# Show filtered dataset
st.subheader("Filtered Dataset (Rating ≥ 4.0, Size ≥ 10M, Updated in January)")
st.dataframe(filtered_df)

# -----------------------------
# Top 10 Categories by Installs
# -----------------------------

category_installs = filtered_df.groupby('Category')['Installs'].sum()

top10_categories = category_installs.sort_values(ascending=False).head(10)

# Show top 10 categories table
st.subheader("Top 10 Categories by Installs")
st.dataframe(top10_categories)

# Filter dataset for those categories
top10_df = filtered_df[filtered_df['Category'].isin(top10_categories.index)]

# -----------------------------
# Final Aggregated Table
# -----------------------------

final_table = top10_df.groupby('Category').agg(
    Average_Rating=('Rating', 'mean'),
    Total_Reviews=('Reviews', 'sum')
).reset_index()
final_table['Total_Reviews_Millions'] = final_table['Total_Reviews'] / 1000000
final_table['Average_Rating'] = final_table['Average_Rating'].round(2)
final_table['Total_Reviews_Millions'] = final_table['Total_Reviews_Millions'].round(2)
final_table = final_table.sort_values(by='Total_Reviews', ascending=False)
# Show aggregated table
st.subheader("Final Aggregated Table")
st.dataframe(final_table)

# -----------------------------
# Grouped Bar Chart
# -----------------------------

# -----------------------------
# Grouped Bar Chart
# -----------------------------

fig = px.bar(
    final_table,
    x='Category',
    y=['Average_Rating', 'Total_Reviews_Millions'],
    barmode='group',
    title="Average Rating vs Total Reviews for Top 10 Categories",
    labels={
        'value': 'Average Rating / Total Reviews (Millions)',
        'Category': 'App Category'
    }
)
fig.update_layout(xaxis_tickangle=-30)

ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)

if 15 <= current_time.hour < 17:
    st.plotly_chart(fig)
else:
    st.warning("Graph is available only between 3 PM and 5 PM IST.")








