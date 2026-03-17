import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config for individual pages just in case
st.set_page_config(page_title="Overview | GitHub Peru", page_icon="🇵🇪", layout="wide")

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "users.csv")
    try:
        df = pd.read_csv(path, low_memory=False)
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        df["join_year"] = df["created_at"].dt.year.astype("Int64")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df_raw = load_data()

st.title("Overview")

if df_raw.empty:
    st.warning("Data not found. Did you run the extraction script?")
    st.stop()
    
# Apply sidebar filters
with st.sidebar:
    st.markdown("**Filter by account type**")
    account_filter = st.multiselect(
        "Account type",
        options=["User", "Organization"],
        default=["User", "Organization"],
        label_visibility="collapsed",
    )
    st.markdown("**Minimum followers**")
    min_followers = st.slider("Min followers", 0, 500, 0, label_visibility="collapsed")

df = df_raw[
    df_raw["type"].isin(account_filter) &
    (df_raw["followers"] >= min_followers)
].copy()

# ── KPI METRICS ───────────────────────────────────────────────────────────────
users_only = df[df["type"] == "User"]

total_users  = len(df)
n_orgs       = (df["type"] == "Organization").sum()
avg_followers = int(users_only["followers"].mean()) if not users_only.empty else 0
hireable_pct = (
    round(users_only["hireable"].sum() / len(users_only) * 100, 1)
    if not users_only.empty else 0
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("👥 Total Records",      f"{total_users:,}")
k2.metric("🏢 Organizations",      f"{n_orgs:,}")
k3.metric("⭐ Avg Followers",       f"{avg_followers:,}")
k4.metric("💼 Hireable Users",      f"{hireable_pct}%")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 3 — NEW USERS BY JOIN YEAR
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### GitHub Account Creation by Year")
st.markdown(
    "Tracks how many users created their GitHub account each year. The steady rise reflects both "
    "GitHub's global growth and Peru's expanding developer ecosystem."
)
year_counts = df["join_year"].value_counts().sort_index().reset_index()
year_counts.columns = ["year", "count"]
year_counts = year_counts.dropna(subset=["year"])
year_counts["year"] = year_counts["year"].astype(str)

fig3 = px.bar(
    year_counts, x="year", y="count",
    color="count", color_continuous_scale="viridis",
    text="count",
    labels={"year": "Join Year", "count": "New Users"},
)
fig3.update_traces(textposition="outside")
fig3.update_layout(coloraxis_showscale=False, height=400)
st.plotly_chart(fig3, use_container_width=True)
