# run with: streamlit run GCode.py
import streamlit as st
from pathlib import Path
import uuid
import re

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

def create_st_button(link_text, link_url, hover_color="#6cf", st_col=None):
    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)
    button_css = f"""
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.8em;
                # position: relative;
                text-decoration: none;
                border-radius: 100px;
                border-width: 3px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
                position: absolute;
                top: 50%;
                left: 50%;
                -ms-transform: translate(-50%, -50%);
                transform: translate(-50%, -50%);
            }}
            #{button_id}:hover {{
                border-color: {hover_color};
                color: {hover_color};
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: {hover_color};
                color: white;
                }}
        </style> """
    html_str = f'<a href="{link_url}" id="{button_id}";>{link_text}</a><br></br>'
    if st_col is None:
        st.markdown(button_css + html_str, unsafe_allow_html=True)
    else:
        st_col.markdown(button_css + html_str, unsafe_allow_html=True)

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

create_st_button("About this app", "#about-this-app", st_col=st.sidebar)
create_st_button("Usage", "#usage", st_col=st.sidebar)
create_st_button("Support", "#support", st_col=st.sidebar)
create_st_button("How to cite", "#how-to-cite", st_col=st.sidebar)
create_st_button("License", "#license)", st_col=st.sidebar)
