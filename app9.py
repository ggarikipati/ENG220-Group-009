import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Title and Introduction
st.title("Group-009")

st.markdown("""
### Firearm Arrest Analysis in New Mexico (2018–2023)

This project analyzes firearm-related arrest data in **New Mexico** from **2018 to 2023**, based on records from the **FBI's NIBRS (National Incident-Based Reporting System)**.  
It provides visualizations of monthly and annual arrest trends, showing a significant increase over the years — potentially due to either policy shifts or improved data reporting.
""")

# Load CSVs from local path
current_dir = os.path.dirname(__file__)
file1 = os.path.join(current_dir, 'weapon_arrests_monthly.csv')
file2 = os.path.join(current_dir, 'weapon_arrests_summary.csv')
file3 = os.path.join(current_dir, 'weapon_arrests_monthly_averages.csv')

try:
    monthly_data = pd.read_csv(file1)
    summary_data = pd.read_csv(file2)
    monthly_avg = pd.read_csv(file3)

    # Year selection
    years = sorted(monthly_data['Year'].unique())
    selected_years = st.multiselect("Select Years", years, default=years)

    filtered_data = monthly_data[monthly_data['Year'].isin(selected_years)]

    # Monthly Trends
    st.subheader("Monthly Arrests with Moving Averages")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['Arrests'], name='Monthly Arrests', mode='lines+markers'))
    fig1.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['3_Month_Avg'], name='3-Month Avg', line=dict(dash='dash')))
    fig1.add_trace(go.Scatter(x=filtered_data['Year_Month'], y=filtered_data['12_Month_Avg'], name='12-Month Avg', line=dict(dash='dot')))
    fig1.update_layout(xaxis_title='Date', yaxis_title='Number of Arrests', hovermode='x unified')
    st.plotly_chart(fig1, use_container_width=True)

    # Year-over-Year Comparison
    st.subheader("Year-over-Year Comparison")
    yoy_data = filtered_data.pivot(index='Month', columns='Year', values='Arrests')
    fig2 = px.line(yoy_data, markers=True, title="Monthly Arrests by Year")
    fig2.update_layout(xaxis_title='Month', yaxis_title='Number of Arrests')
    st.plotly_chart(fig2, use_container_width=True)

    # Heatmap for YoY change
    yoy_pivot = filtered_data.pivot(index='Year', columns='Month', values='YoY_Change')
    fig3 = px.imshow(yoy_pivot, title='YoY Change Heatmap (%)', color_continuous_scale='RdYlBu')
    st.plotly_chart(fig3, use_container_width=True)

    # Monthly Averages
    st.subheader("Average Monthly Arrests (All Years)")
    fig4 = px.bar(monthly_avg, x='Month', y='Average_Arrests', error_y='Std_Dev',
                  labels={'Average_Arrests': 'Avg Arrests'}, title="Monthly Averages with Std Deviation")
    st.plotly_chart(fig4, use_container_width=True)

    # Summary Statistics
    st.subheader("Summary Statistics")
    st.dataframe(summary_data)

except Exception as e:
    st.error(f"""
        ❌ Error loading data: {e}

        Please ensure the following files exist in this folder:
        - weapon_arrests_monthly.csv
        - weapon_arrests_summary.csv
        - weapon_arrests_monthly_averages.csv
    """)
