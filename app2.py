import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# 1. Title and Introduction
st.title("Airbnb")
st.markdown("Airbnb Analysis. Julia Caballero.")

# 2. Load Data
df = pd.read_csv("/Users/juliacaballerogomez/Desktop/Guided Lab/airbnb.csv", encoding="utf-8")

# Sidebar Filters
st.sidebar.header("Filters")
neighbourhood_group = st.sidebar.multiselect("Select Neighbourhood Group", df["neighbourhood_group"].unique(), default=df["neighbourhood_group"].unique())
neighbourhood = st.sidebar.multiselect("Select Neighbourhood", df["neighbourhood"].unique(), default=df["neighbourhood"].unique())
room_type = st.sidebar.multiselect("Select Room Type", df["room_type"].unique(), default=df["room_type"].unique())

# Filtered Data
df_filtered = df[
    (df["neighbourhood_group"].isin(neighbourhood_group)) &
    (df["neighbourhood"].isin(neighbourhood)) &
    (df["room_type"].isin(room_type))
]

# Create Tabs
tab1, tab2 = st.tabs(["Overview", "Detailed Analysis"])

# Overview Tab
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Map of Listings")
        st.map(df_filtered.dropna(), latitude="latitude", longitude="longitude")
    
    with col2:
        st.subheader("Boxplot of Prices by Neighbourhood")
        fig_boxplot = px.box(df_filtered[df_filtered["price"] < 600], x="neighbourhood", y="price")
        st.plotly_chart(fig_boxplot)

    # Top Hosts
    df_host = df_filtered.groupby(["host_id", "host_name"]).size().reset_index()
    df_host["host"] = df_host["host_id"].astype(str) + "---" + df_host["host_name"]
    df_top10_host = df_host.sort_values(by=0, ascending=False).head(10)
    fig_host = px.bar(df_top10_host, x=0, y="host", orientation='h', hover_name="host_name")
    st.subheader("Top 10 Hosts")
    st.plotly_chart(fig_host)

# Detailed Analysis Tab
with tab2:
    st.subheader("Price Distribution by Listing Type")
    fig_price = px.box(df_filtered[df_filtered["price"] < 600], x="room_type", y="price")
    st.plotly_chart(fig_price)

    st.subheader("Listings with Most Reviews per Month")
    df_reviews = df_filtered.sort_values(by="reviews_per_month", ascending=False).head(10)
    fig_reviews = px.bar(df_reviews, x="reviews_per_month", y="name", orientation='h', title="Top Reviewed Listings")
    st.plotly_chart(fig_reviews)

    st.subheader("Relationship Between Reviews and Price")
    fig_scatter = px.scatter(df_filtered, x="number_of_reviews", y="price", color="room_type")
    st.plotly_chart(fig_scatter)

st.sidebar.text("Dashboard Created by Julia Caballero Gomez")
