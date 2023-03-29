import math
import streamlit as st
from ressources.Lines import *

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
# Definition of User Interface
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
st.sidebar.title("Definition of printing area")
col1, col2 = st.sidebar.columns(2)
XMIN = col1.number_input("X min:", value=50., step=1., key="lines_XMIN")
XMAX = col2.number_input("X max:", value=350., step=1., key="lines_XMAX")
YMIN = col1.number_input("Y min:", value=50., step=1., key="lines_YMIN")
YMAX = col2.number_input("Y max:", value=350., step=1., key="lines_YMAX")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

st.sidebar.title("Lines Parameters")
col1, col2 = st.sidebar.columns(2)
Nlayers = col1.number_input("Number of layers:", 1, 2000, 1)
Nsub = col2.number_input("Number of sub-layers:", 1, 20, 1)
Nrow = 2

st.sidebar.write("### Line length (mm)")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
length = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    length.append([float(x.number_input(f"Sublayer #{i+1+line*Nrow}", value=200., step=1., format="%.3f", key=f"length{i+line*Nrow}"))
            for i, x in enumerate(cols)])
length = [item for sublist in length for item in sublist]

st.sidebar.write("### Step (mm)")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
step = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    step.append([float(x.number_input(f"Sublayer #{i+1+line*Nrow}", value=10., step=1., format="%.3f", key=f"step{i+line*Nrow}"))
                for i, x in enumerate(cols)])
step = [item for sublist in step for item in sublist]

st.sidebar.write("### Number of lines per sublayer")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
Nline = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    Nline.append([int(x.number_input(f"Sublayer #{i+1+line*Nrow}", value=10, key=f"Nline{i+line*Nrow}"))
                for i, x in enumerate(cols)])
Nline = [item for sublist in Nline for item in sublist]

st.sidebar.write("### Angle")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
angle = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    angle.append([float(x.number_input(f"Sublayer #{i+1+line*Nrow}", value=(i+line*Nrow)*30., key=f"angle{i+line*Nrow}"))
                for i, x in enumerate(cols)])
angle = [item for sublist in angle for item in sublist]

st.sidebar.write("### Shift in X of each sublayer (mm)")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
shiftX = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    shiftX.append([float(x.number_input(f"Sublayer #{i+1+line*Nrow}", value=0., step=1., format="%.3f", key=f"shiftX{i+line*Nrow}"))
                for i, x in enumerate(cols)])
shiftX = [item for sublist in shiftX for item in sublist]

st.sidebar.write("### Shift in Y of each sublayer (mm)")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
shiftY = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    shiftY.append([float(x.number_input(f"Sublayer #{i+1+line*Nrow}", value=0., step=1., format="%.3f", key=f"shiftY{i+line*Nrow}"))
                for i, x in enumerate(cols)])
shiftY = [item for sublist in shiftY for item in sublist]

st.sidebar.write("### Miror image in X")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
mirrorX = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    mirrorX.append([x.checkbox(f"Sublayer #{i+1+line*Nrow}", value=0, key=f"mirrorX{i+line*Nrow}")
                    for i, x in enumerate(cols)])
mirrorX = [item for sublist in mirrorX for item in sublist]

st.sidebar.write("### Miror image in Y")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
mirrorY = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    mirrorY.append([x.checkbox(f"Sublayer #{i+1+line*Nrow}", value=0, key=f"mirrorY{i+line*Nrow}")
                for i, x in enumerate(cols)])
mirrorY = [item for sublist in mirrorY for item in sublist]

st.sidebar.write("### Inverse points order")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
reverse = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    reverse.append([x.checkbox(f"Sublayer #{i+1+line*Nrow}", value=0, key=f"reverse{i+line*Nrow}")
                    for i, x in enumerate(cols)])
reverse = [item for sublist in reverse for item in sublist]

st.sidebar.write("### Add a point to sublayer (X coordinates)")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
ADDX = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    ADDX.append([float(x.number_input(f"Sublayer #{i+1+line*Nrow}", value=0., step=1., format="%.3f", key=f"ADDX{i+line*Nrow}"))
                for i, x in enumerate(cols)])
ADDX = [item for sublist in ADDX for item in sublist]

st.sidebar.write("### Add a point to sublayer (Y coordinates)")
nlines = int(Nsub/Nrow) + math.ceil((Nsub % Nrow)/Nrow)
ADDY = []
for line in range(nlines):
    ncol = min(Nrow, Nsub-line*Nrow)
    cols = st.sidebar.columns(ncol)
    ADDY.append([float(x.number_input(f"Sublayer #{i+1+line*Nrow}", value=0., step=1., format="%.3f", key=f"ADDY{i+line*Nrow}"))
                for i, x in enumerate(cols)])
ADDY = [item for sublist in ADDY for item in sublist]

st.sidebar.write("### Shift of the whole pattern")
col1, col2 = st.sidebar.columns(2)
centershift = col1.number_input(
    "Shift X", value=0., step=1., format="%.3f"), col2.number_input("Shift Y", value=0., step=1., format="%.3f")

col1, col2 = st.sidebar.columns(2); cols = st.sidebar.columns(2)
st.sidebar.write("## Ending loops parameters")

col1, col2 = st.sidebar.columns(2)
loopdiameter = col1.number_input(
    "Diameter (mm)", value=10., step=1., format="%.3f",)
looppoints = col2.number_input("Number of points", value=0)
loopshiftX = col1.number_input(
    "Lateral shift (mm)", value=0., step=1., format="%.3f")
loopSkip = col2.number_input("Excluding angle", value=90)

col1, col2 = st.sidebar.columns(2); 
st.sidebar.write("## Add Text every N sublayer")
col1, col2 = st.sidebar.columns(2); 
text_to_add = st.sidebar.text_area("Text:", key="text_to_add")
Ntext_start = col1.number_input("N start", key="Ntext_start", step=1, value=1, min_value=1)
Ntext = col2.number_input("N", key="Ntext", step=1, value=1, min_value=1)

st.sidebar.write("## Other parameters")
remote_voltage = st.sidebar.checkbox(
    'Remote voltage/current control', value=0, key="lines_remote")

# # # # # # # # # # # # # # # # # # # # # # # 
# Main interface : plot and buttons
# # # # # # # # # # # # # # # # # # # # # # #
GP = Lines(Nlayers, angle,length,step,Nline,shiftX,
           shiftY,loopdiameter,looppoints,loopshiftX,loopSkip,Nsub,
           mirrorX,mirrorY,reverse,ADDX,ADDY,centershift, remote_voltage,
           text_to_add, Ntext_start,Ntext,plotarea,
           XMIN, XMAX, YMIN, YMAX)

if 'zoom' not in st.session_state:
    st.session_state.zoom = 0
if bt.button("Zoom in/out", key="lines_zoom"):
    st.session_state.zoom = (st.session_state.zoom + 1) % 2
bt.download_button('Download GCODE', GP.writeout(), key="lines_dwn")
GP.plotstruct(st.session_state.zoom)
