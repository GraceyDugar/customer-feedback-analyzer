import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RapidNative Feedback Insights", layout="wide")

df = pd.read_csv("data/analyzed_feedback.csv")

st.title("Customer Feedback Insights")
st.caption("Sentiment and theme analysis pipeline — built for RapidNative")

# Top-line metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total feedback analyzed", len(df))
col2.metric("Negative sentiment", (df["sentiment"].str.upper() == "NEGATIVE").sum())
col3.metric("Positive sentiment", (df["sentiment"].str.upper() == "POSITIVE").sum())

st.divider()

# Theme volume chart
theme_counts = df["theme"].value_counts().reset_index()
theme_counts.columns = ["theme", "count"]
fig1 = px.bar(theme_counts, x="theme", y="count", title="Feedback Volume by Theme")
st.plotly_chart(fig1, use_container_width=True)

# Negative sentiment by theme — the priority view
neg_df = df[df["sentiment"].str.upper() == "NEGATIVE"]
neg_counts = neg_df["theme"].value_counts().reset_index()
neg_counts.columns = ["theme", "negative_count"]
fig2 = px.bar(neg_counts, x="theme", y="negative_count",
              title="Negative Sentiment by Theme (Priority Signal)",
              color="negative_count", color_continuous_scale="Reds")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Filterable raw data table — lets a viewer explore themselves
st.subheader("Explore the feedback")
selected_theme = st.selectbox("Filter by theme", ["All"] + sorted(df["theme"].unique().tolist()))
if selected_theme != "All":
    st.dataframe(df[df["theme"] == selected_theme][["text", "sentiment", "theme"]])
else:
    st.dataframe(df[["text", "sentiment", "theme"]])

st.caption("Note: current dataset is a synthetic sample modeled on real RapidNative user-testing themes, since public review volume was too sparse to sample directly.")