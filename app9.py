import streamlit as st

st.set_page_config(
    page_title="Weapon Arrests Dashboard Book",
    page_icon="🚔",
    layout="wide",
)

st.title("🚔 Welcome to the Weapon Arrests Dashboard Book")

st.markdown(
    """
    This application contains interactive dashboards for **weapon-related arrest datasets (2018–2023)**.

    Use the **sidebar** to navigate between the following visualizations:

    - 📅 **Monthly Arrest Data** (Trends over time)
    - 📊 **Monthly Averages** (Seasonal patterns)
    - 📈 **Yearly Summary Statistics**

    Each dashboard allows you to:
    - Select columns for X and Y axes
    - Choose plot types (Line, Bar, Scatter, Pie)
    - Interactively explore the data
    """
)

st.info("Navigate using the left menu to begin exploring the datasets.")
