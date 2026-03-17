import streamlit as st

st.set_page_config(page_title="Languages | GitHub Peru", page_icon="🇵🇪", layout="wide")

st.title("💻 Programming Languages")

st.info(
    "This page will analyze the primary programming languages used by developers in Peru. "
    "**Data Collection Required**: We need to use `repo_extractor.py` to pull repository histories "
    "before populating this view."
)
