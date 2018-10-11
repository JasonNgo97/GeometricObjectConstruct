import numpy as np
import random
import math
from Vertex import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy.optimize import fmin
from numpy import linalg as LA

class Line:
    vertexSource = None;
    # This vertex is on the bottom
    vertexSignaled = None;
    #This is the vertex of the top
    newVertexSignaled = None;
    #This is the vertex with its position adjusted

    def __init__(self,vertexSource,vertexSignaled):
        self.vertexSource = vertexSource;
        self.vertexSignaled = vertexSignaled;

    def drawLine(self,ax):
        vertex1 = np.array(self.vertexSource.vertexPosition);
        vertex2 = np.array(self.vertexSignaled.vertexPosition);
        ax.plot([vertex1[0],vertex2[0]],[vertex1[1],vertex2[1]],[vertex1[2],vertex2[2]]);
        return;
