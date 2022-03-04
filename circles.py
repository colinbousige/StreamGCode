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
    bt1, bt2 = st.columns(2)
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
    GP.XMIN = col1.number_input("X min:", value=50., step=1.)
    GP.XMAX = col2.number_input("X max:", value=350., step=1.)
    GP.YMIN = col1.number_input("Y min:", value=50., step=1.)
    GP.YMAX = col2.number_input("Y max:", value=350., step=1.)
    GP.CENTERX = (GP.XMAX + GP.XMIN)/2.
    GP.CENTERY = (GP.YMAX + GP.YMIN)/2.
    GP.DELTAX = GP.XMAX - GP.XMIN
    GP.DELTAY = GP.YMAX - GP.YMIN

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Definition of functions
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def circle(x_center, y_center, nbrpoints=10, diameter=50, Xstart=GP.CENTERX-1):
        global GP
        X = np.array([])
        Y = np.array([])
        angmax = theta0 = 0
        if Xstart < GP.CENTERX:
            theta0 = np.pi
        if nbrpoints > 1:
            angmax = (2*np.pi)/(nbrpoints-1)
        for i in range(nbrpoints):
            theta = theta0 + angmax*i
            newX = x_center + diameter/2. * np.cos(theta)
            newY = y_center + diameter/2. * np.sin(theta)
            X = np.append(X, newX)
            Y = np.append(Y, newY)
        return X, Y
    
    def circle_grid(x_center, y_center, pas=1, diameter=50, ncouche=1):
        global GP
        X = np.array([x_center - diameter/2])
        Y = np.array([y_center])
        theta0 = theta = 0
        i = 1
        while abs(float(np.cos(theta0) - pas/(diameter/2))) < 1:
            theta = np.arccos(float(np.cos(theta0) - pas/(diameter/2)))
            if i % 2 == 0:
                newX = x_center + diameter/2. * np.cos(np.pi-theta)
                newY = y_center + diameter/2. * np.sin(np.pi-theta)
                X = np.append(X, newX)
                Y = np.append(Y, newY)
                newX = x_center + diameter/2. * np.cos(np.pi+theta)
                newY = y_center + diameter/2. * np.sin(np.pi+theta)
                X = np.append(X, newX)
                Y = np.append(Y, newY)
            if i % 2 == 1:
                newX = x_center + diameter/2. * np.cos(np.pi+theta)
                newY = y_center + diameter/2. * np.sin(np.pi+theta)
                X = np.append(X, newX)
                Y = np.append(Y, newY)
                newX = x_center + diameter/2. * np.cos(np.pi-theta)
                newY = y_center + diameter/2. * np.sin(np.pi-theta)
                X = np.append(X, newX)
                Y = np.append(Y, newY)
            theta0 = theta
            i = i+1
        X = np.append(X, x_center + diameter/2)
        Y = np.append(Y, y_center)
        XX = X
        YY = Y
        if ncouche > 1:
            for j in range(1, ncouche):
                if j % 2 == 1:
                    XX = np.append(XX, np.flipud(X))
                    YY = np.append(YY, np.flipud(Y))
                if j % 2 == 0:
                    XX = np.append(XX, X)
                    YY = np.append(YY, Y)
        return XX, YY

    def update_GP_circle():
        """
        Update the global 'structure' object based on the defined parameters
        """
        global GP
        GP.ncoucheCircle = ncoucheCircle
        GP.ncoucheGrid = ncoucheGrid
        GP.diam = diam
        GP.delta = delta
        GP.pas = pas
        GP.NpointsCircle = NpointsCircle
        GP.Xstart = GP.CENTERX - GP.diam/2.
        GP.Ystart = GP.CENTERY - GP.diam/2.
        GP.X, GP.Y = [], []
        # la grille
        loopX, loopY = circle_grid(GP.CENTERX, GP.CENTERY,
                                   pas=GP.pas,
                                   diameter=(GP.diam - GP.delta),
                                   ncouche=GP.ncoucheGrid)
        GP.X.append(loopX)
        GP.Y.append(loopY)
        for j in range(GP.ncoucheCircle):  # le cercle
            loopX, loopY = circle(GP.CENTERX, GP.CENTERY,
                                  nbrpoints=GP.NpointsCircle,
                                  diameter=GP.diam,
                                  Xstart=GP.X[0][-1])
            GP.X.append(loopX)
            GP.Y.append(loopY)

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
        lc = LineCollection(segments, array=z, cmap=cmap,
                            norm=norm, linewidth=1.5, alpha=.8)
        f = Figure(figsize=(6, 4), dpi=150)
        f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        ax1 = f.add_subplot(1, 1, 1)
        ax1.add_collection(lc)
        ax1.plot([GP.XMIN, GP.XMAX, GP.XMAX, GP.XMIN, GP.XMIN],
                 [GP.YMIN, GP.YMIN, GP.YMAX, GP.YMAX, GP.YMIN], c='black', linewidth=3, zorder=1)
        ax1.axis('off')
        if zoom:
            ax1.set_xlim(x.min()-5, x.max()+5)
            ax1.set_ylim(y.min()-5, y.max()+5)
        else:
            ax1.set_xlim(GP.XMIN, GP.XMAX)
            ax1.set_ylim(GP.YMIN, GP.YMAX)
        ax1.set_aspect('equal', 'datalim')
        st.pyplot(f)

    def writeout():
        """
        Function to write GCODE file from a 'structure' object
        
        Returns a string
        """
        global GP
        update_GP_circle()
        GCODE = ""
        GCODE += f"; Circle diameter (mm) : {diam}\n"
        GCODE += f"; N points circle      : {NpointsCircle}\n"
        GCODE += f"; N layers circle      : {ncoucheCircle}\n"
        GCODE += f"; Spacing (mm)         : {delta}\n"
        GCODE += f"; Step grid (mm)       : {pas}\n"
        GCODE += f"; N layers grid        : {ncoucheGrid}\n"
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
        x, y = np.round(GP.X[0],4), np.round(GP.Y[0],4)
        GCODE += "\n\nG1 F33000 X"+str(x[0])+" Y"+str(y[0])+" ; Grid\n"
        for i in range(1,len(x)):
            GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
        GCODE += "\n"
        for couche in range(1,GP.ncoucheCircle+1):
            x, y = np.round(GP.X[couche],4), np.round(GP.Y[couche],4)
            GCODE += "G1 F33000 X"+str(x[0])+" Y"+str(y[0])+" ; Circle "+\
                     str(couche)+" / "+str(GP.ncoucheCircle)+"\n"
            for i in range(1,len(x)):
                GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
        return(GCODE)

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

    st.sidebar.write("## Other parameters")
    remote_voltage = st.sidebar.checkbox(
        'Remote voltage/current control', value=0)

    # # # # # # # # # # # # # # # # # # # # # # #
    # Main interface : plot and buttons
    # # # # # # # # # # # # # # # # # # # # # # #

    update_GP_circle()
    if 'zoom' not in st.session_state:
        st.session_state.zoom = 0
    if bt1.button("Zoom in/out"):
        st.session_state.zoom = (st.session_state.zoom + 1) % 2
    bt2.download_button('Download GCODE', writeout())
    plotstruct(GP, st.session_state.zoom)
