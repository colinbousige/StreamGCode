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
            width: 700px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 700px;
            margin-left: -700px;
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
    def spiral(x_center, y_center, pas=1, diameter=50, ncouche=1, nbrpoints=100, fermi=0):
        global GP
        X = np.array([])
        Y = np.array([])
        Ntours = np.floor(diameter/(pas*2))
        d_theta = Ntours*(np.pi)/(nbrpoints-1)
        thetamax = d_theta*(nbrpoints-1)
        if fermi:
            step = -diameter/2/np.sqrt(thetamax)/np.cos(thetamax)
        else:
            step = -diameter/2/thetamax/np.cos(thetamax)
        for i in range(nbrpoints):
            theta = d_theta*i
            if fermi:
                newX = step*np.sqrt(theta) * np.cos(theta)
                newY = step*np.sqrt(theta) * np.sin(theta)
            else:
                newX = step*theta * np.cos(theta)
                newY = step*theta * np.sin(theta)
            X = np.append(X, newX)
            Y = np.append(Y, newY)
        X = np.flipud(X)
        Y = np.flipud(Y)
        X = np.append(X, -np.flipud(X))
        Y = np.append(Y, -np.flipud(Y))
        XX = X
        YY = Y
        if ncouche > 1:
            for i in range(ncouche-1):
                if i % 2 == 0:
                    XX = np.append(XX, np.flipud(X))
                    YY = np.append(YY, np.flipud(Y))
                else:
                    XX = np.append(XX, X)
                    YY = np.append(YY, Y)
        return XX + x_center, YY + y_center

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

    def update_GP_spiral():
        """
        Update the global 'structure' object based on the defined parameters
        """
        global GP
        GP.ncoucheCircle = ncoucheCircle_sp
        GP.ncoucheSpir = ncoucheSpir
        GP.diam = diamCircle_sp
        GP.delta = deltaCircle_sp
        GP.pas = pasSpir
        GP.NpointsCircle = NpointsCircle_sp
        GP.NptSpir = NptSpir
        GP.fermi = fermi
        GP.Xstart = GP.CENTERX - GP.diam/2.
        GP.Ystart = GP.CENTERY - GP.diam/2.
        GP.X, GP.Y = [], []
        # Spiral definition
        loopX, loopY = spiral(GP.CENTERX, GP.CENTERY,
                              pas=GP.pas,
                              diameter=(GP.diam - GP.delta),
                              ncouche=GP.ncoucheSpir,
                              nbrpoints=GP.NptSpir,
                              fermi=GP.fermi)
        GP.X.append(loopX)
        GP.Y.append(loopY)
        for j in range(GP.ncoucheCircle):  # The circle
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
        st.pyplot(f)


    def writeout():
        """
        Function to write GCODE file from a 'structure' object
        
        Returns a string
        """
        global GP
        update_GP_spiral()
        GCODE = ""
        GCODE += f"; Circle diameter (mm) : {diamCircle_sp}\n"
        GCODE += f"; N points circle      : {NpointsCircle_sp}\n"
        GCODE += f"; N layers circle      : {ncoucheCircle_sp}\n"
        GCODE += f"; Spiral step (mm)     : {pasSpir}\n"
        GCODE += f"; Delta diameters (mm) : {deltaCircle_sp}\n"
        GCODE += f"; N layerss spiral     : {ncoucheSpir}\n"
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
        x, y = np.round(GP.X[0], 4), np.round(GP.Y[0], 4)
        GCODE += "\n\nG1 F33000 X"+str(x[0])+" Y"+str(y[0])+" ; Spiral\n"
        for i in range(1, len(x)):
            GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
        GCODE += "\n"
        for couche in range(1, GP.ncoucheCircle+1):
            x, y = np.round(GP.X[couche], 4), np.round(GP.Y[couche], 4)
            GCODE += "G1 F33000 X"+str(x[0])+" Y"+str(y[0]) + \
                     " ; Circle "+str(couche)+" / "+str(GP.ncoucheCircle)+"\n"
            for i in range(1, len(x)):
                GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
            GCODE += "\n"
        return(GCODE)
        

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Definition of User Interface
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    st.sidebar.title("Spiral Parameters")
    col1, col2 = st.sidebar.columns(2)
    diamCircle_sp = col1.number_input("Outer circle diameter (mm):", value=200., step=1., min_value=0.)
    NpointsCircle_sp = col2.number_input("Number of points in the circle:", value=100, step=1, min_value=1)
    ncoucheCircle_sp = col1.number_input(
        "Number of layers in the outer circle:", value=1, step=1, min_value=0)
    pasSpir = col2.number_input("Spiral step:", value=10., step=1., min_value=0.)
    NptSpir = col1.number_input("Number of points in the spiral:", value=500, step=1, min_value=0)
    deltaCircle_sp = col2.number_input("Delta between spiral and outer circle (mm):", value=2., step=0.1, min_value=0.)
    ncoucheSpir = col1.number_input("Number of layers in the spiral (x2):", value=1, step=1, min_value=0)
    fermi = col2.checkbox("Fermi spiral?", value=False)

    st.sidebar.write("## Other parameters")
    remote_voltage = st.sidebar.checkbox(
        'Remote voltage/current control', value=0)

    # # # # # # # # # # # # # # # # # # # # # # # 
    # Main interface : plot and buttons
    # # # # # # # # # # # # # # # # # # # # # # #

    update_GP_spiral()
    if 'zoom' not in st.session_state:
        st.session_state.zoom = 0
    if bt1.button("Zoom in/out"):
        st.session_state.zoom = (st.session_state.zoom + 1) % 2
    bt2.download_button('Download GCODE', writeout())
    plotstruct(GP, st.session_state.zoom)
