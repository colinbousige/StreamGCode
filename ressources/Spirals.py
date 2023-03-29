import numpy as np
# matplotlib: plot
import matplotlib.cm as cm
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from matplotlib.figure import Figure
# implement the default mpl key bindings
from matplotlib.collections import LineCollection

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Definition of global options
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class Spirals(object):
    def __init__(self, ncoucheCircle,ncoucheSpir,diamCircle,deltaCircle,
                 pasSpir,NpointsCircle,NptSpir,fermi, remote_voltage, 
                 plotarea,XMIN, XMAX, YMIN, YMAX):
        self.XMIN           = XMIN
        self.XMAX           = XMAX
        self.YMIN           = YMIN
        self.YMAX           = YMAX
        self.CENTERX        = (self.XMAX + self.XMIN)/2.
        self.CENTERY        = (self.YMAX + self.YMIN)/2.
        self.DELTAX         = self.XMAX - self.XMIN
        self.DELTAY         = self.YMAX - self.YMIN
        self.diamCircle     = diamCircle
        self.pasSpir        = pasSpir
        self.delta          = deltaCircle
        self.ncoucheSpir    = ncoucheSpir
        self.ncoucheCircle  = ncoucheCircle
        self.ncoucheSpir    = ncoucheSpir
        self.diam           = diamCircle
        self.pas            = pasSpir
        self.NpointsCircle  = NpointsCircle
        self.NptSpir        = NptSpir
        self.fermi          = fermi
        self.remote_voltage = remote_voltage
        self.plotarea       = plotarea
        self.update_GP()

    def spiral(self, x_center, y_center, pas=1, diameter=50, 
               ncouche=1, nbrpoints=100, fermi=0):
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

    def update_GP(self):
        """
        Update the global 'structure' object based on the defined parameters
        """
        self.Xstart = self.CENTERX - self.diam/2.
        self.Ystart = self.CENTERY - self.diam/2.
        self.X, self.Y = [], []
        # Spiral definition
        loopX, loopY = self.spiral(self.CENTERX, self.CENTERY,
                                pas=self.pas,
                                diameter=(self.diam - self.delta),
                                ncouche=self.ncoucheSpir,
                                nbrpoints=self.NptSpir,
                                fermi=self.fermi)
        self.X.append(loopX)
        self.Y.append(loopY)
        for j in range(self.ncoucheCircle):  # The circle
            loopX, loopY = self.circle(self.CENTERX, self.CENTERY,
                                    nbrpoints=self.NpointsCircle,
                                    diameter=self.diam,
                                    Xstart=self.X[0][-1])
            self.X.append(loopX)
            self.Y.append(loopY)

    def plotstruct(self, zoom=0):
        """
        Plots the defined 'structure' object, with option to zoom in or out
        """
        self.update_GP()
        cmap = cm.RdYlGn_r
        x, y = np.concatenate(self.X), np.concatenate(self.Y)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        norm = plt.Normalize(0.0, 1.0)
        z = np.asarray(np.linspace(0.0, 1.0, len(x)))
        lc = LineCollection(segments, array=z, cmap=cmap, norm=norm,linewidth=1.5, alpha=.8)
        f = Figure(figsize=(6, 4), dpi=150)
        f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        ax1 = f.add_subplot(1,1,1)
        ax1.add_collection(lc)
        ax1.plot([self.XMIN,self.XMAX,self.XMAX,self.XMIN,self.XMIN], 
                    [self.YMIN,self.YMIN,self.YMAX,self.YMAX,self.YMIN], c='black',linewidth=3, zorder=1)
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
        GCODE += f"; Circle diameter (mm) : {self.diamCircle}\n"
        GCODE += f"; N points circle      : {self.NpointsCircle}\n"
        GCODE += f"; N layers circle      : {self.ncoucheCircle}\n"
        GCODE += f"; Spiral step (mm)     : {self.pasSpir}\n"
        GCODE += f"; Delta diameters (mm) : {self.delta}\n"
        GCODE += f"; N layerss spiral     : {self.ncoucheSpir}\n"
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
        x, y = np.round(self.X[0], 4), np.round(self.Y[0], 4)
        GCODE += "\n\nG1 F33000 X"+str(x[0])+" Y"+str(y[0])+" ; Spiral\n"
        for i in range(1, len(x)):
            GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
        GCODE += "\n"
        for couche in range(1, self.ncoucheCircle+1):
            x, y = np.round(self.X[couche], 4), np.round(self.Y[couche], 4)
            GCODE += "G1 F33000 X"+str(x[0])+" Y"+str(y[0]) + \
                        " ; Circle "+str(couche)+" / "+str(self.ncoucheCircle)+"\n"
            for i in range(1, len(x)):
                GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
            GCODE += "\n"
        return(GCODE)
        
