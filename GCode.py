# run with: streamlit run GCode.py
import streamlit as st
from multipage import MultiPage
from pages import about, lines, circles, spirals

app = MultiPage()

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

app.add_page("About", about.app)
app.add_page("Lines", lines.app)
app.add_page("Circles", circles.app)
app.add_page("Spirals", spirals.app)

app.run()
