import streamlit as st

st.set_page_config(
    page_title="GitHub Peru Users Dashboard",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border: 1px solid #2e3450;
        border-radius: 12px;
        padding: 16px;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #c9d1d9;
        border-left: 4px solid #58a6ff;
        padding-left: 10px;
        margin: 24px 0 6px 0;
    }
    .desc-box {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.9rem;
        color: #8b949e;
        margin-bottom: 10px;
    }
    [data-testid="stSidebar"] {
        background: #161b22;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/9919?v=4", width=60)
    st.markdown("## 🇵🇪 GitHub Peru\n**User Analytics Dashboard**")
    st.markdown("---")
    st.markdown("Please select a page above to navigate the dashboard.")

st.markdown(
    "<h1 style='text-align:center; color:#58a6ff;'>🇵🇪 GitHub Peru Analytics</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#8b949e;'>Welcome to the modular GitHub Peru dashboard.</p>",
    unsafe_allow_html=True,
)

st.info("👈 Use the sidebar to navigate to specific sections!")
