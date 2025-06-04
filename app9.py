import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# Title
st.title("Group-009")

st.markdown("""
### Firearm Arrest Analysis in New Mexico (2018–2023)

This project analyzes firearm-related arrest data in **New Mexico** from **2018 to 2023**, based on records from the **FBI's NIBRS (National Incident-Based Reporting System)**.  
It provides a visual comparison of arrest trends **monthly and annually**, revealing a significant rise in arrests over time — possibly due to policy shifts or improved data collection methods.
""")

# Get current directory
current_dir = os.path.dirname(__file__)
file1 = os.path.join(current_dir, 'weapon_arrests_monthly.csv')
file2 = os.path.join(current_dir, 'weapon_arrests_summary.csv')
file3 = os.path.join(current_dir, 'weapon_arrests_monthly_averages.csv')

# Load CSV files
try:
    monthly_data = pd.read_csv(file1)
    summary_data = pd.read_csv(file2)
    monthly_averages = pd.read_csv(file3)

    # Filter by year range
    years = sorted(monthly_data['Year'].unique())
    year_range = st.select_slider("Select Year Range", options=years, value=(min(years), max(years)))
    filtered_data = monthly_data[(monthly_data['Year'] >= year_range[0]) & (monthly_data['Year'] <= year_range[1])]

    # Monthly trend plot
    st.subheader("Monthly Arrests with Moving Averages")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['Arrests'], name='Monthly Arrests', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['3_Month_Avg'], name='3-Month Avg', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['12_Month_Avg'], name='12-Month Avg', line=dict(dash='dot')))
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of Arrests', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # Year-over-Year line plot
    st.subheader("Year-over-Year Monthly Comparison")
    yoy_data = filtered_data.pivot(index='Month', columns='Year', values='Arrests')
    st.plotly_chart(px.line(yoy_data, title="Monthly Arrests by Year"), use_container_width=True)

    # Monthly averages bar chart
    st.subheader("Average Monthly Arrests (All Years)")
    st.plotly_chart(px.bar(monthly_averages, x='Month', y='Average_Arrests', error_y='Std_Dev', labels={'Average_Arrests': 'Avg Arrests'}), use_container_width=True)

    # Summary stats table
    st.subheader("Summary Statistics")
    st.dataframe(summary_data)

except Exception as e:
    st.error(f"Error loading data: {e}")
