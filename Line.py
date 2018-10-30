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
        ax.plot([vertex1[0],vertex2[0]],[vertex1[1],vertex2[1]],[vertex1[2],vertex2[2]], c = 'b');
        return;

    def drawDefLine(self,ax):
        vertex1 = np.array(self.vertexSource.vertexPosition);
        vertex2 = np.array(self.newVertexSignaled.vertexPosition);
        ax.plot([vertex1[0],vertex2[0]],[vertex1[1],vertex2[1]],[vertex1[2],vertex2[2]], c = 'r');
        return;

    def scaleLine(self, length):
        PointO = np.array(self.vertexSource.vertexPosition);
        PointD = np.array(self.vertexSignaled.vertexPosition);
        dist = np.linalg.norm(PointO - PointD);
        print( "Distance: " + str(dist));
        print( "Vec: " + str(PointO - PointD));
        vecToScale = PointD - PointO;
        self.scaleVector(vecToScale,length);
        print( "Scaled Vec: " + str(vecToScale));
        PointDnew = PointO +vecToScale;
        idNew = self.vertexSignaled.vertexID;
        self.newVertexSignaled = Vertex(self.vertexSource.numOfVertices, PointDnew, idNew);


    def scaleVector(self, vectorScale, size):
        print("Scale size: "+ str(size));
        print("Vector to scale: "+str(vectorScale));
        alpha = size/LA.norm(vectorScale);
        for x in range(len(vectorScale)):
                vectorScale[x]=alpha*vectorScale[x];
                print(" Scaled Component: "+str(vectorScale[x]));
        return;
