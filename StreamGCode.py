# run with: streamlit run StreamGCode.py
import streamlit as st
import hydralit_components as hc
import lines
import circles
import spirals


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

            This app was made by [Colin Bousige](https://lmi.cnrs.fr/author/colin-bousige/). Contact me for support or to signal a bug.
            """
    }
)

# Menu definition
menu_data = [
    {'icon': "fas fa-crop-alt", 'label': "Lines"},
    {'icon': "fas fa-bullseye", 'label': "Circles"},
    {'icon': "fas fa-redo", 'label': "Spirals"},
]

over_theme = {'txc_inactive': '#000','txc_active': '#fff', 
              'menu_background': '#fff', 'option_active':'#000'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='About',
    hide_streamlit_markers=False,
    sticky_nav=True,
    use_animation=False,
    sticky_mode='jumpy'
)

if menu_id == "About":
    st.write("Hello")

if menu_id == "Lines":
    lines.app()

if menu_id == "Circles":
    circles.app()

if menu_id == "Spirals":
    spirals.app()

