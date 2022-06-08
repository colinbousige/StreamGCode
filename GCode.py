# run with: streamlit run GCode.py
import streamlit as st
from pathlib import Path

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

st.set_page_config(
    page_title="Simple G-Code creator for precise Direct-writing",
    page_icon=":hammer_and_pick:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://lmi.cnrs.fr/author/colin-bousige/',
        'Report a bug': "https://lmi.cnrs.fr/author/colin-bousige/",
        'About': """
            ### Simple G-Code creator for precise Direct-writing
            Version date 2022-02-24.

            This app was made by [Colin Bousige](mailto:colin.bousige@cnrs.fr). Contact me for support or to signal a bug.
            """
    }
)

st.markdown(
    """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 400px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 400px;
            margin-left: -400px;
        }
        </style>
        """,
    unsafe_allow_html=True
)


about_markdown = read_markdown_file("pages/about.md")
st.markdown(about_markdown, unsafe_allow_html=True)
st.sidebar.write("""
### [About this app](#about-this-app)
### [Usage](#usage)
### [Support](#support)
### [How to cite](#how-to-cite)
### [License](#license)""")

