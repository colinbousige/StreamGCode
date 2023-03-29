import numpy as np
# matplotlib: plot
import matplotlib.cm as cm
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from matplotlib.figure import Figure
# implement the default mpl key bindings
from matplotlib.collections import LineCollection

class Lines(object):
    def __init__(self, Nlayers, angle,length,step,Nline,shiftX,shiftY,
                 loopdiameter,looppoints,loopshiftX,loopSkip,Nsub,mirrorX,
                 mirrorY,reverse,ADDX,ADDY,centershift, remote_voltage,
                 text_to_add, Ntext_start,Ntext,plotarea, XMIN, XMAX, YMIN, YMAX):
        self.Nlayers        = int(Nlayers)
        self.length         = length
        self.step           = step
        self.Nline          = Nline
        self.loopdiameter   = loopdiameter
        self.looppoints     = looppoints
        self.loopshiftX     = loopshiftX
        self.loopSkip       = loopSkip
        self.XMIN           = XMIN
        self.XMAX           = XMAX
        self.YMIN           = YMIN
        self.YMAX           = YMAX
        self.CENTERX        = (self.XMAX + self.XMIN)/2.
        self.CENTERY        = (self.YMAX + self.YMIN)/2.
        self.DELTAX         = self.XMAX - self.XMIN
        self.DELTAY         = self.YMAX - self.YMIN
        self.angle          = np.asarray(angle)
        self.longueur       = np.asarray(length)
        self.pas            = np.asarray(step)
        self.Nbrelig        = np.asarray(Nline)
        self.shiftX         = np.asarray(shiftX)
        self.shiftY         = np.asarray(shiftY)
        self.diameter       = loopdiameter
        self.nbrpoints      = looppoints
        self.shiftXloop     = loopshiftX
        self.skipangleloop  = loopSkip
        self.addX           = np.asarray(ADDX)
        self.addY           = np.asarray(ADDY)
        self.shiftXY        = np.asarray(centershift)
        self.Nsub           = int(Nsub)
        self.mirrorX        = mirrorX
        self.mirrorY        = mirrorY
        self.reverse        = reverse
        self.remote_voltage = remote_voltage
        self.text_to_add    = text_to_add
        self.Ntext_start    = Ntext_start
        self.Ntext          = Ntext
        self.plotarea       = plotarea
        self.update_GP()
        
    def rotation(self, X, Y, theta):
        """
        Rotates X and Y coordinates from an angle theta
        """
        xx, yy = X - self.CENTERX, Y - self.CENTERY
        rotX = self.CENTERX + xx*np.cos(theta*np.pi/180) + yy*np.sin(theta*np.pi/180)
        rotY = self.CENTERY - xx*np.sin(theta*np.pi/180) + yy*np.cos(theta*np.pi/180)
        return rotX, rotY


    def endloop(self, x0, y0, x1, y1, nbrpoints=10, diameter=50, ang=10):
        """
        Creates a loop at the end of a line to connect 2 lines without sharp angles
        """
        X = np.array([])
        Y = np.array([])
        if x0 > self.CENTERX:  # right
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


    def update_GP(self):
        """
        Update the global 'structure' object based on the defined parameters
        """
        DY = self.pas * (self.Nbrelig - 1) / 2.
        self.Xstart = self.CENTERX - self.longueur/2.
        self.Ystart = self.CENTERY - DY
        self.X, self.Y = [], []
        for j in range(self.Nsub):
            ligne = self.Nbrelig[j]
            newX, newY = np.array([]), np.array([])
            for i in range(ligne):
                if i % 2 == 0:
                    x0, y0 = self.Xstart[j], self.Ystart[j] + i*self.pas[j]
                    if i > 0:
                        loopX, loopY = self.endloop(
                            x1, y1, x0, y0, nbrpoints=self.nbrpoints, diameter=self.diameter, ang=self.skipangleloop)
                        rotloopX, rotloopY = self.rotation(
                            loopX - self.shiftXloop, loopY, self.angle[j])
                        newX = np.append(newX, rotloopX+self.shiftX[j])
                        newY = np.append(newY, rotloopY+self.shiftY[j])
                    rotX, rotY = self.rotation(x0, y0, self.angle[j])
                    newX = np.append(newX, rotX+self.shiftX[j])
                    newY = np.append(newY, rotY+self.shiftY[j])
                    x1, y1 = self.Xstart[j] + \
                        self.longueur[j], self.Ystart[j] + i*self.pas[j]
                    rotX, rotY = self.rotation(x1, y1, self.angle[j])
                    newX = np.append(newX, rotX+self.shiftX[j])
                    newY = np.append(newY, rotY+self.shiftY[j])
                if i % 2 == 1:
                    x0, y0 = self.Xstart[j] + \
                        self.longueur[j], self.Ystart[j] + i*self.pas[j]
                    loopX, loopY = self.endloop(
                        x1, y1, x0, y0, nbrpoints=self.nbrpoints, diameter=self.diameter, ang=self.skipangleloop)
                    rotloopX, rotloopY = self.rotation(
                        loopX + self.shiftXloop, loopY, self.angle[j])
                    newX = np.append(newX, rotloopX+self.shiftX[j])
                    newY = np.append(newY, rotloopY+self.shiftY[j])
                    rotX, rotY = self.rotation(x0, y0, self.angle[j])
                    newX = np.append(newX, rotX+self.shiftX[j])
                    newY = np.append(newY, rotY+self.shiftY[j])
                    x1, y1 = self.Xstart[j], self.Ystart[j] + i*self.pas[j]
                    rotX, rotY = self.rotation(x1, y1, self.angle[j])
                    newX = np.append(newX, rotX+self.shiftX[j])
                    newY = np.append(newY, rotY+self.shiftY[j])
            newX = np.append(newX, newX[-1]+self.addX[j])
            newY = np.append(newY, newY[-1]+self.addY[j])
            self.X.append(newX)
            self.Y.append(newY)
            if self.mirrorX[j]:
                for i in range(len(self.X[j])):
                    if self.X[j][i] > self.CENTERX+self.shiftX[j]:
                        self.X[j][i] = self.X[j][i] - 2 * np.abs(self.X[j][i] - self.CENTERX+self.shiftX[j])
                        continue
                    if self.X[j][i] < self.CENTERX+self.shiftX[j]:
                        self.X[j][i] = self.X[j][i] + 2 * np.abs(self.X[j][i] - self.CENTERX+self.shiftX[j])
            if self.mirrorY[j]:
                for i in range(len(self.Y[j])):
                    if self.Y[j][i] > self.CENTERY+self.shiftY[j]:
                        self.Y[j][i] = self.Y[j][i] - 2 * np.abs(self.Y[j][i] - self.CENTERY+self.shiftY[j])
                        continue
                    if self.Y[j][i] < self.CENTERY+self.shiftY[j]:
                        self.Y[j][i] = self.Y[j][i] + 2 * np.abs(self.Y[j][i] - self.CENTERY+self.shiftY[j])
            if self.reverse[j]:
                self.X[j] = np.flipud(self.X[j])
                self.Y[j] = np.flipud(self.Y[j])
        self.X = [self.X[j] + self.shiftXY[0] for j in range(self.Nsub)]
        self.Y = [self.Y[j] + self.shiftXY[1] for j in range(self.Nsub)]


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
        GCODE += f"; Number of layers         : {self.Nlayers}\n"
        GCODE += f"; Number of sub-layers     : {self.Nsub}\n"
        GCODE += f"; Line length (mm)         : {self.length}\n"
        GCODE += f"; Step (mm)                : {self.step}\n"
        GCODE += f"; Number of lines          : {self.Nline}\n"
        GCODE += f"; Angle                    : {self.angle}\n"
        GCODE += f"; Shift X (mm)             : {self.shiftX}\n"
        GCODE += f"; Shift Y (mm)             : {self.shiftY}\n"
        GCODE += "; Loop parameters          :\n"
        GCODE += f"; Diameter                 : {self.loopdiameter}\n"
        GCODE += f"; Number of points         : {self.looppoints}\n"
        GCODE += f"; X shift                  : {self.loopshiftX}\n"
        GCODE += f"; Points exclusion angle   : {self.loopSkip}\n"
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
        for couche in range(1, self.Nlayers+1):
            if len(self.text_to_add)>0:
                if couche >= self.Ntext_start:
                    if (couche-self.Ntext_start) % self.Ntext == 0:
                        GCODE += "; Additional text:\n"
                        GCODE += self.text_to_add+"\n"
            for souscouche in range(len(self.X)):
                x, y = np.round(self.X[souscouche], 4), np.round(self.Y[souscouche], 4)
                GCODE += "G1 F33000 X"+str(x[0])+" Y"+str(y[0])+" ; Layer "+str(couche)+ \
                        "/"+str(self.Nlayers)+" - Sub Layer "+str(souscouche+1)+"/"+str(len(self.X))+"\n"
                for i in range(1,len(x)):
                    GCODE += "G1 X"+str(x[i])+" Y"+str(y[i])+"\n"
                GCODE += "\n"
        return(GCODE)