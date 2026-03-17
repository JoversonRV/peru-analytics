import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Repositories | GitHub Peru", page_icon="🇵🇪", layout="wide")

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
    
st.title("📁 Repositories & Activity")

users_only = df_raw[df_raw["type"] == "User"]

# CHART 5 — FOLLOWERS vs PUBLIC REPOS
st.markdown("### Followers vs Public Repositories (Top 300)")
st.markdown(
    "A scatter plot comparing number of followers vs number of public repositories. "
    "Users in the top-right corner have both a large following and a prolific repository history."
)

scatter_df = (
    users_only.nlargest(300, "followers")[["login", "name", "public_repos", "followers", "bio"]]
    .dropna(subset=["public_repos", "followers"])
)
fig5 = px.scatter(
    scatter_df,
    x="public_repos", y="followers",
    color="followers",
    color_continuous_scale="viridis",
    hover_name="login",
    hover_data={"name": True, "bio": True, "public_repos": True, "followers": True},
    size="followers",
    size_max=30,
    labels={"public_repos": "Public Repositories", "followers": "Followers"},
    opacity=0.8,
)
fig5.update_layout(coloraxis_showscale=False, height=500)
st.plotly_chart(fig5, use_container_width=True)


# CHART 7 — TOP 15 BY PUBLIC REPOS
st.markdown("---")
st.markdown("### Top 15 Users by Number of Public Repositories")
st.markdown(
    "Highlights users who have published the most public repositories. "
    "A high repo count can indicate an educator sharing course materials, a hobbyist experimenting "
    "with many projects, or a prolific open-source contributor."
)

top_repos = (
    users_only.nlargest(15, "public_repos")[["login", "public_repos", "name"]]
    .sort_values("public_repos")
)
fig7 = px.bar(
    top_repos,
    x="public_repos", y="login",
    orientation="h",
    color="public_repos", color_continuous_scale="teal",
    text="public_repos",
    hover_data={"name": True, "public_repos": True},
    labels={"public_repos": "Public Repos", "login": "Username"},
)
fig7.update_traces(textposition="outside")
fig7.update_layout(coloraxis_showscale=False, height=500, xaxis_title="Number of Public Repos", yaxis_title="")
st.plotly_chart(fig7, use_container_width=True)
