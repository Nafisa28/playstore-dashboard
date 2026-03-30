import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import pytz

# Load dataset
df = pd.read_csv("/data/play_store_data.csv")

# Title
st.title("Task 6: Dual Axis Chart - Installs vs Revenue (Free vs Paid)")



# Data Cleaning
df['Installs'] = df['Installs'].str.replace('+', '', regex=False)
df['Installs'] = df['Installs'].str.replace(',', '', regex=False)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

df['Price'] = df['Price'].str.replace('$', '', regex=False)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

df['Size'] = df['Size'].str.replace('M', '', regex=False)
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')

df['Android Ver'] = df['Android Ver'].str.replace(' and up', '', regex=False)
df['Android Ver'] = pd.to_numeric(df['Android Ver'], errors='coerce')

# Revenue column
df['Revenue'] = df['Installs'] * df['Price']

# App name length
df['App_Name_Length'] = df['App'].str.len()

filtered_df = df[
    (df['Installs'] >= 10000) &
    (df['Revenue'] >= 10000) &
    (df['Android Ver'] > 4.0) &
    (df['Size'] > 15) &
    (df['Content Rating'] == 'Everyone') &
    (df['App'].str.len() <= 30)
]

st.subheader("Filtered Dataset")
st.dataframe(filtered_df)

category_installs = filtered_df.groupby('Category')['Installs'].sum()

top3_categories = category_installs.sort_values(ascending=False).head(3)

st.subheader("Top 3 Categories")
st.dataframe(top3_categories)

top3_df = df[df['Category'].isin(top3_categories.index)]

final_table = top3_df.groupby(['Category', 'Type']).agg(
    Avg_Installs=('Installs', 'mean'),
    Total_Revenue=('Revenue', 'sum')
).reset_index()
final_table = final_table.sort_values(['Category', 'Type'])

st.subheader("Final Aggregated Table")
st.dataframe(final_table)


fig = go.Figure()

# Average Installs
fig.add_bar(
    x=final_table['Category'] + " - " + final_table['Type'],
    y=final_table['Avg_Installs'],
    name='Average Installs',
    yaxis='y1'
)

# Revenue
fig.add_bar(
    x=final_table['Category'] + " - " + final_table['Type'],
    y=final_table['Total_Revenue'],
    name='Revenue',
    yaxis='y2'
)

fig.update_layout(
    title="Average Installs vs Revenue (Free vs Paid Apps)",
    xaxis=dict(title="Category - App Type"),
    yaxis=dict(title="Average Installs", side='left'),
    yaxis2=dict(title="Revenue", overlaying='y', side='right'),
    barmode='group'
)


ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)

if 13 <= current_time.hour < 14:
    st.plotly_chart(fig)
else:
    st.warning("Graph available only between 1 PM and 2 PM IST")
