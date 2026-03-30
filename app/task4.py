import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pytz
from datetime import datetime
import os

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "../data/play_store_data.csv")
df = pd.read_csv(data_path)

st.title("Task 4 - Stacked Area Chart Analysis")

st.write("All unique categories in dataset:")
st.write(df['Category'].unique())

st.subheader("Dataset Preview")
st.dataframe(df.head())


# Clean Installs column
df['Installs'] = df['Installs'].str.replace('+', '', regex=False)
df['Installs'] = df['Installs'].str.replace(',', '', regex=False)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

# Convert Reviews to numeric
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

# Convert Rating to numeric
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Convert Date
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Convert Size to numeric MB
df['Size_MB'] = df['Size'].str.replace('M', '', regex=False)
df['Size_MB'] = pd.to_numeric(df['Size_MB'], errors='coerce')


filtered_df = df.copy()

# 1️⃣ Rating >= 4.2
filtered_df = filtered_df[filtered_df['Rating'] >= 4.2]

# 2️⃣ App name without numbers
filtered_df = filtered_df[
    ~filtered_df['App'].str.contains(r'\d', regex=True, na=False)
]

# 3️⃣ Category starts with T or P (strict check)
filtered_df = filtered_df[
    filtered_df['Category'].str.upper().str.startswith(('T', 'P'))
]

# 4️⃣ Reviews > 1000
filtered_df = filtered_df[filtered_df['Reviews'] > 1000]

# 5️⃣ Size between 20MB and 80MB
filtered_df = filtered_df[
    (filtered_df['Size_MB'] >= 20) &
    (filtered_df['Size_MB'] <= 80)
]
st.write("Unique categories after filtering:")
st.write(filtered_df['Category'].unique())

st.subheader("Filtered Dataset")
st.dataframe(filtered_df)
st.subheader("Apps Count by Category (After Filtering)")
st.dataframe(filtered_df['Category'].value_counts())

# Create Month column
filtered_df['Month'] = filtered_df['Last Updated'].dt.to_period('M')
filtered_df['Month'] = filtered_df['Month'].dt.start_time

# Group data
grouped = (
    filtered_df
    .groupby(['Month', 'Category'])['Installs']
    .sum()
    .reset_index()
)

grouped = grouped.sort_values('Month')
grouped['Cumulative_Installs'] = grouped.groupby('Category')['Installs'].cumsum()



fig4 = go.Figure()

categories = grouped['Category'].unique()

# Stacked area chart
for category in categories:

    cat_data = grouped[grouped['Category'] == category]

    display_name = (
"Voyage et Local" if category == "TRAVEL_AND_LOCAL" else
"Productividad" if category == "PRODUCTIVITY" else
"写真" if category == "PHOTOGRAPHY" else
category
)
    fig4.add_trace(go.Scatter(
        x=cat_data['Month'],
        y=cat_data['Cumulative_Installs'],
        mode='lines',
        stackgroup='one',
        name=display_name
    ))

# Growth markers
for category in categories:

    cat_data = grouped[grouped['Category'] == category].copy()

    cat_data['Growth'] = cat_data['Installs'].pct_change()

    high_growth = cat_data[cat_data['Growth'] > 0.25]

    fig4.add_trace(go.Scatter(
        x=high_growth['Month'],
        y=high_growth['Installs'],
        mode='markers',
        marker=dict(size=9),
        showlegend=False
    ))

    fig4.update_layout(
    title="Cumulative Installs by Category (Stacked Area Chart)",
    xaxis_title="Month",
    yaxis_title="Cumulative Installs",
    template="plotly_white",
    hovermode="x unified"
)

# Time restriction (4 PM – 6 PM IST)
ist = pytz.timezone("Asia/Kolkata")
current_hour = datetime.now(ist).hour

if 16 <= current_hour < 18:
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("This visualization is only visible between 4 PM and 6 PM IST.")
