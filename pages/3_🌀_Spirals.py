import streamlit as st
from ressources.Spirals import *


bt, plotarea = st.columns([1,6])
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
# Definition of User Interface
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

st.sidebar.title("Definition of printing area")
col1, col2 = st.sidebar.columns(2)
XMIN = col1.number_input("X min:", value=50., step=1., key="spir_XMIN")
XMAX = col2.number_input("X max:", value=350., step=1., key="spir_XMAX")
YMIN = col1.number_input("Y min:", value=50., step=1., key="spir_YMIN")
YMAX = col2.number_input("Y max:", value=350., step=1., key="spir_YMAX")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

st.sidebar.title("Spiral Parameters")
col1, col2 = st.sidebar.columns(2)
diamCircle = col1.number_input(
    "Outer circle diameter (mm):", value=200., step=1., min_value=0., key="spir_diamCircle_sp")
NpointsCircle = col2.number_input(
    "# of points in the circle:", value=100, step=1, min_value=1, key="spir_NpointsCircle_sp")
ncoucheCircle = col1.number_input(
    "# of layers in the outer circle:", value=1, step=1, min_value=0, key="spir_ncoucheCircle_sp")
pasSpir = col2.number_input("Spiral step:", value=10., step=1., min_value=0.)
NptSpir = col1.number_input("Number of points in the spiral:", value=500, step=1, min_value=0)
deltaCircle = col2.number_input("Delta between spiral and outer circle (mm):", value=2., step=0.1, min_value=0.)
ncoucheSpir = col1.number_input("# of layers in the spiral (x2):", value=1, step=1, min_value=0)
fermi = col2.checkbox("Fermi spiral?", value=False)

st.sidebar.write("## Other parameters")
remote_voltage = st.sidebar.checkbox(
    'Remote voltage/current control', value=0, key="spirals_remote")

# # # # # # # # # # # # # # # # # # # # # # # 
# Main interface : plot and buttons
# # # # # # # # # # # # # # # # # # # # # # #

GP = Spirals(ncoucheCircle,ncoucheSpir,diamCircle,deltaCircle,
             pasSpir,NpointsCircle,NptSpir,fermi, remote_voltage, 
             plotarea,XMIN, XMAX, YMIN, YMAX)

if 'zoom' not in st.session_state:
    st.session_state.zoom = 0
if bt.button("Zoom in/out", key="spirals_zoom"):
    st.session_state.zoom = (st.session_state.zoom + 1) % 2
bt.download_button('Download GCODE', GP.writeout(), key="download_spirals")
GP.plotstruct(st.session_state.zoom)
