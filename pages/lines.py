import math
import streamlit as st
import numpy as np
# matplotlib: plot
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
# implement the default mpl key bindings
from matplotlib.collections import LineCollection


def app():
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

    class structure(object):
        """
        Class defining a `structure`.
        """
        def __init__(self, name):
            self.name = name

    global GP
    GP = structure('')
    st.sidebar.title("Definition of printing area")
    col1, col2 = st.sidebar.columns(2)
    GP.XMIN = col1.number_input("X min:", value=50., step=1., key="lines_XMIN")
    GP.XMAX = col2.number_input("X max:", value=350., step=1., key="lines_XMAX")
    GP.YMIN = col1.number_input("Y min:", value=50., step=1., key="lines_YMIN")
    GP.YMAX = col2.number_input("Y max:", value=350., step=1., key="lines_YMAX")
    GP.CENTERX = (GP.XMAX + GP.XMIN)/2.
    GP.CENTERY = (GP.YMAX + GP.YMIN)/2.
    GP.DELTAX = GP.XMAX - GP.XMIN
    GP.DELTAY = GP.YMAX - GP.YMIN

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Definition of functions
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def rotation(X, Y, theta):
        """
        Rotates X and Y coordinates from an angle theta
        """
        global GP
        xx, yy = X - GP.CENTERX, Y - GP.CENTERY
        rotX = GP.CENTERX + xx*np.cos(theta*np.pi/180) + yy*np.sin(theta*np.pi/180)
        rotY = GP.CENTERY - xx*np.sin(theta*np.pi/180) + yy*np.cos(theta*np.pi/180)
        return rotX, rotY


    def endloop(x0, y0, x1, y1, nbrpoints=10, diameter=50, ang=10):
        """
        Creates a loop at the end of a line to connect 2 lines without sharp angles
        """
        global GP
        X = np.array([])
        Y = np.array([])
        if x0 > GP.CENTERX:  # right
            centX = x0 + diameter/2.
            rot = 1
            theta0 = np.pi
        else:  # left
            centX = x0 - diameter/2.
            rot = -1
            theta0 = 0
        centY = (y0+y1)/2.
        ang = ang*np.pi/180
        if nbrpoints > 1:
            angmax = (2*np.pi - 2*ang)/(nbrpoints-1)
        else:
            angmax = 0
        for i in range(nbrpoints):
            theta = theta0 + rot*ang + rot*angmax*i
            newX = centX + diameter/2. * np.cos(theta)
            newY = centY + diameter/2. * np.sin(theta)
            X = np.append(X, newX)
            Y = np.append(Y, newY)
        return X, Y


    def update_GP():
        """
        Update the global 'structure' object based on the defined parameters
        """
        global GP
        GP.couche = int(Nlayers)
        GP.angle = np.asarray(angle)
        GP.longueur = np.asarray(length)
        GP.pas = np.asarray(step)
        GP.Nbrelig = np.asarray(Nline)
        GP.shiftX = np.asarray(shiftX)
        GP.shiftY = np.asarray(shiftY)
        diameter = loopdiameter
        nbrpoints = looppoints
        shiftXloop = loopshiftX
        skipangleloop = loopSkip
        addX = np.asarray(ADDX)
        addY = np.asarray(ADDY)
        shiftXY = np.asarray(centershift)
        DY = GP.pas * (GP.Nbrelig - 1) / 2.
        GP.Xstart = GP.CENTERX - GP.longueur/2.
        GP.Ystart = GP.CENTERY - DY
        GP.X, GP.Y = [], []
        for j in range(Nsub):
            ligne = GP.Nbrelig[j]
            newX, newY = np.array([]), np.array([])
            for i in range(ligne):
                if i % 2 == 0:
                    x0, y0 = GP.Xstart[j], GP.Ystart[j] + i*GP.pas[j]
                    if i > 0:
                        loopX, loopY = endloop(
                            x1, y1, x0, y0, nbrpoints=nbrpoints, diameter=diameter, ang=skipangleloop)
                        rotloopX, rotloopY = rotation(
                            loopX - shiftXloop, loopY, GP.angle[j])
                        newX = np.append(newX, rotloopX+GP.shiftX[j])
                        newY = np.append(newY, rotloopY+GP.shiftY[j])
                    rotX, rotY = rotation(x0, y0, GP.angle[j])
                    newX = np.append(newX, rotX+GP.shiftX[j])
                    newY = np.append(newY, rotY+GP.shiftY[j])
                    x1, y1 = GP.Xstart[j] + \
                        GP.longueur[j], GP.Ystart[j] + i*GP.pas[j]
                    rotX, rotY = rotation(x1, y1, GP.angle[j])
                    newX = np.append(newX, rotX+GP.shiftX[j])
                    newY = np.append(newY, rotY+GP.shiftY[j])
                if i % 2 == 1:
                    x0, y0 = GP.Xstart[j] + \
                        GP.longueur[j], GP.Ystart[j] + i*GP.pas[j]
                    loopX, loopY = endloop(
                        x1, y1, x0, y0, nbrpoints=nbrpoints, diameter=diameter, ang=skipangleloop)
                    rotloopX, rotloopY = rotation(
                        loopX + shiftXloop, loopY, GP.angle[j])
                    newX = np.append(newX, rotloopX+GP.shiftX[j])
                    newY = np.append(newY, rotloopY+GP.shiftY[j])
                    rotX, rotY = rotation(x0, y0, GP.angle[j])
                    newX = np.append(newX, rotX+GP.shiftX[j])
                    newY = np.append(newY, rotY+GP.shiftY[j])
                    x1, y1 = GP.Xstart[j], GP.Ystart[j] + i*GP.pas[j]
                    rotX, rotY = rotation(x1, y1, GP.angle[j])
                    newX = np.append(newX, rotX+GP.shiftX[j])
                    newY = np.append(newY, rotY+GP.shiftY[j])
            newX = np.append(newX, newX[-1]+addX[j])
            newY = np.append(newY, newY[-1]+addY[j])
            GP.X.append(newX)
            GP.Y.append(newY)
            if mirrorX[j]:
                for i in range(len(GP.X[j])):
                    if GP.X[j][i] > GP.CENTERX+shiftX[j]:
                        GP.X[j][i] = GP.X[j][i] - 2 * np.abs(GP.X[j][i] - GP.CENTERX+shiftX[j])
                        continue
                    if GP.X[j][i] < GP.CENTERX+shiftX[j]:
                        GP.X[j][i] = GP.X[j][i] + 2 * np.abs(GP.X[j][i] - GP.CENTERX+shiftX[j])
            if mirrorY[j]:
                for i in range(len(GP.Y[j])):
                    if GP.Y[j][i] > GP.CENTERY+shiftY[j]:
                        GP.Y[j][i] = GP.Y[j][i] - 2 * np.abs(GP.Y[j][i] - GP.CENTERY+shiftY[j])
                        continue
                    if GP.Y[j][i] < GP.CENTERY+shiftY[j]:
                        GP.Y[j][i] = GP.Y[j][i] + 2 * np.abs(GP.Y[j][i] - GP.CENTERY+shiftY[j])
            if reverse[j]:
                GP.X[j] = np.flipud(GP.X[j])
                GP.Y[j] = np.flipud(GP.Y[j])
        GP.X = [GP.X[j] + shiftXY[0] for j in range(Nsub)]
        GP.Y = [GP.Y[j] + shiftXY[1] for j in range(Nsub)]


    def plotstruct(GP, zoom=0):
        """
        Plots the define 'structure' object, with option to zoom in or out
        """
        cmap = cm.RdYlGn_r
        x, y = np.concatenate(GP.X), np.concatenate(GP.Y)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        norm = plt.Normalize(0.0, 1.0)
        z = np.asarray(np.linspace(0.0, 1.0, len(x)))
        lc = LineCollection(segments, array=z, cmap=cmap, norm=norm,linewidth=1.5, alpha=.8)
        f = Figure(figsize=(6, 4), dpi=150)
        f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        ax1 = f.add_subplot(1,1,1)
        ax1.add_collection(lc)
        ax1.plot([GP.XMIN,GP.XMAX,GP.XMAX,GP.XMIN,GP.XMIN], 
                    [GP.YMIN,GP.YMIN,GP.YMAX,GP.YMAX,GP.YMIN], c='black',linewidth=3, zorder=1)
        ax1.axis('off')
        if zoom:
            ax1.set_xlim(x.min()-5, x.max()+5)
            ax1.set_ylim(y.min()-5, y.max()+5)
        else:
            ax1.set_xlim(GP.XMIN, GP.XMAX)
            ax1.set_ylim(GP.YMIN, GP.YMAX)
        ax1.set_aspect('equal', 'datalim')
        plotarea.pyplot(f)


    def writeout():
        """
        Function to write GCODE file from a 'structure' object
        
        Returns a string
        """
        global GP
        update_GP()
        GCODE = ""
        GCODE += "; Number of layers         : " +str(Nlayers)+"\n"
        GCODE += "; Number of sub-layers     : " +str(Nsub)+"\n"
        GCODE += "; Line length (mm)         : " +str(length)+"\n"
        GCODE += "; Step (mm)                : " +str(step)+"\n"
        GCODE += "; Number of lines          : " +str(Nline)+"\n"
        GCODE += "; Angle                    : " +str(angle)+"\n"
        GCODE += "; Shift X (mm)             : " +str(shiftX)+"\n"
        GCODE += "; Shift Y (mm)             : " +str(shiftY)+"\n"
        GCODE += "; Loop parameters          :\n"
        GCODE += "; Diameter                 : " +str(loopdiameter)+"\n"
        GCODE += "; Number of points         : " +str(looppoints)+"\n"
        GCODE += "; X shift                  : " +str(loopshiftX)+"\n"
        GCODE += "; Points exclusion angle   : " +str(loopSkip)+"\n"
        GCODE += "G21 ; set units to millimeters\n"
        GCODE += "M107\n"
        GCODE += "\n"
        GCODE += "\n"
        GCODE += "G90 ; use absolute coordinates\n"
        GCODE += "M107\n"
        if(remote_voltage):
            GCODE += "; Remote voltage/current control\n"
            GCODE += "M42 S255 P5\n"
            GCODE += "M42 S24 P4\n"
        GCODE += "\n"
        GCODE += "\n"
        GCODE += "; ----------------- End of GCODE init -----------------\n"
        GCODE += "\n"
        for couche in range(1, GP.couche+1):
            if len(text_to_add)>0:
                if couche >= Ntext_start:
                    if (couche-Ntext_start) % Ntext == 0:
                        GCODE += "; Additional text:\n"
                        GCODE += text_to_add+"\n"
            for souscouche in range(len(GP.X)):
                x, y = np.round(GP.X[souscouche], 4), np.round(GP.Y[souscouche], 4)
                GCODE += "G1 F33000 X"+str(x[0])+" Y"+str(y[0])+" ; Layer "+str(couche)+ \
                        "/"+str(GP.couche)+" - Sub Layer "+str(souscouche+1)+"/"+str(len(GP.X))+"\n"
                for i in range(1,len(x)):
                    GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
                GCODE += "\n"
        return(GCODE)
        

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Definition of User Interface
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

    update_GP()
    if 'zoom' not in st.session_state:
        st.session_state.zoom = 0
    if bt.button("Zoom in/out", key="lines_zoom"):
        st.session_state.zoom = (st.session_state.zoom + 1) % 2
    bt.download_button('Download GCODE', writeout(), key="lines_dwn")
    plotstruct(GP, st.session_state.zoom)
