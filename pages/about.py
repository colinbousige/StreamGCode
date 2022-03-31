import streamlit as st
from pathlib import Path

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


def app():
    about_markdown = read_markdown_file("pages/about.md")
    st.markdown(about_markdown, unsafe_allow_html=True)
    st.sidebar.write("""
    - [About this app](#about-this-app)
    - [Usage](#usage)
    - [Support](#support)
    - [How to cite](#how-to-cite)
    - [License](#license)""")
