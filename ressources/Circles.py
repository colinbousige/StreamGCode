import streamlit as st
import numpy as np
# matplotlib: plot
import matplotlib.cm as cm
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from matplotlib.figure import Figure
# implement the default mpl key bindings
from matplotlib.collections import LineCollection


class Circles(object):

    def __init__(self,ncoucheCircle,ncoucheGrid,diam,delta,pas,angle,
                 NpointsCircle,remote_voltage, plotarea, XMIN, XMAX, YMIN, YMAX):
        self.ncoucheCircle  = ncoucheCircle
        self.ncoucheGrid    = ncoucheGrid
        self.diam           = diam
        self.delta          = delta
        self.pas            = pas
        self.angle          = angle
        self.plotarea       = plotarea
        self.remote_voltage = remote_voltage
        self.NpointsCircle  = NpointsCircle
        self.XMIN           = XMIN
        self.XMAX           = XMAX
        self.YMIN           = YMIN
        self.YMAX           = YMAX
        self.CENTERX        = (self.XMAX + self.XMIN)/2.
        self.CENTERY        = (self.YMAX + self.YMIN)/2.
        self.DELTAX         = self.XMAX - self.XMIN
        self.DELTAY         = self.YMAX - self.YMIN
        self.update_GP()


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Definition of functions
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def circle(self, x_center, y_center, nbrpoints=10, 
               diameter=50, Xstart=0):
        X = np.array([])
        Y = np.array([])
        angmax = theta0 = 0
        if Xstart < self.CENTERX:
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

    def circle_grid(self, x_center, y_center, pas=1, diameter=50, ncouche=1):
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

    def rotation(self, X, Y, theta):
        """
        Rotates X and Y coordinates from an angle theta
        """
        xx, yy = X - self.CENTERX, Y - self.CENTERY
        rotX = self.CENTERX + xx * \
            np.cos(theta*np.pi/180) + yy*np.sin(theta*np.pi/180)
        rotY = self.CENTERY - xx * \
            np.sin(theta*np.pi/180) + yy*np.cos(theta*np.pi/180)
        return rotX, rotY

    def update_GP(self):
        """
        Update the global 'structure' object based on the defined parameters
        """
        self.Xstart = self.CENTERX - self.diam/2.
        self.Ystart = self.CENTERY - self.diam/2.
        self.X, self.Y = [], []
        # la grille
        loopX, loopY = self.circle_grid(self.CENTERX, self.CENTERY,
                                    pas=self.pas,
                                    diameter=(self.diam - self.delta),
                                    ncouche=self.ncoucheGrid)
        self.X.append(loopX)
        self.Y.append(loopY)
        for j in range(self.ncoucheCircle):  # le cercle
            loopX, loopY = self.circle(self.CENTERX, self.CENTERY,
                                    nbrpoints=self.NpointsCircle,
                                    diameter=self.diam,
                                    Xstart=self.X[0][-1])
            self.X.append(loopX)
            self.Y.append(loopY)
        if(self.angle>0):
            for i in range(len(self.X)):
                self.X[i], self.Y[i] = self.rotation(self.X[i], self.Y[i], self.angle)

    def plotstruct(self, zoom=0):
        """
        Plots the define 'structure' object, with option to zoom in or out
        """
        self.update_GP()
        cmap = cm.RdYlGn_r
        x, y = np.concatenate(self.X), np.concatenate(self.Y)
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
        ax1.plot([self.XMIN, self.XMAX, self.XMAX, self.XMIN, self.XMIN],
                    [self.YMIN, self.YMIN, self.YMAX, self.YMAX, self.YMIN], c='black', linewidth=3, zorder=1)
        ax1.axis('off')
        if zoom:
            ax1.set_xlim(x.min()-5, x.max()+5)
            ax1.set_ylim(y.min()-5, y.max()+5)
        else:
            ax1.set_xlim(self.XMIN, self.XMAX)
            ax1.set_ylim(self.YMIN, self.YMAX)
        ax1.set_aspect('equal', 'datalim')
        self.plotarea.pyplot(f)

    def writeout(self):
        """
        Function to write GCODE file from a 'structure' object
        
        Returns a string
        """
        self.update_GP()
        GCODE = ""
        GCODE += f"; Circle diameter (mm) : {self.diam}\n"
        GCODE += f"; N points circle      : {self.NpointsCircle}\n"
        GCODE += f"; N layers circle      : {self.ncoucheCircle}\n"
        GCODE += f"; Spacing (mm)         : {self.delta}\n"
        GCODE += f"; Step grid (mm)       : {self.pas}\n"
        GCODE += f"; N layers grid        : {self.ncoucheGrid}\n"
        GCODE += "G21 ; set units to millimeters\n"
        GCODE += "M107\n"
        GCODE += "\n"
        GCODE += "\n"
        GCODE += "G90 ; use absolute coordinates\n"
        GCODE += "M107\n"
        if(self.remote_voltage):
            GCODE += "; Remote voltage/current control\n"
            GCODE += "M42 S255 P5\n"
            GCODE += "M42 S24 P4\n"
        GCODE += "\n"
        GCODE += "\n"
        GCODE += "; ----------------- End of GCODE init -----------------\n"
        GCODE += "\n"
        x, y = np.round(self.X[0],4), np.round(self.Y[0],4)
        GCODE += "\n\nG1 F33000 X"+str(x[0])+" Y"+str(y[0])+" ; Grid\n"
        for i in range(1,len(x)):
            GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
        GCODE += "\n"
        for couche in range(1,self.ncoucheCircle+1):
            x, y = np.round(self.X[couche],4), np.round(self.Y[couche],4)
            GCODE += "G1 F33000 X"+str(x[0])+" Y"+str(y[0])+" ; Circle "+\
                        str(couche)+" / "+str(self.ncoucheCircle)+"\n"
            for i in range(1,len(x)):
                GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
        return(GCODE)