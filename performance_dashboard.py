import streamlit as st
import json
import pandas as pd
import altair as alt

RESULTS_PATH = "evaluation/results.json"

st.set_page_config(page_title="RAG Evaluation Dashboard", layout="wide")

st.title("📊 RAG System Performance Dashboard")

# Load data
try:
    with open(RESULTS_PATH, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("⚠ No results found. Run `rag_eval_lite.py` first.")
    st.stop()

df = pd.DataFrame(data)

# Summary metrics
st.subheader("📌 System Summary Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Avg Score", f"{df['final_score'].mean():.2f} / 1.0")
col2.metric("Avg Latency", f"{df['total_latency_seconds'].mean():.2f} sec")
col3.metric("Worst Latency", f"{df['total_latency_seconds'].max():.2f} sec")

# Line chart: latency trend
st.subheader("📈 Latency Trend Over Queries")

latency_chart = (
    alt.Chart(df.reset_index())
    .mark_line(point=True)
    .encode(
        x="index",
        y="total_latency_seconds",
        tooltip=["query", "total_latency_seconds"],
    )
)
st.altair_chart(latency_chart, use_container_width=True)

# Score distribution
st.subheader("🎯 Score Distribution")

score_chart = (
    alt.Chart(df.reset_index())
    .mark_bar()
    .encode(
        x="final_score:Q",
        y="count()",
        tooltip=["count()", "final_score"]
    )
)
st.altair_chart(score_chart, use_container_width=True)

# Raw table
st.subheader("📄 Raw Evaluation Log")
st.dataframe(df)