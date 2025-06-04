# -*- coding: utf-8 -*-
# Group 009 - Firearm Arrests in New Mexico Dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set wide layout
st.set_page_config(layout="wide", page_title="Group-009")

# Title and intro
st.title("Group-009")

st.markdown("""
### Firearm-Related Arrests Analysis in New Mexico (2018–2023)

In this project, the objective is to **analyze firearm-related arrests** and compare them both **annually and monthly**, with a focus on the state of **New Mexico**.  
The data was sourced directly from the **Federal Bureau of Investigation (FBI)**.  

From our analysis, we observe that between **2018 and 2023**, gun-related arrests have increased significantly.  
This trend may reflect **policy failures**, or alternatively, **improvements in data reporting and collection** by law enforcement agencies.

---
""")

# Load data
@st.cache_data
def load_data():
    monthly_data = pd.read_csv("weapon_arrests_monthly.csv")
    summary_data = pd.read_csv("weapon_arrests_summary.csv")
    monthly_averages = pd.read_csv("weapon_arrests_monthly_averages.csv")
    return monthly_data, summary_data, monthly_averages

try:
    monthly_data, summary_data, monthly_averages = load_data()

    # Year slider
    years = sorted(monthly_data['Year'].unique())
    year_range = st.select_slider("Select Year Range", options=years, value=(min(years), max(years)))

    # Filter by selected years
    filtered_data = monthly_data[
        (monthly_data['Year'] >= year_range[0]) &
        (monthly_data['Year'] <= year_range[1])
    ]

    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Arrests", f"{filtered_data['Arrests'].sum():,.0f}")
    with col2:
        st.metric("Avg. Monthly Arrests", f"{filtered_data['Arrests'].mean():.1f}")
    with col3:
        st.metric("Avg. YoY Change", f"{filtered_data['YoY_Change'].mean():.1f}%")
    with col4:
        trend = "📈" if filtered_data['YoY_Change'].mean() > 0 else "📉"
        st.metric("Trend", trend)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Monthly Trends", 
        "Year-over-Year Comparison", 
        "Seasonal Patterns", 
        "Detailed Statistics"
    ])

    with tab1:
        st.subheader("Monthly Arrest Trends")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered_data['Year_Month'],
            y=filtered_data['Arrests'],
            mode='lines+markers',
            name="Monthly Arrests",
            line=dict(color="#1f77b4")
        ))
        fig.add_trace(go.Scatter(
            x=filtered_data['Year_Month'],
            y=filtered_data['3_Month_Avg'],
            name="3-Month Average",
            line=dict(color="#ff7f0e", dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=filtered_data['Year_Month'],
            y=filtered_data['12_Month_Avg'],
            name="12-Month Average",
            line=dict(color="#2ca02c", dash="dash")
        ))
        fig.update_layout(
            title="Monthly Arrests with Moving Averages",
            xaxis_title="Date",
            yaxis_title="Number of Arrests",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Year-over-Year Comparison")
        yoy_line = filtered_data.pivot(index="Month", columns="Year", values="Arrests")
        fig = px.line(
            yoy_line,
            title="Year-over-Year Comparison by Month",
            labels={"value": "Number of Arrests", "Month": "Month"}
        )
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        yoy_heatmap = filtered_data.pivot(index="Year", columns="Month", values="YoY_Change")
        fig_heat = px.imshow(
            yoy_heatmap,
            title="Year-over-Year Change Heatmap (%)",
            color_continuous_scale="RdYlBu"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with tab3:
        st.subheader("Seasonal Patterns")
        bar = px.bar(
            monthly_averages,
            x="Month",
            y="Average_Arrests",
            error_y="Std_Dev",
            title="Average Monthly Arrests (All Years)",
            labels={"Average_Arrests": "Average Number of Arrests"}
        )
        st.plotly_chart(bar, use_container_width=True)

        box = px.box(
            filtered_data,
            x="Month",
            y="Arrests",
            title="Monthly Distribution of Arrests",
            labels={"Arrests": "Number of Arrests"}
        )
        st.plotly_chart(box, use_container_width=True)

    with tab4:
        st.subheader("Detailed Statistics")
        st.dataframe(summary_data.style.format({
            'Total_Arrests': '{:,.0f}',
            'Average_Monthly_Arrests': '{:.1f}',
            'Max_Monthly_Arrests': '{:.0f}',
            'Min_Monthly_Arrests': '{:.0f}',
            'Standard_Deviation': '{:.1f}'
        }))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Monthly Averages")
            st.dataframe(monthly_averages.style.format({
                'Average_Arrests': '{:.1f}',
                'Std_Dev': '{:.1f}',
                'Min_Arrests': '{:.0f}',
                'Max_Arrests': '{:.0f}'
            }))

        with col2:
            st.subheader("Year-over-Year Changes")
            yearly_stats = filtered_data.groupby("Year")['Arrests'].agg(
                Total_Arrests='sum'
            ).reset_index()
            yearly_stats['YoY_Change'] = yearly_stats['Total_Arrests'].pct_change() * 100
            st.dataframe(yearly_stats.style.format({
                'Total_Arrests': '{:,.0f}',
                'YoY_Change': '{:.1f}%'
            }))

    # Footer
    st.markdown("---")
    st.markdown("""
    🔍 **Data Source**: FBI NIBRS (National Incident-Based Reporting System)  
    📅 **Last updated**: {}
    """.format(pd.Timestamp.now().strftime("%Y-%m-%d")))

except Exception as e:
    st.error(f"""
    ❌ Error loading data: {e}

    Please ensure the following files exist in the same folder as this script:
    - weapon_arrests_monthly.csv
    - weapon_arrests_summary.csv
    - weapon_arrests_monthly_averages.csv
    """)
