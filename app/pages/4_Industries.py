import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Industries | GitHub Peru", page_icon="🇵🇪", layout="wide")

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "users.csv")
    try:
        return pd.read_csv(path, low_memory=False)
    except FileNotFoundError:
        return pd.DataFrame()

df_raw = load_data()
if df_raw.empty:
    st.warning("Data not found.")
    st.stop()
    
st.title("🏢 Industries & Companies")

# CHART 2 — ACCOUNT TYPES (User vs Org)
st.markdown("### Account Type Breakdown")
st.markdown(
    "Shows the proportion of individual **User** accounts vs **Organization** accounts. "
    "Organizations in Peru include tech companies, universities, open-source collectives, "
    "and bootcamps that maintain public code repositories."
)

type_counts = df_raw["type"].value_counts().reset_index()
type_counts.columns = ["type", "count"]
fig2 = px.pie(
    type_counts, names="type", values="count",
    color_discrete_sequence=px.colors.qualitative.Set2,
    hole=0.45,
)
fig2.update_layout(height=400)
st.plotly_chart(fig2, use_container_width=True)


# CHART 4 — TOP 15 COMPANIES
st.markdown("---")
st.markdown("### Top 15 Companies Represented")
st.markdown(
    "Lists the most frequently mentioned employers among GitHub users in Peru. "
    "This data comes from the optional `company` profile field."
)

companies = (
    df_raw["company"].dropna()
    .str.strip().str.lstrip("@").str.title()
    .replace("", pd.NA).dropna()
)
top_companies = companies.value_counts().head(15).sort_values().reset_index()
top_companies.columns = ["company", "count"]

fig4 = px.bar(
    top_companies, x="count", y="company",
    orientation="h",
    color="count", color_continuous_scale="magma",
    text="count",
    labels={"count": "Users", "company": "Company"},
)
fig4.update_traces(textposition="outside")
fig4.update_layout(coloraxis_showscale=False, height=500, xaxis_title="Number of Users", yaxis_title="")
st.plotly_chart(fig4, use_container_width=True)
