import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Developers | GitHub Peru", page_icon="🇵🇪", layout="wide")

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

st.title("👨‍💻 Top Developers")

users_only = df_raw[df_raw["type"] == "User"]

# CHART 1 — TOP 15 USERS BY FOLLOWERS
st.markdown("### Top 15 Users by Followers")
st.markdown(
    "This chart ranks the 15 most-followed individual GitHub users. Followers are a proxy for "
    "public recognition and community influence."
)

top_followers = (
    users_only.nlargest(15, "followers")[["login", "followers", "name", "bio"]]
    .sort_values("followers")
)
fig1 = px.bar(
    top_followers,
    x="followers", y="login",
    orientation="h",
    color="followers",
    color_continuous_scale="viridis",
    text="followers",
    hover_data={"name": True, "bio": True, "followers": True},
    labels={"followers": "Followers", "login": "Username"},
)
fig1.update_traces(textposition="outside")
fig1.update_layout(coloraxis_showscale=False, height=500, xaxis_title="Number of Followers", yaxis_title="")
st.plotly_chart(fig1, use_container_width=True)

# CHART 6 — HIREABLE STATUS
st.markdown("---")
st.markdown("### Hireable Status")
st.markdown("Indicates the percentage of individual users who have explicitly set their profile as **open to work**.")

hireable_series = (
    users_only["hireable"]
    .map({True: "Hireable", False: "Not Hireable"})
    .fillna("Not Specified")
    .value_counts().reset_index()
)
hireable_series.columns = ["status", "count"]
fig6 = px.pie(
    hireable_series, names="status", values="count",
    color_discrete_sequence=px.colors.qualitative.Set3,
    hole=0.45,
)
fig6.update_layout(height=400)
st.plotly_chart(fig6, use_container_width=True)
