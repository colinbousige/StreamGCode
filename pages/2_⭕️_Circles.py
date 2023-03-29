import streamlit as st
import numpy as np
from ressources.Circles import *

bt, plotarea = st.columns([1, 6])
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Definition of global options
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
st.sidebar.title("Definition of printing area")
col1, col2 = st.sidebar.columns(2)
XMIN = col1.number_input("X min:", value=50., step=1., key="circ_XMIN")
XMAX = col2.number_input("X max:", value=350., step=1., key="circ_XMAX")
YMIN = col1.number_input("Y min:", value=50., step=1., key="circ_YMIN")
YMAX = col2.number_input("Y max:", value=350., step=1., key="circ_YMAX")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Definition of User Interface
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

st.sidebar.title("Circle Parameters")
col1, col2 = st.sidebar.columns(2)
diam = col1.number_input(
    "Outer circle diameter (mm):", value=200., step=1., min_value=0.)
NpointsCircle = col2.number_input(
    "# of points in the circle:", value=100, step=1, min_value=1)
ncoucheCircle = col1.number_input(
    "Number of layers in the outer circle:", value=1, step=1, min_value=0)
ncoucheGrid = col2.number_input(
    "Number of layers in the inner grid:", value=1, step=1, min_value=0)
pas = col1.number_input(
    "Step between lines in the grid (mm):", value=5., step=1., min_value=0.)
delta = col2.number_input(
    "Spacing between outer circle and grid (mm):", value=20., step=0.1, min_value=0.)
angle = col1.number_input(
    "Rotation of the grid:", value=0., step=0.1, min_value=0.)

st.sidebar.write("## Other parameters")
remote_voltage = st.sidebar.checkbox(
    'Remote voltage/current control', value=0, key="circle_remote_voltage")

# # # # # # # # # # # # # # # # # # # # # # #
# Main interface : plot and buttons
# # # # # # # # # # # # # # # # # # # # # # #
GP = Circles(ncoucheCircle,ncoucheGrid,diam,delta,pas,angle,
             NpointsCircle,remote_voltage, plotarea, XMIN, XMAX, YMIN, YMAX)
GP.update_GP()
if 'zoom' not in st.session_state:
    st.session_state.zoom = 0
if bt.button("Zoom in/out", key="circles_zoom"):
    st.session_state.zoom = (st.session_state.zoom + 1) % 2
bt.download_button('Download GCODE', GP.writeout(), key="circles_download")
GP.plotstruct(st.session_state.zoom)
