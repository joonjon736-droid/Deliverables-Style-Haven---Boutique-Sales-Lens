import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Marketing Performance Dashboard", layout="wide")

# Load data
df = pd.read_csv("Data - Sheet1.csv")
df['Date'] = pd.to_datetime(df['Date'])

# KPI Calculations
df['ROAS'] = df['Revenue'] / df['Ad Spend']
df['CPA'] = df['Ad Spend'] / df['Conversions'].replace(0, None)

# Sidebar filters
st.sidebar.header("Filters")
channel = st.sidebar.multiselect("Channel", df['Channel'].unique(), df['Channel'].unique())
customer = st.sidebar.multiselect("Customer Type", df['Customer Type'].unique(), df['Customer Type'].unique())

filtered_df = df[
    (df['Channel'].isin(channel)) &
    (df['Customer Type'].isin(customer))
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.2f}")
col2.metric("Total Ad Spend", f"${filtered_df['Ad Spend'].sum():,.2f}")
col3.metric("Average ROAS", f"{filtered_df['ROAS'].mean():.2f}")

# Charts
st.subheader("Revenue by Channel")
fig, ax = plt.subplots()
filtered_df.groupby("Channel")['Revenue'].sum().plot(kind='bar', ax=ax)
st.pyplot(fig)

st.subheader("Revenue by Time of Day")
fig, ax = plt.subplots()
filtered_df.groupby("Time of Day")['Revenue'].sum().plot(kind='bar', ax=ax)
st.pyplot(fig)

st.subheader("Daily Revenue Trend")
daily = filtered_df.groupby("Date")['Revenue'].sum()
fig, ax = plt.subplots()
daily.plot(ax=ax)
st.pyplot(fig)
