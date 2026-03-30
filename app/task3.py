import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pytz
from datetime import datetime
import os

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "../data/play_store_data.csv")
df = pd.read_csv(data_path)
st.title("Task 3 - Time Series Analysis")


st.subheader("Dataset Preview")
st.dataframe(df.head(10))


# Remove '+' and ',' from Installs
df['Installs'] = df['Installs'].str.replace('+', '', regex=False)
df['Installs'] = df['Installs'].str.replace(',', '', regex=False)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

# Convert Reviews to numeric
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

# Convert Date
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')


task3_df = df.copy()

# Reviews > 500
task3_df = task3_df[task3_df['Reviews'] > 500]

# App name should NOT start with x, y, z
task3_df = task3_df[
    ~task3_df['App'].str.lower().str.startswith(('x', 'y', 'z'), na=False)
]

# App name should NOT contain letter 'S'
task3_df = task3_df[
    ~task3_df['App'].str.contains('s', case=False, na=False)
]

# Category should start with E, C, B
task3_df = task3_df[
    task3_df['Category'].str.upper().str.startswith(('E','C','B','D'), na=False)
]
st.write(task3_df['Category'].unique())

st.subheader("Filtered Dataset (After All Conditions)")
st.dataframe(task3_df.head(10))

category_translation = {
    "BEAUTY": "सौंदर्य",      # Hindi
    "BUSINESS": "வணிகம்",    # Tamil
    "DATING": "Partnersuche"  # German
}

task3_df["Category_Display"] = task3_df["Category"].map(
    lambda x: category_translation.get(x, x)
)

task3_df['Last Updated'] = pd.to_datetime(task3_df['Last Updated'])
task3_df['Month'] = task3_df['Last Updated'].dt.to_period('M')
task3_df['Month'] = task3_df['Month'].dt.start_time

monthly_installs = task3_df.groupby(
    ['Month', 'Category_Display']
)['Installs'].sum().reset_index()

monthly_installs = monthly_installs.sort_values('Month')


st.subheader("Monthly Install Summary (After All Conditions)")
st.dataframe(monthly_installs)

monthly_installs["Growth"] = monthly_installs.groupby(
    "Category_Display"
)["Installs"].pct_change()

high_growth = monthly_installs[monthly_installs["Growth"] > 0.20]

st.subheader("High Growth Months (>20%)")
st.dataframe(high_growth)

ist = pytz.timezone("Asia/Kolkata")
current_hour = datetime.now(ist).hour

import plotly.graph_objects as go

if 18 <= current_hour < 21:

    fig = go.Figure()

    for category in monthly_installs['Category_Display'].unique():

        cat_data = monthly_installs[
            monthly_installs['Category_Display'] == category
        ].sort_values('Month')

        # Calculate growth
        cat_data['Growth'] = cat_data['Installs'].pct_change()

        # Add main line
        fig.add_trace(go.Scatter(
    x=cat_data['Month'],
    y=cat_data['Installs'],
    mode='lines+markers',
    name=category,
    line=dict(width=2),
    marker=dict(size=6),
    opacity=0.8
))
        # Highlight >20% growth
        high_growth = cat_data[cat_data['Growth'] > 0.20]

        fig.add_trace(go.Scatter(
            x=high_growth['Month'],
            y=high_growth['Installs'],
            mode='markers',
            marker=dict(size=9),
            name=f"{category} (>20% Growth)",
            showlegend=False
        ))

    fig.update_layout(
    title="Total Installs Over Time",
    xaxis_title="Month",
    yaxis_title="Total Installs (Log Scale)",
    hovermode="x unified",
    template="plotly_white",
    yaxis=dict(type="log"),
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
)
)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("This graph is only visible between 6 PM and 9 PM IST.")
